# 🎄 Interactive Christmas Present App 🎄

import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import os
import pygame
from threading import Thread

# ----------------------
# SETTINGS
# ----------------------
PHOTOS = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
MUSIC_FILE = "music.mp3"
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 1920

# ----------------------
# INITIALIZATION
# ----------------------
pygame.mixer.init()
music_playing = False
current_photo_index = -1
present_opened = False

class ChristmasPresentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Christmas Present")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg='#DC143C')  # Red background
        
        # Create canvas
        self.canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                           bg='#DC143C', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)  # Click to interact
        self.canvas.bind("<Motion>", self.on_motion)   # Mouse movement
        
        self.present_opened = False
        self.photo_index = -1
        
        # Start music in background
        self.play_music()
        
        # Draw initial present
        self.draw_present()
    
    def draw_present(self):
        """Draw the closed present"""
        self.canvas.delete("all")
        
        if not self.present_opened:
            # Draw box (gift box) - CLOSED
            box_x1 = 240
            box_y1 = 560
            box_x2 = 840
            box_y2 = 1360
            
            # Box
            self.canvas.create_rectangle(box_x1, box_y1, box_x2, box_y2,
                                        fill='#228B22', outline='#FFD700', width=8)
            
            # Ribbon - horizontal
            ribbon_y = (box_y1 + box_y2) // 2
            self.canvas.create_line(box_x1, ribbon_y, box_x2, ribbon_y,
                                   fill='#FFD700', width=15)
            
            # Ribbon - vertical
            ribbon_x = (box_x1 + box_x2) // 2
            self.canvas.create_line(ribbon_x, box_y1, ribbon_x, box_y2,
                                   fill='#FFD700', width=15)
            
            # Bow on top
            bow_x = (box_x1 + box_x2) // 2
            bow_y = box_y1
            self.canvas.create_oval(bow_x - 60, bow_y - 60, bow_x + 60, bow_y + 60,
                                   fill='#FF6464', outline='#FFD700', width=3)
            
            # Text instructions
            self.canvas.create_text(540, 400, text="CLICK TO OPEN PRESENT",
                                   font=("Arial", 48, "bold"), fill='#FFD700')
            self.canvas.create_text(540, 480, text="Click anywhere on the gift!",
                                   font=("Arial", 32), fill='white')
        else:
            # Show photos when opened
            self.show_photo()
    
    def show_photo(self):
        """Display current photo"""
        self.canvas.delete("all")
        
        # Background
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
                                    fill='#228B22')
        
        if self.photo_index < len(PHOTOS) and self.photo_index >= 0:
            photo_path = PHOTOS[self.photo_index]
            
            if os.path.exists(photo_path):
                # Load and display photo
                img = Image.open(photo_path)
                img.thumbnail((WINDOW_WIDTH - 100, WINDOW_HEIGHT - 300))
                self.photo_image = ImageTk.PhotoImage(img)
                
                x = (WINDOW_WIDTH - img.width) // 2
                y = (WINDOW_HEIGHT - img.height) // 2 - 100
                
                self.canvas.create_image(x, y, image=self.photo_image, anchor="nw")
        
        # Photo counter
        self.canvas.create_text(540, 1800, 
                               text=f"Photo {self.photo_index + 1} of {len(PHOTOS)}",
                               font=("Arial", 28), fill='#FFD700')
        
        # Instructions
        if self.photo_index < len(PHOTOS) - 1:
            self.canvas.create_text(540, 1900,
                                   text="CLICK for next photo",
                                   font=("Arial", 32, "bold"), fill='white')
        else:
            self.canvas.create_text(540, 1900,
                                   text="Happy Holidays!",
                                   font=("Arial", 36, "bold"), fill='#FFD700')
    
    def on_click(self, event):
        """Handle mouse click"""
        if not self.present_opened:
            # Open the present
            self.present_opened = True
            self.photo_index = 0
            self.show_photo()
        else:
            # Show next photo
            if self.photo_index < len(PHOTOS) - 1:
                self.photo_index += 1
                self.show_photo()
            else:
                # Restart from present
                self.present_opened = False
                self.photo_index = -1
                self.draw_present()
    
    def on_motion(self, event):
        """Handle mouse hover for cursor change"""
        # Change cursor to pointer when over the app
        self.root.config(cursor="hand2")
    
    def play_music(self):
        """Play background music"""
        if os.path.exists(MUSIC_FILE):
            try:
                pygame.mixer.music.load(MUSIC_FILE)
                pygame.mixer.music.play(-1)  # Loop
                pygame.mixer.music.set_volume(0.3)
            except Exception as e:
                print(f"Could not play music: {e}")

# ----------------------
# RUN APP
# ----------------------
print("🎄 Starting Interactive Christmas Present App...")
print("📦 Instructions: Click on the present to open it!")
print("📸 Then click to view each photo")

root = tk.Tk()
app = ChristmasPresentApp(root)

# Center window on screen
root.update()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - WINDOW_WIDTH) // 2
y = (screen_height - WINDOW_HEIGHT) // 2
root.geometry(f"+{x}+{y}")

try:
    root.mainloop()
except KeyboardInterrupt:
    print("\n🎄 Closing app...")
finally:
    pygame.mixer.quit()