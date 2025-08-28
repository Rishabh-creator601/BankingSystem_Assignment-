
from datetime import datetime
from collections import namedtuple






## default user profiles and lists 

User = namedtuple("User",["name","UnitID","reward_points"])
apartment_rate_list =  {"duck":106.7,"goose":145.2,"swan":95.0}


u1  =  User("Alyssa","U12swan",20)
u2 =  User("Luigi","U20goose",50)
u3 =  User("Oliver","U49GOOSE",45)


profiles = [u1,u2,u3]


print("""
*********************
      WECOME TO
*** Debuggers Hut ***
*********************""")




print("""
-- Welcome to Apartment Management System --
Our buildings are:
- Swan
- Goose 
- Duck 

""")


now  = datetime.now().strftime("%d/%m/%Y")

main_guest =  input("Enter the name of main guest [eg : Oliver]:\n")
n_guests = int(input("Enter the number of guests [eg : 3]:\n"))
unit_apartment = input("Enter apartment Unit ID to book [ex :  U20swan]:\n")
check_in_date =  input("Enter check-in date [format :  d/m/yyyy]:\n")
check_out_date = input("Enter check-out date [format :  d/m/yyyy]:\n")
stay_length =  int(input("Enter length of stay [in days]:\n"))
date_input  =  input(f"Enter booking date [i.e : {now} ][default : Y]:\n")
booking_date = now if date_input.lower() == 'y' or date_input == '' else date_input


## calculating apartment rate
for apt,rate in apartment_rate_list.items():
    if apt in unit_apartment.lower():
        apartment_rate_per_night = rate
        break
    
## calculating total cost and reward points
total_cost = apartment_rate_per_night * stay_length
reward_points = round(total_cost)

user =  User( main_guest,unit_apartment,reward_points)
profiles.append(user)

print("\nUser name : {} | Unit ID : {} | Reward Points : {} added to the list".format(user.name,user.UnitID,user.reward_points))




print(f"""
=========================================================
 Debuggers Hut Serviced Apartments - Booking Receipt
=========================================================
Guest Name: {main_guest}
Number of guests: {n_guests}
Apartment name: {unit_apartment}
Apartment rate: ${apartment_rate_per_night} (AUD)
Check-in date: {check_in_date}
Check-out date: {check_out_date}
Length of stay: {stay_length} (nights)
Booking date: {booking_date}
--------------------------------------------------------------------------------
Total cost: ${total_cost} (AUD)
Earned rewards: {reward_points} (points)
Thank you for your booking! We hope you will have an enjoyable stay.
=========================================================
""")
