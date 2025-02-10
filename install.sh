#!/bin/bash

mkdir -p ~/.local/bin
cp ./main.py ~/.local/bin/connectvm
mkdir -p ~/.config/connectvm
cp ./bash_completion ~/.config/connectvm/completion
chmod 744 ~/.config/connectvm/completion
echo "source ~/.config/connectvm/completion" >> ~/.bashrc
