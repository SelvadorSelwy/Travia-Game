from pickle import LIST
import sys
from tkinter import CENTER
from PyQt5.QtWidgets import QLabel, QPushButton ,QGridLayout, QLineEdit,  QComboBox, QRadioButton, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
import json
import pandas as pd
import random
from database import checking_player_name, close_db, create_player, getting_player_data,save_player_score_temperarly,\
     save_player_score_Permenently,clear_current_table, checking_player_level, save_player_level, clear_progress


with open(r"lsyn.json") as my_data:
    data = json.load(my_data)
    df = pd.DataFrame(data["results"])

def preload_data(idx, current_difficulty):
    difficulty = df["difficulty"][idx]

    if difficulty != current_difficulty.lower():
        preload_data(quez_checker(random.randint(0,49)), current_difficulty )
    else:
        question = df["question"][idx]
        correct = df["correct_answer"][idx]
        incorrect = df["incorrect_answers"][idx]

        formatting=[
                ("#039","'"),
                ("&'","'"),
                ("&quot",'"'),
                ("&lt","<"),
                ("&gt",">"),
                (";",""),
            ]
        for tuple in formatting:
            question = question.replace(tuple[0], tuple[1])
            correct = correct.replace(tuple[0], tuple[1])
            incorrect = [item.replace(tuple[0], tuple[1]) for item in incorrect]

        all_answers = incorrect + [correct]
        random.shuffle(all_answers)
        parameters["difficulty"].append(difficulty)
        parameters["question"].append(question)
        parameters["correct"].append(correct)
        for i in range(len(all_answers)):
            parameters["answer"+str(i+1)].append(all_answers[i])
        print(correct)

current_difficulty= "my global difficulty"

parameters = {
    "question": [],
    "correct": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "score":[0], 
    "user_id":[],
    "difficulty": [],
    "current_player":[],
}

widgets= {
    "logo": [],
    "button": [],
    "score": [],
    "current_difficulty": [],
    "question": [],
    "answer1":[],
    "answer2":[],
    "answer3":[],
    "answer4":[],
    "about":[],
    "developer": [],
    "exit_btn": [],
    "win_message":[],
    "player_pic1":[],
    "los_message":[],
    "user_in":[],
    "user_la":[],
    "difficulty":[],
    "difficulty_label":[],
    "off_opt":[],
    "off_la":[],
    "ok_btn":[],
    "add_btn":[],
    "exit_btn":[],
    "player": [],
}

def quez_checker(index):
    if str(index) in current_player_quez:
        quez_checker(random.randint(0,49))
    else:
        current_player_quez.append(str(index))
    return int(current_player_quez[-1])

# The Main Function to Check The Answer Counting The Score and Moving The Level Up.       
def is_correct(answer):
    if answer == parameters["correct"][-1]:
        fake_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(fake_score+ 10)
        widgets["score"][-1].setText(str(parameters["score"][-1]))
        current_player_score = parameters["score"][-1]
        current_quiz_index = current_player_quez[-1]
        save_player_score_temperarly(current_player , current_quiz_index, current_player_score)
                
        if parameters["score"][-1] == 150:
            # The Easy Level has Finished , Start The Medium Level
            show_msg("You Finished this Level Successfuly, Get The Next... ", current_difficulty.lower())
            saved = save_player_score_Permenently(parameters["difficulty"][-1], True)
            if saved:
                clear_current_table()
                save_player_level( current_player, current_difficulty)
                start_game(current_player, current_difficulty)

        elif parameters["score"][-1] == 300:
            # The Medium Level has Finished , Start The Hard Level
            show_msg("You Finished this Level Successfuly, Get The Next... " , current_difficulty.lower())
            saved = save_player_score_Permenently(parameters["difficulty"][-1], True)
            if saved:
                clear_current_table()
                save_player_level( current_player, current_difficulty)
                start_game(current_player, current_difficulty)
        
        elif parameters["score"][-1] == 500:
            # Game over , Winning Board , The Hard Level has fininshed
            saved = save_player_score_Permenently(parameters["difficulty"][-1], True)
            clear_current_table()
            clear_widgets()
            winner_board()
        else:
            # Next question
            clear_widgets()
            preload_data(quez_checker(random.randint(0,49)), current_difficulty )
            question_board()
    else: 
        #return to the saved score (begining of the round)
        clear_current_table()
        clear_widgets()
        lose_board()

def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(len(widgets[widget])):
            widgets[widget].pop()

def clear_parameters():
    for parm in parameters:
        if len(parameters[parm]) >0:
            parameters[parm].pop()
            for i in range(len(parameters[parm])):
                parameters[parm].pop()
    parameters["score"].append(0)

def start_game(player, current_difficulty):
    global current_player
    global current_player_quez
    global current_player_score
    global initial_score
    # global current_quiz_index 

    if not player:
        player = parameters["current_player"][-1]
    clear_widgets()
    clear_parameters()

    current_player = getting_player_data(player)["name"]
    current_player_score = getting_player_data(current_player)["score"]
    initial_score = getting_player_data(current_player)["score"]
    current_player_quez = getting_player_data(current_player)["quiz"]

    parameters["current_player"].append(current_player)
    parameters["score"].append(current_player_score)
    
    current_quiz_index = quez_checker(random.randint(0,49))
    preload_data(current_quiz_index, current_difficulty)
    question_board()

def play_again():
    global current_difficulty
    clear_progress(current_player)

    show_msg("This will Delete You Progress, Are you sure!")
    current_difficulty= checking_player_level(current_player)
    start_game(current_player, current_difficulty)

def show_msg(msg, cur= None):
    global current_difficulty
    msg_box = QMessageBox()
    my_icon = QIcon(r"images/icon.png")
    msg_box.setWindowIcon(my_icon)
    msg_box.setWindowTitle("Selwy")
    msg_box.setText(msg)
    if cur == "easy":
        current_difficulty= "medium"
    else: current_difficulty= "hard"
    msg_box.exec_()

def check_user_id():
    global current_difficulty
    user = widgets["user_in"][-1].text()
    if not user:
        show_msg('Enter user name !!')
    else:
        if checking_player_name(user):
            current_difficulty = checking_player_level(user)
            clear_current_table()
            start_game(user, current_difficulty)
        else: 
            show_msg("You have not regestered yet, Press NEW PLAYER to registered")

def add_user():
    player = widgets["user_in"][-1].text()

    if widgets["off_opt"][-1].isChecked():
        if len(player) >= 3:
            if create_player(player):
                print(f"a new user have been added sucessfuly.\n{player}")
                widgets["user_in"][-1].setText(player)
                widgets["off_opt"][-1].setChecked(False)
                widgets["add_btn"][-1].setVisible(False)
                widgets["ok_btn"][-1].setVisible(True)
                widgets["difficulty"][-1].setCurrentIndex(1)
                print(widgets["off_opt"][-1].isChecked())
                show_msg(f"{player.upper()} has registered successfuly, press OK button to start chalange!!")
            else:  
                newUser()
        else:
            show_msg("enter a name in user id box.")
            newUser()
    else: check_user_id()

def newUser():
    print(widgets["off_opt"][-1].isChecked())
    if widgets["off_opt"][-1].isChecked():
        widgets["ok_btn"][-1].setVisible(False)
        widgets["add_btn"][-1].setVisible(True)
        return True
    else: 
        widgets["add_btn"][-1].setVisible(False)
        widgets["ok_btn"][-1].setVisible(True)

grid= QGridLayout()

def create_logo():
    image= QPixmap(r"images/logo_bottom.png")
    logo= QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin: 50px;")
    return logo

def create_label(name):
    label = QLabel(name)
    label.setStyleSheet("color: #fff; font-size: 16px; margin-bottom: 0px; margin-top: 5px;")
    label.setFixedHeight(20)
    return label

def create_button(answer):
    button = QPushButton(answer)
    button.setFixedWidth(430)
    button.setStyleSheet("*{border:3px solid #BC006C; border-radius: 15px; color: #fff; font-size: 20px; padding:10px;\
    margin:15px 10px;}"+"*:hover{background:#BC006C}")
    button.clicked.connect(lambda a: is_correct(answer))
    return button

def create_btm_logo():
    image = QPixmap(r"images/logo_bottom.png")
    logo= QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    return(logo)

def create_combobox():
    comboBox = QComboBox()
    comboBox.addItem(u"Select Difficulty")
    comboBox.addItem(u"Easy")
    comboBox.addItem(u"Medium")
    comboBox.addItem(u"Hard")
    comboBox.setDisabled(True)
    return comboBox


#First window , Login board
def login():
    logo = create_logo()
    logo.setStyleSheet("padding: 5px; margin: 5px auto;")
    widgets["logo"].append(logo)

    about_la = create_label(" Are You Interesting in Information Technology? \nSo.. \nTest Your Knowledge.")
    about_la.setStyleSheet(" padding:5px; border-radius: 15px;\
     margin: 5px auto; color: #161219; background:#eee; font-size: 14px; max-height:300px;")
    about_la.setAlignment(QtCore.Qt.AlignCenter)

    widgets["about"].append(about_la)

    user_la = create_label("User Name")
    widgets["user_la"].append(user_la)

    user_in = QLineEdit()
    user_in.setStyleSheet("background:#eee; padding:5px; margin-top:0px ; margin-left:4px;\
    max-width:300px; border: 1px solid #000; border-radius:10px; font-size: 20px")
    
    widgets["user_in"].append(user_in)

    difficulty_c = create_combobox()
    difficulty_c.setStyleSheet("background:#eee; padding:5px; margin-top:0px ; margin-left:4px;\
    max-width:300px; border: 1px solid #000; border-radius:10px; font-size: 20px")
    
    widgets["difficulty"].append(difficulty_c)

    difficulty_label = create_label("Difficulty")
    widgets["difficulty_label"].append(difficulty_label)

    off_opt = QRadioButton()
    off_opt.setStyleSheet(" margin-right:0px; margin-left:10px;height: 30px;")
    off_opt.setGeometry(200, 150, 120,40)
    off_opt.toggled.connect(newUser)
    
    widgets["off_opt"].append(off_opt)

    off_la = create_label("New Player")
    off_la.setStyleSheet("margin-top: 10p; margin-left: 0px; font-size: 16px; color: #fff; padding: 10px 0px; max-height: 30px;")

    off_la.setGeometry(200, 200, 150, 40)
    widgets["off_la"].append(off_la)

    ok_btn = QPushButton("OK")
    ok_btn.setFixedSize(150, 80)
    ok_btn.setStyleSheet("*{border:3px solid #BC006C; border-radius: 15px; color: #fff; font-size: 20px; padding:10px;\
    margin:15px 10px;}"+"*:hover{background:#BC006C}")
    ok_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    ok_btn.clicked.connect(check_user_id)
    widgets["ok_btn"].append(ok_btn)

    add_btn = QPushButton("Add User")
    add_btn.setFixedSize(150, 80)
    add_btn.setStyleSheet("*{border:3px solid #BC006C; border-radius: 15px; color: #fff; font-size: 20px; padding:10px;\
    margin:15px 10px;}"+"*:hover{background:#BC006C}")
    add_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    add_btn.clicked.connect(lambda u: add_user())
    add_btn.setVisible(False)
    widgets["add_btn"].append(add_btn)

    exit_btn = QPushButton("Exit")
    exit_btn.setFixedSize(150, 80)
    exit_btn.setStyleSheet("*{border:3px solid #BC006C; border-radius: 15px; color: #FFF; font-size: 20px; padding:10px;\
    margin:15px 10px;}"+"*:hover{background:#BC006C;}")
    exit_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    widgets["exit_btn"].append(exit_btn)
    exit_btn.clicked.connect(sys.exit)
    
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2, QtCore.Qt.AlignLeft )
    grid.addWidget(widgets["about"][-1], 7, 0, 1, 2)
    grid.addWidget(widgets["user_la"][-1], 1, 0)
    grid.addWidget(widgets["user_in"][-1], 2,0,1,2)
    grid.addWidget(widgets["difficulty_label"][-1], 3,0)
    grid.addWidget(widgets["difficulty"][-1], 4,0,1,2)
    grid.addWidget(widgets["off_opt"][-1], 5,0, QtCore.Qt.AlignLeft)
    grid.addWidget(widgets["off_la"][-1], 5, 0, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["ok_btn"][-1], 6, 0, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["add_btn"][-1], 6, 0, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["exit_btn"][-1], 6, 1, QtCore.Qt.AlignCenter)


# QUISTION WINDOW - MAIN WINDOW 
def question_board():
    player= QLabel(parameters["current_player"][-1])
    player.setFixedSize(250, 60)
    player.setStyleSheet(" padding:10px; border-radius: 5%;\
     margin: 30px; color: #BC006C; font-size: 25px; font-weight:500; max-width:250px; max-height:100px;\
     text-transform: uppercase; letter-spacing: 1px;")
    player.setAlignment(QtCore.Qt.AlignCenter)

    current_difficulty_label= QLabel(current_difficulty)
    current_difficulty_label.setFixedSize(250, 60)
    current_difficulty_label.setStyleSheet(" padding:10px; border-radius: 5%;\
     margin: 30px; color: #BC006C; font-size: 25px; font-weight:500; max-width:250px; max-height:100px;\
     text-transform: uppercase; letter-spacing: 1px;")
    current_difficulty_label.setAlignment(QtCore.Qt.AlignCenter)
    
    score= QLabel(str(parameters["score"][-1]))
    score.setFixedSize(160, 160)
    score.setStyleSheet("border:4px solid #BC006C; border-radius: 50%; padding:10px;\
     margin: 30px; color: #BC006C; font-size: 30px; font-weight:500; max-width:250px; max-height:250px;")
    score.setAlignment(QtCore.Qt.AlignCenter)

    question = QLabel(parameters["question"][-1])
    question.setStyleSheet("background: #fff; border-radius:3px; padding: 10px; margin: 10px;\
     font-size: 16px;  max-width: 900px")
    question.setWordWrap(True)
    question.setAlignment(QtCore.Qt.AlignCenter)

    button1 = create_button(parameters["answer1"][-1])
    button2 = create_button(parameters["answer2"][-1])
    button3 = create_button(parameters["answer3"][-1])
    button4 = create_button(parameters["answer4"][-1])

    logo= create_btm_logo()

    developer = QLabel("Developed By Abdulbaset Selwy 2022")
    developer.setAlignment(QtCore.Qt.AlignCenter)
    developer.setStyleSheet("color:#BC006C")

    widgets["player"].append(player)
    widgets["current_difficulty"].append(current_difficulty_label)
    widgets["score"].append(score)
    widgets["question"].append(question)
    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)
    widgets["logo"].append(logo)

    widgets["developer"].append(developer)
    grid.addWidget(widgets["player"][-1], 0, 0, QtCore.Qt.AlignLeft)
    grid.addWidget(widgets["current_difficulty"][-1], 0, 1, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["score"][-1],0, 1, QtCore.Qt.AlignRight)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets["logo"][-1], 4, 0,1 , 2, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["developer"][-1], 5, 0, 1, 2, QtCore.Qt.AlignCenter)


#LOSE THE GAME, GIVE A WRONG ANSWER
def lose_board():
    
    los_message = QLabel("Sorry, This answer was wrong..\nYour Score is")
    los_message.setStyleSheet("font-size:30px; color: #fff; padding:20px, 20px")

    score= QLabel(str(initial_score))
    score.setStyleSheet("padding:10px; color: #fff; font-size: 50px; font-weight:700; max-width:250px;")

    button= QPushButton("Try again")
    button.setFixedWidth(300)
    button.setStyleSheet("*{border:3px solid #BC006C; border-radius: 15px; color: #fff; font-size: 25px; padding:10px;\
    margin:10px; }"+"*:hover{background:#BC006C}")

    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(lambda x: start_game(current_player, current_difficulty))
    
    logo= create_btm_logo()

    developer = QLabel("Developed By Abdulbaset Selwy 2022")
    developer.setAlignment(QtCore.Qt.AlignCenter)
    developer.setStyleSheet("color:#BC006C")

    widgets["los_message"].append(los_message)
    widgets["score"].append(score)
    widgets["button"].append(button)
    widgets["logo"].append(logo)
    widgets["developer"].append(developer)

    grid.addWidget(los_message, 0, 0)
    grid.addWidget(widgets["score"][-1], 1, 0, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["button"][-1], 2, 0, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["logo"][-1], 4, 0, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["developer"][-1], 3, 0, QtCore.Qt.AlignCenter)
    
# WINING THE GAME 
def winner_board():
    picture = QPixmap(r"images/Os2.jpg")
    player_pic1 = QLabel()
    player_pic1.setPixmap(picture)
    player_pic1.setAlignment(QtCore.Qt.AlignCenter)

    win_message = QLabel(f'Congretulation\n{parameters["current_player"][-1]}\nYou win.')
    win_message.setStyleSheet("font-size:40px; color: #fff; padding:10px; margin:40px 2px 40px 5px;")
    score= QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("margin: 40px 5px; color: #fff; font-size: 50px; font-weight:700;")
    score.setAlignment(QtCore.Qt.AlignLeft)

    button= QPushButton("Play again")
    button.setFixedWidth(180)
    button.setStyleSheet("*{border:3px solid #BC006C; border-radius: 15px; color: #fff; font-size: 25px; padding:10px 2px;\
    margin:10px 0px 0px 10px; }"+"*:hover{background:#BC006C}")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    exit_btn= QPushButton("Exit")
    exit_btn.setFixedWidth(180)
    exit_btn.setStyleSheet("*{border:3px solid #BC006C; border-radius: 15px; color: #fff; font-size: 25px; padding:10px 2px;\
    margin:10px 0px 0px;}"+"*:hover{background:#BC006C}")
    exit_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    developer = QLabel("Developed By Abdulbaset Selwy 2022")
    developer.setAlignment(QtCore.Qt.AlignCenter)
    developer.setStyleSheet("color:#BC006C")
    
    logo= create_logo()
    # logo.setStyleSheet("margin: 50px 5px;")

    button.clicked.connect(play_again)
    exit_btn.clicked.connect(close_db)
    exit_btn.clicked.connect(sys.exit)

    widgets["player_pic1"].append(player_pic1)
    widgets["win_message"].append(win_message)
    widgets["score"].append(score)
    widgets["button"].append(button)
    widgets["exit_btn"].append(exit_btn)
    widgets["developer"].append(developer)
    widgets["logo"].append(logo)

    grid.addWidget(widgets["player_pic1"][-1], 0, 2, 5, 2 )
    grid.addWidget(widgets["win_message"][-1], 0, 0, 2, 2)
    grid.addWidget(widgets["score"][-1], 1, 1, 1, 1 )
    grid.addWidget(widgets["button"][-1], 2, 0, QtCore.Qt.AlignLeft)
    grid.addWidget(widgets["exit_btn"][-1], 2, 1, QtCore.Qt.AlignLeft)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2, QtCore.Qt.AlignCenter)
    grid.addWidget(widgets["developer"][-1], 4, 0, 1 , 2, QtCore.Qt.AlignCenter)