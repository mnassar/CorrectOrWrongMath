
def populate():
    scoreboard = {}
    with open ("scoreboard.txt", 'r') as f:
        for line in f.readlines():
            l = line.split()
            k = l[0]
            v = int(l[1])
            scoreboard [ k ] = v


    return {k: v for k, v in sorted(scoreboard.items(), key=lambda item: item[1], reverse=True)}

def update_scoreboard(username, score, scoreboard):
    print ("username", username)
    print (scoreboard)
    if username in scoreboard:
        scoreboard[username] = score + scoreboard[username]
    else:
        scoreboard[username] = score
    with open("scoreboard.txt", 'w') as f:
        for k, v in scoreboard.items():
            f.write(k + " " + str(v) + "\n")







