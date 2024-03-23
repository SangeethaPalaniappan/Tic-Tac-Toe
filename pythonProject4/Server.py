import sys
sys.path.append(r'C:\Users\sange\PycharmProjects\pythonProject4\TicTacToe.py')
import socket
import TicTacToe
s = socket.socket()
print("Socket Created")

s.bind(('192.168.220.54', 9999))
s.listen(3)
print("Waiting for connections")


def print_arr(game_arr):
    board = ""
    n = len(game_arr)
    for i in range(n):
        for j in range(n):
            board = board + "\t" + str(game_arr[i][j])
        board = board + "\n"
    return board

def board_details(game_arr):
    board = print_arr(game_arr)

    print(board)
    n = c_1.send(bytes("Board", "utf-8"))
    print(c_1.recv(1024).decode())
    m = c_1.send(bytes(board, "utf-8"))
    print(c_1.recv(1024).decode())
    c_2.send(bytes("Board", "utf-8"))
    print(c_2.recv(1024).decode())
    c_2.send(bytes(board, "utf-8"))

    #board details received
    print(c_2.recv(1024).decode())


dic = {}
print("Waiting for the Player 1")
c_1, addr_1 = s.accept()
c_1.send(bytes("Welcome to Tic Tac Toe\n", "utf-8"))
name_1 = c_1.recv(1024).decode()
print(name_1)
n = 3

ip_addr_1 = list(addr_1)[0]
port_no_1 = list(addr_1)[1]
dic[port_no_1] = name_1
print("Waiting for the Player 2")

c_2, addr_2 = s.accept()
c_2.send(bytes("Welcome to Tic Tac Toe\n", "utf-8"))
name_2 = c_2.recv(1024).decode()
print(name_2)
ip_addr_2 = list(addr_2)[0]
port_no_2 = list(addr_2)[1]
dic[port_no_2] = name_2
obj = TicTacToe.TicTacToe()

print(addr_1)
print(addr_2)
print("c1: ", c_1)
print("c2: ", c_2)


print("Connected with ", addr_1)
print("Connected with ", addr_2)


print("Connected with ", ip_addr_1, name_1)

print("Connected with ", ip_addr_2, name_2)

print(dic)

game_arr = obj.play(int(n))
c_1.send(bytes("Player 1\n", "utf-8"))
c_2.send(bytes("Player 2\n", "utf-8"))
board_details(game_arr)

for i in range(5):
    c_1.send(bytes("Play", 'utf-8'))
    row_1, column_1 = c_1.recv(1024).decode().split(",")
    game_arr = obj.player(name_1, name_2, game_arr, int(row_1), int(column_1), 1)
    board_details(game_arr)
    check = obj.check(1, game_arr)
    if check == "Win":
        c_1.send(bytes("Win", "utf-8"))
        print(c_1.recv(1024).decode())
        c_1.send(bytes("You win the match", "utf-8"))
        c_2.send(bytes("Lose", "utf-8"))
        print(c_2.recv(1024).decode())
        c_2.send(bytes("You lose the match", "utf-8"))
        break
    if i == 4:
        c_1.send(bytes("Match Draw", "utf-8"))
        print(c_1.recv(1024).decode())
        c_1.send(bytes("Match Draw", "utf-8"))
        c_2.send(bytes("Match Draw", "utf-8"))
        print(c_1.recv(1024).decode())
        c_2.send(bytes("Match Draw", "utf-8"))
        break
    if i != 4:
        c_2.send(bytes("Play", "utf-8"))
        row_2, column_2 = c_2.recv(1024).decode().split(",")
        game_arr = obj.player(name_1, name_2, game_arr, int(row_2), int(column_2), 0)
        board_details(game_arr)
        check = obj.check(0, game_arr)
        if check == "Win":
            c_2.send(bytes("Win", "utf-8"))
            print(c_2.recv(1024).decode())
            c_2.send(bytes("You win the match", "utf-8"))
            c_1.send(bytes("Lose", "utf-8"))
            print(c_1.recv(1024).decode())
            c_1.send(bytes("You lose the match", "utf-8"))
            break


c_1.close()
c_2.close()
