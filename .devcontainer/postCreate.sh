#!/bin/sh
sudo chown -R abdelrahman:abdelrahman /home/mount
sudo chown abdelrahman .pixi
export PATH="/home/abdelrahman/.pixi/bin:${PATH}"
pixi install
