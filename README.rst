dnsmanager.io DNS Authenticator Plugin for Certbot
==================================================

.. image:: https://snapcraft.io/certbot-dns-dnsmanager/badge.svg?version=latest
    :alt: Snap Store Badge
    :target: https://snapcraft.io/certbot-dns-dnsmanager

.. image:: https://img.shields.io/pypi/v/certbot-dns-dnsmanager
    :alt: PyPI Version Badge
    :target: https://pypi.org/project/certbot-dns-dnsmanager/

This plugin enables DNS verification with certbot when using `dnsmanager.io`_.

.. _dnsmanager.io: https://app.dnsmanager.io?ref=certbot-dns-dnsmanager

Installation
------------

If you installed certbot as a snap, then you have to install this plugin as a snap as well.

.. code:: bash

    snap install certbot-dns-dnsmanager
    snap set certbot trust-plugin-with-root=ok
    snap connect certbot:plugin certbot-dns-dnsmanager

and can be upgraded using the ``refresh`` command:

.. code:: bash

    snap refresh certbot-dns-dnsmanager

Alternatively this package can be installed with pip:

.. code:: bash

    pip install certbot-dns-dnsmanager

and can be upgraded using the ``--upgrade`` flag

.. code:: bash

    pip install --upgrade certbot-dns-dnsmanager

Credentials
-----------

You need to supply certbot with your ``dnsmanager.io`` API credentials, this is an example:

.. code:: ini
   :name: certbot_dnsmanager_credentials.ini

   # dnsmanager.io API credentials used by Certbot
   dns_dnsmanager_api_id = 4b968ab4-b30b-4376-898d-659b3e8b9028
   dns_dnsmanager_api_key = DprstzDtrGXUUVb5X8AThDOLdmpyPCqw

Examples
--------

Simple example for a single domain:

.. code:: bash

   certbot certonly \
     --authenticator dns-dnsmanager \
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \
     -d example.com

Simple example for wildcard domain:

.. code:: bash

   certbot certonly \
     --authenticator dns-dnsmanager \
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \
     -d example.com \
     -d *.example.com

Example changing the propagation delay, although you should not have to adjust it normally:

.. code:: bash

   certbot certonly \
     --authenticator dns-dnsmanager \
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \
     --dns-dnsmanager-propagation-seconds 120 \
     -d example.com
