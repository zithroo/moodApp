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
class User():
    def __init__(self):
        self.total_score = None
        self.scores = []

    def add_score(self, score, index):
        print('add_score:' + str(score) + ' in question_' + str(index))
        self.scores.append(score)
    
    def show_scores(self):
        print("catch this scores")
        sum = 0
        for score in self.scores:
            sum += score
            print(score, end= "*")
        self.total_score = sum
        print("sum  = %d" %(self.total_score))

class Home(Screen):
    pass

class Question(Screen):
    
    def __init__(self):
        super().__init__()
        self.current_answer = -1
        self.current_question = 0
        # self.total_question = len(questions)
        self.total_question = 3
        self.ids.name_question.text = questions[0]

    def get_answer(self, value):
        id = 'answer_' + str(value)
        for i in range(0, 4):
            self.ids['answer_' + str(i)].background_color = (192/255.0,192/255.0,192/255.0,1)
        self.ids[id].background_color = (128/255.0, 42/255.0, 42/255.0, 1)
        self.current_answer = value
        if(self.current_question == (self.total_question - 1)):
            self.ids.send.text = '結果'
            user.add_score(self.current_answer, self.current_question)
            self.ids.send.on_press = self.show_result

    def submit(self):
        if(self.current_answer == -1):
            print("NO input")
        else:
            if(self.current_question < (self.total_question -1)):
                user.add_score(self.current_answer, self.current_question)
                '''
                if(self.current_question == (self.total_question - 1)):
                    self.show_result()
                else:
                '''
                self.ids['answer_' + str(self.current_answer)].background_color = (192/255.0,192/255.0,192/255.0,1)
                self.current_answer = -1
                self.current_question += 1
                self.ids.name_question.text = questions[self.current_question]
                    
    def show_result(self):
        self.manager.current = 'result'
        user.show_scores()


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
    user = User()
    MyApp().run()