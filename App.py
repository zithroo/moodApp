import os
from kivy.resources import resource_add_path, resource_find
from kivy.core.text import LabelBase
resource_add_path(os.path.abspath('./chinese.msyh.ttf')) 
LabelBase.register('Roboto', 'chinese.msyh.ttf')
'''
    引入字體檔案
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import kivy.utils
from kivy.properties import ObjectProperty
'''
    引入kivy模塊
'''
main = Builder.load_file('main.kv')

with open('./question/question.txt', 'r', encoding="utf-8") as f:
    questions = f.read().splitlines()

Window.size = (360, 600) #應該要 3:5

class User():
    '''
        使用者資訊
    '''
    def __init__(self):
        self.total_score = None
        self.scores = []

    def add_score(self, score, index):
        print('add_score:' + str(score) + ' in question_' + str(index))
        self.scores.append(score)
    
    def show_scores(self):
        scores_length = len(self.scores)
        if(scores_length != len(questions)):
            print("input number wrong!")
            return
        else:
            print('total input: %d' %(scores_length))
        sum = 0
        for score in self.scores:
            sum += score
            print(score, end= "*")
        self.total_score = sum
        print("\n sum  = %d" %(self.total_score))
        self.rank()

    def rank(self):
        total_score = self.total_score
        print("心情指數:", end=" ")
        if(total_score < 13):
            rank = '第一級'
        elif(total_score < 25):
            rank = '第二級'
        elif(total_score < 37):
            rank = '第三級'
        elif(total_score < 49):
            rank = '第四級'
        else:
            rank = '第五級'
        print('In User.rank = ' + rank)
        sc = App.get_running_app().root.get_screen('result') # 取得Screen
        sc.ids.name_result.text = rank

class Home(Screen):
    pass

class Question(Screen):
    
    def __init__(self):
        super().__init__()
        self.current_answer = -1
        self.current_question = 0
        self.total_question = len(questions)
        # self.total_question = 3
        self.ids.name_question.text = questions[0]

    def get_answer(self, value):
        id = 'answer_' + str(value)
        for i in range(0, 4):
            self.ids['answer_' + str(i)].background_color = (192/255.0,192/255.0,192/255.0,1)
        self.ids[id].background_color = (128/255.0, 42/255.0, 42/255.0, 1)
        self.current_answer = value
        if(self.current_question == (self.total_question - 1)):
            self.ids.send.text = '結果'

    def submit(self):
        if(self.current_answer == -1):
            print("NO input")
        else:
            if(self.current_question < (self.total_question)):
                user.add_score(self.current_answer, self.current_question)
                # print("submit(): is answer_%d" %(self.current_question))

                if(self.current_question == (self.total_question - 1)):
                    # print("result success")
                    self.ids.send.on_press = self.show_result
                else:
                    self.ids['answer_' + str(self.current_answer)].background_color = (192/255.0,192/255.0,192/255.0,1)
                    self.current_answer = -1
                    self.current_question += 1
                    self.ids.name_question.text = questions[self.current_question]
                        
    def show_result(self):
        # result_screen = self.manager.get_screen('result')
        self.manager.current = 'result'
        user.show_scores()
        


class Result(Screen):
    def show_rank(self, rank):
        print("In Result rank:" + rank)


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