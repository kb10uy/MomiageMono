#!/usr/bin/env bash
set -e

mkdir -p "fonts/gen-ei-mono-go"
pushd "fonts/gen-ei-mono-go"
    if [[ ! -f "GenEiMonoGothic_v1.0.zip" ]]; then
        echo "You have to download \"GenEiMonoGothic_v1.0.zip\" manually."
        echo "https://okoneya.jp/font/genei-mono-go.html"
    else
        unzip -j "GenEiMonoGothic_v1.0.zip" "GenEiMonoGothic_v1.0/GenEiMonoGothic-*.ttf"
    fi
popd

mkdir -p "fonts/jetbrains-mono"
pushd "fonts/jetbrains-mono"
    wget -O "jetbrains-mono.zip" "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.242/JetBrainsMono-2.242.zip"
    unzip -j "jetbrains-mono.zip" "fonts/ttf/*"
popd

mkdir -p "dist"
