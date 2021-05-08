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
'''
    引入問題檔案
'''
import random
Window.size = (650, 700) #應該要 360:600

class User():
    '''
        使用者資訊，提供問卷結果的分級和資料紀錄

        :Events:
            `add_score`: (score, index)
            將每題提交的分數加入
            `show_score`: ()
            顯示所有的分數及總分
            `rank`: ()
            將總分進行分級並回饋
    '''

    def __init__(self):
        self.total_score = None
        self.scores = []
        self.rank_number = None

    def add_score(self, score, index):
        try:
            self.scores[index] = score
            print('add_score:' + str(score) + ' in question_' + str(index) + ' with update')
        except IndexError:
            self.scores.append(score)
            print('add_score:' + str(score) + ' in question_' + str(index) + ' with append')
        except:
            print("user.addscore unexpected error: ")
            print(self.scores)
            print(index)
    
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
            self.rank_number = 1
        elif(total_score < 25):
            rank = '第二級'
            self.rank_number = 2
        elif(total_score < 37):
            rank = '第三級'
            self.rank_number = 3
        elif(total_score < 49):
            rank = '第四級'
            self.rank_number = 4
        else:
            rank = '第五級'
            self.rank_number = 5
        print('In User.rank = %d' %(self.rank_number))
        sc = App.get_running_app().root.get_screen('result') # 取得Screen
        sc.ids.name_result.text = rank
        random_image_path = self.get_image(self.rank_number)
        sc.ids.name_image.source = random_image_path
        # print(type(App.get_running_app().root))
    
    def get_image(self, rank_number):
        print("get_image in image/class_" + str(rank_number))
        path = "image/class_" + str(rank_number)
        dirs = os.listdir(path)
        '''
        for file in dirs:
            print(file)
        '''
        file_numbers = len(dirs)
        random_image_path = path + '/' + dirs[random.randint(0, file_numbers - 1)]
        return random_image_path

    def reset(self):
        self.rank_number = None
        self.total_score = None
        self.scores = []
        print(self.total_score)
        print(self.scores)
        print("user reset!")
        

class Home(Screen):
    pass

class Question(Screen):
    '''
        填寫問題的頁面，用以提交問題及將頁面轉至Result

        :Events:
            `get_answer`: (value)
            儲存使用者按下的答案按鈕，並將選取的答案變色，若是已經到最後一題，
            則改變提交按鈕的文字為'結果'
            `submit`: ()
            提交每一題的答案至User，並跳到下一題
            若已經為最後一題，則顯現結果
    '''
    def __init__(self):
        super().__init__()
        self.current_answer = None
        self.current_question = 0
        self.total_question = len(questions)
        self.ids.name_question.text = questions[0]

    def get_answer(self, value):
        if(self.current_question == (self.total_question - 1)):
            self.ids.send.text = '結果'
        id = 'answer_' + str(value)
        self.reset_button()
        self.ids[id].background_color = (128/255.0, 42/255.0, 42/255.0, 1)
        self.current_answer = value
        user.add_score(self.current_answer, self.current_question)
        

    def submit(self):
        if(self.current_answer == None):
                print('current answer == None')
                return
        self.reset_button()
        print("current_question: %d" %(self.current_question))
        print("len in user scores: %d"%(len(user.scores)))
        self.ids['answer_' + str(self.current_answer)].background_color = (192/255.0,192/255.0,192/255.0,1)
        if(self.ids.send.text == '結果'):
            print("show_result is working")
            self.manager.current = 'result'
            user.show_scores()

        elif(self.ids.send.text == '下一題'):
            self.ids.previous.text = '上一題'
            if(self.current_question < self.total_question):
                self.current_question += 1
                self.ids.name_question.text = questions[self.current_question]
                try:
                    self.ids['answer_' + str(user.scores[self.current_question])].background_color = (128/255.0, 42/255.0, 42/255.0, 1)
                except:
                    self.current_answer = None
                if(len(user.scores) == self.total_question):
                    self.ids.send.text = '結果'
            else:
                print("出大事了")
        else:
            print('some unexpect error of send text' + self.ids.send.text)

    def goto_previous(self):
        self.ids.send.text = '下一題'
        if(self.ids.previous.text == '回首頁'):
            print("go back to home in question.goto_previous")
            sc = App.get_running_app().root.get_screen('result')
            sc.restart()
        else:
            if(self.current_question == 1):
                self.ids.previous.text = '回首頁'

            if(self.current_question > 0):
                self.current_question -= 1
                self.ids.name_question.text = questions[self.current_question]
                print("goto_previous: current.question: %d" %(self.current_question))
                try:
                    self.reset_button()
                    self.current_answer = user.scores[self.current_question]
                    print("goto_previous: current.answer: %d" %(self.current_answer))
                    self.ids['answer_' + str(self.current_answer)].background_color = (128/255.0, 42/255.0, 42/255.0, 1)

                except IndexError:
                    print("IndexError of user.scores[%d]" %(self.current_question))
                except:
                    print("goto previous unexpect error")


    def reset_button(self):
        for i in range(0, 4):
            self.ids['answer_' + str(i)].background_color = (192/255.0,192/255.0,192/255.0,1)
        

    def reset(self):
        self.current_answer = None
        self.current_question = 0
        self.ids.name_question.text = questions[0]
        self.reset_button()
        self.ids.send.text = '下一題'
        self.ids.previous.text = '回首頁'
        print("question.reset success")


class Result(Screen):
    def __inti__(self):
        super().__init__()
        self.rank_number = None

    def restart(self):
        self.manager.current = 'home'
        self.manager.transition.direction = 'right'
        self.rank_number = None
        question_screen = self.manager.get_screen('question')
        user.reset()
        question_screen.reset()


class MoodApp(App):
    def build(self):
        Window.clearcolor = kivy.utils.get_color_from_hex('#ffffe0')
        sm = ScreenManager()
        sm.add_widget(Home())
        sm.add_widget(Question())
        sm.add_widget(Result())
        return sm

if __name__ == '__main__':
    user = User()
    MoodApp().run()
    