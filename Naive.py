# Note, I've commented N2.py since these two files are nearly identical

import json
import random
import re

aLen = 2315
bLen = 10657
tLen = aLen+bLen

with open('dict.json') as json_file:
    data = json.load(json_file)

def randWord(data):
    return data["a"][random.randrange(0,aLen)]

possGuesses = sorted(data["a"])


def naiveFW(data):
    possAnswers = sorted(list(data))

    total = {}
    tops = {}
    minTotal = 150000
    totalWord = ''
    p = re.compile(r"(?!.*(\w).*\1{1})[aeilnorsty]{5}")
    pG= list(filter(p.match, possGuesses))
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
                break
        if total[g] < minTotal:
            minTotal = total[g]
            totalWord = g
    return totalWord

def naiveSW(data):
    l = len(data)
    if l == 1 or l == 2:
        return data[0]
    possAnswers = sorted(set(data))
    total = {}
    tops = {}
    minTotal = 150000
    totalWord = ''
    pG = possAnswers
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
            if total[g] > minTotal:
                break
        if total[g] <= minTotal:
            minTotal = total[g]
            totalWord = g
            if total[g] == l:
                break

    return totalWord

def Naive(w, possAnswers, depth):
    l = len(possAnswers)
    if l == 1 or l == 0:
        return l
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
    total = 1
    d = "".join(["--" for v in range(0, depth)])
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
        print(d + gu)
        fin[res] = {}
        fin[res][gu] = Naive(gu, bucket[2:], depth+1)

    return fin



# word = randWord(data)

# t = ['alarm', 'award', 'braid', 'brain']
# t = ['biddy', 'billy', 'blimp', 'blind', 'blink', 'bliss', 'bluff', 'blush', 'buddy', 'buggy', 'build', 'bulky', 'bully', 'bunch', 'bunny', 'bushy', 'chick', 'child', 'chili', 'chill', 'chuck', 'chump', 'chunk', 'cinch', 'civic', 'civil', 'click', 'cliff', 'climb', 'cling', 'clink', 'cluck', 'clump', 'clung', 'cubic', 'cumin', 'cynic', 'dilly', 'dimly', 'dingy', 'dizzy', 'duchy', 'dully', 'dummy', 'dumpy', 'dusky', 'dying', 'ficus', 'filly', 'filmy', 'finch', 'fishy', 'fizzy', 'flick', 'fling', 'fluff', 'fluid', 'flung', 'flunk', 'flush', 'fully', 'fungi', 'funky', 'funny', 'fussy', 'fuzzy', 'giddy', 'gipsy', 'glyph', 'guild', 'gulch', 'gully', 'gummy', 'guppy', 'gypsy', 'hilly', 'hippy', 'humid', 'humph', 'humus', 'hunch', 'hunky', 'husky', 'hussy', 'icily', 'icing', 'idyll', 'imply', 'jiffy', 'juicy', 'jumpy', 'kinky', 'lipid', 'livid', 'lucid', 'lucky', 'lumpy', 'lunch', 'lupus', 'lying', 'lymph', 'lynch', 'milky', 'mimic', 'minim', 'minus', 'missy', 'mucky', 'mucus', 'muddy', 'mulch', 'mummy', 'munch', 'mushy', 'music', 'musky', 'ninny', 'nymph', 'picky', 'piggy', 'pinch', 'pinky', 'pluck', 'plumb', 'plump', 'plunk', 'plush', 'pubic', 'pudgy', 'puffy', 'pulpy', 'punch', 'pupil', 'puppy', 'pushy', 'pygmy', 'quick', 'quill', 'shiny', 'shuck', 'shush', 'shyly', 'silky', 'silly', 'sissy', 'skiff', 'skill', 'skimp', 'skulk', 'skull', 'skunk', 'slick', 'slimy', 'sling', 'slink', 'slump', 'slung', 'slunk', 'slush', 'slyly', 'sniff', 'snuck', 'snuff', 'spicy', 'spiky', 'spill', 'spiny', 'spunk', 'squib', 'suing', 'sulky', 'sully', 'sunny', 'sushi', 'swill', 'swing', 'swish', 'swung', 'undid', 'unify', 'unzip', 'using', 'vigil', 'vinyl', 'vivid', 'vying', 'which', 'whiff', 'whiny', 'whisk', 'willy', 'wimpy', 'winch', 'windy', 'wispy']
t = data["a"]
starter = "roate"
print(starter)
print(json.dumps(Naive(starter, t, 1)))
