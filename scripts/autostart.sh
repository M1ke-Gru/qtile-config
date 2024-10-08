#!/bin/bash

function run {
	if ! pgrep $1; then
		$@ &
	fi
}

#starting utility applications at boot time
lxsession &
run nm-applet &
run pamac-tray &
numlockx on &
blueman-applet &
#flameshot &
#picom --config $HOME/.config/picom/picom.conf &
picom --config .config/picom/picom.conf --experimental-backends &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
# feh --randomize --bg-fill /usr/share/wallpapers/garuda-wallpapers/*
feh --bg-fill ~/Bilder/nord-theme-city-lights-building-night-street-light-hd-wallpaper-preview.jpg
#starting user applications at boot time
run volumeicon &
#run discord &
#nitrogen --random --set-zoom-fill &
#run caffeine -a &
#run vivaldi-stable &
#run firefox &
#run thunar &
#run dropbox &
#run insync start &
#run spotify &
#run atom &
#run telegram-desktop &
