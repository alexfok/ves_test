import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os
import sys
from random import SystemRandom
import argparse
from pathlib import Path
import random
import cv2

#random = SystemRandom()

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

def create_gby_slide(infile):
    ############################
    # Candidate image preparation
    img = Image.open(infile)
#    img = img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
#    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))

    infile_name = Path(infile).stem
#    infile_img_n = Image.new('1', img.size)
    outfile = infile_name + '_BWVESSlide.png'

    width = img.size[0]
    height = img.size[1]
    # Define the blue color
    blue_color = (0, 0, 255)  # RGB value for blue
    green_color = (0, 255, 0)  # RGB value for green
    yellow_color = (255, 255, 0)  # RGB value for yellow
    img2 = Image.new(mode="RGB", size=(width, height), color = blue_color)
    # Define the colors
#    colors = ["blue", "yellow"]
    colors = [blue_color, yellow_color]  # Blue and yellow colors
    black_pixels_count = 0
    white_pixels_count = 0

    # Cycle through pixels
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            # Draw a random color
            random_color = random.choice(colors)
            img2.putpixel((x, y), random_color)

    print("WXH ({},{}) black_pixels_count: {} white_pixels_count {}".format(width, height, black_pixels_count, white_pixels_count))
    # 262144

    img2.save(outfile, 'PNG')
#    printImage(outfile)
    return
def create_gby_image_cv2(infile):
    ############################
    # Candidate image preparation
    # img = Image.open(infile)
    img = cv2.imread(infile)

    img = img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
#    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))

    infile_name = Path(infile).stem
#    infile_img_n = Image.new('1', img.size)

    width = img.size[0]
    height = img.size[1]
    # Define the blue color
    blue_color = (0, 0, 255)  # RGB value for blue
    green_color = (0, 255, 0)  # RGB value for green
    yellow_color = (255, 255, 0)  # RGB value for yellow
    img2 = Image.new(mode="RGB", size=(width, height), color = blue_color)
    # Define the colors
#    colors = ["blue", "yellow"]
    colors = [blue_color, yellow_color]  # Blue and yellow colors
    black_pixels_count = 0
    white_pixels_count = 0

    # Cycle through pixels
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            pixel = img.getpixel((x, y))
            if pixel == 0:
#                pixels[i, j] = blue_color
#                print('black pixel: {}'.format(pixel))
                img2.putpixel((x, y), green_color)
                black_pixels_count+=1
            else:
#                print('white pixel: {}'.format(pixel))
                # Draw a random color
                random_color = random.choice(colors)
#                random_color = blue_color
                img2.putpixel((x, y), random_color)
                white_pixels_count+=1
#            if type(pixel) == tuple:
#                print(pixel)

            # Negate image pixel
#            print("Pixels: O:{} N:{}".format(infile_img.getpixel((x, y)), 256 -1 - infile_img.getpixel((x, y))))
    print("WXH ({},{}) black_pixels_count: {} white_pixels_count {}".format(width, height, black_pixels_count, white_pixels_count))
    # 262144

#    img2.save(outfile, 'PNG')
    cv2.imwrite(infile_name + '_BWVES.png', img2)

#    printImage(outfile)
    return

def create_gby_image(infile, root_dir='./2024'):
    ############################
    print(f'create_gby_image: {infile}')
    # Candidate image preparation
    img = Image.open(infile)

    img = img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
#    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))

    infile_name = Path(infile).stem
#    infile_img_n = Image.new('1', img.size)

    width = img.size[0]
    height = img.size[1]
    # Define the blue color
    blue_color = (0, 0, 255)  # RGB value for blue
    green_color = (0, 255, 0)  # RGB value for green
    yellow_color = (255, 255, 0)  # RGB value for yellow
    img2 = Image.new(mode="RGB", size=(width, height), color = blue_color)
    # Define the colors
#    colors = ["blue", "yellow"]
    colors = [blue_color, yellow_color]  # Blue and yellow colors
    black_pixels_count = 0
    white_pixels_count = 0

    # Cycle through pixels
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            pixel = img.getpixel((x, y))
            if pixel == 0:
#                pixels[i, j] = blue_color
#                print('black pixel: {}'.format(pixel))
                img2.putpixel((x, y), green_color)
                black_pixels_count+=1
            else:
#                print('white pixel: {}'.format(pixel))
                # Draw a random color
                random_color = random.choice(colors)
#                random_color = blue_color
                img2.putpixel((x, y), random_color)
                white_pixels_count+=1
#            if type(pixel) == tuple:
#                print(pixel)

            # Negate image pixel
#            print("Pixels: O:{} N:{}".format(infile_img.getpixel((x, y)), 256 -1 - infile_img.getpixel((x, y))))
    print("WXH ({},{}) black_pixels_count: {} white_pixels_count {}".format(width, height, black_pixels_count, white_pixels_count))
    # 262144
    outfile = root_dir + '/' + infile_name + '_BW.png'
    print(f'create_gby_image outfile: {outfile}')
    img.save(outfile, 'PNG')
    outfile = root_dir + '/' + infile_name + '_BWVES.png'
    print(f'create_gby_image outfile: {outfile}')
    img2.save(outfile, 'PNG')

#    cv2.imwrite(infile_name + '_BWVES.png', img2)

#    printImage(outfile)
    return


################################
# RGB slides games
def create_rgb_slide(infile, root_dir='ncaieee_ext'):
    ############################
    # Candidate image preparation
    #img = Image.open(infile)
#    img = img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
#    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))

    infile_name = Path(infile).stem

    # Split the image into R, G, and B channels
    # Load the RGB image
    image = cv2.imread(infile)
#    img_b, img_g, img_r = cv2.split(image)
    # Convert the image to RGB color space
#    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_rgb = image

    # Extract the R, G, and B channels
    img_b = img_rgb[:, :, 0]
    img_g = img_rgb[:, :, 1]
    img_r = img_rgb[:, :, 2]

    # Create a new image with only the blue channel
    out_img_r = np.zeros_like(image)
    out_img_g = np.zeros_like(image)
    out_img_b = np.zeros_like(image)
#    out_img_r[:, :, 0] = img_r
#    out_img_g[:, :, 1] = img_g
#    out_img_b[:, :, 2] = img_b
    out_img_b[:, :, 0] = img_rgb[:, :, 0]
    out_img_g[:, :, 1] = img_rgb[:, :, 1]
    out_img_r[:, :, 2] = img_rgb[:, :, 2]

    # Save or work with the individual channels as needed
    
    cv2.imwrite(root_dir + '/' + infile_name + '_gr_r.png', img_r)
    cv2.imwrite(root_dir + '/' + infile_name + '_gr_g.png', img_g)
    cv2.imwrite(root_dir + '/' + infile_name + '_gr_b.png', img_b)
    cv2.imwrite(root_dir + '/' + infile_name + '_c_r.png', out_img_r)
    cv2.imwrite(root_dir + '/' + infile_name + '_c_g.png', out_img_g)
    cv2.imwrite(root_dir + '/' + infile_name + '_c_b.png', out_img_b)

#    printImage(infile_name + '_gr_r.png')
#    printImage(infile_name + '_gr_b.png')
#    return

    out_img_r2 = np.zeros_like(image)
    out_img_g2 = np.zeros_like(image)
    out_img_b2 = np.zeros_like(image)
    print(image.shape)
    print(image.size)
    width = image.shape[0]
    height = image.shape[1]
    # Define the colors
    white_color = (255, 255, 255)  # RGB value for blue
    blue_color = (255, 0, 0)  # RGB value for blue
    green_color = (0, 255, 0)  # RGB value for green
    red_color = (0, 0, 255)  # RGB value for red
#    img2 = Image.new(mode="RGB", size=(width, height), color = blue_color)
    # Define the colors
    colors_b = [blue_color, white_color]
    colors_g = [green_color, white_color]
    colors_r = [red_color, white_color]
    black_pixels_count = 0
    white_pixels_count = 0

    # Cycle through pixels
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            # Draw a random color
            random_color = random.choice(colors_b)
            out_img_b2[x, y] = random_color
            random_color = random.choice(colors_g)
            out_img_g2[x, y] = random_color
            random_color = random.choice(colors_r)
            out_img_r2[x, y] = random_color

    print("WXH ({},{}) black_pixels_count: {} white_pixels_count {}".format(width, height, black_pixels_count, white_pixels_count))
    # 262144

    cv2.imwrite(root_dir + '/' + infile_name + '_slide_b.png', out_img_b2)
    cv2.imwrite(root_dir + '/' + infile_name + '_slide_g.png', out_img_g2)
    cv2.imwrite(root_dir + '/' + infile_name + '_slide_r.png', out_img_r2)
    #img2.save(outfile, 'PNG')
#    printImage(outfile)
    return

def create_single_rgb_slide(infile, color, root_dir='ncaieee_ext'):
    ############################
    # Candidate image preparation
    #img = Image.open(infile)
#    img = img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
#    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))
    print('create_single_rgb_slide')
    infile_name = Path(infile).stem
    # infile_name = root_dir + '/' + infile_name
    # Split the image into R, G, and B channels
    # Load the RGB image
    image = cv2.imread(infile)
#    img_b, img_g, img_r = cv2.split(image)
    # Convert the image to RGB color space
#    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_rgb = image

    # Extract the R, G, and B channels and Create a new images with only single channel
    out_img_c = np.zeros_like(image)
    if color == 'b':
        out_img_gr = img_rgb[:, :, 0]
        out_img_c[:, :, 0] = img_rgb[:, :, 0]
    elif color == 'g':
        out_img_gr = img_rgb[:, :, 1]
        out_img_c[:, :, 1] = img_rgb[:, :, 1]
    elif color == 'r':
        out_img_gr = img_rgb[:, :, 2]
        out_img_c[:, :, 2] = img_rgb[:, :, 2]

    # Save or work with the individual channels as needed
    print(out_img_gr.shape)
    print(out_img_gr.size)
    cv2.imwrite(root_dir + '/' + infile_name + f'_gr_{color}.png', out_img_gr)
    cv2.imwrite(root_dir + '/' + infile_name + f'_c_{color}.png', out_img_c)

    out_img_2 = np.zeros_like(image)
#    print(image.shape)
#    print(image.size)
    width = image.shape[0]
    height = image.shape[1]
    # Define the colors
    white_color = (255, 255, 255)  # RGB value for blue
    blue_color = (255, 0, 0)  # RGB value for blue
    green_color = (0, 255, 0)  # RGB value for green
    red_color = (0, 0, 255)  # RGB value for red
#    img2 = Image.new(mode="RGB", size=(width, height), color = blue_color)
    # Define the colors
    colors = []
    if color == 'b':
        colors = [blue_color, white_color]
    elif color == 'g':
        colors = [green_color, white_color]
    elif color == 'r':
        colors = [red_color, white_color]

    # Cycle through pixels and create random slide from the original and white color
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            # Draw a random color
            random_color = random.choice(colors)
            out_img_2[x, y] = random_color

    cv2.imwrite(infile_name + f'_slide_{color}.png', out_img_2)
##
    # Cycle through pixels and create random slide from the original and white color
    # Redefine the colors
    out_img_2gr = np.zeros_like(image)
    out_img_2c = np.zeros_like(image)
    random_percentage = random.uniform(0, 100)
    random_percentage = 30.0
    print(f'random_percentage: {random_percentage}')
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            # Draw a random color
            random_color = random.choice(colors)
            out_img_2gr[x,y] = out_img_gr[x,y]
            out_img_2c[x,y] = out_img_c[x,y]
            out_img_2gr[x,y] = out_img_2gr[x,y] - (random_percentage / 100) * out_img_2gr[x,y]
            if color == 'b':
                #out_img_2gr[x,y,0] = out_img_2gr[x,y,0] - (random_percentage / 100) * out_img_2gr[x,y,0]
                out_img_2c[x,y,0] = out_img_2c[x,y,0] - (random_percentage / 100) * out_img_2c[x,y,0]
            elif color == 'g':
                #out_img_2gr[x,y,1] = out_img_2gr[x,y,1] - (random_percentage / 100) * out_img_2gr[x,y,0]
                out_img_2c[x,y,1] = out_img_2c[x,y,1] - (random_percentage / 100) * out_img_2c[x,y,0]
            elif color == 'r':
                #out_img_2gr[x,y,2] = out_img_2gr[x,y,2] - (random_percentage / 100) * out_img_2gr[x,y,0]
                out_img_2c[x,y,2] = out_img_2c[x,y,2] - (random_percentage / 100) * out_img_2c[x,y,0]

    cv2.imwrite(infile_name + f'_slide_{color}_gr_sub.png', out_img_2gr)
    cv2.imwrite(infile_name + f'_slide_{color}_c_sub.png', out_img_2c)
    #img2.save(outfile, 'PNG')
#    printImage(outfile)
    return

################################
# ncaieee games
def recover_image(infile):
    print('recover_image')
    infile_name = Path(infile).stem
    infile_name = 'ncaieee/' + infile_name
    # Split the image into R, G, and B channels
    # Load the RGB image
    image_r_gr = cv2.imread(infile_name + f'_slide_r_gr_sub.png')
    image_g_gr = cv2.imread(infile_name + f'_slide_g_gr_sub.png')
    image_b_gr = cv2.imread(infile_name + f'_slide_b_gr_sub.png')
    image_r_c = cv2.imread(infile_name + f'_slide_r_c_sub.png')
    image_g_c = cv2.imread(infile_name + f'_slide_g_c_sub.png')
    image_b_c = cv2.imread(infile_name + f'_slide_b_c_sub.png')
#    img_b, img_g, img_r = cv2.split(image)
    # Convert the image to RGB color space
#    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    out_img_2gr = np.zeros_like(image_r_gr)
    out_img_2c = np.zeros_like(image_r_c)


    out_img_2c[:, :, 0] = image_b_c[:, :, 0]
    out_img_2c[:, :, 1] = image_g_c[:, :, 1]
    out_img_2c[:, :, 2] = image_r_c[:, :, 2]
    # Calculate the average of corresponding values

#    out_img_2gr[:, :,] = (image_r_gr[:, :,] + image_g_gr[:, :,] + image_b_gr[:, :,])/3 + 30
    out_img_2gr = (image_r_gr + image_g_gr + image_b_gr)/3 + 30

    width = out_img_2gr.shape[0]
    height = out_img_2gr.shape[1]
    random_percentage = random.uniform(0, 100)
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            out_img_2c[x,y,0] = out_img_2c[x,y,0] - (random_percentage / 100) * out_img_2c[x,y,0]
            out_img_2c[x,y,1] = out_img_2c[x,y,1] - (random_percentage / 100) * out_img_2c[x,y,1]
            out_img_2c[x,y,2] = out_img_2c[x,y,2] - (random_percentage / 100) * out_img_2c[x,y,2]
            #out_img_2c[x, y,0] = (image_r_gr[x, y] + image_g_gr[x, y] + image_b_gr[x, y])/3

    cv2.imwrite(infile_name + f'_slide_gr_rec.png', out_img_2gr)
    cv2.imwrite(infile_name + f'_slide_c_rec.png', out_img_2c)

def create_gs_image(infile, root_dir = './2024'):
    print('create_gs_image')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem
    infile_name_gs = root_dir + '/' + infile_name + 'gs.png'

    # Convert to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    print(f'create_gs_image infile_name_gs: {infile_name_gs}')
    cv2.imwrite(infile_name_gs, gray_image)
    # Apply binary thresholding
    # 127 is the threshold value, and 255 is the maximum value that can be assigned
    infile_name_bw = root_dir + '/' + infile_name + 'bw.png'
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    print(f'create_gs_image infile_name_bw: {infile_name_bw}')
    cv2.imwrite(infile_name_bw, binary_image)


def ves_games(infile):
    print('ves_games')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem

    # Convert to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    shifted_pixels_count = 0
    high_range_limit_count = 0
    width = gray_image.shape[0]
    height = gray_image.shape[1]
    some_ranges = [(0, 31), (32, 63), (96, 127)]
    step_ranges = [(0, 31), (32, 63), (64, 95), (96, 127), (128, 159), (160, 191), (192, 223), (224, 255)]
    # Cycle through pixels
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            # Draw a random color
            for start, end in some_ranges:
                if start <= gray_image[x, y] <= end:
                    # in_range = True
                    gray_image[x, y] += 32
                    shifted_pixels_count += 1
    # Cycle through pixels
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            # Draw a random color
            for start, end in step_ranges:
                if start <= gray_image[x, y] <= end:
                    # in_range = True
                    if gray_image[x, y] == end:
                        high_range_limit_count += 1
                    gray_image2[x, y] = end

    print("shifted_pixels_count: {} out of total pixels: {}, high_range_limit_count: {}".format(shifted_pixels_count, width*height, high_range_limit_count))

    # Save the grayscale image
    cv2.imwrite('ncaieee_ext/' + infile_name + '_shifted.png', gray_image)
    cv2.imwrite('ncaieee_ext/' + infile_name + '_gs_8c.png', gray_image2)

def create_ranges(X, n):
    ranges = []

    # Start with the first range
    start = 0
    end = start + n - 1  # The first range can have a size of at most n or X, whichever is smaller

    while start < X:
        ranges.append((start, end))

        # Move to the next range
        start = end + 1
        end = start + n - 1

    return ranges

def add_random_noise_img(infile):
    print('add_random_noise_img')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem

    # Convert to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    shifted_pixels_count = 0
    width = gray_image.shape[0]
    height = gray_image.shape[1]
    step_ranges = create_ranges(256, 32)
    # Select X random ranges from the list
    some_ranges = random.sample(step_ranges, 5)
#    some_ranges = [(0, 31), (32, 63), (96, 127)]
#    step_ranges = [(0, 31), (32, 63), (64, 95), (96, 127), (128, 159), (160, 191), (192, 223), (224, 255)]
    # Cycle through pixels
    for x in range(0, int(width)):
        for y in range(0, int(height)):
            # Draw a random color
            random_integer = random.randint(0, 31)
            for start, end in some_ranges:
                if start <= gray_image[x, y] <= end:
                    # in_range = True
                    gray_image[x, y] += random_integer
                    shifted_pixels_count += 1

    print("shifted_pixels_count: {} out of total pixels: {}".format(shifted_pixels_count, width*height))

    # Save the grayscale image
    out_file_name = 'ncaieee_ext/' + infile_name + '_shifted.png'
    print(f'save image: {out_file_name}')
    cv2.imwrite(out_file_name, gray_image)

def create_unary_labels(n_labels):
#    labels = create_unary_labels(3, 32, step_ranges)
#    n_labels = len(selected_ranges)
    labels = []
    print(f'create_unary_labels: n_labels: {n_labels}')
    for i in range(n_labels):
#        range_index = selected_ranges[i]
        label = [0] * n_labels  # Initialize a list of zeros for each range
#        label = [0] * 8  # Initialize a list of 8 zeros

        # Set the corresponding range's label to 1
#        label[i] = 1
#        print(f'{i}: label before: {label}')
#        label[:i] = [1] * (i+1)
#        label[:i] = [1] * i
        label[i:] = [1] * (n_labels - i)
#        print(f'label after: {label}')
        #labels.append(label)
        labels.insert(0, label)

    return labels

# print_orig_and_unary_pixels - Run on the original image and print coordinates, original pixel value, unary label value from the steps_ranges list
# run on 3 color files
def print_orig_and_unary_pixels(r_infile, g_infile, b_infile,
                                search_range = (200, 255), steps_ranges = [4,64]):
    print('print_orig_and_unary_pixels')
    # Load the RGB image
    r_image = cv2.imread(r_infile)
    infile_name = Path(infile).stem
    print(f'print_orig_and_unary_pixels: read input image: {r_infile}')
    print(f'print_orig_and_unary_pixels: search_ranges: {search_range}, steps_ranges: {steps_ranges}')
    # Convert to grayscale
    r_gray_image = cv2.cvtColor(r_image, cv2.COLOR_BGR2GRAY)

    g_image = cv2.imread(g_infile)
    b_image = cv2.imread(b_infile)
    g_gray_image = cv2.cvtColor(g_image, cv2.COLOR_BGR2GRAY)
    b_gray_image = cv2.cvtColor(b_image, cv2.COLOR_BGR2GRAY)

    width = r_gray_image.shape[0]
    height = r_gray_image.shape[1]
#    steps_ranges = [2,4,8,16,32,64,128]
#    steps_ranges = [64,128]
#    range_size = 32
#    n_colors = 256//range_size
    for range_size in steps_ranges:
        step_ranges = create_ranges(256, range_size)
        found_pixel_count = 0
        # print(step_ranges)
        # n_colors = 256//range_size
        # labels = create_unary_labels(len(step_ranges))
        # print(f"range_size: {range_size}, Label: {labels[0]}")
        print(f"range_size: {range_size}")

        # Zero out gray_image
        #gray_image[:] = 0
        # Cycle through pixels
        for x in range(0, int(width)):
            for y in range(0, int(height)):
                for start, end in step_ranges:
                    if  start <= r_gray_image[x, y] <= end and \
                        start <= g_gray_image[x, y] <= end and \
                        start <= b_gray_image[x, y] <= end and \
                        search_range[0] <= r_gray_image[x, y] <= search_range[1] and \
                        search_range[0] <= g_gray_image[x, y] <= search_range[1] and \
                        search_range[0] <= b_gray_image[x, y] <= search_range[1]:
                        # in_range = True
                        found_pixel_count += 1
                        print(f'XY{x,y}: RGB{r_gray_image[x, y], g_gray_image[x, y], b_gray_image[x, y]} -> {end}')
#                        print(f'XY{x,y}: RGB{r_gray_image[x, y], g_gray_image[x, y], b_gray_image[x, y]} -> start, end:{start, end}')

        # Save the grayscale image
        # out_file_name = root_dir + '/' + infile_name + f'_gs_{n_colors}c_noinc.png'
        # print(f'save image: {out_file_name}')
        # cv2.imwrite(out_file_name, gray_image)
        print(f'found_pixel_count: {found_pixel_count}')

# create_unary_images_no_inc - Operate on the original image and creates image of the original size
def create_unary_images_no_inc(infile, root_dir='ncaieee_ext'):
    print('create_unary_images_no_inc')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem
    print(f'create_unary_images_no_inc: read input image: {infile}')

    # Convert to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    width = gray_image.shape[0]
    height = gray_image.shape[1]
    steps_ranges = [2,4,8,16,32,64,128]
#    steps_ranges = [64,128]
#    range_size = 32
#    n_colors = 256//range_size
    for range_size in steps_ranges:
        step_ranges = create_ranges(256, range_size)
        # print(step_ranges)
        n_colors = 256//range_size
        # labels = create_unary_labels(len(step_ranges))
        # print(f"range_size: {range_size}, Label: {labels[0]}")
        print(f"range_size: {range_size}")

        # Zero out gray_image
        #gray_image[:] = 0
        # Cycle through pixels
        for x in range(0, int(width)):
            for y in range(0, int(height)):
                for start, end in step_ranges:
                    if start <= gray_image[x, y] <= end:
                        # in_range = True
                        gray_image[x, y] = end

        # Save the grayscale image
        out_file_name = root_dir + '/' + infile_name + f'_gs_{n_colors}c_noinc.png'
        print(f'save image: {out_file_name}')
        cv2.imwrite(out_file_name, gray_image)

def get_pixel_range(pixel_value, ranges):
    idx = 0
    for start, end in ranges:
        if start <= pixel_value <= end:
            return idx
        idx += 1
    return -1

def get_pixel_from_label(label):
    if label == 0:
        return 0
    else:
        return 255
# create_unary_images - Creates increased image - each original pixel is replaced by the unary label
def create_unary_images(infile, root_dir='ncaieee_ext'):
    print('create_unary_images2')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem

    print(f'create_unary_images2: read input image: {infile}')
    # Convert to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    width = gray_image.shape[0]
    height = gray_image.shape[1]
    steps_ranges = [2,4,8,16,32,64,128]
    scale_factors = [(8,16),(8,8),(4,8),(4,4),(2,4),(2,2),(1,2)]
    # steps_ranges = [8]
    # scale_factors = [(4,8)]

    for range_size, scale_factor in zip(steps_ranges,scale_factors):
        step_ranges = create_ranges(256, range_size)
        #print(step_ranges)
        n_colors = 256//range_size
        # label_len=n_colors and number of labels
        label_len = len(step_ranges)
        labels = create_unary_labels(label_len)
        print(f"range_size: {range_size}, scale_factor: {scale_factor}, n_colors: {n_colors}, Labels[0]: {labels[0]}")

        # Get the dimensions of the existing array
        width_in, height_in = gray_image.shape

        # Create a new larger array filled with zeros
        width = width_in * scale_factor[0]
        height = height_in * scale_factor[1]
        out_img = np.zeros((width, height), dtype=gray_image.dtype)

        #out_img = np.zeros_like(gray_image*label_len)
        width = out_img.shape[0]
        height = out_img.shape[1]

        print(f'width: {width}, height: {height}')
        # Cycle through pixels
        for x in range(0, width_in):
            for y in range(0, height_in):
                #print(f'x,y: {x},{y}')
                range_index = get_pixel_range(gray_image[x, y], step_ranges)
                for i in range(0, scale_factor[0]):
                    for j in range(0, scale_factor[1]):
                        #print(f'i,j:{i,j} y*scale_factor[1]+j: {y*scale_factor[1]+j},  x*scale_factor[0]+i: {x*scale_factor[0]+i}')
                        if y*scale_factor[1]+j < height and x*scale_factor[0]+i < width:
                            #print(f'i*scale_factor[0] + j: {i*scale_factor[0] + j}')
                            #print(f'j*scale_factor[1] + i: {j*scale_factor[1] + i}')
                            out_img[x*scale_factor[0]+i, y*scale_factor[1]+j] = get_pixel_from_label(labels[range_index][i*scale_factor[0] + j])

        # Save the grayscale image
        out_file_name = root_dir + '/' + infile_name + f'_gs_{n_colors}c_inc.png'
        print(f'save image: {out_file_name}')
        cv2.imwrite(out_file_name, out_img)


def ncaieee_rgb_games(infile):
#    create_single_rgb_slide(infile, color)
    infile_name = Path(infile).stem

    # create_unary_images_no_inc - Operate on the original image and creates image of the original size
    # create_unary_images_no_inc('ncaieee_ext/' + infile_name + '_gr_r.png', root_dir='ncaieee_rgb_games')
    # create_unary_images_no_inc('ncaieee_ext/' + infile_name + '_gr_g.png', root_dir='ncaieee_rgb_games')
    # create_unary_images_no_inc('ncaieee_ext/' + infile_name + '_gr_b.png', root_dir='ncaieee_rgb_games')

    # create_unary_images - Creates increased image - each original pixel is replaced by the unary label
    # create_unary_images('ncaieee_ext/' + infile_name + '_gr_r.png', root_dir='ncaieee_rgb_games')
    # create_unary_images('ncaieee_ext/' + infile_name + '_gr_g.png', root_dir='ncaieee_rgb_games')
    # create_unary_images('ncaieee_ext/' + infile_name + '_gr_b.png', root_dir='ncaieee_rgb_games')

    # read already split images
    n_colors = 128
    in_file_name = 'ncaieee_rgb_games/' + infile_name + '_gr_r' + f'_gs_{n_colors}c_noinc.png'
    img_r = cv2.imread(in_file_name)
    in_file_name = 'ncaieee_rgb_games/' + infile_name + '_gr_g' + f'_gs_{n_colors}c_noinc.png'
    img_g = cv2.imread(in_file_name)
    in_file_name = 'ncaieee_rgb_games/' + infile_name + '_gr_b' + f'_gs_{n_colors}c_noinc.png'
    img_b = cv2.imread(in_file_name)

    # Create a new image with only the blue channel
#    rgb_image_in = cv2.imread(infile)
#    rgb_image_out = np.zeros_like(rgb_image_in)
    rgb_image_out = np.zeros_like(img_r)
    rgb_image_out[:, :, 0] = img_b[:, :, 0]
    rgb_image_out[:, :, 1] = img_g[:, :, 1]
    rgb_image_out[:, :, 2] = img_r[:, :, 2]

    # Save or work with the individual channels as needed
    cv2.imwrite('ncaieee_rgb_games/' + infile_name + f'_combined_{n_colors}_noinc.png', rgb_image_out)

    #cv2.imwrite(infile_name + '_c_r.png', out_img_r)
    #cv2.imwrite(infile_name + '_c_g.png', out_img_g)
    #cv2.imwrite(infile_name + '_c_b.png', out_img_b)
    # Extract the R, G, and B channels
    #img_b = img_rgb[:, :, 0]
    #img_g = img_rgb[:, :, 1]
    #img_r = img_rgb[:, :, 2]

    # Create a new image with only the blue channel
    #out_img_r = np.zeros_like(image)
    #out_img_g = np.zeros_like(image)
    #out_img_b = np.zeros_like(image)
#    out_img_r[:, :, 0] = img_r
#    out_img_g[:, :, 1] = img_g
#    out_img_b[:, :, 2] = img_b
    # out_img_b[:, :, 0] = img_rgb[:, :, 0]
    # out_img_g[:, :, 1] = img_rgb[:, :, 1]
    # out_img_r[:, :, 2] = img_rgb[:, :, 2]
    return

# print_orig_and_unary_pixels - Run on the original image and print coordinates, original pixel value, unary label value from the steps_ranges list
# run on 3 color files
def print_unary_pixels_rgb(infile, search_range = (200, 255)):
    print('print_orig_and_unary_pixels')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem
    print(f'print_orig_and_unary_pixels: read input image: {infile}')
    print(f'print_orig_and_unary_pixels: search_ranges: {search_range}')
    # Convert to grayscale
    rgb_grey_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)


    width = rgb_grey_image.shape[0]
    height = rgb_grey_image.shape[1]
#    steps_ranges = [2,4,8,16,32,64,128]
#    steps_ranges = [64,128]
#    range_size = 32
#    n_colors = 256//range_size
    # Cycle through pixels
    # for x in range(0, int(width)):
    #     for y in range(0, int(height)):
    #         if search_range[0] <= rgb_gray_image[x, y] <= search_range[1] and \
    #             search_range[0] <= rgb_gray_image[x, y] <= search_range[1] and \
    #             search_range[0] <= rgb_gray_image[x, y] <= search_range[1]:
    #             # in_range = True
    #             found_pixel_count += 1
    #             print(f'XY{x,y}: RGB{rgb_gray_image[x, y], rgb_gray_image[x, y], rgb_gray_image[x, y]}')
#                        print(f'XY{x,y}: RGB{r_gray_image[x, y], g_gray_image[x, y], b_gray_image[x, y]} -> start, end:{start, end}')
    rgb_pixels = {}
    # for x in range(0, int(width)):
    #     for y in range(0, int(height)):
    #         if str(rgb_image[x, y]) in rgb_pixels:
    #             rgb_pixels[str(rgb_image[x, y])] += 1
    #         else:
    #             rgb_pixels[str(rgb_image[x, y])] = 1
    # print(f'rgb_pixels: {rgb_pixels}')
    for x in range(0, search_range[0], 4):
        for y in range(0, search_range[1], 4):
                #print(f'XY{x,y}: RGB_grey{rgb_grey_image[x, y], rgb_grey_image[x, y], rgb_grey_image[x, y]}')
                # if (rgb_image[x, y,0] > 0 and rgb_image[x, y,0] < 255) or\
                #       (rgb_image[x, y,1] > 0 and rgb_image[x, y,1] < 255) or\
                #           (rgb_image[x, y,2] > 0 and rgb_image[x, y,2] < 255):
                    print(f'XY{x,y}: RGB{str(rgb_image[x, y]),str(rgb_image[x, y+1]),str(rgb_image[x, y+2]),str(rgb_image[x, y+3])}')
                    print(f'XY{x+1,y}: RGB{str(rgb_image[x+1, y]),str(rgb_image[x+1, y+1]),str(rgb_image[x+1, y+2]),str(rgb_image[x+1, y+3])}')
                    print(f'XY{x+2,y}: RGB{str(rgb_image[x+2, y]),str(rgb_image[x+2, y+1]),str(rgb_image[x+2, y+2]),str(rgb_image[x+2, y+3])}')
                    print(f'XY{x+3,y}: RGB{str(rgb_image[x+3, y]),str(rgb_image[x+3, y+1]),str(rgb_image[x+3, y+2]),str(rgb_image[x+3, y+3])}')
                    print('\n')
#                    print(f'XY{x,y}: RGB{rgb_image[x, y,0], rgb_image[x, y,1], rgb_image[x, y,2]}')

        # Save the grayscale image
        # out_file_name = root_dir + '/' + infile_name + f'_gs_{n_colors}c_noinc.png'
        # print(f'save image: {out_file_name}')
        # cv2.imwrite(out_file_name, gray_image)
    #print(f'found_pixel_count: {found_pixel_count}')


# randomize_unary_pixels_rgb - Run on the original image and randomize the original pixels layout
def randomize_unary_pixels_rgb2(infile, step = 4, search_range = (200, 255), root_dir='ncaieee_ext'):
    print('print_orig_and_unary_pixels')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem
    print(f'randomize_unary_pixels_rgb: read input image: {infile}')
    print(f'randomize_unary_pixels_rgb: search_ranges: {search_range}')
    # Convert to grayscale
    #rgb_grey_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

    # Save or work with the individual channels as needed
#    cv2.imwrite('ncaieee_rgb_games/' + infile_name + f'_combined_{step}c_inc_rand.png', rgb_image_out)

    rgb_image_out = np.zeros_like(rgb_image)
    width = 16
    height = 16
    rgb_image_out[:, :, :] = rgb_image[:, :, :]
    for x in range(0, width, step):
        for y in range(0, height, step):
            # Randomize pixels in the unary box - independently for every color
            # Generate random indices for x and y
            random_x = np.random.permutation(step) + x
            random_y = np.random.permutation(step) + y
            # random_x = x
            # random_y = y

            # Swap the pixels in rgb_image and rgb_image_out
#            rgb_image_out[random_x, random_y, :] = rgb_image[x, y, :]
            # Working copy
            # rgb_image_out[x:x+step, y:y+step, :] = rgb_image[x:x+step, y:y+step, :]
            seq_count = 0
            for ii in range(step):
                for jj in range(step):
                    # Generate random indices within the step for swapping
                    rand_x = np.random.randint(x+ii, min(x + step, width))
                    rand_y = np.random.randint(y+jj, min(y + step, height))
                    print(f'rand_x: {rand_x}, rand_y: {rand_y}')
                    # Swap values between rgb_image and rgb_image_out at random indices
                    print(f'Before: XY{x+ii, y+jj}: RGB{str(rgb_image_out[x+ii, y+jj,:]),str(rgb_image_out[rand_x, rand_y,:])}')
#                    rgb_image_out[x+ii, y+jj,:], rgb_image_out[rand_x, rand_y,:] = (rgb_image_out[rand_x, rand_y,:], rgb_image_out[x+ii, y+jj,:]
                    temp = (rgb_image_out[x+ii, y+jj,:]).copy()
                    rgb_image_out[x+ii, y+jj,:] = rgb_image_out[rand_x, rand_y,:]
                    rgb_image_out[rand_x, rand_y,:] = temp
                    print(f'After: XY{x+ii, y+jj}: RGB{str(rgb_image_out[x+ii, y+jj,:]),str(rgb_image_out[rand_x, rand_y,:])}')

                    #rgb_image_out[ii, jj, :] = rgb_image[seq_count, seq_count, :]
                    #seq_count = +1
            # print(f'random_x: {random_x}, random_y: {random_y}')
            # print(f' shape rgb_image: {rgb_image[x:x+step, y:y+step, :].shape}, shape rgb_image_out_dif_col: {rgb_image_out[random_x, random_y, :].shape}')
            # rgb_image_out[random_x, random_y, :] = rgb_image[x:x+step, y:y+step, :]
            # if not np.array_equal(rgb_image[x, y, :], [0, 0, 0]):
            #     print(f'XY{x,y}: RGB{str(rgb_image_out[x, y,:]),str(rgb_image[x, y,:])}')


#            print(f'XY{x,y}: RGB{str(rgb_image_out[x, y,:]),str(rgb_image[x, y,:])}')

def randomize_unary_pixels_rgb_rand(infile, step = 4, search_range = (200, 255), root_dir='ncaieee_ext'):
    print('randomize_unary_pixels_rgb_rand')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem
    print(f'randomize_unary_pixels_rgb_rand: read input image: {infile}')
    print(f'randomize_unary_pixels_rgb_rand: search_ranges: {search_range}')

    rgb_image_out = np.zeros_like(rgb_image)
    width = rgb_image_out.shape[0]
    height = rgb_image_out.shape[1]
    rgb_image_out[:, :, :] = rgb_image[:, :, :]
    for x in range(0, width, step):
        for y in range(0, height, step):
            for ii in range(step):
                for jj in range(step):
                    # Generate random indices within the step for swapping
                    rand_x = np.random.randint(x+ii, min(x + step, width))
                    rand_y = np.random.randint(y+jj, min(y + step, height))
#                    print(f'rand_x: {rand_x}, rand_y: {rand_y}')
                    # Swap values between rgb_image and rgb_image_out at random indices
#                    print(f'Before: XY{x+ii, y+jj}: RGB{str(rgb_image_out[x+ii, y+jj,:]),str(rgb_image_out[rand_x, rand_y,:])}')
                    temp = (rgb_image_out[x+ii, y+jj,:]).copy()
                    rgb_image_out[x+ii, y+jj,:] = rgb_image_out[rand_x, rand_y,:]
                    rgb_image_out[rand_x, rand_y,:] = temp
#                    print(f'After: XY{x+ii, y+jj}: RGB{str(rgb_image_out[x+ii, y+jj,:]),str(rgb_image_out[rand_x, rand_y,:])}')

            # Working copy
#            rgb_image_out[x:x+step, y:y+step, :] = rgb_image[x:x+step, y:y+step, :]

    # Save the new image
    out_file_name = root_dir + '/' + infile_name + f'_combined_{step}c_inc_rand.png'
    print(f'save image: {out_file_name}')
    cv2.imwrite(out_file_name, rgb_image_out)


    # print pixels in search_range
    for x in range(0, search_range[0], step):
        for y in range(0, search_range[1], step):
            print(f'XY{x,y}: RGB{str(rgb_image_out[x, y]),str(rgb_image_out[x, y+1]),str(rgb_image_out[x, y+2]),str(rgb_image_out[x, y+3])}')
            print(f'XY{x+1,y}: RGB{str(rgb_image_out[x+1, y]),str(rgb_image_out[x+1, y+1]),str(rgb_image_out[x+1, y+2]),str(rgb_image_out[x+1, y+3])}')
            print(f'XY{x+2,y}: RGB{str(rgb_image_out[x+2, y]),str(rgb_image_out[x+2, y+1]),str(rgb_image_out[x+2, y+2]),str(rgb_image_out[x+2, y+3])}')
            print(f'XY{x+3,y}: RGB{str(rgb_image_out[x+3, y]),str(rgb_image_out[x+3, y+1]),str(rgb_image_out[x+3, y+2]),str(rgb_image_out[x+3, y+3])}')
            print('\n')
#                    print(f'XY{x,y}: RGB{rgb_image[x, y,0], rgb_image[x, y,1], rgb_image[x, y,2]}')


def randomize_unary_pixels_rgb_rand_dif_col(infile, step = 4, search_range = (200, 255), root_dir='ncaieee_ext'):
    print('randomize_unary_pixels_rgb_rand_dif_col')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem
    print(f'randomize_unary_pixels_rgb_rand_dif_col: read input image: {infile}')
    print(f'randomize_unary_pixels_rgb_rand_dif_col: search_ranges: {search_range}')

    rgb_image_out_dif_col = np.zeros_like(rgb_image)
    width = rgb_image_out_dif_col.shape[0]
    height = rgb_image_out_dif_col.shape[1]
    rgb_image_out_dif_col[:, :, :] = rgb_image[:, :, :]
    for x in range(0, width, step):
        for y in range(0, height, step):
            # Randomize pixels in the unary box - independently for every color
            # Generate random indices for x and y
            for ii in range(step):
                for jj in range(step):
                    # Generate random indices within the step for swapping
                    rand_x = np.random.randint(x+ii, min(x + step, width))
                    rand_y = np.random.randint(y+jj, min(y + step, height))
#                    print(f'rand_x: {rand_x}, rand_y: {rand_y}')
                    # Swap values between rgb_image and rgb_image_out at random indices
#                    print(f'Before: XY{x+ii, y+jj}: RGB{str(rgb_image_out[x+ii, y+jj,:]),str(rgb_image_out[rand_x, rand_y,:])}')
#                    rgb_image_out[x+ii, y+jj,:], rgb_image_out[rand_x, rand_y,:] = (rgb_image_out[rand_x, rand_y,:], rgb_image_out[x+ii, y+jj,:]
                    for z in range(3):
                        # random_x = np.random.permutation(step) + x
                        # random_y = np.random.permutation(step) + y
                        random_x = x
                        random_y = y
                        rand_x = np.random.randint(x+ii, min(x + step, width))
                        rand_y = np.random.randint(y+jj, min(y + step, height))
                        # Swap the pixels in rgb_image and rgb_image_out
                        # print(f'shape rgb_image_out_dif_col: {rgb_image_out_dif_col[random_x, random_y, i]}, shape rgb_image: {rgb_image[x:x+step, y:y+step, i]}')
                        temp = (rgb_image_out_dif_col[x+ii, y+jj,z]).copy()
                        rgb_image_out_dif_col[x+ii, y+jj,z] = rgb_image_out_dif_col[rand_x, rand_y,z]
                        rgb_image_out_dif_col[rand_x, rand_y,z] = temp

        #                rgb_image_out[x:x+step, y:y+step, i] = rgb_image[x:x+step, y:y+step, i]
#                        rgb_image_out_dif_col[random_x, random_y, i] = rgb_image[x, y, i]

    # Save the new image
    out_file_name = root_dir + '/' + infile_name + f'_combined_{step}c_inc_rand_dif_col.png'
    print(f'save image: {out_file_name}')
    cv2.imwrite(out_file_name, rgb_image_out_dif_col)

    # print pixels in search_range
    for x in range(0, search_range[0], step):
        for y in range(0, search_range[1], step):
            print(f'XY{x,y}: RGB{str(rgb_image_out_dif_col[x, y]),str(rgb_image_out_dif_col[x, y+1]),str(rgb_image_out_dif_col[x, y+2]),str(rgb_image_out_dif_col[x, y+3])}')
            print(f'XY{x+1,y}: RGB{str(rgb_image_out_dif_col[x+1, y]),str(rgb_image_out_dif_col[x+1, y+1]),str(rgb_image_out_dif_col[x+1, y+2]),str(rgb_image_out_dif_col[x+1, y+3])}')
            print(f'XY{x+2,y}: RGB{str(rgb_image_out_dif_col[x+2, y]),str(rgb_image_out_dif_col[x+2, y+1]),str(rgb_image_out_dif_col[x+2, y+2]),str(rgb_image_out_dif_col[x+2, y+3])}')
            print(f'XY{x+3,y}: RGB{str(rgb_image_out_dif_col[x+3, y]),str(rgb_image_out_dif_col[x+3, y+1]),str(rgb_image_out_dif_col[x+3, y+2]),str(rgb_image_out_dif_col[x+3, y+3])}')
            print('\n')
#                    print(f'XY{x,y}: RGB{rgb_image[x, y,0], rgb_image[x, y,1], rgb_image[x, y,2]}')

    #print(f'found_pixel_count: {found_pixel_count}')

if __name__ == '__main__':
    infile = './Images/Lenna.png'
    """
    parse the arguments and parse the topology file
    """
    parser = argparse.ArgumentParser(prog='PROG', description='Images manipulation utility')
#    parser.add_argument('-i', dest='i', help='The input image', required=True, default=False)
    parser.add_argument('-i', dest='i', help='The input image', default=infile)
    args = parser.parse_args()

    infile = str(args.i)
    if not os.path.isfile(infile):
        print("File {} does not exist.".format(infile))
        exit()

    # create_single_rgb_slide(infile,'r')
    # create_single_rgb_slide(infile,'b')
    # create_single_rgb_slide(infile,'g')

    # recover_image(infile)
    # create_gs_image(infile)
    
    # step_ranges = create_ranges(256, 32)
    # print(f'step_ranges:{step_ranges}')
    # # Create unary labels for the selected ranges
    # labels = create_unary_labels(len(step_ranges))
    # # Print the selected ranges and their unary labels
    # for i in range(256//32):
    #     print(f"Range: {step_ranges[i]}, Label: {labels[i]}")

    #add_random_noise_img(infile)
    # create_unary_images(infile)

#    create_unary_images(infile)

#    ncaieee_rgb_games(infile)

#    ves_games(infile)

    # 31.10.2023
#    infile = './Lenna_combined_16.png'
#    print_unary_pixels_rgb(infile, search_range = (200, 255))


    # 03.11.2023
    # infile = './Lenna_combined_64.png'
    # #randomize_unary_pixels_rgb_rand(infile, step = 4, search_range = (16, 16), root_dir='ncaieee_ext')
    # randomize_unary_pixels_rgb_rand_dif_col(infile, step = 8, search_range = (4, 4), root_dir='ncaieee_ext')

    # 03.06.2024
    root_dir = './2024'
    infile = './2024/Mandrill512X512X24.tiff'
    #infile = './2024/Mandrill512X512X24_gr_b.png'
    create_gs_image(infile, root_dir='./2024')
    infile_name = Path(infile).stem
    infile_name_bw = root_dir + '/' + infile_name + 'bw.png'

    create_gby_image(infile_name_bw, root_dir='./2024')
    #create_single_rgb_slide(infile,'r', root_dir='./2024')
    #create_single_rgb_slide(infile,'b', root_dir='./2024')
    #create_single_rgb_slide(infile,'g', root_dir='./2024')

    # recover_image(infile)
    # create_gs_image(infile)

    # print_orig_and_unary_pixels - Run on the original image and print coordinates, original pixel value, unary label value from the steps_ranges list
    # run on 3 color files
    # default parameters: search_range = (200, 255), steps_ranges = [4,64]):
#     infile_name = Path(infile).stem
#     r_infile = 'ncaieee_ext/' + infile_name + '_gr_r.png'
#     g_infile = 'ncaieee_ext/' + infile_name + '_gr_g.png'
#     b_infile = 'ncaieee_ext/' + infile_name + '_gr_b.png'
#     search_range = (220, 255)
# #    search_range = (0, 60)
#     print_orig_and_unary_pixels(r_infile, g_infile, b_infile, search_range, steps_ranges = [64])
    #create_rgb_slide(infile)
#    create_gby_image(infile)
#    create_gby_slide(infile)
#    main()
