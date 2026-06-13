from PIL import Image, ImageDraw, ImageFont
import os

# Create images directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Create a simple logo
img = Image.new('RGB', (100, 100), color='#667eea')
draw = ImageDraw.Draw(img)

# Draw a white circle
draw.ellipse((10, 10, 90, 90), fill='white')

# Add text
try:
    # Try to use a default font
    font = ImageFont.load_default()
    draw.text((35, 40), "SMS", fill='#667eea', font=font)
except:
    draw.text((35, 40), "SMS", fill='#667eea')

# Save the image
img.save('static/images/header_logo.png')
print("✅ Logo created at static/images/header_logo.png")