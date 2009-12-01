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
# Image size half: 2122 x 1145

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
   
Lyall_Bay=\
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
     'headline':'Coromandel Town',
    'caption':'The main town of the beautiful Coromandel Penisnula is really no more than a small sleepy village.'}

Castlepoint=\
    {'name':'Castlepoint',
    'caption':'Castlepoint is hidden well away on the Wairarapa coast. It has one of New Zealand\'s oldest lighthouses.'}

Milford_Sound=\
    {'name':'Milford Sound',
    'caption':'In the middle of the vast Southland National Park is Milford Sound, one of the few accessible places on the wild southern West Coast of the South Island'}

Mitre_Peak=\
    {'name':'Mitre Peak',
     'map':'Milford Sound',
    'caption':'Possibly one of New Zealand\'s best known landmarks: Mitre Peak rising out of Milford Sound.'}

Variable_Oystercatcher=\
    {'name':'Variable Oystercatcher',
     'map':'Banks Peninsula',
    'caption':'These birds are common along the coastlines of the South Island. This showed his displeasure about being photographed in Le Bons Bay, Banks Peninsula'}

Tui=\
    {'name':'Tui',
     'map':'Kapiti Island',
    'caption':'One of the few surviving indigeneous bird species: The Tui. Although not common, numbers are increasing. This one was photographed on Kapiti Island.'}

Homewood=\
    {'name':'Homewood',
     'caption':'South of Riversdale in the Wairarapa, the tar seal will stop and the road continues as a metal road. Along this road, the world seems to end.'}

Tongariro_National_Park=\
    {'name':'Tongariro National Park',
     'caption':'The Tongariro Crossing, one of the \'Great Walks\', leads through some wonderous volcanically active landscapes.'}

Lake_Hawea=\
    {'name':'Lake Hawea',
     'caption':'The road connecting Wanaka via the Haast Pass to the West coast winds along Lake Hawea for a while.'}

Arthurs_Pass=\
    {'name':'Arthur\'s Pass',
     'map':'Arthur\'s Pass',
     'caption':'The Southern Alps can be crossed only in a few places. One of the more spectacular ones is Arthur\'s Pass.'}

Waimakariri_River=\
    {'name':'Waimakariri River',
     'map':'Arthur\'s Pass',
     'caption':'The vast flood plain of the Waimakariri River on the east side of Arthur\'s Pass'}

Arthurs_Pass_Forest=\
    {'name':'Arthur\'s Pass Forest',
     'map':'Arthur\'s Pass',
     'caption':'Arthur\' Pass National Park has many different types of native bush, depending on the height of the terrain.'}

Rotorua=\
    {'name':'Rotorua',
     'caption':'This boiling waterfall is in a thermal field very near to Rotorua: Hell\'s Gate'}

Lost_Soles=\
    {'name':'Lost Soles',
     'map':'Castlepoint',
     'caption':'Castlepoint is a strange spot in more than on way!'}

Aylesbury=\
    {'name':'Aylesbury',
     'caption':'The TansAlpine railway runs once a day in each direction between Christchurch and Greymouth across Arthur\' Pass'}

Martinborough=\
    {'name':'Martinborough',
     'caption':'This small town in the Wairarapa has become famous for its ecellent Pinot Noir and Riesling wines.'}

Napier=\
    {'name':'Napier',
     'caption':'Napier was once one of the leading wool exporting ports of the country. This is one of the woolsheds on the quayside.'}

The_Catlins=\
    {'name':'The Catlins',
     'caption':'Situated on the south-east coast of the South Island, this virtually unknown area is fantastic for all kinds of wildlife.'}

Punakaiki=\
    {'name':'Punakaiki',
     'caption':'Also known as \'Pancake Rocks\', these rock formations are a major tourist attraction on the West Coast.'}

Kapiti_Island=\
    {'name':'Kapiti Island',
     'caption':'Kapiti Island has been rodent-free for the last 15 years. It is a conservation area, where human access is strictly controlled.'}

Fern_Frond=\
    {'name':'Fern Frond',
     'caption':'Ferns grow everywhere in New Zealand. There are very many different species, many of which are indigenous to the country.'}

Motupiko=\
    {'name':'Motupiko',
     'caption':'A wee church'}

Tiniroto=\
    {'name':'Tiniroto',
     'caption':'On the inland road leading from Wairoa to Gisborne'}

Pongaroa=\
    {'name':'Pongaroa',
     'caption':'In the northern Wairarapa.'}

The_Beehive=\
    {'name':'The Beehive',
     'caption':'Wellington'}

Wellington_Railway_Station=\
    {'name':'Wellington Railway Station',
     'caption':'Wellington.'}

Lake_Ferry=\
    {'name':'Lake Ferry',
     'caption':'wairarapa'}

Taupo=\
    {'name':'Taupo',
     'caption':'trees'}

Lake_Taupo=\
    {'name':'Lake Taupo',
     'caption':'Lake'}

Mitre_Peak_2=\
    {'name':'Mitre Peak 2',
     'caption':'Peak'}

Civic_Square=\
    {'name':'Civic Square',
     'caption':'Balls'}

pages = [(Hamilton,Coromandel),#ok
         (Ahikiwi,Wairarapa),#ok
         (Castlepoint,Ninety_Mile_Beach),#ok
         (Milford_Sound,Mitre_Peak),#ok
         (Variable_Oystercatcher,Tui),#ok
         (Homewood, Lyall_Bay),#ok
         (Tongariro_National_Park,Lake_Hawea),#ok
         (Flea_Bay, Little_Blue_Penguin),#ok
         (Fern_Frond,Arthurs_Pass_Forest),#ok
         (Lost_Soles, Aylesbury),#ok
         (Martinborough, The_Catlins),#ok
         (Kapiti_Island, Taupo),
         (Waimakariri_River, Punakaiki),
         (Lake_Taupo, Civic_Square),
         (Cathedral_Cove, Mitre_Peak_2),
         (Motupiko, Rotorua),#ok
         (Tiniroto, Pongaroa),
         (The_Beehive, Wellington_Railway_Station),#ok
         
         (Arthurs_Pass,),#ok
         (Te_Marua,),#ok
         (Lake_Ferry,),#ok
         (Auckland,),#ok

         ]

image_src = r"C:\Users\Horst\Pictures\Output\Books\NZ\src"
output_folder = r"C:\Users\Horst\Pictures\Output\Books\NZ"

width = 5138
height = 3416

margin = 48
marg_x = 40

marg_y = 30

left_image_x = 450
max_text_width = left_image_x - margin - marg_x - 30
#print "Max txt width: %i" %max_text_width

marg_x_map = (left_image_x  - 282)

marg_x_map = (marg_x)

bg_col = '#ffffff'

fontname_big = "GILB____.TTF"
fontname_small = "GIL_____.TTF"

font_size_big = 52
font_size_small = 40

t_align_right_page = "left"

font_big = ImageFont.truetype("%s" %fontname_big, font_size_big)
font_small = ImageFont.truetype("%s" %fontname_small, font_size_small)



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
            draw.rectangle((margin,margin,width-margin,height-margin), fill='#ffdddd')
        name = imd['name']
        picture = imd.get('src', name)
        picture = Image.open("%s/%s.jpg" %(image_src, picture))
        header = imd.get('header', name)
        map = imd.get('map', name)
        try:
            map = Image.open("%s/%s.png" %(image_src, map))
        except:
            print("No Map: %s!" %map)
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


