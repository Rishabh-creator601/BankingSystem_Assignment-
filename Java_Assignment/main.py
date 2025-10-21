List =  ["wood","desk"]


name =  input("enter : ")




for i in List:
    if i == name:
        print(i)
        break
        
    else:
        List.append(name)
        print("not found")
        break 
    

print(List)



# name = input("Enter Object Name:")
# List = ["Desk","Chair","Wood"]
# for i in List:
#     if i == name :
#         print(i)
#     else :
#         List.append(name)
# print(List)