# Import Things used
import random
import numpy as np
import tkinter as tk

# The minesweeper Game


class minesweep:

    # Initalize
    def __init__(self, master, size):

        # Getting stats
        self.list1 = []

        with open('stats.txt', 'r') as f:
            data = f.readlines()

        for x in range(len(data)):
            if (data[x][:-1] if len(data[x]) > 1 else data[x]).isdigit():
                self.list1.append(
                    int(data[x][:-1]) if len(data[x]) > 1 else int(data[x]))

        # Setting all the variables to what they need to be and generating a array of buttons
        self.size = size
        self.score = 0
        self.values = [0, 'F']
        self.probability = [.85, .15]
        self.grid = np.random.choice(
            self.values, self.size*self.size, p=self.probability).reshape(self.size, self.size)
        self.grid = self.format(self.grid)
        self.blank = np.random.choice(
            [''], self.size*self.size).reshape(self.size, self.size)
        self.winState = '   '
        self.master = master
        frame = tk.Toplevel(self.master)
        self.buttons = [[None for _ in range(self.size)]
                        for _ in range(self.size)]
        self.turn = 0

        # Giving the buttons different functions on right and left click for flagging or mining
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j] = tk.Button(frame, text=" ",
                                               height='1', width='3')
                self.buttons[i][j].bind(
                    '<Button-1>', lambda e, i=i, j=j: self.search(i, j, True))
                self.buttons[i][j].bind(
                    '<Button-3>', lambda e, i=i, j=j: self.flag(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    # Formats the array
    def format(self, grid):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                count = 0
                if self.grid[y][x] != 'F':

                    if (y-1 >= 0) and (self.grid[y - 1][x] == 'F'):
                        count += 1
                    if (y-1 >= 0) and (x-1 >= 0) and (self.grid[y - 1][x - 1] == 'F'):
                        count += 1
                    if (x-1 >= 0) and (self.grid[y][x - 1] == 'F'):
                        count += 1
                    if (y+1 < self.size) and (self.grid[y + 1][x] == 'F'):
                        count += 1
                    if (y+1 < self.size) and (x+1 < self.size) and (self.grid[y + 1][x + 1] == 'F'):
                        count += 1
                    if (x+1 < self.size) and (self.grid[y][x + 1] == 'F'):
                        count += 1
                    if (y+1 < self.size) and (x-1 >= 0) and (self.grid[y + 1][x - 1] == 'F'):
                        count += 1
                    if (y-1 >= 0) and (x+1 < self.size) and (self.grid[y - 1][x + 1] == 'F'):
                        count += 1
                    self.grid[y][x] = count
        return self.grid

    # Mines things
    def search(self, y, x, i=False):
        # Win state
        if self.winState == '   ':
            if np.array_equal(self.blank, self.grid):
                self.score += 100

                self.winState = 'won'
                loss(self.master, 'Minesweeper', self.winState, self.turn, self.score)
                if self.list1[5] == 0:
                    self.list1[5] = self.score
                elif self.list1[5] > self.score:
                    self.list1[5] = self.score
                if self.list1[4] == 0:
                    self.list1[4] = self.score
                elif self.list1[4] == 0 < self.score:
                    self.list1[4] = self.score

                with open('stats.txt', 'w') as f:
                    f.write(f"Hangman\nHigh Score\n{str(self.list1[0])}\nLow Score\n{str(self.list1[1])}\nTimes Played\n{str(self.list1[2])}\nWins\n{str(self.list1[3])}\nMinesweeper\nHigh Score\n{str(self.list1[4])}\nLow Score\n{str(self.list1[5])}\nTimes Played\n{str(self.list1[6] + 1)}\nWins\n{str(self.list1[7] + 1)}")

            # Ensures the first score is always blank
            if (self.turn == 0) and (self.grid[y][x] != 0):
                self.grid[y][x] = 0
                self.grid[y+1][x] = 0
                self.grid[y][x+1] = 0
                self.grid[y-1][x] = 0
                self.grid[y][x-1] = 0
                self.grid[y+1][x+1] = 0
                self.grid[y-1][x-1] = 0
                self.grid[y+1][x-1] = 0
                self.grid[y-1][x+1] = 0
                self.grid = self.format(self.grid)

            if i and self.buttons[y][x]["text"] == " ":
                self.turn += 1

            # Lose state
            if self.grid[y][x] == 'F' and self.buttons[y][x]["text"] != "F":
                self.buttons[y][x]["text"] = "M"
                self.buttons[y][x]["fg"] = "Blue"
                self.winState = 'lost'
                loss(self.master, 'Minesweeper', self.winState, self.turn, self.score)
                if self.list1[5] == 0:
                    self.list1[5] = self.score
                elif self.list1[5] > self.score:
                    self.list1[5] = self.score
                if self.list1[4] == 0:
                    self.list1[4] = self.score
                elif self.list1[4] == 0 < self.score:
                    self.list1[4] = self.score
                with open('stats.txt', 'w') as f:
                    f.write(f"Hangman\nHigh Score\n{str(self.list1[0])}\nLow Score\n{str(self.list1[1])}\nTimes Played\n{str(self.list1[2])}\nWins\n{str(self.list1[3])}\nMinesweeper\nHigh Score\n{str(self.list1[4])}\nLow Score\n{str(self.list1[5])}\nTimes Played\n{str(self.list1[6] + 1)}\nWins\n{str(self.list1[7])}")

            # mining function
            elif self.buttons[y][x]["text"] == " ":
                # Score + 2 for every uncovered square
                self.score += 2
                self.blank[y][x] = self.grid[y][x]
                self.buttons[y][x]["text"] = self.grid[y][x]
                if self.grid[y][x] == '0':
                    if (y-1 >= 0) and (self.blank[y-1][x] == ''):
                        self.search(y-1, x)
                    if (y-1 >= 0) and (x-1 >= 0) and (self.blank[y-1][x-1] == ''):
                        self.search(y-1, x-1)
                    if (x-1 >= 0) and (self.blank[y][x-1] == ''):
                        self.search(y, x-1)
                    if (y+1 < self.size) and (self.blank[y+1][x] == ''):
                        self.search(y+1, x)
                    if (y+1 < self.size) and (x+1 < self.size) and (self.blank[y+1][x+1] == ''):
                        self.search(y+1, x+1)
                    if (x+1 < self.size) and (self.blank[y][x+1] == ''):
                        self.search(y, x+1)
                    if (y+1 < self.size) and (x-1 >= 0) and (self.blank[y+1][x-1] == ''):
                        self.search(y+1, x-1)
                    if (y-1 >= 0) and (x+1 < self.size) and (self.blank[y-1][x+1] == ''):
                        self.search(y-1, x+1)

    # Flag function
    def flag(self, y, x):
        if self.buttons[y][x]["text"] == " ":
            self.blank[y][x] = 'F'
            self.score += 1
            self.buttons[y][x]["text"] = "F"
            self.buttons[y][x]["fg"] = 'red'
        elif self.buttons[y][x]["text"] == "F" and self.buttons[y][x]["fg"] == 'red':
            self.buttons[y][x]["text"] = " "
            self.blank[y][x] = ''
            self.score -= 1
            self.buttons[y][x]["fg"] = 'black'

# What pops up when you finish a game


def loss(master, game, winState, turn=0, score=0, word=''):

    # New window that prints out if you lost or won
    newWindow = tk.Toplevel(master)
    label1 = tk.Label(newWindow, text="You " + winState +
                      " in " + str(turn) + " turns!\tScore: " + str(score))
    if game != 'minesweeper':
        tk.Label(newWindow, text=str(word) + ' was the word')
    label1.pack()

# The hub


class hub:
    # Initalizing
    def __init__(self, master, list1):
        self.master = master
        options = [10, 15, 20, 25]
        self.clicked = tk.StringVar()
        self.clicked.set(15)
        tk.OptionMenu(self.master, self.clicked, *options).grid(row=0, column=1)
        # Buttons for each thing
        tk.Button(text="Minesweeper", command=self.run).grid(row=0, column=0)
        tk.Button(text="Hangman", command=self.run1).grid(row=1)
        tk.Button(text="Stats", command=self.run2).grid(row=2)
        tk.Button(text="About", command=self.run3).grid(row=3)

    # Launches various windows when pressed
    def run(self):
        app = minesweep(self.master, int(self.clicked.get()))
        self.master.mainloop()

    def run1(self):
        app = hangman(self.master)
        self.master.mainloop()

    def run2(self):
        app = stats(self.master)
        self.master.mainloop()

    def run3(self):
        app = about(self.master)
        self.master.mainloop()

# Stats


class stats:
    # Imports then just makes labels out of everything
    def __init__(self, master):
        self.master = master

        with open('stats.txt', 'r') as f:
            data = f.readlines()

        frame = tk.Toplevel(self.master)
        tk.Label(frame, text=data[0][:-1]).pack()
        tk.Label(frame, text=data[1][:-1]).pack()
        tk.Label(frame, text=data[2][:-1]).pack()
        tk.Label(frame, text=data[3][:-1]).pack()
        tk.Label(frame, text=data[4][:-1]).pack()
        tk.Label(frame, text='Win%').pack()
        try:
            tk.Label(frame, text=str(
                round(int(data[8][:-1])/int(data[6][:-1]) * 100)) + '%').pack()
        except:
            tk.Label(frame, text='0%').pack()
        tk.Label(frame, text='Loss%').pack()
        try:
            tk.Label(frame, text=str(
                100 - round(int(data[8][:-1])/int(data[6][:-1]) * 100)) + '%').pack()
        except:
            tk.Label(frame, text='0%').pack()
        tk.Label(frame, text=data[9][:-1]).pack()
        tk.Label(frame, text=data[10][:-1]).pack()
        tk.Label(frame, text=data[11][:-1]).pack()
        tk.Label(frame, text=data[12][:-1]).pack()
        tk.Label(frame, text=data[13][:-1]).pack()
        tk.Label(frame, text='Win%').pack()
        try:
            tk.Label(frame, text=str(
                round(int(data[17])/int(data[15][:-1]) * 100)) + '%').pack()
        except:
            tk.Label(frame, text='0%').pack()
        tk.Label(frame, text='Loss%').pack()
        try:
            tk.Label(frame, text=str(
                100 - round(int(data[17])/int(data[15][:-1]) * 100)) + '%').pack()
        except:
            tk.Label(frame, text='0%').pack()

# Hangman


class hangman:
    # initalizes everything needed and makes the format for the game
    def __init__(self, master):
        self.list1 = []

        with open('stats.txt', 'r') as f:
            data = f.readlines()

        for x in range(len(data)):
            if (data[x][:-1] if len(data[x]) > 1 else data[x]).isdigit():
                self.list1.append(
                    int(data[x][:-1]) if len(data[x]) > 1 else int(data[x]))

        self.master = master
        frame = tk.Toplevel(self.master)
        self.guesses = []
        self.blanks = []
        self.Lword = []
        self.word = ''
        self.Uguess = ''
        self.guess = 6
        self.points = 0
        self.turns = 0

        with open('words.txt', 'r') as f:
            self.words = f.readlines()
        self.word = (random.choice(self.words)[:-1])
        self.Lword = list(self.word)

        for x in range(len(self.Lword)):
            self.blanks.append('*')

        self.lives = tk.Label(frame, text='Lives: ' + str(self.guess))
        self.bl = tk.Label(frame, text=' '.join(self.blanks), fg="red")
        self.e1 = tk.Entry(frame, text="Enter a letter")
        tk.Button(frame, text='Guess letter',
                  command=self.guessL).grid(row=2, column=1)
        self.ge = tk.Label(frame, text='Guesses: ' + ' '.join(self.guesses))
        self.e1.grid(row=2, column=0)
        self.bl.grid(row=1)
        self.lives.grid(row=0)
        self.ge.grid(row=3)

    # This happens when a guess is submitted
    def guessL(self):
        self.turns += 1
        Uguess = self.e1.get().lower()
        if self.guess != 0:
            if ((not Uguess.isalpha())):
                NotL = tk.Toplevel(self.master)
                tk.Label(NotL, text='ERROR: not a letter', fg="red").pack()
            elif Uguess in self.Lword:
                self.points += 2
                indices = [i for i, x in enumerate(self.word) if x == Uguess]
                for index in indices:
                    self.blanks[index] = Uguess
                self.bl['text'] = ' '.join(self.blanks)
                self.guesses.append(Uguess)
                self.ge['text'] = 'Guesses: ' + str(self.guesses)
            else:
                self.points -= 2
                self.guess -= 1
                self.lives['text'] = 'Lives: ' + str(self.guess)
                self.guesses.append(Uguess)
                self.ge['text'] = 'Guesses: ' + str(self.guesses)

            # Win condition
            if self.Lword == self.blanks:
                loss(self.master, 'Hangman', 'won', self.turns, self.points, word=self.word)
                self.guess = 0
                if self.list1[1] == 0:
                    self.list1[1] = self.points
                elif self.list1[1] > self.points:
                    self.list1[1] = self.points
                if self.list1[0] == 0:
                    self.list1[0] = self.points
                elif self.list1[0] == 0 < self.points:
                    self.list1[0] = self.points

                with open('stats.txt', 'w') as f:
                    f.write(f"Hangman\nHigh Score\n{str(self.list1[0])}\nLow Score\n{str(self.list1[1])}\nTimes Played\n{str(self.list1[2] + 1)}\nWins\n{str(self.list1[3] + 1)}\nMinesweeper\nHigh Score\n{str(self.list1[4])}\nLow Score\n{str(self.list1[5])}\nTimes Played\n{str(self.list1[6])}\nWins\n{str(self.list1[7])}")
        # Loss condidion
        if (self.Lword != self.blanks) and (self.guess == 0):
            loss(self.master, 'Hangman', 'lost', self.turns, self.points, word=self.word)
            if self.list1[1] == 0:
                self.list1[1] = self.points
            elif self.list1[1] > self.points:
                self.list1[1] = self.points
            if self.list1[0] == 0:
                self.list1[0] = self.points
            elif self.list1[0] == 0 < self.points:
                self.list1[0] = self.points
            with open('stats.txt', 'w') as f:
                f.write(f"Hangman\nHigh Score\n{str(self.list1[0])}\nLow Score\n{str(self.list1[1])}\nTimes Played\n{str(self.list1[2] + 1)}\nWins\n{str(self.list1[3])}\nMinesweeper\nHigh Score\n{str(self.list1[4])}\nLow Score\n{str(self.list1[5])}\nTimes Played\n{str(self.list1[6])}\nWins\n{str(self.list1[7])}")
        self.e1.delete(0, 'end')

# About


class about:
    # Quick about section
    def __init__(self, master):
        self.master = master
        frame = tk.Toplevel(self.master)
        tk.Label(frame, text="Made By Max Meadowcroft For CSE 107").pack()

# main function


def main():
    # Just a small main function that mostly runs the hub
    data2 = []

    root = tk.Tk()
    root.title("GAME HUB")

    app1 = hub(root, data2)
    root.mainloop()


# Runs function when main is ran
if __name__ == '__main__':
    main()
