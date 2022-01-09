import json
import random
import re

aLen = 2315

with open('../dict.json') as json_file:
    data = json.load(json_file)

def randWord(data):
    return data["a"][random.randrange(0,aLen)]

# Creates Global variable for the total bank of words that we can guess with
possGuesses = sorted(data["b"]+data["a"])

# Function outputs the best first word based on our specified criteria
# This algorithm finds the best word by finding the word that leaves the fewest
# words remaining at the next level
def naiveFW(data):
    possAnswers = sorted(list(data))

    total = {}
    tops = {}
    minTotal = 150000
    totalWord = ''

    # Filters out all possible answers that don't have repeat letters and only
    # contain the common letters: [aeilnorsty]. This is done to improve execution time
    p = re.compile(r"(?!.*(\w).*\1{1})[aeilnorsty]{5}")
    # pG= list(filter(p.match, possGuesses))
    pG = possAnswers

    # Searches through each of our filtered guesses for every possible answer
    # This will help us determine which guess gives us the fewest remaining at the
    # Next level
    for g in pG:
        total[g] = 0
        for word in possAnswers:
            str = ""
            chars = "[abcdefghijklmnopqrstuvwxyz]"
            rep = ""
            for i in range(0,5):
                if g[i] == word[i]:
                    str = str + g[i]
                elif g[i] in word:
                    str = str+g[i].upper()
                    rep = rep + g[i].upper()
                else:
                    chars = chars.replace(g[i], "")
                    str = str+"*"
            strstr = str
            for let in rep:
                str = str.replace(let, chars.replace(let.lower(), ""))
            str = str.replace("*", chars)
            for z in set(rep):
                str = '(?=.*' + z.lower() + ')' + str

            r = re.compile(str)
            results = len(list(filter(r.match, possAnswers)))
            total[g]+=results
            if total[g] > minTotal:
                total[g] = 150000
                break
        if total[g] < minTotal:
            minTotal = total[g]
            totalWord = g
        if total[g] < 150000:
            print(g, total[g])
    return totalWord

# Function outputs the best non first word based on our specified criteria
# This algorithm finds the best word by finding the word that leaves the fewest
# words remaining at the next level
def naiveSW(data):
    l = len(data)
    if l == 1 or l == 2:
        return data[0]
    possAnswers = sorted(set(data))
    total = {}
    tops = {}
    minTotal = 150000
    totalWord = ''
    # We no longer filter out any guesses, since the subsequent next best guess
    # tends to be pretty counterintuitive

    # We start with the remaining words since they are more likely to be the answer
    pG = possAnswers+possGuesses
    for g in pG:
        total[g] = 0
        for word in possAnswers:
            str = ""
            chars = "[abcdefghijklmnopqrstuvwxyz]"
            rep = ""
            for i in range(0,5):
                if g[i] == word[i]:
                    str = str + g[i]
                elif g[i] in word:
                    str = str+g[i].upper()
                    rep = rep + g[i].upper()
                else:
                    chars = chars.replace(g[i], "")
                    str = str+"*"
            strstr = str
            for let in rep:
                str = str.replace(let, chars.replace(let.lower(), ""))
            str = str.replace("*", chars)
            for z in set(rep):
                str = '(?=.*' + z.lower() + ')' + str

            r = re.compile(str)
            results = len(list(filter(r.match, possAnswers)))
            total[g]+=results
            if g == word:
                total[g] -= 1

            # Here we prune branches that cannot win
            if total[g] > minTotal:
                break
        if total[g] <= minTotal:
            minTotal = total[g]
            totalWord = g
            # If we find an answer that results in same number of words as we have
            # Possible answers we know we can quit. Since we started with
            # remaining answers we don't have to filter for that
            if total[g] == l:
                break

    return totalWord

# Recursive function tha finds the buckets of words for the next generation.
# Will call NaiveSW to grab the best word for the next generation bucket
def Naive(w, possAnswers):

    # Recursive base case
    l = len(possAnswers)
    if l == 1 or l == 0:
        return l

    # Fills the next generation of buckets given a word and possible answers
    buckets = []
    usedInBuckets = set()
    for word in possAnswers:
        if word in usedInBuckets:
            continue
        str = ""
        chars = "[abcdefghijklmnopqrstuvwxyz]"
        rep = ""
        for i in range(0,5):
            if w[i] == word[i]:
                str = str + w[i]
            elif w[i] in word:
                str = str+w[i].upper()
                rep = rep + w[i].upper()
            else:
                chars = chars.replace(w[i], "")
                str = str+"*"
        strstr = str
        for let in rep:
            str = str.replace(let, chars.replace(let.lower(), ""))
        str = str.replace("*", chars)
        for z in set(rep):
            str = '(?=.*' + z.lower() + ')' + str

        r = re.compile(str)
        results = [strstr, w] + (list(filter(r.match, possAnswers)))
        buckets.append(results)
        for wo in results[2:]:
            usedInBuckets.add(wo)
    fin = dict()
    for bucket in buckets:
        # print(sorted(bucket), end="    ")
        gu = naiveSW(bucket[2:])
        res = ""
        for letter in bucket[0]:
            if letter.isupper():
                res += "Y"
            elif letter.islower():
                res += "G"
            else:
                res += "B"


        print("You guessed: " + bucket[1] + " result: " + res)
        fin[res] = {}
        fin[res][gu] = Naive(gu, bucket[2:])

    return fin

# Main code. Initializes the set of words and calls our recursive function which
# will output the json decision tree for us to use
t = data["a"]
# t = ['joker', 'mower', 'rebel', 'foyer', 'wooer', 'fewer', 'rower', 'lower', 'boxer', 'roger', 'revel', 'rover', 'hyper', 'poker', 'ember', 'lover', 'buyer', 'upper', 'ruler', 'refer', 'hover', 'flyer', 'offer', 'repel', 'purer', 'bluer', 'leper', 'homer', 'queer', 'lever', 'fever', 'power', 'mover']
# starter = "dines"
# print(starter)
# print(json.dumps(Naive(starter, t)))
print(naiveFW(t))
