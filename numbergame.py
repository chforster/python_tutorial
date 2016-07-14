secret = 1234
choosen = 0
counter = 0
while choosen != secret:
    choosen = int(input("waehl weise:"))
    if choosen == 0:
        print("ABBRUCH DURCH 0")
        break
    if choosen < secret:
	    print("z'kloan")
		
    if choosen > secret:
	    print("z'gross")
    counter = counter + 1
else: # While else - wird nur ausgeführt wenn while = false bzw. kein Break
    print("disco in", counter)

