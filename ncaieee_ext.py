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

def create_gby_image(infile):
    ############################
    # Candidate image preparation
    img = Image.open(infile)
    img = img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
#    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))

    infile_name = Path(infile).stem
#    infile_img_n = Image.new('1', img.size)
    outfile = infile_name + '_BWVES.png'

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

    img2.save(outfile, 'PNG')
#    printImage(outfile)
    return


################################
# RGB slides games
def create_rgb_slide(infile):
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
    cv2.imwrite(infile_name + '_gr_r.png', img_r)
    cv2.imwrite(infile_name + '_gr_g.png', img_g)
    cv2.imwrite(infile_name + '_gr_b.png', img_b)
    cv2.imwrite(infile_name + '_c_r.png', out_img_r)
    cv2.imwrite(infile_name + '_c_g.png', out_img_g)
    cv2.imwrite(infile_name + '_c_b.png', out_img_b)

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

    cv2.imwrite(infile_name + '_slide_b.png', out_img_b2)
    cv2.imwrite(infile_name + '_slide_g.png', out_img_g2)
    cv2.imwrite(infile_name + '_slide_r.png', out_img_r2)
    #img2.save(outfile, 'PNG')
#    printImage(outfile)
    return

def create_single_rgb_slide(infile, color):
    ############################
    # Candidate image preparation
    #img = Image.open(infile)
#    img = img.convert('1')  # convert image to 1 bit
#    infile_img.save(cimg_filename_bw, 'PNG')
#    print("save_negative_image: Candidate Image size: {}".format(infile_img.size))
    print('create_single_rgb_slide')
    infile_name = Path(infile).stem
    infile_name = 'ncaieee/' + infile_name
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
    cv2.imwrite(infile_name + f'_gr_{color}.png', out_img_gr)
    cv2.imwrite(infile_name + f'_c_{color}.png', out_img_c)

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

def create_gs_image(infile):
    print('create_gs_image')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem
    infile_name = 'ncaieee/' + infile_name + 'gl.png'

    # Convert to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv2.imwrite(infile_name, gray_image)

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

def create_unary_images(infile):
    print('create_unary_images')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem

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
        print(step_ranges)
        n_colors = 256//range_size
        labels = create_unary_labels(len(step_ranges))
        print(f"range_size: {range_size}, Label: {labels[0]}")

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
        out_file_name = 'ncaieee_ext/' + infile_name + f'_gs_{n_colors}c.png'
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
    
def create_unary_images(infile):
    print('create_unary_images')
    # Load the RGB image
    rgb_image = cv2.imread(infile)
    infile_name = Path(infile).stem

    # Convert to grayscale
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    width = gray_image.shape[0]
    height = gray_image.shape[1]
#    steps_ranges = [2,4,8,16,32,64,128]
#    scale_factors = [(8,16),(8,8),(4,8),(4,4),(2,4),(2,2),(1,2)]
    steps_ranges = [16]
    scale_factors = [(4,4)]

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
        out_file_name = 'ncaieee_ext/' + infile_name + f'_gs_{n_colors}c_inc.png'
        print(f'save image: {out_file_name}')
        cv2.imwrite(out_file_name, out_img)

if __name__ == '__main__':
    infile = './Images/Lenna.png'
    """
    parse the arguments and parse the topology file
    """
    parser = argparse.ArgumentParser(prog='PROG', description='Images manipulation utility')
    parser.add_argument('-i', dest='i', help='The input image', required=True, default=False)
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
    create_unary_images(infile)

#    ves_games(infile)

    #create_rgb_slide(infile)
#    create_gby_image(infile)
#    create_gby_slide(infile)
#    main()
