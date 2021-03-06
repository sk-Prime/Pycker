# Pycker
## Python Tkinter based Color picker
Pycker is a python tkinter based color picker tool. Tkinter has no mouse tracking system outside a widget. So in this software we use an invisible toplevel window to get the mouse coordination (x,y). 
To get color value we used Pillow library/mss library to take a screenshot, and load that screenshot image to get pixel value from mouse coordination. pillow screenshot has some problem with higher resolution screen and maybe not working on linux. so mss is the best option.

## Requirements
1.	Python 3
2.  <a href ="https://pypi.org/project/mss/">mss</a> library<br>
or Python Imaging Library – Pillow (PIL)-not required, if mss exist in system (mss highly recomended)

## High DPI monitor setting
In high DPI monitor pycker (1.1 rel) doesn't work as expected. In windows 10 you can fix it by following the steps listed bellow
1. Right click on pycker.exe and open properties
2. Then click on compatible tab
3. At the bottom of the dialog there is a option named "change high dpi setting" click on it. It will open a new dialog.
4. Tick the override high dpi scaling behavior checkbox.

Then pycker will work as expected.


## User manual
Look at the image and match the numbers<br>
<img src="https://github.com/sk-Prime/Pycker/blob/master/Pycker/Pycker%20Manual_files/Pycker%20Manual.png" height="800">
1.	the ‘color view’ frame will update with color name, if the color’s hex value exists in database  (dict)
2.	It is the view of main color, either inputted manually or picked by “Pick Color” button. **Right mouse click** will copy       hex color value to clipboard.
3.	Analogous colors of main color. clicking any of this four colors will send it to the center, main color view.
4.	137 degree rotation in HSL color space. clicking any of this four colors will send it to the center, main color view.
5.	Monochrome colors of main color. clicking any of this four colors will send it to the center, main color view.
6.	Triad color of main color. clicking any of this four colors will send it to the center, main color view.
7.	To pick color from window press “Pick Color” button, it will activate mouse tracking, to release tracking press **left mouse button.**
8.	RGB color entry box. You can type your own RGB value, then press **Enter key** to activate. For example: insert 255, 99, 71 then press enter. The color view will update with that particular color known as tomato color. **Left mouse click** on this entry will change Slider mode to RGB. **Right click** will copy the code to clipboard.
some other commands
* random : to generate single random color
* random all : to fill all color label to randomly generated color
* stepsX : to change the color step’s (15) step. Replace X to any number
9.	HSL color entry. **Left mouse click** on this entry will change slider mode HSL. **Right click** will copy the code to clipboard.
10. Hex color value entry. **Right click** to copy to clipboard.
11. Slider mode indicator. **HSL** and **RGB** two mode exist.
12. This button will change the base color (14) to currently selected color
13. end step of steps
14. Base step, from where color will stepping begins
15. All the steps required to travel base step to end step. Use stepsX (8.c) to change required steps

The color_data.dbp was created from https://github.com/meodai/color-names
it is a pickled dictionary, which contains {hex_code:color_name}

icon collected from https://www.flaticon.com/free-icon/color-picker_719747
