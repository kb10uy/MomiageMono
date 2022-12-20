#!/usr/bin/env bash

python3 "scripts/momiage-mono.py"

nerd-fonts/font-patcher -c -out "dist" "dist/MomiageMono-Regular.ttf"
nerd-fonts/font-patcher -c -out "dist" "dist/MomiageMono-Bold.ttf"
mv "dist/MomiageMono-Regular Nerd Font Complete.ttf" "dist/MomiageMono-Regular-NerdFont.ttf"
mv "dist/MomiageMono-Bold Nerd Font Complete.ttf" "dist/MomiageMono-Bold-NerdFont.ttf"
