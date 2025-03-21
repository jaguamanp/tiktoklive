import tkinter as tk
from view import TikTokLiveView
from controller import TikTokLiveController

def main():
    # Crear la ventana raíz de Tkinter
    root = tk.Tk()

    # Crear la vista
    view = TikTokLiveView(root)

    # Crear el controlador y pasárselo a la vista
    controller = TikTokLiveController(root, view)

    # Ejecutar la aplicación Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
