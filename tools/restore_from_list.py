# Open the file as f.
from typing import Counter


f = open('tools\list.txt', 'r')

# get the content, list of lines
content = f.read().splitlines()

# we know the format of the file (copy pasted from bot ".perc list" output) is:
# Player
# name1
# name2
# ...
# Count
# count1
# count2
# ...

# find the number of players
numPlayers = content.index('Count')

s = ''

# loop through all players in the list
for i in range(1,numPlayers):
    # and add their names to the string once for each point they have
    for j in range(int(content[i + numPlayers])):
        s = s + ' ' + content[i]
    # print(content[i+numPlayers])
    # print(content[i])

# print the command string
print('.perc add' + s)