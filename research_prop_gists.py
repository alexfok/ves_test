import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os
import sys
from random import SystemRandom
import argparse
from pathlib import Path
import random

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
#    infile = './Images/LennaBWOrig.jpeg'
#    create_gby_image(infile)
#    create_gby_slide(infile)
    main()
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
