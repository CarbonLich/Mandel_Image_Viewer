from os import path as OSPath
import math
import tkinter as TTK
from Imports import Mandelbrot_Base_Functions as Mandel, Mandelbrot_File_Functions as Files
from threading import Thread

Current_Program_Location = f"{OSPath.dirname(OSPath.realpath(__file__))}\\"
Image_Folder = f"{Current_Program_Location}Images\\"
Image_Import_Folder = f"{Current_Program_Location}Imports\\Images_For_Importing\\"
Mandel_PPM_Save_Location = f"{Image_Folder}Mandelbrot PPMs\\"
Gradient_PPM_Save_Location = f"{Image_Folder}Gradient PPMs\\"
Resolution_Standard = (480, 288)
Resolution_Half = (240, 144)
Resolution_Quarter = (120, 72)
Resolution_Eighth = (60, 36)
Resolution_List = [Resolution_Standard, Resolution_Half, Resolution_Quarter, Resolution_Eighth]

Main_Program = TTK.Tk()
Main_Program.iconbitmap(f"{Image_Import_Folder}Mandel_Program_Icon.ico")


def Zoom_In_Or_Out(event):

    if (Real_Pointer_Val:=Base_Window.winfo_pointerx()-Mandelbrot_Image_Label.winfo_rootx()-3) < 0 or Real_Pointer_Val > 480:
        return
    if (Imag_Pointer_Val:=Base_Window.winfo_pointery()-Mandelbrot_Image_Label.winfo_rooty()-3) < 0 or Imag_Pointer_Val > 288:
        return
    if event.delta >0:

        Zoom_Value = TTK_VAR_Mandelbrot_Zoom_In.get()
    else:
        Zoom_Value = TTK_VAR_Mandelbrot_Zoom_Out.get()

    Old_Center_Real, Old_Center_Imag = TTK_VAR_Mandelbrot_Center_Real.get(), TTK_VAR_Mandelbrot_Center_Imag.get()
    Old_Zoom = TTK_VAR_Mandelbrot_Zoom.get()
    Old_Step = float(400/(Old_Zoom*288))

    if (New_Zoom := Mandel.Round_Float_To_Int(Old_Zoom*Zoom_Value)) < 100:
        New_Zoom = 100
    
    New_Step = 400/(New_Zoom*288)

    New_Center_Real, New_Center_Imag = Old_Center_Real - 240*Old_Step + Real_Pointer_Val*(Old_Step), Old_Center_Imag - 144*Old_Step + Imag_Pointer_Val*(Old_Step)
    New_Center_Real, New_Center_Imag = New_Center_Real + 240*New_Step - Real_Pointer_Val*(New_Step), New_Center_Imag + 144*New_Step - Imag_Pointer_Val*(New_Step)

    if New_Center_Real < -2:
        New_Center_Real = -2
    if New_Center_Real > 2:
        New_Center_Real = 2
    if New_Center_Imag < -2:
        New_Center_Imag = -2
    if New_Center_Imag > 2:
        New_Center_Imag = 2

    TTK_VAR_Mandelbrot_Center_Imag.set(New_Center_Imag)
    TTK_VAR_Mandelbrot_Center_Real.set(New_Center_Real)
    TTK_VAR_Mandelbrot_Center_Imag_Mouse.set(New_Center_Imag)
    TTK_VAR_Mandelbrot_Center_Real_Mouse.set(New_Center_Real)
    TTK_VAR_Mandelbrot_Zoom.set(value=New_Zoom)

    Thread(target=Rerender_Mandelbrot, args=(New_Zoom, New_Center_Real, New_Center_Imag)).start()


## These are the various Windows for dividing up the program

Base_Window = TTK.Frame(Main_Program, padx=25, pady=25)
Base_Window.grid(column=0, row=0)

Picture_Window = TTK.Frame(Base_Window, padx=25, pady=25)
Picture_Window.grid(column=0, row=0, columnspan=2)

Options_Window_Gradient = TTK.Frame(Base_Window, borderwidth=3, relief="solid")
Options_Window_Gradient.grid(column=0, row=1)

Color_Options_Window_Gradient = TTK.Frame(Options_Window_Gradient, padx=49, pady=5)
Color_Options_Window_Gradient.grid(column=0, row=0)

Function_Settings_Window_Gradient = TTK.Frame(Options_Window_Gradient, padx=5, pady=5)
Function_Settings_Window_Gradient.grid(column=0, row=1)

Buttons_Window_Gradient = TTK.Frame(Base_Window, padx=25, pady=25)
Buttons_Window_Gradient.grid(column=0, row=2)

Options_Window_Mandel = TTK.Frame(Base_Window, padx=25, pady=25, borderwidth=3, relief="solid")
Options_Window_Mandel.grid(column=1, row=1)

Buttons_Window_Mandel = TTK.Frame(Base_Window, padx=25, pady=25)
Buttons_Window_Mandel.grid(column=1, row=2)


## These are all the Variables I use in the program

TTK_VAR_Render_Mouse_Click = TTK.BooleanVar(Base_Window, value=False)

TTK_VAR_Color_Mode = TTK.StringVar(Base_Window, value="HSV")
TTK_VAR_Color_Val_1_Function = TTK.StringVar(Base_Window, value="x*4")
TTK_VAR_Color_Val_2_Function = TTK.StringVar(Base_Window, value="100")
TTK_VAR_Color_Val_3_Function = TTK.StringVar(Base_Window, value="100")
TTK_VAR_Gradient_Length = TTK.IntVar(Base_Window, 90)
TTK_VAR_Gradient_Test_List = TTK.Variable(Base_Window, value=[])

TTK_VAR_Mandelbrot_Center_Real = TTK.DoubleVar(Base_Window, value=0.0)
TTK_VAR_Mandelbrot_Center_Imag = TTK.DoubleVar(Base_Window, value=0.0)
TTK_VAR_Mandelbrot_Center_Real_Mouse = TTK.DoubleVar(Base_Window, value=0.0)
TTK_VAR_Mandelbrot_Center_Imag_Mouse = TTK.DoubleVar(Base_Window, value=0.0)
TTK_VAR_Mouse_Click_Location_Real = TTK.DoubleVar(Base_Window, value=0.0)
TTK_VAR_Mouse_Click_Location_Imag = TTK.DoubleVar(Base_Window, value=0.0)
TTK_VAR_Mandelbrot_Zoom = TTK.IntVar(Base_Window, value=100)
TTK_VAR_Mandelbrot_Zoom_In = TTK.DoubleVar(Base_Window, value=1.25)
TTK_VAR_Mandelbrot_Zoom_Out = TTK.DoubleVar(Base_Window, value=.8)
TTK_VAR_Mandelbrot_Max_Iter = TTK.IntVar(Base_Window, value=250)
TTK_VAR_Saved_Mandel_Resolution_Real = TTK.IntVar(Base_Window, 1920)
TTK_VAR_Saved_Mandel_Resolution_Imag = TTK.IntVar(Base_Window, 1080)
TTK_VAR_Mandelbrot_Test_Iter_List = TTK.Variable(Base_Window, value=[0])

## These are the the Gradient preview and Mandelbrot Preview respectively
TTK_IMG_Gradient_Image_Reference = TTK.PhotoImage(format="ppm")
Gradient_Image_Label = TTK.Label(Picture_Window, image=TTK_IMG_Gradient_Image_Reference, width=500, height=50, borderwidth=3, relief="solid")
Gradient_Image_Label.grid(column=0, row=1, pady=10)

Mandelbrot_Image_Reference = TTK.PhotoImage(format="ppm")
Mandelbrot_Image_Label = TTK.Label(Picture_Window, image=Mandelbrot_Image_Reference, width=480, height=288, borderwidth=3, relief="solid")
Mandelbrot_Image_Label.bind("<MouseWheel>", Zoom_In_Or_Out)

Mandelbrot_Image_Label.grid(column=0, row=0)

## These are the entries ascociated with the Gradient image
ColorModeLabel = TTK.Label(Color_Options_Window_Gradient, text="Color Mode", width=12)
ColorModeLabel.grid(column=0, row=0, pady=5)
RGB_Var = TTK.OptionMenu(Color_Options_Window_Gradient, TTK_VAR_Color_Mode, "HSV", "RGB", "HSLuv", "HPLuv")#, command=Set_RGB)
RGB_Var.grid(column=1, row=0, pady=5)

ColorVal1Label = TTK.Label(Function_Settings_Window_Gradient, text="H/R Func", width=12)
ColorVal1Label.grid(column=0, row=0, pady=5)
ColorVal1 = TTK.Entry(Function_Settings_Window_Gradient, textvariable=TTK_VAR_Color_Val_1_Function, width=25)
ColorVal1.grid(column=1, row=0, pady=5, padx=25)

ColorVal2Label = TTK.Label(Function_Settings_Window_Gradient, text="S/G Func", width=12)
ColorVal2Label.grid(column=0, row=1, pady=5)
ColorVal2 = TTK.Entry(Function_Settings_Window_Gradient, textvariable=TTK_VAR_Color_Val_2_Function, width=25)
ColorVal2.grid(column=1, row=1, pady=5, padx=25)

ColorVal3Label = TTK.Label(Function_Settings_Window_Gradient, text="V/B Func", width=12)
ColorVal3Label.grid(column=0, row=2, pady=5)
ColorVal3 = TTK.Entry(Function_Settings_Window_Gradient, textvariable=TTK_VAR_Color_Val_3_Function, width=25)
ColorVal3.grid(column=1, row=2, pady=5, padx=25)

Gradient_Length_Label = TTK.Label(Function_Settings_Window_Gradient, text="Length", width=12)
Gradient_Length_Label.grid(column=0, row=3, pady=5)
Gradient_Length = TTK.Entry(Function_Settings_Window_Gradient, textvariable=TTK_VAR_Gradient_Length, width=25)
Gradient_Length.grid(column=1, row=3, pady=5, padx=25)


## These are the buttons ascociated with the Gradient image
Test_Gradient_Image = TTK.Button(Buttons_Window_Gradient, text="Test Gradient", width = 12)
Test_Gradient_Image.grid(column=0, row=0, padx=10)
Save_Gradient_Image = TTK.Button(Buttons_Window_Gradient, text="Save Gradient", width=12)
Save_Gradient_Image.grid(column=1, row=0, padx=10)

## These are the entries ascociated with the Mandelbrot image
Mandelbrot_Center_Label = TTK.Label(Options_Window_Mandel, text="Center Cordinates (x+iy)")
Mandelbrot_Center_Label.grid(column=0, row=0, pady=5)
Mandelbrot_Center_Real = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Mandelbrot_Center_Real)
Mandelbrot_Center_Real.grid(column=1, row=0)
Mandelbrot_Center_Imag = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Mandelbrot_Center_Imag)
Mandelbrot_Center_Imag.grid(column=2, row=0)

Mandelbrot_Zoom_Label = TTK.Label(Options_Window_Mandel, text="Zoom Level")
Mandelbrot_Zoom_Label.grid(column=0, row=1, pady=5)
Mandelbrot_Zoom = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Mandelbrot_Zoom)
Mandelbrot_Zoom.grid(column=1, row=1, columnspan=2)

Mandelbrot_Zoom_Step_Label = TTK.Label(Options_Window_Mandel, text="Zoom Amount (In/Out)")
Mandelbrot_Zoom_Step_Label.grid(column=0, row=2, pady=5)
Mandelbrot_Zoom_Step_In = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Mandelbrot_Zoom_In)
Mandelbrot_Zoom_Step_In.grid(column=1, row=2)
Mandelbrot_Zoom_Step_Out = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Mandelbrot_Zoom_Out)
Mandelbrot_Zoom_Step_Out.grid(column=2, row=2)

Mandelbrot_Resolution_Label = TTK.Label(Options_Window_Mandel, text="Saving Resolution")
Mandelbrot_Resolution_Label.grid(column=0, row=3, pady=5)
Mandelbrot_Resolution_Real = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Saved_Mandel_Resolution_Real)
Mandelbrot_Resolution_Real.grid(column=1, row=3)
Mandelbrot_Resolution_Imag = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Saved_Mandel_Resolution_Imag)
Mandelbrot_Resolution_Imag.grid(column=2, row=3)

Max_Iteration_Level_Label = TTK.Label(Options_Window_Mandel, text="Max Iteration")
Max_Iteration_Level_Label.grid(column=0, row=4, pady=5)
Max_Iteration_Level = TTK.Entry(Options_Window_Mandel, textvariable=TTK_VAR_Mandelbrot_Max_Iter, width= 35)
Max_Iteration_Level.grid(column=1, row=4, columnspan=2)

Test_Mandelbrot_Image = TTK.Button(Buttons_Window_Mandel, text="Test new Mandelbrot")
Test_Mandelbrot_Image.grid(column=0, row=0, padx=15)
Save_Mandelbrot_Image = TTK.Button(Buttons_Window_Mandel, text="Save current Mandelbrot")
Save_Mandelbrot_Image.grid(column=2, row=0, padx=15)

def Rerender_Gradient():

    New_Gradient_List = Mandel.Create_Gradient_List((
        TTK_VAR_Color_Val_1_Function.get(),
        TTK_VAR_Color_Val_2_Function.get(),
        TTK_VAR_Color_Val_3_Function.get()),
        TTK_VAR_Gradient_Length.get(),
        TTK_VAR_Color_Mode.get(),
        False
    )

    TTK_VAR_Gradient_Test_List.set(New_Gradient_List)

    New_Gradient_Display_List = Mandel.Create_Gradient_List((
        TTK_VAR_Color_Val_1_Function.get(),
        TTK_VAR_Color_Val_2_Function.get(),
        TTK_VAR_Color_Val_3_Function.get()),
        TTK_VAR_Gradient_Length.get(),
        TTK_VAR_Color_Mode.get(),
        True
    )

    TTK_IMG_Gradient_Image_Reference.config(data=Mandel.Gradient_Color_To_Bytes(New_Gradient_Display_List))

def Rerender_Mandelbrot(Zoom_Level, Center_Real, Center_Imag):

    for Render_Level in range(0, 4):
        if TTK_VAR_Mandelbrot_Zoom.get() != Zoom_Level or TTK_VAR_Mandelbrot_Center_Real.get() != Center_Real or TTK_VAR_Mandelbrot_Center_Imag.get() != Center_Imag:
            return
        New_Mandelbrot_List = Mandel.Create_Mandelbrot_List(float(TTK_VAR_Mandelbrot_Center_Real.get()),
                                                            float(TTK_VAR_Mandelbrot_Center_Imag.get()),
                                                            int(TTK_VAR_Mandelbrot_Zoom.get()),
                                                            int(TTK_VAR_Mandelbrot_Max_Iter.get()),
                                                            Resolution_List[3-Render_Level]) 
        TTK_VAR_Mandelbrot_Test_Iter_List.set(New_Mandelbrot_List)
        Mandelbrot_Image_Reference.configure(data = Mandel.Mandel_Color_To_Bytes(
                Mandel.Color_Mandel_List(
                    New_Mandelbrot_List,
                    TTK_VAR_Gradient_Test_List.get()
                ), 2**(3-Render_Level)
            ))

def Recolor_Mandelbrot():
    Mandelbrot_Image_Reference.configure(data = Mandel.Mandel_Color_To_Bytes(
                Mandel.Color_Mandel_List(
                    TTK_VAR_Mandelbrot_Test_Iter_List.get(),
                    TTK_VAR_Gradient_Test_List.get()
                ), 1
            ))
    
def Test_Gradient_Button_Func():
    Rerender_Gradient()
    Recolor_Mandelbrot()

def Click_Move_Mandelbrot_Func(event):
    
    Change_Real = event.x
    Change_Imag = event.y
    Current_Step = float(400/(TTK_VAR_Mandelbrot_Zoom.get()*288))

    New_Center_Real = TTK_VAR_Mandelbrot_Center_Real_Mouse.get() + (TTK_VAR_Mouse_Click_Location_Real.get()-Change_Real)*Current_Step
    New_Center_Imag = TTK_VAR_Mandelbrot_Center_Imag_Mouse.get() + (TTK_VAR_Mouse_Click_Location_Imag.get()-Change_Imag)*Current_Step

    if New_Center_Real < -2:
        New_Center_Real = -2
    if New_Center_Real > 2:
        New_Center_Real = 2
    if New_Center_Imag < -2:
        New_Center_Imag = -2
    if New_Center_Imag > 2:
        New_Center_Imag = 2


    TTK_VAR_Mandelbrot_Center_Real.set(New_Center_Real)
    TTK_VAR_Mandelbrot_Center_Imag.set(New_Center_Imag)

    Thread(target=Rerender_Mandelbrot, args=(TTK_VAR_Mandelbrot_Zoom.get(), New_Center_Real, New_Center_Imag)).start()

    return

def Set_Mouse_Click_Location():

    if (Real_Pointer_Val:=Base_Window.winfo_pointerx()-Mandelbrot_Image_Label.winfo_rootx()-3) < 0 or Real_Pointer_Val > 480:
        return
    if (Imag_Pointer_Val:=Base_Window.winfo_pointery()-Mandelbrot_Image_Label.winfo_rooty()-3) < 0 or Imag_Pointer_Val > 288:
        return
    
    TTK_VAR_Render_Mouse_Click.set(True)

    TTK_VAR_Mandelbrot_Center_Real_Mouse.set(TTK_VAR_Mandelbrot_Center_Real.get())
    TTK_VAR_Mandelbrot_Center_Imag_Mouse.set(TTK_VAR_Mandelbrot_Center_Imag.get())

    TTK_VAR_Mouse_Click_Location_Real.set(Real_Pointer_Val)
    TTK_VAR_Mouse_Click_Location_Imag.set(Imag_Pointer_Val)



Base_Window.after(1, Rerender_Gradient)
Thread(target=Rerender_Mandelbrot, args=(100, 0, 0)).start()

Test_Mandelbrot_Image.configure(command=lambda:Thread(target=Rerender_Mandelbrot, args=(TTK_VAR_Mandelbrot_Zoom.get(), TTK_VAR_Mandelbrot_Center_Real.get(), TTK_VAR_Mandelbrot_Center_Imag.get())).start())

Test_Gradient_Image.configure(command=Test_Gradient_Button_Func)

Save_Mandelbrot_Image.configure(command=lambda:Files.Save_PPM_Bytes(Mandel.Mandel_Color_To_Bytes(Mandel.Color_Mandel_List(
                                                                        Mandel.Create_Mandelbrot_List(TTK_VAR_Mandelbrot_Center_Real.get(),
                                                                            TTK_VAR_Mandelbrot_Center_Imag.get(),
                                                                            TTK_VAR_Mandelbrot_Zoom.get(),
                                                                            TTK_VAR_Mandelbrot_Max_Iter.get(),
                                                                            (TTK_VAR_Saved_Mandel_Resolution_Real.get(), TTK_VAR_Saved_Mandel_Resolution_Imag.get())),
                                                                    TTK_VAR_Gradient_Test_List.get()), 1),
                                                                                                   Mandel_PPM_Save_Location, "Mandelbrot"))\

Save_Gradient_Image.configure(command=lambda:Files.Save_PPM_Bytes(Mandel.Gradient_Color_To_Bytes(TTK_VAR_Gradient_Test_List.get()), Gradient_PPM_Save_Location, "Gradient"))

Mandelbrot_Image_Label.bind(sequence="<Button-1>", func=lambda event:Set_Mouse_Click_Location())

Mandelbrot_Image_Label.bind(sequence="<B1-Motion>", func=Click_Move_Mandelbrot_Func)


Main_Program.mainloop()