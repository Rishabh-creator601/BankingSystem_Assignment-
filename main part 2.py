## User class instead of namedtuple
class User:
    def __init__(self, name, UnitID, reward_points,supplementary_items_dict={},capacity=1):
        self.name = name
        self.UnitID = UnitID
        self.reward_points = reward_points
        self.capacity =  capacity # Default capacity (no of beds)
        self.supplementary_items_dict =  supplementary_items_dict  # Dict to hold supplementary items

    def __repr__(self):
        return f"User(name={self.name}, UnitID={self.UnitID}, reward_points={self.reward_points})"


apartment_rate_list = {"duck": 106.7, "goose": 145.2, "swan": 95.0}

# Supplementary items
supplementary_items = {
    "car_park": {"price": 25, "desc": "Car park for 1 car (per night)"},
    "breakfast": {"price": 21, "desc": "Continental breakfast meal (per person)"},
    "toothpaste": {"price": 5, "desc": "Toothpaste (generic brand)"},
    "extra_bed": {"price": 50, "desc": "Removable extra bed (per night, fits 2)"}
}

## default profiles
u1 = User("Alyssa", "U12swan", 20)
u2 = User("Luigi", "U20goose", 50)
u3 = User("Oliver", "U49goose", 457)
u4 =  User("Riva","U30duck",100,{"car_park":25,"breakfast":21})

profiles = [u1, u2, u3, u4]


def validate_apartment_id(apt_id):
    if not apt_id.startswith("U"):
        return False
    # Remove leading 'U' and split number from building name
    num_part = ""
    i = 1
    while i < len(apt_id) and apt_id[i].isdigit():
        num_part += apt_id[i]
        i += 1
    building_part = apt_id[i:].lower()
    if not num_part.isdigit() or building_part not in ["swan", "goose", "duck"]:
        return False
    return True


def update_apartment():
    
    while True:
        apt_id = input("Enter apartment Unit ID to book [eg : U20swan]:\n")
        if validate_apartment_id(apt_id):
            break
        else:
            print(" Error: Invalid apartment ID. Must contain swan/goose/duck.")
        
    for p in profiles:
        if p.UnitID == apt_id:
            print("Hello {p.name} !")
            print(f" found User {p.name}: Apartment : {apt_id} || rate :  ${p.reward_points} || capacity : { p.capacity}.")
            updated_value =  input("Enter new values : [apartment_id rate capacity] : \n for ex: U20swan 195.0 3 \n").split()
            p.reward_points = float(updated_value[1])
            p.capacity = int(updated_value[2])
            print("Values updated successfully.")
            break 
    else:
        print(" Apartment not found in profiles.")
        print(" Adding new apartment details...")
        make_booking()
        
        

def update_supplementary_item():
    
    
    apt_id =  input("Enter apartment Unit ID to update supplementary item [eg : U20swan]:\n")
    
        
    for p in profiles:
        if p.UnitID == apt_id:
           print(f"Hello {p.name} !")
           print(f" found User {p.name} : Apartment : {apt_id} || rate :  ${p.reward_points} || capacity : { p.capacity}.")
           if p.supplementary_items_dict == {}:
               print("No supplementary items found for this user.")
           else:
               for key , value in p.supplementary_items_dict.items():
                   print(f"- {key} : ${value}")
            
    item_to_update = input("Enter item ID and rate to update format : [item_id 45]\n for ex :  toothpaste 54.5 \n").strip().lower()
    item_parts = item_to_update.split()
    supp_id =  item_parts[0]
    new_rate = float(item_parts[1])
    if supp_id in list(p.supplementary_items_dict.keys()):
        p.supplementary_items_dict[supp_id] = new_rate
        print(f" Supplementary item {supp_id} updated to ${new_rate}.")
            
        
           
            
    



def make_booking():

    # --- Guest name validation ---

    while not (main_guest := input("Enter the name of main guest [eg : Oliver]:\n")).isalpha():
        print(" Error: Guest name must contain only letters.")

    # --- Number of guests validation ---

    try:
        
        while not (n_guests := input("Enter the number of guests [eg : 3]:\n")).isdigit() or int(n_guests) <= 0:
            print(" Error: Number of guests must be a positive integer.")
            n_guests = int(n_guests)
    except:
        print(" Error: Please enter a valid integer.")

    # --- Apartment ID validation ---
    while True:
        unit_apartment = input("Enter apartment Unit ID to book [eg : U20swan]:\n")
        if validate_apartment_id(unit_apartment):
            break
        else:
            print(" Error: Invalid apartment ID. Must contain swan/goose/duck.")

    check_in_date = input("Enter check-in date [format : d/m/yyyy]:\n")
    check_out_date = input("Enter check-out date [format : d/m/yyyy]:\n")

    # --- Stay length validation ---
    while True:
        try:
            stay_length = int(input("Enter length of stay [1–7 days]:\n"))
            if 1 <= stay_length <= 7:
                break
            else:
                print(" Error: Stay length must be between 1 and 7 days.")
        except:
            print(" Error: Please enter a valid integer.")

    # --- Booking date (default today) ---
    booking_date = input(f"Enter booking date [format : d/m/yyyy]\n")
    

    # calculate apartment rate
    for apt, rate in apartment_rate_list.items():
        if apt in unit_apartment.lower():
            apartment_rate_per_night = rate
            break

    # total cost & reward points
    total_cost = apartment_rate_per_night * stay_length
    reward_points = round(total_cost)

    # --- Supplementary items ---
    extras_total = 0
    extras_selected = []
    extras_selected_dict = {}
    while (want_extras := input("Do you want supplementary items? (y/n): ").lower()) not in ["y", "n"]:
        print(" Error: Please answer with y or n.")

    if want_extras == "y":
        print("\nAvailable Supplementary Items:")
        for item, details in supplementary_items.items():
            print(f"- {item} : ${details['price']} | {details['desc']}")

        while True:
            choice = input("\nEnter item ID to add (or 'done' to finish): ").strip().lower()
            if choice == "done":
                break
            if choice in supplementary_items:
                while True:
                    try:
                        qty = int(input(f"Enter quantity for {choice}: "))
                        if qty > 0:
                            break
                        else:
                            print(" Error: Quantity must be greater than 0.")
                    except ValueError:
                        print(" Error: Please enter a valid integer.")
                cost = supplementary_items[choice]["price"] * qty
                extras_total += cost
                extras_selected.append((choice, qty, cost))
                extras_selected_dict[choice] = cost # Store in dict
            else:
                print(" Error: Invalid item ID. Try again.")

    # Add extras to total
    total_cost += extras_total

    # update profiles (add new or update existing)
    for i, u in enumerate(profiles):
        if u.name == main_guest:
            updated_points = u.reward_points + reward_points
            profiles[i] = User(u.name, unit_apartment, updated_points)
            break
    else:
        profiles.append(User(main_guest, unit_apartment, reward_points,supplementary_items_dict=extras_selected_dict))

    # print receipt
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
        Bed Capacity (default): 1
        --------------------------------------------------------------------------------""")

    if extras_selected:
        print("Supplementary Items:")
        for item, qty, cost in extras_selected:
            print(f"- {item} x {qty} = ${cost}")
        print("--------------------------------------------------------------------------------")

    print(f"""Total cost: ${total_cost} (AUD)
        Earned rewards: {reward_points} (points)
        Thank you for your booking! We hope you will have an enjoyable stay.
        =========================================================
        """)


def show_guests():
    print("\n -- Guest Profiles: --")
    for u in profiles:
        print(f"- {u.name} | Unit ID: {u.UnitID} | Reward Points: {u.reward_points} | Capacity: {u.capacity} | Supplementary Items: {u.supplementary_items_dict  if u.supplementary_items_dict else 'None' }")


def show_apartments():
    print("\n -- Apartments and Rates: --")
    for apt, rate in apartment_rate_list.items():
        print(f"- {apt.title()} Apartment : ${rate} (AUD)")


def menu():
    while True:
        print("""
        =============================
        Debuggers Hut - Main Menu
        =============================
        1. Make a booking
        2. Add/update information of an apartment unit
        3. Add/update information of a supplementary item
        4. Show all guests
        5. Show all apartments
        6. Exit
        """)
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            make_booking()
        elif choice == "2":
            update_apartment()
        
        elif choice == "3":
            update_supplementary_item()
        elif choice == "4":
            show_guests()
        elif choice == "5":
            show_apartments()
        elif choice == "6":
            print(" Thank you for using Debuggers Hut Booking System!")
            break
        else:
            print(" Invalid choice. Please try again.")


print("""
*********************
      WELCOME TO
*** Debuggers Hut ***
*********************
""")

menu()
