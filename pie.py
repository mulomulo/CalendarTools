#-*- coding:utf8 -*-

from __future__ import division
#import PngImagePlugin
import Image
import ImageFont, ImageDraw, ImageChops, ImageStat, ImageEnhance
import math

fontname_bold = "GILB____.TTF"
fontname_normal = "GIL_____.TTF"

font_bar_labels = ImageFont.truetype("%s" %fontname_bold, 60)
font_bar_title  = ImageFont.truetype("%s" %fontname_bold, 80)

grey = '#dedede'

headline_colour = '#335588'

def save_file(IM,name,q):
  try:
    savename = "%s/%s-%s.png" %(basedir,q,name[:15])
    savename = savename.replace('"','')
    IM.save(savename)
  except:
    savename = "%s/%s.png" %(basedir,"FAILED.png")
    IM.save(savename)

def get_transpose(o_l):
  i = 0
  t_l = []

  for line in o_l:
    line_l = line.split("\t")
    j = 0
    for item in line_l:
      if j == 0 and i == 0:
        for k in range(len(line_l)):
          t_l.append("")
      item = item.strip()
      t_l[j] += "%s\t" %item
      print "%s\t" %item
      j +=1
    i += 1
  return t_l


def get_survey_file_l(filename):
  rFile = open(filename,'r')
  survey_l = rFile.readlines()
  rFile.close()

  transpose = get_transpose(survey_l)

  return transpose


def get_choice_answers(txt_l):
  for line in txt_l:
    no_answer = 0
    bits = {}
#    print "\n-------------------------"
    line_l = line.split("\t")
    total_n = len(line_l)
    try:
      title = line_l[2].strip("?")
      title = line_l[2].replace("?","")
      title = title.strip('"')
      title = title.strip()

      q = line_l[0]
    except:
      continue
#    print "%s" %title
#    print "-------------------------"
    for bit in line_l:
      bit = bit.strip()
      bit = bit.replace('"','')
      if not bit:
        no_answer += 1
        print no_answer,
      if bit.startswith("Q"):
        no_answer -= 1
        continue
      if "," in bit and len(bit) < 40:
        bi = bit.split(",")
        for b in bi:
          b = b.strip()
          bits.setdefault(b,0)
          bits[b] += 1
      elif len(bit) < 20:
        bit = bit.strip()
        bits.setdefault(bit,0)
        bits[bit] += 1
    if len(bits) > 15:
      continue

    if bits.has_key("yes") and bits.has_key("no"):
      no_n = bits["no"]
      yes_n = bits["yes"]
      na_n = total_n - no_n - yes_n
      no = no_n/total_n
      yes = yes_n/total_n
      na = na_n/total_n
      print ("%s -- Yes: %.2f (%s), No: %.2f (%s), No answer: %.2f(%s) -- Check: %.2f, %i" %(title, yes, yes_n, no, no_n, na, na_n, yes + no + na, total_n - yes_n - no_n - na_n))
      make_pie_graph(yes_n=yes_n, no_n=no_n, total_n=total_n, name=title, q = q)

    else:
      l = []
      ok = False
      defin = ['not at all', 'a bit', 'a lot', 'very much',
               'very satisfied', 'satisfied', 'indifferent', 'not satisfied',  'n/a',
               'daytime', 'evenings', 'weekends', 'no problems',
               'not an issue', 'slighly upset', 'not bothered', 'slightly upset', 'very upset',
               '19-25', '26-35', '36-45', '46-55', '56-65', '66-75', '76-85', 'over 85',
               'up to 1 year', '1-3 years', '4-10 years', '11-20 years', 'more than 20 years', 'all my life',
               'bus', 'taxi'
               ]
      accounted_for = 0
      for term in defin:
        try:
          l.append((term,bits[term]))
          ok = True
          accounted_for += bits[term]
        except Exception, err:
          print err
      if ok:

        #l.append(("no answer", total_n-accounted_for))
        l.append(("no answer", no_answer))
        print no_answer
        no_answer = 0
        make_bar_graph(l, total_n, name=title, q=q)

      else:
        for bit in bits:
          l.append((bit,bits[bit]))
        make_bar_graph(l, total_n, name=title, q=q)



def make_bar_graph(l, total, name='fred', q='1'):
  text_margin = 20
  bar_height = 100
  bar_gap = 30
  title_height = 160
  height = title_height + bar_height * len(l) + bar_gap * (len(l) -1)
  colour = "#ffffff"
  width = 1800
  size = (width,height)
  IM = Image.new('RGBA', size, colour)
  draw = ImageDraw.Draw(IM)

  draw.text((0, 0), "%s" %name, font=font_bar_title, fill=headline_colour)

  max = 0
  for item in l:
    if item[1] > max:
      max = item[1]

  i = 0
  colours = ["#00aa00","#228800","#882200","#aa0000",grey]
  for item in l:
    val = item[1]/max
    var = item[0]
    x = 0
    y = i * (bar_height + bar_gap) + title_height
    dx = int(width * val)
    dy = bar_height + y
    try:
      colour = colours[i]
    except:
      colour = grey
    if "age group" in name or "Which school" in name or "How long have" in name or "Which nursery" in name:
      colour = grey
    if "no answer" in var:
      colour = grey

    draw.rectangle((x, y, dx, dy), fill=colour)


    txt = "%s (%s)" %(var,item[1])
    wX, wY = draw.textsize("%s " %txt, font=font_bar_labels)
    tx = dx - wX - text_margin
    ty = int(y + (bar_height - wY)/2)
    if tx < wX + text_margin:
      tx = dx + text_margin
    draw.text((tx, ty), "%s" %txt, font=font_bar_labels, fill='#ababab')

    i += 1

  save_file(IM, name, q)




def make_pie_graph(yes_n=60, no_n=40, total_n=100, name='fred', q="1"):
  no = no_n/total_n
  yes = yes_n/total_n

  na_n = total_n - yes_n - no_n
  na = na_n/total_n

  colour = "#ffffff"
  size = (1800,950)
  IM = Image.new('RGBA', size, colour)
  draw = ImageDraw.Draw(IM)
  legend_left = 950
  border_width = 5
  font_pie_title  = ImageFont.truetype("%s" %fontname_bold, 80)
  font_pie_legend  = ImageFont.truetype("%s" %fontname_normal, 105)
  lt = 500
  ls = 130
  legg = 170
  legend_top = 40
  rad = 900
  rotation = -90
  margin = 0

  max_width = size[0] - legend_left

  tit = name.split()

  l = []
  txt = ""
  w = 0
  for bit in tit:
    wX, wY = draw.textsize("%s " %bit, font=font_bar_title)
    if w + wX < max_width:
      w += wX
      txt += "%s " %bit
    else:
      l.append(txt)
      txt = "%s " %bit
      w = wX
  l.append("%s?" %txt.strip())

  i = 0
  for line in l:
    y = i * 90 + legend_top
    draw.text((legend_left, y), "%s" %line, font=font_pie_title, fill=headline_colour)
    i += 1

  border_colour = "#dedede"
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

  yes_end = int(360*yes)
  no_end = int(360*yes) + int(360*no)

  a = margin/2+rad/2+border_width/2
  b = margin/2+rad/2+border_width/2

  #draw.rectangle((a-5, b-5, a + 5, b + 5), fill="#ff0000")

  x = a + 160 * math.cos(yes_end+90)
  y = b + 160 * math.sin(yes_end+90)


  x = a + 160 * math.cos(no_end+90)
  y = b + 160 * math.sin(no_end+90)

  lll = legend_left + 40
  draw.text((lll, lt), "yes:", font=font_pie_legend, fill=pie_colour_yes)
  draw.text((lll, lt+ls), "no:", font=font_pie_legend, fill=pie_colour_no)
  draw.text((lll, lt+ls*2), "n/a:", font=font_pie_legend, fill='#999999')

  draw.text((lll+legg, lt), "%.0f%% (%i)" %(yes*100, yes_n), font=font_pie_legend, fill=pie_colour_yes)
  draw.text((lll+legg, lt+ls), "%.0f%% (%i)" %(no*100, no_n), font=font_pie_legend, fill=pie_colour_no)
  draw.text((lll+legg, lt+ls*2), "%.0f%% (%i)" %(na*100, na_n), font=font_pie_legend, fill='#999999')

  #draw.line((lx , ly, ldx, ldy), fill=border_colour, width=border_width/2)
  #draw.line((x_begin_no, y_begin_no, x_end_no, y_end_no), fill=border_colour, width=border_width/2)

  save_file(IM, name, q)

basedir = "C:/Users/Horst/Documents/SurveyResult"
filename = "All"
survey_l = get_survey_file_l(("%s/%s.txt" %(basedir,filename)))
#get_yes_no_answers(survey_l)
get_choice_answers(survey_l)


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
        make_pie_graph(yes=yes, no=no, name=title, q = q)
      except Exception, err:
        print("Error %s" %err)
