import sys
sys.path.append(r'C:\Users\sange\PycharmProjects\pythonProject4\TicTacToe.py')
import socket
import TicTacToe
s = socket.socket()
print("Socket Created")

s.bind(('192.168.1.4', 9999))
s.listen(3)
print("Waiting for connections")


def print_arr(game_arr):
    n = len(game_arr)
    for i in range(n):
        for j in range(n):
            c.send(bytes((str(game_arr[i][j]) + "\t"), "utf-8"))
        c.send(bytes("\n", "utf-8"))

while True:
    c, addr = s.accept()
    print("c:", c)
    ip_addr = list(addr)[0]
    print("Connected with ", ip_addr)
    arr = []
    dic = {}
    file = open("DetailsFile.txt")
    i = 0
    for details in file:
        arr.append(details.split("-"))
        dic[arr[i][0]] = arr[i][1]
        i += 1
    file.close()

    if ip_addr in dic.keys():
        c.send(bytes("Yes", "utf-8"))
        c.send(bytes("Hi " + dic[ip_addr], "utf-8"))
    else:
        name = c.recv(1024).decode()
        print("Connected with ", ip_addr, name)
        arr.append([ip_addr, name])

    obj = TicTacToe.TicTacToe()
    c.send(bytes("Welcome to Tic Tac Toe\n", "utf-8"))

    n = c.recv(1024).decode()
    game_arr = obj.play(int(n))
    print_arr(game_arr)
    c.send(bytes("Player 1", "utf-8"))




    file = open("DetailsFile.txt", "w")
    for details in arr:
        print("File has been written")
        file.write(str(details[0]) + "-" + details[1] + "-\n")
    file.close()

    c.close()
