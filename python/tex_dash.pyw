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
        
        self.clear_all_button = Button(self, text = 'Clear all (Ctrl-A)', command = clear_all)
        self.clear_all_button.pack()
        

def clear_all():
    text1.delete('1.0', END)

def copy_to_clipboard():
    root.clipboard_clear()
    txt = text2.get('1.0', END)
    root.clipboard_append(txt)

def process_text(event = None):
    txt = text1.get('1.0', END)
    new_txt = delete_newlines_and_hyphens(txt)
    new_txt = preprocess_sym(new_txt)
    text2.delete('1.0', END)
    text2.insert('1.0', new_txt)
    
def preprocess_sym(txt):
    new_txt = ''
    cnt = 0 # Четная - открываюшая
    for i in range(0, len(txt)):
        if txt[i] == '"' or txt[i] == '“' or txt[i] == '”':
            cnt += 1
            if cnt % 2 == 1:
                new_txt += '<<'
            else:
                new_txt += '>>'
        elif (txt[i] == '\u002d' or txt[i] == '\u2013' and
            i != 0 and i != len(txt) - 1 and txt[i - 1] == ' ' and txt[i + 1] == ' '):
                new_txt += '"---'
        elif txt[i] == '№': #textcomp package
            new_txt += '\\textnumero'
        else:
            new_txt += txt[i]    
            
    return new_txt        

def delete_newlines_and_hyphens(txt):
    new_txt = ''
    prev_ind = 0
    ind = txt.find('\n')
    while ind != -1:
        if ind != 0 and txt[ind - 1] == '\u002d': 
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

text1 = ScrolledText(root, height = 10, width = 90, font = 'Consolas 10', wrap = WORD)
text2 = ScrolledText(root, height = 10, width = 90, font = 'Consolas 10', wrap = WORD)

text1.bind('<Control-d>', process_text)
text1.bind('<Control-a>', clear_all)

ButtonsFrame(root).pack(side = RIGHT, anchor = N)
text1.pack(side = TOP, expand = YES, fill = BOTH)
text2.pack(side = BOTTOM, expand = YES, fill = BOTH)

root.mainloop()
