
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import Label, Button#, Frame  #
import tkinter.messagebox as messagebox
import random
import os
import subprocess
import torch
from torch.amp import autocast  # this should still work in recent versions
from diffusers import StableDiffusionPipeline
import pygame
from PIL import ImageTk, Image

# Private modules the log in token to allow access to the image generator on transformers hugging face
from authtoken import auth_token  # see teams chat

# Get the directory of the current .py file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create app user interface
app = tk.Tk()
app.geometry("1000x700")  # Set back to original size
app.title("..........Hmmm so... ummmmmmmmmm...")
app.configure(bg='blue')
ctk.set_appearance_mode("dark")

# Initialize Pygame mixer for playing music
pygame.mixer.init()

# Function to play theme
def play_music():
    pygame.mixer.music.load("Theme.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

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

# Set your background image
set_background("T_BG1.png")

# Play background music when the app starts
play_music()

# Function to load player name from file
def load_player_name():
    if os.path.exists("player_name.txt"):
        with open("player_name.txt", "r") as f:
            return f.read().strip()
    return ""
# Load player name from file
player_name = load_player_name()

# Set Font alternatives (use standard fonts for better compatibility)
Button_font = ctk.CTkFont(family='Comic Sans MS', size=15, weight='bold')

# Add a label to display the player's name
name_label = ctk.CTkLabel(master=app, text=f"Welcome, {player_name}!", font=Button_font, text_color="DodgerBlue2", fg_color="lemon chiffon")
name_label.place(x=530, y=125)

# Function to close Tkinter and run the Pygame script
def quit_tkinter_and_run_pygame():
    pygame.mixer.music.stop()
    app.quit()
    app.destroy()
    
    # Launch the Pygame script using subprocess
    pygame_script = os.path.join(os.getcwd(), "0_ Game_0.py")  # Adjust with the correct name and path
    subprocess.run(["python", pygame_script], check=True)

# Class to manage the GUI interface elements
class GUI_Interface:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    # Function to show random error message
    def show_random_error(self):
        message_dictionary = [
            'ouch!', 'OUCH!', 'Rude!', 'aah, that actually tickles', 'That is INAPPROPRIATE touching!', 'HELP HELP',
            'Now that IS the spot', 'STRANGER DANGER', 'Warning warning warning!', 'Nope, try again!',
            'Is that all you have got?', 'This is serious!', 'I am sensitive, okay!', 'Touching is NOT allowed!',
            'That is not the magic button!', 'Hands off the merchandise!', 'You press, I stress!', 'Easy there, champ!',
            'Press me one more time, I dare you!'
        ]
        error_message = random.choice(message_dictionary)
        messagebox.showwarning("!Did I ask you to CLICK on THESE?!", error_message)

    def create_widgets(self):
        # Add four placeholder buttons in each corner
        button_font = ctk.CTkFont(family='Comic Sans MS', size=15, weight='bold')

        self.button1 = Button(self.master, text="WIN", fg="gold", bg="DodgerBlue2", font=button_font, highlightthickness=0, bd=0, command=self.show_random_error)
        self.button1.place(x=90, y=0)

        self.button2 = Button(self.master, text="RELEASE GRAVITY", fg="gold", bg="DodgerBlue2", font=button_font, highlightthickness=0, bd=0, command=self.show_random_error)
        self.button2.place(x=200, y=0)

        self.button3 = Button(self.master, text="DO NOT CLICK", fg="gold", bg="DodgerBlue2", font=button_font, highlightthickness=0, bd=0, command=self.show_random_error)
        self.button3.place(x=800, y=650)

        self.button4 = Button(self.master, text="If your happy with that click here to get moving!", fg="DodgerBlue2", bg="lemon chiffon", font=button_font, highlightthickness=0, bd=0, command= quit_tkinter_and_run_pygame)
        self.button4.place(x=300, y=650)

        # Set Font alternatives (use standard fonts for better compatibility)
        button_font = ctk.CTkFont(family='Comic Sans MS', size=15, weight='bold')
        default_font = ctk.CTkFont(family='Calibri', size=20)

        #Text for prompt 1
        self.generated_prompt_label1 = ctk.CTkLabel(master=self.master, height=30, width=500,font=default_font, text="What is your favourite fruit?", text_color="DodgerBlue2", fg_color= "lemon chiffon")
        self.generated_prompt_label1.place(x=400, y=150) 
        
        # Create input boxes for the prompt 1
        self.prompt1 = ctk.CTkEntry(master=self.master, height=30, width=500, font=default_font, text_color="DodgerBlue2", fg_color="lemon chiffon", placeholder_text_color='cornsilk2', placeholder_text="'This is nice isnt it.'")
        self.prompt1.place(x=400, y=180)
        
        #Text for prompt 2
        self.generated_prompt_label2 = ctk.CTkLabel(master=self.master, height=30, width=500,font=default_font, text= "What is your favourite colour?", text_color="DodgerBlue2", fg_color="lemon chiffon")
        self.generated_prompt_label2.place(x=390, y=210) 

        # Create input boxes for the prompt 2
        self.prompt2 = ctk.CTkEntry(master=self.master, height=30, width=500, font=default_font, text_color="DodgerBlue2", fg_color="lemon chiffon", placeholder_text_color='cornsilk2', placeholder_text="There has to be something...'")
        self.prompt2.place(x=400, y=240)

        # Create a placeholder to show the generated image
        self.img_placeholder1 = ctk.CTkLabel(master=self.master, height=200, width=200, text="", fg_color="lemon chiffon")
        self.img_placeholder1.place(x=480, y=330)

    trigger = ctk.CTkButton(master=app, height=40, width=300, text_color="DodgerBlue2", fg_color="goldenrod1",
                    text="       Click here and I will whip something healthy up for you on our trip!     ",
                    command=lambda: stable_diffusion_app.generate_image(gui_elements.prompt1, gui_elements.prompt2, gui_elements.img_placeholder1, UC_health))
    trigger.place(x=420, y=270)

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

    def generate_image(self, prompt1, prompt2, img_placeholder, image_list):#prompt2
        # Extract user inputs from both prompts
        user_input1 = prompt1.get()
        user_input2 = prompt2.get()

        # Define a prompt template that includes user inputs
        prompt_template = f"A cocktail drink in a martini glass filled with '{user_input2}'liquid being with slices of'{user_input1}' on a white background, in a paper cutout style. ."
        print(f"Generated Prompt: {prompt_template}")

        if not user_input1.strip():
            messagebox.showwarning("Error", "You need to type something...")
            return

        try:
            with autocast("cuda"):
                image = self.stable_diffusion_model(prompt_template, height=320, width=320, guidance_scale=12).images[0] #guidance scale is how strong to follow the prompt
            print("Image generated successfully!")

            # Scale the image down to 30% of its original size
            original_size = image.size
            new_size = (int(original_size[0] * 0.2), int(original_size[1] * 0.2))
            image = image.resize(new_size, Image.LANCZOS)

            # Save and load the generated image
            image.save('generatedhealth.png')

            img = Image.open("generatedhealth.png")
            img.thumbnail((200, 200))  # This scales the image to fit within the box

            # Convert to CTkImage for display in customtkinter
            ctk_img = CTkImage(light_image=img, size=(320, 320)) 

            # Update the image in the label
            img_placeholder.configure(image=ctk_img)
            img_placeholder.image = ctk_img  # Keep a reference to prevent garbage collection
            image_list.append(image)

        except Exception as e:
            print(f"Error generating image: {e}")
            messagebox.showerror("Generation Error", "Image generation failed.")

# Set up GUI elements
gui_elements = GUI_Interface(app)

# Set up lists to store generated images
UC_health = []

# Set up Stable Diffusion and bind it to the buttons
stable_diffusion_app = StableDiffusionApp()

app.mainloop()
