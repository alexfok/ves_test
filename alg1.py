# Thanks to Robert Donovan, LessonStudio, for the original VES implementation
# ves_test
# Usage:
# python.exe alg1.py -t Lenna.png -c LennaBWOrig.jpeg -enc
# python.exe alg1.py

from PIL import Image, ImageDraw
import os
import sys
from random import SystemRandom
import argparse
from pathlib import Path

random = SystemRandom()
# If you want to use the more powerful PyCrypto (pip install pycrypto) then uncomment the next line and comment out the previous two lines
#from Crypto.Random import random
xrange = range
img_filename_bw = ""
cimg_filename_bw = ""
slide_filename_A = ""
slide_filename_B = ""

def printImage(infile):
    timg = Image.open(infile)
    width = timg.size[0]
    height = timg.size[1]
    # Cycle through pixels
    print("image: {}\n".format(infile))
    # for x in xrange(0, int(width/2)):
    #     for y in xrange(0, int(height/2)):
    #         if type(pixel) == tuple:
    #             pixel = timg.getpixel((x, y))
    #         print("{}".format(pixel))
    #     print("\n")

    pixels = list(timg.getdata())
    for i in range(0, height):
        print("{}\n".format(pixels[i * width:(i + 1) * width]))



def recover_compared_image_count(infile, cinfile, slide_filename_A, slide_filename_B, ext):
    ############################
    # Candidate image preparation
    timg = Image.open(infile)
    timg = timg.convert('1')  # convert image to 1 bit
    cimg = Image.open(cinfile)
    cimg = cimg.convert('1')  # convert image to 1 bit
#    cimg.save(cimg_filename_bw, 'PNG')
#    print("recover_compared_image: Image size: {}".format(cimg.size))
#    print("recover_compared_image from slides: {}, {}".format(slide_filename_A, slide_filename_B))
    # Open slides images
    slide_filename_1 = slide_filename_A + ext
    slide_filename_2 = slide_filename_B + ext
    slide_image_1 = Image.open(slide_filename_1)
    slide_image_2 = Image.open(slide_filename_2)


    width = slide_image_1.size[0]
    height = slide_image_1.size[1]
    recovered_image = Image.new('1', slide_image_1.size)

    match_pixel_count = 0
    mismatch_pixel_count = 0
    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
#            pixel1 = slide_image_1.getpixel((x, y))
#            pixel2 = slide_image_2.getpixel((x, y))
            # AND candidate and target slide images
            recovered_image.putpixel((x*2, y*2), slide_image_1.getpixel((x*2, y*2)) & slide_image_2.getpixel((x*2, y*2)))
            recovered_image.putpixel((x*2+1, y*2), slide_image_1.getpixel((x*2+1, y*2)) & slide_image_2.getpixel((x*2+1, y*2)))
            recovered_image.putpixel((x*2, y*2+1), slide_image_1.getpixel((x*2, y*2+1)) & slide_image_2.getpixel((x*2, y*2+1)))
            recovered_image.putpixel((x*2+1, y*2+1), slide_image_1.getpixel((x*2+1, y*2+1)) & slide_image_2.getpixel((x*2+1, y*2+1)))


            timage_pixel_xy = timg.getpixel((x, y))
            cimage_pixel_xy = cimg.getpixel((x, y))
            pixels_xy = recovered_image.getpixel((x*2, y*2))
            pixels_x1y = recovered_image.getpixel((x*2+1, y*2))
            pixels_xy1 = recovered_image.getpixel((x*2, y*2+1))
            pixels_x1y1 = recovered_image.getpixel((x*2+1, y*2+1))
            sub_pixel_count = pixels_xy + pixels_x1y + pixels_xy1 + pixels_x1y1
            # if sub_pixel_count != 0:
            #     print("\n(x, y) {}, timage_pixel_xy: {}, cimage_pixel_xy: {}".format((x, y), timage_pixel_xy, cimage_pixel_xy))
            #     print("pixels_xy: {}, pixels_x1y:{}, pixels_xy1: {}, pixels_x1y1: {}".format(pixels_xy, pixels_x1y, pixels_xy1, pixels_x1y1))
            #     print("sub_pixel_count: {}".format(sub_pixel_count))
            if ext == '_P.png':
                flag = 'Positive'
                if cimage_pixel_xy == 255 and sub_pixel_count > 0:
                    if timage_pixel_xy == 255:
                        match_pixel_count = match_pixel_count + 1
                    else:
                        mismatch_pixel_count = mismatch_pixel_count + 1
            if ext == '_N.png':
                flag = 'Negative'
#                print("\n(x, y) {}, timage_pixel_xy: {}, cimage_pixel_xy: {}".format((x, y), timage_pixel_xy, cimage_pixel_xy))
#                print("pixels_xy: {}, pixels_x1y:{}, pixels_xy1: {}, pixels_x1y1: {}".format(pixels_xy, pixels_x1y, pixels_xy1, pixels_x1y1))
                if cimage_pixel_xy == 0 and sub_pixel_count == 0:
                    if timage_pixel_xy == 0:
                        match_pixel_count = match_pixel_count + 1
                    else:
                        mismatch_pixel_count = mismatch_pixel_count + 1



    recovered_image_name = Path(cinfile).stem
    recovered_image_name = 'out_images/' + recovered_image_name + '_R' + ext
    total_pixels = int(width/2)*int(height/2)
    print("compare images result image: {}, {} cimage: {}, match_pixel_count: {}, mismatch_pixel_count: {}, total_pixels: {}, match percentage: {:.2%}".format(infile, flag, recovered_image_name, match_pixel_count, mismatch_pixel_count, total_pixels, match_pixel_count/total_pixels))
    recovered_image.save(recovered_image_name, 'PNG')
    return

def recover_compared_image(cinfile, slide_filename_A, slide_filename_B, ext):
    ############################
    # Candidate image preparation
#    cimg = Image.open(cinfile)
#    cimg = cimg.convert('1')  # convert image to 1 bit
#    cimg.save(cimg_filename_bw, 'PNG')
#    print("recover_compared_image: Image size: {}".format(cimg.size))
    print("recover_compared_image from slides: {}, {}".format(slide_filename_A, slide_filename_B))
    # Open slides images
    slide_filename_1 = slide_filename_A + ext
    slide_filename_2 = slide_filename_B + ext
    slide_image_1 = Image.open(slide_filename_1)
    slide_image_2 = Image.open(slide_filename_2)


    width = slide_image_1.size[0]
    height = slide_image_1.size[1]
    recovered_image = Image.new('1', slide_image_1.size)


    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
            pixels_xy = slide_image_1.getpixel((x*2, y*2)) & slide_image_2.getpixel((x*2, y*2))
            pixels_x1y = slide_image_1.getpixel((x*2+1, y*2)) & slide_image_2.getpixel((x*2+1, y*2))
            pixels_xy1 = slide_image_1.getpixel((x*2, y*2+1)) & slide_image_2.getpixel((x*2, y*2+1))
            pixels_x1y1 = slide_image_1.getpixel((x*2+1, y*2+1)) & slide_image_2.getpixel((x*2+1, y*2+1))
            print("pixels_xy: {}, pixels_x1y:{}, pixels_xy1: {}, pixels_x1y1: {}".format(pixels_xy, pixels_x1y, pixels_xy1, pixels_x1y1))

            # AND candidate and target slide images
            recovered_image.putpixel((x*2, y*2), slide_image_1.getpixel((x*2, y*2)) & slide_image_2.getpixel((x*2, y*2)))
            recovered_image.putpixel((x*2+1, y*2), slide_image_1.getpixel((x*2+1, y*2)) & slide_image_2.getpixel((x*2+1, y*2)))
            recovered_image.putpixel((x*2, y*2+1), slide_image_1.getpixel((x*2, y*2+1)) & slide_image_2.getpixel((x*2, y*2+1)))
            recovered_image.putpixel((x*2+1, y*2+1), slide_image_1.getpixel((x*2+1, y*2+1)) & slide_image_2.getpixel((x*2+1, y*2+1)))


    recovered_image_name = Path(cinfile).stem
    recovered_image_name = 'out_images/' + recovered_image_name + '_R' + ext
    print("recover_compared_image: recovered_image name: {}".format(recovered_image_name))
    recovered_image.save(recovered_image_name, 'PNG')
    return

def encryptImage(infile):
    img = Image.open(infile)

    img = img.convert('1')  # convert image to 1 bit
    img.save(img_filename_bw, 'PNG')

    print("encryptImage: Target Image size: {}".format(img.size))
    # Prepare two empty slider images for drawing
    width = img.size[0]*2
    height = img.size[1]*2
    print("Slide size{} x {}".format(width, height))
    slide_image_A = Image.new('1', (width, height))
    slide_image_B = Image.new('1', (width, height))
    draw_A = ImageDraw.Draw(slide_image_A)
    draw_B = ImageDraw.Draw(slide_image_B)
    # There are 6(4 choose 2) possible patterns
    patterns = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
                (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))
    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
            pixel = img.getpixel((x, y))
            if type(pixel) == tuple:
                print("Error: The pixel is RGB, convert it to grey scale before running the encryption".format(infile))
                exit()
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

    slide_image_A.save(slide_filename_A + ".png", 'PNG')
    slide_image_B.save(slide_filename_B + ".png", 'PNG')

def and_images(cinfile, slide_filename):
    ############################
    # Candidate image preparation
    cimg = Image.open(cinfile)
    cimg = cimg.convert('1')  # convert image to 1 bit
    cimg.save(cimg_filename_bw, 'PNG')
    print("and_images: Candidate Image size: {}".format(cimg.size))
    # Slides images preparation
    if not os.path.isfile(slide_filename  + ".png"):
        print("Error: File {} does not exist.".format(slide_filename  + ".png"))
        exit()
    slide = Image.open(slide_filename  + ".png")


    width = cimg.size[0]*2
    height = cimg.size[1]*2
    slide_image_1 = Image.new('1', (width, height))
    slide_image_2 = Image.new('1', (width, height))
    slide_filename_1 = slide_filename + '_P.png'
    slide_filename_2 = slide_filename + '_N.png'

    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
            pixel2 = cimg.getpixel((x, y))

            # AND candidate and target slide images
            slide_image_1.putpixel((x*2, y*2), slide.getpixel((x*2, y*2)) & pixel2)
            slide_image_1.putpixel((x*2+1, y*2), slide.getpixel((x*2+1, y*2)) & pixel2)
            slide_image_1.putpixel((x*2, y*2+1), slide.getpixel((x*2, y*2+1)) & pixel2)
            slide_image_1.putpixel((x*2+1, y*2+1), slide.getpixel((x*2+1, y*2+1)) & pixel2)

            # AND negative candidate and target slide images
            pixel2 = 256 - 1 - cimg.getpixel((x, y))
            slide_image_2.putpixel((x*2, y*2), slide.getpixel((x*2, y*2)) & pixel2)
            slide_image_2.putpixel((x*2+1, y*2), slide.getpixel((x*2+1, y*2)) & pixel2)
            slide_image_2.putpixel((x*2, y*2+1), slide.getpixel((x*2, y*2+1)) & pixel2)
            slide_image_2.putpixel((x*2+1, y*2+1), slide.getpixel((x*2+1, y*2+1)) & pixel2)

    slide_image_1.save(slide_filename_1, 'PNG')
    slide_image_2.save(slide_filename_2, 'PNG')
    return

def save_negative_image(infile):
    ############################
    # Candidate image preparation
    infile_img = Image.open(infile)
    infile_img = infile_img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))

    infile_name = Path(infile).stem
    infile_img_n = Image.new('1', infile_img.size)
    infile_name_n = "out_images/" + infile_name + '_N.png'

    width = infile_img.size[0]
    height = infile_img.size[1]
    # Cycle through pixels
    for x in xrange(0, int(width)):
        for y in xrange(0, int(height)):
            # Negate image pixel
#            print("Pixels: O:{} N:{}".format(infile_img.getpixel((x, y)), 256 -1 - infile_img.getpixel((x, y))))

            infile_img_n.putpixel((x, y), 256 - 1 - infile_img.getpixel((x, y)))

    infile_img_n.save(infile_name_n, 'PNG')
    return

def main():
    global img_filename_bw
    global cimg_filename_bw
    global slide_filename_A
    global slide_filename_B

    """
    parse the arguments and parse the topology file
    """
    parser = argparse.ArgumentParser(prog='PROG', description='Images manipulation utility')
    parser.add_argument('-t', dest='t', help='The image to be split', required=True, default=False)
    parser.add_argument('-c', dest='c', help="The image to compare", required=True, default=False)
    parser.add_argument('-enc', action='store_true', help='Perform image encryption, default - use existing slides')
    parser.add_argument('-pix', action='store_true', help='Print binary images, default - do not print')
    args = parser.parse_args()

    infile = str(args.t)
    cinfile = str(args.c)
    if not os.path.isfile(infile):
        print("File {} does not exist.".format(infile))
        exit()
    if not os.path.isfile(cinfile):
        print("File {} does not exist.".format(cinfile))
        exit()

    # Set output file names
    f, e = os.path.splitext(infile)
#    print("f:{}".format(f))
    f = Path(infile).stem
#    print("f:{}".format(f))
    img_filename_bw = "out_images/" + f + "_bw.png"
    slide_filename_A = "out_images/" + f + "_slideA"
    slide_filename_B = "out_images/" + f + "_slideB"

    f, e = os.path.splitext(cinfile)
    f = Path(cinfile).stem
    cimg_filename_bw = "out_images/" + f + "_bw_C.png"

    if args.pix:
        print("Going to print images image: {} cimage: {}".format(infile, cinfile))
        printImage(infile)
        printImage(cinfile)
        print("Print Imagaes Done.")

    if args.enc:
        print("Going to encrypt image: {}".format(infile))
        encryptImage(infile)
        print("Encryption Done.")

    # if args.and:
    # #(args.t is None or args.c is None)
    print("Going to compare images {}, {}".format(infile, cinfile))
    print("Going to AND images")
    and_images(cinfile, slide_filename_A)
    and_images(cinfile, slide_filename_B)
    save_negative_image(cinfile)
    print("AND images Done.")

#    if args.rec:
    print("Going to recover and compare images")
    recover_compared_image_count(infile, cinfile, slide_filename_A, slide_filename_B, '_P.png')
    recover_compared_image_count(infile, cinfile, slide_filename_A, slide_filename_B, '_N.png')
    print("recover and compare images Done.")
    
    print("Done.")

if __name__ == '__main__':
    main()
'''
TODO
1. Restore original image from 2 slides
2. Try completely different cimage
3. Add fool proof - check target and candidate images are of the same size
Why images are so similar?
4. count equal pixels
5. add partial operation modes
6. test with simple syntetic images
'''