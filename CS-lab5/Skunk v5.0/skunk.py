import json
import subprocess
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
querry = StringVar()

success = []
fail = []
unknown = []

toChange=[]
vars2=StringVar()
arr2=[]
arr2copy=[]

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

def search():
    global structure
    q = querry.get()
    arr = [struct['description'] for struct in structure if q.lower() in struct['description'].lower()]
    global matching
    matching = [struct for struct in structure if q in struct['description']]
    vars.set(arr)

def select_all():
    lstbox.select_set(0, END)
    for struct in structure:
        lstbox.insert(END, struct)

def deselect_all():
    for struct in structure:
        lstbox.selection_clear(0, END)

def make_query(struct):
    query = 'reg query ' + struct ['reg_key'] + ' /v ' + struct ['reg_item']
    out = subprocess.Popen(query,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    output = out.communicate() [0].decode('ascii', 'ignore')
    str = ''
    for char in output:
        if char.isprintable() and char != '\n' and char != '\r':
            str += char
    output = str
    output = output.split(' ')
    output = [x for x in output if len(x) > 0]
    value = ''
    if 'ERROR' in output [0]:
        unknown.append(struct ['reg_key'] + struct['reg_item'])
    for i in range(len(output)):
        if 'REG_' in output [i]:
            for element in output [i + 1:]:
                value = value + element + ' '
            value = value [:len(value) - 1]
            if struct ['value_data'] [:2] == '0x':
                struct ['value_data'] = struct ['value_data'] [2:]
            struct ['value_data'] = hex(int(struct ['value_data']))
            p = re.compile('.*' + struct ['value_data'] + '.*')
            if p.match(value):
                print('Patern:', struct ['value_data'])
                print('Value:', value)
                success.append(struct ['reg_key'] + struct ['reg_item'] + '\n' + 'Value:' + value)
            else:
                print('Did not pass: ', struct ['value_data'])
                print('Value which did not pass: ', value)
                fail.append([struct, value])

def check():

    for struct in structure:
        if 'reg_key' in struct and 'reg_item' in struct and 'value_data' in struct:
            make_query(struct)

    for i in range(len(fail)):
        item=fail[i]
        arr2.append(' Item:' + item[0]['reg_item'] + ' Value:' + item[1] + ' Desired:' + item[0]['value_data'])
        global arr2copy
        arr2copy=arr2
    vars2.set(arr2)

def changeFailures():
    global arr2copy
    global arr2
    backup()
    for i in range(len(failedselected)):
        struct=failedselected[i][0]
        query = 'reg add "' + struct ['reg_key'] + '" /v ' + struct ['reg_item'] +' /d "'+ struct['value_data']+ '" /f'
        print(query)
        out = subprocess.Popen(query,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        output = out.communicate() [0].decode('ascii', 'ignore')
        str = ''
        for char in output:
            if char.isprintable() and char != '\n' and char != '\r':
                str += char
        output = str
        print(output)
        vars2.set(arr2)
        arr2copy=arr2

def restore():
    f=open('backup.txt')
    fail=json.loads(f.read())
    print(fail)
    f.close()

    for i in range(len(fail)):
        struct=fail[i][0]
        query = 'reg add ' + struct ['reg_key'] + ' /v ' + struct ['reg_item'] +' /d '+ fail[i][1]+ ' /f'
        print('Query:',query)
        out = subprocess.Popen(query,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        output = out.communicate() [0].decode('ascii', 'ignore')
        str = ''
        for char in output:
            if char.isprintable() and char != '\n' and char != '\r':
                str += char
        output = str
        print(output)


def backup():
    f=open('backup.txt','w')
    backupString=json.dumps(fail)
    f.write(backupString)
    f.close()

def on_select_failed(evt):
    w = evt.widget
    actual = w.curselection()

    global failedselected
    global arr2
    failedselected=[]
    for i in actual:
        failedselected.append(fail[i])
    localarr2=[]
    for i in actual:
        localarr2.append(arr2copy[i])
    arr2=localarr2
    arr2=[x for x in arr2copy if x not in arr2]
    print(failedselected)


# **************************************************************************

myFont = Font(family="Helvetica", size=14)

mainframe = Frame(main, width=1200, height=20)
mainframe.grid(row=0, column=0)

frame1 = Frame(mainframe, pady=40, width=1200, height=10)
frame1.grid(row=0, column=0, sticky=N)

Label(frame1, text="Audit Policies Compiler", font="Helvetica 20 bold").grid(row=0, column=0, sticky=N)

frame2 = Frame(mainframe, width=1200, height=10)
frame2.grid(row=1, column=0, sticky=NW)

lstbox = Listbox(frame2, bg="#2e2e2e", font=myFont, fg="white", listvariable=vars, selectmode=MULTIPLE,
                 height=6, width=107)
lstbox.config(highlightbackground="black")
lstbox.grid(row=0, column=0, padx=10, pady=1, sticky=W)
lstbox.bind('<<ListboxSelect>>', on_select_configuration)

frame3 = Frame(mainframe)
frame3.grid(row=2, column=0, sticky=NW)

text = Text(frame3, bg="#e3e3e3", fg="black", font=myFont, height=6, width=107)
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
global e
e = Entry(frame4, bg="#ffe4d1", font=myFont, width=30, textvariable=querry).grid(row=1, column=0, sticky=NSEW, padx=10, pady=5)
search_button = Button(frame4, bg="#ffffff", fg="black", font=myFont, text="Search", width=7, height=1,
                       command=search).grid(row=1, column=1, sticky=NSEW, padx=10, pady=5)
selectAllButton = Button(frame4, bg="#4B4B4B", fg="white", font=myFont, text="Select All", width=7, height=1,
                         command=select_all).grid(row=2, column=0, sticky=NSEW, padx=10, pady=5)
deselectAllButton = Button(frame4, bg="#4B4B4B", fg="white", font=myFont, text="Deselect All", width=10, height=1,
                           command=deselect_all).grid(row=2, column=1, sticky=NSEW, padx=10, pady=5)

frame5 = Frame(mainframe, padx=10, pady=20, width=1200, height=6, bg="#9B1723")
frame5.grid(row=4, column=0, sticky=SW)
frame5.columnconfigure(0, weight=1)
frame5.columnconfigure(1, weight=1)
frame5.columnconfigure(2, weight=1)
frame5.columnconfigure(3, weight=1)

text2 = Text(frame5, bg="#bdbfff", font=myFont, width=50, height=1).grid(row=0, column=0, sticky=NSEW, padx=10, pady=5)
text2.insert(END, '\n\n'.join(success))

changeButton = Button(frame5, text='Change', command=changeFailures, bg="#300000", font=myFont, width=10, height=1).grid(row=0, column=1, sticky=NSEW, padx=10, pady=5)

listbox_fail = Listbox(frame2, bg="#bdbfff", font=myFont, listvariable=vars2, selectmode=MULTIPLE, width=50, height=1).grid(row=0, column=2, sticky=NSEW, padx=10, pady=5)
listbox_fail.bind('<<ListboxSelect>>', on_select_failed)

restoreButton = Button(frame5, text='Restore', command=restore, bg="#300000", font=myFont, width=10, height=1).grid(row=0, column=3, sticky=NSEW, padx=10, pady=5)

main.mainloop()
