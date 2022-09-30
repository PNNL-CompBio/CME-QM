#!/bin/bash

# for reference: https://unix.stackexchange.com/a/603250/304490
#mkdir -p /mnt/anub229_msshare/
mount -t cifs -o vers=3.0,username=anub229 //pnl.gov/Projects/MSSHARE/Anubhav /mnt/anub229_msshare/anubhav
mkdir -p /mnt/anub229_msshare/anubhav
mount /mnt/anub229_msshare/anubhav
~