import sys

from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import *

class ButtonsFrame(Frame):
    def __init__(self, parent = None):
        Frame.__init__(self, parent)
        #self.pack()
        self.make_widgets()
    
    def make_widgets(self):
        self.delete_newlines_button = Button(self, text = 'Delete newlines (Ctrl-D)', command = process_text)
        self.delete_newlines_button.pack()  
        
        self.copy_button = Button(self, text = 'Copy to the clipboard', command = copy_to_clipboard)
        self.copy_button.pack()
        

def copy_to_clipboard():
    root.clipboard_clear()
    txt = text2.get('1.0', END)
    root.clipboard_append(txt)

def process_text(event = None):
    txt = text1.get('1.0', END)
    new_txt = delete_newlines_and_dashes(txt)
    text2.delete('1.0', END)
    text2.insert('1.0', new_txt)
    
def delete_newlines_and_dashes(txt):
    new_txt = ''
    prev_ind = 0
    ind = txt.find('\n')
    while ind != -1:
        if ind != 0 and txt[ind - 1] == '-': 
            new_txt = ''.join([new_txt, txt[prev_ind:ind - 1]])
        elif ind != 0 and txt[ind - 1].isspace():
            new_txt = ''.join([new_txt, txt[prev_ind:ind - 1], ' '])
        else:
            new_txt = ''.join([new_txt, txt[prev_ind:ind], ' '])
        prev_ind = ind + 1
        if txt[ind + 1:].find('\n') != -1:
            ind = ind + 1 + txt[ind + 1:].find('\n')
        else:
            ind = -1
    new_txt = ''.join([new_txt, txt[prev_ind:]])
    return new_txt

root = Tk()
root.title('tex_dash.pyw')

text1 = ScrolledText(root, height = 10, width = 90, font = 'Arial 14', wrap = WORD)
text2 = ScrolledText(root, height = 10, width = 90, font = 'Arial 14', wrap = WORD)

text1.bind('<Control-d>', process_text)

ButtonsFrame(root).pack(side = RIGHT, anchor = N)
text1.pack(side = TOP, expand = YES, fill = BOTH)
text2.pack(side = BOTTOM, expand = YES, fill = BOTH)

root.mainloop()