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
  def __init__(self, year, language, cal_name, basedir, bw, feiertage, print_location_in_index, belongs_to, holidays, calendar_caption, output_dir):
    #super(Calendar, self).__init__(year, language, cal_name, basedir, bw, feiertage, print_location_in_index, belongs_to, holidays)
    self.year = '2010'
    self.bw = bw
    self.belongs_to = belongs_to
    self.holidays = holidays
    self.basedir = "%s/%s" %(basedir, self.year)
    self.output_dir = "%s/%s" %(output_dir, self.year)
    self.print_location_in_index = print_location_in_index
    try:
      self.cal_name = cal_name.split("_")[0]
      self.subset = cal_name.split("_")[1]
    except:
      self.cal_name = cal_name
      self.subset = False

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
        month = int(month[0].split('.jpg')[0])
        l.append((month,image))
      self.l = l
        
    image = self.make_calendar()

  def get_images_in_folder(self):
    src_folder = "%s/src/%s/" %(self.basedir, self.cal_name)
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

    self.fontname = "trebuc.TTF"
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
        print "Making %s" %self.month
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
    font = ImageFont.truetype("%s" %self.fontname, 90)
##beware dragons 
    try:
      text = self.cal_name.split(".")[0].split("-")[1]
    except:
      text = self.cal_name
      text = self.cal_name.split('.')[0]
  
    draw.text((x-4, y), "%s" %text, font=font, fill=self.month_col)

    y = (j * tn_height + self.border_top + j * gap_y) + 105
    fontname = "trebucbd.TTF"
    font = ImageFont.truetype("%s" %fontname, 20)
    text = "Horst Puschmann"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    font = ImageFont.truetype("%s" %self.fontname, 20)
    text = "5 South Street"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    font = ImageFont.truetype("%s" %self.fontname, 20)
    text = "Sherburn Village"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    font = ImageFont.truetype("%s" %self.fontname, 20)
    text = "Durham DH6 1HP, U.K."
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    y += spacing
    fontname = "trebucbd.TTF"
    font = ImageFont.truetype("%s" %fontname, 20)
    text = "horst.puschmann@gmail.com"
    draw.text((x, y), "%s" %text, font=font, fill=self.month_col)

    fontname = "trebuc.TTF"
    font = ImageFont.truetype("%s" %fontname, 24)
    y += 40
    x = self.border_sides
#    for text in self.msg:
#      text = text.replace("\n", "")
#      y += spacing + 3
#      draw.text((x, y), "%s" %text, font=font, fill=self.month_col)
    iptc = self.thumbnails[0][1]
#    text = iptc.get('iptc_caption', "")
    text = calendar_caption
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
    
    image_location = r"%s/%s-%s/%s%i-%s-%s.jpg" %(self.output_dir, self.cal_name, self.belongs_to, j, self.mcount, month, self.belongs_to)
    image_location = "%s/%s%i-%s-%s.jpg" %(self.target_directory, j, self.mcount, month, self.belongs_to)
    image_location = "%s/%s%i-%s.jpg" %(self.target_directory, j, self.mcount, self.belongs_to)
    
    image_path = "%s/%s" %(self.output_dir, self.belongs_to)
    if not os.path.exists(image_path):
      os.mkdir(image_path)
    self.target_directory = "%s/%s%i-%s.jpg" %(image_path, j, self.mcount, self.belongs_to)
    self.image.save("%s" %self.target_directory, "JPEG", quality=100)
    #image_location = "Calendars/%s/%s%i-%s.png" %(self.cal_name, j, self.mcount, month)
    #self.image.save("%s" %image_location, "PNG")

    
  def draw_title(self):
    stat = ImageStat.Stat(self.image)
    s = stat.mean[:3]
    month_col = (int(s[0]/2), int(s[1]/2), int(s[2]/2))
    draw = self.draw
    font = ImageFont.truetype("%s" %self.fontname, 130)
    text = self.cal_name.split('.')[0]
    t = text.split("-")
    if len(t) > 1:
      i = 0
      for text in t:
        if i == 0:
          font = ImageFont.truetype("%s" %self.fontname, 80)
          txt_size = draw.textsize(text, font=font)
        else:
          font = ImageFont.truetype("%s" %self.fontname, 130)
          txt_size = draw.textsize(text, font=font)
        x = int(int((self.width/2) - (txt_size[0]/2)))
        y  = int(self.height * self.title_begin + i * 90)
        draw.text((x, y), "%s" %text, font=font, fill=month_col)
        i += 1
    else:
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
      
    elif self.holidays == "sc":
      feiertage_2007 = [(1,1), (2,1), (6,4), (9,4), (7,5), (28,5), (6,8), (25,12), (26,12)]
      feiertage_2009 = [(1,1), (2,1), (10,4), (4,5), (25,5), (3,8), (30,11), (25,12), (28,12)]
      feiertage_2010 = [(1,1), (4,1), (2,4), (3,5), (31,5), (1,8), (30,11), (25,12), (28,12)]
      
    elif self.holidays == "nz":
      feiertage_2007 = [(1,1), (2,1), (6,2), (6,4), (9,4), (25,4), (4,6), (22,10), (25,12), (26,12)]
      feiertage_2008 = [(1,1), (2,1), (6,2), (21,3), (24,3), (25,4), (2,6), (27,10), (25,12), (26,12)]
      feiertage_2009 = [(1,1), (2,1), (6,2), (10,4), (13,3), (25,4), (1,6), (26,10), (25,12), (28,12)]
      feiertage_2010 = [(1,1), (4,1), (6,2), (2,4), (5,3), (25,4), (7,6), (25,10), (27,12), (28,12)]
      
    elif self.holidays == "gr":
      feiertage_2009 = [(1,1), (6,1), (9,3), (25,3), (1,4), (17,4), (20,4), (1,5), (8,6), (15,8), (1,10), (28,10), (25,12), (26,12)]
      
    elif self.holidays == "de":
      feiertage_2007 = [(1,1), (6,1), (6,4), (9,4), (1,5), (17,5), (28,5), (7,6), (15,8), (3,10), (1,11), (25,12), (26,12)]
      feiertage_2008 = [(1,1), (6,1), (21,3), (24,3), (1,5), (12,5), (22,5), (8,8), (15,8), (3,10), (31,10), (1,11), (19,11), (25,12), (26,12)]
      feiertage_2009 = [(1,1), (10,4), (13,4), (1,5), (21,5), (1,6), (3,10), (24,12), (25,12), (26,12), (31,12)]
      feiertage_2010 = [(1,1), (2,4), (5,4), (1,5), (13,5), (24,5), (3,10), (24,12), (25,12), (26,12), (31,12)]
      
    elif self.holidays == "by":
      feiertage_2007 = [(1,1), (6,1), (6,4), (9,4), (1,5), (17,5), (28,5), (7,6), (15,8), (3,10), (1,11), (25,12), (26,12)]
      feiertage_2008 = [(1,1), (21,3), (24,3), (1,5), (12,5), (22,5), (8,8), (15,8), (3,10), (31,10), (1,11), (19,11), (25,12), (26,12)]
    if not self.feiertage or self.holidays == "ne":
      feiertage = []
    week_2007 = [(), (0, 31), (3, 28), (3, 31), (6, 30), (1, 31), (4, 30), (6, 31), (2, 31), (5, 30), (0, 31), (3, 30), (5, 31)]
    week_2008 = [(), (1, 31), (4, 29), (5, 31), (1, 30), (3, 31), (6, 30), (1, 31), (4, 31), (0, 30), (2, 31), (5, 30), (0, 31)]
    week_2009 = [(), (3, 31), (6, 28), (6, 31), (2, 30), (4, 31), (0, 30), (2, 31), (5, 31), (1, 30), (3, 31), (6, 30), (1, 31)]
    week_2010 = [(), (4, 31), (0, 28), (6, 31), (2, 30), (4, 31), (0, 30), (2, 31), (5, 31), (1, 30), (3, 31), (6, 30), (1, 31)]
    if self.year == "2008":
      weeks = week_2008
    if self.year == "2009":
      weeks = week_2009
      feiertage = feiertage_2009
    if self.year == "2010":
      weeks = week_2010
      feiertage = feiertage_2010

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

  FellEnd= {
    'name':
      'Fell End',
    'belongs_to':
      ['FellEnd.Bohmwick-english.de', 'FellEnd.Booth-english.en', 'FellEnd.DebbieJulian-english.en', 'FellEnd.DebbiePaul-english.en', 'FellEnd.HelgaColin-english.en',
       'FellEnd.Janetta-english.en', 'FellEnd.Larissa-english.en', 'FellEnd.Steffi-english.en'],
    'calendar_caption':
      "These pictures were taken in Fell end in July 2009",
    'print_location_index':
      ['location']
  }
  
  Sheep = {
    'name':
      'Sheep',
    'belongs_to':
      ['Johannes-german.de', 'Hazel-english.en', 'Oleg-english.en', 'SuziSimon-english.en'],
    'calendar_caption':
      "These sheep were photographed in various locations around the globe",
    'print_location_index':
      ['country', 'location']
  }

  NZ = {
    'name':
      'New Zealand',
    'belongs_to':
      ['Christine-german.de', 'Ratz-german.de', 'Dieter-german.de', 'Nadine-german.de', 'Sebastian-german.de', 'KateRich-english.sc', 'OlgaDima-english.en',
       'Catherine-english.en', 'Victoria-english.en', 'David-english.en', 'KarenJames-english.en', 'MargaretRichard-enlgish.en', 'Marcus-enlgish.nz', 'Paul-english.en',
       'Karen-english.en',],
    'calendar_caption':
      "These images were taken in December 2008 and January 2009 - many on the spectacular Banks Peninsula, close to Christchurch on the east coast of New Zealands's South Island.",
    'print_location_index':
      ['location']
  }
  
  Istanbul = {
    'name':
      'Istanbul',
    'belongs_to':
      ['Zoltan-english.en', 'Olly-english.en', 'Mathias-english.en', 'Leigh-english.en', 'Luc-english.en', 'Richard-english.en', 'Judith-english.en',],
    'calendar_caption':
      "A selection of images taken when walking around in Istanbul during the European Crytallographic Meeting in August 2009",
    'print_location_index':
      ['location']
  }

  Amorgos = {
    'name':
      'Amorgos',
    'belongs_to':
      ['Carsten-greek.de', 'Volker-greek.de', 'Walter-greek.de', 'Dina-greek.gr', 'Periklies-greek.gr', 'Kallioope-greek.gr',
       'Sabine-greek.gr', 'Thomas-greek.de', 'Manfred-greek.gr', 'CarolineOliver-greek.gr', 'Doris-greek.gr', 'Marco-greek.gr',
       'FerdinandTraudel-greek.gr', 'MartinaJack-greek.gr', 'Heribert-german.de'],
    'calendar_caption':
      "All images were taken in Amorgos in September 2009",
    'print_location_index':
      ['location']
  }
  
  CountryShows = {
    'name':
      'Country Shows',
    'belongs_to':
      ['Annette-german.de', 'Graeme-english.sc', 'Colin-english.en', 'Ehmke-english.en', 'LoraineJimmy-english.en', 'LindaDave-english.en', 'Jenny-english.en', 'Gerry-german.nz'],
    'calendar_caption':
      "These pictures were taken at two agricultural shows in the North East of England: The Slayley Show in August 2009 and The Blanchland Show in September 2009",
    'print_location_index':
      ['location']
  }
  
  Ballon = {
    'name':
      'Balloon',
    'belongs_to':
      ['Balloon.Oma-german.de', 'Birgit-german.de', 'Doph-english.en', 'Chris-german.de', 'Emma-english.sc', 
       'Father-english.sc', 'Granny-english.en', 'Holly-english.en', ],
    'calendar_caption':
      "",
    'print_location_index':
      ['location']
  }

  Callist = Ballon
  name = Callist['name']
  calendar_caption = Callist['calendar_caption']
  print_location_index = Callist['print_location_index']
  
  for cal_name in Callist['belongs_to']:

    if "-" in cal_name:
      language = cal_name.split("-")[1].split(".")[0]
      holidays = cal_name.split("-")[1].split(".")[1]
      belongs_to = cal_name.split("-")[0]
      if "." in belongs_to:
        cal_name = cal_name.split("-")[0]
        belongs_to = cal_name.split(".")[1]
      else:
        cal_name = name
    
    if "." in cal_name:
      belongs_to = cal_name.split('.')[1]
    
    basedir = 'C:/Users/Horst/Pictures/Output/Calendars/' 
    output_dir = 'C:/Users/Horst/Pictures/Output/Calendars/' 
    print u"Making %s" %cal_name
    print u"Making Calendar"
    year = "2010"
    bw = False
    feiertage = True
    a = Calendar(year = year, language = language, cal_name = cal_name, basedir = basedir, bw = bw, feiertage = feiertage, print_location_in_index = print_location_in_index, belongs_to = belongs_to, holidays = holidays, calendar_caption = calendar_caption, output_dir = output_dir)
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
