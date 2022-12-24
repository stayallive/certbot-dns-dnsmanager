# [Certbot](https://certbot.eff.org/) [dnsmanager.io](https://app.dnsmanager.io?ref=certbot-dns-dnsmanager) plugin

[![Snap Store Badge](https://snapcraft.io/certbot-dns-dnsmanager/badge.svg?version=latest)](https://snapcraft.io/certbot-dns-dnsmanager)
[![PyPI Version Badge](https://img.shields.io/pypi/v/certbot-dns-dnsmanager)](https://pypi.org/project/certbot-dns-dnsmanager/)

This plugin enables DNS verification with [Certbot](https://certbot.eff.org/) when using [dnsmanager.io](https://app.dnsmanager.io?ref=certbot-dns-dnsmanager).

## Installation

If you installed certbot as a snap, then you have to install this plugin as a snap as well:

```bash
snap install certbot-dns-dnsmanager
snap set certbot trust-plugin-with-root=ok
snap connect certbot:plugin certbot-dns-dnsmanager
```

and can be upgraded using the `refresh` command:

```bash
snap refresh certbot-dns-dnsmanager
```

Alternatively this package can be installed with pip:

```bash
pip install certbot-dns-dnsmanager
```

and can be upgraded using the `--upgrade` flag

```bash
pip install --upgrade certbot-dns-dnsmanager
```

## Credentials

You need to supply Certbot with your `dnsmanager.io` API credentials, this is an example of how a credentials file can look:

```ini
# dnsmanager.io API credentials used by Certbot
dns_dnsmanager_api_id = 4b968ab4-b30b-4376-898d-659b3e8b9028
dns_dnsmanager_api_key = DprstzDtrGXUUVb5X8AThDOLdmpyPCqw
```

You can create a new set of API credentials in your [dnsmanager.io account](https://app.dnsmanager.io/account/api/keys?ref=certbot-dns-dnsmanager).

Keep in mind that the credentials file should be readable only by the user running Certbot and the credentials cannot be scoped, so they can be used to perform any action on your behalf if compromised.

## Examples

Simple example for a single domain:

```bash
certbot certonly \
  --authenticator dns-dnsmanager \
  --dns-dnsmanager-credentials ~/.secrets/dnsmanager.ini \
  -d example.com
```

Simple example for wildcard domain:

```bash
certbot certonly \
  --authenticator dns-dnsmanager \
  --dns-dnsmanager-credentials ~/.secrets/dnsmanager.ini \
  -d example.com \
  -d *.example.com
```

Example changing the propagation delay, although you should not have to
adjust it normally:

```bash
certbot certonly \
  --authenticator dns-dnsmanager \
  --dns-dnsmanager-credentials ~/.secrets/dnsmanager.ini \
  --dns-dnsmanager-propagation-seconds 120 \
  -d example.com
```

## Security Vulnerabilities

If you discover a security vulnerability, please send an e-mail to Alex Bouma at `alex+security@bouma.me`. All security vulnerabilities will be swiftly addressed.
