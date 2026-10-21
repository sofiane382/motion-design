#!/usr/bin/env bash
# Prépare les plans vidéo du montage : coupe, vitesse (image + son), retrait du logo « Ai »,
# mise en 1080x1920 à 30 i/s, son AAC 48 kHz stéréo. Sortie : ../hyperframes/assets/plans/
set -euo pipefail
cd "$(dirname "$0")"
SRC=../../sources
OUT=../hyperframes/assets/plans
mkdir -p "$OUT"

# Le logo « Ai » est vers x 60-150, y 60-140 en 2160x3840 : delogo sur le ciel.
DELOGO="delogo=x=36:y=36:w=140:h=124"

# plan  source  début  fin  vitesse  gain (dB : les plans calmes sont quasi muets, on remonte leur ambiance)
plan() {
  local nom=$1 src=$2 debut=$3 fin=$4 vit=$5 gain=${6:-0}
  local trim="trim=start=$debut" atrim="atrim=start=$debut"
  if [ "$fin" != "fin" ]; then trim="$trim:end=$fin"; atrim="$atrim:end=$fin"; fi
  ffmpeg -v error -y -i "$SRC/$src" -filter_complex "
    [0:v]$trim,setpts=(PTS-STARTPTS)/$vit,$DELOGO,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v];
    [0:a]$atrim,asetpts=PTS-STARTPTS,atempo=$vit,volume=${gain}dB,aresample=48000,aformat=channel_layouts=stereo[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 14 -g 15 -c:a aac -b:a 256k -shortest \
    -movflags +faststart "$OUT/$nom.mp4"
  echo "$nom : $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$nom.mp4") s"
}

plan p01_calme      clip_1.mp4 0    fin  1.9  14
plan p02_ennui      clip_2.mp4 0    3.13 1.25 16
plan p04_lecture    clip_2.mp4 3.13 fin  1    14
plan p06_tete       clip_3.mp4 1.0  fin  1.25
plan p07_zbeul      clip_4.mp4 0    fin  1
plan p08_airpods    clip_5.mp4 0    fin  1
plan p09_calme_apres clip_6.mp4 0   3.5  1    18
