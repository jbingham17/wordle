There will 5 algorithm files:
1. Random.py which selects a random remaining word at each stage and uses that to solve the problem
2. R2.py secondary which starts at the best word and uses random remaining word from then on to solve. This is how most people play.
3. Naive.py which uses the best remaining word and guesses the best remaining word where "best" picks the word that results in the fewest possibilities at the next level.
4. N2 which uses the best word and guesses the best word where "best" picks the word that results in the fewest possibilities at the next level.
5. bucket.py which uses the best word and picks the best word where "best" results in the most buckets of possibilities at the next level.
6. short.py which uses the best word and picks the best word where "best" results in the smallest worse case bucket.
