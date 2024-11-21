#References:
#https://www.youtube.com/watch?v=BE0wRHhU11U&list=PLHlrXTRZkTLBQ7k06CFoP3-gayAmfp-GG&index=3
#https://www.youtube.com/watch?v=q8WDvrjPt0M
#https://www.youtube.com/watch?v=aswECYz_oVI
#https://www.youtube.com/watch?v=4qEZned9qWM
#Campus Navigation Project
#Chatgpt used for debugging


#GUI imports
import tkinter as tk
from tkinter import messagebox
import fitz
from tkinter import filedialog
import os

#Creating main window
root = tk.Tk()
root.title("PDF Phrase Search")
root.geometry("600x500")
root.configure(bg="#ADD8E6")

#Functions
def get_text(pdf, count):
    text = ""
    for i in range(count):
        page = pdf.load_page(i)
        text += page.get_text()
    return text

def get_pdf():
    global pdf_path
    global file_name
    global pdf
    global pdf_text

    pdf_path = filedialog.askopenfilename()

    if pdf_path:
        file_name = os.path.basename(pdf_path)
        pdf = fitz.open(pdf_path)
        pg_count = pdf.page_count
        pdf_text = get_text(pdf, pg_count)

        label_1.config(text=file_name)
        pdf.close()
    
def get_input():
    global phrase
    global pdf_text
    phrase = input.get()

    if phrase == "":
        messagebox.showerror("Error", "Please enter a phrase!")
    else:
        if pdf_text == "":
            messagebox.showerror("Error", "No valid text to search through has been provided!")
        else:
            display(pdf_text, phrase)

def Rabin_Karp(text, phrase, d=26, q=89):
    n = len(text)
    m = len(phrase)
    h = pow(d, m-1) % q
    hash_t = 0
    hash_p = 0
    indices = []
    for i in range(m):
        hash_t = (d * hash_t + ord(text[i])) % q
        hash_p = (d * hash_p + ord(phrase[i])) % q

    for i in range(n-m+1):
        if hash_t == hash_p:
            if text[i:i+m] == phrase:
                indices.append(i)
        if i < n-m:
            hash_t = (d * (hash_t - ord(text[i]) * h) + ord(text[i+m])) % q
            if hash_t < 0:
                hash_t += q
    return indices

def display(text, phrase):
    global count
    global results

    indices = Rabin_Karp(text, phrase)

    num = len(indices)
    count = str(num)
    results = str(indices)

    if num == 0:
        label_3.config(text="Phrase was not found!")
    else:
        label_3.config(text="Phrase found " + count + " times at positions (0-indexed): " + results)



#Variables
pdf_path = ""
file_name = ""
pdf = None
pdf_text = ""
phrase = ""
count = ""
results = ""



# UI
#Upload button
uploadButton = tk.Button(root, text="Upload", font=("Arial",14 ,"bold"), fg="white", bg="#6A8DAD", command=get_pdf)
uploadButton.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

#File name printout
label_1 = tk.Label(root, text=file_name, font = ("Arial",14, "bold"), fg="#6A8DAD", bg= "#ADD8E6")
label_1.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="e")

#User prompt
label_2 = tk.Label(root, text="Enter phrase to search: ", font = ("Arial",14, "bold"), fg="#6A8DAD", bg= "#ADD8E6")
label_2.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="e")

#Input box
input = tk.Entry(root, width=40)
input.grid(row=1, column=2, columnspan= 2, padx=10, pady=10)

#Submit Button
subButton = tk.Button(root, text="Search Phrase", font=("Arial",14 ,"bold"), fg="white", bg="#6A8DAD", command=get_input)
subButton.grid(row=2, column=1, columnspan=2, pady=10)

#User prompt
label_3 = tk.Label(root, text="" + results, font = ("Arial",14, "bold"), fg="#6A8DAD", bg= "#ADD8E6", wraplength=500)
label_3.grid(row=5, column=0, columnspan= 5, padx=10, pady=10, sticky="ew")




#Configuring grid columns
root.grid_columnconfigure(0, weight=0, minsize=150)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=0, minsize=50)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=0, minsize=50)
root.grid_columnconfigure(5, weight=1)

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)

#Event Loop
root.mainloop()