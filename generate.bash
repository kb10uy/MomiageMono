#!/usr/bin/env bash
set -e

rm -rf dist/*

python3 "scripts/momiage-mono.py"

pushd "dist"
    for filename in *.ttf; do
        subfamily=$(echo $filename | sed -E 's/.+-(.+)\.ttf/\1/')

        ../fonts/nerd-fonts-patcher/font-patcher -c $filename
        mv "MomiageMonoNerdFont-${subfamily}.ttf" "MomiageMono-${subfamily}-NerdFont.ttf"

        zip "package.zip" $filename "MomiageMono-${subfamily}-NerdFont.ttf"
    done

    zip -j "package.zip" "../LICENSE"
popd
