# Copyright, Robert Donovan, LessonStudio, 2014
# If you use this then tweet what you did with it @LessonStudio.

# This file takes one argument which is a file that you would like to split into two encrypted images.
# The original image can only be viewed by overlaying the two encrypted images.
# If printed on clear plastic, It can be very finicky to align the two images if the pixel count is too high.
# For best results keep the original image below 200x200 pixels and print as large as possible onto clear plastic to
# obtain the best results.

# You can go to higher resolutions but you then really have to be precise when aligning the two images.

# The resulting images will be twice as wide and twice as tall pixelwise and there is only 1 bit colour.#Copyright, Robert Donovan, LessonStudio, 2014
# If you use this then tweet what you did with it @LessonStudio.

# This file takes one argument which is a file that you would like to split into two encrypted images.
# The original image can only be viewed by overlaying the two encrypted images.
# If printed on clear plastic, It can be very finicky to align the two images if the pixel count is too high.
# For best results keep the original image below 200x200 pixels and print as large as possible onto clear plastic to
# obtain the best results.

# You can go to higher resolutions but you then really have to be precise when aligning the two images.

# The resulting images will be twice as wide and twice as tall pixelwise and there is only 1 bit colour.

# Future features should include alignment marks to make aligning the two transparancies easier.

# Maybe I will increase the efficiency of the conversion except that I find that I spend more prep time in
# photoshop by many orders of magnitude than any time savings that could be extracted.

# The reason I built this is that I found many tools out there for doing this that didn't work for a
# variety of reasons including being built for long dead versions of Python or PIL.

# USAGE: python visual_cryptography.py file_to_encrypt.png

from PIL import Image, ImageDraw
import os
import sys
from random import SystemRandom
import argparse

random = SystemRandom()
# If you want to use the more powerful PyCrypto (pip install pycrypto) then uncomment the next line and comment out the previous two lines
#from Crypto.Random import random
xrange = range
img_filename_bw = ""
cimg_filename_bw = ""
slide_filename_A = ""
slide_filename_B = ""
slide_filename_A1 = ""
slide_filename_A2 = ""
slide_filename_B1 = ""
slide_filename_B2 = ""

def and_images(cinfile):
    ############################
    # Candidate image preparation
    cimg = Image.open(cinfile)
    cimg = cimg.convert('1')  # convert image to 1 bit
    cimg.save(cimg_filename_bw, 'PNG')
    print("Candidate Image size: {}".format(cimg.size))
    # Slides images preparation
    slide_A = Image.open(slide_filename_A)

    width = cimg.size[0]*2
    height = cimg.size[1]*2
    slide_image_A1 = Image.new('1', (width, height))
    slide_image_A2 = Image.new('1', (width, height))
    draw_slide_A1 = ImageDraw.Draw(slide_image_A1)
    draw_slide_A2 = ImageDraw.Draw(slide_image_A2)

    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
            pixel2 = cimg.getpixel((x, y))
#            pixel2 = 1

            # AND candidate and target slide images
#            slide_image_A1.putpixel((x*2, y*2), slide_A.getpixel((x*2, y*2)) & pixel2)
            draw_slide_A1.point((x*2, y*2), slide_A.getpixel((x*2, y*2)) & pixel2)
            draw_slide_A1.point((x*2+1, y*2), slide_A.getpixel((x*2+1, y*2)) & pixel2)
            draw_slide_A1.point((x*2, y*2+1), slide_A.getpixel((x*2, y*2+1)) & pixel2)
            draw_slide_A1.point((x*2+1, y*2+1), slide_A.getpixel((x*2+1, y*2+1)) & pixel2)
            
#            print("Pixels: A1:{} A:{} C:{}".format(slide_image_A1.getpixel((x*2, y*2)), slide_A.getpixel((x*2, y*2)), pixel2))
# #            slide_image_A1.putpixel((x*2, y*2), slide_A.getpixel((x*2, y*2)) & pixel2)
#            p = slide_A.getpixel((x*2, y*2)) & pixel2
#            p1 = slide_image_A1.getpixel((x*2, y*2))
#            if p == 255 and p1 == 0:
#                print("Pixels: A1:{} A:{} C:{}".format(p, slide_A.getpixel((x*2, y*2)), pixel2))
#                print("Pixels:({},{}) A11:{} A:{} C:{}".format(x,y,slide_image_A1.getpixel((x*2, y*2)), slide_A.getpixel((x*2, y*2)), pixel2))
            # AND negative candidate and target slide images
#            pixel2 = ~cimg.getpixel((x, y))
#            draw_slide_A2.point((x*2, y*2), slide_A.getpixel((x*2, y*2)) & pixel2)
#            draw_slide_A2.point((x*2+1, y*2), slide_A.getpixel((x*2+1, y*2)) & pixel2)
#            draw_slide_A2.point((x*2, y*2+1), slide_A.getpixel((x*2, y*2+1)) & pixel2)
#            draw_slide_A2.point((x*2+1, y*2+1), slide_A.getpixel((x*2+1, y*2+1)) & pixel2)
#        print('\n')
    slide_image_A1.save(slide_filename_A1, 'PNG')
    slide_image_A2.save(slide_filename_A2, 'PNG')
    return

def encryptImage(infile):
    img = Image.open(infile)

    img = img.convert('1')  # convert image to 1 bit
    img.save(img_filename_bw, 'PNG')

    print("Target Image size: {}".format(img.size))
    # Prepare two empty slider images for drawing
    width = img.size[0]*2
    height = img.size[1]*2
    print("Slide size{} x {}".format(width, height))
    slide_image_A = Image.new('1', (width, height))
    slide_image_B = Image.new('1', (width, height))
    draw_A = ImageDraw.Draw(slide_image_A)
    draw_B = ImageDraw.Draw(slide_image_B)
    # There are 6(4 choose 2) possible patterns and it is too late for me to think in binary and do these efficiently
    patterns = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
                (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))
    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
            pixel = img.getpixel((x, y))
            pat = random.choice(patterns)
            # A will always get the pattern
            draw_A.point((x*2, y*2), pat[0])
            draw_A.point((x*2+1, y*2), pat[1])
            draw_A.point((x*2, y*2+1), pat[2])
            draw_A.point((x*2+1, y*2+1), pat[3])
            if pixel == 0:  # Dark pixel so B gets the anti pattern
                draw_B.point((x*2, y*2), 1-pat[0])
                draw_B.point((x*2+1, y*2), 1-pat[1])
                draw_B.point((x*2, y*2+1), 1-pat[2])
                draw_B.point((x*2+1, y*2+1), 1-pat[3])
            else:
                draw_B.point((x*2, y*2), pat[0])
                draw_B.point((x*2+1, y*2), pat[1])
                draw_B.point((x*2, y*2+1), pat[2])
                draw_B.point((x*2+1, y*2+1), pat[3])

    slide_image_A.save(slide_filename_A, 'PNG')
    slide_image_B.save(slide_filename_B, 'PNG')


def main():
    global img_filename_bw
    global cimg_filename_bw
    global slide_filename_A
    global slide_filename_B
    global slide_filename_A1
    global slide_filename_A2
    global slide_filename_B1
    global slide_filename_B2

    """
    parse the arguments and parse the topology file
    """
    parser = argparse.ArgumentParser(prog='PROG', description='Images manipulation utility')
    parser.add_argument('-t', dest='t', help='The  first argument - the image to be split')
    parser.add_argument('-help', action='store_true', dest='help', help="show this help message and exit")
    parser.add_argument('-c', dest='c', help="The second argument - the image to compare")
    args = parser.parse_args()
    if args.help or (args.t is None or args.c is None):
        parser.print_help()
        exit()
    """
    if len(sys.argv) != 3:
        print("The  first argument - the image to be split.")
        print("The second argument - the image to compare.")
        exit()
    infile = str(sys.argv[1])
    cinfile = str(sys.argv[2])
    """
    infile = str(args.t)
    cinfile = str(args.c)
    if not os.path.isfile(infile):
        print("That file does not exist.")
        exit()
    if not os.path.isfile(cinfile):
        print("That file does not exist.")
        exit()

    # Set output file names
    f, e = os.path.splitext(infile)
    img_filename_bw = "out_images/" + f + "_bw.png"
    slide_filename_A = "out_images/" + f + "_slideA.png"
    slide_filename_B = "out_images/" + f + "_slideB.png"

    f, e = os.path.splitext(cinfile)
    cimg_filename_bw = "out_images/" + f + "_bw.png"
    slide_filename_A1 = "out_images/" + f + "_slideA1.png"
    slide_filename_A2 = "out_images/" + f + "_slideA2.png"
    slide_filename_B1 = "out_images/" + f + "_slideB1.png"
    slide_filename_B2 = "out_images/" + f + "_slideB2.png"

    encryptImage(infile)

    print("Encryption Done.")

    print("Going to AND images")
    and_images(cinfile)

    print("Done.")

if __name__ == '__main__':
    main()
'''
TODO
1. Restore original image from 2 slides
2. Try completely different cimage
3. Add fool proof - check target and candidate images are of the same size
Why images are so similar?
'''