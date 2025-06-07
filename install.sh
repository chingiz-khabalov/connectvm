#!/bin/bash

echo "Installing connectvm"

echo "Copying files"

cp ./main.py ~/.local/bin/connectvm
mkdir -p ~/.config/connectvm
cp ./bash_completion ~/.config/connectvm/completion
chmod 744 ~/.config/connectvm/completion

echo "OK"

echo "Adding source command to ~/.bashrc file"
echo "source ~/.config/connectvm/completion" >> ~/.bashrc
echo "export PATH=~/.local/bin/:$PATH" >> ~/.bashrc
source "$HOME/.bashrc"

echo "OK"

echo "Installing is complete"
