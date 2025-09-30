import csv 

with open("products.csv","r") as f:
    file =  csv.reader(f)
    
    for i in file :
        print(i[0])