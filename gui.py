
import Tkinter
from Tkinter import *
import script
from PIL import Image, ImageTk, ImageFile
import os
import shutil
import ConfigParser,io


# Main Functions
def main():
    # Global Vars
    global outputStack
    global alternateStack
    global head
    global root
    global cv
    global topimg
    global imagelist
    global imagelist_p
    global startup
    # setup
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    outputStack = []
    alternateStack = []
    head = None
    # create window
    root = Tkinter.Tk(className=" MugiPruner ")
    root.geometry("750x750")
    root.tk.call('wm','iconphoto', root._w, tk_image(r'.\img\mugicon.bmp',32,32))
    # create canvas
    cv = Canvas(root)
    cv.pack(expand="yes", fill="both")
    # populate list

    imagelist = script.get_list()
    imagelist_p = []
    #fill gui
    all_function_trigger(cv)
    topimg= Label(cv, image=None, borderwidth=5, bg="#f4a9c9")
    # load images to index
    startup = "true"
    for i in range(Index):
        next_image(cv)
    startup="false"
    next_image(cv)

    root.mainloop()
    return

def background(self):
    background_image = tk_image(r".\img\mugipruner.png",750,750)
    background_label = Label(self, image=background_image)
    background_label.place(x=0, y=0)
    background_label.image = background_image


def show_image(path):
    img = tk_image(path, 500, 500)
    cv.delete(cv.find_withtag("curr"))
    #cv.allready = cv.create_image(375, 375, image=img,
    #                                  anchor='center', tag="curr")
    topimg.configure(image=img)
    topimg.image = img
    topimg.place(x=375, y=357, anchor='center')

    cv.image = img
    #print self.find_withtag("curr")
    total = len(imagelist) + len(imagelist_p)
    strin = "[" + str(total - len(imagelist)) + "/" + str(total) + "]"
    cv.master.title(" MugiPruner {} - ({})".format(strin,os.path.basename(path).encode('utf-8')))
    return

def previous_image(self,event=None):
    try:
        global head

        if imagelist_p:
            imagelist.append(head)
            pop = imagelist_p.pop()
            show_image(pop)
            head = pop
        else:
            print("End of the line!")
    except IndexError as e:
        self.show_image(r".\img\noimagesleft.png")

    #print(self.imagelist)
    #print(self.imagelist_p)
    return
def favorite_image(self,event=None):
    global head
    try:
        shutil.copy(head, FavoriteDir + "\\" + os.path.basename(head))
        if imagelist:
            if head != None:
                imagelist_p.append(head)
            pop = imagelist.pop()
            head = pop
            show_image(pop)
        else:
            print("End of the line")

    except IndexError as e:
        self.show_image(r".\img\noimagesleft.png")
    return

def move_image(val,event=None):
    global head
    try:
        if val==1:
            outputStack.append(head)
        elif val==2:
            alternateStack.append(head)
        pop = imagelist.pop()
        head = pop
        show_image(pop)

    except IndexError as e:
        show_image(r".\img\noimagesleft.png")
    return

def next_image(self,event=None):
    global head
    global startup
    try:
        if imagelist:
            if head != None:
                imagelist_p.append(head)
            pop = imagelist.pop()
            head = pop
            if startup == "false":
                show_image(pop)
        else:
            print("End of the line")

    except IndexError as e:
        show_image(r".\img\noimagesleft.png")
    #print(outputStack)
    #print(self.imagelist)
    #print(self.imagelist_p)
    return

def all_function_trigger(self):
    background(self)
    create_buttons(self)
    window_settings(self)
    self.master.bind('<Right>', next_image)
    self.master.bind('<space>', movehelper)
    self.master.bind('<Up>', movehelper)
    self.master.bind('<Down>', movehelperalt)
    self.master.bind('<Left>', previous_image)
    self.master.bind('f', favorite_image)
    return

def movehelper(self, event=None):
    move_image(1)

def movehelperalt(self, event=None):
    move_image(2)

def window_settings(self):
    self['width'] = self.winfo_screenwidth()
    self['height'] = self.winfo_screenheight()
    return

def create_buttons(self):
    self.img = tk_image(r".\img\saveandexit.png",125,125)
    Tkinter.Button(self,command=finish,image=self.img,borderwidth=0, highlightthickness=0).place(anchor="center", x=642,y=682)
    #Tkinter.Button(self,text=" KEEP ",height="5",width="20", command=next_image).place(x=(210),
      #                                                              y=(650))
    #Tkinter.Button(self, text=" MOVE ",height="5",width="20", command=movehelper).place(x=(375),
      #                                                              y=(650))
    #Tkinter.Button(self, text="Finish",height="5",width="20", command=finish).place(x=(282),
       #                                                             y=(10))
    #Tkinter.Button(self, text="Prev", height="5", width="20", command=previous_image).place(x=(10),
         #                                                                                  y=(375))
    return

def finish():
    while outputStack:
        pop = outputStack.pop()
        os.rename(pop,OutputDir+"\\"+os.path.basename(pop))
    while alternateStack:
        pop = alternateStack.pop()
        os.rename(pop,AlternateDir+"\\"+os.path.basename(pop))
    root.destroy()
    total = len(imagelist) + len(imagelist_p)
    strin = "[" + str(total - len(imagelist)) + "/" + str(total) + "]"
    config.set('config','Index',total - len(imagelist))
    cfgo = open("config.ini", 'w')
    config.write(cfgo)
    cfgo.close()
    print(strin)

def tk_image(path,w,h):
 img = Image.open(path)
 img = img.resize((w,h))
 storeobj = ImageTk.PhotoImage(img)
 return storeobj

# Main Function Trigger
if __name__ == '__main__':
    # load config file
    with open("config.ini") as f:
        sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    Index = config.getint('config','Index')
    FavoriteDir = config.get('config','FavoriteDir')
    AlternateDir = config.get('config','AlternateDir')
    OutputDir = config.get('config','OutputDir')

    main()