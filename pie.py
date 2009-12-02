#-*- coding:utf8 -*-

from __future__ import division
#import PngImagePlugin
import Image
import ImageDraw, ImageChops, ImageColor

def get_survey_file_l(filename):
  rFile = open(filename,'r')
  survey_l = rFile.readlines()
  rFile.close()
  return survey_l


def get_choice_answers(txt_l):
  for line in txt_l:
    bits = {}
    print "\n-------------------------"
    line_l = line.split("\t") 
    title = line_l[0].strip("?")
    print "%s" %title
    print "-------------------------"
    for bit in line_l:
      if not bit:
        continue
      bits.setdefault(bit,0)
      bits[bit] += 1
      
    for bit in bits:
      if bits[bit] > 1:
        print bit, bits[bit]


def get_yes_no_answers(txt_l):
  for line in txt_l:
    title = line.split("\t")[0].strip("?")
    no = line.count("no")
    yes = line.count("yes")
    sum = no + yes
    all = len(line.split("\t"))
    
    if sum < 120:
      continue
    if yes:
      try:
        no = no/all
        yes = yes/all
        print ("%s -- Yes: %.2f, No: %.2f" %(title, yes,no))
        make_pie_graph(yes=yes, no=no, name=title)
      except Exception, err:
        print("Error %s" %err)

def make_pie_graph(yes=0.5, no=0.4, name='fred'):
  colour = "#ffffff"
  size = (1200,1200)
  IM = Image.new('RGBA', size, colour)
  draw = ImageDraw.Draw(IM)
  
  border_colour = "#ababab"
  border_width = 10
  rad = size[0] - border_width
  rotation = -90
  margin = 0
  
  pie_colour_yes = "#00aa00"
  pie_colour_no = "#aa0000"
  
  yes_begin = int(0)
  yes_end = int(360*yes)
  no_begin = yes_end
  no_end = int(360*yes) + int(360*no)
  
  x_begin_yes = rad/2 + border_width/2
  y_begin_yes = rad/2 + border_width/2
  
  x_end_yes = rad/2 + border_width/2
  y_end_yes = 0
  
  x_begin_no = rad/2 + border_width/2
  y_begin_no = rad/2 + border_width/2
  x_end_no = rad
  y_end_no = rad/2 + border_width/2
  
  yes_begin += rotation
  yes_end += rotation
  no_begin += rotation
  no_end += rotation
  
  draw.ellipse((margin, margin, rad+border_width, rad+border_width), fill=border_colour)
  draw.pieslice((margin+border_width, margin+border_width, rad, rad), yes_begin, yes_end, fill=pie_colour_yes)
  draw.pieslice((margin+border_width, margin+border_width, rad, rad), no_begin, no_end, fill=pie_colour_no)
  
  #draw.line((x_begin_yes, y_begin_yes, x_end_yes, y_end_yes), fill=border_colour, width=border_width/2)
  #draw.line((x_begin_no, y_begin_no, x_end_no, y_end_no), fill=border_colour, width=border_width/2)
  
  IM.save("%s/%s.png" %(basedir,name))

basedir = "C:/Users/Horst/Documents/SurveyResult"
survey_l = get_survey_file_l(("%s/test.txt" %basedir))
#get_yes_no_answers(survey_l)
get_choice_answers(survey_l)
