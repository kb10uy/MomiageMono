#!/usr/bin/env bash

python3 "scripts/momiage-mono.py"

nerd-fonts/font-patcher -c -out "dist" "dist/MomiageMono-Regular.ttf"
nerd-fonts/font-patcher -c -out "dist" "dist/MomiageMono-Italic.ttf"
nerd-fonts/font-patcher -c -out "dist" "dist/MomiageMono-Bold.ttf"
nerd-fonts/font-patcher -c -out "dist" "dist/MomiageMono-BoldItalic.ttf"
mv "dist/Momiage Mono Regular Nerd Font Complete.ttf" "dist/MomiageMono-Regular-NerdFont.ttf"
mv "dist/Momiage Mono Italic Nerd Font Complete.ttf" "dist/MomiageMono-Italic-NerdFont.ttf"
mv "dist/Momiage Mono Bold Nerd Font Complete.ttf" "dist/MomiageMono-Bold-NerdFont.ttf"
mv "dist/Momiage Mono Bold Italic Nerd Font Complete.ttf" "dist/MomiageMono-BoldItalic-NerdFont.ttf"
