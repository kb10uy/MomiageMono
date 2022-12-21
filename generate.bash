#!/usr/bin/env bash
set -e

rm -rf dist/*

python3 "scripts/momiage-mono.py"

pushd "dist"
    for filename in *.ttf; do
        subfamily=$(echo $filename | sed -E 's/.+-(.+)\.ttf/\1/')
        subfamily_separated=$(echo $subfamily | sed -E 's/([a-z])([A-Z])/\1 \2/g')

        ../nerd-fonts/font-patcher -c $filename
        mv "Momiage Mono ${subfamily_separated} Nerd Font Complete.ttf" "MomiageMono-${subfamily}-NerdFont.ttf"

        zip "package.zip" $filename "MomiageMono-${subfamily}-NerdFont.ttf"
    done

    zip -j "package.zip" "../LICENSE"
popd
