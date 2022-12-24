import os
import sys

from setuptools import find_packages
from setuptools import setup

version = "0.0.6"

install_requires = [
    "requests>=2.25.1",
    "setuptools>=41.6.0",
]

if not os.environ.get("SNAP_BUILD"):
    install_requires.extend(
        [
            # We specify the minimum acme and certbot version as the current plugin
            # version for simplicity. See
            # https://github.com/certbot/certbot/issues/8761 for more info.
            f"acme>={version}",
            f"certbot>={version}",
        ]
    )
# Snap Core20 Python Plugin is using 'pip install -U .' to build the package.
# PEP 517 builds do not fall back to 'setup.py install' - which is deprecated -
# as pip does for non-PEP 517 builds.
# The following error which was taken from the original certbot dns plugins thus
# always leads to a failed snap build. It is merely a sanity check to ensure
# SNAP_BUILD is not set if actually building a Python wheel for e.g. PyPi and
# not really required. It is kept for completeness and as a reminder to check
# for what kind of replacement the certbot community comes up with.
#
# elif 'bdist_wheel' in sys.argv[1:]:
#    raise RuntimeError('Unset SNAP_BUILD when building wheels '
#                        'to include certbot dependencies.')
if os.environ.get("SNAP_BUILD"):
    install_requires.append("packaging")

# Load readme to use on PyPI
with open("README.md", encoding="utf8") as f:
    readme = f.read()

setup(
    name="certbot-dns-dnsmanager",
    version=version,
    description="dnsmanager.io DNS Authenticator plugin for Certbot",
    url="https://github.com/stayallive/certbot-dns-dnsmanager",
    author="Alex Bouma",
    author_email="alex+certbot-dns-dnsmanager@bouma.me",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-dnsmanager = certbot_dns_dnsmanager.dns_dnsmanager:Authenticator",
        ],
    },
)
