textList = ["One", "Two", "Three", "Four", "Five"]
#
# outF = open("myOutFile.txt", "w+")
# for line in textList:
#     k = line
#     outF.write(line)
#     outF.write("\n")
# print(k)

outF = open("../Dataset/txt files/myOutFile1.txt", "r")
listOfAttribute = outF.readlines()
print(listOfAttribute)

hotel = listOfAttribute[0].split(",")
staff = listOfAttribute[1].split(",")
loc = listOfAttribute[2].split(",")
room = listOfAttribute[3].split(",")

print(type(hotel), hotel, sep="\n")
print(staff)
print(loc)
print(room)


outF.close()