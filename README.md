Check out my medium post on the topic to explain:


This repo contains 4 algorithms.
Each folder for the algorithms contains:
.py the algorithm itself. Has a function to output the first word and others for recursion
.json the resultant best method for play from the algorithm
.txt output of the file's stats

The algorithms are:

1. Naive which uses the best remaining word and guesses the best remaining word where "best" picks the word that results in the fewest possibilities at the next level.
2. N2 which uses the best word and guesses the best word where "best" picks the word that results in the fewest possibilities at the next level.
3. Shortest which uses the best word and picks the best word where "best" results in the smallest worse case bucket.
4. Buckets which uses the best word and picks the best word where "best" results in the most buckets of possibilities at the next level.

Stats.py takes in a json file as its argument and outputs the stats of the algorithm
parseDict.py allows a user to play wordle, and can use a json to give suggestions.
  It also can print a bar chart of letter frequencies
dict.json
