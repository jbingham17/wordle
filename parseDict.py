#!/usr/bin/python3
import json
import random
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GRAY = '\033[91m'
    ENDC = '\033[0m'

aLen = 2315
bLen = 10657
tLen = aLen+bLen

with open('dict.json') as json_file:
    data = json.load(json_file)



possAnswers = set(data["a"])

def randWord(data):
    return data["a"][random.randrange(0,aLen)]

def game(data, word):
    # print(bcolors.YELLOW + "Warning" + bcolors.ENDC)
    # possible = set(data["a"])
    total = set(data["a"]).union(set(data["b"]))
    print(len(total))

    for i in range(0,6):

        guess = input("Enter Guess\n").lower()
        while (guess not in total) or (len(guess) != 5):
            guess = input("Not valid word. Enter another\n")

        res = ""
        for i, letter in enumerate(guess):
            if letter == word[i]:
                res += "G"
                print(bcolors.GREEN + letter + bcolors.ENDC, end='')
            elif letter in word:
                res += "Y"
                print(bcolors.YELLOW + letter + bcolors.ENDC, end='')
            else:
                res += "B"
                print(bcolors.GRAY + letter + bcolors.ENDC, end='')

        print()

        if guess==word:
            print("Sucess!!")
            break

def playNaively(data, word):
    possible = set(data["a"])
    total = set(data["a"]).union(set(data["b"]))
    print(len(total))

    with open('bucketTrace.json') as jsf:
        naiveJson = json.load(jsf)

    for j in range(0,6):

        guess = input("Enter Guess\n").lower()
        while (guess not in total) or (len(guess) != 5):
            guess = input("Not valid word. Enter another\n")

        correct = []
        close = []
        wrong = []

        res = ""
        for i, letter in enumerate(guess):
            if letter == word[i]:
                correct.append((i, letter))
                res += "G"
                print(bcolors.GREEN + letter + bcolors.ENDC, end='')
            elif letter in word:
                close.append((i, letter))
                res += "Y"
                print(bcolors.YELLOW + letter + bcolors.ENDC, end='')
            else:
                wrong.append(letter)
                res += "B"
                print(bcolors.GRAY + letter + bcolors.ENDC, end='')


        print()

        if guess==word:
            print("Sucess!!")
            break


        deletions = set()
        for w in possible:
            skip = False
            for a in wrong:
                if a in w:
                    deletions.add(w)
                    skip = True
                    break
            if skip:
                continue
            for b in correct:
                if b[1] != w[b[0]]:
                    deletions.add(w)
                    skip = True
                    break
            if skip:
                continue
            for c in close:
                if c[1] not in w:
                    deletions.add(w)
                    break
                elif c[1] == w[c[0]]:
                    deletions.add(w)
                    break

        possible = possible.difference(deletions)

        print(possible)
        print("There are " + str(len(possible)) + " possibilities remaining")
        # print(naiveJson)

        # print(naiveJson)
        if j==0:
            string = str(naiveJson[res]).replace("'", '"')
        else:
            string = string[guess][res]


        print("Suggestion: " + str(string)[2:7])
        string = json.loads(str(string).replace("'", '"'))

def naiveCount(data):
    possible = data["a"]
    counts = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}}

    for word in possible:
        for i, letter in enumerate(word):
            if letter in counts[i]:
                counts[i][letter]+=1
            else:
                counts[i][letter]=1

    return counts

def barChart(data):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    lists = {0:[], 1:[], 2:[], 3:[], 4:[]}
    for i in range(0,5):
        for letter in letters:
            if letter in data[i]:
                lists[i].append(data[i][letter])
            else:
                lists[i].append(0)
        print(lists[i], len(lists[i]))

    width = 0.3
    plt.xticks(range(len(letters)), letters)
    plt.xlabel('Letter')
    plt.ylabel('Count')
    A = np.array(lists[0])
    B = np.array(lists[1])
    C = np.array(lists[2])
    D = np.array(lists[3])
    E = np.array(lists[4])
    plt.bar(letters, A, label='1st')
    plt.bar(letters, B, bottom=A, label='2nd')
    plt.bar(letters, C, bottom=A+B, label='3rd')
    plt.bar(letters, D, bottom=A+B+C, label='4th')
    plt.bar(letters, E, bottom=A+B+C+D, label='5th')
    plt.show()

def naiveFWHelper(guess):
    total=0
    deletions = set()
    for word in possAnswers:
        correct = []
        close = []
        wrong = []
        for i, letter in enumerate(guess):
            if letter not in word:
                wrong.append(letter)
            elif letter == word[i]:
                correct.append((i, letter))
            else:
                close.append((i, letter))


        deletions.clear()
        for w in possAnswers:
            skip = False
            for a in wrong:
                if a in w:
                    deletions.add(w)
                    skip = True
                    break
            if skip:
                continue
            for b in correct:
                if b[1] != w[b[0]]:
                    deletions.add(w)
                    skip = True
                    break
            if skip:
                continue
            for c in close:
                if c[1] not in w:
                    deletions.add(w)
                    break
                elif c[1] == w[c[0]]:
                    deletions.add(w)
                    break
        rem = aLen - len(deletions)
        total += rem
    return total


def naiveFW(data):
    possGuesses = sorted(data["b"]+data["a"])


    guesses = possGuesses[0:20]
    total = {f:naiveFWHelper(f) for f in guesses}

    return total




# word = randWord(data)
# counts = naiveCount(data)
# barChart(counts)
playNaively(data, "joker")
