"""Caption new clean CAD frames and encode GIF; requires Pillow.
SPDX-License-Identifier: MIT
"""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1]
work=ROOT.parent/'render-work'
font_path=Path('C:/Windows/Fonts/segoeui.ttf')
font=ImageFont.truetype(str(font_path),26) if font_path.exists() else ImageFont.load_default()
small=ImageFont.truetype(str(font_path),20) if font_path.exists() else ImageFont.load_default()
captions=json.loads((work/'captions.json').read_text())
frames=[]
for i,caption in enumerate(captions):
    im=Image.open(work/('frame-%03d.png'%i)).convert('RGB')
    dr=ImageDraw.Draw(im)
    dr.rectangle((0,0,1440,70),fill='#eef3f7')
    dr.text((28,18),caption,font=font,fill='#19334b')
    dr.rectangle((0,1038,1440,1080),fill='#eef3f7')
    dr.text((28,1048),'TBRTK | Uavhengige referanser | Prototype - fysisk validering gjenstaar',font=small,fill='#405467')
    frames.append(im.resize((960,720),Image.Resampling.LANCZOS))
# A four-second final concept image is included after the CAD sequence.
concept=Image.open(ROOT/'assets/images/complete-setup-person.png').convert('RGB')
end=Image.new('RGB',(960,720),'white');thumb=ImageOps.contain(concept,(960,720),Image.Resampling.LANCZOS)
end.paste(thumb,((960-thumb.width)//2,0));frames.extend([end]*24)
out=ROOT/'assets/animations';out.mkdir(parents=True,exist_ok=True)
dest=out/'public-rs4-assembly.gif'
frames[0].save(dest,save_all=True,append_images=frames[1:],duration=[170,170,160]*36,loop=0,optimize=True)
g=Image.open(dest);dur=0
for i in range(g.n_frames):g.seek(i);dur+=g.info.get('duration',0);g.convert('RGB').load()
print(json.dumps({'frames_after_GIF_optimization':g.n_frames,'duration_ms':dur,'bytes':dest.stat().st_size}))
# Audit contact sheet samples every stage and the final illustration.
sheet=Image.new('RGB',(1440,1080),'#e8edf2')
for j,i in enumerate([0,18,30,42,54,66,78,84,100]):
    s=frames[i].resize((480,360));sheet.paste(s,((j%3)*480,(j//3)*360))
sheet.save(work/'animation-review.png')
