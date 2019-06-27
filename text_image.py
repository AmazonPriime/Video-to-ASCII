"""
Credit: Kobejohn
Github: https://github.com/kobejohn
Code source: https://bit.ly/2Nl6efQ
"""

import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw

def main(num):
    image = textToImage('imagesOut/{}.txt'.format(num))
    image.save('imagesOutPng/{}.png'.format(num))

def textToImage(file):
    PIXEL_ON, PIXEL_OFF = 0, 255
    with open(file) as f:
        lines = tuple(l.rstrip() for l in f.readlines())
    large_font = 20
    font = PIL.ImageFont.load_default()
    pt2px = lambda pt: int(round(pt * 96.0 / 72))
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)
    width = int(round(max_width + 40))
    image = PIL.Image.new('L', (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image
