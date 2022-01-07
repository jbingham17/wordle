import json
import random
import re

aLen = 2315

with open('dict.json') as json_file:
    data = json.load(json_file)

def randWord(data):
    return data["a"][random.randrange(0,aLen)]

# Creates Global variable for the total bank of words that we can guess with
possGuesses = sorted(data["b"]+data["a"])
count = 0

# Function outputs the best first word based on our specified criteria
# This algorithm finds the best word by finding the word that leaves the fewest
# words remaining at the next level
def bucketFW(data):
    possAnswers = sorted(list(data))

    total = {}
    tops = {}
    maxTotal = 145
    totalWord = ''

    # Filters out all possible answers that don't have repeat letters and only
    # contain the common letters: [aeilnorsty]. This is done to improve execution time
    p = re.compile(r"(?!.*(\w).*\1{1})[acdehilnoprstuy]{5}")
    pG= list(filter(p.match, possGuesses))

    # Searches through each of our filtered guesses for every possible answer
    # This will help us determine which guess gives us the fewest remaining at the
    # Next level
    for g in pG:
        total[g] = 0
        used = set()
        for word in possAnswers:
            if word in used:
                continue
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
            results = list(filter(r.match, possAnswers))
            for u in results:
                used.add(u)
            total[g]+=1
        if total[g] > maxTotal:
            maxTotal = total[g]
            totalWord = g
        if total[g] > 145:
            print(g, total[g])
    return totalWord

# Function outputs the best non first word based on our specified criteria
# This algorithm finds the best word by finding the word that leaves the fewest
# words remaining at the next level
def bucketSW(data):
    l = len(data)
    if l == 1 or l == 2:
        return data[0]
    possAnswers = sorted(set(data))
    total = {}
    tops = {}
    maxTotal = 0

    totalWord = ''
    # We no longer filter out any guesses, since the subsequent next best guess
    # tends to be pretty counterintuitive

    # We start with the remaining words since they are more likely to be the answer
    pG = possAnswers+possGuesses
    for g in pG:
        total[g] = 0
        used = set()
        for word in possAnswers:
            if word in used:
                continue
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
            results = list(filter(r.match, possAnswers))
            for u in results:
                used.add(u)
            total[g]+=1
        if total[g] > maxTotal:
            maxTotal = total[g]
            totalWord = g

    return totalWord

# Recursive function that finds the buckets of words for the next generation.
# Will call bucketSW to grab the best word for the next generation bucket
def Bucket(w, possAnswers):

    # Recursive base case
    l = len(possAnswers)
    if l == 1 or l == 0:
        print("Hello")
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
        gu = bucketSW(bucket[2:])
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
        fin[res][gu] = Bucket(gu, bucket[2:])

    return fin

# Main code. Initializes the set of words and calls our recursive function which
# will output the json decision tree for us to use

# t = ['biddy', 'billy', 'blimp', 'blind', 'blink', 'bliss', 'bluff', 'blush', 'buddy', 'buggy', 'build', 'bulky', 'bully', 'bunch', 'bunny', 'bushy', 'chick', 'child', 'chili', 'chill', 'chuck', 'chump', 'chunk', 'cinch', 'civic', 'civil', 'click', 'cliff', 'climb', 'cling', 'clink', 'cluck', 'clump', 'clung', 'cubic', 'cumin', 'cynic', 'dilly', 'dimly', 'dingy', 'dizzy', 'duchy', 'dully', 'dummy', 'dumpy', 'dusky', 'dying', 'ficus', 'filly', 'filmy', 'finch', 'fishy', 'fizzy', 'flick', 'fling', 'fluff', 'fluid', 'flung', 'flunk', 'flush', 'fully', 'fungi', 'funky', 'funny', 'fussy', 'fuzzy', 'giddy', 'gipsy', 'glyph', 'guild', 'gulch', 'gully', 'gummy', 'guppy', 'gypsy', 'hilly', 'hippy', 'humid', 'humph', 'humus', 'hunch', 'hunky', 'husky', 'hussy', 'icily', 'icing', 'idyll', 'imply', 'jiffy', 'juicy', 'jumpy', 'kinky', 'lipid', 'livid', 'lucid', 'lucky', 'lumpy', 'lunch', 'lupus', 'lying', 'lymph', 'lynch', 'milky', 'mimic', 'minim', 'minus', 'missy', 'mucky', 'mucus', 'muddy', 'mulch', 'mummy', 'munch', 'mushy', 'music', 'musky', 'ninny', 'nymph', 'picky', 'piggy', 'pinch', 'pinky', 'pluck', 'plumb', 'plump', 'plunk', 'plush', 'pubic', 'pudgy', 'puffy', 'pulpy', 'punch', 'pupil', 'puppy', 'pushy', 'pygmy', 'quick', 'quill', 'shiny', 'shuck', 'shush', 'shyly', 'silky', 'silly', 'sissy', 'skiff', 'skill', 'skimp', 'skulk', 'skull', 'skunk', 'slick', 'slimy', 'sling', 'slink', 'slump', 'slung', 'slunk', 'slush', 'slyly', 'sniff', 'snuck', 'snuff', 'spicy', 'spiky', 'spill', 'spiny', 'spunk', 'squib', 'suing', 'sulky', 'sully', 'sunny', 'sushi', 'swill', 'swing', 'swish', 'swung', 'undid', 'unify', 'unzip', 'using', 'vigil', 'vinyl', 'vivid', 'vying', 'which', 'whiff', 'whiny', 'whisk', 'willy', 'wimpy', 'winch', 'windy', 'wispy']
t = data["a"]
starter = "trace"
print(starter)
print(json.dumps(Bucket(starter, t)))

# print(bucketFW(data["a"]))
