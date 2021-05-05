import os
from kivy.resources import resource_add_path, resource_find
from kivy.core.text import LabelBase

resource_add_path(os.path.abspath('./chinese.msyh.ttf')) #引入字體檔案
LabelBase.register('Roboto', 'chinese.msyh.ttf')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import kivy.utils
with open('./question/question.txt', 'r', encoding="utf-8") as f:
    questions = f.read().splitlines()

# from kivy.uix.image import Image
# from kivy.properties import ObjectProperty
'''
homepage = Builder.load_file('home.kv')
question = Builder.load_file('question.kv')
result = Builder.load_file('result.kv')
'''
main = Builder.load_file('main.kv')
Window.size = (360, 600)

class Home(Screen):
    pass

class Question(Screen):
    def get_answer(self, value):
        try:
            int(value)
            print(value)
            
        except:
            print("wrong value: " + value)

class Result(Screen):
    pass

class MyApp(App):
    def build(self):
        Window.clearcolor = kivy.utils.get_color_from_hex('#ffffe0')
        sm = ScreenManager()
        sm.add_widget(Home())
        sm.add_widget(Question())
        sm.add_widget(Result())
        return sm

if __name__ == '__main__':
    MyApp().run()

'''
    canvas.before:
        Color:
            rgba: utils.get_color_from_hex('#ffffe0')
        Rectangle:
            pos: self.pos
            size: self.size
'''