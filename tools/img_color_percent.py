from PIL import Image
from collections import Counter

def rgb_to_hex(rgb):
    return '0x{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def analyze_image(image_path):
    # Load the image
    image = Image.open(image_path)
    image = image.convert('RGB')  # Ensure image is in RGB mode

    # Get pixels
    pixels = list(image.getdata())

    # Count colors
    color_count = Counter(pixels)
    total_pixels = len(pixels)

    # Print color percentages
    for color, count in color_count.items():
        percentage = (count / total_pixels) * 100
        if percentage >= 1:
            rgb = color
            hex_color = rgb_to_hex(color)
            print(f"Color: {hex_color}, RGB: {rgb}, Percentage: {percentage:.2f}%")

# Run the analysis
analyze_image('colors.png')
