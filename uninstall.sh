#!/usr/bin/bash

echo "removing script"
rm /usr/local/bin/connectvm
echo "OK"

echo "removing config folder"
rm -r ~/.config/connectvm
echo "OK"

echo "removing sourcing from bashrc"
sed -i "/source ~\/.config\/connectvm\/completion/d" ~/.bashrc
sed -i "export PATH=~\/.local\/bin\/:$PATH/d" ~/.bashrc
echo "OK"

echo "connectvm with its config files has been removed from your system, don't forget to delete this installation directory"
