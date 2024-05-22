from os import path

## These are the constants that I will use in my program

__CURRENT_PROGRAM_LOCATION = f"{path.dirname(path.realpath(__file__))}"
__CURRENT_PROGRAM_LOCATION = __CURRENT_PROGRAM_LOCATION.strip("mandel_imports")
__IMAGE_FOLDER = f"{__CURRENT_PROGRAM_LOCATION}Images\\"
__IMAGE_IMPORT_FOLDER = f"{__CURRENT_PROGRAM_LOCATION}mandel_imports\\Images_For_Importing\\"
__MANDEL_PPM_LOC = f"{__IMAGE_FOLDER}Mandelbrot PPMs\\"
__GRADIENT_PPM_LOC = f"{__IMAGE_FOLDER}Gradient PPMs\\"
RESOLUTION_STANDARD = (480, 288)
RESOLUTION_HALF = (240, 144)
RESOLUTION_QUARTER = (120, 72)
RESOLUTION_EIGHTH = (60, 36)
RESOLUTION_LIST = [RESOLUTION_STANDARD, RESOLUTION_HALF, RESOLUTION_QUARTER, RESOLUTION_EIGHTH]

def printconsts():

    print(__CURRENT_PROGRAM_LOCATION)
    print(__IMAGE_FOLDER)
    print(__IMAGE_IMPORT_FOLDER)
    print(__MANDEL_PPM_LOC)
    print(__GRADIENT_PPM_LOC)
    for a in RESOLUTION_LIST:
        print(a)