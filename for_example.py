print("Iteriere durch List")
for x in [1,2,3]:
    print(x)
	
print ("Iteriere durch String")
for c in "Python":
    print(c)
else:
    print("auch hier ist ein for - else moeglich welches ausgefuehrt wird, wenn die Forschleife regulaer beendet wird")
	
print("range with end value")
for i in range(3):
    print(i)
	
print("range with start value and end")
for j in range(2,4):
    print(j)
	
print("range with start- and end value and incrementor")
for k in range(1,8,2):
    print(k)
	
print("range with start- and end value and incrementor - negative")
for l in range(8,1,-2):
    print(l)