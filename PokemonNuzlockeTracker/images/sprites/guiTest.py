from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

class OverlayLayoutApp(App):
    def build(self):
        float_layout = FloatLayout()

        # Create a Button
        button = Button(text='Button')
        float_layout.add_widget(button)  # Add the button to the FloatLayout

        # Create a BoxLayout to overlay on top of the button
        overlay_layout = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.5))
        label = Label(text = "label", pos_hint = {"right": 1}, color = (1, 1, 1, 1))
        overlay_layout.add_widget(label)
        float_layout.add_widget(overlay_layout)  # Add the overlay to the FloatLayout

        return float_layout

if __name__ == '__main__':
    OverlayLayoutApp().run()
