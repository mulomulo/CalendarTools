# -*- coding: utf-8 -*-

from __future__ import division
import PngImagePlugin
import JpegImagePlugin
import IptcImagePlugin as IPTC
import Image
import glob, os
import ImageFont, ImageDraw, ImageChops, ImageStat, ImageEnhance
import string
import sys

class Calendar(object):
  def __init__(self, year, language, cal_name, basedir, bw, feiertage, belongs_to, holidays, output_dir, d):
    #super(Calendar, self).__init__(year, language, cal_name, basedir, bw, feiertage, print_location_in_index, belongs_to, holidays)
    self.year = '2013'
    self.bw = bw
    self.belongs_to = belongs_to
    self.holidays = holidays
    self.basedir = "%s/%s" %(basedir, self.year)
    self.output_dir = "%s/%s/finished" %(output_dir, self.year)
    self.print_location_in_index = print_location_in_index
    try:
      self.cal_name = cal_name.split("_")[0]
      self.subset = cal_name.split("_")[1]
    except:
      self.cal_name = cal_name
      self.subset = False

    try:
      self.cal_name = self.cal_name.decode('utf-8')
    except:
      pass

    self.language = language
    try:
      self.region = language.split("-")[1]
    except:
      self.region = self.holidays
    self.feiertage = feiertage
    self.l = []
    self.msg = []
    self.thumbnails = {}
    self.iptc = {}
    self.useSRCFile = False
    self.useIPTC = False

  def run(self):

    self.get_images_in_folder()
    if self.subset:
      region = "_%s" %self.subset
    else:
      region = ""
    if self.useSRCFile:
      source_file = "%simage_source_%s%s.txt" %(self.basedir, self.cal_name, region)
      rfile = open(source_file, 'r')
      l= []
      i = 0
      for li in rfile:
        if li[0] != "\\":
          self.msg.append(li)
          continue
        li = li.split(";")
        try:
          text = li[2]
        except:
          text = ""
        l.append([li[1], li[0].split("\n")[0], text])
        i += 1
      l.sort()
      self.l = l
    if self.useIPTC:
      l = []
      for image in self.iptc:
        l.append([self.iptc[image].get("month"),image])
      l.sort
      self.l = l
    else:
      l= []
      for image in self.file_list:
        month = image.split('\\')[-1:]
        try:
          month = int(month[0].split('.jpg')[0])
          l.append((month,image))
        except:
          pass
      self.l = l

    image = self.make_calendar()

  def get_images_in_folder(self):
    src_folder = "%s/src/%s/" %(self.basedir, self.cal_name)
    if not os.path.exists(src_folder):
      try:
        print "Problem going to this location: %s" %self.cal_name
      except:
        print "can't print calendar name, probably non-ascii problem!"
    file_list = []
    g = glob.glob("%s//*.jpg" %(src_folder))
    for item in g:
      #print "Reading IPTC for %s" %item
      self.iptc_extract(item)
      file_list.append(item)
    self.file_list = file_list


  def make_calendar(self):
    cal_name = self.cal_name
    print ""
    print "---------------------------------------"
    #print "Starting on Calendar %s" %cal_name
    language = self.language.split("-")[0]
    if language == "english":
      months = ["Title", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    elif language == "german":
      months = ["Title", "Januar", "Februar", u"März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    elif language == "greek":
      months = ["Title", u"Ιανουάριος", u"Φεβρουάριος", u"Μάρτης", u"Απρίλιος", u"Μάιος", u"Ιούνιος", u"Ιούλιος", u"Αύγουστος", u"Σεπτέμβριος", u"Οκτώβριος", u"Νοέμβριος", u"Δεκέμβριος"]
    else:
      months = ["Title", "January", "February"]
    self.height = 1800
    self.width = 1200
    self.image_width = 0
    self.image_height = 0
    self.border_top = 90
    self.border_sides = 70
    self.bg_col = (255, 255, 255)

    #Distances from the top in fractions
    #self.image_top = 0.06
    self.month_begin = 0.55
    self.week_begin = 0.65
    self.week_days = self.week_begin + 0.06
    self.title_begin = 0.70
    self.title_year_begin = 0.85


    #Colours for the various objects
    self.special_day_col = (255, 0, 0)
    self.special_day_col_sat = (200, 20, 20)
    self.special_day_col = (70, 70, 70)
    self.special_day_col_sat = (70, 70, 70)
    self.feiertag_day_col = (70, 70, 70)
    self.normal_day_col = (150, 150, 150)
    self.week_col = (50, 50, 100)
    self.month_col = (50, 50, 100)
    if self.cal_name == "Marrakech":
      self.week_col = (70, 50, 30)
      self.month_col = (70, 50, 30)
      self.normal_day_col = (150, 110, 70)

    self.tn_per_row = 3
    self.tn_width = self.width/(self.tn_per_row + 0.6)
    self.tn_size = 0

#    self.fontname = "trebuc.TTF"
#    self.fontname_bold = "trebucbd.TTF"
    self.fontname = "cambria.ttc"
    self.fontname_bold = "cambriab.ttf"
    self.index_fontname = "trebuc.TTF"
    self.index_fontname_bold = "trebucbd.TTF"


    self.week_fontsize = 52
    self.mcount = 0
    l = self.l
    assert self.l is not None

    self.imagepaths = []
    for sort, path in l:
      self.imagepaths.append("%s" %(path))
#		for month in months:
#			self.make_sheet(month)
#			self.mcount += 1
    self.months_txt_l = months
    i = 0
    for sheet in self.l:
      i += 1
      if i > 13:
        continue
      self.month = months[sheet[0]-1]
      try:
        print u"Making %s" %self.month
      except:
        print "Printing something with strange Characters"
      self.image_src = sheet[1]
      #self.mcount = int(month[0])
      #self.month = month
      self.mcount = sheet[0] -1
      self.make_sheet()
    self.make_index()
    print "%s DONE."


  def makeInfoLine(self, n):
    text = ""
    iptc = self.thumbnails[n][1]
    if 'headline' in self.print_location_in_index:
      text += "%s " %iptc.get('headline', "").replace(" ","_")
    if 'location' in self.print_location_in_index:
      text += "%s " %iptc.get('location', "").replace(" ","_")
    if 'city' in self.print_location_in_index:
      text += "%s " %iptc.get('city', "").replace(" ","_")
    if 'province' in self.print_location_in_index:
      text += "%s " %iptc.get('province', "").replace(" ","_")
    if 'country' in self.print_location_in_index:
      text += "%s " %iptc.get('country', "").replace(" ","_")
    if text:
      text = text.strip()
      text = text.replace("    ", " ")
      text = text.replace("   ", " ")
      text = text.replace("  ", " ")
      text = text.replace(" ", ", ")
      text = text.replace("_", " ")
    return text

  def make_index(self):
    print "Making Index Sheet"
    self.image = Image.new('RGBA', (self.width, self.height), self.bg_col)
    draw = ImageDraw.Draw(self.image)
    tn_width = self.tn_size[0]
    tn_height = self.tn_size[1]
    gap_y = 60
    gap_x = (self.width - 2 * self.border_sides - (self.tn_per_row * tn_width))/(self.tn_per_row -1)
    text_gap = 6
    i = 0
    j = 0
    for n in xrange(len(self.thumbnails)):
      x = int(i * tn_width + self.border_sides + i * gap_x)
      y = int(j * tn_height + self.border_top + j * gap_y)
      tn = self.thumbnails[n][0]
      self.make_border(tn, 2)
      self.image.paste(tn, (int(x),int(y)))
      text = self.makeInfoLine(n)
      ##FUDGE¬!!!!!!!!!!!!!!!!!!!!!!!
      if not text and self.print_location_in_index:
        text = d.get('idx_%s' %n,' ')

      if not text and self.print_location_in_index:
        text = raw_input("Enter something: ")

        
      
      if text:
        font = ImageFont.truetype("%s" %self.fontname, 20)
        draw.text((x, y + tn_height + text_gap), "%s" %text, font=font, fill=self.month_col)
      i += 1
      if i == 3:
        j += 1
        i = 0

    x = int(i * tn_width + self.border_sides + i * gap_x)
    spacing = 30
    y = int((j * tn_height + self.border_top + j * gap_y) - 7)
    if "-" in self.cal_name:
      font_size = 70
      self.cal_name = self.cal_name.replace("-", " ")
    else:
      font_size = 90

    font = ImageFont.truetype("%s" %self.fontname, font_size)
##beware dragons
#    try:
#      text = self.cal_name.split(".")[0].split("-")[1]
#    except:

    text = self.cal_name
    text = self.cal_name.split('.')[0]
    if text == "Chora":
      text = u'Χώρα'

    ad = d.get('ad_image',None)
    if not ad:
      draw.text((x-4, y), "%s" %text, font=font, fill=self.month_col)
    else:
      im = Image.open("%s/src/%s_400.jpg" %(self.basedir, ad.split('$')[0]))
      orig_width = im.size[0]
      orig_height = im.size[1]
      #px = self.image_width + self.border_sides - orig_width
      #py = 1480
      self.image.paste(im, (x,y + 10))


    if "trebuc" in self.index_fontname:
      fudge_y = 97
    elif "camb" in self.index_fontname:
      fudge_y = 100


    y = (j * tn_height + self.border_top + j * gap_y) + fudge_y
    font = ImageFont.truetype("%s" %self.index_fontname_bold, 20)
    text = "Horst Puschmann"
    if ad: text = "OlexSys Ltd."
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    font = ImageFont.truetype("%s" %self.index_fontname, 20)
    text = "5 South Street"
    if ad: text = "Department of Chemistry"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    font = ImageFont.truetype("%s" %self.index_fontname, 20)
    text = "Sherburn Village"
    if ad: text = "Durham University"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    font = ImageFont.truetype("%s" %self.index_fontname, 20)
    text = "Durham DH6 1HP, U.K."
    if ad: text = "Durham DH1 3LE"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    font = ImageFont.truetype("%s" %self.index_fontname_bold, 20)
    text = "horst.puschmann@gmail.com"
    if ad: text = "horst@olexsys.org"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    font = ImageFont.truetype("%s" %self.index_fontname, 24)
    y += 40
    x = self.border_sides
#    for text in self.msg:
#      text = text.replace("\n", "")
#      y += spacing + 3
#      draw.text((x, y), "%s" %text, font=font, fill=self.month_col)
    iptc = self.thumbnails[0][1]
#    text = iptc.get('iptc_caption', "")
    text = d['caption']
    text = text.decode("utf-8")
    text = text.split()

    w = 0
    lines = []
    l = ""
    max_width = self.width - (self.border_sides * 2)
    for word in text:
      w += draw.textsize("%s " %word, font=font)[0]
      if w < max_width:
        l += "%s " %word
      else:
        lines.append(l)
        l = "%s " %word
        w = draw.textsize("%s " %word, font=font)[0]
    lines.append(l)
    for text in lines:
      y += spacing + 3
      draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    if self.subset:
      region = self.subset
    else:
      region = self.region
    image_location = "%s/%s/%i-index-%s.jpg" %(self.output_dir, self.belongs_to, 13, self.belongs_to)
    self.image.save("%s" %image_location, "JPEG", quality=100)
#		image_location = "Calendars/%s/%i-index.png" %(self.cal_name, self.mcount+1)
#		self.image.save("%s" %image_location, "PNG", quality=95)


  def make_sheet(self):
    month = self.month
    self.image = Image.new('RGBA', (self.width, self.height), self.bg_col)
    self.draw = ImageDraw.Draw(self.image)
    self.draw_image()
    if month == "Title":
      self.draw_title()
    else:
      self.draw_caption()
      self.draw_month(month)
      self.draw_weeks()
    try:
      if self.subset:
        region = "%s" %self.subset
      else:
        region = self.region
      self.target_directory = "%s/%s" %(self.output_dir, self.belongs_to)
      os.mkdir(self.target_directory)
    except:
      pass
    j = "0"
    if self.mcount > 9: j = ""
    #if self.bw:
      #desaturator = 	ImageEnhance.Color(self.image)
      #self.image = desaturator.enhance(0.0)
      #contrast = ImageEnhance.Contrast(self.image)
      #self.image = contrast.enhance(1.2)
    if self.subset:
      region = self.subset
    else:
      region = self.region

    image_location = u"%s/%s-%s/%s%i-%s-%s.jpg" %(self.output_dir, self.cal_name, self.belongs_to, j, self.mcount, month, self.belongs_to)
    image_location = "%s/%s%i-%s-%s.jpg" %(self.target_directory, j, self.mcount, month, self.belongs_to)
    image_location = "%s/%s%i-%s-%s.jpg" %(self.target_directory, j, self.mcount, self.belongs_to, region)

    image_path = "%s/%s" %(self.output_dir, self.belongs_to)
    if not os.path.exists(image_path):
      os.mkdir(image_path)
    self.target_directory = "%s/%s%i-%s-%s.jpg" %(image_path, j, self.mcount, self.belongs_to, region)
    self.image.save("%s" %self.target_directory, "JPEG", quality=100)
    #image_location = "Calendars/%s/%s%i-%s.png" %(self.cal_name, j, self.mcount, month)
    #self.image.save("%s" %image_location, "PNG")


  def draw_title(self):
    stat = ImageStat.Stat(self.image)
    s = stat.mean[:3]
    month_col = (int(s[0]/2), int(s[1]/2), int(s[2]/2))
    draw = self.draw
    self.draw_caption()
    font = ImageFont.truetype("%s" %self.fontname, 130)
    text = self.cal_name.split('.')[0]
    text = d['title']
    text = text.decode("utf-8")
    t = text.split("-")
    if len(t) > 1:
      i = 0
      for text in t:
        text_size = 120
        if i == 0:
          font = ImageFont.truetype("%s" %self.fontname, text_size)
          txt_size = draw.textsize(text, font=font)
        else:
          font = ImageFont.truetype("%s" %self.fontname, text_size)
          txt_size = draw.textsize(text, font=font)
        x = int(int((self.width/2) - (txt_size[0]/2)))
        y  = int(self.height * self.title_begin + i * text_size)
        draw.text((x, y), "%s" %text, font=font, fill=month_col)
        i += 1
    else:
      if text == "Chora":
        text = u'Χώρα'
      txt_size = draw.textsize(text, font=font)
      x = int((self.width/2) - (txt_size[0]/2))
      y  = int(self.height * self.title_begin + 70)
      draw.text((x, y), "%s" %text, font=font, fill=month_col)

    font = ImageFont.truetype("%s" %self.fontname, 90)
    text = self.year
    txt_size = draw.textsize(text, font=font)
    x = int((self.width/2) - (txt_size[0]/2))
    y  = int(self.height * self.title_year_begin)
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)
    self.draw = draw


  def draw_caption(self):
    draw = self.draw
    font = ImageFont.truetype("%s" %self.fontname, 26)
    x = 926
    y = 895
    ty = y + 2
    tx = self.border_sides
    img_src =d.get('ad_image',None)
    img_width = 200
    text = d.get('cap_%s' %self.mcount,None)
    if text:
      text = text.decode("utf-8")
    if text:
      txt_size = draw.textsize(text, font=font)
    if img_src:
      if '$L' in img_src:
        x = self.border_sides
        img_src = img_src.strip('$L')
        tx = int(self.border_sides + self.image_width - txt_size[0])
      elif '$C' in img_src:
        x = int(self.border_sides + (self.image_width/2 - img_width/2))
        img_src = img_src.strip('$C')
        tx = self.border_sides
      elif '$R' in img_src:
        x = int(self.border_sides + self.image_width - img_width)
        img_src = img_src.strip('$R')
        tx = self.border_sides

      im = Image.open("%s/src/%s.jpg" %(self.basedir, img_src))
      orig_width = im.size[0]
      orig_height = im.size[1]
#      new_width = 200
#      new_height = (orig_height/orig_width) * new_width
#      im = im.resize((int(new_width), int(new_height)))
      self.image.paste(im, (x,y))
    if text:
      draw.text((tx, ty), "%s" %text, font=font, fill="#ababab")
    self.draw = draw
    

  def draw_month(self, month):
    draw = self.draw
    font = ImageFont.truetype("%s" %self.fontname, 80)
    text = month.upper()
    text = month
    #print u"Making %s" %(unicode.decode(text))
    txt_size = draw.textsize(text, font=font)
    x = int((self.width/2) - (txt_size[0]/2))
    y  = int(self.height * self.month_begin)
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)
    self.draw = draw

  def draw_weeks(self):
    if 'english' in self.language:
      week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    elif 'german' in self.language:
      week_days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    elif 'greek' in self.language:
      week_days = [u"Δε", u"Τρ", u"Τε", u"Πέ", u"Πα", u"Σά", u"Κυ"]


    if self.holidays == "en":
      feiertage_2007 = [(1,1), (6,4), (9,4), (7,5), (28,5), (27,8), (25,12), (26,12)]
      feiertage_2008 = [(1,1), (21,3), (24,4), (5,5), (26,5), (25,8), (25,12), (26,12)]
      feiertage_2009 = [(1,1), (10,4), (13,4), (4,5), (25,5), (31,8), (25,12), (28,12)]
      feiertage_2010 = [(1,1), (2,4), (5,4), (3,5), (31,5), (30,8), (27,12), (28,12)]
      feiertage_2011 = [(3,1), (22,4), (25,4), (2,5), (30,5), (29,8), (26,12), (27,12)]
      feiertage_2012 = [(2,1), (6,4), (9,4), (7,5), (4,6), (5,6), (27,8), (25,12), (26,12)]
      feiertage_2013 = [(1,1), (29,3), (1,4), (6,5), (27,5), (26,8), (25,12), (26,12)]

    elif self.holidays == "sc":
      feiertage_2007 = [(1,1), (2,1), (6,4), (9,4), (7,5), (28,5), (6,8), (25,12), (26,12)]
      feiertage_2009 = [(1,1), (2,1), (10,4), (4,5), (25,5), (3,8), (30,11), (25,12), (28,12)]
      feiertage_2010 = [(1,1), (4,1), (2,4), (3,5), (31,5), (1,8), (30,11), (25,12), (28,12)]
      feiertage_2011 = [(3,1), (4,1), (22,4), (2,5), (30,5), (29,8), (30,11), (26,12), (27,12)]
      feiertage_2012 = [(2,1), (3,1), (6,4), (9,4), (7,5), (4,6), (5,6), (27,8), (25,12), (26,12)]
      feiertage_2013 = [(1,1), (2,1), (29,3), (1,4), (6,5), (27,5), (26,8), (2,12), (25,12), (26,12)]

    elif self.holidays == "nz":
      feiertage_2007 = [(1,1), (2,1), (6,2), (6,4), (9,4), (25,4), (4,6), (22,10), (25,12), (26,12)]
      feiertage_2008 = [(1,1), (2,1), (6,2), (21,3), (24,3), (25,4), (2,6), (27,10), (25,12), (26,12)]
      feiertage_2009 = [(1,1), (2,1), (6,2), (10,4), (13,3), (25,4), (1,6), (26,10), (25,12), (28,12)]
      feiertage_2010 = [(1,1), (4,1), (6,2), (2,4), (5,3), (25,4), (7,6), (25,10), (27,12), (28,12)]
      feiertage_2011 = [(1,1), (2,1), (6,2), (22,4), (25,4), (6,6), (24,10), (25,12), (26,12)]
      feiertage_2012 = [(2,1), (6,2), (6,4), (9,4), (25,4), (4,6), (22,10), (25,12), (26,12)]
      feiertage_2013 = [(1,1), (6,2), (29,3), (1,4), (25,4), (3,6), (28,10), (25,12), (26,12)]

    elif self.holidays == "gr":
      feiertage_2009 = [(1,1), (6,1), (9,3), (25,3), (1,4), (17,4), (20,4), (1,5), (8,6), (15,8), (1,10), (28,10), (25,12), (26,12)]
      feiertage_2010 = [(1,1), (2,4), (5,4), (1,5), (13,5), (24,5), (3,10), (24,12), (25,12), (26,12), (31,12)]
      feiertage_2011 = [(1,1), (6,1), (25,3), (22,4), (25,4), (1,5), (15,8), (25,12), (26,12)]
      feiertage_2012 = [(1,1), (6,1), (27,2), (25,3), (13,4), (16,4), (1,5), (4,6), (15,8), (28,10), (25,12), (26,12)]

    elif self.holidays == "de":
      feiertage_2007 = [(1,1), (6,1), (6,4), (9,4), (1,5), (17,5), (28,5), (7,6), (15,8), (3,10), (1,11), (25,12), (26,12)]
      feiertage_2008 = [(1,1), (6,1), (21,3), (24,3), (1,5), (12,5), (22,5), (8,8), (15,8), (3,10), (31,10), (1,11), (19,11), (25,12), (26,12)]
      feiertage_2009 = [(1,1), (10,4), (13,4), (1,5), (21,5), (1,6), (3,10), (24,12), (25,12), (26,12), (31,12)]
      feiertage_2010 = [(1,1), (2,4), (5,4), (1,5), (13,5), (24,5), (3,10), (24,12), (25,12), (26,12), (31,12)]
      feiertage_2011 = [(1,1), (6,1), (22,4), (25,4), (1,5), (13,6), (3,10), (24,12), (25,12), (26,12), (31,12)]
      feiertage_2012 = [(1,1), (6,4), (9,4), (1,5), (17,5), (28,5), (15,8), (3,10), (1,11), (25,12), (26,12)]
      feiertage_2013 = [(1,1), (6,1), (29,3), (31,3), (1,4), (1,5), (9,5), (20,5), (30,5), (3,10), (1,11), (25,12), (26,12)]

    elif self.holidays == "us":
      feiertage_2013 = [(1,1), (21,1), (18,2), (27,5), (4,7), (2,9), (14,10), (11,11), (28,11), (25,12)]
      

    elif self.holidays == "by":
      feiertage_2007 = [(1,1), (6,1), (6,4), (9,4), (1,5), (17,5), (28,5), (7,6), (15,8), (3,10), (1,11), (25,12), (26,12)]
      feiertage_2008 = [(1,1), (21,3), (24,3), (1,5), (12,5), (22,5), (8,8), (15,8), (3,10), (31,10), (1,11), (19,11), (25,12), (26,12)]
      feiertage_2012 = [(1,1), (6,1), (6,4), (9,4), (1,5), (17,5), (28,5), (3,10), (25,12), (26,12)]

    if not self.feiertage or self.holidays == "ne":
      feiertage = []
    week_2007 = [(), (0, 31), (3, 28), (3, 31), (6, 30), (1, 31), (4, 30), (6, 31), (2, 31), (5, 30), (0, 31), (3, 30), (5, 31)]
    week_2008 = [(), (1, 31), (4, 29), (5, 31), (1, 30), (3, 31), (6, 30), (1, 31), (4, 31), (0, 30), (2, 31), (5, 30), (0, 31)]
    week_2009 = [(), (3, 31), (6, 28), (6, 31), (2, 30), (4, 31), (0, 30), (2, 31), (5, 31), (1, 30), (3, 31), (6, 30), (1, 31)]
    week_2010 = [(), (4, 31), (0, 28), (6, 31), (2, 30), (4, 31), (0, 30), (2, 31), (5, 31), (1, 30), (3, 31), (6, 30), (1, 31)]
    week_2011 = [(), (5, 31), (1, 28), (1, 31), (4, 30), (6, 31), (2, 30), (4, 31), (0, 31), (3, 30), (5, 31), (1, 30), (3, 31)]
    week_2012 = [(), (6, 31), (2, 29), (3, 31), (6, 30), (1, 31), (4, 30), (6, 31), (2, 31), (5, 30), (0, 31), (3, 30), (5, 31)]
    week_2013 = [(), (1, 31), (4, 28), (4, 31), (0, 30), (2, 31), (5, 30), (0, 31), (3, 31), (6, 30), (1, 31), (4, 30), (6, 31)]
    if self.year == "2008":
      weeks = week_2008
    if self.year == "2009":
      weeks = week_2009
      feiertage = feiertage_2009
    if self.year == "2010":
      weeks = week_2010
      feiertage = feiertage_2010
    if self.year == "2011":
      weeks = week_2011
      feiertage = feiertage_2011
    if self.year == "2012":
      weeks = week_2012
      feiertage = feiertage_2012
    if self.year == "2013":
      weeks = week_2013
      feiertage = feiertage_2013

    draw = self.draw
    font = ImageFont.truetype("%s" %self.fontname, self.week_fontsize)
    i = 0
    for day in week_days:
      i += 1
      text = day
      txt_size = draw.textsize(text, font=font)
      x = int((self.width/(len(week_days)+1) * i) - (txt_size[0]/2))
      y  = int(self.height * self.week_begin)
      txt_col = self.week_col
      if i == 7: txt_col = self.special_day_col
      if i == 6: txt_col = self.special_day_col_sat
      draw.text((x, y), "%s" %text, font=font, fill=txt_col)

    font = ImageFont.truetype("%s" %self.fontname, self.week_fontsize)
    i = 0
    i += weeks[self.mcount][0]
    days = weeks[self.mcount][1]
    row = 0
    for j in xrange(days+1):
      if i == 8:
        i = 1
        row += 1
      text = str(j)
      if text == "0": text = ""
      txt_size = draw.textsize(text, font=font)
      txt_col = self.normal_day_col
      if i == 7: txt_col = self.special_day_col
      if i == 6: txt_col = self.special_day_col_sat
      if (j, self.mcount) in feiertage:
        txt_col = self.feiertag_day_col
      x = int((self.width/(len(week_days)+1) * i) - (txt_size[0]/2))
      y  = int(self.height * self.week_days) + row * txt_size[1] * 1.4
      draw.text((x, y), "%s" %text, font=font, fill=txt_col)
      i += 1

  def draw_image(self):
    #im = Image.open(r"C:\t\Calendars\Test\1.jpg")
#    im = Image.open(self.imagepaths[self.mcount])
    im = Image.open(self.image_src)
    orig_width = im.size[0]
    orig_height = im.size[1]
    new_width = self.width - (self.border_sides *2)
    new_height = (orig_height/orig_width) * new_width
    #im = im.resize((int(new_width), int(new_height)))
    self.image_width = int(new_width)
    self.image_height = int(new_height)
    self.make_border(im, 2)

    if self.bw:
      im = im.convert("L")
      #desaturator = 	ImageEnhance.Color(im)
      #im = desaturator.enhance(0.0)
      #contrast = ImageEnhance.Contrast(im)
      #im = contrast.enhance(1.1)
      #brighten = ImageEnhance.Brightness(im)
      #im = brighten.enhance(1.05)

    else:
      brighten = ImageEnhance.Brightness(im)
      im = brighten.enhance(1.05)


    grain = False
    if grain:
      grain = Image.open("%sgrain-1800_1200.jpg" %basedir)
      grain = grain.convert("L")
      x = self.image_width
      y = self.image_height
      grain = grain.crop((0, 0, x, y ))
      mask = im.point(lambda i : i == 124 and 255)   # create RGB mask
      mask = mask.convert('L')                       # mask to grayscale
      mask = mask.point(lambda i : i == 124 and 255) # mask to B&W grayscale
      mask = ImageChops.invert(mask)
      R, G, B = im.split()
      img = Image.merge('RGBA', (R, G, B, mask))

      #multi = ImageChops.multiply(im, grain)
      #im = ImageChops.composite(multi, grain,  mask)

#			screen = ImageChops.screen(im, grain)
#			im = ImageChops.composite(grain, im,  mask)


      #screen = ImageChops.screen(im, grain)
      #im = ImageChops.composite(im, screen, multi)
      #mask = ImageChops.invert(mask)
      #im = ImageChops.blend(im, grain, 0.2)
      #im = ImageChops.composite(im, grain, mask)
      #im = ImageChops.multiply(im, grain)
      #im = ImageChops.screen(im, grain)
      #im = ImageChops.constant(im, grain)

    #self.image.paste(n, (int((self.width * 0.15)/2),int(self.image_top * self.height)))
    self.image.paste(im, (int(self.border_sides),int(self.border_top)))
    tn_width = self.tn_width
    self.tn_size = (int(tn_width), int(tn_width * (self.image_height/self.image_width)))
    tn = im.resize(self.tn_size)
    self.thumbnails.setdefault(self.mcount, (tn, self.iptc[self.image_src]))

  def make_border(self, im, width):
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

  def iptc_extract(self, image_path):
    m = int((image_path.split(".jpg")[0][-2:]).replace("\\", "")) -1
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
                                       'month':m,
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
      print "NO METADATA for %s" %image_path
    
def belongs_to_from_file(year):
  belongs_to_from_file = {}
  rFile = open("%s_belongs_to.txt"%year,'r')
  fi = rFile.readlines()
  for line in fi:
    if line.startswith('#'):
      continue
    line = line.strip()
    if not line.startswith('[') and line:
      belongs_to_from_file.setdefault(cal,{})
      li = line.split("=")
      if not li[1]: li[1] = "."
      belongs_to_from_file[cal].setdefault(li[0],li[1])
    else:
      cal = line.strip('[').strip(']')

  return belongs_to_from_file




if __name__ == "__main__":
  belongs_to = ""

  #cal_name = "UK Landscapes"
  #print_location_in_index = ['headline', 'location', 'province',]

  #cal_name = "Strange Nature"
  #print_location_in_index = ['headline', 'location', 'country']

  #cal_name = "Machine Parts"
  #print_location_in_index = ['headline', 'location', 'country']

  #cal_name = "Durham"
  #print_location_in_index = ['headline', 'location',]

  #cal_name = "Birds"
  #print_location_in_index = ['headline', 'location', 'country',]

  #cal_name = "Chora"
  #print_location_in_index = []

  #cal_name = "Aileen"
  #print_location_in_index = ['location', 'city', 'country']

  #cal_name = "Toilet Signs"
  #print_location_in_index = ['city', 'country']

  #cal_name = "Skopelitis"
  #print_location_in_index = []

  #cal_name = "Anna & Kati"
  #print_location_in_index = []

  #cal_name = "NZ Churches"
  #print_location_in_index = ['headline', 'location', 'city',]

  #cal_name = "Oberstdorf"
  #print_location_in_index = []

  #cal_name = "Farmers"
  #print_location_in_index = []

  #cal_name = "Rabbits"
  #print_location_in_index = []

  #cal_name = "Fell End"
  #print_location_in_index = []

  #print_location_in_index = ['location', 'city', 'province', 'country']
  #print_location_in_index = ['headline', 'location', 'city', 'country']
  #print_location_in_index = ['headline', 'location', 'province',]
  #print_location_in_index = ['headline', 'location', 'city', 'province', 'country']

  #language = "german-by"
  language = "english-en"
  #language = "english-nz"
  #language = "english-sc"
  #language = "greek-ne"

  cal_name = "Easter.Nadine.english.de"
  print_location_in_index = ['location']

  cal_name = "Stencil.Matthias.german.de"
  print_location_in_index = []

  cal_name = u"Μετέωρα.David.greek.gr"
  print_location_in_index = []

  cal_name = u"Μετέωρα.Dieter.german.de"
  print_location_in_index = []

  cal_name = u"Μετέωρα.LindaDP.english.en"
  print_location_in_index = []

  cal_name = u"Μετέωρα.Granny.english.en"
  print_location_in_index = []

  cal_name = u"Μετέωρα.Rob.english.en"
  print_location_in_index = []

  cal_name = u"Μετέωρα.Michaela.german.de"
  print_location_in_index = []



  cal_name = u"Chicken"
  belongs_to = "LorraineJim"

  cal_name = u"White"
  belongs_to = "Ben"

  cal_name = u"Osaka"
  belongs_to = "Werner"

  #language = "english"
  #holidays = "en"
  #print_location_in_index = []

  cal_name = u"Adventures of a-Small Farmer.Johannes.english.de"


  #cal_name = u"Μόνο λόγια.Karen.english.en"
  #print_location_in_index = ['location']
  #calendar_caption = "Hello Rabbit's Friend!"


  cal_name = u"Balloon.Janetta-german.en"
  calendar_caption = "Hello Rabbit's Friend!"
  print_location_in_index = ['location']

  FellEnd2010= {
    'name':
      'Fell End',
    'belongs_to':
      ['FellEnd.Pohl-english.en', 'FellEnd.Bohmwick-english.de', 'FellEnd.Booth-english.en', 'FellEnd.Warren-english.en', 'FellEnd.FellEnd-english.en',
       'FellEnd.Janetta-english.en', 'FellEnd.Larissa-english.en', ],
    'calendar_caption':
      "These pictures were taken on the Fell End Weekend in July 2009",
    'print_location_index':
      ['']
  }


  Rabbits= {
    'name':
      'Rabbits',
    'belongs_to':
      [],
    'calendar_caption':
      "Rabbits. Rabbits everywhere. And Elephant managed to sneak in, too.",
    'print_location_index':
      []
  }


  Sheep2010 = {
    'name':
      'Sheep',
    'belongs_to':
      [],
    'calendar_caption':
      "These sheep were photographed in various locations around the globe. But mostly in Britain.",
    'print_location_index':
      ['country', 'location']
  }

  NZ = {
    'name':
      'New Zealand',
    'belongs_to':
      ['NewZealand-english.en', 'XChristine-german.de', 'XRatz-german.de', 'XDieter-german.de', 'XNadine-english.de', 'XSebastian-german.de', 'KateRich-english.sc', 'XOlgaDima-english.en',
       'XCatherine-english.en', 'XVictoria-english.en', 'XDavid-english.en', 'XKarenJames-english.en', 'XMargaretRichard-english.en', 'XMarcus-english.nz', 'XPaul-english.en',
       'XKaren-english.en',],
    'calendar_caption':
      "These images were taken in December 2008 and January 2009. We started out on Banks Peninsula, on the east coast of the South Islands, drove across Arthur's Pass\
 to the West Coast, then up to Farewell Spit. We ended up in Wellington and the Wairarapa, in the south of the North Island.",
    'print_location_index':
      ['headline', 'location', 'city', 'province']
  }

  Istanbul = {
    'name':
      'Istanbul',
    'belongs_to':
      ['Istanbul-english.en', 'XDavid-english.en', 'XZoltan-english.en', 'XOlly-english.en', 'XMathias-english.en', 'XLeigh-english.en', 'XLuc-english.en', 'XRichard-english.en', 'XJudith-english.en', 'XEmma-english.sc', 'XAlex-english.en'],
    'calendar_caption':
      "This is a fairly random selection of images taken during a one-week stay in Istanbul in August 2009. Istanbul is the 5th largest city in the world with about 11M inhabitants with papers and a further estimated 6M without.",
    'print_location_index':
      ['location']
  }

  DurhamCathedral = {
    'name':
      'Durham-Cathedral',
    'belongs_to':
      ['Opa-german.de', 'CraigBarbara-english.en', 'Gill-english.en', 'Lami-english.en', ],
    'calendar_caption':
      "These images were all taken during an open photography event in Durham Cathedral in Jun2 2009. Normally, photography is prohibited inside the cathedral. A few hundred people turned up for the event...",
    'print_location_index':
      ['location']
  }

  Sand = {
    'name':
      'Sand',
    'belongs_to':
      ['Sarah-english.en', 'Werner-german.de', 'Sand-english.en', 'Elinor-english.en', 'RF-english.en', 'Volker-german.de', 'Ben-english.en'],
    'calendar_caption':
      "Sometimes, it is nice to not only look at the sea, but straight down towards your feet. It's astonishing what you can see there.",
    'print_location_index':
    ['country', 'location',]
  }

  Colours = {
    'name':
      'Colours',
    'belongs_to':
      ['Colours-english.en', 'JohnC-english.en', 'JuliaFiona-english.en', 'Stefan-german.de', 'Roland-german.de'],
    'calendar_caption':
      "A series of unrelated images - except that something about their overall colour appearance defines something in common.",
    'print_location_index':
    ['country', 'city']
  }

  Walls = {
    'name':
      'Walls',
    'belongs_to':
      ['Walls-english.en', 'Anna-english.en', 'Rob-english.nz', 'Adrian-english.en', 'Birger-german.de', 'Helena-english.en', 'RolandB-german.de'],
    'calendar_caption':
      "Walls are everywhere. Walls surround us. We don't normally look at walls very much. If you do, and take pictures of them, people laugh at you. Here are some walls.",
    'print_location_index':
    ['country', 'city']
  }



  Amorgos = {
    'name':
      'Αμοργός',
    'belongs_to':
      [],
    'calendar_caption':
      "We didn't go to Amorgos in 2011. So here is a collection of images taken in 1985 instead. All images were taken on Ilford HP5 film and have been left exactly as they came out of the negative scanner.",
    'print_location_index':
      []
  }

  AgriculturalShows = {
    'name':
      'Agricultural-Shows',
    'belongs_to':
      ['Annette-english.de', 'Graeme-english.sc', 'Colin-english.en', 'Ehmke-english.en', 'LoraineJimmy-english.en', 'LindaDave-english.en', 'Jenny-english.en', 'XGerry-english.nz'],
    'calendar_caption':
      "These pictures were taken at two agricultural shows in the North East of England: The Slayley Show in August 2009 and The Blanchland Show in September 2009",
    'print_location_index':
      ['location']
  }

  Balloon = {
    'name':
      'Balloon',
    'belongs_to':
      ['Oma-german.de', 'XBirgit-german.de', 'Doph-english.en', 'XChris-english.de',
       'Father-english.sc', 'Granny-english.en', 'Holly-english.en', 'Cloud Nine-english.en'],
    'calendar_caption':
      "These images were taken during a 35 minute balloon ride, taking off in Allensford and landing near Burnopfield - in the North East of England. More pictuers and trace \
of the flight can be found at http://maps.google.com/maps/ms?ie=UTF&msa=0&msid=102123436356381590541. 00046cbb791494649e28f. (Sorry about the typing!)",
    'print_location_index':
      ['location']
  }

  Aileen= {
    'name':
      'Aileen',
    'belongs_to':
      ['Cath-english.sc'],
    'calendar_caption':
      "",
    'print_location_index':
    ['country', 'city', 'location']
  }

  Matiu= {
    'name':
      'Matiu',
    'belongs_to':
      ['Paolo-english.nz'],
    'calendar_caption':
      "",
    'print_location_index':
    ['country', 'city']
  }

## ---------------------------------------------------------------
## 2011 CALENDARS


  China= {
    'name':
      'China',
    'belongs_to':
      ['#Volker-german.de', '#Matthias-german.de', '#Werner-german.de', 'Rob-english.nz'],
    'calendar_caption':
      "The images in ths calendar were taken on two trips to China: One in June and the other in November 2010. I only visited cities - the smallest of which is Fuzhou with 7 million inhabitants.",
    'print_location_index':
    ['city', 'location']
    }

  North_Pennines= {
    'name':
      'North Pennines',
    'belongs_to':
      [],
    'calendar_caption':
      "In September 2011, we stayed near the small village of Garrigill, near Alston, in the North Pennines for one week. These images were made on the long walks we took in this amazing and remote region of the very north of England.",
    'print_location_index':
    ['city', 'location']
    }

  FellEnd= {
    'name':
      'Fell End',
    'belongs_to':
      ['#Oma-german.de'],
    'calendar_caption':
      "These pictures were taken on the Fell End Weekend in July 2012.Cover",
    'print_location_index':
      ['']
  }

  EasterInAmorgos= {
    'name':
      'Πάσχα στην-Αμοργό',
    'belongs_to':
      ['#Christine-german.de','#Michaela-german.de','#Opa-german.de','#Stefan-greek.de','#Dina-greek.gr','#Kalliopi-greek.gr','#Sabina-greek.gr','#Perikles-greek.gr'],
    'calendar_caption':
      "Easter in Chora on the island of Amorgos. In 2010, Greek Orthodox Easter was on the very earliest date possible: the 4th of April. It also happened to be on the same day as Easter everywhere else in the world.",
    'print_location_index':
      ['']
  }

  Sheep = {
    'name':
      'Sheep',
    'belongs_to':
      ['Oleg-english.en'],
    'calendar_caption':
      "All these sheep were seen on various trips to the Pennines, to the East of Durham.",
    'print_location_index':
      ['location',
       'city',
       'province',
#       'country',
       ]
  }

  Green = {
    'name':
      'Green',
    'belongs_to':
      [],
    'calendar_caption':
      "Green things. Mainly plants. In fact, they are all plants.",
    'print_location_index':
    ['location', 'city', 'country']
  }


  ChrisAndLudo= {
    'name':
      'Christina-and Ludovic',
    'belongs_to':
      [],
    'calendar_caption':
      "The Wedding of Christina and Ludovic in Saumur, October 16, 2010",
    'print_location_index':
      []
  }

  BlacktonGrange= {
    'name':
      'Blackton Grange',
    'belongs_to':
      ['Carol-english.en', 'Jannetta-english.en', 'Steffi-english.en'],
    'calendar_caption':
      "Carol's 40th Birthday party in Blackton Grange.",
    'print_location_index':
      ['country', 'location']
  }

  ToiletSigns= {
    'name':
      'Toilet Signs',
    'belongs_to':
      [],
    'calendar_caption':
      "Various toilet signs seen around the world. These are not always easy to photograph - especially when there are other toilet users around!",
    'print_location_index':
      ['country', 'location']
  }

  Olex2 = {
    'name':
      'Olex2',
    'belongs_to':
      [],
    'calendar_caption':
      "This is a collection of images. Some are more, others are less connected with the Olex2 project.",
    'print_location_index':
      []
  }

  Auerberg = {
    'name':
      'Auerberg',
    'belongs_to':
      [],
    'calendar_caption':
      "Zweimal Winterurlaub in Salchenried. Viel Wandern, viel Schee und eine Super Zeit dort. Vielen Dank!",
    'print_location_index':
      []
  }

  TheBooths= {
    'name':
      'The Booths',
    'belongs_to':
      [],
    'calendar_caption':
      "These are pictures of The Booths. Mainly taken in Waterhouses. Some were taken elsewhere. All were taken in 2011.",
    'print_location_index':
      []
  }

  ThePohls= {
    'name':
      'The Pohls',
    'belongs_to':
      [],
    'calendar_caption':
      "These are pictures of The Pohls. Mainly taken in Durham. Some were taken in Spain. All were taken in 2011.",
    'print_location_index':
      []
  }


## ---------------------------------------------------------------
## 2012 CALENDARS

  Kew= {
    'name':
      'Kew',
    'belongs_to':
      [],
    'calendar_caption':
      "A day in Kew Gardens with Karen, James and Alexander. July 2011.",
    'print_location_index':
      []
  }

  Lake_District = {
    'name':
      'Lake District',
    'belongs_to':
      [],
    'calendar_caption':
      'A weekend in the English Lake District in late October 2011. So basically: "Autumn in the Lakes"',
    'print_location_index':
      ['city']
  }

  Numbers = {
    'name':
      'Numbers',
    'belongs_to':
      [],
    'calendar_caption':
      'Numbers. Photographed in various locations around the globe. Often with amused onlookers looking on.',
    'print_location_index':
    ['location', 'city', 'country']
  }

  Durham = {
    'name':
      'County Durham',
    'belongs_to':
      [],
    'calendar_caption':
      '',
    'print_location_index':
    ['location', 'city', 'country']
  }


  Johnnie = {
    'name':
      'Johnnie',
    'belongs_to':
      [],
    'calendar_caption':
      '',
    'print_location_index':
    ['location', 'city', 'country']
  }


  Auerbergland= {
    'name':
      'Auerbergland',
    'belongs_to':
      [],
    'calendar_caption':
      'A few days in Salchenried in July 2011. Located south of the Auerberg in Southern Bavaria, the Auerberg is close to the Alps, but far enough away so it never really gets busy even in the main season.',
    'print_location_index':
    []
  }

  Nanning = {
    'name':'Nanning',
    'belongs_to':
      [],
    }

  Chora = {
    'name':'Chora',
    'belongs_to':
      [],
    }


  Boston = {
    'name':'Boston',
    'belongs_to':
      [],
    }

  Ben = {
    'name':'Ben',
    'belongs_to':
      [],
    }

  Donkeys= {
    'name':'Donkeys',
    'belongs_to':
      [],
    }

  Munich= {
    'name':'Munich',
    'belongs_to':
      [],
    }



  Schlipsheimer = {
    'name':'Schlipsheimer',
    'belongs_to':
      [],
    }



  Jyvaskyla = {
    'name':'Jyvaskyla',
    'belongs_to':
      [],
    }

  Kalliope = {
    'name':'Kalliope',
    'belongs_to':
      [],
    }



  Lumiere= {
    'name':
      'Lumiere',
    'belongs_to':
      [],
    'calendar_caption':
      'Lumiere Durham 2011. Durham City was transformed for four nights in November by about 30 light installations. These pictures are snaps from the event, taken on two different evenings.',
    'print_location_index':
    ['location']
  }

  #Callist = EasterInAmorgos
  #Callist = Sheep
  #Callist = Green
  #Callist = ToiletSigns
  #Callist = China
  #Callist = North_Pennines
  #Callist = Kew
  #Callist = Lake_District
  #Callist = Numbers
  #Callist = Auerbergland
  #Callist = Lumiere
  #Callist = Amorgos
  #Callist = Olex2
  #Callist = Aileen
  #Callist = Rabbits
  #Callist = ChrisAndLudo
  #Callist = Auerberg
  #Callist = TheBooths
  Callist = FellEnd

  for Callist in [Durham]:
#  for Callist in [Sheep, Green, North_Pennines, Lake_District, Numbers, Auerbergland, Lumiere, Amorgos, Aileen]:

    name = Callist['name']
    #calendar_caption = Callist['calendar_caption']
    #print_location_in_index = Callist['print_location_index']
    year = "2013"
    a = belongs_to_from_file(year)
    d = a[name]
    Callist['belongs_to'].append(a[name]['stamp'])
  
    for cal_name in Callist['belongs_to']:
      belongs_to = cal_name.split("-")[0]
      if "-" in cal_name:
        if '#' in belongs_to:
          continue
        language = cal_name.split("-")[1].split(".")[0]
        holidays = cal_name.split("-")[1].split(".")[1]
        if "." in belongs_to:
          cal_name = cal_name.split("-")[0]
          belongs_to = cal_name.split(".")[1]
        else:
          cal_name = name
  
      if "." in cal_name:
        belongs_to = cal_name.split('.')[1]
  
      basedir = 'R:/Users/Horst/Pictures/Output/Calendars/'
      output_dir = 'R:/Users/Horst/Pictures/Output/Calendars/'
  
      try:
        print u"++++++++++++++++++++\n\nMaking '%s' for %s" %(cal_name, belongs_to)
      except:
        print "error printing names"
      print u"Making Calendar"
      year = "2013"
      bw = False
      feiertage = True
      a = Calendar(year = year, language = language, cal_name = cal_name, basedir = basedir, bw = bw, feiertage = feiertage, belongs_to = belongs_to, holidays = holidays, output_dir = output_dir, d=d)
      a.run()


#### AMORGOS
  #cal_l = ['Manolis','Walter','Carsten','Marco','Doris','TraudlFerdinand','Roland','Heribert','Thomas','Sabine','Kalliope','Volker','Ntina']
  #cal_l = ['Martina']
  #i = 0
  #for name in cal_l:
    #i += 1
    #cal_name = u"Αμοργός.%s.greek.gr" %name
    #belongs_to = cal_name.split('.')[1]
    #language = cal_name.split('.')[2]
    #holidays = cal_name.split('.')[3]
    #print "Making calendar for %i/%i: %s" %(i, len(cal_l), name)
    #a = Calendar(year = year, language = language, cal_name = cal_name, basedir = basedir, bw = bw, feiertage = feiertage, print_location_in_index = print_location_in_index, belongs_to = belongs_to, holidays=holidays)
    #a.run()

###Fell End
  #cal_l = ['CarolColin','SueSteve','DebbieJulian','DebbiePaul','HelgeColin','SteffiEhmke']
  ##cal_l = ['SteffiEhmke']
  #i = 0
  #for name in cal_l:
    #i += 1
    #cal_name = u"Fell End.%s.english-en" %name
    #belongs_to = cal_name.split('.')[1]
    #language = cal_name.split('.')[2]
    #holidays = "en"
    #print "Making calendar for %i/%i: %s" %(i, len(cal_l), name)
    #try:
      #a = Calendar(year = year, language = language, cal_name = cal_name, basedir = basedir, bw = bw, feiertage = feiertage, print_location_in_index = print_location_in_index, belongs_to = belongs_to, holidays = holidays)
      #a.run()
      #print "Made calendar %s %i/%i: %s" %(cal_name, i, len(cal_l), name)
    #except:
      #print "Failed to make calendar %s %i/%i: %s" %(cal_name, i, len(cal_l), name)


    ##Previous Calendars
