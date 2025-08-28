## User class instead of namedtuple
class User:
    def __init__(self, name, UnitID, reward_points):
        self.name = name
        self.UnitID = UnitID
        self.reward_points = reward_points

    def __repr__(self):
        return f"User(name={self.name}, UnitID={self.UnitID}, reward_points={self.reward_points})"


## default user profiles and lists 
apartment_rate_list = {"duck": 106.7, "goose": 145.2, "swan": 95.0}

u1 = User("Alyssa", "U12swan", 20)
u2 = User("Luigi", "U20goose", 50)
u3 = User("Oliver", "U49GOOSE", 45)

profiles = [u1, u2, u3]

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

main_guest = input("Enter the name of main guest [eg : Oliver]:\n")
n_guests = int(input("Enter the number of guests [eg : 3]:\n"))
unit_apartment = input("Enter apartment Unit ID to book [ex :  U20swan]:\n")
check_in_date = input("Enter check-in date [format :  d/m/yyyy]:\n")
check_out_date = input("Enter check-out date [format :  d/m/yyyy]:\n")
stay_length = int(input("Enter length of stay [in days]:\n"))
booking_date = input("Enter booking date [format : d/m/yyyy]:\n")

## calculating apartment rate
apartment_rate_per_night = None
for apt, rate in apartment_rate_list.items():
    if apt in unit_apartment.lower():
        apartment_rate_per_night = rate
        break

if apartment_rate_per_night is None:
    print("❌ Invalid apartment Unit ID!")
    exit()

## calculating total cost and reward points
total_cost = apartment_rate_per_night * stay_length
reward_points = round(total_cost)

user = User(main_guest, unit_apartment, reward_points)
profiles.append(user)

print("\nUser name : {} | Unit ID : {} | Reward Points : {} added to the list"
      .format(user.name, user.UnitID, user.reward_points))

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
