from .base_page import BasePage
from PyQt5.QtWidgets import QLabel, QVBoxLayout

class MainPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_content()

    def setup_content(self):
        layout = self.layout()
        
      