from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
import logging


class SnackbarHandler(logging.Handler):
    def __init__(self, text, **kwargs):
        super().__init__(*kwargs)
        self.app = MDApp.get_running_app()
    
    def emit(self, record):
        log_entry = self.format(record)
        if self.app:
            Snackbar(text=log_entry).open()