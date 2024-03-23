from flask import Flask, request, jsonify
import sqlite3
import sys
sys.path.append(r'C:\Users\sange\PycharmProjects\pythonProject4\TicTacToe.py')
import TicTacToe
sys.path.append(r'C:\Users\sange\PycharmProjects\pythonProject4\Database.py')
from Database import Database
import random

app = Flask(__name__)
print(__name__)
dic = {}


def object_create(objc = None):
    if objc == None:
        objc = TicTacToe.TicTacToe()
    return objc


@app.route('/tictactoe')
def welcome():
    return ("Welcome to TicTacToe!")


@app.route('/tictactoe/next')
def game_id_inst():
    return ("If you have game id, enter the game id, else start the game")


class Sqlite(Database):
    def add_player_details(self, name, number, mail_id):
        con = sqlite3.connect('TicTacToe.db')
        cursor = con.cursor()
        token = random.randint(1000, 9999)
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY, name TEXT, token INTEGER, number INTEGER, mail_id TEXT, score INTEGER)''')

        cursor.execute("INSERT INTO users (name, token, number, mail_id, score) VALUES (?, ?, ?, ?, ?)", (name, token, number, mail_id, 0))
        con.commit()
        con.close()

    def game_history(self, game_id, player_1, player_2, status):
        con = sqlite3.connect('TicTacToe.db')
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS history
                         (id INTEGER, game_id INTEGER, player_1 INTEGER, player_2 INTEGER, Winner TEXT)''')
        cursor.execute("INSERT INTO history (game_id, player_1, player_2, Winner) VALUES (?, ?, ?, ?)", (game_id, player_1, player_2, status))
        con.commit()
        con.close()


    def table_id(self, game_id, obj):
        con = sqlite3.connect('TicTacToe.db')
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS table_id
                                 (game_id INTEGER , obj TEXT)''')
        cursor.execute("INSERT INTO table_id (game_id, obj) VALUES (?, ?)",
                       (game_id, obj))
        con.commit()
        con.close()


    def leader_board(self):
        con = sqlite3.connect('TicTacToe.db')
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM users ORDER BY score ASC''')
        con.commit()
        con.close()


objec = Sqlite()


@app.route('/tictactoe/game')
def game():
    return "Game not started yet, Start the game!!!"


@app.route('/tictactoe/game/start/<player_1>/<player_2>')
def creating_obj(player_1, player_2):
    obj = object_create()
    obj.status = "Started"
    game_id = random.randint(100, 999)
    dic[game_id] = obj
    print(dic)
    players = player_1 + "," + player_2
    return jsonify({'status': "Game started" , players + " game_id" : game_id})


@app.route('/tictactoe/options')
def options():
    obj = TicTacToe.TicTacToe()
    return obj.options()


@app.route('/tictactoe/game/<options>/post', methods= ['POST', 'GET'])
def select_option(options):
    obj = TicTacToe.TicTacToe()
    details = request.json
    if options == str(1):
        print(details)
        for key, value in details.items():
            if key == "name":
                name = value.lower()

            elif key == "number":
                mobile = int(value)

            elif key == "mail_id":
                mail_id = value.lower()

        objec.add_player_details(name, mobile, mail_id)

        return jsonify({"status" : "Your details added successfully"})

    elif options == str(2):
        return "Leader Board"

    return obj.options_and_its_functions(int(options))



@app.route('/tictactoe/<game_id>/<player_1>/<player_2>/post', methods = ['POST', 'GET'])
def json_format(game_id, player_1, player_2):
    data = request.json
    game_id = int(game_id)
    obj = dic[game_id]
    print("Before : ", obj.game_arr)
    if obj.status == "Started":
        #p_1 = id_select(player_1)
        #p_2 = id_select(player_2)
        print(data)
        for key, value in data.items():
            print(key, value)
            if key == "userid":
                userid = value
            if key == "row":
                row = value
            if key == "column":
                column = value
        main_func, user_id = obj.gplay(int(userid), int(row), int(column), int(player_1), int(player_2))
        print("After : ", obj.game_arr)
        if main_func == "Win":
            increment_value(user_id)
            obj.status = "Ended"
            del dic[game_id]
            objec.game_history(game_id, player_1, player_2, user_id)
            return jsonify({"status" : "Win"})

        if main_func == "Match Draw":
            objec.game_history(game_id, p_1, p_2, -1)
            obj.status = "Ended"
            del dic[game_id]
            return jsonify({"status" : "Draw"})

        if main_func == "You can't place here":
            return jsonify({"Error" : "The Block is already occupied"})
        return jsonify({"status" : "Playing"})
    elif obj.status == "Not started" or obj.status == "Ended":
        object_create()

        return jsonify({"Msg" : "Please start the game"})


def id_select(mail):
    con = sqlite3.connect("TicTacToe.db")
    cursor = con.cursor()
    i_d = cursor.execute(f'''SELECT id FROM users WHERE mail_id = ?''', (mail,))
    results = cursor.fetchall()

    con.commit()
    con.close()
    return results[0][0]



def add_column(name, type, file_name, table_name):
    con = sqlite3.connect(file_name)
    cursor = con.cursor()
    alter = f"ALTER TABLE {table_name} ADD COLUMN {name} {type}"
    cursor.execute(alter)
    con.commit()
    con.close()

'''
add_column_option = input("Do you need to add column?(Yes/No) : ")
if add_column_option == "Yes":
    column_name = input("Table Name : ")
    name = input("Column Name : ")
    type = input("Data Type : ")
    file_name = input("File Name : ")

    add_column(name, type, file_name, column_name)'''




def choose_option(option, nam = None, num = None, mail = None, player_1 = None, player_2 = None, status = -1):
    if option == 1:
        objec.add_player_details(nam, num, mail)

    elif option == 2:
        objec.game_history(player_1, player_2, status)


def increment_value(game_id):
    con = sqlite3.connect('TicTacToe.db')
    cursor = con.cursor()
    cursor.execute('''UPDATE users SET score = score + 1 WHERE id = ?''', (game_id,))
    con.commit()
    con.close()

if __name__ == '__main__':
    app.run( host="0.0.0.0")