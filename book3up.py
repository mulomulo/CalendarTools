from __future__ import division
import PngImagePlugin
import JpegImagePlugin
import IptcImagePlugin as IPTC
import Image
import glob, os
import ImageFont, ImageDraw, ImageChops, ImageStat, ImageEnhance
import string
import sys


def draw_text(draw, text, font, x, y, fill='#ababab', max_width = 200, line_spacing = 50):
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
        curr_y = y + j * line_spacing
        draw.text((x, curr_y), "%s" %l, font=font, fill=fill)
        j += 1

    return curr_y + wY
    
book = [

    #{'name':'Te Marua',
    #'map':'Te Marua',
    #'header':'Te Marua',
    #'caption':'Just north of Wellington lies the Te Marua area. Part of the Tararua Forest Park, much of Wellington\'s watersupply originates in this native rainforest area.',
    #'src':"Te Marua"},
    
    #{'name':'Auckland',
    #'caption':'Auckland is New Zealand\s biggest city - with just over 1M people it is by no means a big city though.'},

    #{'name':'Golden Bay',
    #'caption':'The Golden Bay area is separated by the rest of the South Island by the Takaka Hills.'},
    
    #{'name':'Marlborough Sounds',
    #'caption':'At the top of the South Island - most of it accessible only by boat. This is a truly magical area of New Zealand.'},

    #{'name':'Picton',
    #'caption':'Sometimes known as the \'Gateway to the Sout Island\' this town links the North Island with the South Island because of it\' Interislander Ferry Terminal'},

    #{'name':'Lake Ferry',
    #'caption':'Situated at the southern tip of the North Island, in the Wairarapa region, this area feels well and truly like the end of the world.'},

    {'name':'Featherston',
    'caption':'A half hour drive away from Wellington over the Rimutaka Hills, the first town of the Wairarapa is Featherston.'},
   
    {'name':'1',
    'caption':'A half hour drive away from Wellington over the Rimutaka Hills, the first town of the Wairarapa is Featherston.'},

    {'name':'2',
     'left':True,
    'caption':'A half hour drive away from Wellington over the Rimutaka Hills, the first town of the Wairarapa is Featherston.'},
    
]

image_src = "C:\Users\Horst\Pictures\Output\Books\NZ\src"
output_folder = "C:\Users\Horst\Pictures\Output\Books\NZ"

width = 5138
height = 3416

margin = 48
marg_x = 40

marg_y = 40

left_image_x = 450
max_text_width = left_image_x - margin - marg_x - 30
print "Max txt width: %i" %max_text_width

marg_x_map = (left_image_x + margin - 282)/2


bg_col = '#ffffff'

fontname_big = "GILB____.TTF"
fontname_small = "GIL_____.TTF"

font_size_big = 52
font_size_small = 40

font_big = ImageFont.truetype("%s" %fontname_big, font_size_big)
font_small = ImageFont.truetype("%s" %fontname_small, font_size_small)



#draw.rectangle((margin,margin,width-margin,height-margin), fill='#ffdddd')
#draw.rectangle((margin,margin,left_image_x,height-margin), fill='#ff0000')

image_height = (height-2*margin)/3

y_l = [margin, margin+image_height, margin+image_height * 2]

continue_on_page = False
for imd in book:
    left = False
    if not continue_on_page:
        IM = Image.new('RGBA', (width, height), bg_col)
        draw = ImageDraw.Draw(IM)
    
    name = imd['name']
    picture = imd.get('src', name)
    picture = Image.open("%s/%s.jpg" %(image_src, picture))
    header = imd.get('header', name)
    map = imd.get('map', name)
    map = Image.open("%s/%s.png" %(image_src, map))
    caption = imd['caption']
    left = imd.get('left', False)
    
    print "Now making page %s" %name
    
    i = 0
    
    if not continue_on_page:
        for y in y_l:
            y = int(y)
            #draw.line((0, y, width, y), fill='#ababab')
            #draw.text((margin + marg_x, marg_y + y), "%s" %text, font=font_big, fill='#888888')
            x = margin + marg_x
            curr_y = draw_text(draw, text=header, x=x, y=marg_y + y, font=font_big, fill='#888888', max_width = max_text_width)
            curr_y = draw_text(draw, text=caption, x=x, y=curr_y + 20, font=font_small, fill='#ababab', max_width = max_text_width)
            if i == 0:
                y_adjust = margin - 10
            else:
                y_adjust = 0
            IM.paste(picture, (left_image_x, y - y_adjust))
            if picture.size[0] < 3000:
                continue_on_page = True
                extra_name = name
            #draw.rectangle((left_image_x, y, width-margin, y + image_height-2), fill='#88ff88')
            IM.paste(map, (margin + marg_x_map, y + image_height - 320))
            i += 1
        if not continue_on_page:
            IM.save("%s\%s.jpg" %(output_folder,name), "JPEG", quality=100)
        
    else:
        for y in y_l:
            y = int(y)
            #draw.line((0, y, width, y), fill='#ababab')
            #draw.text((margin + marg_x, marg_y + y), "%s" %text, font=font_big, fill='#888888')
            if left:
                x = width/2 + margin + marg_x
            else:
                x = width - left_image_x + marg_x
            curr_y = draw_text(draw, text=header, x=x, y=marg_y + y, font=font_big, fill='#888888', max_width = max_text_width)
            curr_y = draw_text(draw, text=caption, x=x, y=curr_y + 20, font=font_small, fill='#ababab', max_width = max_text_width)
            IM.paste(map, (x, y + image_height - 320))
            if i == 0:
                y_adjust = margin - 10
            else:
                y_adjust = 0

            if left:
                x = width/2 + marg_x + left_image_x
            else:
                x = width/2
            IM.paste(picture, (x, y - y_adjust))
            continue_on_page = False
            #draw.rectangle((left_image_x, y, width-margin, y + image_height-2), fill='#88ff88')
            i += 1
        IM.save("%s\%s and %s.jpg" %(output_folder,extra_name,name), "JPEG", quality=100)
    

print "Done."


