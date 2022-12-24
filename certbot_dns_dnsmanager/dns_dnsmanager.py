"""DNS Authenticator for dnsmanager.io DNS."""
import logging
from base64 import b64encode
from typing import Any
from typing import Callable
from typing import Tuple
from typing import Optional

import requests

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)

CREDENTIAL_URL = "https://app.dnsmanager.io/account/api/keys"


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for dnsmanager.io

    This Authenticator uses the dnsmanager.io API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using dnsmanager.io for DNS)."

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(
            cls, add: Callable[..., None], default_propagation_seconds: int = 120
    ) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="dnsmanager.io credentials INI file.")

    def more_info(self) -> str:
        return "This plugin configures a DNS TXT record to respond to a dns-01 challenge using the dnsmanager.io API."

    def _validate_credentials(self, credentials: CredentialsConfiguration) -> None:
        api_id = credentials.conf("api-id")
        api_key = credentials.conf("api-key")
        if not api_id or not api_key:
            raise errors.PluginError(
                "{}: api-id and api-key required for authentication (see {})".format(
                    credentials.confobj.filename, CREDENTIAL_URL
                )
            )

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "dnsmanager.io credentials INI file",
            None,
            self._validate_credentials,
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_dnsmanager_client().add_txt_record(
            domain, validation_name, validation
        )

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_dnsmanager_client().del_txt_record(domain, validation_name, validation)

    def _get_dnsmanager_client(self) -> "_DnsmanagerClient":
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return _DnsmanagerClient(self.credentials.conf("api-id"), self.credentials.conf("api-key"))


class _DnsmanagerClient:
    """
    Encapsulates all communication with the dnsmanager.io API.
    """

    def __init__(self, api_id: str, api_key: str) -> None:
        token = b64encode(f"{api_id}:{api_key}".encode('utf-8')).decode("ascii")
        self.headers = {"Accept": "application/json", "Authorization": f'Basic {token}'}

    def add_txt_record(
            self, domain: str, record_name: str, record_content: str
    ) -> None:
        """
        Add a TXT record using the supplied information.

        :param str domain: The domain to use to look up the dnsmanager.io domain ID.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises certbot.errors.PluginError: if an error occurs communicating with the dnsmanager.io API
        """

        domain_id, domain_name = self._find_domain_id(domain)

        # Set content type because we are posting
        post_headers = self.headers
        post_headers["Content-Type"] = "application/json"

        # Check if record_name contains zone_name (it should) and remove it
        if record_name.endswith(domain_name):
            record_name = record_name[: -(len(domain_name) + 1)]

        payload = {
            "type": "TXT",
            "name": record_name,
            "content": record_content,
        }

        response = requests.put(
            f"https://api.dnsmanager.io/api/v1/user/domain/{domain_id}/records",
            json=payload,
            headers=post_headers,
        )
        logger.debug("Attempting to add record to zone %s: %s", domain_id, payload)

        if response.status_code != 200:
            raise errors.PluginError(
                f"API error ({response.status_code}): {response.text}"
            )

        record_id = self._find_txt_record_id(domain_id, domain_name, record_name, record_content)
        logger.debug("Successfully added TXT record with record_id: %s", record_id)

    def del_txt_record(
            self, domain: str, record_name: str, record_content: str
    ) -> None:
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain: The domain to use to look up the dnsmanager.io domain ID.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """

        try:
            domain_id, domain_name = self._find_domain_id(domain)
        except errors.PluginError as e:
            logger.debug("Encountered error finding domain_id during deletion: %s", e)
            return

        # Check if record_name contains zone_name (it should) and remove it
        if record_name.endswith(domain_name):
            record_name = record_name[: -(len(domain_name) + 1)]

        if domain_id:
            record_id = self._find_txt_record_id(domain_id, domain_name, record_name, record_content)
            if record_id:
                response = requests.delete(
                    f"https://api.dnsmanager.io/api/v1/user/domain/{domain_id}/record/{record_id}",
                    headers=self.headers,
                )
                if response.status_code != 200:
                    logger.error(
                        "API error (%s): %s", response.status_code, response.text
                    )
            else:
                logger.debug("TXT record not found; no cleanup needed.")
        else:
            logger.debug("Zone not found; no cleanup needed.")

    def _find_domain_id(self, domain: str) -> Tuple[str, str]:
        """
        Find the domain ID for a given domain name.

        :param str domain: The domain name for which to find the ID.
        :returns: The ID, if found.
        :rtype: tuple(str, str)
        :raises certbot.errors.PluginError: if no domain is found.
        """

        zone_name_guesses = dns_common.base_domain_name_guesses(domain)

        for zone_name_guess in zone_name_guesses:
            # Test if zone_name_guess contains a `.` otherwise skip it
            if "." not in zone_name_guess:
                continue

            # We prepend the query with a `!` to force an exact match
            response = requests.get(
                f"https://api.dnsmanager.net/api/v1/user/domains?query=!{zone_name_guess}",
                headers=self.headers,
            )

            if response.status_code != 200:
                raise errors.PluginError(
                    f"API error ({response.status_code}): {response.text}"
                )

            response = response.json()
            if len(response["results"]) == 1:
                return response["results"][0]["id"], zone_name_guess

        raise errors.PluginError("Could not find domain in account.")

    def _find_txt_record_id(
            self, domain_id: str, domain_name: str, record_name: str, record_content: str
    ) -> Optional[str]:
        """
        Find the record_id for a TXT record with the given name and content.

        :param str domain_id: The domain_id which contains the record.
        :param str domain_name: The domain name.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :returns: The record_id, if found.
        :rtype: str
        """

        # Check if record_name contains zone_name (it should) and remove it
        if record_name.endswith(domain_name):
            record_name = record_name[: -(len(domain_name) + 1)]

        response = requests.get(
            f"https://api.dnsmanager.io/api/v1/user/domain/{domain_id}/records?query=!{record_name}",
            headers=self.headers
        )

        if response.status_code != 200:
            raise errors.PluginError(
                f"API error ({response.status_code}): {response.text}"
            )

        # Iterate through records and find the TXT record with the right name and value
        for record in response.json()["results"]:
            if (
                    record["type"] == "TXT"
                    and record["name"] == record_name
                    and record["content"] == record_content
            ):
                return record["id"]

        logger.debug("Unable to find TXT record.")
        return None
