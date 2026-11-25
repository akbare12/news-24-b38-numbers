import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; OUT=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png')
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
SER='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; SAN='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; SANB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f_ser(s): return F(SER,s)
def f_san(s): return F(SAN,s)
def f_sanb(s): return F(SANB,s)
CREAM=(250,246,235); INK=(20,20,22); RED=(178,34,34); NAVY=(24,48,88); GREY=(110,110,108); LGREY=(228,224,214); GREEN=(34,120,60); BLUE=(30,90,170); ORANGE=(200,110,20)
CHIP={'CONFIRMED':GREEN,'OFFICIAL':BLUE,'REPORTED':(90,90,90),'CLAIM':ORANGE}
def txt(d,x,y,s,font,fill=INK,anchor='la'):
    d.text((x,y),s,font=font,fill=fill,anchor=anchor)
def wrap(d,s,font,maxw):
    words=s.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def para(d,x,y,s,font,maxw,lh,fill=INK,maxl=4):
    ls=wrap(d,s,font,maxw)[:maxl]
    for i,l in enumerate(ls): d.text((x,y+i*lh),l,font=font,fill=fill)
    return y+len(ls)*lh
def chip(d,x,y,s):
    f=f_sanb(8); w=d.textlength(s,font=f)+8; d.rounded_rectangle([x,y,x+w,y+12],radius=3,fill=CHIP.get(s,GREY)); d.text((x+4,y+1),s,font=f,fill=(255,255,255)); return x+w+4
def _scene_raw(d,b,k):
    x0,y0,x1,y1=b; d.rectangle(b,fill=(210,225,240) if k in ('tower','court','rocket') else (200,215,200) if k in ('drone','ship','heli') else (225,215,190))
    if k=='tower':
        d.rectangle([x0+120,y0+8,x0+165,y1-6],fill=NAVY); d.rectangle([x0+128,y0+2,x0+157,y0+12],fill=NAVY); d.ellipse([x0+200,y0+14,x0+232,y0+46],fill=(255,150,40)); d.polygon([(x0+215,y0+46),(x0+235,y0+70),(x0+195,y0+70)],fill=(255,110,30)); d.rectangle([x0+8,y1-22,x1-8,y1-6],fill=(60,60,60))
        for i in range(5): d.rectangle([x0+20+i*28,y1-52-i*4,x0+40+i*28,y1-22],fill=(90,110,140))
    elif k=='party':
        d.rectangle([x0+40,y0+30,x0+270,y1-8],fill=(150,40,40)); d.rectangle([x0+110,y0+55,x0+200,y1-8],fill=(90,20,20)); d.polygon([(x0+155,y0+8),(x0+175,y0+30),(x0+135,y0+30)],fill=(200,170,60)); d.rectangle([x0+210,y0+45,x0+290,y1-8],fill=(240,240,230)); d.rectangle([x0+222,y0+50,x0+278,y0+60],fill=NAVY); d.text((x0+222,y0+61),'FILE',font=f_sanb(8),fill=INK)
    elif k=='court':
        d.rectangle([x0+60,y0+35,x0+250,y1-10],fill=(200,190,170)); d.polygon([(x0+55,y0+35),(x0+155,y0+5),(x0+255,y0+35)],fill=(140,40,40)); d.rectangle([x0+95,y0+60,x0+115,y1-10],fill=(255,255,255)); d.rectangle([x0+195,y0+60,x0+215,y1-10],fill=(255,255,255)); d.ellipse([x0+135,y0+52,x0+175,y0+88],fill=(30,90,170)); d.text((x0+140,y0+63),'10/12',font=f_sanb(11),fill=(255,255,255))
    elif k=='drone':
        d.rectangle([x0,y0,x1,y0+45],fill=(30,30,50)); d.ellipse([x0+130,y0+18,x0+180,y0+40],fill=(120,120,120)); d.rectangle([x0+105,y0+26,x0+205,y0+32],fill=(80,80,80)); d.ellipse([x0+230,y0+55,x0+275,y0+95],fill=(255,150,40)); d.rectangle([x0+8,y1-18,x1-8,y1-6],fill=(70,70,70))
    elif k=='trophy':
        d.rectangle([x0+130,y0+12,x0+180,y0+78],fill=(220,180,40)); d.rectangle([x0+118,y0+22,x0+132,y0+52],fill=(220,180,40)); d.rectangle([x0+178,y0+22,x0+192,y0+52],fill=(220,180,40)); d.rectangle([x0+140,y0+78,x0+170,y0+95],fill=(180,140,20)); d.rectangle([x0+20,y0+70,x0+110,y0+95],fill=(20,120,60)); d.rectangle([x0+200,y0+70,x0+290,y0+95],fill=(200,40,40))
    elif k=='ship':
        d.rectangle([x0,y0+70,x1,y1],fill=(40,90,140)); d.rectangle([x0+70,y0+38,x0+250,y0+72],fill=(200,60,40)); d.rectangle([x0+70,y0+22,x0+110,y0+38],fill=(240,240,240)); d.ellipse([x0+240,y0+8,x0+285,y0+45],fill=(255,150,40))
    elif k=='chart':
        d.rectangle([x0+20,y0+60,x0+290,y1-8],fill=(240,240,230)); d.line([(x0+25,y0+75),(x0+100,y0+65),(x0+180,y0+45),(x0+285,y0+18)],fill=GREEN,width=4); d.line([(x0+25,y0+40),(x0+285,y0+40)],fill=RED,width=2); d.text((x0+30,y0+42),'50,000',font=f_sanb(10),fill=RED); d.text((x0+200,y0+60),'50,018',font=f_sanb(12),fill=GREEN)
    elif k=='data':
        d.rectangle([x0+30,y0+15,x0+280,y1-10],fill=(30,30,40)); d.text((x0+45,y0+25),'CODE RED',font=f_sanb(16),fill=(255,60,60)); d.rectangle([x0+45,y0+55,x0+265,y0+68],fill=(255,60,60)); d.text((x0+45,y0+75),'11,000+ messages',font=f_sanb(10),fill=(255,255,255))
    elif k=='heli':
        d.ellipse([x0+90,y0+35,x0+220,y0+70],fill=(90,110,90)); d.rectangle([x0+60,y0+48,x0+95,y0+58],fill=(70,90,70)); d.rectangle([x0+210,y0+50,x0+285,y0+56],fill=(70,90,70)); d.polygon([(x0+20,y0+85),(x0+120,y0+70),(x0+290,y0+85),(x0+290,y1-6),(x0+20,y1-6)],fill=(120,140,120))
    elif k=='market':
        d.rectangle([x0+40,y0+20,x0+270,y1-10],fill=(230,220,200)); d.rectangle([x0+60,y0+35,x0+130,y0+70],fill=(180,60,60)); d.rectangle([x0+150,y0+35,x0+250,y0+70],fill=(120,120,120)); d.text((x0+70,y0+72),'25 HELD',font=f_sanb(11),fill=INK)
    elif k=='desert':
        d.polygon([(x0,y1-6),(x0+120,y0+40),(x0+230,y1-6)],fill=(210,180,120)); d.rectangle([x0+130,y0+25,x0+190,y0+65],fill=(120,90,60)); d.text((x0+135,y0+35),'60 km',font=f_sanb(11),fill=(255,255,255))
    elif k=='rocket':
        d.polygon([(x0+150,y0+8),(x0+170,y0+45),(x0+140,y0+45)],fill=(200,40,40)); d.rectangle([x0+140,y0+45,x0+170,y0+90],fill=(240,240,240)); d.ellipse([x0+120,y0+88,x0+190,y0+105],fill=(255,150,40)); d.ellipse([x0+240,y0+20,x0+290,y0+65],fill=(200,200,200))
    else:
        d.rectangle([x0+40,y0+20,x0+270,y1-10],fill=(180,180,160))
def scene(d,b,k):
    x0,y0,x1,y1=b
    tmp=Image.new('RGB',(310,90),(210,225,240)); td=ImageDraw.Draw(tmp); _scene_raw(td,(0,0,310,90),k); tmp=tmp.resize((x1-x0,y1-y0)); d._image.paste(tmp,(x0,y0))
HERO=[('1','RIYADH','MIDDLE EAST','CONFIRMED','Houthi drone hits Riyadh tallest tower again, 11 hurt','A Houthi drone struck the PIF tower, the tallest in Riyadh, for the second time in a week. At least 11 people were hurt.','tower','Saudi officials · 14:27 UTC'),('2','SHANGHAI','ASIA','OFFICIAL','China probes Shanghai party chief Chen Jining','Chen Jining, 62, Shanghai party chief, faces a probe for serious violations. He is the fourth Politburo member to fall.','party','CCDI · Official'),('3','NEW YORK','US / TECH','CONFIRMED','Huawei guilty on 10 of 12 counts','A US jury found Huawei guilty on 10 of 12 counts. It was cleared of racketeering, with sentencing in Sep 2027.','court','US court · 20:41 UTC')]
CARDS=[('4','ZAPORIZHZHIA','EUROPE','REPORTED','Russian attacks kill 9 across Ukraine in a day','96 drones launched; 73 shot down. 9 killed and 81 wounded.','drone','Ukraine officials · 11:37 UTC'),('5','DAKAR','AFRICA / SPORT','OFFICIAL','CAS hands Senegal back the AFCON title','CAS restored the AFCON title to Senegal: Morocco forfeited 3-0, so Senegal won 1-0.','trophy','CAS · Official'),('6','HORMUZ','MIDDLE EAST','REPORTED','IRGC attacks container ship in Hormuz','IRGC hit a container ship in Hormuz at 18:58 UTC, disabling navigation.','ship','UKMTO · 18:58 UTC'),('7','NEW YORK','WORLD / MARKETS','CONFIRMED','Dow closes above 50,000 for the first time','The Dow closed at 50,018, its first finish above 50,000, while the Taiex rose 8.99%.','chart','Market close · Confirmed'),('8','REDMOND','WORLD / TECH','REPORTED','Microsoft declares Code Red after historic outage','After a historic 24-hour outage, Microsoft declared Code Red, aiming for one-hour recovery.','data','Reuters · Reported'),('9','ESKISEHIR','EUROPE','REPORTED','Turkish military helicopter crash kills 5','A Turkish military AS-532 helicopter crashed in Eskisehir, killing all 5 aboard.','heli','Turkish officials · 19:52 UTC'),('10','CARTAGENA','AMERICAS','REPORTED','Supermarket hostages: 25 held in Cartagena','Gunmen held 25 hostages in a Cartagena supermarket and released 5 elderly women.','market','Colombia officials · 17:35 UTC'),('11','ADEN','MIDDLE EAST','REPORTED','Houthis advance within 60 km of Aden','Houthi forces advanced to within 60 km of Aden, closing in on the southern port city.','desert','Wires · 16:51 UTC'),('12','LAHJ','MIDDLE EAST','REPORTED','Saudi strikes kill 25, wound 6 in Yemen','Saudi strikes in Lahj left 25 people dead or missing and 6 wounded.','desert','Yemen officials · 10:42 UTC'),('13','JIUQUAN','WORLD / SPACE','OFFICIAL','China names first foreign astronaut for Tiangong','Shenzhou-24 crew named, with the first foreign astronaut for Tiangong.','rocket','CMSA · Official')]
ALSO=[('14','Ankara','Haftar visits Turkey for the first time','REPORTED'),('15','London','UK sanctions Houthis + 4 officials','OFFICIAL'),('16','Villavicencio','Car bomb injures 23','REPORTED'),('17','Gaza','Israel kills Hamas internal security chief','REPORTED'),('18','Baghdad','Iraq orders federal control of Kurdish oilfields + crossings','OFFICIAL'),('19','Gaza','Meningitis epidemic alert: 272 cases in Oct, 15 dead in 2026','OFFICIAL'),('20','DR Congo','Missing Cessna 208, rebels claim shootdown; 4 aboard','CLAIM'),('21','Hanoi','Hot-pot explosion kills at least 6, 10 hurt','REPORTED'),('22','Gulf of Finland','Ukraine hits Russian ship Sparta II; 16 crew evacuated','REPORTED'),('23','Kuala Lumpur','Malaysia to return thousands of migrants to Myanmar','OFFICIAL'),('24','Ulleungdo','S. Korea shelter order as Russian jets enter ADIZ','OFFICIAL'),('25','Dhaka','Hasina plans return on 16 Dec','REPORTED'),('26','The Hague','14 nations endorse ICJ Myanmar ruling, 9-6','REPORTED'),('27','Jakarta','Indonesia nominates 2 VP candidates','OFFICIAL'),('28','China','China sentences official Ma to death for spying','OFFICIAL'),('29','Brussels','NATO vows defence against space threat','OFFICIAL'),('30','Mexico City','El Chapo Isidro: US drone aided weekend capture; Mexico to try him','REPORTED'),('31','San Salvador','Bukele names 3 Salvadoran soldiers killed in Haiti','OFFICIAL'),('32','Ottawa','Pentagon rebukes Canada: only 41.9% of air fleet ready','REPORTED'),('33','Washington','US adds Megaspeed to trade blacklist','OFFICIAL'),('34','Kyiv','Zelensky urges Ukraine/Russia/US/Europe talks soon','REPORTED'),('35','Ras Al Khaimah','UAE bus-truck crash kills 13; 41 aboard, 14 hurt','REPORTED'),('36','London','England record 5,258 heat deaths, summer 2026','OFFICIAL'),('37','Kourou','Ariane 6 lofts 36 Amazon satellites','OFFICIAL'),('38','Cikande','Factory-fire toll rises to 26','REPORTED')]
NUMBERS=[('11','hurt in Riyadh'),('9','killed in Ukraine'),('50,018','Dow close'),('+8.99%','Taiex record'),('25','dead/missing, Yemen'),('26','Cikande fire toll'),('10/12','Huawei guilty'),('96','drones at Ukraine')]
UTC=[('02:15','NATO vows space defence'),('08:16','Hanoi hot-pot blast'),('10:42','Saudi strikes Yemen'),('14:27','Riyadh tower hit'),('16:51','Houthis 60 km from Aden'),('18:58','Hormuz ship attack'),('20:41','Huawei guilty')]
CONT=[([(-168,66),(-140,70),(-120,72),(-95,80),(-85,70),(-75,62),(-65,45),(-75,35),(-80,25),(-85,30),(-95,29),(-105,22),(-115,30),(-125,40),(-145,60)],'NA'),([(-80,10),(-70,12),(-60,5),(-50,0),(-40,-5),(-35,-10),(-40,-20),(-50,-30),(-60,-40),(-70,-50),(-75,-35),(-70,-20),(-80,-5)],'SA'),([(-10,36),(-5,43),(0,48),(-2,50),(5,53),(8,57),(18,55),(20,60),(25,65),(30,70),(40,68),(45,60),(35,55),(30,45),(28,40),(22,38),(15,38),(10,44),(3,42),(-2,37)],'EU'),([(-17,15),(-10,30),(0,35),(10,37),(20,32),(32,31),(35,28),(43,12),(51,10),(48,0),(40,-10),(35,-20),(30,-30),(20,-35),(15,-25),(12,-10),(10,0),(5,5),(-15,10)],'AF'),([(40,70),(60,72),(80,73),(100,76),(120,73),(140,72),(160,70),(178,66),(170,60),(160,55),(155,50),(140,45),(135,35),(130,35),(127,38),(120,32),(115,22),(108,18),(105,10),(100,8),(95,15),(90,22),(85,20),(80,10),(77,8),(72,20),(65,25),(60,25),(55,26),(50,28),(48,30),(45,28),(42,30),(40,35),(38,40),(35,42)],'AS'),([(113,-22),(122,-14),(132,-12),(142,-11),(150,-22),(153,-28),(150,-37),(140,-38),(130,-32),(120,-34),(114,-30)],'OC')]
PINS=[('1',24.7,46.7,'Riyadh'),('2',31.2,121.5,'Shanghai'),('3',40.7,-74.0,'New York'),('4',47.8,35.2,'Zaporizhzhia'),('5',14.7,-17.4,'Dakar'),('6',26.5,56.5,'Hormuz'),('7',40.7,-74.0,'New York'),('8',47.7,-122.1,'Redmond'),('9',39.8,30.5,'Eskisehir'),('10',10.4,-75.5,'Cartagena'),('11',12.8,45.0,'Aden'),('12',13.0,44.9,'Lahj'),('13',39.7,98.5,'Jiuquan')]
OFF={'7':(26,-14),'12':(24,12),'3':(-24,10)}
def main():
    img=Image.new('RGB',(W,H),CREAM); d=ImageDraw.Draw(img); d.rectangle([0,0,W,6],fill=RED)
    txt(d,12,10,'THE WORLD ON ONE DAY',f_sanb(11),RED); txt(d,1012,10,'38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS',f_sanb(11),INK,anchor='ra')
    txt(d,512,26,'Tuesday 24 November 2026',f_ser(30),INK,anchor='ma'); txt(d,512,60,'Riyadh tower hit again \u00b7 Shanghai party chief probed \u00b7 Huawei guilty 10 of 12',f_ser(13),RED,anchor='ma')
    d.rectangle([12,80,1012,104],fill=NAVY); txt(d,512,84,'Europe 9  \u00b7  Middle East 8  \u00b7  Asia 8  \u00b7  Africa 2  \u00b7  Americas 7  \u00b7  World/Space 4',f_sanb(13),(255,255,255),anchor='ma')
    txt(d,12,110,'THE DAY IN UTC',f_sanb(10),RED)
    x=12
    for t,ev in UTC:
        txt(d,x,122,t,f_sanb(10),RED); txt(d,x,134,ev,f_san(8),INK); x+=143
    d.line([(12,150),(1012,150)],fill=GREY,width=1); txt(d,12,154,'THE DAY IN NUMBERS',f_sanb(10),RED)
    x=12
    for n,lab in NUMBERS:
        txt(d,x,166,n,f_ser(17),INK); txt(d,x,186,lab,f_san(8),GREY); x+=125
    # Heroes
    y=206; hw=326; gap=11
    for i,(n,city,reg,ch,head,deck,kind,src) in enumerate(HERO):
        x=12+i*(hw+gap); d.rectangle([x,y,x+hw,y+154],outline=INK,width=1); scene(d,(x+1,y+1,x+hw-1,y+78),kind); txt(d,x+8,y+82,n+' '+city+' \u00b7 '+reg,f_sanb(10),RED); xe=chip(d,x+8,y+96,ch); txt(d,xe+4,y+97,src,f_san(8),GREY); para(d,x+8,y+110,head,f_sanb(11),hw-16,12,INK,2); para(d,x+8,y+134,deck,f_san(9),hw-16,10,INK,2)
    # Cards 5+5
    y=366; cw=192; cg=10
    for i,(n,city,reg,ch,head,deck,kind,src) in enumerate(CARDS):
        r=i//5; c=i%5; x=12+c*(cw+cg); yy=y+r*108; d.rectangle([x,yy,x+cw,yy+104],outline=INK,width=1); scene(d,(x+1,yy+1,x+cw-1,yy+36),kind); txt(d,x+5,yy+39,n+' '+city,f_sanb(8),RED); chip(d,x+5,yy+51,ch); para(d,x+5,yy+64,head,f_sanb(9),cw-10,10,INK,2); para(d,x+5,yy+84,deck,f_san(8),cw-10,9,GREY,2)
    return img,d
def draw_map(d):
    mx0,my0,mw,mh=12,588,660,204
    d.rectangle([mx0,my0,mx0+mw,my0+mh],outline=INK,width=1,fill=(185,210,235))
    def P(lon,lat): return (mx0+(lon+170)/360*mw,my0+(83-lat)/138*mh)
    for poly,_ in CONT: d.polygon([P(lo,la) for lo,la in poly],fill=(190,205,165),outline=(120,140,110))
    for n,lat,lon,city in PINS:
        px,py=P(lon,lat); ox,oy=OFF.get(n,(0,0)); qx,qy=px+ox,py+oy
        if (ox,oy)!=(0,0): d.line([(px,py),(qx,qy)],fill=RED,width=1)
        d.ellipse([qx-9,qy-9,qx+9,qy+9],fill=RED,outline=(255,255,255),width=1); d.text((qx,qy),n,font=f_sanb(9),fill=(255,255,255),anchor='mm')
    txt(d,682,588,'MAP KEY 1-13',f_sanb(10),RED)
    for i,(n,lat,lon,city) in enumerate(PINS):
        txt(d,682,604+i*14,n+'. '+city,f_san(9),INK)
    txt(d,682,604+13*14,'Pins = story numbers.',f_san(8),GREY)
def draw_also(d):
    txt(d,12,798,'ALSO ON TUESDAY 24 NOVEMBER \u2014 25 MORE STORIES',f_sanb(11),RED); d.line([(12,812),(1012,812)],fill=RED,width=1)
    for i,(n,city,head,ch) in enumerate(ALSO):
        col=i//13; row=i%13; x=12+col*504; y=816+row*10; f=f_san(8); s=n+' '+city+': '+head
        while d.textlength(s,font=f)>430 and len(s)>10: s=s[:-4]+'\u2026'
        d.text((x,y),s,font=f,fill=INK); chip(d,x+436,y-1,ch)
def draw_date(d):
    d.rectangle([12,948,1012,1002],outline=RED,width=1,fill=(255,240,240))
    s='DATE CHECK: Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov); Huang returns as Nvidia CEO (23 Nov); EU 22nd sanctions package (23 Nov); COP31 ends with no deal (22 Nov); corvette Merkury sunk (22 Nov); El Chapo Isidro arrested Fri 20 Nov; Cikande factory fire began Sat 21 Nov; Trump hush-money appeal ruling (23 Nov). NOT YET: Shenzhou-24 launch Wed 25 Nov 00:18 UTC; MPR session to pick VP (11 Dec); Huawei sentencing (Sep 2027); Hasina returns to Bangladesh (16 Dec).'
    para(d,18,952,s,f_san(8),976,10,INK,4)
    txt(d,12,1008,'Sources: dailysummaryof.com/world/2026-11-24 \u00b7 Reuters \u00b7 AP \u00b7 UKMTO \u00b7 CAS \u00b7 CMSA \u00b7 CCDI. CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side\u2019s claim. Scenes are drawn illustrations, not photographs.',f_san(7),GREY)
if __name__=='__main__':
    img,d=main(); draw_map(d); draw_also(d); draw_date(d); os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True); img.save(OUT); print(OUT,img.size)
