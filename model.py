import asyncio
import pandas as pd
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from gtts import gTTS
from websockets.exceptions import ConnectionClosedError
from datetime import datetime
import os

class TikTokLiveModel:
    def __init__(self, username):
        self.username = username
        self.client = TikTokLiveClient(unique_id=username)
        self.processed_comments = set()
        self.csv_filename = f'comentarios_{self.username}_{datetime.now().strftime("%Y-%m-%d")}.csv'

    async def run_client(self):
        """Conectar a TikTok Live y gestionar comentarios."""
        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            print(f"Conectado a @{event.unique_id}")

        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            """Procesar los comentarios recibidos."""
            new_comment = {"nick_name": event.user_info.nick_name, "comment": event.comment}
            comment_key = (new_comment['nick_name'], new_comment['comment'])

            if comment_key in self.processed_comments:
                return  # Si ya se procesó este comentario, ignorarlo

            self.processed_comments.add(comment_key)

            # Guardar el comentario en el CSV
            new_df = pd.DataFrame([new_comment])
            with open(self.csv_filename, 'a', newline='', encoding='utf-8') as f:
                new_df.to_csv(f, header=f.tell() == 0, index=False)

            # Convertir el comentario a audio
            self.convert_comment_to_audio(new_comment)

            # Llamar a un método de la vista (que se maneja desde el controlador)
            self.on_comment_received(new_comment)

        try:
            await self.client.start()  # Iniciar la conexión con TikTok Live
        except ConnectionClosedError:
            print("Conexión cerrada inesperadamente. Reintentando en 5 segundos...")
            await asyncio.sleep(5)

    def convert_comment_to_audio(self, comment):
        """Convertir el comentario a voz utilizando gTTS."""
        text_to_read = f"{comment['nick_name']} dijo: {comment['comment']}"
        tts = gTTS(text=text_to_read, lang='es')
        tts.save("output.mp3")

        # Reproducir audio según el sistema operativo
        if os.name == "nt":
            os.system("start output.mp3")
        else:
            os.system("mpg321 output.mp3")

    def on_comment_received(self, comment):
        """Este método será llamado por el controlador cuando un comentario sea recibido."""
        pass  # El controlador manejará la interacción con la vista

    def stop(self):
        """Detener la conexión a TikTok Live."""
        if self.client and self.client.is_connected:
            print("Desconectando de TikTok Live...")
            self.client.stop()  # Detener la conexión de TikTok Live
        else:
            print("No hay conexión activa para detener.")
