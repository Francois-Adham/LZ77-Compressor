from bitarray import bitarray
import numpy as np
from PIL import Image

lookahead_buffer_size = input("Enter look-ahead size: ")
lookahead_buffer_size = int(lookahead_buffer_size)
width = input("Enter Width: ")
width = int(width)
height = input("Enter Height: ")
height = int(height)
U16 = False
if lookahead_buffer_size > 256:
    U16 = True
flags = bitarray()
with open('flags.txt', 'rb') as flags_file:
    flags.fromfile(flags_file)
if U16:
    colors = np.fromfile('colors.npy', dtype=np.uint8)
    colors = list(colors)
    tags = np.fromfile('tags.npy', dtype=np.uint16)
    tags = list(tags)
else:
    tags = np.fromfile('tags.npy', dtype=np.uint8)
    tags = list(tags)
print(flags)
print(tags)
image = []
i = 0
pixel = 0
while pixel < (width * height) and len(tags) > 0:
    if flags[i]:
        if U16:
            matched_colors_index = pixel - tags[0]
            tags.pop(0)
            j = 0
            while j < tags[0]:
                image.append(image[matched_colors_index])
                pixel += 1
                matched_colors_index += 1
                j += 1
            tags.pop(0)
            if pixel < (width * height):
                image.append(colors[0])
                pixel += 1
                colors.pop(0)
        else:
            matched_colors_index = pixel - tags[0]
            tags.pop(0)
            j = 0
            while j < tags[0]:
                image.append(image[matched_colors_index])
                pixel += 1
                matched_colors_index += 1
                j += 1
            tags.pop(0)
            if pixel < (width * height):
                image.append(tags[0])
                pixel += 1
                tags.pop(0)
    else:
        if U16:
            image.append(colors[0])
            pixel += 1
            colors.pop(0)
        else:
            image.append(tags.pop(0))
            pixel += 1
    i += 1
print(image)
while len(image) < width * height:
    image.append(1)

image = np.reshape(image, (height, width))
im = Image.fromarray(np.array(image, dtype=np.uint8))
im.save("final.jpg")
im.save("final.jpeg")
im.save("final.png")
