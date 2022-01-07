import json

file = "shortestRaise.json"
with open(file) as json_file:
    data = json.load(json_file)

with open('dict.json') as di:
    check = json.load(di)["a"]

found = set(check)

def recurs(data):
    if data == 1:
        return data
    data = str(data).replace("'", '"')
    data = json.loads(data)
    d = {}
    for key in data:
        d[key] = recurs(data[key])
    return d

alg = recurs(data)
guess1 = 0
guess2 = 0
guess3 = 0
guess4 = 0
guess5 = 0
guess6 = 0
failed = 0

for a in alg:
    for b in alg[a]:
        if str(type(alg[a][b])) == str(type(1)):
            guess2 += 1
        else:
            for c in alg[a][b]:
                for d in alg[a][b][c]:
                    if d == b:
                        guess2 += 1
                        guess3 -= 1
                    if str(type(alg[a][b][c][d])) == str(type(1)):
                        guess3 += 1
                    else:
                        for e in alg[a][b][c][d]:
                            for f in alg[a][b][c][d][e]:
                                if f == d:
                                    guess3 += 1
                                    guess4 -= 1
                                if str(type(alg[a][b][c][d][e][f])) == str(type(1)):
                                    guess4 += 1
                                else:
                                    for g in alg[a][b][c][d][e][f]:
                                        for h in alg[a][b][c][d][e][f][g]:
                                            if h == f:
                                                guess4 += 1
                                                guess5 -= 1
                                            if str(type(alg[a][b][c][d][e][f][g][h])) == str(type(1)):
                                                guess5 += 1
                                            else:
                                                for i in alg[a][b][c][d][e][f][g][h]:
                                                    for j in alg[a][b][c][d][e][f][g][h][i]:
                                                        if i == h:
                                                            guess5 += 1
                                                            guess6 -= 1
                                                        if str(type(alg[a][b][c][d][e][f][g][h][i][j])) == str(type(1)):
                                                            guess6 += 1
                                                        else:
                                                            for k in alg[a][b][c][d][e][f][g][h][i][j]:
                                                                for l in alg[a][b][c][d][e][f][g][h][i][j][k]:
                                                                    if i == l:
                                                                        guess6 += 1
                                                                        failed -= 1
                                                                    if str(type(alg[a][b][c][d][e][f][g][h][i][j][k][l])) == str(type(1)):
                                                                        failed += 1
                                                                    else:
                                                                        for m in alg[a][b][c][d][e][f][g][h][i][j][k][l]:
                                                                            for n in alg[a][b][c][d][e][f][g][h][i][j][k][l][m]:
                                                                                if str(type(alg[a][b][c][d][e][f][g][h][i][j][k][l][m][n])) == str(type(1)):
                                                                                    failed += 1
                                                                                else:
                                                                                    for o in alg[a][b][c][d][e][f][g][h][i][j][k][l][m][n]:
                                                                                        for p in alg[a][b][c][d][e][f][g][h][i][j][k][l][m][n][o]:
                                                                                            if str(type(alg[a][b][c][d][e][f][g][h][i][j][k][l][m][n][o][p])) == str(type(1)):
                                                                                                failed += 1
                                                                                            else:
                                                                                                pass

guessRate = guess1+2*guess2+3*guess3+4*guess4+5*guess5+6*guess5
print("Guess 1: ", guess1)
print("Guess 2: ", guess2)
print("Guess 3: ", guess3)
print("Guess 4: ", guess4)
print("Guess 5: ", guess5)
print("Guess 6: ", guess6)
print("Failed: ", failed)
tot = guess1+guess2+guess3+guess4+guess5+guess6+failed
print("Total: ", tot)
print("Average guesses: ", guessRate/tot)
