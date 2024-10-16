# Libraries for building GUI tkinter additions
import tkinter as tk
import customtkinter as ctk
from tkinter import Label, Button, Frame  # Importing Button and Label directly
import tkinter.messagebox as messagebox  # Import messagebox
import random  # for funny error messages

# Machine Learning libraries for the image generator may need transformers latest version
import torch
from torch.amp import autocast  # this should still work in recent versions
from diffusers import StableDiffusionPipeline

# Libraries for processing image used to display images in tkinter
from PIL import ImageTk, Image

# Private modules the log in token to allow access to the image generator on transformers hugging face
from authtoken import auth_token  # see teams chat

# Create app user interface
app = tk.Tk()
app.geometry("1000x700")  # Set back to original size
app.title("..........Hmmm so... ummmmmmmmmm...")
app.configure(bg='blue')
ctk.set_appearance_mode("dark")

# Set Font alternatives (use standard fonts for better compatibility)
Button_font = ctk.CTkFont(family='Comic Sans MS', size=15, weight='bold')

# Load and set background image
def set_background(image_path):
    # Open the image and resize it to fit the app window
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((1000, 700), Image.LANCZOS)
    
    # Convert to PhotoImage for Tkinter
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Create a label to hold the background image
    bg_label = Label(app, image=bg_photo)
    bg_label.image = bg_photo  # Keep reference
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()  # Send the background label to the back layer

# Set your background image (replace 'TKINTER BG.png' with the actual path)
set_background('TKINTER BG.png')

# Class to manage the GUI interface elements
class GUI_Interface:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    # Function to show random error message
    def show_random_error(self, event=None):
        message_dictionary = [
            'ouch!', 'OUCH!', 'Rude!', 'aah, that actually tickles', 'That is INAPPROPRIATE touching!', 'HELP HELP',
            'Now that IS the spot', 'STRANGER DANGER', 'Warning warning warning!', 'Nope, try again!',
            'Is that all you have got?', 'This is not a video game!', 'I am sensitive, okay?', 'Touching is NOT allowed!',
            'That is not the magic button!', 'Hands off the merchandise!', 'You press, I stress!', 'Easy there, champ!',
            'Press me one more time, I dare you!'
        ]
        error_message = random.choice(message_dictionary)
        messagebox.showwarning("!Did I ask you to CLICK on THESE?!", error_message)

    def create_widgets(self):
        # Add four placeholder buttons in each corner
        button_font = ctk.CTkFont(family='Comic Sans MS', size=15, weight='bold')

        self.button1 = Button(self.master, text="WIN", fg="blue", bg="yellow", font=button_font, highlightthickness=0, bd=0, command=self.show_random_error)
        self.button1.place(x=90, y=0)

        self.button2 = Button(self.master, text="CLICK ME", fg="blue", bg="yellow", font=button_font, highlightthickness=0, bd=0, command=self.show_random_error)
        self.button2.place(x=200, y=0)

        self.button3 = Button(self.master, text="DO NOT CLICK", fg="blue", bg="yellow", font=button_font, highlightthickness=0, bd=0, command=self.show_random_error)
        self.button3.place(x=800, y=650)

        self.button4 = Button(self.master, text="LAUNCH SEQUENCE", fg="blue", bg="yellow", font=button_font, highlightthickness=0, bd=0, command=self.show_random_error)
        self.button4.place(x=300, y=650)

        # Set Font alternatives (use standard fonts for better compatibility)
        button_font = ctk.CTkFont(family='Comic Sans MS', size=15, weight='bold')
        default_font = ctk.CTkFont(family='Calibri', size=20)  # Standard font

        # Create input boxes for the prompts
        self.prompt1 = ctk.CTkEntry(master=self.master, height=30, width=500, font=default_font, text_color="black", fg_color="gold", placeholder_text_color='grey', placeholder_text="'Tell me stuff that makes you feel good...'")
        self.prompt1.place(x=280, y=150)

        self.prompt2 = ctk.CTkEntry(master=self.master, height=30, width=500, font=default_font, text_color="black", fg_color="gold", placeholder_text_color='grey', placeholder_text="'Tell me what does not impress you at all...'")
        self.prompt2.place(x=275, y=360)

        # Create a placeholder to show the generated image
        self.img_placeholder1 = ctk.CTkLabel(master=self.master, height=200, width=200, text="", fg_color="transparent")
        self.img_placeholder1.place(x=790, y=150)

        self.img_placeholder2 = ctk.CTkLabel(master=self.master, height=200, width=200, text="", fg_color="transparent")
        self.img_placeholder2.place(x=790, y=360)

# StableDiffusionApp Class to manage image generation
class StableDiffusionApp:
    def __init__(self):
        self.setup_stable_diffusion()

    def setup_stable_diffusion(self):
        try:
            modelid = "CompVis/stable-diffusion-v1-4"
            device = "cuda"
            self.stable_diffusion_model = StableDiffusionPipeline.from_pretrained(
                modelid, variant="fp16", torch_dtype=torch.float16, use_auth_token=auth_token
            )
            self.stable_diffusion_model.safety_checker = None
            self.stable_diffusion_model.to(device)
        except Exception as e:
            print(f"Error loading model: {e}")
            messagebox.showerror("Model Loading Error", "Failed to load the image generation model.")

    def generate_image(self, prompt, img_placeholder, image_list):
        user_input = prompt.get()
        print(f"User input: {user_input}")

        if not user_input.strip():
            messagebox.showwarning("Error", "You need to type something...")
            return

        try:
            with autocast("cuda"):
                image = self.stable_diffusion_model(user_input, height=400, width=400, guidance_scale=8.5).images[0]
            print("Image generated successfully!")

            # Save and load the generated image
            image.save('generatedimage.png')
            img = Image.open("generatedimage.png")
            tk_img = ImageTk.PhotoImage(img)
            img_placeholder.configure(image=tk_img)
            img_placeholder.image = tk_img  # Keep reference
            image_list.append(image)
        except Exception as e:
            print(f"Error generating image: {e}")
            messagebox.showerror("Generation Error", "Image generation failed.")

# Set up GUI elements
gui_elements = GUI_Interface(app)

# Set up lists to store generated images
UC_health = []
UC_poison = []

# Set up Stable Diffusion and bind it to the buttons
stable_diffusion_app = StableDiffusionApp()

trigger = ctk.CTkButton(master=app, height=40, width=200, text_color="blue", fg_color="yellow",
                        text="Click here and I will whip something healthy up for you",
                        command=lambda: stable_diffusion_app.generate_image(gui_elements.prompt1, gui_elements.img_placeholder1, UC_health))
trigger.place(x=460, y=310)

# Create a second trigger button for the UC_poison prompt
trigger2 = ctk.CTkButton(master=app, height=40, width=200, text_color="blue", fg_color="yellow",
                         text="Hmm ok well let's have you stay away from these..",
                         command=lambda: stable_diffusion_app.generate_image(gui_elements.prompt2, gui_elements.img_placeholder2, UC_poison))
trigger2.place(x=480, y=520)

app.mainloop()
