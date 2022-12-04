# import modules
from tkinter import *
from par_lyr import SongTitle

# 006ccf95329444616
# AIzaSyCoz2ZFPaBxvU1Yqh0VrYqru5pxUGRyFBI

# user defined function


def get_name():
    extract_song_name = SongTitle("AIzaSyCoz2ZFPaBxvU1Yqh0VrYqru5pxUGRyFBI", "006ccf95329444616")
    temp = extract_song_name.get_song_name(str(e.get()))
    res_name = temp['song_name']
    result_name.set(res_name)
    

# object of tkinter and background set to light grey
master = Tk()
master.configure(bg='light grey')

# Variable Classes in tkinter
result_name = StringVar()

# Creating label for each information name using widget Label
Label(master, text="Enter lyrics : ", bg="light grey").grid(row=0, sticky=W)
Label(master, text="Result : ", bg="light grey").grid(row=3, sticky=W)

# Creating label for class variable name using widget Entry
Label(master, text="", textvariable=result_name, bg="light grey").grid(row=3, column=1, sticky=W)
# Label(master, text=f'{result_name}', bg="light grey").grid(row=0, column=1, sticky=W)
e = Entry(master, width=50)
e.grid(row=0, column=1)

# creating a button using the widget
b = Button(master, text="show", command=get_name, bg="Blue")

b.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=5,)

mainloop()
