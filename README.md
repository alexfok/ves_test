# ves_test
# How to run:
C:/Users/afok/AppData/Local/Programs/Python/Python39/python.exe "c:/Work/Private/BGU/Thesis/Thesis Code/visual_cryptography_py3.py" -t Lenna.png -c LennaBWOrig.jpeg
python.exe visual_cryptography_py3.py

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