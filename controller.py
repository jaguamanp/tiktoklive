import threading
import asyncio
from tkinter import messagebox
from view import TikTokLiveView
from model import TikTokLiveModel

from TikTokLive.events import ConnectEvent, CommentEvent

class TikTokLiveController:
    def __init__(self, root, view):
        self.view = view
        self.model = None

        # Enlazar las funciones de inicio y parada de la vista
        self.view.update_on_start(self.start_tiktok_live, self.stop_tiktok_live)

    def start_tiktok_live(self):
        username = self.view.entry_username.get().strip()

        if not username:
            self.view.show_error("Debes ingresar un usuario de TikTok")
            return

        # Deshabilitar el botón de 'Iniciar' y habilitar 'Detener'
        self.view.disable_start_button()
        self.view.enable_stop_button()

        self.model = TikTokLiveModel(username)

        # Asignar la función de recibir comentarios en el modelo
        self.model.client.on(ConnectEvent, self.on_connect)
        self.model.client.on(CommentEvent, self.on_comment)

        # Iniciar el loop de asyncio en un hilo separado
        threading.Thread(target=self.start_asyncio_loop, daemon=True).start()

    def start_asyncio_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.model.run_client())  # Ejecutar la conexión
        loop.run_forever()

    def on_connect(self, event):
        """ Callback cuando se conecta a TikTok Live """
        print(f"Conectado a {event.unique_id}")

    def on_comment(self, event):
        """ Callback cuando se recibe un comentario """
        comment_text = f"{event.user_info.nick_name}: {event.comment}"
        self.view.display_comment(comment_text)

    def stop_tiktok_live(self):
        """ Detener la conexión """
        if self.model:
            print("Desconectando de TikTok Live...")
            self.model.client.stop()  # Detener la conexión de TikTok Live

            # Habilitar el botón 'Iniciar' y deshabilitar el botón 'Detener'
            self.view.enable_start_button()
            self.view.disable_stop_button()

    def close_app(self):
        """ Cerrar la aplicación """
        if self.model:
            self.stop_tiktok_live()
        self.view.close_app()
