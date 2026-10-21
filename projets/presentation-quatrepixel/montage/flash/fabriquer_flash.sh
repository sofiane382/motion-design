#!/usr/bin/env bash
# Flash blanc + sifflement d'oreille (acouphène) pour la coupe après le plan AirPods.
set -euo pipefail
cd "$(dirname "$0")"
# Sifflement : sinus 2,6 kHz avec un léger tremblement, assez bas pour ne pas faire mal, qui s'éteint en 3 s.
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.16*sin(2*PI*2600*t)*(1+0.08*sin(2*PI*6*t))*exp(-0.55*t)':s=48000:d=3" \
  -af "afade=t=in:d=0.02,afade=t=out:st=2.2:d=0.8" -ac 2 sifflement_3s.wav
# Coup sourd au moment de la coupe : grave qui s'éteint vite.
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.5*sin(2*PI*55*t)*exp(-9*t)':s=48000:d=0.6" -ac 2 coup.wav
ffmpeg -v error -y -i coup.wav -i sifflement_3s.wav -filter_complex "[0][1]amix=inputs=2:duration=longest:normalize=0" -ac 2 son_flash_3s.wav
# Vidéo : 0,6 s de blanc pur en 9:16 avec le coup + le début du sifflement.
ffmpeg -v error -y -f lavfi -i "color=c=white:s=720x1280:r=24:d=0.6" -i son_flash_3s.wav \
  -map 0:v -map 1:a -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest flash_blanc_0-6s.mp4
# Le reste du sifflement (après les 0,6 s) à poser sous le début du plan calme.
ffmpeg -v error -y -ss 0.6 -i son_flash_3s.wav -c:a aac -b:a 192k sifflement_suite_2-4s.m4a
rm coup.wav sifflement_3s.wav
