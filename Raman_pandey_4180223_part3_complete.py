## User class instead of namedtuple
class User:
    def __init__(self, name, UnitID, reward_points, supplementary_items_dict=None, capacity=3):
        self.name = name
        self.UnitID = UnitID
        self.reward_points = reward_points
        self.capacity = capacity  # Default capacity (no of beds)
        self.supplementary_items_dict = supplementary_items_dict or {}  # Dict to hold supplementary items

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
u4 = User("Riva", "U30duck", 100, {"car_park": 25, "breakfast": 21})

profiles = [u1, u2, u3, u4]

# Store guest order history
order_history = {}  # { "GuestName": [ { "items": [...], "total": ..., "earned": ... }, ... ] }


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


def get_id(apt_id):
    local_p = None
    for p in profiles:
        if p.UnitID == apt_id:
            local_p = p
            break
    return local_p


def update_apartment():
    while True:
        apt_id = input("Enter apartment Unit ID to book [eg : U20swan]:\n")
        if validate_apartment_id(apt_id):
            break
        else:
            print(" Error: Invalid apartment ID. Must contain swan/goose/duck.")

    p = get_id(apt_id)

    if p:
        print(f"Hello {p.name}!")
        print(f" Found User {p.name}: Apartment: {apt_id} || rate: ${p.reward_points} || capacity: {p.capacity}.")
        updated_value = input("Enter new values : [apartment_id rate capacity] : \n for ex: U20swan 195.0 3 \n").split()
        p.reward_points = float(updated_value[1])
        p.capacity = int(updated_value[2])
        print("Values updated successfully.")

    else:
        print(" Apartment not found in profiles.")
        print(" Adding new apartment details...")
        make_booking()


def update_supplementary_item():
    local_User = None

    apt_id = input("Enter apartment Unit ID to update supplementary item [eg : U20swan]:\n")
    p = get_id(apt_id)
    if p:
        print(f"Hello {p.name}!")
        print(f" Found User {p.name}: Apartment: {apt_id} || rate: ${p.reward_points} || capacity: {p.capacity}.")
        local_User = p
        if p.supplementary_items_dict == {}:
            print("No supplementary items found for this user.")
        else:
            for key, value in p.supplementary_items_dict.items():
                print(f"- {key} : ${value}")

    item_to_update = input(
        "Enter item ID and rate to update format : [item_1 rate_1, item_2 rate_2]\n for ex : toothpaste 54.5, breakfast 30 \n"
    ).strip().lower()
    item_parts = item_to_update.split(",")

    for part in item_parts:
        part_ = part.strip().split()
        if len(part_) == 2 and part_[0] in supplementary_items.keys():
            local_User.supplementary_items_dict[part_[0]] = float(part_[1])

    print(f" ({len(item_parts)}) Supplementary items updated/Added successfully.")


def make_booking():
    # --- Guest name validation ---
    while not (main_guest := input("Enter the name of main guest [eg : Oliver]:\n")).isalpha():
        print(" Error: Guest name must contain only letters.")

    # --- Number of guests validation ---
    while True:
        n_guests = input("Enter the number of guests [eg : 3]:\n")
        if n_guests.isdigit() and int(n_guests) > 0:
            n_guests = int(n_guests)
            break
        else:
            print(" Error: Number of guests must be a positive integer.")

    # --- Apartment ID validation ---
    max_beds = 2
    default_capacity = 3
    new_capacity = 0
    while True:
        unit_apartment = input("Enter apartment Unit ID to book [eg : U20swan]:\n")
        if validate_apartment_id(unit_apartment):
            if n_guests > default_capacity:
                print(f"Please consider ordering an extra bed.")
                n_beds_add = input("How many beds you want to add? (0-2): \n (each bed accommodates 2 guests) \n")

                if n_beds_add.isdigit() and 0 <= int(n_beds_add) <= max_beds:
                    n_beds_add = int(n_beds_add)
                    new_capacity = default_capacity + (n_beds_add * 2)
                    if new_capacity >= n_guests:
                        print(f" New capacity with extra beds is : {new_capacity}")
                        print(f"[AUTO] The Selected extra bed(s) cost: ${supplementary_items['extra_bed']['price'] * n_beds_add}")
                    else:
                        print("Booking cannot proceed as capacity is less than number of guests. \n Canceling booking...")
                        return

            apartment_type = next((apt for apt in apartment_rate_list if apt in unit_apartment), None)
            print(f"[AUTO] The Selected Unit rate is : ${apartment_rate_list[apartment_type]}")
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

    if new_capacity > 0:
        extras_selected_dict["extra_bed"] = supplementary_items['extra_bed']['price'] * n_beds_add
        extras_selected.append(("extra_bed", n_beds_add, supplementary_items['extra_bed']['price'] * n_beds_add))
        extras_total += supplementary_items['extra_bed']['price'] * n_beds_add

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
                print(f"[AUTO] The Selected Item rate is : ${supplementary_items[choice]['price']}")
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
                extras_selected_dict[choice] = cost
            else:
                print(" Error: Invalid item ID. Try again.")

    total_cost += extras_total

    # --- Reward Point Redemption ---
    guest_profile = next((u for u in profiles if u.name == main_guest), None)
    if guest_profile and guest_profile.reward_points >= 100:
        print(f"{guest_profile.name} currently has {guest_profile.reward_points} reward points.")
        use_points = input("Do you want to redeem your reward points for this booking? (y/n): ").lower()
        if use_points == "y":
            redeemable_sets = guest_profile.reward_points // 100
            redeemable_dollars = redeemable_sets * 10
            print(f"You can redeem up to ${redeemable_dollars} from this booking.")

            while True:
                try:
                    redeem_sets = int(input(f"How many sets of 100 points do you want to use? (0–{redeemable_sets}): "))
                    if 0 <= redeem_sets <= redeemable_sets:
                        break
                    else:
                        print(" Error: Please enter a valid number within the range.")
                except ValueError:
                    print(" Error: Please enter an integer.")

            if redeem_sets > 0:
                deduction = redeem_sets * 10
                total_cost -= deduction
                guest_profile.reward_points -= redeem_sets * 100
                print(f"[AUTO] ${deduction} has been deducted from your total cost using reward points.")
                print(f"[AUTO] Remaining reward points: {guest_profile.reward_points}")

    # update profiles (add new or update existing)
    for i, u in enumerate(profiles):
        if u.name == main_guest:
            updated_points = u.reward_points + reward_points
            u.reward_points = updated_points
            u.UnitID = unit_apartment
            u.supplementary_items_dict.update(extras_selected_dict)
            print(f" Updated {u.name}'s reward points to {updated_points}.")
            break
    else:
        profiles.append(User(main_guest, unit_apartment, reward_points, supplementary_items_dict=extras_selected_dict))

    # --- Save order to history ---
    order_items = []
    # Add apartment as item (always 1)
    order_items.append((unit_apartment, 1, apartment_rate_per_night))

    # Add extras
    for item, qty, cost in extras_selected:
        order_items.append((item, qty, cost))

    order_record = {
        "items": order_items,
        "total": round(total_cost, 2),
        "earned": reward_points
    }

    if main_guest in order_history:
        order_history[main_guest].append(order_record)
    else:
        order_history[main_guest] = [order_record]

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
        Bed Capacity (default): {default_capacity}
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
        print(
            f"- {u.name} | Unit ID: {u.UnitID} | Reward Points: {u.reward_points} | Capacity: {u.capacity} | Supplementary Items: {u.supplementary_items_dict if u.supplementary_items_dict else 'None'}"
        )


def show_apartments():
    print("\n -- Apartments and Rates: --")
    for apt, rate in apartment_rate_list.items():
        print(f"- {apt.title()} Apartment : ${rate} (AUD)")


# taken from chatgpt 

def show_guest_history():
    while True:
        name = input("Enter guest name to view history (or type 'exit' to return): ").strip().title()

        if name.lower() == "exit":
            return  # go back to menu

        # check if guest exists in profiles
        guest_profile = next((u for u in profiles if u.name == name), None)
        if not guest_profile:
            print(" Error: Guest not found. Please try again.")
            continue

        # check if guest has order history
        if name not in order_history or not order_history[name]:
            print(f"No booking history yet for {name}.")
            return

        # show history
        print(f"\nThis is the booking and order history for {name}.")
        print("List\t\tTotal Cost\tEarned Rewards")
        for i, order in enumerate(order_history[name], 1):
            items_str = ", ".join([f"{qty} x {nm}" for nm, qty, cost in order["items"]])
            print(f"Order {i}\t{items_str}\t{order['total']}\t{order['earned']}")
        return



def menu():
    while True:
        print("""
        =============================
        Debuggers Hut - Main Menu
        =============================
        1. Make a booking
        2. Add/update information of an apartment unit
        3. Add/update information of a supplementary item(s))
        4. Show all guests
        5. Show all apartments
        6. Exit
        7. Display a guest booking and order history
        """)
        choice = input("Enter your choice (1-7): ")

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
        elif choice == "7":
            show_guest_history()
        else:
            print(" Invalid choice. Please try again.")


print("""
*********************
      WELCOME TO
*** Debuggers Hut ***
*********************
""")

menu()
