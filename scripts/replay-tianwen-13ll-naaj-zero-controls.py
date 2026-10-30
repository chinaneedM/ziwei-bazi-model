#!/usr/bin/env python3
"""Replay same-page circular-zero color/mask crops; no OCR or plate identification.

Pass: PDF_2810037 PDF_2810038 COLOR_DIRECTORY OUTPUT_DIRECTORY.
COLOR_DIRECTORY contains the two 13LJ *-p006-numeric-roi.png files and the two
13LL *-p006-second-zero-color.jpg files. Native coordinates are never resized.
"""
import hashlib,json,sys
from pathlib import Path
import fitz
from PIL import Image,ImageDraw
PDFS={'281-0037':'8892b16c3b8e17f12211195cf7b58acfd5b7dc0d0aefca6623f653a04d4da93e','281-0038':'73322281149551c76f96008c1b9f3933e817543f7cb8710c92268ade9ca031eb'}
WINDOWS={
 '281-0037':{'NUMERIC_ZERO':{'parent':[3277,472,3566,3955],'glyph':[3350,2600,3490,2720],'rgb':'eba797ce34a75cf5fb899403e415bcf5eb9dd239b9181f7b2f37855a27dbaede'},'SAME_PAGE_ZERO':{'parent':[2080,2250,2430,2800],'glyph':[2190,2400,2345,2530],'rgb':'11c16c785f1dca8a9d1e9d285cb5b8af56e7571b7a343819e4ee3e7004c4b6b0'}},
 '281-0038':{'NUMERIC_ZERO':{'parent':[3383,499,3738,4044],'glyph':[3420,2680,3565,2800],'rgb':'ce90010e39364a36d4440d9b18c0fcd8b4824657e3eb7ea2b9015d84d7e31dac'},'SAME_PAGE_ZERO':{'parent':[2140,2350,2490,2900],'glyph':[2235,2515,2385,2640],'rgb':'05466e2935bfe16298f878271e911e40d2ec3404a42d97ed7ae7e5757daf92b8'}}}

def sha(b):return hashlib.sha256(b).hexdigest()
def components(mask):
    w,h=mask.size;data=mask.tobytes();seen=set();areas=[]
    for start,v in enumerate(data):
        if not v or start in seen:continue
        stack=[start];seen.add(start);area=0
        while stack:
            k=stack.pop();area+=1;x=k%w;y=k//w
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    xx=x+dx;yy=y+dy
                    if 0<=xx<w and 0<=yy<h:
                        nk=yy*w+xx
                        if data[nk] and nk not in seen:seen.add(nk);stack.append(nk)
        if area>=8:areas.append(area)
    return sorted(areas,reverse=True)

def replay(pdf_paths,color_dir,out_dir):
    color_dir=Path(color_dir);out_dir=Path(out_dir);out_dir.mkdir(exist_ok=True,parents=True)
    result={'schema':'TIANWEN-13LL-SAME-PAGE-CIRCULAR-ZERO-COLOR-MASK-REPLAY','no_ocr':True,'resized':False,'connectivity':8,'component_min_area':8,'mask_polarity':'WHITE_FOREGROUND_BLACK_BACKGROUND','physical_damage_inference':False,'glyphs':[]}
    panel=Image.new('RGB',(4*230,2*250),'white');draw=ImageDraw.Draw(panel)
    for source_index,(holding,path) in enumerate(zip(PDFS,pdf_paths)):
        raw=Path(path).read_bytes();assert sha(raw)==PDFS[holding],'wrong source PDF'
        doc=fitz.open(stream=raw,filetype='pdf');pix=fitz.Pixmap(doc,33);mask=Image.frombytes('L',(pix.width,pix.height),pix.samples)
        for row,(tag,spec) in enumerate(WINDOWS[holding].items()):
            filename=holding+('-p006-numeric-roi.png' if tag=='NUMERIC_ZERO' else '-p006-second-zero-color.jpg')
            color=Image.open(color_dir/filename).convert('RGB');assert sha(color.tobytes())==spec['rgb'],'wrong parent color image'
            x1,y1,x2,y2=spec['parent'];gx1,gy1,gx2,gy2=spec['glyph'];assert color.size==(x2-x1,y2-y1)
            cg=color.crop((gx1-x1,gy1-y1,gx2-x1,gy2-y1));mg=mask.crop(spec['glyph']);assert cg.size==mg.size
            cfile=holding+'-'+tag.lower()+'-color.png';mfile=holding+'-'+tag.lower()+'-mask.png';cg.save(out_dir/cfile);mg.save(out_dir/mfile)
            result['glyphs'].append({'holding':holding,'page':6,'tag':tag,'source_pdf_sha256':PDFS[holding],'mask_xref':33,'parent_color_rgb_sha256':spec['rgb'],'parent_color_roi_xyxy':spec['parent'],'glyph_xyxy':spec['glyph'],'pixels':list(cg.size),'color_glyph_rgb_sha256':sha(cg.tobytes()),'mask_glyph_gray_sha256':sha(mg.tobytes()),'mask_white_pixels':sum(v>0 for v in mg.tobytes()),'mask_component_areas_ge8':components(mg),'color_file':cfile,'mask_file':mfile})
            y=row*250
            for j,(im,label) in enumerate([(cg,'color'),(mg.convert('RGB'),'mask')]):
                x=(source_index*2+j)*230;panel.paste(im,(x+20,y+70));draw.text((x+10,y+12),holding+' '+label,fill='black');draw.text((x+10,y+34),tag,fill='black')
        doc.close()
    panel.save(out_dir/'zero-color-mask-comparison.png')
    (out_dir/'replay.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result
if __name__=='__main__':
    if len(sys.argv)!=5:raise SystemExit('Pass two PDFs, color input directory, output directory')
    print(json.dumps(replay(sys.argv[1:3],sys.argv[3],sys.argv[4]),ensure_ascii=False,indent=2))
