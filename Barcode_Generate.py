# import EAN13 from barcode module 
from barcode import Code128 
# import ImageWriter to generate an image file 
from barcode.writer import ImageWriter 
# Imports PIL module
from PIL import Image
import os 
import sys 
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 

def generate(number):
    # Make sure to pass the number as string 

    # Now, let's create an object of EAN13 class and 
    # pass the number with the ImageWriter() as the 
    # writer 
    my_code = Code128(number, writer=ImageWriter()) 

    # Our barcode is ready. Let's save it. 
    my_code.save(number)

    # open method used to open different extension image file
    im = Image.open(number+".png")

    # This method will show image in any image viewer
    im.show()

    return im