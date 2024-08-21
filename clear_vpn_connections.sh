#!/bin/bash

for conn in $(nmcli --fields UUID,TYPE connection show | grep vpn | awk '{print $1}'); do
    nmcli connection delete "$conn";
done

