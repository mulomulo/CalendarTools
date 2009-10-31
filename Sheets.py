# -*- coding: utf-8 -*-

from __future__ import division
import PngImagePlugin
import JpegImagePlugin
import IptcImagePlugin as IPTC
import glob, os
import ImageFont, ImageDraw, ImageChops, ImageStat, ImageEnhance
from PIL import Image, ImageOps
import string
import sys

class Sheet(object):
  def __init__(self, input):
    self.input = input
    self.width = 1800
    self.height = 2700
    self.bg_col = "#ffffff"
    self.border_sides = 40
    self.border_top = 40
    self.border_between = 36
    self.path = r"P:/Output/Weddingprint"
    self.fill = "#ababab"
    self.fontname = "trebuc.TTF"

    
  def setup_image(self):
    self.image = Image.new('RGBA', (self.width, self.height), self.bg_col)
    
  def open_image(self, name):
    try:
      im = Image.open("%s/%s.jpg" %(self.path, name))
    except:
      im = Image.new('RGBA', (300, 300), "#ff0000")
      d = ImageDraw.Draw(im)
      font = ImageFont.truetype("%s" %self.fontname, 60)
      d.text((3, 230), "%s" %name, font=font, fill="#000000")
      

      
      
    return im

  
  
  def make_linear_ramp(self, white):
      # putpalette expects [r,g,b,r,g,b,...]
      ramp = []
      r, g, b = white
      for i in range(255):
          ramp.extend((r*i/255, g*i/255, b*i/255))
      return ramp
  
    
  def make_sepia(self):
    # make sepia ramp (tweak color as necessary)
    sepia = self.make_linear_ramp((255, 252, 240))
    
    im = Image.open("%s/%s.jpg" %(self.path, self.name))
    
    # convert to grayscale
    if im.mode != "L":
        im = im.convert("L")
    
    # optional: apply contrast enhancement here, e.g.
    #im = ImageOps.autocontrast(im)
    
    # apply sepia palette
    im.putpalette(sepia)
    
    # convert back to RGB so we can save it as JPEG
    # (alternatively, save it in PNG or similar)
    im = im.convert("RGB")
    
    im.save("%s/file.jpg" %self.path)  
  
  
  def one_portrait(self):
    margin = 0
    if self.save_as == "19-church6":
      margin = 300
    draw = ImageDraw.Draw(self.image)
    im1 = self.open_image(self.name)
    height1 = im1.size[1]
    width1 = im1.size[0]
    left = self.border_sides
    top = self.border_top + margin
    draw.rectangle(((left -1, top -1), (width1 + left + 0, height1 + top + 0)), fill=self.fill)
    self.image.paste(im1, (left,top))

  def one_square_one_long(self):
    draw = ImageDraw.Draw(self.image)
    im1 = self.open_image(self.name[0])
    height1 = im1.size[1]
    width1 = im1.size[0]
    left = self.border_sides
    top = self.border_top
    draw.rectangle(((left -1, top -1), (width1 + left + 0, height1 + top + 0)), fill=self.fill)
    self.image.paste(im1, (left,top))
    im2 = self.open_image(self.name[1])
    height2 = im2.size[1]
    width2 = im2.size[0]
    top = self.border_top + self.border_between + height1
    draw.rectangle(((left -1, top -1), (width2 + left, height2 + top)), fill=self.fill)
    self.image.paste(im2, (left, top))

  def three_long(self):
    draw = ImageDraw.Draw(self.image)
    im1 = self.open_image(self.name[0])
    height1 = im1.size[1]
    width1 = im1.size[0]
    left = self.border_sides
    top = self.border_top
    draw.rectangle(((left -1, top -1), (width1 + left + 0, height1 + top + 0)), fill=self.fill)
    self.image.paste(im1, (left,top))
    im2 = self.open_image(self.name[1])
    height2 = im2.size[1]
    width2 = im2.size[0]
    top = self.border_top + self.border_between + height1
    draw.rectangle(((left -1, top -1), (width2 + left, height2 + top)), fill=self.fill)
    self.image.paste(im2, (left, top))
    im3 = self.open_image(self.name[2])
    height3 = im3.size[1]
    width3 = im3.size[0]
    top = self.border_top + self.border_between + height1 + self.border_between + height2
    draw.rectangle(((left -1, top -1), (width3 + left, height3 + top)), fill=self.fill)
    self.image.paste(im3, (left, top))

    
  def six_landscape(self):
    draw = ImageDraw.Draw(self.image)
    ## First Row
    im1 = self.open_image(self.name[0])
    height1 = im1.size[1]
    width1 = im1.size[0]
    top = self.border_top
    left = self.border_sides
    draw.rectangle(((left -1, top -1), (width1 + left, height1 + top)), fill=self.fill)
    self.image.paste(im1, (left, top))

    im2 = self.open_image(self.name[1])
    height2 = im2.size[1]
    width2 = im2.size[0]
    left = self.border_sides + width1 + self.border_between
    draw.rectangle(((left -1, top -1), (width2 + left, height2 + top)), fill=self.fill)
    self.image.paste(im2, (left,top))

    
    ##Second Row
    im3 = self.open_image(self.name[2])
    height3 = im3.size[1]
    width3 = im3.size[0]
    top = self.border_top + height1 + self.border_between
    left = self.border_sides
    draw.rectangle(((left -1, top -1), (width3 + left, height3 + top)), fill=self.fill)
    self.image.paste(im3, (left, top))

    im4 = self.open_image(self.name[3])
    height4 = im4.size[1]
    width4 = im4.size[0]
    top = self.border_top + height2 + self.border_between
    left = self.border_sides + width3 + self.border_between
    draw.rectangle(((left -1, top -1), (width4 + left, height4 + top)), fill=self.fill)
    self.image.paste(im4, (left,top))

    ##Third Row
    im5 = self.open_image(self.name[4])
    height5 = im5.size[1]
    width5 = im5.size[0]
    top = self.border_top + height1 + height3 + self.border_between *2
    left = self.border_sides
    draw.rectangle(((left -1, top -1), (width5 + left, height5 + top)), fill=self.fill)
    self.image.paste(im5, (left, top))

    im6 = self.open_image(self.name[5])
    height6 = im6.size[1]
    width6 = im6.size[0]
    top = self.border_top + height2 + height4 + self.border_between *2
    left = self.border_sides + width5 + self.border_between
    draw.rectangle(((left -1, top -1), (width6 + left, height6 + top)), fill=self.fill)
    self.image.paste(im6, (left,top))
    
    
  def one_square_two_landscape(self):
    draw = ImageDraw.Draw(self.image)
    im1 = self.open_image(self.name[0])
    height1 = im1.size[1]
    width1 = im1.size[0]
    left = self.border_sides
    top = self.border_top
    draw.rectangle(((left -1, top -1), (width1 + left + 0, height1 + top + 0)), fill=self.fill)
    self.image.paste(im1, (left,top))

    im2 = self.open_image(self.name[1])
    height2 = im2.size[1]
    width2 = im2.size[0]
    top = self.border_top + self.border_between + height1
    draw.rectangle(((left -1, top -1), (width2 + left, height2 + top)), fill=self.fill)
    self.image.paste(im2, (left, top))

    im3 = self.open_image(self.name[2])
    height2 = im2.size[1]
    width2 = im2.size[0]
    left = int(self.border_sides) + int(im2.size[0]) + self.border_between
    top = self.border_top + self.border_between + height1
    draw.rectangle(((left -1, top -1), (width2 + left, height2 + top)), fill=self.fill)
    self.image.paste(im3, (left,top))
    
    
  def save_image(self):
    self.image = self.image.convert("L")
    self.image.save("%s/Pages/%s.jpg" %(self.path, self.save_as), "JPEG", quality=100)
    
  def run(self):
    i=1
    for design in self.input:
      for image in design:
        self.name = image[0]
        self.make_what = image[1]
        self.save_as = image[2]
        self.setup_image()
        i += 1
        print "Making %s (%s)" %(self.save_as, i)
        getattr(self, self.make_what)()
        self.save_image()
        
        #if self.make_what == "one_portrait":
          #self.one_portrait()
        #elif self.make_what == "one_square_one_long":
          #self.one_square_one_long()
        #elif self.make_what == "one_square_two_landscape":
          #self.one_square_two_landscape()
        #elif self.make_what == "three_long":
          #self.three_long()
        #elif self.make_what == "six_landscape":
          #self.six_landscape()
        #if "sepia" in input:
          #self.make_sepia()
    
      

if __name__ == "__main__":

  one_portrait = [
    ("DSC_3763", "one_portrait", "12-green3"),
    ("DSC_3751", "one_portrait", "13-green4"),
    ("DSC_2642", "one_portrait", "01-page1"),
    ("DSC_2648", "one_portrait", "16-church3"),
    ("DSC_3801", "one_portrait", "01A-page1"),
    ("DSC_3828", "one_portrait", "17-church4"),
    ("DSC_3895", "one_portrait", "19-church6","margin = 120"),
    ("DSC_3930", "one_portrait", "21-mill2"),
    ("IMG_1309", "one_portrait", "22-mill3"),
    ("DSC_4055", "one_portrait", "28-mill9"),
    ("DSC_4232", "one_portrait", "29-mill10"),
    ("DSC_3992", "one_portrait", "31-mill11"),
    ("DSC_3994", "one_portrait", "32-mill12")
  ]
   
  one_square_one_long = [
    (("DSC_3627", "DSC_3620"), "one_square_one_long", "03-SA0"),
    (("DSC_3612", "DSC_3678"), "one_square_one_long", "04-SA3"),
    (("DSC_3740", "DSC_3729"), "one_square_one_long", "11-green1"),
    (("DSC_3724", "DSC_3720"), "one_square_one_long", "07-bus2"),
    (("DSC_2671", "DSC_2659"), "one_square_one_long", "15-church2"),
    (("DSC_3904", "DSC_3910"), "one_square_one_long", "20-mill1"),
    
  ]
  
  
  one_square_two_landscape = [
    (("DSC_3625", "DSC_3615", "DSC_3631"), "one_square_two_landscape", "05-SA1"),
    (("DSC_3709", "DSC_3703", "DSC_3705"), "one_square_two_landscape", "06-bus1"),
    (("DSC_3737", "DSC_3731", "DSC_3728"), "one_square_two_landscape", "10-green2"),
    (("DSC_3773", "DSC_3747", "DSC_3796"), "one_square_two_landscape", "09-bus3"),
    (("DSC_2646", "DSC_2657", "DSC_2638"), "one_square_two_landscape", "14-church1"),
    (("DSC_3845", "DSC_3836", "DSC_2686"), "one_square_two_landscape", "18-church5"),
    (("DSC_4264", "DSC_4265", "DSC_4267"), "one_square_two_landscape", "30-mill11"),
  ]

  three_long = [
    (("DSC_3602", "DSC_3593", "DSC_3596"), "three_long", "02-SA2"),
    (("DSC_3714", "DSC_3713", "DSC_3700"), "three_long", "08-bus4"),
    (("DSC_3943", "DSC_3946", "DSC_4274"), "three_long", "23-mill4"),
    (("DSC_3952", "DSC_3969", "DSC_3996"), "three_long", "24-mill5"),
    (("DSC_3951", "DSC_3959", "DSC_3964"), "three_long", "25-mill6"),
    (("DSC_3981", "DSC_3975", "DSC_4288"), "three_long", "26-mill7"),
    (("DSC_4000", "DSC_4002", "DSC_4006"), "three_long", "27-mill8"),
  ]
  
  six_landscape =[
    ]

  input = [one_portrait, one_square_one_long, one_square_two_landscape, three_long, six_landscape]
  
  a = Sheet(input)
  a.run()
  

  
  input = ("1-1", "one_portrait", "Page1")
  input = (("4-1", "4-2"), "one_square_one_long", "Page2")
  input = (("3-1", "3-2", "3-3"), "one_square_two_landscape", "Page3")
  input = (("SA3-1", "SA3-2"), "one_square_one_long", "SA3")
  input = (("SA1-1", "SA1-2", "SA1-3"), "one_square_two_landscape", "SA1")
  input = (("SA2-1", "SA2-2", "SA2-3"), "three_long", "SA2")
  input = (("SA0-1", "SA0-2"), "one_square_one_long", "SA0")
  input = (("bus1-1", "bus1-2", "bus1-3"), "one_square_two_landscape", "bus1")
  input = (("bus2-1", "bus2-2"), "one_square_one_long", "bus2")
  input = (("bus3-1", "bus3-2", "bus3-3"), "one_square_two_landscape", "bus3")
  input = (("bus4-1", "bus4-2", "bus4-3"), "three_long", "bus4")
  input = (("green1-1", "green1-2"), "one_square_one_long", "green1")
  input = ("green4-1", "one_portrait", "green4")
  input = ("green3-1", "one_portrait", "green3")
  input = (("green2-1", "green2-2", "green2-3"), "one_square_two_landscape", "green2")
  
