import openai
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image,ImageTk
import pyttsx3
import threading

# Define custom font
custom_font = ("Comic Sans MS", 12)

#======================================================================================
#for speaking text to speech
def speak(text):
    engine = pyttsx3.init()
    """
    Speaks the given text using the Pyttsx3 engine.
    """
    engine.say(text)
    engine.runAndWait()


#=======================================================================================
# Making a Place holder class
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder='', color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.show_placeholder()

    def show_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def on_focus_in(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def on_focus_out(self, event):
        if not self.get():
            self.show_placeholder()

#=======================================================================================
#for determining time
now = datetime.now()
hour = now.hour
minute = now.minute
time_str = now.strftime("%I:%M %p")
print(time_str)

#greeting according to time.
greetings = {
        "morning": "Good morning",
        "afternoon": "Good afternoon",
        "evening": "Good evening",
        "night": "Good night"
        }

if hour < 12:
    greeting_type = "morning"
elif hour < 18:
    greeting_type = "afternoon"
elif hour < 22:
    greeting_type = "evening"
else:
    greeting_type = "night"

#specify name of the user
name = "Student"

#formating the greeting part
greet = f"{greetings[greeting_type]} {name}!"

#=======================================================================================

# Set your OpenAI API key
openai.api_key = 'API KEY'
    
def generate_interpretation():
    prompt = entry_text.get()
    if prompt=="Enter the Input":
        messagebox.showwarning("Warning", "Please enter text.")
        return

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Student: '{prompt}' \nTutor:",
            max_tokens=300,
            n=1,
            stop=None
        )
        
        interpretation = response.choices[0].text.strip()  # Remove leading/trailing spaces

        # Display the interpretation
        text_interpretation.delete(1.0, tk.END)  # Clear previous interpretation
        text_interpretation.insert(tk.END, interpretation)
    except openai.error.OpenAIError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    

#=======================================================================================
def generate_interpretation_speak():
    prompt = entry_text.get()
    if prompt=="Enter the Input":
        messagebox.showwarning("Warning", "Please enter text.")
        return

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Student: '{prompt}' \nTutor:",
            max_tokens=100,
            n=1,
            stop=None
        )
        
        interpretation = response.choices[0].text.strip()  # Remove leading/trailing spaces
        
        # Display the interpretation
        text_interpretation.delete(1.0, tk.END)  # Clear previous interpretation
        text_interpretation.insert(tk.END, interpretation)
        
    except openai.error.OpenAIError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    thread = threading.Thread(target=speak, args=(interpretation,))
    thread.start()
    
        
        

#=======================================================================================




# Create the main window
window = tk.Tk()
window.title("Student Tutoring Assistant")

window.geometry("1480x800") 

# Set a custom background color
window.configure(bg="#c2e4fd")

# Create and configure widgets
style = ttk.Style()
style.configure("TButton", foreground="green", background="blue", font=custom_font)
style.map("TButton", foreground=[("active", "blue"), ("disabled", "#D3D3D3")])

#Open image using Image module  
im1 = Image.open(r"C:\Users\Harsh Raj\Pictures\Camera Roll\8ba615e8c14d1ebb6cb54ead8bd6e176.png")  
im2 = Image.open(r"C:\Users\Harsh Raj\Pictures\Camera Roll\Designer_1.png")  
im3 = Image.open(r"C:\Users\Harsh Raj\Pictures\Camera Roll\Designer_2.png")  

# Create an ImageTk.PhotoImage object from the loaded image
img_tk1 = ImageTk.PhotoImage(im1)
img_tk2 = ImageTk.PhotoImage(im2)
img_tk3 = ImageTk.PhotoImage(im3)


# Create a label widget and set its image
label1 = tk.Label(window, image=img_tk1, bg="#c2e4fd")
label2 = tk.Label(window, image=img_tk2, bg="#309bfe")
label3 = tk.Label(window, image=img_tk3, bg="#309bfe")
label1.pack(side="top", pady=10)
label2.pack(side="left", padx=50)
label3.pack(side="right", padx=50)

label_instruction = tk.Label(window, text=greet+"\nWelcome to the Student Tutoring Assistant!", font=("Courier", 17))
label_instruction.configure(bg="#c2e4fd")

entry_text = PlaceholderEntry(window, width=50, font=custom_font, placeholder="Enter the Input")

frame = tk.Frame(window,bg="#c2e4fd")
button_generate = ttk.Button(frame, text="Ask & Read",command=generate_interpretation, width=20)
button_listen = ttk.Button(frame, text="Ask & Listen",command=generate_interpretation_speak, width=20)
text_interpretation = tk.Text(window, height=16, width=50, font=custom_font)
text_interpretation.config(wrap="word")

# Place widgets on the window
label_instruction.pack(pady=10)
entry_text.pack(pady=5)
frame.pack(pady=10)
button_generate.pack(side="left", padx=10)
button_listen.pack(side="right", padx=10)
text_interpretation.pack(pady=10)



# Start the GUI main loop
window.mainloop()

