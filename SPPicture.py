#file	-	SPPicture.py
#pack	-	SPPicture
#ver	- 	1.0
#since 	-	6.4.16
#author	-	Spalynx

''' SPPicture.py
#    This program allows a user to put up a floating resizable image,
#     that can be forced to stay above other programs, and act in full screen
#     mode. Note, this program can stay above windowed games, not full screen.
'''
import tkinter as tk
from PIL import Image, ImageTk
root = tk.Tk()

#TODO: Should probably refactor this to a dictionary. Namespace clashes!
#-------------------------- Globals ------------------------------
W_Width,W_Height =300,300;          #(int, int)     -> The Bounds of the main window of the program.
full = False; top = False;          #(bool, bool)   -> Switches for the program; If full or top are true, the program goes full screen and always top level.
previous = "";  current = "";       #(Str, Photo)   -> Image storage, so if the imageloading fails, there are backups.
buttons = [];                       #(list[photo])  -> Because of the ImageTk GC bug, this is a store of the button images.
ZW,ZH = 300,300;                    #(int, int)     -> Zoom widht/height, is reset on window resize.
coords = {"lastx":0, "lasty":0, "i_x":0, "i_y":0};

#--------------- Mutators ------------------------------------
def set_coords():
    c = canvas.coords(canvas.find_withtag("IMAGE"))
    coords["i_x"], coords["i_y"] = c[0], c[1];  #UPDATE COORDS
def set_full():
    '''Sets the program to a psuedo-fullscreen, taskbar buttons dissappear.'''
    global full;
    
    full = False if full else True; #flip/flop (bool) full
    root.overrideredirect(full);    #uses Tk.overrideredirect();
def set_top():
    ''' A flip/flop switch for whether the program stays above other programs. '''
    global top;
    
    if (top):       #sets it persistant top level
        root.title("[T]SPPicture V1");
        root.after(1000,root.call('wm','attributes','.','-topmost',True));
    else:           #resets it to not stay on top level.
        root.title("SPPicture V1");
        root.call('wm','attributes','.','-topmost',False)
    #Flips the value of top.
    top = False if top else True;

#-------------- Accessor ------------------------------
def get_img(browse=True): #browse = false is for setting picture in certain cases.
    '''Obtains image filename from user, and creates an image object for later use.'''
    global previous, current;
    filename = "";
    
    if(browse): #If browse is true it allows the user to browse for a file.
        from tkinter import filedialog
        filename = filedialog.askopenfilename(filetypes =(("Image Files", "*.jpeg;*.jpg;*.png;*.bmp")
                                                            ,("Jpeg", "*.jpeg;*.jpg")
                                                            ,("Png", "*.png")
                                                            ,("Bitmap", "*.bmp")
                                                            ,("All files", "*.*") ))
    try:
        if(filename != ""):         #if a file is given, it setsh the photo to set.
            photo = ImageTk.PhotoImage(file = filename);
            previous = filename;    #filling previous with current.
            current = photo;
        elif(previous != ""):       #if file isnt given, but something is previously defined, sets to previous.
            photo = ImageTk.PhotoImage(file = previous);
            current = photo;
        #Called on init, and error cases.
        else:   #no filename/no previous -> sets to splash screen.
            previous = "data/Splash.png";
            photo = ImageTk.PhotoImage(file = previous);
            current = photo;
            print("No photo given.");
    except:
        print("Processing of image failed.");

#------------------ Drawing Functions -----------------------
def draw_img(zoom = False, x = 0, y = 0):
    '''Draws the image to the canvas.'''
    if (current == None):   #No image? Nope!
        return;

    #deleting buttons for redraw
    canvas.delete(canvas.find_withtag("img"));
    canvas.delete(canvas.find_withtag("full"));
    canvas.delete(canvas.find_withtag("top"));

    #Zoom centers the image based upon the cursor, !zoom draws at origin.
    if(not zoom):
        canvas.create_image(x,y, image = current, anchor = tk.NW, tag = "IMAGE");
    if(zoom):
        canvas.create_image(x,y, image = current, anchor = tk.CENTER, tag = "IMAGE")
    draw_buttons();                         #redraw buttons, they were deleted 6 lines ago. 
def draw_resized(event=None):
    '''Draws the image to screen, it's size based upon set width and height.'''
    global W_Width, W_Height, previous, current, ZW, ZH;
    ZW, ZH = W_Width, W_Height;
    
    if (previous == "" or current == ""):   #exit if no image
        return
    if (event != None):                     #If it isn't an event, don't gather width/height
        W_Width, W_Height = event.width, event.height;
        
    canvas.delete("IMAGE");                 #Deletes drawn image, for redraw.
    
    #Creates new image based upon previous, and resizes image
    im = Image.open(previous);              #open.
    res_im = im.resize((W_Width, W_Height), Image.ANTIALIAS);   #resize.
    current = ImageTk.PhotoImage(res_im);   #draw image.
    draw_img();
def draw_buttons():
    ''' Draws buttons to screen. The buttons images with mouse events at their coords.
    Full -> Removes the border from the program.
    Img  -> Allows the user to select an image.
    Top  -> Toggles whether the image is always on top or not.          '''
    
    global buttons;

    #Draw all three buttons with their given images to the screen.
    canvas.create_text(7,7, fill = "white", activefill = "black", text = "F", anchor = tk.CENTER, tag = "full");
    canvas.create_text(23,7, fill = "white", activefill = "black", text = "I", anchor = tk.CENTER, tag = "img");
    canvas.create_text(W_Width-7,7, fill = "white", activefill = "black", text = "T", anchor = tk.CENTER, tag = "top");

#------------------ Event handlers --------------------------
def click (event):
    '''Event handler for mouse button down.'''
    global img; global col;
    x = event.x;    y = event.y;

    #Button animations for mouse click down at given coords.
    img = None;
    if(x > 0 and x < 15 and y > 0 and y < 15):          #Full
        img = canvas.find_withtag("full"); col = 0;
        set_full(); #Sets fullscreen, removes border.
        
    if(x > 15 and x < 30 and y > 0 and y < 15):         #Img
        img = canvas.find_withtag("img"); col = 1;
        get_img(); draw_resized(None); #Resizes and draws img.
        
    if(x > W_Width-15 and x < W_Width and y > 0 and y < 15):#Top
        img = canvas.find_withtag("top"); col = 2;
        set_top(); #Sets window to always top
    canvas.itemconfigure(img, text = "+");
def click_release (event):
    ''' Mouse release event, just resets the button image. '''
    global img;
    x,y = event.x, event.y;
    if(y > 0 and y < 10):       #If it's within a certain y bound.
       if((x > 0 and x < 30) or (x > W_Width-15 and x < W_Width)): #and 3 x bound areas.
           canvas.itemconfigure(img, text=buttons[col]);   #reset the button image.
def zoom_img(event):
    ''' Event handler for <ctrl-scroll>  redraws image with 50 px of zoom.'''
    global W_Width, W_Height, previous, current, ZW, ZH, coords;
    zoomin = False;
    
    #If eventtype is 2, checks for keypresses.
    if(int(event.type) == 2):
        if(event.keysym == "minus"):
            zoomin = False;
        elif(event.keysym == "equal"):
            zoomin = True;
        else: return;
    #otherwise it's a scrollwheel event.
    else:
        if(event.delta < 0):
            zoomin = False;
        elif(event.delta >= 0):
            zoomin = True;
        else: return;
        
    #Displacement of 50px is added to zoom width and height.
    if(zoomin):
        ZW += 50;
        ZH += 50;
    else:
        ZW -= 50;
        ZH -= 50;
        
    canvas.delete("IMAGE")  #Deletes previous image.

    #image too small to resize
    if((ZW < 1 or ZH < 1) and (zoomin)):
        ZW, ZH = 0, 0;
        return;
    
    #Image is redrawn based upon zoom w/h.
    im = Image.open(previous);
    res_im = im.resize((ZW, ZH), Image.ANTIALIAS)
    current = ImageTk.PhotoImage(res_im);

    #resizes based upon the input type.
    if(int(event.type) == 2):               #Keypress   -> Resizes at center.
        if(zoomin):
            coords["i_x"] -= 50; coords["i_y"] -= 50; 
        else:
            coords["i_x"] += 50; coords["i_y"] += 50;
        draw_img(False,coords["i_x"],coords["i_y"]);
    else:
        #mouse_x - Zoomed width/2
        coords["i_x"] = event.x - ZW/2; coords["i_y"] = event.y - ZH/2;
        draw_img(True, event.x, event.y);   #Scroll     -> Resizes at mouse.
def mvmt_event(event):
    coords["lastx"], coords["lasty"] = event.x, event.y;
def drag_img(event):
    global coords;
    dx,dy = 0, 0;

    #Check mouse displacement, to see how much to move.
    if(event.x != coords["lastx"]):
        dx = event.x - coords["lastx"];
    if(event.y != coords["lasty"]):
        dy = event.y - coords["lasty"];
    #shouldn't happen, considering this is a motion based event.
    if(dx == 0 and dy == 0):
        return;

    coords["lastx"], coords["lasty"] = event.x, event.y;

    canvas.delete("IMAGE");
    draw_img(False, coords["i_x"]+dx, coords["i_y"]+dy);
    set_coords();
def key_event(event):
    print(event.keysym);
    if(event.keysym == 'F' or event.keysym == 'f'):
        set_full();
    elif(event.keysym == 'I' or event.keysym == 'i'):
        get_img(); draw_resized(None);
    elif(event.keysym == 'T' or event.keysym == 't'):
        set_top();
    else: return;


#=================== Main Program ===========================
import sys;

#Image argument invoked and passed to draw.
if (len(sys.argv) >= 2):
    previous = sys.argv[1];

root.title("SPPicture V1");              #initialize root.    
root.resizable(1,1);

canvas = tk.Canvas(root, width=W_Width, height=W_Height, background = "black");

#Adding button images to the buttons list.
buttons.append('F');
buttons.append('I');
buttons.append("V");

#Draw items to the canvas.
draw_buttons();
get_img(False); draw_resized(None);

#Event handlers for the functionality of the program.
canvas.bind("<Button-1>", click);
canvas.bind("<ButtonRelease-1>", click_release);
canvas.bind("<B1-Motion>", drag_img);
canvas.bind("<Motion>", mvmt_event);


canvas.bind("<Configure>", draw_resized);

canvas.bind("<Control-MouseWheel>", zoom_img)
root.bind("<Key>", key_event)
root.bind("<Control-minus>", zoom_img);
root.bind("<Control-equal>", zoom_img);

#Throw canvas onto the screen.
canvas.pack(fill=tk.BOTH,expand=1);

#Automatically brings the window to top level.
set_top();
root.mainloop()
