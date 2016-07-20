fobj = open("dictionary.txt", "r")
english_words = {}
german_words = {}
for line in fobj:
    line = line.strip() #removes linebreak
    assignment = line.split(" ")
    english_words[assignment[0]] = assignment[1]
    german_words[assignment[1]] = assignment[0]
fobj.close()
while True:
    word = input("Enter a Country or 'exit' to stop the program: ")
    if word == "exit":
        print("bye")
        break
    if word in english_words:
        print("The german word is:", english_words[word])
    elif word in german_words:
        print("The english word is:", german_words[word])
    else:
        if(input("Unknown word, Wanna add (y/n)? ") == "y"):
            fobj = open("dictionary.txt", "a")
            language = input("is '{}' (g)erman or (e)nglish?".format(word))
            if (language == "g"):
                fobj.write("{} {}\n".format(input("English pendant:"), word))
            else:
                fobj.write("{} {}\n".format(word, input("German pendant:")))
            fobj.close()
	 