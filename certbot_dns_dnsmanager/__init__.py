"""
The `~certbot_dns_dnsmanager.dns_dnsmanager` plugin automates the process of
completing a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and
subsequently removing, TXT records using the `dnsmanager.io`_ API.

.. _dnsmanager.io: https://app.dnsmanager.io?ref=certbot-dns-dnsmanager

.. note::
   The plugin is not installed by default.

Installation
------------

If you followed the official instructions, you likely installed certbot as a
snap. In that case, you can install the plugin by running:

.. code:: bash

    snap install certbot-dns-dnsmanager
    snap connect certbot:plugin certbot-dns-dnsmanager

Alternatively, you can install certbot using pip and install the plugin by
running:

.. code:: bash

    pip install certbot-dns-dnsmanager

Named Arguments
---------------

========================================  =====================================
``--dns-dnsmanager-credentials``          dnsmanager.io credentials_ INI file. (Required)
``--dns-dnsmanager-propagation-seconds``  The number of seconds to wait for DNS
                                          to propagate before asking the ACME
                                          server to verify the DNS record. (Default: 120)
========================================  =====================================


Credentials
-----------

Use of this plugin requires a configuration file containing dnsmanager.io API
credentials, obtained from your
`dnsmanager.io account <https://app.dnsmanager.io/account/api/keys>`_.

dnsmanager.io credentials are not scoped and give access to all account features.

.. code-block:: ini
   :name: certbot_dnsmanager_credentials.ini
   :caption: Example credentials file:

   # dnsmanager.io API credentials used by Certbot
   dns_dnsmanager_api_id = 4b968ab4-b30b-4376-898d-659b3e8b9028
   dns_dnsmanager_api_key = DprstzDtrGXUUVb5X8AThDOLdmpyPCqw

The path to this file can be provided interactively or using the
``--dns-dnsmanager-credentials`` command-line argument. Certbot records the path
to this file for use during renewal, but does not store the file's contents.

.. caution::
   You should protect these API credentials as you would the password to your
   dnsmanager.io account. Users who can read this file can use these credentials
   to issue arbitrary API calls on your behalf. Users who can cause Certbot to
   run using these credentials can complete a ``dns-01`` challenge to acquire
   new certificates or revoke existing certificates for associated domains,
   even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).


Examples
--------

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``

   certbot certonly \\
     --authenticator dns-dnsmanager \\
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \\
     -d example.com

.. code-block:: bash
   :caption: To acquire a single certificate for both ``example.com`` and
             ``www.example.com``

   certbot certonly \\
     --authenticator dns-dnsmanager \\
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \\
     -d example.com \\
     -d www.example.com

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``, waiting 60 seconds
             for DNS propagation

   certbot certonly \\
     --authenticator dns-dnsmanager \\
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \\
     --dns-dnsmanager-propagation-seconds 60 \\
     -d example.com

"""
