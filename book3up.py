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


class PhotobookPageMaker(object):
  def __init__(self):
    import ImageTools
    self.IT = ImageTools.ImageTools()
    self.get_parameters()

  def define_page_contents(self):
    self.pages, self.iptc = self.IT.get_images_in_folder_list(src_folder=self.image_src)
    
  def define_page_contents_old(self,):
    self.Te_Marua=\
            {'name':'Te Marua',
             'map':'Te Marua',
             'header':'Te Marua',
             'caption':'Just north of Wellington lies the Te Marua area, part of the Tararua Forest Park. Much of Wellington\'s water supply originates in this native rainforest area.',
             'src':"Te Marua"}
    
    self.Auckland=\
            {'name':'Auckland',
             'caption':'Auckland is New Zealand\'s biggest city with 1.3M people. It is by no means a huge city in terms of population. It is, however very large in area.'}
    
    self.Golden_Bay=\
              {'name':'Golden Bay',
               'caption':'The Golden Bay area is separated from the rest of the South Island by the Takaka Hills.'}
    
    self.Marlborough_Sounds=\
                      {'name':'Marlborough Sounds',
                       'caption':'At the top of the South Island - most of it is accessible only by boat. This is a truly magical area of New Zealand.'}
    
    self.Picton=\
          {'name':'Picton',
           'caption':'Sometimes known as the \'Gateway to the South Island\'. This town links the North Island with the South Island with the Interislander Ferry Terminal'}
    
    self.Lake_Ferry=\
              {'name':'Lake Ferry',
               'caption':'Situated at the southern tip of the North Island, in the Wairarapa region. This area feels well and truly like the end of the world.'}
    
    self.Featherston=\
               {'name':'Featherston',
                'caption':'A half hour drive away from Wellington over the Rimutaka Hills. The first town of the Wairarapa is Featherston.'}
    
    self.Lyall_Bay=\
             {'name':'Lyall Bay',
              'caption':'Preparations for a music video by \'The Phoenix Foundation\' were well under way.'}
    
    self.Lyall_Bay_Long=\
                  {'name':'Lyall Bay Long',
                   'header':'Lyall Bay',
                   'map':'Wellington',
                   'caption':'Preparations for a music video by \'The Phoenix Foundation\' were well under way.'}
    
    self.Northland=\
             {'name':'Northland',
              'caption':'At the very far north of New Zealand, the region of Northland is known for it\'s almost subtropical climate. Banana plants have no trouble growing here'}
    
    self.Ninety_Mile_Beach=\
                     {'name':'90 Mile Beach',
                      'caption':'The name promises more than there really is - the wide sandy beach is only about 50 miles long.'}
    
    self.Cathedral_Cove=\
                  {'name':'Cathedral Cove',
                   'caption':'The beaches of the Coromandel Peninsula are famous. This much-visited stretch of coast by Cathedral Cove, has finally been granted marine sanctuary status.'}
    
    self.Taranaki_Coast=\
                  {'name':'Taranaki Coast',
                   'caption':'The stretch of coast to the north of Taranaki is characterised by it\'s black sandy beaches. There are a few caravan sites situated there that seem to come from a different place and time.'}
    
    self.East_Cape=\
             {'name':'East Cape',
              'caption':'One of the North Island\'s least touched regions, the East Cape is a magnificent and very special area.'}
    
    self.Waiapu=\
          {'name':'Waiapu',
           'caption':'On the long road around the East Cape, there are a few places like Waiapu.'}
    
    self.Ahikiwi=\
           {'name':'Ahikiwi',
            'caption':'Along SH 12 near Ahikiwi. This far north, the green is intense. This is in stark contrast with the blue of the sea and the sky and with the white of the clouds'}
    
    self.Wairarapa=\
             {'name':'Wairarapa',
              'caption':'At the other end of the North Island, the Wairarapa becomes very dry at the end of the summer.'}
    
    
    self.Little_River=\
                {'name':'Little River',
                 'caption':'The first place encountered on Banks Peninsula is Little River. Once, this place had a railway station and must have been bustling with life.'}
    
    self.Close=\
         {'name':'Closed',
          'map':'Little River',
          'caption':'Now, most people head straight for the more famous town of Akaroa. Outside the main tourist season, Little River sleeps.'}
    
    self.Flea_Bay=\
            {'name':'Flea Bay',
             'caption':'On the southern coast of Banks Peninsula, this little bay has been declared a marine reserve. It is inaccessible by road.'}
    
    self.Korora=\
          {'name':'Korora',
           'map':'Flea Bay',
           'caption':'Flea Bay is home to around 1000 Little Blue Penguins. A few years ago, there were only 20. Thanks to the efforts of the landowners, the population has been re-established.'}
    
    self.Hamilton=\
            {'name':'Hamilton',
             'caption':'The facade of a music store in Hamilton. Unusual and colourful shop-fronts are common in New Zealand.'}
    
    self.Coromandel=\
              {'name':'Coromandel',
               'headline':'Coromandel Town',
               'caption':'The main town of the beautiful Coromandel Peninsula is really no more than a small sleepy village.'}
    
    self.Castlepoint=\
               {'name':'Castlepoint',
                'caption':'Castlepoint is hidden away on the Wairarapa coast. It has one of New Zealand\'s oldest lighthouses.'}
    
    self.Milford_Sound=\
                 {'name':'Milford Sound',
                  'caption':'In the middle of the vast Fiordland National Park is Milford Sound, one of the few accessible places on the wild southern West Coast of the South Island'}
    
    self.Mitre_Peak=\
              {'name':'Mitre Peak',
               'map':'Milford Sound',
               'caption':'One of New Zealand\'s best known landmarks: Mitre Peak rising out of Milford Sound.'}
    
    self.Variable_Oystercatcher=\
                          {'name':'Variable Oystercatcher',
                           'map':'Banks Peninsula',
                           'caption':'These birds are common along the coastlines of the South Island. This one showed his displeasure about being photographed in Le Bons Bay, Banks Peninsula'}
    
    self.Tui=\
       {'name':'Tui',
        'map':'Kapiti Island',
        'caption':'One of the few surviving endemic bird species: The Tui. Although not common, numbers are increasing. This one was photographed on Kapiti Island.'}
    
    self.Homewood=\
            {'name':'Homewood',
             'caption':'South of Riversdale in the Wairarapa, the tar seal stops and the road continues as a metal road. Along this road, the world seems to end.'}
    
    self.Homewood_Long=\
                 {'name':'Homewood Long',
                  'header':'Homewood',
                  'map':'Homewood',
                  'caption':'South of Riversdale in the Wairarapa, the tar seal stops and the road continues as a metal road. Along this road, the world seems to end.'}
    
    
    self.Tongariro_National_Park=\
                           {'name':'Tongariro National Park',
                            'caption':'The Tongariro Alpine Crossing is one of New Zealand\'s most spectacular one-day tracks, it leads through some wondrous volcanically active landscapes.'}
    
    self.Lake_Hawea=\
              {'name':'Lake Hawea',
               'caption':'The road connecting Wanaka via the Haast Pass to the West Coast winds along Lake Hawea for a while.'}
    
    self.Arthurs_Pass=\
                {'name':'Arthur\'s Pass',
                 'map':'Arthur\'s Pass',
                 'caption':'The Southern Alps can be crossed only in a few places. One of the more spectacular is Arthur\'s Pass.'}
    
    self.Waimakariri_River=\
                     {'name':'Waimakariri River',
                      'map':'Arthur\'s Pass',
                      'caption':'The vast flood plain of the Waimakariri River on the east side of Arthur\'s Pass'}
    
    self.Arthurs_Pass_Forest=\
                       {'name':'Arthur\'s Pass Forest',
                        'map':'Arthur\'s Pass',
                        'caption':'Arthur\'s Pass National Park has many different types of native bush, depending on the height of the terrain.'}
    
    self.Rotorua=\
           {'name':'Rotorua',
            'caption':'This boiling waterfall is in a thermal field very near to Rotorua: Hell\'s Gate'}
    
    self.Lost_Soles=\
              {'name':'Lost Soles',
               'map':'Castlepoint',
               'caption':'Castlepoint is a strange spot in more than one way!'}
    
    self.Aylesbury=\
             {'name':'Aylesbury',
              'caption':'The TranzAlpine train runs once a day in each direction between Christchurch and Greymouth through the magnificent Southern Alps'}
    
    self.Martinborough=\
                 {'name':'Martinborough',
                  'header':'West Wairarapa',
                  'caption':'Small chapel near Martinborough, a small town that has become famous for its excellent Pinot Noir and Riesling wines.'}
    
    self.Napier=\
          {'name':'Napier',
           'caption':'Napier was once one of the leading wool exporting ports of the country. This is one of the wool sheds on the quayside.'}
    
    self.The_Catlins=\
               {'name':'The Catlins',
                'caption':'Situated on the south-east coast of the South Island, this virtually unknown area is fantastic for all kinds of wildlife.'}
    
    self.Punakaiki=\
             {'name':'Punakaiki',
              'caption':'Also known as \'Pancake Rocks\', these rock formations are a major tourist attraction on the West Coast.'}
    
    self.Kapiti_Island=\
                 {'name':'Kapiti Island',
                  'caption':'Kapiti Island has been rodent-free for the last 15 years. It is a conservation area, where human access is strictly controlled.'}
    
    self.Fern_Frond=\
              {'name':'Fern Frond',
               'map':'nz',
               'caption':'Ferns grow everywhere in New Zealand. There are very many different species, many of which are indigenous to the country.'}
    
    self.Motupiko=\
            {'name':'Motupiko',
             'caption':'St George\'s Church'}
    
    self.Tiniroto=\
            {'name':'Tiniroto',
             'caption':'On the inland road leading from Wairoa to Gisborne'}
    
    self.Pongaroa=\
            {'name':'Pongaroa',
             'caption':'In the northern Wairarapa, this village has a population of around 30, but supports the surrounding farms, which brings the total population to around 300.'}
    
    self.The_Beehive=\
               {'name':'The Beehive',
                'map':'Wellington',
                'caption':'The Beehive is the common name for the executive wing of the New Zealand Parliament Buildings'}
    
    self.Wellington_Railway_Station=\
                              {'name':'Wellington Railway Station',
                               'map':'Wellington',
                               'caption':'There used to be a well-functioning railway system in New Zealand. Overland trains are now mainly a tourist attraction, with two Intercity trains between Wellington and Auckland each day.'}
    
    self.Lake_Ferry=\
              {'name':'Lake Ferry',
               'caption':'Lake Ferry is a small settlement between the shores of Lake Onoke and Palliser Bay'}
    
    self.Taupo=\
         {'name':'Taupo',
          'caption':'Taupo is a centre of volcanic and geothermal activity.'}
    
    self.Lake_Taupo=\
              {'name':'Lake Taupo',
               'caption':'Lake Taupo is New Zealand\'s largest lake.'}
    
    self.Mitre_Peak_2=\
                {'name':'Mitre Peak',
                 'map':'Milford Sound',
                 'caption':'Mitre Peak is a majestic peak. It resembles a bishop\'s headdress when viewed from the right direction'}
    
    self.Civic_Square=\
                {'name':'Civic Square',
                 'map':'Wellington',
                 'caption':'An iconic 3.4 metre diameter sphere of sculpted leaves of several ferns endemic to New Zealand is suspended 14 metres above the centre of the Civic Square'}
    
    self.Toi_Toi=\
           {'name':'Toi Toi',
            'map':'Castlepoint',
            'caption':'There are four species of grass native to New Zealand known as Toi Toi. The plant can grow up to 4 metres tall.'}
    
    self.Waterfall=\
             {'name':'Waterfall',
              'map':'Banks Peninsula',
              'caption':'Many waterfalls be seen on the Banks Peninsula Track.'}
    
    self.Boat_Houses=\
               {'name':'Wellington Boat Sheds',
                'map':'Wellington',
                'caption':'Boat Sheds in Oriental Bay'}
    
    self.Shed=\
        {'name':'Shed',
         'map':'Homewood',
         'caption':'In New Zealand sheds can be found nearly everywhere.'}
    
    self.Wellington_From_Matui_2=\
                           {'name':'Wellington from Matui 2',
                            'header':'Wellington from Matui/Somes',
                            'map':'Wellington',
                            'caption':'Matui/Somes was formerly a quarantine island. It is now a conservation area, where many native species are re-establishing themselves.'}
    
    self.Wellington_Airport=\
                      {'name':'Wellington Airport',
                       'map':'Wellington',
                       'caption':'Good Bye'}
    
    self.Mount_Victoria=\
                  {'name':'Mount Victoria',
                   'header':'Mount Victoria',
                   'map':'Wellington',
                   'caption':'Rising above the Overseas Terminal - now a marina - is Mt. Victoria. It is one of Wellington\' most thought after location.'}
  
  
  
  def define_pages(self):
    self.pages = [(Hamilton,Coromandel),#ok
             #(Ahikiwi,Wairarapa),#ok
             #(Castlepoint,Ninety_Mile_Beach),#ok
             #(Milford_Sound,Mitre_Peak),#ok
             #(Variable_Oystercatcher,Tui),#ok
             #(Homewood, Lyall_Bay),#ok
             #(Tongariro_National_Park,Lake_Hawea),#ok
             #(Flea_Bay, Korora),#ok
             (Fern_Frond,Arthurs_Pass_Forest),#ok
             #(Lost_Soles, Aylesbury),#ok
             #(Martinborough, The_Catlins),#ok
             #(Kapiti_Island, Taupo),
             #(Waimakariri_River, Punakaiki),
             #(Lake_Taupo, Civic_Square),
             #(Cathedral_Cove, Mitre_Peak_2),
             #(Motupiko, Rotorua),#ok
             #(Tiniroto, Pongaroa),
             #(The_Beehive, Wellington_Railway_Station),#ok
             #(Waterfall, Toi_Toi),#ok
             #(Shed, Boat_Houses, ),#ok
             #(Wellington_From_Matui_2, Marlborough_Sounds, ),#ok
    
             #(Arthurs_Pass,),#ok
             #(Lyall_Bay_Long,),
             #(Homewood_Long,),
             #(Te_Marua,),#ok
             #(Lake_Ferry,),#ok
             #(Auckland,),#ok
             #(Mount_Victoria,),#ok
    
             ]
  
  
    
  def get_parameters(self):  
    self.image_src = r"C:\Users\Horst\Pictures\Output\Books\NZ\src"
    self.output_folder = r"C:\Users\Horst\Pictures\Output\Books\NZ"
    self.width = int(5138/2)
    self.height = 3416
    self.margin = 48
    self.marg_x = 40
    self.marg_y = 30
    self.left_image_x = 450
    self.max_text_width = self.left_image_x - self.margin - self.marg_x - 30
    self.marg_x_map = (self.left_image_x  - 282)
    self.marg_x_map = (self.marg_x)
    self.bg_col = '#ffffff'
    self.fontname_big = "GILB____.TTF"
    self.fontname_small = "GIL_____.TTF"
    self.font_size_big = 52
    self.font_size_small = 40
    self.t_align_right_page = "left"
    self.font_big = ImageFont.truetype("%s" %self.fontname_big, self.font_size_big)
    self.font_small = ImageFont.truetype("%s" %self.fontname_small, self.font_size_small)
    self.image_height = int((self.height-2*self.margin)/3)
    self.y_l = [self.margin, self.margin+self.image_height, self.margin+self.image_height * 2]
    
  def run(self):
    self.define_page_contents()
    for self.picture in self.pages:
      self.initialise_page()
      self.make_page()
    
  def initialise_picture(self):
    p = self.picture
    self.name = self.iptc[p].get('title')
    self.picture_obj = Image.open("%s" %(p))
    if self.picture_obj.size[0] > self.width:
      if self.page_left_right == 'left':
        cut = (0,0,self.width - self.left_image_x, self.image_height)
      else:
        cut = (self.width - self.left_image_x,0,self.picture_obj.size[0], self.image_height)
      self.picture_obj = self.picture_obj.crop(cut)
    self.header = self.iptc[p].get('title', self.name)
    self.map = self.iptc[p].get('location', self.name)
    try:
      self.map = Image.open("%s/%s.png" %(self.image_src, self.map))
    except:
      print("No Map: %s!" %self.map)
    self.caption = self.iptc[p].get('caption')
    
      
  def initialise_page(self):
    self.filename = self.picture.split("\\")[-1:][0].strip(".jpg").split("_")[0]
    self.IM = Image.new('RGBA', (self.width, self.height), self.bg_col)
    self.draw = ImageDraw.Draw(self.IM)
    try:
      if not int(self.filename) %2:
        self.page_left_right = "left"
      else:
        self.page_left_right = "right"
    except:
      pass
    
    
  def make_page(self):
    i = 0
    self.picture_first = self.picture
    for y in self.y_l:
      if i==1:
        path = "%s_A.jpg" %self.picture.strip(".jpg")
        if os.path.exists(path):
          self.picture = path
      elif i==2:
        path = "%s_B.jpg" %self.picture.strip(".jpg")
        if os.path.exists(path):
          self.picture = path
        else:
          self.picture = self.picture_first
        
      self.initialise_picture()
      draw = self.draw
      header = self.header
      caption = self.caption
      y = int(y)
      if self.page_left_right == "left":
        x = self.margin + self.marg_x
        align = None
        px = self.left_image_x
      if self.page_left_right == "right":
        x = self.width - self.left_image_x + self.marg_x
        align = self.t_align_right_page
        px = 0
      self.curr_y = self.IT.draw_text(self.draw, text=self.header, x=x, y=self.marg_y + y, font=self.font_big, fill='#888888', max_width = self.max_text_width,align=align)
      self.curr_y = self.IT.draw_text(self.draw, text=self.caption, x=x, y=self.curr_y + 20, font=self.font_small, fill='#ababab', max_width=self.max_text_width, align=align)
      if i == 0:
        y_adjust = self.margin - 10
      else:
        y_adjust = 0
      try:
        self.IM.paste(self.map, (self.margin + self.marg_x_map, y + self.image_height - 320))
      except:
        pass
      self.IM.paste(self.picture_obj, (px, y - y_adjust ))
        
      i += 1
    self.IM.save("%s\%s.jpg" %(self.output_folder,self.filename), "JPEG", quality=100)
    print("Done Making ans saving page.")

PPM = PhotobookPageMaker()
PPM.run()

