import json
from tkinter import *
from tkinter import filedialog as fd
from tkinter.font import Font
import parse_audit

global previous
main = Tk()
main.title("Skunk SBT")
main.geometry("1200x700")
main.resizable(0, 0)


previous = []
index = 0
arr = []
matching = []
vars = StringVar()
tofile = []
structure = []

def on_select_configuration(evt):
    global previous
    global index
    w = evt.widget
    actual = w.curselection()

    difference = [item for item in actual if item not in previous]
    if len(difference) > 0:
        index = [item for item in actual if item not in previous][0]
    previous = w.curselection()

    text.delete(1.0, END)
    str = '\n'
    for key in matching[index]:
        str += key + ':' + matching[index][key] + '\n'
    text.insert(END, str)

def import_audit():
    global arr
    file_name = fd.askopenfilename(initialdir="../portal_audits")
    if file_name:
        arr = []
    global structure
    structure = parse_audit.main(file_name)
    for element in structure:
        for key in element:
            str = ''
            for char in element[key]:
                if char != '"' and char != "'":
                    str += char
            isspacefirst = True
            str2 = ''
            for char in str:
                if char == ' ' and isspacefirst:
                    continue
                else:
                    str2 += char
                    isspacefirst = False
            element[key] = str2

    global matching
    matching = structure
    if len(structure) == 0:
        f = open(file_name, 'r')
        structure = json.loads(f.read())
        f.close()
    for struct in structure:
        if 'description' in struct:
            arr.append(struct['description'])
        else:
            arr.append('Error in selecting')
    vars.set(arr)

def save_config():
    file_name = fd.asksaveasfilename(filetypes=(("Audit FILES", ".audit"),
                                                ("All files", ".")))
    file_name += '.audit'
    file = open(file_name, 'w')
    selection = lstbox.curselection()
    for i in selection:
        tofile.append(matching[i])
    json.dump(tofile, file)
    file.close()

myFont = Font(family="Helvetica", size=14)

mainframe = Frame(main, width=1200, height=20)
mainframe.grid(row=0, column=0)

frame1 = Frame(mainframe, pady=40, width=1200, height=20)
frame1.grid(row=0, column=0, sticky=N)

Label(frame1, text="Audit Policies Compiler", font="Helvetica 20 bold").grid(row=0, column=0, sticky=N)

frame2 = Frame(mainframe, width=1200, height=10)
frame2.grid(row=1, column=0, sticky=NW)

lstbox = Listbox(frame2, bg="#2e2e2e", font=myFont, fg="white", listvariable=vars, selectmode=MULTIPLE,
                 height=10, width=107)
lstbox.config(highlightbackground="black")
lstbox.grid(row=0, column=0, padx=10, pady=1, sticky=W)
lstbox.bind('<<ListboxSelect>>', on_select_configuration)

frame3 = Frame(mainframe)
frame3.grid(row=2, column=0, sticky=NW)

text = Text(frame3, bg="#e3e3e3", fg="black", font=myFont, height=10, width=107)
text.config(highlightbackground="black")
text.grid(row=0, column=0, padx=10, pady=5, sticky=W)

frame4 = Frame(mainframe, padx=10, pady=20, width=1200, height=10)
frame4.grid(row=3, column=0, sticky=NSEW)
frame4.columnconfigure(0, weight=1)
frame4.columnconfigure(1, weight=1)

import_button = Button(frame4, bg="#9B1723", fg="white", font=myFont, text="Import", width=7, height=1,
                       command=import_audit).grid(row=0, column=0, sticky=NSEW, padx=10)
saveButton = Button(frame4, bg="#041D7E", fg="white", font=myFont, text="Save As", width=12, height=1,
                    command=save_config).grid(row=0, column=1, sticky=NSEW, padx=10)

main.mainloop()
