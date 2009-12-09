from __future__ import division
import PngImagePlugin
import JpegImagePlugin
import IptcImagePlugin as IPTC
import Image
import glob, os
import ImageFont, ImageDraw, ImageChops, ImageStat, ImageEnhance
import string
import sys


class ImageTools(object):
  def __init__(self):
    pass
  def get_images_in_folder_list(self, src_folder):
    self.iptc = {}
    file_list = []
    g = glob.glob("%s//*.jpg" %(src_folder))
    for item in g:
      self.iptc_extract(item)
      if "_" not in item:
        file_list.append(item)
    return file_list, self.iptc
    
  def draw_text(self, draw, text, font, x, y, fill='#ababab', max_width = 200, line_spacing = 50, align='left'):
    text = text.split()
    width = 0
    line = []
    txt = ""
    curr_y = y
    for word in text:
      (wX, wY) = draw.textsize("%s " %word, font=font)
      width += wX 
      if width < max_width:
        txt += "%s " %word
      else:
        line.append(txt)
        txt = "%s " %word
        width = wX
    line.append(txt)
    j = 0
    for l in line:
      l = l.strip()
      if align == "right":
        x_t = x + max_width - draw.textsize("%s " %l, font=font)[0]
      else:
        x_t = x
      curr_y = y + j * line_spacing
      draw.text((x_t, curr_y), "%s" %l, font=font, fill=fill)
      j += 1
    return curr_y + wY
  
  def iptc_extract(self, image_path):
    im = Image.open(image_path)
    iptc_d = IPTC.getiptcinfo(im)
    
    #for i in xrange(120):
      #s = iptc_d.get((2,i), "None")
      #print i, s
    
    if iptc_d:
      self.iptc.setdefault(image_path,{'title':iptc_d.get((2, 5), ""),
                                  'headline':iptc_d.get((2,105), ""),
                                  'caption':iptc_d.get((2,120), ""),
                                  'country':iptc_d.get((2,101), ""),
                                  'province':iptc_d.get((2,95), ""),
                                  'city':iptc_d.get((2,90), ""),
                                  'location':iptc_d.get((2,92), ""),
                                  'iptc_caption':iptc_d.get((2,120), ""),
                                  'Status-JobID':iptc_d.get((2,103), ""),
                                  'Status-Provider':iptc_d.get((2,110), ""),
                                  'Status-Source':iptc_d.get((2,115), ""),
                                  'Status-Instructions':iptc_d.get((2,40), ""),
                                  'Status-Title':iptc_d.get((2,40), ""),
                                })
    else:
      self.iptc.setdefault(image_path,{})
      