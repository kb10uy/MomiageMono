#!/usr/bin/env bash

python3 "scripts/momiage-mono.py"

nerd-fonts/font-patcher -c -out "dist" "dist/MomiageMono-Regular.ttf"
mv "dist/MomiageMono-Regular Nerd Font Complete.ttf" "dist/MomiageMono-NerdFont.ttf"
