from model import TikTokLiveModel
from view import TikTokLiveView

class TikTokLiveController:
    def __init__(self, root):
        self.view = TikTokLiveView(root, self)
        self.model = TikTokLiveModel(username="")

    def start(self):
        username = self.view.get_username()
        if username:
            self.model.__init__(username)
            self.model.start_client()

    def stop(self):
        self.model.stop_client()
