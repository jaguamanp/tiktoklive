import tkinter as tk
from tkinter import messagebox

class TikTokLiveView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

        # Configurar interfaz
        self.username_label = tk.Label(root, text="Usuario de TikTok:", font=("Arial", 12))
        self.username_label.pack(pady=10)

        self.entry_username = tk.Entry(root, font=("Arial", 12))
        self.entry_username.pack(pady=5)

        self.btn_start = tk.Button(root, text="Iniciar", font=("Arial", 12), command=self.start)
        self.btn_start.pack(pady=10)

        self.btn_stop = tk.Button(root, text="Detener", font=("Arial", 12), command=self.stop)
        self.btn_stop.pack(pady=10)

        self.text_display = tk.Text(root, width=60, height=15, wrap=tk.WORD, font=("Arial", 10))
        self.text_display.pack(pady=10)
        self.text_display.config(state=tk.DISABLED)

    def start(self):
        self.controller.start()

    def stop(self):
        self.controller.stop()

    def get_username(self):
        return self.entry_username.get().strip()
