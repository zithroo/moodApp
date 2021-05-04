import os
from kivy.resources import resource_add_path, resource_find
from kivy.core.text import LabelBase

resource_add_path(os.path.abspath('./chinese.msyh.ttf')) #引入字體檔案
LabelBase.register('Roboto', 'chinese.msyh.ttf')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

homepage = Builder.load_file('home.kv')
Window.size = (360, 600)
class MyLayout(Widget):
    def __init__(self):
        super().__init__()
    

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()


'''
self.add_widget(Label(text='密碼: '))
self.password = TextInput(multiline=False)
self.press = Button(text = 'Click me')
'''