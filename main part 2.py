
from datetime import datetime
from collections import namedtuple


User = namedtuple("User", ["name", "UnitID", "reward_points"])
apartment_rate_list = {"duck": 106.7, "goose": 145.2, "swan": 95.0}

# Supplementary items
supplementary_items = {
    "car_park": {"price": 25, "desc": "Car park for 1 car (per night)"},
    "breakfast": {"price": 21, "desc": "Continental breakfast meal (per person)"},
    "toothpaste": {"price": 5, "desc": "Toothpaste (generic brand)"},
    "extra_bed": {"price": 50, "desc": "Removable extra bed (per night, fits 2)"}
}


## default profiles

u1 = User("Alyssa", "U12swan", 20),
u2 = User("Luigi", "U20goose", 50),
u3 =   User("Oliver", "U49goose", 45)


profiles  = [u1,u2,u3]


def make_booking():
    now = datetime.now().strftime("%d/%m/%Y")

    # --- Guest name validation ---
    while True:
        main_guest = input("Enter the name of main guest [eg : Oliver]:\n")
        if main_guest.isalpha():
            break
        else:
            print(" Error: Guest name must contain only letters.")

    # --- Number of guests --- validation ---
    while True:
        try:
            n_guests = int(input("Enter the number of guests [eg : 6]:\n"))
            if n_guests > 0:
                break
            else:
                print(" Error: Number of guests must be greater than 0.")
        except :
            print(" Error: Please enter a valid integer.")

    # --- Apartment ID validation ---
    while True:
        unit_apartment = input("Enter apartment Unit ID to book [eg : U20swan]:\n")
        if any(apt in unit_apartment.lower() for apt in apartment_rate_list):
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
        except :
            print(" Error: Please enter a valid integer.")

    # --- Booking date (default today) ---
    date_input = input(f"Enter booking date [i.e : {now}] [default : Y]:\n")
    booking_date = now if date_input.lower() == "y" or date_input.strip() == "" else date_input

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
    while True:
        want_extras = input("Do you want supplementary items? (y/n): ").lower()
        if want_extras in ["y", "n"]:
            break
        else:
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
        profiles.append(User(main_guest, unit_apartment, reward_points))

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
        print(f"- {u.name} | Unit ID: {u.UnitID} | Reward Points: {u.reward_points}")


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
2. Show all guests
3. Show all apartments
4. Exit
""")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            make_booking()
        elif choice == "2":
            show_guests()
        elif choice == "3":
            show_apartments()
        elif choice == "4":
            print(" Thank you for using Debuggers Hut Booking System!")
            break
        else:
            print(" Invalid choice. Please try again.")


if __name__ == "__main__":
    print("""
*********************
      WELCOME TO
*** Debuggers Hut ***
*********************
""")

    menu()
