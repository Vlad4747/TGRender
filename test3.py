
from PIL import Image, ImageFont, ImageDraw, ImageEnhance


# (2024) no need RGBA if you don't use `composite()` (besides JPG can't write RGBA)
source_img = Image.new("RGB", (700, 300), "white")  # .convert("RGBA")

# create image with size (100,100) and black background
font = ImageFont.truetype("arial")

text = "very loooooooooooooooooong text"

# get text size
text_size = font.getbbox(text)
print(text_size)
# set button size + 10px margins
button_size = (text_size[2]-text_size[0]+20, text_size[3]+text_size[1]+20)
print(button_size)
# create image with correct size and black background
button_img = Image.new('RGBA', button_size, "black")

# put text on button with 10px margins
button_draw = ImageDraw.Draw(button_img)
button_draw.text((10, 10), text, font=font)

# put button on source image in position (0, 0)
source_img.paste(button_img, (0, 0))

# save in new file
source_img = source_img.convert("RGB")  # (2024) if you want to save as JPG
source_img.save("output.jpg", "JPEG")