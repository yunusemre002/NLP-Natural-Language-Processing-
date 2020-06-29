textList = ["One", "Two", "Three", "Four", "Five"]
#
# outF = open("myOutFile.txt", "w+")
# for line in textList:
#     k = line
#     outF.write(line)
#     outF.write("\n")
# print(k)

outF = open("myOutFile1.txt", "r")
listOfAttribute = outF.readlines()
print(listOfAttribute)

hotel = listOfAttribute[0].split(",")
staff = listOfAttribute[1].split(",")
loc = listOfAttribute[2].split(",")
room = listOfAttribute[3].split(",")
breakfast = listOfAttribute[4].split(",")
bed = listOfAttribute[5].split(",")
service = listOfAttribute[6].split(",")
bath = listOfAttribute[7].split(",")
view = listOfAttribute[8].split(",")
food = listOfAttribute[9].split(",")
rest = listOfAttribute[10].split(",")

print(type(hotel), hotel, sep="\n")
print(staff)
print(loc)
print(room)


outF.close()