import time


class TicTacToe:
    def __init__(self):
        self.player_arr = []
        player_det = open("PlayersDataFile.txt")
        for details in player_det:
            self.player_arr.append(details.split(","))
        player_det.close()  

        self.game_history_arr = []
        game_hist = open("GameHistory.txt")
        for history in game_hist:
            self.game_history_arr.append(history.split(","))
        game_hist.close()
        self.arr = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.game_arr = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.status = "Not started"

    def add_new_players(self):
        name     = input("Enter your Name   : ")
        number   = int(input("Enter your Number : "))
        email_id = input("Enter your Email  : ")
        self.player_arr.append([name, number, email_id, "0", "\n"])


    '''def arr(self):

        for row in range(3):
            for column in range(3):
                print(-1, "\t", end="")
            print("\n")
        return self.game_arr'''


    def game_running(self, number, row, column,player_1, player_2):
        game_status = self.game_play(number, row, column, player_1, player_2)
        if game_status == "Win":
            return game_status
        elif game_status == "You can't place here":
            return game_status
        if self.game_draw_details() == "Match Draw":
            return "Match Draw"

        self.print_arr()
        return "Playing"

    def add_to_game_history(self, player, p1, p2, date_time):
        winner = player + " wins the game"
        print(winner)
        self.game_history_arr.append([p1, p2, winner, date_time])
        self.game_history()
        self.add_points(player)

    def game_draw_details(self):
        for row in self.game_arr:
            for column in row:
                if column == -1:
                    return "Not draw"
        self.print_arr()
        print("Match Draw")
        return "Match Draw"

    def assign_input(self, row, column, number):
        while True:
            '''if row >= len(game_arr) or column >= len(game_arr):
                print("Give input within n")
                continue'''

            if self.game_arr[row][column] == -1:
                self.game_arr[row][column] = number
                return "Playing"

            else:
                print("You can't place here\n Place in another block")
                return "You can't place here"

    def game_play(self, number, row, column, player_1, player_2):
        status = self.assign_input(row, column, number)
        if status != "Playing":
            return status
        if self.check(number) == "Win":
            if number == 0:
                print("user_id", player_1, " wins the game")
            else:
                print("user_id", player_2, " wins the game")
            return "Win"
        return "Playing"

    def check(self, number):
        indices = [self.game_arr[0][0], self.game_arr[0][1], self.game_arr[0][2], self.game_arr[1][0],
                   self.game_arr[1][1], self.game_arr[1][2], self.game_arr[2][0], self.game_arr[2][1],
                   self.game_arr[2][2]]
        if indices[0] == number and (
                (indices[1] == number and indices[2] == number) or (indices[3] == number and indices[6] == number) or (
                indices[4] == number and indices[8] == number)):
            self.print_arr()
            self.game_arr = self.arr
            return "Win"
        elif indices[8] == number and (
                (indices[2] == number and indices[5] == number) or (indices[6] == number and indices[7] == number)):
            self.print_arr()
            self.game_arr = self.arr
            return "Win"
        elif indices[4] == number and ((indices[6] == number and indices[2] == number) or (indices[1] == number and indices[7] == number) or (indices[5] == number and indices[3] == number)):
            self.print_arr()
            self.game_arr = self.arr
            return "Win"
        else:
            return "Play"

    def add_points(self, name):
        for player in self.player_arr:
            if player[0] == name:
                player[3] = int(player[3]) + 1
                self.over_ride_details()
                break
                
    def over_ride_details(self):
        player = open("PlayersDataFile.txt", "w")
        for details in self.player_arr:
            player.write(details[0] + "," + details[1] + "," + details[2] + "," + str(details[3])  + ",")
            player.write("\n")
        player.close()            

    def game_history(self):
        game_hist = open("GameHistory.txt", "w")
        for history in self.game_history_arr:
            game_hist.write(history[0] + "," + history[1] + "," +  history[2] + "," +  str(history[3] + ",\n"))
        game_hist.close()

    def print_arr(self):
        for row in self.game_arr:
            for column in row:
                print(column, "\t", end="")
            print("\n")

    def leader_board(self):
        players_dict = {}
        player_det = open("PlayersDataFile.txt")
        i = 0
        for details in player_det:
            players_dict[self.player_arr[i][0]] = int(self.player_arr[i][3])
            i += 1
        player_det.close()
        print("Name", "\t\t", "Score", "\t", "Rank", "\n")
        sorted_val_arr = list(players_dict.values())
        sorted_val_arr.sort(reverse = True)
        val_arr = list(players_dict.values())
        key_arr = list(players_dict.keys())
        rank = 1
        leader_board_file = open("LeaderBoardFile.txt", "w")
        for value in range(len(sorted_val_arr)):
            index = val_arr.index(sorted_val_arr[value])
            player = key_arr[index]
            score = val_arr[index]
            players_dict[player] = -1
            val_arr[index] = -1
            leader_board_file.write(player + " - " + str(score) + " - " + str(rank) +"\n")
            print(player, "\t", score, "\t", rank)
            rank += 1
        leader_board_file.close()

    '''def undo(self, row, column, self.game_arr):
        option = input("Do you want to Undo? (Yes/No) : ")
        if option == "Yes":
            self.game_arr[row][column] = -1
            self.print_arr(self.game_arr)
            return self.game_arr
        else:
            return None'''
        
    def timer(self):
        start = time.time()
        print(start)
        i = 0
        while time.time() - start <= 10:
            if int(time.time() - start) == 5 and i == 0:
                print("5 seconds more")
                i = 1
        print("Your opponent have won the match")

    def options(self):
        return " 1. Add new player \n"+ "2. Leader Board \n"+ "3. Exit \n"

    def gplay(self, userid, row, column, player_1, player_2):
        print("user_id", userid, "'s turn!")
        if userid == player_1:
            return self.game_running(0, row, column, player_1, player_2), userid
        elif userid == player_2:
            return self.game_running(1, row, column, player_1, player_2), userid

    def options_and_its_functions(self, option):
        if option == 1:
            return self.add_new_players()

        elif option == 2:
            return self.leader_board()

        elif option == 3:
            print("Thank you for playing")
            return 1













'''obj = TicTacToe()
obj_result = obj.gplay("sangee@123", 0, 0, "sangee@123", "sabi@123")
obj_result_1 = obj.gplay("sabi@123", 1, 0, "sangee@123", "sabi@123")
obj_result_2 = obj.gplay("sangee@123", 2, 2, "sangee@123", "sabi@123")
obj_result_3 = obj.gplay("sabi@123", 1, 2, "sangee@123", "sabi@123")
obj_result_4 = obj.gplay("sangee@123", 1, 1, "sangee@123", "sabi@123")
''''''obj_result_5 = obj.gplay("sabi@123", 2, 0, "sangee@123", "sabi@123")
obj_result_6 = obj.gplay("sangee@123", 0, 2, "sangee@123", "sabi@123")
obj_result_7 = obj.gplay("sabi@123", 0, 1, "sangee@123", "sabi@123")
obj_result_8 = obj.gplay("sangee@123", 2, 1, "sangee@123", "sabi@123")

'''