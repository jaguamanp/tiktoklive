import asyncio
import pandas as pd
import os
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from gtts import gTTS
from datetime import datetime
from websockets.exceptions import ConnectionClosedError

class TikTokLiveModel:
    def __init__(self, username):
        self.client = TikTokLiveClient(unique_id=username)
        self.processed_comments = set()
        self.csv_filename = None

    def start_client(self):
        """Inicia el cliente de TikTok Live"""
        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            print(f"Conectado a @{event.unique_id} (Room ID: {self.client.room_id})")

        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            self.handle_comment(event)

        async def run_client():
            while True:
                try:
                    await self.client.start()
                except ConnectionClosedError:
                    print("Conexión cerrada inesperadamente. Reintentando en 5 segundos...")
                    await asyncio.sleep(5)

        loop = asyncio.get_event_loop()
        loop.create_task(run_client())
        loop.run_forever()

    def stop_client(self):
        """Detener el cliente de TikTok Live"""
        if self.client:
            self.client.stop()  # O client.close(), según sea necesario.

    def handle_comment(self, event):
        new_comment = {"nick_name": event.user_info.nick_name, "comment": event.comment}
        
        comment_key = (new_comment['nick_name'], new_comment['comment'])
        if comment_key in self.processed_comments:
            return  

        self.processed_comments.add(comment_key)

        # Guardar en el archivo CSV
        if not self.csv_filename:
            now = datetime.now()
            formatted_date = now.strftime("%Y-%m-%d")
            self.csv_filename = f'comentarios_{self.client.unique_id}_{formatted_date}.csv'

        new_df = pd.DataFrame([new_comment])
        with open(self.csv_filename, 'a', newline='', encoding='utf-8') as f:
            new_df.to_csv(f, header=f.tell() == 0, index=False)

        # Convertir texto a voz
        text_to_read = f"{new_comment['nick_name']} dijo: {new_comment['comment']}"
        tts = gTTS(text=text_to_read, lang='es')
        tts.save("output.mp3")

        # Reproducir audio según sistema operativo
        if os.name == "nt":
            os.system("start output.mp3")
        else:
            os.system("mpg321 output.mp3")
