from __future__ import division
import PngImagePlugin
import JpegImagePlugin
import IptcImagePlugin as IPTC
import Image
import glob, os
import ImageFont, ImageDraw, ImageChops, ImageStat, ImageEnhance
import string
import sys


# Image size full: 4685 x 1145
# Image size half: 2119 x 1139

def draw_text(draw, text, font, x, y, fill='#ababab', max_width = 200, line_spacing = 50, align='left'):
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
    
Te_Marua=\
    {'name':'Te Marua',
    'map':'Te Marua',
    'header':'Te Marua',
    'caption':'Just north of Wellington lies the Te Marua area. Part of the Tararua Forest Park, much of Wellington\'s watersupply originates in this native rainforest area.',
    'src':"Te Marua"}

Auckland=\
    {'name':'Auckland',
    'caption':'Auckland is New Zealand\s biggest city - with just over 1M people it is by no means a big city though.'}

Golden_Bay=\
    {'name':'Golden Bay',
    'caption':'The Golden Bay area is separated by the rest of the South Island by the Takaka Hills.'}

Marlborough_Sounds=\
    {'name':'Marlborough Sounds',
     'caption':'At the top of the South Island - most of it accessible only by boat. This is a truly magical area of New Zealand.'}
    
Picton=\
    {'name':'Picton',
    'caption':'Sometimes known as the \'Gateway to the Sout Island\' this town links the North Island with the South Island because of it\' Interislander Ferry Terminal'}
    
Lake_Ferry=\
    {'name':'Lake Ferry',
    'caption':'Situated at the southern tip of the North Island, in the Wairarapa region, this area feels well and truly like the end of the world.'}

Featherston=\
    {'name':'Featherston',
    'caption':'A half hour drive away from Wellington over the Rimutaka Hills, the first town of the Wairarapa is Featherston.'}
   
Lyal_Bay=\
    {'name':'Lyall Bay',
    'caption':'On Wellington\'s south coast, preparations for a music video by ... were well under way.'}

Northland=\
    {'name':'Northland',
    'caption':'At the very far North of New Zealand, the region of Northland is known for it\'s almost subtropical climate. Banana plants have no trouble growing here'}

Ninety_Mile_Beach=\
    {'name':'90 Mile Beach',
    'caption':'The name promises more than there really is - the wide sandy beach is only about 50 miles long.'}

Cathedral_Cove=\
    {'name':'Cathedral Cove',
    'caption':'The beaches of the Coromandel Peninsula are famous. Perhaps none is as famous as this much-visited stretch of coast by Cathredral Coast, which has finally been granted marine sanctuary status.'}

Taranaki_Coast=\
    {'name':'Taranaki Coast',
    'caption':'The stretch of coast to the north of Taranaki is characterised by it\'s black sandy beaches. There are a few caravan sites situated there that seem to come from a different place and time.'}

East_Cape=\
    {'name':'East Cape',
    'caption':'One of the North Island\'s least touched regions, the East Cape is a magnificent and very special piece of land.'}

Waiapu=\
    {'name':'Waiapu',
    'caption':'On the long road around the East Cape, there are a few places like Waiapu.'}

Ahikiwi=\
    {'name':'Ahikiwi',
    'caption':'Along SH 12 near Ahikiwi. This far north, the green is intense. This is in stark contrast with the blue of the sea and the sky and with the white of the clounds'}

Wairarapa=\
    {'name':'Wairarapa',
    'caption':'At the other end of the North Island, the Wairarapa dries out more or less completely towards the end of the summer.'}

    
Little_River=\
    {'name':'Little River',
    'caption':'The first place on Banks Peninsula you encounter is Little River. Once, this place had a railway station and must have been bustling with life.'}

Close=\
    {'name':'Closed',
    'map':'Little River',
    'caption':'Now, most people head straight for the more famous town of Akaroa. Outside the main tourist season, Little River sleeps.'}

Flea_Bay=\
    {'name':'Flea Bay',
    'caption':'On the southen coast of Banks Peninsula, this little bay has been declared a marine reserve. It is also inaccessible by land.'}

Little_Blue_Penguin=\
    {'name':'Little Blue Penguin',
    'map':'Flea Bay',
    'caption':'Flea Bay is home to around 1000 Little Blue Penguins. A few years ago, there were around 20. Due to the efforts of one farmer, the population could be re-esablished.'}

Hamilton=\
    {'name':'Hamilton',
    'caption':'The facade of a music store in Hamilton. Unusual and colourful shop-fronts are common in New Zealand.'}

Coromandel=\
    {'name':'Coromandel',
    'header':'Coromandel Town',
    'caption':'The main town of the beautiful Coromandel Penisnula is really no more than a small sleepy village.'}

pages = [(Ninety_Mile_Beach,Northland),
         (Flea_Bay,Little_Blue_Penguin),
         (Ninety_Mile_Beach,Northland)]

image_src = r"C:\Users\Horst\Pictures\Output\Books\NZ\src"
output_folder = r"C:\Users\Horst\Pictures\Output\Books\NZ"

width = 5138
height = 3416

margin = 48
marg_x = 40

marg_y = 40

left_image_x = 450
max_text_width = left_image_x - margin - marg_x - 30
#print "Max txt width: %i" %max_text_width

marg_x_map = (left_image_x + margin - 282)/2


bg_col = '#ffffff'

fontname_big = "GILB____.TTF"
fontname_small = "GIL_____.TTF"

font_size_big = 52
font_size_small = 40

t_align_right_page = "left"

font_big = ImageFont.truetype("%s" %fontname_big, font_size_big)
font_small = ImageFont.truetype("%s" %fontname_small, font_size_small)



#draw.rectangle((margin,margin,width-margin,height-margin), fill='#ffdddd')
#draw.rectangle((margin,margin,left_image_x,height-margin), fill='#ff0000')

image_height = int((height-2*margin)/3)

y_l = [margin, margin+image_height, margin+image_height * 2]

continue_on_page = False
for page in pages:
    for imd in page:
        left = False
        if not continue_on_page:
            IM = Image.new('RGBA', (width, height), bg_col)
            draw = ImageDraw.Draw(IM)
        
        name = imd['name']
        picture = imd.get('src', name)
        picture = Image.open("%s/%s.jpg" %(image_src, picture))
        header = imd.get('header', name)
        map = imd.get('map', name)
        try:
            map = Image.open("%s/%s.png" %(image_src, map))
        except:
            print("No Map!")
        caption = imd['caption']
        left = imd.get('left', False)
        
        print("Now making page %s" %name)
        
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
                try:
                    IM.paste(map, (margin + marg_x_map, y + image_height - 320))
                except:
                    pass
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
                curr_y = draw_text(draw, text=header, x=x, y=marg_y + y, font=font_big, fill='#888888', max_width = max_text_width, align=t_align_right_page)
                curr_y = draw_text(draw, text=caption, x=x, y=curr_y + 20, font=font_small, fill='#ababab', max_width = max_text_width, align=t_align_right_page)
                try:
                    IM.paste(map, (x, y + image_height - 320))
                except:
                    pass
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
            print("Page saved")
    

print("Done.")


