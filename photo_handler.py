from PIL import Image

top_images = [
    Image.open("t-shirt-czarna-lahtipro-przod-min.jpg"),
    Image.open("05MA4C481A01.jpg"),
    Image.open("05MA4C481A01.jpg")
] # tu bedzie ladowanie z api jak front zrobi wysylanie, potem przerobie endpoint
bottom_images = [
    Image.open("05MA4C481A01.jpg"),
    Image.open("05MA4C481A01.jpg"),
    Image.open("05MA4C481A01.jpg")
] # tu tez

base_width, base_height = top_images[0].size
top_images = [img.resize((base_width, base_height)) for img in top_images]
bottom_images = [img.resize((base_width, base_height)) for img in bottom_images]

total_width = base_width * len(top_images)
total_height = base_height * 2

canvas = Image.new("RGB", (total_width, total_height), (255, 255, 255))

x = 0
y = 0
for img in top_images:
    canvas.paste(img, (x, y))
    x += base_width

x = 0
y = base_height
for img in bottom_images:
    canvas.paste(img, (x, y))
    x += base_width

canvas.show()