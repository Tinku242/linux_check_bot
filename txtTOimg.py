from PIL import Image, ImageDraw, ImageFont


def textToimage(save, text, width, height):
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("PlaypenSans.ttf", 16)
    draw.text((10, 10), text, (0, 0, 0), font=font)
    image.save(f"images/{save}.png")
