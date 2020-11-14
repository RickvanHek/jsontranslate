import errno
import glob
import json
import os
import tkinter as tk
from tkinter import filedialog

from googletrans import Translator

translator = Translator()

excluded_keys = ["url", "tel"]


def translate_dict(d, u, src, dest):
    for k, v in u.items():
        if k in excluded_keys:
            continue
        if isinstance(v, dict):
            d[k] = translate_dict(d.get(k, {}), v, src, dest)
        else:
            try:
                translation = translator.translate(v, src=src, dest=dest)
                d[k] = translation.text
            except Exception as e:
                print(e)
    return d


def main():
    print("Translating from: " + originalLanguage.get() + " to: " + targetLanguage.get())
    for filename in glob.glob(os.path.join(folder_path.get(), originalLanguage.get(), '*.json')):
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            outputFilename = os.path.join(folder_path.get(), targetLanguage.get(), os.path.basename(filename))
            if not os.path.exists(os.path.dirname(outputFilename)):
                try:
                    os.makedirs(os.path.dirname(outputFilename))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            result = json.load(currentFile)
            with open(outputFilename, 'w') as outfile:
                print(filename)
                res = translate_dict(result, result, src=originalLanguage.get(), dest=targetLanguage.get())
                json.dump(res, outfile)


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)


master = tk.Tk()
master.title("Translator")

tk.Label(master, text="Select root folder").grid(row=0)
folder_path = tk.StringVar(value=os.path.dirname(__file__))
lbl1 = tk.Label(master=master, textvariable=folder_path)
lbl1.grid(row=1)
button2 = tk.Button(text="Browse", command=browse_button)
button2.grid(row=1, column=1)


tk.Label(master, text="Enter original language: ").grid(row=2)
tk.Label(master, text="Enter target language: ").grid(row=3)

originalLanguage = tk.Entry(master)
targetLanguage = tk.Entry(master)

originalLanguage.grid(row=2, column=1)
targetLanguage.grid(row=3, column=1)

tk.Button(master,
          text='Start translation', command=main).grid(row=4,
                                          column=1,
                                          sticky=tk.W,
                                          pady=4)

master.mainloop()
