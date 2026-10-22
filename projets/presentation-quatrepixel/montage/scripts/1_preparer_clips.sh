#!/usr/bin/env bash
# Prépare les plans vidéo du montage, SANS PERTE et en pleine définition (2160x3840, 30 i/s) :
# coupe, vitesse, retrait du logo « Ai ». Vidéo en H.264 -crf 0 (sans perte), son à part en WAV 48 kHz stéréo
# (accéléré avec atempo pour rester synchro). Sortie : ../hyperframes/assets/plans/
# Le seul encodage avec perte est l'export final (scripts/6_exporter.sh).
set -euo pipefail
cd "$(dirname "$0")"
SRC=../../sources
OUT=../hyperframes/assets/plans
mkdir -p "$OUT"

# Logo « Ai » vers x 60-150, y 60-140 en 2160x3840 : delogo sur le ciel (vérifié en zoom, pas de tache).
DELOGO="delogo=x=36:y=36:w=140:h=124,"

# plan  source  début  fin  vitesse  gain_dB  logo(1/0)
plan() {
  local nom=$1 src=$2 debut=$3 fin=$4 vit=$5 gain=$6 logo=$7
  local trim="trim=start=$debut" atrim="atrim=start=$debut"
  if [ "$fin" != "fin" ]; then trim="$trim:end=$fin"; atrim="$atrim:end=$fin"; fi
  local dl=""; [ "$logo" = 1 ] && dl="$DELOGO"
  ffmpeg -v error -y -i "$SRC/$src" -filter_complex "
    [0:v]$trim,setpts=(PTS-STARTPTS)/$vit,fps=30,${dl}scale=2160:3840:flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p[v]" \
    -map "[v]" -an -c:v libx264 -preset veryfast -crf 0 -g 30 "$OUT/$nom.mp4"
  local d; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$nom.mp4")
  # Son à la même durée exacte que l'image (complété par du silence si besoin).
  ffmpeg -v error -y -i "$SRC/$src" -af "$atrim,asetpts=PTS-STARTPTS,atempo=$vit,volume=${gain}dB,aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo,apad,atrim=end=$d" \
    -c:a pcm_s16le "$OUT/$nom.wav"
  echo "$nom : $d s"
}

# Les plans calmes sont quasi muets à la source (-45 à -53 dB) : on remonte leur ambiance (vent).
plan p01_calme       clip_1.mp4 0.5  fin  1.9  14 1
plan p02_ennui       clip_2.mp4 0.2  3.13 1.25 16 1
plan p04_lecture     clip_2.mp4 3.13 fin  1    14 1
plan p06_tete        clip_3.mp4 1.0  fin  1.25 0  1
plan p07_zbeul       clip_4.mp4 0    fin  1    -2 0
plan p08_airpods_src clip_5.mp4 0    fin  1    -2 1
plan p09_calme_src   clip_6.mp4 0    3.5  1    18 0
