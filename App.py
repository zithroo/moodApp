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

import random
import time
'''
    引入繪圖模塊
'''
import matplotlib.pyplot as plt
'''
    引入kivy模塊
'''
main = Builder.load_file('main.kv')

try:
    with open('./question/question.txt', 'r', encoding="utf-8") as f:
        questions = f.read().splitlines()
except FileNotFoundError:
    print("please check the folder ./question")
    print("there may be no file named question.txt")
    exit(1)
'''
    引入問卷檔案
'''

Window.size = (650, 700) # 設定視窗大小 360:600

class User():
    '''
        使用者資訊，提供問卷結果的分級和資料紀錄

        :Events:
            `add_score`: (score, index)
            將每題提交的分數加入
            `show_result`: ()
            顯示所有的user屬性，跳至Screen: result，並顯現結果
            `rank`: ()
            return str
            將總分進行分級，回傳分級結果
            `get_image`: (rank_nuber)
            return str
            依照rank_number提供隨機的檔案路徑
            `record`: (time, total_score)
            將時間和總分數寫入./user/record.txt
            `reset`: ()
            重置資料
    '''

    def __init__(self):
        self.total_score = None # 計算總得分
        self.scores = [] # 儲存每一個題目的答案
        self.rank_number = None # 儲存處立後的結果
        self.time = None # 紀錄填完問卷當下時間

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
    
    def show_result(self):
        scores_length = len(self.scores)
        if(scores_length != len(questions)):
            print("input number wrong!")
            return
        else:
            print('Success! total input: %d' %(scores_length))
        self.time = time.strftime("%m-%d %H:%M:%S", time.localtime())
        sum = 0
        for score in self.scores:
            sum += score
        self.total_score = sum
        rank = self.rank()
        sc = App.get_running_app().root.get_screen('result') # 取得Screen
        sc.ids.name_result.text = rank
        random_image_path = self.get_image(self.rank_number)
        sc.ids.name_image.source = random_image_path
        # print(type(App.get_running_app().root))
        print("------------------------------")
        print("User.show_result() Success!")
        print("user.total_score: %d" %(self.total_score))
        print("user.scores: " + str(self.scores))
        print("user.rank_number: %d" %(self.rank_number))
        print("user.time: " + self.time)
        user.record(self.time, self.total_score)
        
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
        return rank
    
    def get_image(self, rank_number):
        print("get_image in image/class_" + str(rank_number))
        path = "image/class_" + str(rank_number)
        dirs = os.listdir(path)
        file_numbers = len(dirs)
        random_image_path = path + '/' + dirs[random.randint(0, file_numbers - 1)]
        return random_image_path

    def record(self, time, total_score):
        try:
            with open('./user/record.txt', 'a', encoding="utf-8") as f:
                f.write(time + '/' + str(total_score) + '\n')
            print("user.record Success")
        except FileNotFoundError:
            print("please check the folder ./user")
            print("there may be no file named record.txt")
            exit(1)
        
    def reset(self):
        self.rank_number = None
        self.total_score = None
        self.scores = []
        self.time = None
        print("user reset!")
        

class Home(Screen):
    '''
        首頁，將頁面轉至Quesiotion
        :Events:
            `show_record`: ()
            顯示最近五次紀錄的圖表
    '''
    def __init__(self):
        super().__init__()

    def show_record(self):
        print("home.show_record()")
        try:
            with open('./user/record.txt', 'r', encoding="utf-8") as f:
                records = f.readlines()
            data_x = []
            data_y = []
            
            length = len(records)
            if(length > 5):
                for line in range(length - 5, length):
                    record = records[line].split('/')
                    data_x.append(record[0])
                    data_y.append(int(record[1].strip()))
            else:
                for line in records:
                    record = line.split('/')
                    data_x.append(record[0])
                    data_y.append(int(record[1].strip()))
            
            print(data_x)
            print(data_y)
            bottom = min(data_y) - (min(data_y) % 5)
            top = max(data_y) + (5 - (max(data_y) %5))
            plt.plot(data_x, data_y, 'b-*') #畫線
            plt.title("Record", fontsize=24) #圖表標題
            plt.xlabel("time", fontsize=16) #x軸標題
            plt.ylim(bottom, top)
            plt.ylabel("Mood index", fontsize=20) #y軸標題
            try:
                os.remove('./user/record.jpg')
            except OSError as e:
                print(e)
            else:
                print("File is deleted successfully")
            plt.savefig('./user/record.jpg')
            # plt.show() #顯示繪製的圖形
            sc = App.get_running_app().root.get_screen('record') # 取得Screen
            sc.ids.name_image.reload()

        except FileNotFoundError:
            print("please check the folder ./user")
            print("there may be no file named record.txt")
            exit(1)


class Question(Screen):
    '''
        填寫問題的頁面，用以提交問題及將頁面轉至Result

        :Events:
            `get_answer`: (value)
            儲存使用者按下的答案按鈕，儲存至User.scores，並將選取的答案變色，若是已經到最後一題，
            則改變提交按鈕的文字為'結果'
            `submit`: ()
            提交每一題的答案至User，並跳到下一題
            若已經為最後一題，則顯現結果
            `goto_previous`:()
            回到上一題，若已經為第一題則重置
            `reset_button‵:()
            將answer的button顏色重置
            `reset`: ()
            重置Screen: question
    '''
    def __init__(self):
        super().__init__()
        self.current_answer = None # 目前的問題
        self.current_question = 0 # 目前的答案
        self.total_question = len(questions) # 問題的個數
        self.ids.name_question.text = questions[0] # 取得 id: name_question物件 並改變其文字

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
            user.show_result()

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
    '''
        顯示結果的頁面

        :Events:
            `restart`: ()
            重置Screen: result
    '''
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

class Record(Screen):
    '''
        顯示紀錄的頁面
    '''
    pass

class MoodApp(App):
    '''
        App本身
        加入ScreenManager，以及三個Screen
    '''
    def build(self):
        Window.clearcolor = kivy.utils.get_color_from_hex('#ffffe0')
        sm = ScreenManager()
        sm.add_widget(Home())
        sm.add_widget(Question())
        sm.add_widget(Result())
        sm.add_widget(Record())
        return sm

if __name__ == '__main__':
    user = User()
    MoodApp().run()
    