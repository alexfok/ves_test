# TODO 22.05.2024
run alg1 with image:    ./2025/Images/Mandrill512X512X24bw_BW.png
1. encode image
    save slides in ./2025/slides/
    save results in ./2025/out_images/
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png -c ./2025/Images/Mandrill512X512X24bw_BW.png -enc
2. extend encryption algorithm to support more than 2 slides
3. Analyze and collect images statistics
4. Define and implement Byzantine actions
5. Run Byzantine on created slides and decode image
6. Analyze and collect images statistics
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png -enc --nslides 2 --comp1
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png -enc --nslides 21 --comp1 --b_num 5 --b_pixels 250144
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png -enc --nslides 21 --comp1 --b_num 0,1,2,3,4,5 --b_pixels 262144
# Encrypt and run Byzantine affected recovery
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png -enc --nslides 21 --comp1 --b_num 0,1,2,3,4,5 --b_pixels 20000 --m 4 --k 2 --rand
# run Byzantine affected recovery
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png --nslides 21 --comp1 --b_num 0,1,2,3,4,5 --b_pixels 20000 --m 4 --k 2 --rand

#
Original Image: total=262144, black=124158 (47.36%), white=137986 (52.64%)

# Plot Byzantine recovery with --b_pixels 20000
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png --plot_results
    x_values: ['0', '1', '2', '3', '4', '5'] x_values lenght: 6
    y_values: [1.0, 0.9242894206658646, 0.8538329975504761, 0.7887176959981448, 0.727697012740423, 0.6722928413027408] y_values lenght: 6
    results: [(0, 20000, 1.0), (1, 20000, 0.9242894206658646), (2, 20000, 0.8538329975504761), (3, 20000, 0.7887176959981448), (4, 20000, 0.727697012740423), (5, 20000, 0.6722928413027408)] results lenght: 6

# Byzantine recovery with --b_pixels 40000 + plot
python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png --nslides 21 --comp1 --b_num 0,1,2,3,4,5 --b_pixels 40000 --m 4 --k 2 --rand
    x_values: ['0', '1', '2', '3', '4', '5'] x_values lenght: 6
    y_values: [1.0, 0.8480280608177642, 0.7191091849897816, 0.6098299827518734, 0.5172191381734379, 0.43683417158262433] y_values lenght: 6
    results: [(0, 40000, 1.0), (1, 40000, 0.8480280608177642), (2, 40000, 0.7191091849897816), (3, 40000, 0.6098299827518734), (4, 40000, 0.5172191381734379), (5, 40000, 0.43683417158262433)] results lenght: 6


python alg1.py -t ./2025/Images/Mandrill512X512X24bw_BW.png --nslides 21 --comp1 --b_num 0,1,2,3,4,5 --b_pixels 80000 --m 4 --k 2 --rand
    x_values: ['0', '1', '2', '3', '4', '5'] x_values lenght: 6
    y_values: [1.0, 0.6953893873291493, 0.48351282014117375, 0.3334541185337643, 0.23503109011059092, 0.16253098140391053] y_values lenght: 6
    results: [(0, 80000, 1.0), (1, 80000, 0.6953893873291493), (2, 80000, 0.48351282014117375), (3, 80000, 0.3334541185337643), (4, 80000, 0.23503109011059092), (5, 80000, 0.16253098140391053)] results lenght: 6

print_orig_and_unary_pixels: search_ranges: (220, 255), steps_ranges: [64]
range_size: 64
XY(272, 117): RGB(251, 245, 224) -> 255
found_pixel_count: 1

print_orig_and_unary_pixels: search_ranges: (0, 60), steps_ranges: [64]
range_size: 64
XY(71, 508): RGB(59, 4, 43) -> 63
XY(185, 281): RGB(59, 12, 59) -> 63
XY(189, 275): RGB(60, 8, 60) -> 63
XY(191, 274): RGB(59, 9, 59) -> 63
XY(197, 265): RGB(56, 4, 60) -> 63
XY(198, 264): RGB(59, 3, 55) -> 63
XY(198, 266): RGB(59, 14, 60) -> 63
XY(329, 155): RGB(60, 6, 53) -> 63
XY(344, 147): RGB(60, 11, 54) -> 63
XY(433, 183): RGB(59, 7, 58) -> 63
XY(498, 142): RGB(59, 10, 59) -> 63
found_pixel_count: 11

# python ncaieee_ext.py -i ./Images/Lenna.png
create_unary_images
create_unary_labels: n_labels: 16
range_size: 16, scale_factor: (4, 4), n_colors: 16, Labels[0]: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]  
width: 2048, height: 2048
save image: ncaieee_ext/Lenna_gs_16c_inc.png

# ves_test
# Usage:
C:/Users/afok/AppData/Local/Programs/Python/Python39/python.exe "c:/Work/Private/BGU/Thesis/Thesis Code/alg1.py" -t Lenna.png -c LennaBWOrig.jpeg
# Match 2 identical images
python alg1.py -t Images/LennaBWOrig.jpeg -c Images/LennaBWOrig.jpeg -enc
<!-- compare images result image: Images/LennaBWOrig.jpeg, Positive cimage: ncaieee_ext/LennaBWOrig_R_P.png, match_pixel_count: 114451, mismatch_pixel_count: 0, total_pixels: 262144, match percentage: 43.66%
compare images result image: Images/LennaBWOrig.jpeg, Negative cimage: ncaieee_ext/LennaBWOrig_R_N.png, match_pixel_count: 147693, mismatch_pixel_count: 0, total_pixels: 262144, match percentage: 56.34%
recover and compare images Done. -->
# Match original image with black square
python alg1.py -t Images/LennaBWOrig.jpeg -c Images/LennaBWOrig_bs.jpg -enc
python.exe alg1.py --help

# ncaieee_ext/Lenna_gs_16c.png
# python alg1.py -t ncaieee_ext/Lenna_gs_16c.png -c ncaieee_ext/Lenna_gs_16c.png -enc
compare images result image: ncaieee_ext/Lenna_gs_16c.png, Positive cimage: ncaieee_ext/Lenna_gs_16c_R_P.png, match_pixel_count: 135246, mismatch_pixel_count: 0, total_pixels: 262144, match percentage: 51.59%
compare images result image: ncaieee_ext/Lenna_gs_16c.png, Negative cimage: ncaieee_ext/Lenna_gs_16c_R_N.png, match_pixel_count: 126898, mismatch_pixel_count: 0, total_pixels: 262144, match percentage: 48.41%

# python alg1.py -t ncaieee_ext/Lenna_gs_64c.png -c ncaieee_ext/Lenna_gs_64c.png -enc
compare images result image: ncaieee_ext/Lenna_gs_64c.png, Positive cimage: ncaieee_ext/Lenna_gs_64c_R_P.png, match_pixel_count: 129035, mismatch_pixel_count: 0, total_pixels: 262144, match percentage: 49.22%
compare images result image: ncaieee_ext/Lenna_gs_64c.png, Negative cimage: ncaieee_ext/Lenna_gs_64c_R_N.png, match_pixel_count: 133109, mismatch_pixel_count: 0, total_pixels: 262144, match percentage: 50.78%

# python alg1.py -t ncaieee_ext/Lenna_gs_16c_inc.png -c ncaieee_ext/Lenna_gs_16c_inc.png -enc
compare images result image: ncaieee_ext/Lenna_gs_16c_inc.png, Positive cimage: ncaieee_ext/Lenna_gs_16c_inc_R_P.png, match_pixel_count: 2171800, mismatch_pixel_count: 0, total_pixels: 4194304, match percentage: 51.78%        
compare images result image: ncaieee_ext/Lenna_gs_16c_inc.png, Negative cimage: ncaieee_ext/Lenna_gs_16c_inc_R_N.png, match_pixel_count: 2022504, mismatch_pixel_count: 0, total_pixels: 4194304, match percentage: 48.22%        

# python alg1.py -t ncaieee_ext/Lenna_gs_16c_inc.png -c ncaieee_ext/LennaBWOrig_bs_gs_16c_inc.png -enc
compare images result image: ncaieee_ext/LennaBWOrig_bs_gs_16c_inc_R_P.png, match_pixel_count: 1381285, mismatch_pixel_count: 0, total_pixels: 4194304, match percentage: 32.93%
compare images result image: ncaieee_ext/Lenna_gs_16c_inc.png, Negative cimage: ncaieee_ext/LennaBWOrig_bs_gs_16c_inc_R_N.png, match_pixel_count: 1467975, mismatch_pixel_count: 0, total_pixels: 4194304, match percentage: 35.00%       

# out_images
The test folders. The following naming convention used:

{image_name}_bw.png - Original image {image_name} (Lenna_bw.png)

{image_name}_slideA.png - VES slide A

{image_name}_slideB.png - VES slide B

{image_name}_bw_C.png - image used for comparison (C)

{image_name}_slideA_P.png - VES slide A AND C

{image_name}_slideA_N.png - VES slide A AND NOT(C)

{image_name}_slideB_P.png - VES slide B AND C

{image_name}_slideB_N.png - VES slide B AND NOT(C)


# Folder Test1_Rect
LennaBW1_bw_C.png used for comparison - Black rectangle with white rectangle in the middle
# Folder Test2_LennaOrigBlack
LennaBW_bw_C.png used for comparison - original Lenna image black\white with addition of black areas
# Folder Test3_LennaOrig
LennaBWOrig_bw_C.png used for comparison - original Lenna image black\white

timage_pixel_xy: 255, cimage_pixel_xy: 0
pixels_xy: 0, pixels_x1y:0, pixels_xy1: 0, pixels_x1y1: 0

timage_pixel_xy: 0, cimage_pixel_xy: 0
pixels_xy: 0, pixels_x1y:0, pixels_xy1: 0, pixels_x1y1: 0

timage_pixel_xy: 0, cimage_pixel_xy: 0
pixels_xy: 255, pixels_x1y:0, pixels_xy1: 255, pixels_x1y1: 0

timage_pixel_xy: 0, cimage_pixel_xy: 0
pixels_xy: 255, pixels_x1y:0, pixels_xy1: 255, pixels_x1y1: 0

timage_pixel_xy: 255, cimage_pixel_xy: 0
pixels_xy: 255, pixels_x1y:255, pixels_xy1: 0, pixels_x1y1: 0

timage_pixel_xy: 255, cimage_pixel_xy: 255
pixels_xy: 0, pixels_x1y:0, pixels_xy1: 0, pixels_x1y1: 0

timage_pixel_xy: 0, cimage_pixel_xy: 255
pixels_xy: 0, pixels_x1y:0, pixels_xy1: 255, pixels_x1y1: 255
