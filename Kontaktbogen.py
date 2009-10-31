from __future__ import division
import PngImagePlugin
import JpegImagePlugin
import IptcImagePlugin as IPTC
import Image
import glob, os
import ImageFont, ImageDraw, ImageChops, ImageStat, ImageEnhance
import string
import sys


def make_border(im, width):
  border_width = width
  bw = border_width
  w = im.size[0]
  h = im.size[1]
  border_col = (0,0,0)
  draw = ImageDraw.Draw(im)
  begin = (0, 0)
  end = (w, 0)
  try:
    draw.line((begin ,end), fill=border_col, width=border_width)
  except:
    border_col = (0)
    draw.line((begin ,end), fill=border_col, width=border_width)
  
  begin = (-1, 0)
  end = (-1, h)
  draw.line((begin ,end), fill=border_col, width=border_width)
  begin = (w, 0)
  end = (w, h )
  draw.line((begin ,end), fill=border_col, width=border_width)
  begin = (0, h )
  end = (w, h)
  draw.line((begin ,end), fill=border_col, width=border_width) 
    
  


image_location = "C:\Users\Horst\Pictures\Output\Colin's Birthday"
src_folder = "C:\Users\Horst\Pictures\Output\Colin's Birthday"

width = 2450
height = 3240

bg_col = '#000000'

tn_width = 230
tn_height = 153

gap_x = 26
gap_y = 32

per_row = 8

text_gap = 0
border_sides = 170
border_top = 130

fontname = "trebuc.TTF"
font_size = 16
image = Image.new('RGBA', (width, height), bg_col)
draw = ImageDraw.Draw(image)

file_list = []
g = glob.glob("%s//*.jpg" %(src_folder))
for item in g:
  file_list.append(item)

i = 0
j = 0
i = 0
for image_path in file_list:
  if "Kontakt" in image_path:
    continue
  print "Printing %s" %image_path
  im = Image.open(image_path)
  tn = im.resize((tn_width,tn_height))
  x = int(i * tn_width + border_sides + i * gap_x)
  y = int(j * tn_height + border_top + j * gap_y)
  make_border(tn, 2)
  image.paste(tn, (int(x),int(y)))
  text = image_path.split("\\")[-1:][0]
  if text:
    font = ImageFont.truetype("%s" %fontname, font_size)
    draw.text((x, y + tn_height + text_gap), "%s" %text, font=font, fill='#ababab')
  i += 1
  if i == per_row:
    j += 1
    i = 0

image.save("%s\Kontakt.jpg" %image_location, "JPEG", quality=100)  

