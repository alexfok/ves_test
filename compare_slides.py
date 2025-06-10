import os
from PIL import Image
import numpy as np

def compare_images(img1_path, img2_path):
    """Compare two images and return match statistics"""
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    
    # Convert to numpy arrays for faster comparison
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    total_pixels = arr1.size
    matching_pixels = np.sum(arr1 == arr2)
    match_percentage = (matching_pixels / total_pixels) * 100
    
    return total_pixels, matching_pixels, match_percentage

def analyze_image_pixels(img):
    """Analyze black and white pixels in an image"""
    arr = np.array(img)
    total_pixels = arr.size
    black_pixels = np.sum(arr == 0)
    white_pixels = np.sum(arr == 255)
    
    return {
        'total': total_pixels,
        'black': black_pixels,
        'white': white_pixels,
        'black_percent': (black_pixels / total_pixels) * 100,
        'white_percent': (white_pixels / total_pixels) * 100
    }

def compare_original_recovered(original_image, recovered_image):
    """Compare original and recovered images with detailed pixel analysis"""
    orig_img = Image.open(original_image)
    rec_img = Image.open(recovered_image)
    
    orig_stats = analyze_image_pixels(orig_img)
    rec_stats = analyze_image_pixels(rec_img)
    
    print(f"\nOriginal Image Analysis:")
    print(f"Total pixels: {orig_stats['total']}")
    print(f"Black pixels: {orig_stats['black']} ({orig_stats['black_percent']:.2f}%)")
    print(f"White pixels: {orig_stats['white']} ({orig_stats['white_percent']:.2f}%)")
    
    print(f"\nRecovered Image Analysis:")
    print(f"Total pixels: {rec_stats['total']}")
    print(f"Black pixels: {rec_stats['black']} ({rec_stats['black_percent']:.2f}%)")
    print(f"White pixels: {rec_stats['white']} ({rec_stats['white_percent']:.2f}%)")
    
    # Compare pixel ratios
    black_ratio = rec_stats['black'] / orig_stats['black'] if orig_stats['black'] > 0 else 0
    white_ratio = rec_stats['white'] / orig_stats['white'] if orig_stats['white'] > 0 else 0
    
    print(f"\nPixel Ratios:")
    print(f"Black pixel ratio (recovered/original): {black_ratio:.2f}")
    print(f"White pixel ratio (recovered/original): {white_ratio:.2f}")

def main():
    base_dir = "./2025"
    image_name = "Mandrill512X512X24bw_BW"
    
    # Define paths
    old_slides = [
        os.path.join(base_dir, "slides", f"{image_name}_slideA.png"),
        os.path.join(base_dir, "slides", f"{image_name}_slideB.png")
    ]
    
    new_slides = [
        os.path.join(base_dir, "slides", f"{image_name}_slide0.png"),
        os.path.join(base_dir, "slides", f"{image_name}_slide1.png")
    ]
    
    original_image = os.path.join(base_dir, "Images", f"{image_name}.png")
    recovered_positive = os.path.join(base_dir, "out_images", f"{image_name}_R_P.png")
    recovered_negative = os.path.join(base_dir, "out_images", f"{image_name}_R_N.png")
    
    # Check if files exist
    all_files = old_slides + new_slides + [original_image, recovered_positive, recovered_negative]
    for file_path in all_files:
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            return
    
    print("Comparing old and new slides:")
    for i, (old_slide, new_slide) in enumerate(zip(old_slides, new_slides)):
        print(f"Comparing {old_slide} with {new_slide}:")
        total, matching, percentage = compare_images(old_slide, new_slide)
        print(f"Total pixels: {total}")
        print(f"Matching pixels: {matching}")
        print(f"Match percentage: {percentage:.2f}%")
        print("---")
    
    print("\nComparing new slides with each other:")
    total, matching, percentage = compare_images(new_slides[0], new_slides[1])
    print(f"Total pixels: {total}")
    print(f"Matching pixels: {matching}")
    print(f"Match percentage: {percentage:.2f}%")
    print("---")
    
    print("\nAnalyzing original vs recovered images:")
    print("\nPositive recovery:")
    compare_original_recovered(original_image, recovered_positive)
    print("\nNegative recovery:")
    compare_original_recovered(original_image, recovered_negative)

if __name__ == "__main__":
    main() 