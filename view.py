import tkinter as tk
from tkinter import messagebox

class TikTokLiveView:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi bot de TikTok")
        self.root.geometry("600x600")

        tk.Label(root, text="Usuario de TikTok:", font=("Arial", 12)).pack(pady=10)
        self.entry_username = tk.Entry(root, font=("Arial", 12))
        self.entry_username.pack(pady=5)

        # Botón Iniciar
        self.btn_start = tk.Button(root, text="Iniciar", font=("Arial", 12))
        self.btn_start.pack(pady=10)

        # Botón Detener
        self.btn_stop = tk.Button(root, text="Detener", font=("Arial", 12), state=tk.DISABLED)  # Deshabilitado por defecto
        self.btn_stop.pack(pady=10)

        # Cuadro de texto para mostrar comentarios
        self.text_display = tk.Text(root, width=60, height=15, wrap=tk.WORD, font=("Arial", 10))
        self.text_display.pack(pady=10)
        self.text_display.config(state=tk.DISABLED)

        # Botón Cerrar
        self.btn_close = tk.Button(root, text="Cerrar", font=("Arial", 12), command=self.close_app)
        self.btn_close.pack(side=tk.BOTTOM, pady=10)

    def display_comment(self, comment_text):
        """Mostrar los comentarios en el cuadro de texto."""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.insert(tk.END, comment_text)
        self.text_display.yview(tk.END)
        self.text_display.config(state=tk.DISABLED)

    def show_error(self, message):
        """Mostrar mensajes de error."""
        messagebox.showerror("Error", message)

    def close_app(self):
        """Cerrar la aplicación."""
        self.root.quit()

    def enable_start_button(self):
        """Habilitar el botón 'Iniciar'."""
        self.btn_start.config(state=tk.NORMAL)

    def disable_start_button(self):
        """Deshabilitar el botón 'Iniciar'."""
        self.btn_start.config(state=tk.DISABLED)

    def enable_stop_button(self):
        """Habilitar el botón 'Detener'."""
        self.btn_stop.config(state=tk.NORMAL)

    def disable_stop_button(self):
        """Deshabilitar el botón 'Detener'."""
        self.btn_stop.config(state=tk.DISABLED)

    def update_on_start(self, start_callback, stop_callback):
        """Actualizar las funciones de los botones."""
        self.btn_start.config(command=start_callback)
        self.btn_stop.config(command=stop_callback)
