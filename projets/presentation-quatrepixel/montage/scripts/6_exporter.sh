#!/usr/bin/env bash
# Export final : UN seul encodage avec perte, à partir du master 4K sans perte rendu par HyperFrames
# et du son sans perte (mix.wav). Sorties : ../../export/quatrepixel_presentation.mp4 (1080x1920)
# et ../../export/quatrepixel_presentation_4K.mp4 (2160x3840).
#
# Master : cd ../hyperframes && npx hyperframes@0.8.185 render --resolution portrait-4k -f 30 -q delivery \
#            --crf 0 --video-frame-format png -o <master_4k.mp4>
set -euo pipefail
cd "$(dirname "$0")"
MASTER=${1:?chemin du master 4K sans perte}
MIX=../hyperframes/assets/audio/mix.wav
OUT=../../export
mkdir -p "$OUT"
X264="-c:v libx264 -preset slow -pix_fmt yuv420p -profile:v high -movflags +faststart"
# 4K : -crf 14 (≈ 28 Mb/s). 1080 : -crf 14 ne donnait que ≈ 10 Mb/s ; -crf 10 (meilleur) pour dépasser 15 Mb/s.
AAC="-c:a aac -b:a 320k -ar 48000 -ac 2"

ffmpeg -v error -y -i "$MASTER" -i "$MIX" -map 0:v -map 1:a \
  -vf "scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int" -r 30 $X264 -crf 10 -level 4.2 $AAC -shortest \
  "$OUT/quatrepixel_presentation.mp4"
[ "${SANS_4K:-0}" = 1 ] || ffmpeg -v error -y -i "$MASTER" -i "$MIX" -map 0:v -map 1:a \
  -r 30 $X264 -crf 14 -level 5.2 $AAC -shortest \
  "$OUT/quatrepixel_presentation_4K.mp4"
for f in "$OUT"/quatrepixel_presentation*.mp4; do
  echo "$f : $(ffprobe -v error -show_entries format=duration,bit_rate -of csv=p=0 "$f")"
done
