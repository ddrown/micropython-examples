#!/bin/sh

for i in 1 2 3 4 5 6 7 8 9 0; do
  magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:$i $i.pbm
done

magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:: colon.pbm
magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:. dot.pbm
magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:- dash.pbm
