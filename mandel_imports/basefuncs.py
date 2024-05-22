from numba import njit
from hsluv import hsluv_to_rgb, hpluv_to_rgb
from time import localtime, time
from os.path import isfile
import math

###############################################################################################

# Returns a Mandelbrot list with the following characteristics:
# 
# Center_Point_Real: Float representing the real portion of the center point
# Center_Point_Imag: Float representing the imaginary portion of the center point
# Zoom: calculated so that a zoom level of 1 creates an image with the vertical axis of -2i <--> 2i and each power of 10 divides the axis by 10
# Max_Iter: number of times the program goes through a mandelbrot function for each pixel
# Resolution_X_Y: The list dimensions that the function will return
#
# The return list format is (Center_Real, Center_Imag, Zoom, Max_Iter, [Resolution_X_Y[0], Resolution_X_Y[1]], [[Final_Iteration_Result*Col]*Row])
# the value of each pixel is offset by a half step in both directions so that the color is based on the center of the pixel, not the corner

###############################################################################################

@njit
def Recursion_Depth(Complex_Number_Vals, Max_Iter):
    Complex_Real_Start = Complex_Number_Vals[0]
    Complex_Imag_Start = Complex_Number_Vals[1]
    Current_Real, Current_Imag = 0 ,0
    for Current_Iter in range (0, Max_Iter):
        if Current_Real*Current_Real + Current_Imag*Current_Imag > 4:
            return Current_Iter
        Current_Real, Current_Imag = (Current_Real*Current_Real-Current_Imag*Current_Imag + Complex_Real_Start), (2*Current_Real*Current_Imag + Complex_Imag_Start)
    return Max_Iter

@njit
def Create_Mandelbrot_List(
    Center_Point_Real:float,
    Center_Point_Imag:float,
    Zoom_Level:int,
    Max_Iter:int,
    Image_Resolution:tuple,
    ):

    Mandel_Iter_List = [[
        Recursion_Depth((Center_Point_Real+(400*(Real_Step+.5)/Zoom_Level/Image_Resolution[1]),Center_Point_Imag+(400*(Imag_Step+.5)/Zoom_Level/Image_Resolution[1])), Max_Iter)
        for Real_Step in range (int(-Image_Resolution[0]/2), int(Image_Resolution[0]/2))
    ]for Imag_Step in range (int(-Image_Resolution[1]/2), int(Image_Resolution[1]/2))]

    return Center_Point_Real, Center_Point_Imag, Zoom_Level, Max_Iter, Image_Resolution, Mandel_Iter_List

###############################################################################################

# This function generates a gradient list
# This take in a str variable list and uses the eval fucntion to evauate them.
# math is imported normaly so any funtions that are in it need to be math.The_Chosen_Function() in order to work
# The Color_Type variable currently has 4 options: "RGB", "HSV", "HSLuv", and "HPLuv"
# The mod version creates a version that always is 500 length but the functions are squashed or streched to fit
# Length is the gradient Length
# Gradient_For_Display is a bool where yes means the gradient will get modded to be for a 500 pixel length image and no will be for an unmodded gradient image.
#
# The return list format is ([RGB_Functions[Red], RGB_Functions[Green], RGB_Functions[Blue]], Mod_Length, [[Red_Val, Green_Val, Blue_Val]*Col])

###############################################################################################

def Create_Gradient_List (
    RGB_Functions:list[str, str, str],
    Length:int,
    Color_Type:str,
    Gradient_For_Display:bool
    ):    

    Mod_RGB_Functions = ["Mod_Hue_or_Red_Function", "Mod_Sat_or_Green_Function", "Mod_Val_or_Blue_Function"]
    if Gradient_For_Display:
        Mod_Length = 500
    else:
        Mod_Length = Length

    for Func_Num in range(0,3):
        if Length == Mod_Length:
            Mod_RGB_Functions[Func_Num] = RGB_Functions[Func_Num]
            continue
        Mod_Func = ""
        for a in RGB_Functions[Func_Num]:
            if a != "x":
                Mod_Func += a
            else:
                Mod_Func += f"(x*{Length}/{Mod_Length})"
        Mod_RGB_Functions[Func_Num] = Mod_Func

    if Color_Type == "RBG":

        Temp_List = [
                [Bound_Num(eval(Mod_RGB_Functions[0])),
                Bound_Num(eval(Mod_RGB_Functions[1])),
                Bound_Num(eval(Mod_RGB_Functions[2]))
                ]
                for x in range (0, Mod_Length)
                ]
        return [Mod_RGB_Functions[0], Mod_RGB_Functions[1], Mod_RGB_Functions[2]], Mod_Length, Temp_List

    elif Color_Type == "HSV":

        Temp_List = [
                Convert_HSV_To_RGB(
                [eval(Mod_RGB_Functions[0]),
                eval(Mod_RGB_Functions[1]),
                eval(Mod_RGB_Functions[2])
                ])
                for x in range (0, Mod_Length)
                ]
        return [Mod_RGB_Functions[0], Mod_RGB_Functions[1], Mod_RGB_Functions[2]], Mod_Length, Temp_List

    elif Color_Type == "HSLuv":
        
        Temp_List = [
                Convert_HSLuv_To_RGB(
                [eval(Mod_RGB_Functions[0]),
                eval(Mod_RGB_Functions[1]),
                eval(Mod_RGB_Functions[2])
                ])
                for x in range (0, Mod_Length)
                ]
        return [Mod_RGB_Functions[0], Mod_RGB_Functions[1], Mod_RGB_Functions[2]], Mod_Length, Temp_List

    
    elif Color_Type == "HPLuv":
        
        Temp_List = [
                Convert_HPLuv_To_RGB(
                [eval(Mod_RGB_Functions[0]),
                eval(Mod_RGB_Functions[1]),
                eval(Mod_RGB_Functions[2])
                ])
                for x in range (0, Mod_Length)
                ]
        
        return [Mod_RGB_Functions[0], Mod_RGB_Functions[1], Mod_RGB_Functions[2]], Mod_Length, Temp_List

###############################################################################################

# These Functions are involved in changing a given type of 3 part color into an RBG color that can be displayed by the computer
#
# Round_Float_To_Int is simply there so I can have 155.7 be 156 instead of 155. it's not really important and can be edited out if need be
# Bound_Num makes is necisary since you can't have PPM images with negetive integer RGB values or RGB values that are greater than 255
# The next three functions (Convert_HSV_To_RGB, Convert_HSLuv_To_RGB, and Convert_HPLuv_To_RGB) each make RGB Tuples using different rules and assumptions
# Each of the three functions always produces an RBG tuple with a min of 0, max of 255, and a value that is always an int

###############################################################################################

def Round_Float_To_Int (
    Float_To_Round:float
    ):
    if Float_To_Round - int(Float_To_Round) <.5:
        return int(Float_To_Round)
    else:
        return int(Float_To_Round)+1


def Bound_Num (
    Number:float,
    Bound:int
    ):
    if Number < 0:
        return 0
    if Number > Bound:
        return Bound
    return Round_Float_To_Int(Number)


def Convert_HSV_To_RGB (
    Starting_Vals:list[float, float, float]
    ):

    Starting_Val_Hue = Starting_Vals[0]%360
    Starting_Val_Sat = Round_Float_To_Int(255*Bound_Num(Starting_Vals[1], 100)/100)
    Starting_Val_Value = Round_Float_To_Int(255*Bound_Num(Starting_Vals[2], 100)/100)
    Starting_Val_Hue_Mod = Starting_Val_Hue%60
 
    if Starting_Val_Hue >=0 and Starting_Val_Hue < 60:
 
        Temp_Val = 255/60*Starting_Val_Hue_Mod
        Temp_Val = Temp_Val+(255-Temp_Val)*(255-Starting_Val_Sat)/255
 
        return (
            Round_Float_To_Int(Starting_Val_Value),
            Round_Float_To_Int(Temp_Val*Starting_Val_Value/255),
            Round_Float_To_Int((255-Starting_Val_Sat)*Starting_Val_Value/255)
        )
 
    elif Starting_Val_Hue >=60 and Starting_Val_Hue < 120:
 
        Temp_Val = 255/60*(60-Starting_Val_Hue_Mod)
        Temp_Val = Temp_Val+(255-Temp_Val)*(255-Starting_Val_Sat)/255
 
        return (
            Round_Float_To_Int(Temp_Val*Starting_Val_Value/255),
            Round_Float_To_Int(Starting_Val_Value),
            Round_Float_To_Int((255-Starting_Val_Sat)*Starting_Val_Value/255)
        )
 
    elif Starting_Val_Hue >=120 and Starting_Val_Hue < 180:
 
        Temp_Val = 255/60*Starting_Val_Hue_Mod
        Temp_Val = Temp_Val+(255-Temp_Val)*(255-Starting_Val_Sat)/255
 
        return (
            Round_Float_To_Int((255-Starting_Val_Sat)*Starting_Val_Value/255),
            Round_Float_To_Int(Starting_Val_Value),
            Round_Float_To_Int(Temp_Val*Starting_Val_Value/255)
        )
   
    elif Starting_Val_Hue >=180 and Starting_Val_Hue < 240:
       
        Temp_Val = 255/60*(60-Starting_Val_Hue_Mod)
        Temp_Val = Temp_Val+(255-Temp_Val)*(255-Starting_Val_Sat)/255
 
        return (
            Round_Float_To_Int((255-Starting_Val_Sat)*Starting_Val_Value/255),
            Round_Float_To_Int(Temp_Val*Starting_Val_Value/255),
            Round_Float_To_Int(Starting_Val_Value)
        )
 
    elif Starting_Val_Hue >=240 and Starting_Val_Hue < 300:
 
        Temp_Val = 255/60*Starting_Val_Hue_Mod
        Temp_Val = Temp_Val+(255-Temp_Val)*(255-Starting_Val_Sat)/255
 
        return (
            Round_Float_To_Int(Temp_Val*Starting_Val_Value/255),
            Round_Float_To_Int((255-Starting_Val_Sat)*Starting_Val_Value/255),
            Round_Float_To_Int(Starting_Val_Value)
        )
   
    elif Starting_Val_Hue >=300 and Starting_Val_Hue < 360:
 
        Temp_Val = 255/60*(60-Starting_Val_Hue_Mod)
        Temp_Val = Temp_Val+(255-Temp_Val)*(255-Starting_Val_Sat)/255
 
        return (
            Round_Float_To_Int(Starting_Val_Value),
            Round_Float_To_Int((255-Starting_Val_Sat)*Starting_Val_Value/255),
            Round_Float_To_Int(Temp_Val*Starting_Val_Value/255)
        )


def Convert_HSLuv_To_RGB (
    HSLuv_Vals:list[float, float, float]
    ):
    Frac_Vals = hsluv_to_rgb((Bound_Num(HSLuv_Vals[0], 360), Bound_Num(HSLuv_Vals[1], 100), Bound_Num(HSLuv_Vals[2], 100)))
    return (Round_Float_To_Int(255*Frac_Vals[0]), Round_Float_To_Int(255*Frac_Vals[1]), Round_Float_To_Int(255*Frac_Vals[2]))


def Convert_HPLuv_To_RGB (
    HPLuv_Vals:list[float, float, float]
    ):
    Frac_Vals = hpluv_to_rgb((Bound_Num(HPLuv_Vals[0], 360), Bound_Num(HPLuv_Vals[1], 100), Bound_Num(HPLuv_Vals[2], 100)))
    return (Round_Float_To_Int(255*Frac_Vals[0]), Round_Float_To_Int(255*Frac_Vals[1]), Round_Float_To_Int(255*Frac_Vals[2]))

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

# This Functions takes the lists generated by the Create_Mandelbrot_List and the Create_Gradient_List
# The returned list is a shallow copy of the Mandel_List where the Iter_Result values are replaced with RGB values from the Gradient_List
#
# The return list format is ([Center_Point_Real, CenterPoint_Imag], Zoom, Max_Iter, [Resolution_X_Y[0], Resolution_X_Y[1]], [[[Red_Value, Green_Value, Blue_Value]*Col]*Row])

###############################################################################################

def Color_Mandel_List (
        Mandel_List:list[float, float, int, int, list[int, int], list[list[int]]],
        Gradient_List:list[int, list[list[int, int, int]]]
        ):
    Mandel_List_Colored = [[0]*Mandel_List[4][0] for Imag in range(0, Mandel_List[4][1])]
    for Real in range (0, Mandel_List[4][0]):
        for Imag in range (0, Mandel_List[4][1]):
            if Mandel_List[5][Imag][Real] != Mandel_List[3]:
                Mandel_List_Colored[Imag][Real] = Gradient_List[2][Mandel_List[5][Imag][Real]%Gradient_List[1]]
            else:
                Mandel_List_Colored[Imag][Real] = [0,0,0]
    return Mandel_List[0], Mandel_List[1], Mandel_List[2], Mandel_List[3], [Mandel_List[4][0], Mandel_List[4][1]], Mandel_List_Colored

###############################################################################################

# Creates a Mandelbrot Color PPM Byte list
# returns a bytearray that is represents a PPM image of the given Mandelbrot List

###############################################################################################

def Mandel_Color_To_Bytes (Mandel_Color_List, Scaling_Factor:int):

    Mandelbrot_Header_Top = f"P6\n"
    Mandelbrot_Header_Mid = f"{Mandel_Color_List[4][0]*Scaling_Factor} {Mandel_Color_List[4][1]*Scaling_Factor}\n"
    Mandelbrot_Header_Bot = f"255#{Mandel_Color_List[0]}#{Mandel_Color_List[1]}#{Mandel_Color_List[2]}#{Mandel_Color_List[3]}\n"
    Mandelbrot_Header_Full = f"{Mandelbrot_Header_Top}{Mandelbrot_Header_Mid}{Mandelbrot_Header_Bot}"
    
    Mandelbrot_Color_Bytes = b"".join([bytearray(Mandel_Color_List[5][Imag//Scaling_Factor][Real//Scaling_Factor]) for Imag in range (0, Mandel_Color_List[4][1]*Scaling_Factor) for Real in range (0, Mandel_Color_List[4][0]*Scaling_Factor)])
    return bytes(Mandelbrot_Header_Full, "utf-8")+Mandelbrot_Color_Bytes
###############################################################################################

# Creates a Gradient Color PPM Byte list
# returns a bytearray that is represents a PPM image of the given Gradient List

###############################################################################################

def Gradient_Color_To_Bytes (Gradient_Color_List):

    Gradient_Header_Full = f"P6\n{Gradient_Color_List[1]} 50\n255#{Gradient_Color_List[0][0]}#{Gradient_Color_List[0][1]}#{Gradient_Color_List[0][2]}\n"
    Gradient_Color_Bytes = b"".join([Gradient_Color_List[2][Col][RGB].to_bytes(1) for Row in range (0, 50) for Col in range (0, Gradient_Color_List[1]) for RGB in range (0, 3)])

    return bytes(Gradient_Header_Full, "utf-8")+Gradient_Color_Bytes

###############################################################################################

# Saves a PPM of a given Bytes list in a given location

###############################################################################################

def Save_PPM_Bytes(Color_Bytes_PPM, Save_Location, Gradient_Or_Mandelbrot):

    Save_Name = Name_Generation(Gradient_Or_Mandelbrot, Save_Location, 'ppm')

    with open(f"{Save_Location}{Save_Name}", "wb") as Mandelbrot_Saved:
        Mandelbrot_Saved.write(Color_Bytes_PPM)

    return

###############################################################################################
    
# Preconfigured Mandelbrot Lists and Gradient lists

###############################################################################################

__Test_Mandelbrot_List = Create_Mandelbrot_List(-0.7882523148148148, 0.1395833333333333, 1024, 2000, (40, 30))

__Test_Gradient_List = Create_Gradient_List(["x", "50 + 50*math.sin(math.pi*x/45)", "50 + 50*math.cos(math.pi*x/90)"], 360, "HSV", False)

__Test_Mandelbrot_Colored = Color_Mandel_List(__Test_Mandelbrot_List, __Test_Gradient_List)

__Test_Mandelbrot_Bytes = Mandel_Color_To_Bytes(__Test_Mandelbrot_Colored, 1)

#################################################################################################

## Testing Area only un comment if something needs to be tested

#################################################################################################