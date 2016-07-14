integerValue = 1
floatingPoint = 1.5
string1 = "Hello"
string2 = 'World'
list = [1, "two", ["another",'list']]

print("integer:", integerValue)
print("floating point:", floatingPoint)
print("String concatenation:", string1, string2) # print with comma adds space between string1 and string2
print("List:", list)
print ("addition:", 1 + 1)
print ("division resulting in fp:", 4 / 2) # floating Point
print ("division resulting in int:", 4 // 2) # integer

print("--------- dictionary ------------ ")
dictionary = {'key1' : "value1", 2:1.5}
print(dictionary["key1"])
print(dictionary[2])
dictionary["key1"] = "anotherValue" # change value of existing key
print(dictionary["key1"])
dictionary["key3"] = "value 3" # add new value
print(dictionary["key3"])
