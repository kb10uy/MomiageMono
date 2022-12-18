#!/usr/bin/env bash
set -e

rm -rf "fonts"

mkdir -p "fonts/mplus2"
pushd "fonts/mplus2"
    wget -O "mplus2.zip" "https://fonts.google.com/download?family=M%20PLUS%202"
    unzip -j "mplus2.zip" "static/*"
popd

mkdir -p "fonts/source-han-sans"
pushd "fonts/source-han-sans"
    wget -O "source-han-sans.zip" "https://github.com/adobe-fonts/source-han-sans/releases/download/2.004R/SourceHanSansJ.zip"
    unzip -j "source-han-sans.zip" "OTF/Japanese/*"
popd

mkdir -p "fonts/jetbrains-mono"
pushd "fonts/jetbrains-mono"
    wget -O "jetbrains-mono.zip" "https://fonts.google.com/download?family=JetBrains%20Mono"
    unzip -j "jetbrains-mono.zip" "static/*"
popd
