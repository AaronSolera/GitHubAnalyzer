file = open("ouput.txt","w")
for i in range(0,10000000):
    file.seek(0)
    file.write(str(i)+"\r")
    file.truncate()
file.close()
