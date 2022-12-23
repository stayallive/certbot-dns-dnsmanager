dnsmanager.io DNS Authenticator Plugin for Certbot
==================================================

.. image:: https://img.shields.io/github/license/stayallive/certbot-dns-dnsmanager?style=for-the-badge
    :alt: License Badge
    :target: LICENSE

.. image:: https://img.shields.io/pypi/v/certbot-dns-dnsmanager?style=for-the-badge
    :alt: PyPI Version Badge
    :target: https://pypi.org/project/certbot-dns-dnsmanager/

.. image:: https://img.shields.io/pypi/pyversions/certbot-dns-dnsmanager?style=for-the-badge
    :alt: Supported Python Versions Badge
    :target: https://pypi.org/project/certbot-dns-dnsmanager/

.. image:: https://readthedocs.org/projects/certbot-dns-dnsmanager/badge/?version=latest&style=for-the-badge
    :alt: Documentation Badge
    :target: https://certbot-dns-dnsmanager.readthedocs.io/en/latest/

.. image:: https://flat.badgen.net/snapcraft/v/certbot-dns-dnsmanager/?scale=1.4
    :alt: Snap Store Badge
    :target: https://snapcraft.io/certbot-dns-dnsmanager

This plugin enables DNS verification with certbot when using `dnsmanager.io`_ DNS. Full documentation is on `Read the Docs`_.

.. _dnsmanager.io: https://app.dnsmanager.io?ref=certbot-dns-dnsmanager
.. _Read the Docs: https://certbot-dns-dnsmanager.readthedocs.io/en/latest/

Installation
------------

This package can be installed with pip

.. code:: bash

    pip install certbot-dns-dnsmanager

and can be upgraded using the ``--upgrade`` flag

.. code:: bash

    pip install --upgrade certbot-dns-dnsmanager

If you installed certbot as a snap, then you have to install this plugin as a snap as well.

.. code:: bash

    snap install certbot-dns-dnsmanager
    snap connect certbot:plugin certbot-dns-dnsmanager

Credentials
-----------

.. code:: ini
   :name: certbot_dnsmanager_credentials.ini

   # dnsmanager.io API credentials used by Certbot
   dns_dnsmanager_api_id = 4b968ab4-b30b-4376-898d-659b3e8b9028
   dns_dnsmanager_api_key = DprstzDtrGXUUVb5X8AThDOLdmpyPCqw

Examples
--------

.. code:: bash

   certbot certonly \
     --authenticator dns-dnsmanager \
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \
     -d example.com

.. code:: bash

   certbot certonly \
     --authenticator dns-dnsmanager \
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \
     -d example.com \
     -d www.example.com

.. code:: bash

   certbot certonly \
     --authenticator dns-dnsmanager \
     --dns-dnsmanager-credentials ~/.secrets/certbot/dnsmanager.ini \
     --dns-dnsmanager-propagation-seconds 60 \
     -d example.com
