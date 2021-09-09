import glob
import json
import subprocess
import tarfile
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font
import requests
import parse_audit
import re

global previous
main = Tk()
myFont = Font(family="Cambria", size=14)
s = ttk.Style()
s.configure('TFrame', background='#413F3E')
main.title("Skunk SBT")
main.geometry("1900x1000")
frame = ttk.Frame(main, width=1900, height=1000, style='TFrame', padding=(4, 4, 450, 450))
frame.grid(column=0, row=0)
previous = []
index = 0
arr = []
matching = []

SystemDict = {}
querry = StringVar()
vars = StringVar()
tofile = []
structure = []

success = []
fail = []
unknown = []

toChange=[]
vars2=StringVar()
arr2=[]
arr2copy=[]

failedselected=[]

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
        unknown.append(struct ['reg_key'] + struct ['reg_item'])
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



def entersearch(evt):
    search()


def search():
    global structure
    q = querry.get()
    arr = [struct['description'] for struct in structure if q.lower() in struct['description'].lower()]
    global matching
    matching = [struct for struct in structure if q in struct['description']]
    vars.set(arr)


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


lstbox = Listbox(frame, bg="#2e2e2e", font=myFont, fg="white", listvariable=vars, selectmode=MULTIPLE, width=130,
                 height=29, highlightthickness=1)
lstbox.config(highlightbackground="black")
lstbox.grid(row=0, column=0, columnspan=3, padx=10, pady=160)
lstbox.bind('<<ListboxSelect>>', on_select_configuration)


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


def select_all():
    lstbox.select_set(0, END)
    for struct in structure:
        lstbox.insert(END, struct)


def deselect_all():
    for struct in structure:
        lstbox.selection_clear(0, END)


def download_url(url, save_path, chunk_size=1024):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def extract_download():
    url = "https://www.tenable.com/downloads/api/v1/public/pages/download-all-compliance-audit-files/downloads/7472/download?i_agree_to_tenable_license_agreement=true"
    path = "audits.tar.gz"
    download_url(url, path)
    tf = tarfile.open("audits.tar.gz")
    tf.extractall()
    print(glob.glob("portal_audits/*"))


text = Text(frame, bg="#e3e3e3", fg="black", font=myFont, width=36, height=40, highlightthickness=1)
text.config(highlightbackground="black")
text.grid(row=0, column=3, columnspan=3, padx=30)
import_button = Button(frame, bg="#9B1723", fg="white", font=myFont, text="Import", width=7, height=1,
                       command=import_audit).place(relx=0.005, rely=0.849)
saveButton = Button(frame, bg="#041D7E", fg="white", font=myFont, text="Save As", width=12, height=1,
                    command=save_config).place(relx=0.136, rely=0.849)
selectAllButton = Button(frame, bg="#252020", fg="white", font=myFont, text="Select All", width=8, height=1,
                         command=select_all).place(relx=0.646, rely=0.849)
deselectAllButton = Button(frame, bg="#252020", fg="white", font=myFont, text="Deselect All", width=10, height=1,
                           command=deselect_all).place(relx=0.696, rely=0.849)
downloadButton = Button(frame, bg="#9B1723", fg="white", font=myFont, text="Download policies", width=15, height=1,
                        command=extract_download).place(relx=0.05, rely=0.849)
global e
e = Entry(frame, bg="white", font=myFont, width=30, textvariable=querry).place(relx=0.533, rely=0.917)
search_button = Button(frame, bg="#413F3E", fg="white", font=myFont, text="Search", width=7, height=1,
                       command=search).place(relx=0.711, rely=0.910)

main.bind('<Return>', entersearch)
main.mainloop()
