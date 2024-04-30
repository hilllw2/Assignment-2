#!/usr/bin/env python
# coding: utf-8

# without gui 

# In[ ]:


def game_board(board):
    for i, row in enumerate(board):
        print('|'.join(row))
        if i < len(board) - 1:
            print('-' * 5)
#3x3 board for tic tac toe 
board = [[' 'for _ in range(3)] for _ in range(3)]
game_board(board)

#game environment
def check_win(board, player):
    #check rows 
    for row in board:
        if all(cell == player for cell in row):
            return True
        
        #check columns
    for column in range(3):
        if all(board[row][column] == player for row in range(3)):
            return True
        
        #check diagnols
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False


#if the game gets drawn
def draw(board):
    return all(cell != ' ' for row in board for cell in row)

#player moves against the AI Agent
def player_move(board):
    while True:
        try:
            row = int(input("enter row (0,1,2) "))
            column = int(input("enter column (0,1,2) "))
            if 0 <= row <= 2 and 0 <= column <= 2 and board[row][column] == ' ':
                return row, column
            else:
                print("Invalid move, try again.")
        except ValueError:
            print("Invalid input, enter numbers from 0-2.")

#AI moves against the player
def ai_move(board, max_depth):
    best_eval = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minmax(board, 0, False, max_depth)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

#building Minmax AI player
def minmax(board, depth, is_maximizing, max_depth):
    if check_win(board, 'X'):
        return -1
    elif check_win(board, 'O'):
        return 1
    elif draw(board) or depth == max_depth:
        return 0
    if is_maximizing:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minmax(board, depth + 1, False, max_depth)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minmax(board, depth + 1, True, max_depth)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

#playing against the A1 player
def main():
    
    #reset board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_turn = True
    while True:
        game_board(board)
        if player_turn:
            print("\nyour turn.")
            row, column = player_move(board)
            board[row][column] = 'X'
        else:
            input("\npress enter for AI player to go")
            move = ai_move(board, 0)
            if move:
                row, column = move
                board[row][column] = 'O'
        if check_win(board, 'X'):
            game_board(board)
            print("you win")
            break
        elif check_win(board, 'O'):
            game_board(board)
            print("AI wins")
            break
        elif draw(board):
            game_board(board)
            print("It's a draw")
            break
        player_turn = not player_turn

if __name__ == "__main__":
    main()


# with gui

# In[3]:


import tkinter as tk
from tkinter import messagebox

def reset_board():
    global board, buttons, label
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=' ', state='normal', bg='SystemButtonFace')
            board[i][j] = ' '
    label.config(text="Player X's turn")
    
#if a player has won the game
def check_win(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  #row check
            highlight_winner(i, 0, i, 1, i, 2)
            return True
        if all(board[j][i] == player for j in range(3)):  #column check
            highlight_winner(0, i, 1, i, 2, i)
            return True

    if all(board[i][i] == player for i in range(3)):  #diagonal check
        highlight_winner(0, 0, 1, 1, 2, 2)
        return True

    if all(board[i][2-i] == player for i in range(3)):  #antidiagonal check
        highlight_winner(0, 2, 1, 1, 2, 0)
        return True

    return False

#highlight the winning combination
def highlight_winner(r1, c1, r2, c2, r3, c3):
    buttons[r1][c1].config(bg="green")
    buttons[r2][c2].config(bg="green")
    buttons[r3][c3].config(bg="green")

#for draw
def draw():
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

#player moves
def player_move(row, column):
    board[row][column] = 'X'
    buttons[row][column].config(text='X', state='disabled')
    if check_win('X'):
        game_over("X wins")
    elif draw():
        game_over("It's a draw!")
    else:
        ai_move()

# AI moves
def ai_move():
    # simple Ai first empty cell
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                buttons[i][j].config(text='O', state='disabled')
                if check_win('O'):
                    game_over("AI wins")
                elif draw():
                    game_over("It's a draw!")
                return

#disable all buttons after the game ends
def disable_all_buttons():
    for row in buttons:
        for button in row:
            button.config(state="disabled")

#end the game and show message
def game_over(message):
    label.config(text=message)
    disable_all_buttons()

#create the main window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")

    top_frame = tk.Frame(root)
    top_frame.pack(side="top")

    label = tk.Label(top_frame, text="Player X's turn", font=('consolas', 20), height=2)
    label.pack(side="left")

    restart_button = tk.Button(top_frame, text="restart", font=('consolas', 20), command=reset_board)
    restart_button.pack(side="right")

    grid_frame = tk.Frame(root)
    grid_frame.pack()

    buttons = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            cmd = lambda i=i, j=j: player_move(i, j)
            buttons[i][j] = tk.Button(grid_frame, text=' ', font=('consolas', 20), width=5, height=2, command=cmd)
            buttons[i][j].grid(row=i, column=j)

    board = [[' ' for _ in range(3)] for _ in range(3)]
    reset_board() 
    root.mainloop()


# In[ ]:




