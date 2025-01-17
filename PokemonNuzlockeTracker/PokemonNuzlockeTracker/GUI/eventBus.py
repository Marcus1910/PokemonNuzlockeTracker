from kivy.event import EventDispatcher

class EventBus(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type("on_updateTrainer")
        super().__init__(**kwargs)
    
    def updateTrainerEvent(self):
        self.dispatch("on_updateTrainer")
    
    def on_updateTrainer(self, *args):
        pass

eventBus = EventBus()