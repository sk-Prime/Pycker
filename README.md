# Pycker
Python Tkinter based Color picker

![Manual Image](https://github.com/sk-Prime/Pycker/blob/master/Pycker/Pycker%20Manual_files/image001.png)

Pycker is a python tkinter based color picker tool. Tkinter has no mouse tracking system outside a widget. So in this software we use a invisible toplevel window to get the mouse coordination (x,y). 
To get color value we used Pillow library to take a screenshot, and load that screenshot image to get pixel value from mouse coordination. 

## Requirements
1.	Python 3
2.	Python Imaging Library – Pillow (PIL)


## User manual
1.	the ‘color view’ frame will update with color name, if the color’s hex value exists in database  (dict)
2.	It is the view of main color, either inputted manually or picked by “Pick Color” button. Right mouse button click will copy       hex color value to clipboard.
3.	Analogous colors of main color
4.	137 degree in HSL color space
5.	Monochrome colors of main color
6.	Triad color of main color
7.	To pick color from window press “Pick Color” button, it will activate mouse tracking, to release tracking press left mouse button.
8.	RGB color entry box. You can type your own RGB value, then press Enter key to activate. For example: insert 255, 99, 71 then press enter. The color view will update with that particular color, also known as tomato. You can type ‘random’ then press enter to get randomly generated color.
Left mouse click on this entry will change Slider mode to RGB. Right click will copy the code to clipboard.
9.	HSL color entry. Left mouse click on this entry will change slider mode HSL. Right click will copy the code to clipboard.
10.	Hex color value entry. Right click to copy to clipboard.
11.	Slider mode indicator. HSL and RGB two mode exist.
