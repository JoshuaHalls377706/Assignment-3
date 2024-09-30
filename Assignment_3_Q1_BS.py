# Libraries for building GUI tkinter additions
import tkinter as tk
import customtkinter as ctk
from tkinter import font as tkFont
from tkinter import Label, Button, Frame  # Importing Button and Label directly
import tkinter.messagebox as messagebox  # Import messagebox

import random #for funny error messages

# Machine Learning libraries for the image generator may need transformers latest version
import torch
from torch.amp import autocast  # this should still work in recent versions
from diffusers import StableDiffusionPipeline

# Libraries for processing image used to display images in tkinter
from PIL import ImageTk, Image #custom message boxes

# Private modules the log in token to allow access to the image generator on transformers hugging face
from authtoken import auth_token #see teams chat

#---------------------------------------------------------------------------------------------------------------------------
#Once finished create classes O_encapsulaion
#---------------------------------------------------------------------------------------------------------------------------


# Create app user interface
app = tk.Tk()
app.geometry("1200x900")
app.title("Text to Image app")
app.configure(bg='black')
ctk.set_appearance_mode("dark") 

#------------------------------------------------------------------------------------------------------------------------------------
#set up tkinter face ... face
#------------------------------------------------------------------------------------------------------------------------------------

# Set Font alternatives (use standard fonts for better compatibility)
Button_font = ctk.CTkFont(family='Comic Sans MS', size=15, weight='bold')
Title_font = ctk.CTkFont(family='Broadway', size=20, weight='bold')  # Example standard font
STitle_font = ctk.CTkFont(family='Arial', size=20, weight='bold')     # Another standard font
Default = ctk.CTkFont(family='Calibri', size=20)  # Standard font

#------------------------------------------------------------------------------------------------------------------------------------

# Create input box on the user interface 
prompt = ctk.CTkEntry(master=app, height=30, width=1180, font= Default, text_color="black", fg_color="aqua", placeholder_text_color='grey', placeholder_text= "'Hmm, this is awkward, your mind seems to be completely void of function ... I work well with interpretive dance?? ... No? Just type here ...'") 
prompt.place(x=10, y=300)

# Create a placeholder to show the generated image
img_placeholder = ctk.CTkLabel(master=app, height=400, width=400, text="")
img_placeholder.place(x=400, y=385)
#------------------------------------------------------------------------------------------------------------------------------------


#Label windows
Labeltop = Label(app, text="Sasusage on a stick productions presents ...",font=Title_font,bg="black", fg="aqua")
Labeltop.pack() # basically places this widget inside the window

Labelbot = Label(app, text="I hope you enjoyed this Q1 OPTION for the final assignment \n Developed by Tkinter powered by vegan sausages",font=Title_font,bg="black", fg="aqua")
Labelbot.pack(side=tk.BOTTOM,fill=tk.X) # basically places this widget inside the window

#Label Colours
Episode = Label(app, text="Episode One", bg="black", fg="aqua",font=STitle_font)
Episode.pack()
Title = Label(app, text="The Crazy Hungry Bandicoot creates MAGIC TOKENS especially for you...", bg="black", fg="aqua",font=STitle_font)
Title.pack(fill=tk.X) # fill=X - makes the widget as wide as the parent
LHS = Label(app, bg="black", fg="black")
LHS.pack(side=tk.LEFT, fill=tk.Y)
RHS = Label(app, bg="black", fg="black")
RHS.pack(side=tk.RIGHT, fill=tk.Y)
BASE = Label(app, bg="black", fg="black")
BASE.pack(side=tk.BOTTOM, fill=tk.X)
Instruction = Label(app, text="'Please, concentrate and communicate to me the image inspiration floating in your mind ...'",font=Default ,bg="black", fg="aqua")
Instruction.place(x=250, y=260)

# Frame is a rectangular area that can contain other widgets
topFrame = Frame(app)
bottomFrame = Frame(app)
leftFrame = Frame(app)
rightFrame = Frame(app)

#set frame location
topFrame.pack()
bottomFrame.pack(side=tk.BOTTOM)
leftFrame.pack(side=tk.LEFT)
rightFrame.pack(side=tk.RIGHT)
#---------------------------------------------------------------------------------------------------------------------------
message_dictionary = [
    '               ouch!              ',
    '                 OUCH!            ',
    '             Rude!                ',
    'aah, that actually tickles       ',
    'That is INNAPROPRIATE touching!   ',
    '          HELP HELP               ',
    '      Now that IS the spot        ',
    '       STANGER DANGER            ',
    '   Warning warning warning!        ',
    '    Nope, try again!               ',
    '    Is that all you have got?       ',
    '     This is not a video game!      ',
    '     I am sensitive, okay?          ',
    '    Touching is NOT allowed!         ',
    '    That is not the magic button!     ',
    '   Hands off the merchandise!      ',
    '        You press, I stress!       ',
    '     Easy there, champ!            ',
    'Press me one more time, I dare you!',
]

# ----------------------------------------------------------------------------

# Load and display a static GIF of crazy bandicoot
def display_static_gif(gif_path, width=100, height=100):
    img = Image.open(gif_path)
    img = img.resize((width, height), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    img_label = Label(app, image=tk_img, bg="grey")
    img_label.image = tk_img
    img_label.place(x=550, y=140)

# Example usage for static GIF
display_static_gif('crazy_bandicoot.gif', width=100, height=100)

# ----------------------------------------------------------------------------
#Button action event is a mouse click as message box not terminal
def show_random_error(event=None):
    #call error from list
    error_message = random.choice(message_dictionary)
#   print("ÓUCH!")#show in terminal
#print in warning box title
    messagebox.showwarning("!Did I ask you to CLICK on THESE?!",error_message)#make random from a dictionary (ouch, rude, dont do that, inappropriate)

# ----------------------------------------------------------------------------

#Button names and location
button1 = Button(topFrame, text="Button 1", fg="violet",bg="grey",font=Button_font)
button2 = Button(topFrame, text="Wrong way GO BACK", fg="purple",bg="grey",font=Button_font)
button3 = Button(topFrame, text="ABORT!", fg="red",bg="grey",font=Button_font)
button4 = Button(bottomFrame, text="Didn't think this out? CLick ME", fg="purple",bg="grey",font=Button_font)
jump = Button(leftFrame, text="JUMP", fg="green",bg="grey",font=Button_font)
stop = Button(rightFrame, text="!!!STOP!!!", fg="red",bg="grey",font=Button_font)

# These buttons will be on top
button1.pack(side=tk.LEFT) # place as far left as possible
button2.pack(side=tk.LEFT)
button3.pack(side=tk.LEFT)
# Button 4 is on the bottom
button4.pack(side=tk.BOTTOM)
# ACTION buttons left right
jump.pack(side=tk.LEFT)
stop.pack(side=tk.RIGHT)

#activate buttons
button1.bind("<Button-1>",show_random_error)
button2.bind("<Button-1>",show_random_error)
button3.bind("<Button-1>",show_random_error)
button4.bind("<Button-1>",show_random_error)
jump.bind("<Button-1>",show_random_error)
stop.bind("<Button-1>",show_random_error)

#---------------------------------------------------------------------------------------------------------------------------

# Download stable diffusion model from hugging face transformers
modelid = "CompVis/stable-diffusion-v1-4"
device = "cuda"
stable_diffusion_model = StableDiffusionPipeline.from_pretrained(
    modelid, variant="fp16", torch_dtype=torch.float16, use_auth_token=auth_token
)
stable_diffusion_model.safety_checker = None
stable_diffusion_model.to("cuda")

#---------------------------------------------------------------------------------------------------------------------------
# Generate image from text 
def generate_image(): 
    """ This function generates an image from text with stable diffusion"""
    
    # Debugging: Check if the prompt is retrieved correctly
    user_input = prompt.get()
    print(f"User input: {user_input}")  # Check in the console if the prompt is getting retrieved
    
    # If the input is empty, show an alert box
    if not user_input.strip():
        print("You need to help me out here and type something ...")
        messagebox.showwarning("Errrrr you gotta type something ...")
        return

    # Generate image with Stable Diffusion
    print("Generating image with prompt:", user_input) # Corrected logging

    with autocast('cuda'): 
        image = stable_diffusion_model(user_input, height=400, width=400, guidance_scale=8.5).images[0]  # Get the image
    
    # Debugging: Log successful image generation
    print("Image generated successfully!")

    # Save the generated image
    image.save('generatedimage.png')
    
    # Convert the generated image to be compatible with ImageTk
    img = Image.open("generatedimage.png")
    tk_img = ImageTk.PhotoImage(img)  # Use ImageTk for displaying in tkinter
    
    # Update the label with the ImageTk image
    img_placeholder.configure(image=tk_img) 
    img_placeholder.image = tk_img  # Keep a reference to avoid garbage collection

#---------------------------------------------------------------------------------------------------------------------------
# Create the trigger button with the correct text configuration
trigger = ctk.CTkButton(master=app, height=40, width=120, text_color="aqua", fg_color="black", 
                        text="click here to See THE MAGNIFICENT BANDICOOT at work", command=generate_image)

trigger.place(x=420, y=330)

#---------------------------------------------------------------------------------------------------------------------------
app.mainloop()

#-------------------------------------------------------------------------------------
#Now we want to construct a quiz that feeds into the image generator and and produces four custom items that can be fed into our game...
#so the key words are imputed into a forced prompt that will generate a a set of similarly themed images.

#----------------------------------------------------------------------------------------------------------------------------------------------------------
#Work on custom message boxes
# Function to create a custom message box with an image
def custom_message_box(message, image_path):
    # Create a new window
    msg_box = tk.Toplevel()
    msg_box.title("Custom Message Box")
    msg_box.geometry("300x200")
    
    # Load the image
    img = Image.open(image_path)
    img = img.resize((100, 100), Image.ANTIALIAS)  # Resize image if necessary
    img_tk = ImageTk.PhotoImage(img)
    
    # Create a label for the image
    img_label = tk.Label(msg_box, image=img_tk)
    img_label.image = img_tk  # Keep a reference to avoid garbage collection
    img_label.pack(pady=10)

    # Create a label for the message
    message_label = tk.Label(msg_box, text=message)
    message_label.pack(pady=10)

    # Create a button to close the message box
    close_button = tk.Button(msg_box, text="Close", command=msg_box.destroy)
    close_button.pack(pady=10)

    msg_box.mainloop()

# Button action event is a mouse click
def printName(event):
    custom_message_box("ÓUCH!", "path/to/your/image.png")  # Change the path to your image

# Example button
test_button = tk.Button(app, text="Click Me", command=lambda: printName(None))
test_button.pack(pady=20)
