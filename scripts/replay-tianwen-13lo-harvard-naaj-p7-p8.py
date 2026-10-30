#!/usr/bin/env python3
"""13LO source-bound triple-view p7/p8 collation replay; never infer physical plate identity.
Usage: script Harvard-13KT-evidence.zip NAAJ-13LJ-color.zip NAAJ-13LM-native.zip OUTPUT_DIR
Libraries: PyMuPDF, Pillow, OpenCV-python-headless, numpy.
"""
import hashlib,io,json,sys,zipfile
from pathlib import Path
import fitz,cv2,numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/research/TIANWEN-13LO-NAJDA-HARVARD-J35-P7-P8-THREE-WAY-SOURCE-CROSSWALK-R1.json'
def hash_bytes(x):return hashlib.sha256(x).hexdigest()
def replay(hzip,nzip,rz,out):
 e=json.loads(E.read_text(encoding='utf8'))
 hz=Path(hzip).read_bytes();nz=Path(nzip).read_bytes();nr=Path(rz).read_bytes()
 assert hash_bytes(hz)==e['harvard']['existing_artifact']['artifact_zip_sha256']
 assert hash_bytes(nr)==e['naaj']['verified_six_native_color_roi_archive_sha256']
 with zipfile.ZipFile(io.BytesIO(hz)) as a,zipfile.ZipFile(io.BytesIO(nz)) as b,zipfile.ZipFile(io.BytesIO(nr)) as c:
  pdf=a.read('harvard-mingshi-v11.pdf')
  assert len(pdf)==e['harvard']['original_pdf_bytes'] and hash_bytes(pdf)==e['harvard']['original_pdf_sha256']
  doc=fitz.open(stream=pdf,filetype='pdf');assert len(doc)==e['harvard']['original_pdf_pages']
  pix=doc[7].get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
  har=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
  assert [pix.width,pix.height]==e['harvard']['same_text_page']['pdf_image_pixels']
  assert hash_bytes(pix.samples)==e['harvard']['same_text_page']['page_rgb_sha256']
  naz={}
  for holding in e['naaj']['physical_holdings']:
   naz[holding]=Image.open(io.BytesIO(b.read(f'{holding}-p007-iiif.jpg'))).convert('L')
  acquisition=json.loads(c.read('acquisition.json'))
  assert len(acquisition['controls'])==6
  clips=[]
  for row in e['same_passage_three_locus_controls']:
   cr=har.crop(row['harvard_page_8_rgb_roi_xyxy'])
   assert list(cr.size)==row['harvard_roi_pixels'] and hash_bytes(cr.tobytes())==row['harvard_roi_rgb_sha256']
   group=[cr]
   for holding in e['naaj']['physical_holdings']:
    target=next(t for t in acquisition['controls'] if t['holding']==holding and t['target_id']==row['target_id'])
    raw=c.read(target['file']);assert hash_bytes(raw)==target['jpeg_sha256']
    col=Image.open(io.BytesIO(raw)).convert('RGB')
    assert hash_bytes(col.tobytes())==target['rgb_sha256']
    group.insert(0,col)
   clips.append(group)
  out=Path(out);out.mkdir(parents=True,exist_ok=True)
  contact=Image.new('RGB',(1500,1320),'white');d=ImageDraw.Draw(contact)
  for j,group in enumerate(clips):
   d.text((8,j*420+22),e['same_passage_three_locus_controls'][j]['target_id'],fill='black')
   for k,im in enumerate(group):
    t=im.copy();t.thumbnail((465,360))
    contact.paste(t,(k*500+12,j*420+50))
  contact.save(out/'three-source-native-contact.png')
  def gray(im):
   return cv2.resize(np.asarray(im),(1500,1000))
  for page in [6,7,8,9]:
   px=doc[page-1].get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csGRAY,alpha=False)
   img=np.frombuffer(px.samples,np.uint8).reshape(px.height,px.width)
   naz['Harvard'+str(page)]=Image.fromarray(img)
  sift=cv2.SIFT_create(nfeatures=4000,contrastThreshold=.016)
  fs={k:sift.detectAndCompute(gray(v),None) for k,v in naz.items()}
  def align(a,b):
   k1,d1=fs[a];k2,d2=fs[b]
   matches=cv2.BFMatcher().knnMatch(d1,d2,k=2)
   good=[m for m,n in matches if m.distance<.76*n.distance]
   if len(good)<8:return {'pairs':len(good),'inliers':0}
   P=np.float32([k1[m.queryIdx].pt for m in good]);Q=np.float32([k2[m.trainIdx].pt for m in good])
   H,mask=cv2.findHomography(P,Q,cv2.RANSAC,5)
   return {'pairs':len(good),'inliers':int(mask.sum()) if mask is not None else 0}
  expected=e['exploratory_geometric_page_identification']
  result={}
  for key,holding in [('naaj_2810037_vs_harvard_pdf_pages','281-0037'),('naaj_2810038_vs_harvard_pdf_pages','281-0038')]:
   result[key]={str(p):align(holding,'Harvard'+str(p)) for p in [6,7,8,9]}
   # Versions can change SIFT matches. Match the selected page only when it wins
   # without treating metric variations as a physical woodblock determination.
   assert result[key]['8']['inliers']>max(result[key][str(p)]['inliers'] for p in [6,7,9]),'local page8 geometry does not win in this library stack'
  result['naaj_2810037_vs_2810038_p7']=align('281-0037','281-0038')
  result['no_ocr']=True;result['same_woodblock_proven']=False;result['different_woodblock_proven']=False
  (out/'replay.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  return result
if __name__=='__main__':
 if len(sys.argv)!=5:raise SystemExit('Need 3 source ZIPs and output directory')
 print(json.dumps(replay(*sys.argv[1:]),ensure_ascii=False,indent=2))
