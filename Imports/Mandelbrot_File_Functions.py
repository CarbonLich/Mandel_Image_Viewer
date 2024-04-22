from time import localtime
from os.path import isfile


###############################################################################################

# These Functions Read a given PPM file and eaxtract the information in order to replicate them
#
# Round_Float_To_Int is simply there so I can have 155.7 be 156 instead of 155. it's not really important and can be edited out if need be
# Bound_Num makes is necisary since you can't have PPM images with negetive integer RGB values or RGB values that are greater than 255
# The next three functions (Convert_HSV_To_RGB, Convert_HSLuv_To_RGB, and Convert_HPLuv_To_RGB) each make RGB Tuples using different rules and assumptions
# Each of the three functions always produces an RBG tuple with a min of 0, max of 255, and a value that is always an int

###############################################################################################

def Open_PPM_as_List (
    File_Name_PPM
    ):

    with open(File_Name_PPM, "rb") as Reading_File:
        List_From_PPM = ["", "",[]]
        Reading_File.readline()
        Length_Width = str(Reading_File.readline()).removeprefix("b'").removesuffix("\\n'").split(" ")
        List_From_PPM[0] = str(Reading_File.readline()).removeprefix("b'").removeprefix("255").removesuffix("\\n'").split("#")
        List_From_PPM[0].pop(0)
        List_From_PPM[1] = int(Length_Width[0])
        for Col in range (0, List_From_PPM[1]):
            Value1 = Reading_File.read(1)
            Value2 = Reading_File.read(1)
            Value3 = Reading_File.read(1)
            List_From_PPM[2].append((int.from_bytes(Value1), int.from_bytes(Value2), int.from_bytes(Value3)))

    return List_From_PPM

def Open_Mandlebrot_PPM_as_Settings (
    File_Name:str
    ):

    with open(File_Name, "rb") as Reading_File:
        Reading_File.readline()
        Length_Width = str(Reading_File.readline()).removeprefix("b'").removesuffix("\\n'").split(" ")
        Center_Zoom_MaxIter = str(Reading_File.readline()).removeprefix("b'").removeprefix("P6").removesuffix("\\n'").split("#")
        Center_Zoom_MaxIter.pop(0)

    Center_Point, Zoom, Max_Iter, Resolution_Real, Resolution_Imag = float(Center_Zoom_MaxIter[0])+float(Center_Zoom_MaxIter[1])*1j, int(Center_Zoom_MaxIter[2]), int(Center_Zoom_MaxIter[3]), int(Length_Width[0]), int(Length_Width[1])
    return Center_Point, Zoom, Max_Iter, (Resolution_Real, Resolution_Imag)

###############################################################################################

# This Function creates the File name and Suffix for a given file 
# This checks for a dupliate file name and adds a number on the end to handle duplicates

###############################################################################################

def Name_Generation (
    File_Name:str,
    Location:str,
    File_Type:str
    ):

    Time_Creation = (f"{localtime().tm_year}_"
                +f"{localtime().tm_mon if len(str(localtime().tm_mon))==2 else str(0)+str(localtime().tm_mon)}_"
                +f"{localtime().tm_mday if len(str(localtime().tm_mday))==2 else str(0)+str(localtime().tm_mday)} at "
                +f"{localtime().tm_hour if len(str(localtime().tm_hour))==2 else str(0)+str(localtime().tm_hour)}_"
                +f"{localtime().tm_min if len(str(localtime().tm_min))==2 else str(0)+str(localtime().tm_min)}"
    )
    Temp_File_Name = f"{File_Name} {Time_Creation}"
    Dupe_Num = 0

    while isfile(f"{Location}{Temp_File_Name}.{File_Type}"):
        Dupe_Num += 1
        Temp_File_Name = f"{File_Name} {Time_Creation} - {Dupe_Num}"


    return f"{Temp_File_Name}.{File_Type}"

###############################################################################################

# Saves a PPM of a given Bytes list in a given location

###############################################################################################

def Save_PPM_Bytes(Color_Bytes_PPM, Save_Location, Gradient_Or_Mandelbrot):

    Save_Name = Name_Generation(Gradient_Or_Mandelbrot, Save_Location, 'ppm')

    with open(f"{Save_Location}{Save_Name}", "wb") as Mandelbrot_Saved:
        Mandelbrot_Saved.write(Color_Bytes_PPM)

    return