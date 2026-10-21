"""Animate the underwater profile artwork. Requires Pillow; run from any directory."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
W, H = 1200, 400
N = 96
TAU = math.tau
base = ImageOps.fit(Image.open(ROOT/'assets/underwater-background.png').convert('RGB'), (W,H)).convert('RGBA')

# Keep the typography legible without obscuring the scenery.
shade = Image.new('RGBA', (W,H))
d = ImageDraw.Draw(shade)
for x in range(W):
    opacity = round(70 * max(0, 1-x/800))
    d.line((x,0,x,H), fill=(0,8,28,opacity))
base = Image.alpha_composite(base, shade)


def flower(layer, x, y, size, colour, phase, offset):
    glow = Image.new('RGBA', (W,H))
    gd = ImageDraw.Draw(glow)
    cx = x + 3*math.sin(TAU*phase+offset)
    cy = y + 3*math.cos(TAU*phase+offset)
    points = []
    for k in range(241):
        angle = TAU*k/240
        radius = size*(.69+.27*math.cos(5*angle))
        points.append((cx+radius*math.cos(angle), cy+radius*math.sin(angle)))
    strength = .82+.18*math.sin(TAU*phase+offset)
    gd.line(points, fill=(*colour,round(230*strength)), width=9, joint='curve')
    layer = Image.alpha_composite(layer, glow.filter(ImageFilter.GaussianBlur(7)))
    core = Image.new('RGBA',(W,H)); cd=ImageDraw.Draw(core)
    cd.line(points,fill=(*colour,round(235*strength)),width=3,joint='curve')
    r=size*.1
    cd.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(*colour,round(200*strength)),width=2)
    return Image.alpha_composite(layer,core)


def jellyfish(layer,x,y,size,phase,offset):
    cx=x+7*math.sin(TAU*phase+offset)
    cy=y+9*math.cos(TAU*phase+offset)
    pulse=.92+.08*math.sin(TAU*phase+offset)
    s=size*pulse
    art=Image.new('RGBA',(W,H)); ad=ImageDraw.Draw(art)
    pink=(255,130,224)
    dome=[(cx-s*math.cos(t),cy-s*.72*math.sin(t)) for t in [math.pi*k/60 for k in range(61)]]
    edge=[(cx+s-2*s*k/60,cy+2.5*math.sin(k/60*math.pi*6)) for k in range(61)]
    ad.polygon(dome+edge,fill=(212,68,183,90))
    ad.line(dome,fill=(*pink,230),width=2)
    ad.line(edge,fill=(*pink,230),width=2)
    ad.arc((cx-s*.7,cy-s*.52,cx+s*.7,cy+s*.35),180,330,fill=(255,193,238,150),width=2)
    for j in range(5):
        points=[]
        for k in range(31):
            t=k/30
            xx=cx+(j-2)*s*.32+math.sin(t*7-TAU*phase+offset+j)*s*.17*t
            yy=cy+s*.1+t*s*(1.05+.12*math.sin(j))
            points.append((xx,yy))
        ad.line(points,fill=(*pink,205),width=2,joint='curve')
    layer=Image.alpha_composite(layer,art.filter(ImageFilter.GaussianBlur(10)))
    layer=Image.alpha_composite(layer,art.filter(ImageFilter.GaussianBlur(3)))
    return Image.alpha_composite(layer,art)


def draw_frame(phase):
    im=base.copy()
    for x,y,s,c,o in [(790,80,47,(172,148,255),0), (1040,68,35,(132,233,159),2),
                        (1150,185,42,(255,158,206),4), (730,293,28,(70,171,222),3)]:
        im=flower(im,x,y,s,c,phase,o)
    for x,y,s,o in [(920,160,23,1),(1130,35,14,3),(1080,275,18,5)]:
        im=jellyfish(im,x,y,s,phase,o)
    bubbles=Image.new('RGBA',(W,H)); bd=ImageDraw.Draw(bubbles)
    for i in range(14):
        x=690+(i*103)%500+4*math.sin(TAU*phase+i)
        y=((i*71)%460-phase*H)%460-30
        r=2+(i%4)
        bd.ellipse((x-r,y-r,x+r,y+r),outline=(151,217,244,85),width=1)
        bd.point((x-1,y-r+1),fill=(211,247,255,150))
    im=Image.alpha_composite(im,bubbles)
    text=Image.new('RGBA',(W,H)); td=ImageDraw.Draw(text)
    regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    td.text((52,101),'Nam Tran',font=ImageFont.truetype(bold,64),fill=(247,252,255),
            stroke_width=1,stroke_fill=(6,21,47,90))
    td.text((56,188),'Hardware & embedded systems',font=ImageFont.truetype(regular,26),fill=(166,236,234))
    td.text((56,241),'Nanotechnology Engineering',font=ImageFont.truetype(regular,19),fill=(210,224,242))
    td.text((56,271),'University of Waterloo',font=ImageFont.truetype(regular,19),fill=(210,224,242))
    td.text((56,346),'CIRCUITS  /  PCB LAYOUT  /  HARDWARE TEST',font=ImageFont.truetype(regular,14),fill=(147,187,211))
    return Image.alpha_composite(im,text).convert('RGB')


poster=draw_frame(.25)
poster.save(ROOT/'assets/header-ocean-static.png',optimize=True)
# Shared palette preserves the painted background and avoids colour flicker.
palette=poster.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
frames=[draw_frame(i/N).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(N)]
path=ROOT/'assets/header-ocean.gif'
frames[0].save(path,save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True,disposal=1)
print(f'{path}: {path.stat().st_size:,} bytes, {N} frames, {N*.08:.2f}s loop')
