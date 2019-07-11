#---------------------------------------#
#Pycker                                 #
#Author:sk_prime                        #
#                                       #
#---------------------------------------#
import tkinter
import pickle
import colorsys
from random import randint
from tkinter import messagebox
try:
    from PIL import ImageGrab
except:
    messagebox.showerror("Module not Found","PIL library is missing")
    exit()

class Main_UI(tkinter.Frame):
    def __init__(self, parent,**kwag):
        tkinter.Frame.__init__(self,parent,**kwag)
        self.parent=parent
        self.parent.title("Pycker 1.1")
        self.parent.iconbitmap("Pyco.ico")

        self.c_size=61 #big center color label size
        self.dbp=1 #if database file exist then color name will be shown
        try:
            with open('color_data.dbp', 'rb') as db:
                self.color_name=pickle.load(db) #unpickle={'hex value':'color name'}
        except:
            self.dbp=0 #else color name won't be available


    #--steps frame----------vertical labels- steps----------
        self.steps_frame=tkinter.Frame(self.parent)
        self.steps_frame.pack(side="left",padx=2,fill="y")

    #frame holder for all other widget and frames
        self.frame_holder=tkinter.Frame(self.parent)
        self.frame_holder.pack(side='right',expand="yes",fill="both")

    #screenshot's pixels---
        self.image_pix=None #pixel value of the screenshot
        self.pick=0

    #entryvar
        self.hex_var=tkinter.StringVar()
        self.rgb_var=tkinter.StringVar()
        self.hsl_var=tkinter.StringVar()

    #slider var
        self.s1_var=tkinter.IntVar()
        self.s2_var=tkinter.IntVar()
        self.s3_var=tkinter.IntVar()

        self.slider_mode='rgb' #slider mode : rgb or hsl, the slider value will change accordingly

    #label objects lists for future tk.label.config
        self.top_labels=[] #each contain four label objects
        self.left_labels=[]
        self.bottom_labels=[]
        self.right_labels=[]
        self.center_label=None #single label object

    #steps var, and labels
        self.steps_labels=[]
        self.step_count=15
        self.step_base_color=(176,224,230)

    #the resolution of the monitor, to make toplevel fullscreen---------------
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()
        self.tracer_win=None #tk toplevel object, future reference>destroy

    #label frame-color view---> Frame object
        self.color_view_frame=tkinter.LabelFrame(self.frame_holder,text="Color View")
        self.color_view_frame.pack(padx=2,pady=2,fill="both",expand="yes")
        tkinter.Grid.rowconfigure(self.color_view_frame,1,weight=1)
        tkinter.Grid.columnconfigure(self.color_view_frame,1,weight=1)
    #---------------------

    #color labels--------all the labels where colors will be shown
        def label_gen(row=0,column=0,incr='col'):
            labels=[]
            for i in range(4):
                temp=tkinter.Label(self.color_view_frame,text='  ',font='consolas 12',background='#b0e0e6')
                if incr=='col':
                    column=i+1
                elif incr=='row':
                    row=i+1

                temp.grid(row=row,column=column,sticky='nsew')

                labels.append(temp)
                temp.bind('<Button-1>',self.color_label_click)
            return labels

        self.top_labels=label_gen(incr='col')
        self.left_labels=label_gen(incr='row')

        self.center_label=tkinter.Label(self.color_view_frame,text='  ',font='consolas %s'%self.c_size,background='#7ec0ee')
        self.center_label.grid(row=1,column=1,columnspan=4,rowspan=4,sticky="nsew")
        self.center_label.bind('<Button-3>',self.center_color_label_click)

        self.bottom_labels=label_gen(row=6,incr='col')
        self.right_labels=label_gen(column=6,incr='row')
    #---------------------------

    #trace button- this button will initiate the toplevel, function> trace_btn_cmd
        self.trace_btn=tkinter.Button(self.frame_holder,text="Pick Color",width=20,height=1,command=self.trace_btn_cmd)
        self.trace_btn.pack(padx=2,pady=1,fill='both')
    #---------------------------

    #entry frame for three entry widget, 1.rgb 2.hsl 3.hex entry -->frame object
        self.entry_frame=tkinter.LabelFrame(self.frame_holder,text="color entry")
        self.entry_frame.pack(padx=2,fill='both')
        #---entry------
        self.rgb_ent=tkinter.Entry(self.entry_frame,width=19,font='consolas 9',textvariable=self.rgb_var)
        self.rgb_ent.pack(padx=3,pady=1,fill='both')
        self.rgb_ent.bind('<Button-3>',lambda e: self.entry_bind(self.rgb_var)) #right mouse button, copy to clipboard
        self.rgb_ent.bind('<Return>',lambda e: self.entry_return_bind(self.rgb_var)) #take user input
        self.rgb_ent.bind('<Button-1>',lambda e: self.slider_mode_entry_bind('rgb')) #change the slider mode to RGB

        self.hsl_ent=tkinter.Entry(self.entry_frame,width=19,font='consolas 9',textvariable=self.hsl_var)
        self.hsl_ent.pack(padx=3,pady=1,fill='both')
        self.hsl_ent.bind('<Button-3>',lambda e: self.entry_bind(self.hsl_var))
        self.hsl_ent.bind('<Return>',lambda e: self.entry_return_bind(self.hsl_var))
        self.hsl_ent.bind('<Button-1>',lambda e: self.slider_mode_entry_bind('hsl')) #change slider mode to hsl

        self.hex_ent=tkinter.Entry(self.entry_frame,width=19,font='consolas 9',textvariable=self.hex_var)
        self.hex_ent.pack(padx=3,pady=1,fill='both')
        self.hex_ent.bind('<Button-3>',lambda e: self.entry_bind(self.hex_var))
        self.hex_ent.bind('<Return>',lambda e: self.entry_return_bind(self.hex_var))
    #------------------

    #slider frame to hold three slider, -->frame object
        self.slider_frame=tkinter.LabelFrame(self.frame_holder,text="Slider")
        self.slider_frame.pack(padx=2,fill='both')
        #sliders----
        self.slider_1=tkinter.Scale(self.slider_frame,length=140,width=5,orient="horizontal",variable=self.s1_var,command=self.slider_change_bind)
        self.slider_1.pack(fill='both')
        self.slider_2=tkinter.Scale(self.slider_frame,length=140,width=5,orient="horizontal",variable=self.s2_var,command=self.slider_change_bind)
        self.slider_2.pack(fill='both')
        self.slider_3=tkinter.Scale(self.slider_frame,length=140,width=5,orient="horizontal",variable=self.s3_var,command=self.slider_change_bind)
        self.slider_3.pack(fill='both')
        #-------------
    #step base set button
        self.step_base_btn=tkinter.Button(self.frame_holder,text="Set Step's Base color",width=20,height=1,command=self.step_base_color_set)
        self.step_base_btn.pack(padx=2,pady=1,fill='both')

        self.__generate_steps()
    #-------------------------------
        self.slider_mode_set('rgb') #slidermode set; using self.slider_mode variable

    def __generate_steps(self): #to generate steps
        for pre_exist_labels in self.steps_labels:
            pre_exist_labels.destroy()
        self.steps_labels=[]
        for num in range(self.step_count):
            temp_label=tkinter.Label(self.steps_frame,text='  ',font='courier 16',background='#b0e0e6')
            temp_label.bind('<Button-1>',self.color_label_click)
            self.steps_labels.append(temp_label)
            temp_label.pack(expand="yes")

#end of gui-------------------------------------------------------------------------------------------------

#-----------------------------------------methods---------------------------------------------------------
    def one_func_to_rule_them_all(self,rgb): #this function hold all other function, feeding this function a RGB value will change entire interface accrordingly
        four=self.color_gen_for_labels(rgb)  #color view has four side, so four pallete of colors
        self.__label_color_changer(self.top_labels,four[0]) #changing top labels of main view [(),(),(),()]
        self.__label_color_changer(self.bottom_labels,four[1])
        self.center_label.config(background=self.rgb2hex(rgb))
        self.__label_color_changer(self.left_labels,four[2])
        self.__label_color_changer(self.right_labels,four[3])
        if self.dbp: #if color name database exist then the color view label frame text will  update
            self.colorview_text_change(rgb)
        self.entry_var_set(rgb) #entry widgets: color value set, rgb entry=rgb value, hex entry=hex value
        if self.slider_mode=='rgb' and self.pick==1: #RGB =255, so the slider need to have 250 point
            self.s1_var.set(rgb[0]) #slider 1 is Red, and setting position to given R
            self.s2_var.set(rgb[1])
            self.s3_var.set(rgb[2])
        elif self.slider_mode=='hsl' and self.pick==1: #hsl has 360,100,100. slider point will changed accordingly
            hsl=self.rgb2hsl(rgb)
            self.s1_var.set(hsl[0]) #slider 1 is Hue,
            self.s2_var.set(hsl[1])
            self.s3_var.set(hsl[2])

        self.step_labels_color_set(rgb)

#entry related function-----------------------------------
    def entry_var_set(self,rgb):
        self.rgb_var.set(str(rgb)[1:-1])
        h,s,l=self.rgb2hsl(rgb,1)
        self.hsl_var.set(str(h)+"°"+', '+str(s)+'%, '+str(l)+"%") #adding degree and %, hsl 360degree
        self.hex_var.set(self.rgb2hex(rgb))

    def slider_mode_entry_bind(self,val): #left mouse click bind, slider mode changed rgb or hsl
        if val!=self.slider_mode:
            self.slider_mode_set(val)

    def entry_bind(self,var=0): #right mouse click bind, copy to clipboard
        value=var.get()
        self.parent.clipboard_clear()
        self.parent.clipboard_append(value)

    def __random_all(self): #entry return bind random all input
        for label in self.steps_labels:
            label.config(background=self.rgb2hex(self.random_color()))
        for label in self.top_labels:
            label.config(background=self.rgb2hex(self.random_color()))
        for label in self.left_labels:
            label.config(background=self.rgb2hex(self.random_color()))
        for label in self.right_labels:
            label.config(background=self.rgb2hex(self.random_color()))
        for label in self.bottom_labels:
            label.config(background=self.rgb2hex(self.random_color()))
        self.center_label.config(background=self.rgb2hex(self.random_color()))

    def entry_return_bind(self,var=0): #enter key press bind
        value=var.get()
        self.pick=1
        if str(var)=="PY_VAR0": #if entry is self.hex_ent
            try:
                self.one_func_to_rule_them_all(self.hex2rgb(value))
            except: pass
        elif str(var)=="PY_VAR1": #if self.rgb_ent
            if value=="random":
                value=self.random_color()
            elif value=="random all":
                self.__random_all()
            elif value[:5]=="steps":
                try:
                    steps=int(value[5:])
                    self.step_count=steps
                    self.__generate_steps()
                    self.step_labels_color_set(self.hex2rgb(self.center_label.cget('background')))
                except Exception as e:
                    print(e)
            else:
                value=value.replace(" ",'')
                value=value.split(",")
            try:
                value=[int(v) for v in value]
                self.one_func_to_rule_them_all(value)
            except: pass
        elif str(var)=="PY_VAR2": #if self.hsl ent
            value=value.replace(" ",'')
            value=value.replace("%",'')
            value=value.replace("°",'')
            value=value.split(",")
            try:
                value=[int(v) for v in value]
                self.one_func_to_rule_them_all(self.hsl2rgb(value))
            except: pass
        self.pick=0
#--------------------------------------------------------------------------

#slider related functions-------------------------------------------
    def slider_change_bind(self,event): #slider changes will trigger this
        s1=self.s1_var.get() #getting value from slider 1
        s2=self.s2_var.get() #2
        s3=self.s3_var.get() #and 3
        if self.slider_mode=='rgb':
            self.one_func_to_rule_them_all((s1,s2,s3))
        elif self.slider_mode=='hsl':
            self.one_func_to_rule_them_all(self.hsl2rgb((s1,s2,s3)))
        #self.slider_frame.focus()


    def slider_mode_set(self,key):
        if key=='rgb':
            self.slider_1.config(to=255)
            self.slider_2.config(to=255)
            self.slider_3.config(to=255)
            value=self.rgb_var.get()
            if value:
                value=value.replace(" ",'')
                value=value.split(",")
            else:
                value=[0,0,0]
            try:
                value=[int(v) for v in value]
                self.s1_var.set(value[0]) #changing slider 1 position
                self.s2_var.set(value[1])
                self.s3_var.set(value[2])
                self.slider_frame.config(text="Slider- RGB")
                self.slider_mode='rgb'
            except: pass
        elif key=='hsl':
            self.slider_1.config(to=360)
            self.slider_2.config(to=100)
            self.slider_3.config(to=100)
            value=self.hsl_var.get()
            if value:
                value=value.replace(" ",'')
                value=value.replace("%",'')
                value=value.replace("°",'')
                value=value.split(",")
            else:
                value=[0,0,0]
            try:
                value=[int(v) for v in value]
                self.s1_var.set(value[0])
                self.s2_var.set(value[1])
                self.s3_var.set(value[2])
                self.slider_frame.config(text="Slider- HSL")
                self.slider_mode='hsl'
            except: pass
    #------------------------------------

#---------------color converter------------------------------------
    def rgb2hex(self,rgb):
        return '#%02x%02x%02x'%tuple(rgb)

    def rgb2hsl(self,rgb,r=0):
        rgb=[v/255.0 for v in rgb]
        h,l,s=colorsys.rgb_to_hls(*rgb)
        h=360*h #360 degree color space
        l=100*l
        s=100*s
        if r==0:
            return (h,s,l)
        else:
            return (round(h),round(s),round(l))

    def hsl2rgb(self,hsl):
        h,s,l=hsl
        h=h/360
        l=l/100
        s=s/100
        rgb=colorsys.hls_to_rgb(h,l,s)
        rgb=[round(v*255) for v in rgb]
        return rgb

    def hex2rgb(self,hex_col):
        r=int(hex_col[1:3],16)
        g=int(hex_col[3:5],16)
        b=int(hex_col[5:],16)
        return (r,g,b)


    def random_color(self):
        rgb=[]
        for i in range(3):
            rgb.append(randint(0,255))
        return rgb
#-----------------------------------------------------------

#-----related to color view frame and labels------------------
    def color_label_click(self,event=0): #mouse click event detect, to set color to big center label
        hex_col=event.widget.cget('background') #getting smaller colr label's background color
        self.pick=1 #the slider will be affected now
        self.one_func_to_rule_them_all(self.hex2rgb(hex_col))
        self.pick=0

    def center_color_label_click(self,event=0): #right mouse click copy the value to clip board hexval
        value=self.hex_var.get()
        self.parent.clipboard_clear()
        self.parent.clipboard_append(value)

    def colorview_text_change(self,rgb): #color view frame name change to color name
        hex_col=self.rgb2hex(rgb)
        col_name=self.color_name.get(hex_col,None)
        if col_name:
            self.color_view_frame.config(text="%s"%col_name[0:22])
        else:
            self.color_view_frame.config(text="Color View")

    def __label_color_changer(self,label_list,color_list=[]): #colorlist contains 4 rgb color value
        for i,label in enumerate(label_list):              #label_lists, self.top_labels,self.bottom_labels....
            label.config(background=self.rgb2hex(color_list[i]))

    #color gen for labels and label color changer works with each other to change color view frame
    #--------------------color generator-------this function generate all the colors----------------------------------
    def color_gen_for_labels(self,base_rgb): #it will take a base rgb tuple and create all color for color view labels
        h,s,l=self.rgb2hsl(base_rgb)
        def fix(v):
            return abs(v%360)

        def analogous(deg=18):
            h1=fix(h-deg*2)
            h2=fix(h-deg)
            h3=fix(h+deg)
            h4=fix(h+deg*2)
            modif_h=[h1,h2,h3,h4]
            return [self.hsl2rgb((hv,s,l)) for hv in modif_h]

        def monochrome(value=5):
            def fix_l(v):
                if v>100:
                    return 100
                elif v<0:
                    return 0
                else: return v
            l1=fix_l(l-value*2)
            l2=fix_l(l-value)
            l3=fix_l(l+value)
            l4=fix_l(l+value*2)
            modif_l=[l1,l2,l3,l4]

            return [self.hsl2rgb((h,s,lv)) for lv in modif_l]

        def triad():
            h1=fix((360/2)+h+60)#1
            h2=fix((360/2)+h) #inverted color #2
            h3=fix((360/2)+h-60)#3
            h4=fix((360/2)+h-120) #triad has three color, 1 and 2 is triad. 2 and 4 is to fill the label
            modif_h=[h1,h2,h3,h4]

            return [self.hsl2rgb((hv,s,l)) for hv in modif_h]

        def irrational(deg=137.508): #golden angel
            h1=fix(h+deg)
            h2=fix(h+deg*2)
            h3=fix(h+deg*3)
            h4=fix(h+deg*5)
            modif_h=[h1,h2,h3,h4]
            return [self.hsl2rgb((hv,s,l)) for hv in modif_h]

        return(analogous(),monochrome(),triad(),irrational())

#------------imageGrab- screenshot-----------
    def grab_image(self):
        img = ImageGrab.grab()
        self.image_pix=img.load() #making pixel list

    def get_color_from_pix(self,x,y):#x,y cordination from mouse
        return self.image_pix[x,y] #screen size and the captured imaze have same resolution. so mouse cordination from screen can be applied to get pixel value
#--------------------------------------------


#---top level----------------
    def trace_btn_cmd(self):
        self.tracer_toplevel() #top level widget
        self.trace_btn.config(text="click left mouse button",state="disable")
    def tracer_toplevel(self): #open top level window
        self.pick=1
        self.grab_image()
        self.tracer_win = tkinter.Toplevel(root)
        self.tracer_win.geometry("%dx%d"%(self.screen_width,self.screen_height)) #Whatever size
        self.tracer_win.overrideredirect(1)
        self.tracer_win.attributes('-alpha',0.003) #to make toplevel window invisible
        self.tracer_win.attributes('-topmost', True)
        self.tracer_win.bind('<Motion>',self.__motion)
        self.tracer_win.bind('<Button-1>',self.__close)

    def __motion(self,event=0):
        x = self.tracer_win.winfo_pointerx() #top level will detect mouse pointer motion
        y = self.tracer_win.winfo_pointery()
        rgb=self.get_color_from_pix(x,y)
        self.one_func_to_rule_them_all(rgb)

    def __close(self,event=0): #left mouse click will close the top level
        self.tracer_win.destroy()
        self.trace_btn.config(state="normal",text="Pick Color")
        self.pick=0
#-----------------------------------------
#---steps------------------------------
    def step_labels_color_set(self,end_color):
        def step_make(b,e,step):
            goal=abs(b-e)
            required_step=int(goal/step)
            if b<e:
                return (required_step)
            else:
                return (-required_step)
        def rgb_step():
            output=[]
            for i in range(3):
                b=self.step_base_color[i]
                e=end_color[i]
                output.append(step_make(b,e,self.step_count))
            return output

        r,g,b=rgb_step()
        begin=self.step_base_color
        for i in range(self.step_count):
            color=(begin[0]+(r*i),begin[1]+(g*i),begin[2]+(b*i))
            color='#%02x%02x%02x' % color
            self.steps_labels[i].config(bg=color)

    def step_base_color_set(self):
        try:
            rgb=self.hex2rgb(self.hex_var.get())
            self.step_base_color=rgb
            self.step_labels_color_set(rgb)
        except:
            pass





if __name__=="__main__":
    root=tkinter.Tk()
    ui=Main_UI(root)
    ui.mainloop()
