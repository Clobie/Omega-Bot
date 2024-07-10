from PIL import Image, ImageDraw, ImageFont

def get_color(number):
    if number == 100:
        return (210, 180, 140)  # Tan
    elif number == 99:
        return (255, 192, 203)  # Pink
    elif 95 <= number <= 98:
        return (255, 165, 0)    # Orange
    elif 75 <= number <= 94:
        return (128, 0, 128)    # Purple
    elif 50 <= number <= 74:
        return (0, 0, 255)      # Blue
    elif 25 <= number <= 49:
        return (0, 128, 0)      # Green
    else:
        return (128, 128, 128)  # Grey

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def create_emoji(number):
    # Create a 64x64 image with a transparent background
    image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Set the text color based on the number
    text_color = get_color(number)
    
    # Load a font
    try:
        # Try to load a truetype font
        font = ImageFont.truetype("arialbd.ttf", 48)
    except IOError:
        # If truetype font is not available, load the default bitmap font
        font = ImageFont.load_default()
    
    # Draw the number in the center of the image, scaled to fit
    text = str(number)
    text_width, text_height = textsize(text, font=font)
    while text_width > 64 or text_height > 64:
        font = ImageFont.truetype("arial.ttf", font.size - 1)
        text_width, text_height = textsize(text, font=font)
    text_x = (64 - text_width) // 2
    text_y = (64 - text_height) // 2
    draw.text((text_x, text_y), text, fill=text_color, font=font)
    
    # Save the image
    image.save(f'output/parse_{number}.png')

def create_all_emojis():
    for number in range(101):
        create_emoji(number)

# Run the script to create all emojis
create_all_emojis()
