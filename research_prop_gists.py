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

def plot_waves(x, y1, y2, y3, delta_x, yc_color = 'b', destruct = False):
    # Plot the sine waves
    y1_color = 'b'
    y2_color = 'y'
    y3_color = 'g'
    plt.title("Waves Destructive Interference")
    #constructive interference
    if not destruct:
        plt.title("Waves Constructive Interference")
        y1_color = yc_color
        y2_color = yc_color
        y3_color = yc_color
        #y3 = np.linspace(1,1,100)
        plt.plot(x + delta_x, y1, y1_color, label='Wave 1')
        plt.plot(x + delta_x, y2, y2_color, label='Wave 2')
        plt.plot(x + delta_x, y3, y3_color, label='Resulting wave')
    else:
        plt.plot(x, y1, y1_color, label='Wave 1')
        plt.plot(x + delta_x, y2, y2_color, label='Wave 2')
        plt.plot(x, y3, y3_color, label='Resulting wave')

    # Add labels and a legend
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    #plt.tight_layout() 
    #plt.xlabel('X')
    #plt.ylabel('Y')
    plt.legend()

    # Show the plot
    plt.show()

def main():
    # Create an array of x values from 0 to 4*pi
    x = np.linspace(0, 4*np.pi, 100)

    # Compute the y values for two sine waves with a phase difference of 2*pi
    y1 = np.sin(x)

    # Compute the y values for the constructive interference
    y2 = np.sin(x + 2*np.pi) + 1
    y3 = y1 + y2
    plot_waves(x, y1, y2, y3,0)
    plot_waves(x, y1, y2, y3,np.pi, yc_color='y')
    # Compute the y values for the destructive interference
    y2 = np.sin(x + 2*np.pi)
    y22 = np.sin(x + np.pi)
    y4 = y1 + y22
    plot_waves(x, y1, y2, y4, np.pi, destruct = True)



    # Show the plot
    plt.show()

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
    cv2.imwrite('ncaieee/' + infile_name + '_shifted.png', gray_image)
    cv2.imwrite('ncaieee/' + infile_name + '_gs_8c.png', gray_image2)

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

if __name__ == '__main__':
    infile = './Images/Lenna.png'
    # create_single_rgb_slide(infile,'r')
    # create_single_rgb_slide(infile,'b')
    # create_single_rgb_slide(infile,'g')

    # recover_image(infile)
    # create_gs_image(infile)

    ves_games(infile)

    #create_rgb_slide(infile)
#    create_gby_image(infile)
#    create_gby_slide(infile)
#    main()
'''
# Create an array of x values from 0 to 4*pi
x = np.linspace(0, 4*np.pi, 100)

# Compute the y values for two sine waves with opposite phases
y1 = np.sin(x)
y2 = np.sin(x + np.pi)

# Plot the sine waves
plt.plot(x, y1, 'b-', label='Sine Wave 1')
plt.plot(x, y2, 'r-', label='Sine Wave 2')

# Add labels and a legend
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.tight_layout() 
#plt.xlabel('X')
#plt.ylabel('Y')
plt.legend()

# Show the plot
plt.show()
#This code creates an array of x values from 0 to 4*pi, computes the y values for two sine waves with opposite phases, plots the two sine waves on the same graph, and displays the graph. The b- and r- options in the plot() function specify the color and line style of the two sine waves, respectively. The legend() function adds a legend to the graph and the xlabel() and ylabel() function adds x and y axis labels to the graph.
'''




'''
x=np.arange(0,3*np.pi,0.1)
y=np.sin(x)
plt.plot(x,y)
plt.title("SINE WAVE")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.tight_layout() 
plt.show()

sample_rate = 200 # sampling frequency in Hz (atleast 2 times f)
t = np.linspace(0,5,sample_rate)    #time axis
#print(f't: {t}')
f = 100 #Signal frequency in Hz
sig = np.sin(2*np.pi*f*(t/sample_rate))
t2 = np.linspace(0.5,5.5,sample_rate)    #time axis
print(f't2: {t2}')
sig2 = np.sin(2*np.pi*f*(t2/sample_rate))
plt.plot(t,sig)
plt.plot(t2,sig2)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.tight_layout() 
plt.show()
'''
