from wand.image import Image
from wand.color import Color

# img =  Image(filename='1.pdf')
with Image(filename="1.pdf[0]") as img:
     img.save(filename="temp.jpg")