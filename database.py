import sqlite3

db= sqlite3.connect("users.db")
cr = db.cursor()

cr.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE ,\
     name TEXT UNIQUE, level TEXT , score INTEGER)")
cr.execute("CREATE TABLE IF NOT EXISTS question (quez_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE ,\
difficulty TEXT , quiz_index TEXT, user_id INTEGER NOT NULL)" )
cr.execute("CREATE TABLE IF NOT EXISTS current (user_id INTEGER NOT NULL, name INTEGER, quiz_index TEXT , score INTEGER)")


def clear_progress(user):
    
    user_id_state= ("Select user_id FROM USERS WHERE name = ?")
    cr.execute(user_id_state, (user,))
    get_user_id = cr.fetchone()[0]

    quez_del_statement = ("DELETE  FROM question WHERE user_id = ?")
    
    cr.execute(quez_del_statement, (get_user_id,) )

    score_update_statement = "UPDATE users SET (level , score) = (?, ?) WHERE user_id = ?"
    parameters = ( "easy", 0, get_user_id)
    cr.execute(score_update_statement, parameters)

    db.commit()

def clear_current_table():
    cr.execute("DELETE  FROM current")
    db.commit()

def save_player_score_Permenently(cur_dif, save = False):
    if save:
        cr.execute("SELECT * FROM current")
        data = cr.fetchall()
        for row in data:
            update_player_data(row[0], row[2], row[3] , cur_dif)
        return True

def save_player_score_temperarly(current_player, q_index, current_score):
    #getting user id 
    user_id_state= ("Select user_id FROM USERS WHERE name = ?")
    cr.execute(user_id_state, (current_player,))
    get_user_id = cr.fetchone()[0]

    current_statement = "INSERT INTO current (user_id, name, quiz_index, score) VALUES (?, ?, ?, ? )"
    params = (get_user_id, current_player , q_index,  current_score)

    cr.execute(current_statement, params)

    db.commit()
        

def getting_player_data(user):
    q_state =("select users.name, users.level, users.score, question.quiz_index from users join question on users.user_id = question.user_id\
     where users.name = ?")

    cr.execute(q_state, (user,) )
    quiz_result = cr.fetchall()
    user_quiz = []
    user_quiz_dic= {}
    if len(quiz_result) > 0:
        for quiz in quiz_result:
            user_quiz.append(quiz[3])
        user_quiz_dic["name"] = quiz[0]
        user_quiz_dic["level"] = quiz[1]
        user_quiz_dic["score"] = quiz[2]
        user_quiz_dic["quiz"] = user_quiz
    else:
        user_quiz_dic["name"] = user
        user_quiz_dic["score"] = 0
        user_quiz_dic["quiz"] = user_quiz
    return user_quiz_dic   

def update_player_data( user_id, q_index, current_score , cur_dif):    
    #Adding new row in question table 
    update_state = ("INSERT INTO  question ( difficulty, quiz_index,  user_id) VALUES (?, ?, ?) ")
    params = (cur_dif, q_index, user_id)
    cr.execute(update_state, params)

    #updting score for current user
    score_update_statement = "UPDATE users SET (level , score) = (?, ?) WHERE user_id = ?"
    parameters = ( cur_dif, current_score, user_id)
    cr.execute(score_update_statement, parameters)

    db.commit()

def save_player_level( user, cur_dif):
    user_id_state= ("Select user_id FROM USERS WHERE name = ?")
    cr.execute(user_id_state, (user,))
    get_user_id = cr.fetchone()[0]

    #updting score for current user
    score_update_statement = "UPDATE users SET (level) = (?) WHERE user_id = ?"
    parameters = ( cur_dif, get_user_id)
    cr.execute(score_update_statement, parameters)

    db.commit()

def checking_player_name(user):
    cr.execute("SELECT name FROM users")
    result = cr.fetchall()
    for tuple in result:
        if (user in tuple[0]):
            return True
    else:
        return False

def checking_player_level(user):

    user_id_state= ("Select user_id FROM USERS WHERE name = ?")
    cr.execute(user_id_state, (user,))
    get_user_id = cr.fetchone()[0]

    level_state= ("SELECT level FROM USERS WHERE user_id = ? ")
    cr.execute(level_state, (get_user_id,))

    result = cr.fetchall()
    return result[0][0]   

def create_player(player):
    if player:
        if checking_player_name(player):
            print("This name is not valid , try another name")
            return False
        else:
            create_st = "INSERT INTO users (name, level, score) VALUES (?, ?, ?)  "
            sqlparams = (player, "easy", 0)
            cr.execute(create_st, sqlparams)
            db.commit()
            return True
    
def close_db():
    db.commit()
    db.close()
if __name__ == "__main__":
    # save_player_score_Permenently(True)
    checking_player_level("Sel")
    checking_player_level("you")

    db.close()