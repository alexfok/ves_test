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
import itertools
import numpy as np

random = SystemRandom()
# If you want to use the more powerful PyCrypto (pip install pycrypto) then uncomment the next line and comment out the previous two lines
#from Crypto.Random import random
xrange = range
img_filename_bw = ""
cimg_filename_bw = ""
slide_filename_A = ""
slide_filename_B = ""
base_out_dir = "./2025/out_images/"
slides_dir = "./2025/slides/"
_DEBUG = False
#    base_out_dir = "out_images/"

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


def recover_image_compare_orig_count(infile, slide_filenames, b_num = 2, b_pixels_to_flip = 100):
    # Read and convert original image
    orig_img = Image.open(infile)
    # print(f"Original image mode before conversion: {orig_img.mode}")
    
    orig_img = orig_img.convert('1')  # convert to 1 bit
    # print(f"Image mode after conversion: {orig_img.mode}")
    
    orig_arr = np.array(orig_img)
    
    # Count black and white pixels in original image
    orig_total = orig_arr.size
    # In mode '1', True represents white (255) and False represents black (0)
    orig_white = np.sum(orig_arr)  # Count True values (white pixels)
    orig_black = orig_total - orig_white  # Count False values (black pixels)
    print(f"Original Image: total={orig_total}, black={orig_black} ({orig_black/orig_total:.2%}), white={orig_white} ({orig_white/orig_total:.2%})")
    
    # Debug: Print unique values in the array
    unique_values = np.unique(orig_arr)
    print(f"Unique values in array: {unique_values}")
    
    # Open all slides
    slide_images = []
    for slide_filename in slide_filenames:
        slide_images.append(Image.open(slide_filename + ".png"))

    # Get dimensions from first slide
    width = slide_images[0].size[0]
    height = slide_images[0].size[1]
    recovered_image = Image.new('1', slide_images[0].size)

    n_slides = len(slide_images)
    k = (n_slides + 1) // 2  # threshold for number of black pixels, rounded up

    # Select byzantine slides once at the start
    byzantine_slides = set(random.sample(range(len(slide_images)), b_num))  # Randomly select b_num slides to be byzantine
    pixels_flipped = [0] * len(slide_images)  # Counter for flipped pixels per slide

    # Debug counters
    total_pixels = 0
    black_pixels = 0
    white_pixels = 0
    flipped_pixels = 0  # Counter for actually flipped pixels

    # Cycle through pixels
    for x in xrange(0, width):
        for y in xrange(0, height):
            # Get pixel values from all slides
            pixels = []
            for i, slide in enumerate(slide_images):
                pixel = slide.getpixel((x, y))
                # If this is a byzantine slide and we haven't flipped enough pixels yet
                if i in byzantine_slides and pixels_flipped[i] < b_pixels_to_flip:
                    # Flip the pixel value (0->1 or 1->0)
                    pixel = 1 - pixel
                    pixels_flipped[i] += 1
                    flipped_pixels += 1
                pixels.append(pixel)

            # Count black pixels (0 is black, 1 is white)
            black_count = sum(1 for p in pixels if p == 0)
            total_pixels_slides = len(pixels)
            
            # Debug: Print pixel counts for first few pixels
            if _DEBUG:
                if total_pixels < 5:
                    print(f"Pixel at ({x},{y}): black_count={black_count}, total_pixels={total_pixels_slides}")
                    print(f"Pixel values: {pixels}")
            
            # Determine recovered pixel value based on threshold
            # If more than k slides have black pixels, the recovered pixel should be black
            # For n=9, k=5, so we need at least 5 black pixels to recover a black pixel
            recovered_value = 0 if black_count >= k else 1
            
            # Update debug counters
            total_pixels += 1
            if recovered_value == 0:
                black_pixels += 1
            else:
                white_pixels += 1
            
            # Set pixel in recovered image
            recovered_image.putpixel((x, y), recovered_value)

    # Print debug statistics
    print(f"\nDebug Statistics:")
    print(f"Total pixels processed: {total_pixels}")
    print(f"Black pixels: {black_pixels} ({black_pixels/total_pixels:.2%})")
    print(f"White pixels: {white_pixels} ({white_pixels/total_pixels:.2%})")
    print(f"Total pixels flipped: {flipped_pixels}")
    print(f"Pixels flipped per slide: {pixels_flipped}")
    print(f"Byzantine slides: {byzantine_slides}")
    print(f"Threshold k: {k}")

    # Count black and white pixels in recovered image
    recovered_arr = np.array(recovered_image)
    # In mode '1', True represents white (1) and False represents black (0)
    recovered_total = recovered_arr.size
    recovered_white = np.sum(recovered_arr)  # Count True values (white pixels)
    recovered_black = recovered_total - recovered_white  # Count False values (black pixels)
    print(f"Recovered Image: black={recovered_black} ({recovered_black/recovered_total:.2%}), white={recovered_white} ({recovered_white/recovered_total:.2%})")

    # Save recovered image
    recovered_image_name = base_out_dir + Path(infile).stem + '_R.png'
    recovered_image.save(recovered_image_name, 'PNG')
    return black_pixels, white_pixels, black_pixels/total_pixels, white_pixels/total_pixels


def recover_compared_image_count(infile, cinfile, slide_filenames, ext):
    ############################
    # Candidate image preparation
    timg = Image.open(infile)
    timg = timg.convert('1')  # convert image to 1 bit
    cimg = Image.open(cinfile)
    cimg = cimg.convert('1')  # convert image to 1 bit

    # Open all slides
    slide_images = []
    for slide_filename in slide_filenames:
        slide_filename_full = slide_filename + ext
        slide_images.append(Image.open(slide_filename_full))

    # Get dimensions from first slide
    width = slide_images[0].size[0]
    height = slide_images[0].size[1]
    recovered_image = Image.new('1', slide_images[0].size)

    match_pixel_count = 0
    mismatch_pixel_count = 0
    n_slides = len(slide_images)
    k = n_slides // 2  # threshold for number of black subpixels

    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
            # Get subpixels from all slides
            subpixels = []
            for slide in slide_images:
                # Get all 4 subpixels from this slide
                subpixels.append(slide.getpixel((x*2, y*2)))
                subpixels.append(slide.getpixel((x*2+1, y*2)))
                subpixels.append(slide.getpixel((x*2, y*2+1)))
                subpixels.append(slide.getpixel((x*2+1, y*2+1)))

            # Count black subpixels (0 is black, 255 is white)
            black_count = sum(1 for p in subpixels if p == 0)
            
            # Determine recovered pixel value based on threshold
            # If more than k subpixels are black, the recovered pixel should be black
            recovered_value = 0 if black_count > k else 255
            
            # Set all subpixels in recovered image to the same value
            recovered_image.putpixel((x*2, y*2), recovered_value)
            recovered_image.putpixel((x*2+1, y*2), recovered_value)
            recovered_image.putpixel((x*2, y*2+1), recovered_value)
            recovered_image.putpixel((x*2+1, y*2+1), recovered_value)

            timage_pixel_xy = timg.getpixel((x, y))
            cimage_pixel_xy = cimg.getpixel((x, y))
            
            if ext == '_P.png':
                flag = 'Positive'
                if cimage_pixel_xy == 255 and recovered_value == 255:
                    match_pixel_count = match_pixel_count + 1
                elif cimage_pixel_xy == 0 and recovered_value == 0:
                    match_pixel_count = match_pixel_count + 1
                else:
                    mismatch_pixel_count = mismatch_pixel_count + 1
            if ext == '_N.png':
                flag = 'Negative'
                if cimage_pixel_xy == 0 and recovered_value == 0:
                    match_pixel_count = match_pixel_count + 1
                elif cimage_pixel_xy == 255 and recovered_value == 255:
                    match_pixel_count = match_pixel_count + 1
                else:
                    mismatch_pixel_count = mismatch_pixel_count + 1

    recovered_image_name = Path(cinfile).stem
    recovered_image_name = base_out_dir + recovered_image_name + '_R' + ext
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
    recovered_image_name = base_out_dir + recovered_image_name + '_R' + ext
    print("recover_compared_image: recovered_image name: {}".format(recovered_image_name))
    recovered_image.save(recovered_image_name, 'PNG')
    return

def encryptImage(infile, n_slides=2):
    img = Image.open(infile)
    img = img.convert('1')  # convert image to 1 bit
    img.save(img_filename_bw, 'PNG')
    print("encryptImage: Target Image size: {}".format(img.size))
    width = img.size[0]  # Use original width
    height = img.size[1]  # Use original height
    print("Slide size {} x {}".format(width, height))
    
    # Prepare N empty slide images
    slide_images = [Image.new('1', (width, height)) for _ in range(n_slides)]
    draws = [ImageDraw.Draw(slide) for slide in slide_images]
    
    k = (n_slides + 1) // 2  # threshold for number of black pixels, rounded up
    
    # For each pixel in the original image
    for x in xrange(0, width):
        for y in xrange(0, height):
            pixel = img.getpixel((x, y))
            if type(pixel) == tuple:
                print("Error: The pixel is RGB, convert it to grey scale before running the encryption".format(infile))
                exit()
            
            # For black pixels: k+1 subpixels are black
            # For white pixels: k-1 subpixels are black
            n_black = k if pixel == 0 else k - 1
            
            # Create a list of subpixel values for this pixel
            # Each pixel gets one value per slide
            subpixels = [0] * n_black + [255] * (n_slides - n_black)
            random.shuffle(subpixels)  # Shuffle to randomize which slides get black/white
            
            # Debug: Print subpixel values for first few pixels
            if _DEBUG:
                if x < 2 and y < 2:
                    print(f"Original pixel at ({x},{y}): {pixel}")
                    print(f"Number of black subpixels: {n_black}")
                    print(f"Subpixel values: {subpixels}")
            
            # Assign one value to each slide
            for i, draw in enumerate(draws):
                draw.point((x, y), subpixels[i])
    
    # Save all slides
    for i, slide in enumerate(slide_images):
        slide.save(f"{slides_dir}{Path(infile).stem}_slide{i}.png", 'PNG')

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
    infile_name_n = base_out_dir + infile_name + '_N.png'

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

def encryptImageCol(infile):
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
    parser.add_argument('-c', dest='c', help="The image to compare", default=None)
    parser.add_argument('-enc', action='store_true', help='Perform image encryption, default - use existing slides')
    parser.add_argument('-pix', action='store_true', help='Print binary images, default - do not print')
    parser.add_argument('-encc', action='store_true', help='Perform color image encryption')
    parser.add_argument('--nslides', type=int, default=2, help='Number of slides to generate (default: 2)')
    parser.add_argument('--comp1', action='store_true', help='Compare original and recovered images with detailed pixel statistics')
    parser.add_argument('--b_num', type=lambda x: [int(i) for i in x.split(',')], default=[2], help='List of numbers of byzantine slides (default: [2])')
    parser.add_argument('--b_pixels', type=int, default=100, help='Number of pixels to flip in byzantine slides (default: 100)')
    args = parser.parse_args()

    infile = str(args.t)
    cinfile = str(args.c) if args.c is not None else None
    n_slides = args.nslides
    if not os.path.isfile(infile):
        print("File {} does not exist.".format(infile))
        exit()
    if cinfile and not os.path.isfile(cinfile):
        print("File {} does not exist.".format(cinfile))
        exit()

    # Set output file names
    f, e = os.path.splitext(infile)
    f = Path(infile).stem
    img_filename_bw = base_out_dir + f + "_bw.png"
    
    # Generate slide filenames for N slides
    slide_filenames = [slides_dir + f + f"_slide{i}" for i in range(n_slides)]

    if cinfile:
        f, e = os.path.splitext(cinfile)
        f = Path(cinfile).stem
        cimg_filename_bw = base_out_dir + f + "_bw_C.png"

    if args.encc:
        print("Going to encrypt image: {}".format(infile))
        encryptImageCol(infile)
        print("Encryption Done.")
        exit()

    if args.pix:
        print("Going to print images image: {} cimage: {}".format(infile, cinfile))
        printImage(infile)
        printImage(cinfile)
        print("Print Imagaes Done.")

    if args.enc:
        print(f"Going to encrypt image: {infile} with {n_slides} slides")
        encryptImage(infile, n_slides=n_slides)
        print("Encryption Done.")

    if cinfile:
        print("Going to compare images {}, {}".format(infile, cinfile))
        print("Going to AND images")
        for slide_filename in slide_filenames:
            and_images(cinfile, slide_filename)
        save_negative_image(cinfile)
        print("AND images Done.")

    if args.comp1:
        print("\nPerforming detailed comparison of original and recovered images:")
        # Compare original and recovered images with detailed pixel statistics
        # Create list of tuples for different b_num and b_pixels combinations
        byzantine_configs = [(b_num, args.b_pixels) for b_num in args.b_num]
        
        # Store results for plotting
        results = []
        
        # Run recovery for each configuration
        for b_num, b_pixels in byzantine_configs:
            print(f"\nTesting with b_num={b_num}, b_pixels={b_pixels}")
            black_pixels, white_pixels, black_percentage, white_percentage = recover_image_compare_orig_count(infile, slide_filenames, b_num=b_num, b_pixels_to_flip=b_pixels)
            
            results.append((b_num, b_pixels, black_percentage))
        
        # Plot results
        import matplotlib.pyplot as plt
        
        # Extract data for plotting
        x_values = [f"({b_num},{b_pixels})" for b_num, b_pixels, _ in results]
        y_values = [black_percentage for _, _, black_percentage in results]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, 'bo-')
        plt.xlabel('Byzantine Configuration (b_num, b_pixels)')
        plt.ylabel('Black Pixel Percentage')
        plt.title('Effect of Byzantine Configuration on Black Pixel Percentage')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot
        plt.savefig(f"{base_out_dir}byzantine_effect.png")
        plt.close()
    print("recover and compare images Done.")
    print("Compare original and recovered images Done.")
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