fobj = open("dictionary.txt", "r")
words = {}
for line in fobj:
    line = line.strip() #removes linebreak
    assignment = line.split(" ")
    words[assignment[0]] = assignment[1]
fobj.close()
print(words)