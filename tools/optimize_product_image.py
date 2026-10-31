"""Resize a permitted local photograph; does not verify or publish a manifest entry."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('filename',help='New WebP filename inside static/images/laptops/')
    args=parser.parse_args()
    filename=Path(args.filename)
    if filename.name!=args.filename or filename.suffix.lower()!='.webp':
        parser.error('Use a simple filename ending in .webp')
    target=ROOT/'static/images/laptops'/filename
    if target.exists(): parser.error('Refusing to overwrite an existing asset')
    with Image.open(args.source) as source:
        image=ImageOps.exif_transpose(source)
        original_size=image.size
        image=image.convert('RGBA')
        background=Image.new('RGB',image.size,'white')
        background.paste(image,mask=image.getchannel('A'))
        image=background
        image.thumbnail((1000,1000),Image.Resampling.LANCZOS)
        image.save(target,'WEBP',quality=84,method=6)
    print(json.dumps({'path':'images/laptops/'+filename.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,'width':image.width,'height':image.height,'original_width':original_size[0],'original_height':original_size[1],'modifications':'Thu nhỏ tối đa 1000 px theo tỷ lệ, nén WebP, nền trắng cho vùng trong suốt; không cắt hoặc thay nội dung máy.'},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
