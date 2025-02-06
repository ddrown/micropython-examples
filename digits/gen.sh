#!/bin/bash

# For Fedora imagemagick (7.1.1-41):

for i in {0..9} {a..z}; do
  magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:$i $i.pbm
done

magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:: colon.pbm
magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:. dot.pbm
magick -background black -fill white -font /usr/share/fonts/dejavu-serif-fonts/DejaVuSerif-Bold.ttf -pointsize 36 label:- dash.pbm

# For Ubuntu imagemagick (6.9.13-12):
# convert -background black -fill white -font /usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf -pointsize 36 label:0 0.pbm
