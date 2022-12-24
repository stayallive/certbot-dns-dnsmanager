#!/bin/bash

for snap in certbot-dns-dnsmanager_*.snap; do
  snapcraft upload --release=stable $snap
done
