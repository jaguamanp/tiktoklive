# main.py
import tkinter as tk
from controller import TikTokLiveController

def main():
    root = tk.Tk()
    controller = TikTokLiveController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
