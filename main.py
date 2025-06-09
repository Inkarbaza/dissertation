BACKGROUND_COLOR = "#B1DDC6"

from tkinter import *
from tkinter import messagebox
import random
import pandas as pd
import math

pd.set_option('display.max_columns', None)

# try:
#     data = pd.read_csv('data/words_to_learn.csv')
# except FileNotFoundError:
#     data = pd.read_csv('data/french_words.csv')

file_dir = r'C:\Users\bazarkui\Downloads\англ\English vocabulary.xlsx'
data = pd.read_excel(file_dir).fillna('')
dc2 = data.to_dict('records')
rand_card = random.choice(dc2)

started = False

def change_lan(lang):
    global rand_card
    if lang == 'English':
        filtered_indices = [idx for idx, d in enumerate(dc2) if d['known'] == '']
        print('Unknown words', len(filtered_indices))
        rand_idx = random.choice(filtered_indices)
        rand_card = dc2[rand_idx]
        canvas.itemconfig(img_card, image=front_img)
        txt_clr = 'black'
    else:
        canvas.itemconfig(img_card, image=back_img)
        txt_clr = 'white'
        exmpls = rand_card['Examples']
        canvas.itemconfig(txt_examples, text=exmpls, fill=txt_clr)
    word = rand_card[lang]
    trans = rand_card['Transcript']
    canvas.itemconfig(txt_lan, text=lang, fill=txt_clr)
    canvas.itemconfig(txt_word, text=word, fill=txt_clr)
    canvas.itemconfig(txt_transcript, text=trans, fill=txt_clr)



def swap_words(know):
    global started
    if know and started:
        # dc2.remove(rand_card)
        rand_card['known'] = 1
        #print(rand_card)
    change_lan('English')
    window.update()
    window.after(3000, change_lan('Russian'))
    started = True


def on_closing():
    data2 = pd.DataFrame.from_dict(dc2)
    data2.to_excel(file_dir, index=False)
    window.destroy()


# ----------------------------UI SETUP ------------------------------- #

window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.geometry("900x726")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file='images/card_front.png')
back_img = PhotoImage(file='images/card_back.png')
img_card = canvas.create_image(0, 0, anchor=NW, image=front_img)
canvas.grid(row=0, column=0, columnspan=2)

txt_lan = canvas.create_text(400, 150, text="Start", justify=CENTER, font=("Arial", 25, 'italic'))
txt_word = canvas.create_text(400, 253, text="your journey", justify=CENTER, font=("Arial", 30, 'bold'),width = 500)
txt_transcript = canvas.create_text(400, 380, text="", justify=CENTER, font=("Arial", 20))
txt_examples = canvas.create_text(400, 480, text="", justify=CENTER, font=("Arial", 11))

img_right = PhotoImage(file="images/right.png")
btn_right = Button(image=img_right, highlightthickness=0, command=lambda: swap_words(True))
btn_right.grid(row=2, column=1)

img_wrong = PhotoImage(file="images/wrong.png")
btn_wrong = Button(image=img_wrong, highlightthickness=0, command=lambda: swap_words(False))
btn_wrong.grid(row=2, column=0)


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
