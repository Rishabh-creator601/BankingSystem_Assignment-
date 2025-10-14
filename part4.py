import csv,sys 
from datetime import datetime



'''
NAME : 
STUDENT ID : 
Highest level of attempted : All the requirements 
May malfunction  in calcuation of reward points 

'''



args = sys.argv[1:]

# Default filenames
GUEST_FILE = "guests.csv"
PRODUCT_FILE = "products.csv"
ORDER_FILE = "orders.csv"

if len(args) == 0:
    guest_file, product_file, order_file = GUEST_FILE, PRODUCT_FILE, ORDER_FILE
elif len(args) == 2:
    guest_file, product_file = args
    order_file = ORDER_FILE
elif len(args) == 3:
    guest_file, product_file, order_file = args
else:
    print("⚠️ Incorrect usage!\n")
    print("Usage: python part4.py <guest_file> <product_file> [order_file]")
    sys.exit(1)

print(f" Guests => {guest_file}  |  Products => {product_file}  |  Orders => {order_file}")






def read_csv_file(filename,encoding="utf-8"):
    csvFile = None 
    with open(filename, mode ='r',encoding=encoding) as file:
        csvFile = csv.reader(file)
        data = list(csvFile)
    return data



## Searching for file
try :
    guests =  read_csv_file(guest_file,encoding="utf-8-sig")
    print(" ✔️ File Found and loaded ")
except :
    print("⚠️⚠️ Warning : File not found , please insert it in local directory !!!")


# ---------- GUEST  --------
class Guest:
    def __init__(self, guest_id, name,reward_points):

        self.id = guest_id
        self.name = name
        self.reward_points  = reward_points ## Initalized 50 points for each guest 
        self.reward_rate = 1.0    
        self.redeem_rate = 0.01     

    # Method to calculate reward based on total cost
    def calculate_reward(self, total_cost):
        reward_points = round(total_cost * self.reward_rate)
        return reward_points
        
    
    def get_reward(self,cost):
        self.reward_points += abs(cost * self.reward_rate)
    
    def update_reward(self,value):
        self.reward_points += value 
    
    def get_discount(self):
        discount  = self.reward_points * self.redeem_rate 
        return discount

    # Method to display guest information
    def display_info(self):
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Reward Points: {self.reward_points}")
        print(f"Reward Rate: {self.reward_rate * 100}%")
        print(f"Redeem Rate: {self.redeem_rate * 100}%")


    def set_reward_rate(self, rate_percent):
        self.reward_rate = rate_percent / 100.0


    def set_redeem_rate(self, rate_percent):
        self.redeem_rate = rate_percent / 100.0
        
        
## ------------- helper functions ------------------
## a function to validate if the input is positive and int      
def input_positive_int(prompt,target ,min_value=1):
    """Prompt user until a positive integer (≥ min_value) is entered."""
    while True:
        try:
            val = float(input(prompt))
            if val < min_value:
                raise ValueError
            return val
        except ValueError:
            print(f"⚠️ Invalid {target}. Must be a positive number.")


def validate_positive(value_str,target):
    
    is_pos =  False 
    try:
        value = float(value_str)
        if value > 0:
            is_pos = True   
        else:
            raise ValueError("Value must be positive")

    except ValueError:
        print(f"⚠️ Invalid {target}. Must be a positive number.")
    return is_pos
        
        

           

# ----------- Product ----------
class Product:
    def __init__(self, product_id, name, price):

        self.id = product_id
        self.name = name
        self.price = price
        
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def display_info(self):
        pass


# ------------- Apartment Unit -------------
'''
Apartment Units are :
- Swan  : 100 rooms 
- Goose :  100 rooms 
- Duck : 100 rooms 

'''
# apt rates from previous assignment 
apt_rates =  {"swan":95,
              "duck":106.7,
              "goose":145.2}

class ApartmentUnit(Product):
    def __init__(self, product_id, name, price, capacity=3):

        super().__init__(product_id, name, price)
        self.capacity = capacity

    # Getter 
    def get_capacity(self):
        return self.capacity

    def display_info(self):
        print(f"Apartment ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Price per night: {self.get_price()}")
        print(f"Capacity: {self.capacity} guests")
        
        
        
class Bundle:
    def __init__(self, bundle_id, name, components, price):
        self.id = bundle_id
        self.name = name
        self.components = components  # list of product IDs
        self.price = price

    def display_components(self):
        counts = {}
        for comp in self.components:
            counts[comp] = counts.get(comp, 0) + 1

        return ', '.join(f"{qty} x {comp}" if qty > 1 else comp for comp, qty in counts.items())


    def display(self):
        print(f"{self.id}\t{self.name}\t{self.display_components()}\t{self.price}")
        
        
        
# --------------- Supplementary Item ----------------
class SupplementaryItem(Product):
    def __init__(self, product_id, name, price):
        super().__init__(product_id, name, price)


    def display_info(self):
        print(f"Supplementary Item ID: {self.get_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Price: {self.get_price()}")
        


def generate_receipt(
    guest_name, number_of_guests,apartment_name, apartment_rate,
    checkin_date, checkout_date, nights,booking_date,apartment_sub_total,
    supplementary_items,  # list of tuples: (id, name, qty, unit_price)
    supp_sub_total,total_cost, reward_points, discount, final_total, earned_rewards
):
    print("="*80)
    print(f"Guest name: {guest_name}")
    print(f"Number of guests: {number_of_guests}")
    print(f"Apartment name: {apartment_name}")
    print(f"Apartment rate: $ {apartment_rate:.2f} (AUD)")
    print(f"Check-in date: {checkin_date}")
    print(f"Check-out date: {checkout_date}")
    print(f"Length of stay: {nights} (nights)")
    print(f"Booking date: {booking_date}")
    print(f"Sub-total: $ {apartment_sub_total:.2f} (AUD)")
    print("-"*80)
    print("Supplementary items")
    print(f"{'ID':<10}{'Name':<20}{'Qty':<10}{'Unit Price $':<15}{'Cost $':<10}")
    for (sid, name, qty, unit_price) in supplementary_items:
        print(f"{sid:<10}{name:<20}{qty:<10}{unit_price:<15.2f}{qty*unit_price:<10.2f}")

    print(f"Sub-total: $ {supp_sub_total:.2f}")
    print("-"*80)
    print(f"Total cost: $ {total_cost:.2f} (AUD)")
    print(f"Reward points to redeem: {reward_points}")
    print(f"Discount based on points: $ {discount:.2f} (AUD)")
    print(f"Final total cost: $ {final_total:.2f} (AUD)")
    print(f"Earned rewards: {earned_rewards}")
    print("Thank you for your booking!")
    print("We hope you will have an enjoyable stay.")
    print("="*80)


class User_Order:
    def __init__(self,guest_name,products,is_bundle,total_cost,reward_points,booking_format):
        ## products = {"Obj_id": "Obj_qty"}
        ## booking format =  date and time => date , time 
        self.guest_name = guest_name
        self.products =  products
        self.is_bundle =  is_bundle
        self.total_cost =  total_cost
        self.reward_points  = reward_points
        self.booking_format =  booking_format
        

class Records :
    def __init__(self):
        self.Guests =  {}
        self.guests_list =  list(self.Guests.keys())
        
        self.SupplementaryItems = {}
        self.supp_list =  list(self.SupplementaryItems.keys())
        
        self.ApartmentUnits  = {}
        self.apt_list=  list(self.ApartmentUnits.keys())
        
        self.user_orders = {}  # format : { name : User_Order } 
        self.bundles =  {}
        
        
        self.read_csv(guest_file)
        self.read_products(product_file)
        self.read_orders(order_file)
        
    
    def read_csv(self, filename):
        for g_id, g_name, g_r_rate, g_r, g_redeem_r in read_csv_file(filename,encoding="utf-8-sig"):
            guest = Guest(int(g_id), g_name, int(g_r))
            guest.set_reward_rate(float(g_r_rate))
            guest.set_redeem_rate(float(g_redeem_r))
            self.Guests[int(g_id)] = guest

    
    def read_products(self, filename):
        self.bundles.clear()

        for p in read_csv_file(filename):
            pid = p[0]

            if pid.startswith("S"):
                self.SupplementaryItems[pid] = SupplementaryItem(pid, p[1], float(p[2]))

            elif pid.startswith("U"):
                self.ApartmentUnits[pid] = ApartmentUnit(pid, p[1], float(p[2]), float(p[3]))

            elif pid.startswith("B"):
                bundle_id, name, *components, price = p
                self.bundles[bundle_id] = Bundle(bundle_id, name, components, float(price))
            else:
                pass 
        
        
        self.SupplementaryItems["SI_extra_bed"] =  SupplementaryItem("SI_extra_bed"," Extra Bed",50)
    
    def find_guest(self, id=None, name=None):
        
        if id != None:
            return self.Guests[id]
        if name !=   None:
            return self.get_guest(name)
        return None

    
    def find_product(self, id=None, name=None):
        product_found = None

        # Find by ID
        if id is not None and id in self.SupplementaryItems:
            product_found = self.SupplementaryItems[id]

        # Find by name
        elif name is not None:
            product_found = self.get_product(name)

        return product_found

        
    
    
    def list_guest(self):
        
        print("="*45)
        for id,g in self.Guests.items():
            print(f"""
Guest ID  : {id}
Name : {g.name}
Reward Points : {g.reward_points}
Redeem Rate :  {g.redeem_rate}
Reward Rate : {g.reward_rate}
                   
                  """)
            print("*"*40)
        print("="*45)
    
    
    
    def list_products(self,product_type):
        
        if product_type == "apartment":
            print("="*45)
            for apt_id,apt in self.ApartmentUnits.items():
                apt.display_info()
                print("*"*45)
            print("="*45)
        else:
            print("="*45)
            for p_id,p in self.SupplementaryItems.items():
                p.display_info()
                print("*"*45)
            print("="*45)
    
    def get_guest(self,name):
        
        
        name_obj = None
        for obj in self.Guests.values():
            if obj.name == name:
                name_obj = obj 
        return name_obj  
    
    def get_product(self,name):
        
        name_obj = None
        for obj in self.SupplementaryItems.values():
            if obj.name == name:
                name_obj = obj 
        return name_obj  
                
    
    
    def list_bundles(self):
        if not self.bundles:
            print("⚠️ No bundles found in products.csv")
            return
        
        print(f"{'ID':<10}{'Name':<45}{'Components':<40}{'Price':<10}")
        print("-"*105)
        
        for bundle in self.bundles.values():
            print(f"{bundle.id:<10}{bundle.name:<45}{bundle.display_components():<40}{bundle.price:<10.2f}")
    
    
    def display_existing_products(self):
        print("\nExisting Products:")
        print("------------------")

        # Display normal products (apartments + supplementary)
        ##self.list_products("apartment")## Not displaying apartments 
        self.list_products("supplementary")

        # Then display bundles
        self.list_bundles()
    def read_orders(self,filename):

        try : 
            order_file =  read_csv_file(filename)
        except :
            print("⚠️ Could Not load the Orders file !!")
        

        for row in order_file:
            products_dict = {}
            guest_name = row[0]
            products = row[1:-3]
            total_cost =  float(row[-3])
            earned_rewards  = int(row[-2])
            order_date = row[-1]
            for obj in products:
                qty,name =  obj.split("x")
                products_dict[name.strip()] =  int(qty.strip())
                
            self.user_orders[guest_name] =  User_Order(guest_name,products_dict,False,total_cost,earned_rewards,order_date)
            self.get_guest(guest_name).update_reward(earned_rewards)

            
    def display_orders(self):
        
        print("=" * 90)
        print(f"{'Guest Name':<15}{'Products':<35}{'Total Cost ($)':<15}{'Rewards':<10}{'Date'}")
        print("-" * 90)


        for guest_name, order in self.user_orders.items():
            
            # Build product string like "2x SI1, 1x SI2"
            product_details = ', '.join([f"{qty}x {pid}" for pid, qty in order.products.items()])

            print(f"{guest_name:<15}{product_details:<35}{order.total_cost:<15}{order.reward_points:<10}{order.booking_format}")

        print("=" * 90)   
    
    
    def generate_stats(self):
        
        final_text =  "\n===== Top 3 most valuable guests =====\n"
        most_3 =  {key:obj.total_cost for (key,obj) in self.user_orders.items() }
        most_3_guests = sorted(most_3.items(), key=lambda x: x[1],reverse=True) 
        
        for (name,amount) in most_3_guests[:3]:
            final_text +=  f"\n{name} => {amount}\n"
        
        
        p_count = {}
        for obj in self.user_orders.values():
            for name, qty in obj.products.items():
                p_count[name] =  p_count.get(name,0) +  qty
        
        most_3_supp_item =  sorted(p_count.items(),key=  lambda x :  x[1],reverse=True)
        
        final_text += "\n===== Top 3 most popular products ===== \n"
        for (name,qty) in most_3_supp_item[:3]:
            final_text += f"\n{name} =>  {qty}\n"
        
        print(final_text)
        
        with open("stats.txt","w") as f:
            f.write(final_text)
        
        print("FILE stats.txt Generated !! Please check Our Top3 Guests and  Supplementary Products stats ")
    
    def display_guest_order_history(self):
        print("\n ===== Display Guest Order History =====")
        guest_name = input("Enter guest name: ").strip()

        # Filter all orders for this guest
        guest_orders = [
            (i + 1, order)
            for i, (name, order) in enumerate(self.user_orders.items())
            if name.lower() == guest_name.lower()
        ]

        if not guest_orders:
            print(f"⚠️ No orders found for guest '{guest_name}'.")
            return

        print(f"\nBooking and Order History for {guest_name}:")
        print(f"{'Order ID':<10}{'Products Ordered':<50}{'Total Cost ($)':<20}{'Earned Rewards':<15}")
        print("-" * 95)

        for order_id, order in guest_orders:
            product_details = ', '.join([f"{qty} x {pid}" for pid, qty in order.products.items()])
            print(f"{'Order'+str(order_id):<10}{product_details:<50}{order.total_cost:<20.1f}{order.reward_points:<15}")

        print("-" * 95)


    def save_orders(self, filename="orders.csv"):
        """Save all guest orders to a CSV file in the specified format."""
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                for guest_name, order in self.user_orders.items():
                    # Convert dict like {'U12swan':2, 'SI2':4, 'SI1':2} → ["2 x U12swan", "4 x SI2", "2 x SI1"]
                    products_str = [f"{qty} x {pid}" for pid, qty in order.products.items()]
                    earned_rewards =  self.get_guest(guest_name).calculate_reward(order.total_cost)
                    row = [
                        guest_name,
                        *products_str,
                        f"{order.total_cost:.2f}",
                        earned_rewards,
                        order.booking_format,
                    ]
                    writer.writerow(row)

            print(f"✅ Orders successfully saved to '{filename}'")
        except Exception as e:
            print(f"⚠️ Error saving orders: {e}")
    def save_guests(self, filename="guests.csv"):

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            for g in self.Guests.values():
                writer.writerow([
                    g.id, g.name, g.reward_rate, g.reward_points , g.redeem_rate
                ])
        
        print("✅ GUESTS FILE UPDATED ")
    
    def save_products(self, filename="products.csv"):
        
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)

            # Supplementary items
            for s in self.SupplementaryItems.values():
                writer.writerow([s.id, s.name, s.price])

            # Apartment units
            for u in self.ApartmentUnits.values():
                writer.writerow([u.id, u.name, u.price, u.capacity])

            # Bundles
            for b in self.bundles.values():
                writer.writerow([b.id, b.name, *b.components, b.price])
        
        print("✅ Producst file saved successfully !!")



        
        
R  = Records()
Guests  = R.Guests
SupplementaryItems = R.SupplementaryItems
BundleItems =  R.bundles


# -------  Order -------------


class Order: 
    def __init__(self,guest_id,product_ids,apartment_id,quantity,is_bundle):
        
        self.guest_id =  guest_id
        self.product_ids =  product_ids
        self.quantity =  quantity
        self.apartment_id  = apartment_id
        self.total_cost = 0
        self.discount  = 0
        self.is_bundle =  is_bundle
    
    def compute_cost(self):
        
        for i in self.product_ids:
            self.total_cost +=  BundleItems[i].price if self.is_bundle else SupplementaryItems[i].get_price() * self.quantity
            
        ## if bundle it is already discounted but will get more discount as per rewards  points 
        
        user =  Guests[self.guest_id]
        self.discount =  user.get_discount()
        user.update_reward(user.calculate_reward(self.total_cost))
        self.new_price =  self.total_cost -  self.discount
        
        return (self.total_cost,self.discount, self.new_price)
    

    
class Operations:
    def __init__(self):
        pass 
    
    def add_or_update_apartment(self):
        print("\n🏢 ADD / UPDATE APARTMENT UNIT")
        print("Enter details in format: apartment_id rate capacity")
        print("Example: U12swan 250 4\n")

        data = input("Enter apartment details: ").strip().split()


        if len(data) != 3:
            print("[⚠️] Invalid format. Please enter in format: apartment_id rate capacity")
            print("Returning to main menu...\n")
            return

        apartment_id, rate_str, capacity_str = data


        if len(apartment_id) < 3 or apartment_id[0] != 'U':
            print("[⚠️] Invalid apartment ID format! It must start with 'U' (e.g., U12swan)")
            return


        unit_number = ""
        building_name = ""
        for ch in apartment_id[1:]:
            if ch.isdigit():
                unit_number += ch
            else:
                building_name += ch

        if unit_number == "" or building_name == "":
            print("[⚠️] Invalid apartment ID! It must contain both a unit number and a building name.")
            print("Example: U12swan → Unit 12 in Swan building.")
            return


        rate_status = validate_positive(rate_str,"rate")
        capacity_status  =  validate_positive(capacity_str,"capacity")
        price =  apt_rates[apartment_id[3:]]
        
        if rate_status  and capacity_status:
            rate = float(rate_str)
            capacity =  float(capacity_str)
    
            if apartment_id[3:] in R.ApartmentUnits.keys():
                print(f"[INFO] Apartment {apartment_id} already exists. Updating details...")
                apt = R.ApartmentUnits[apartment_id]
                apt.rate = rate
                apt.price =  price 
                apt.capacity = capacity
            else:
                print(f"✅ Adding new apartment unit: {apartment_id}")
                new_apt = ApartmentUnit(apartment_id, rate, price ,capacity)
                R.ApartmentUnits[apartment_id] = new_apt


            print(f"✅ Apartment saved successfully!")
            print(f"ID: {apartment_id} | Rate: ${rate} | Capacity: {capacity} beds\n")
    
    
    def adjust_reward_rate_all_guests(self):
        print("\n🎯 Adjust Reward Rate for All Guests")
        while True:
            try:
                rate_input = input("Enter new reward rate percentage (e.g., 120 for 120%): ").strip()
                rate_status  = validate_positive(rate_input,"rate")
                
                if rate_status:
                    rate =  float(rate_input)
                
                    for guest in R.Guests.values():
                        guest.set_reward_rate(rate)
                    
                    print(f"✅ Reward rate for all guests updated to {rate:.0f}%")
                    break

            except ValueError as e:
                print(f"⚠️ Invalid input: {e}. Please try again.")
    
    
    def adjust_redeem_rate_all_guests(self):
         print("\n🎯 Adjust Redeem Rate for All Guests")
         while True:
            try:
                rate_input = input("Enter new redeem rate percentage (e.g., 2 for 2%): ").strip()
                rate = float(rate_input)
                if rate < 1:
                    raise ValueError("Redeem rate too low. Must be at least 1%.")
                
                for guest in R.Guests.values():
                    guest.set_redeem_rate(rate)
                
                print(f"✅ Redeem rate for all guests updated to {rate:.0f}%")
                break

            except ValueError as e:
                print(f"⚠️ Invalid input: {e}. Please try again.")
                
    def add_or_update_bundle(self):
        print("\n[🛠️] Add/Update Bundle Product")
        print("Enter details in format: bundle_id name component_ids (space-separated) price")
        print("Example: B1 WeekendPack SI1 SI2 U12swan 200\n")

        user_input = input("Enter bundle details: ").strip().split()
        
        if len(user_input) < 3:
            print("⚠️ Invalid input. At least bundle_id, name, one component, and price are required.")
            return

        bundle_id = user_input[0]
        bundle_name = user_input[1]
        price_str = user_input[-1]
        components = user_input[2:-1]  # all IDs between name and price

        if not bundle_id.startswith("B"):
            print("⚠️ Invalid bundle ID. It must start with 'B'.")
            return

        # Validate components
        invalid_components = [c for c in components if c not in R.SupplementaryItems.keys() and c not in R.ApartmentUnits.keys()]
        if invalid_components:
            print(f"⚠️ Invalid component IDs: {', '.join(invalid_components)}")
            return

        price_status = validate_positive(price_str,"price")
        
        if price_status:
            price=  float(price_str)

            # Update or add
            if bundle_id in R.bundles.keys():
                R.bundles[bundle_id].name = bundle_name
                R.bundles[bundle_id].components = components
                R.bundles[bundle_id].price = price
                print(f"✅ Bundle {bundle_id} updated successfully.")
            else:
                R.bundles[bundle_id] = Bundle(bundle_id, bundle_name, components, price)
                print(f"✅ Bundle {bundle_id} added successfully.")

    
    
    
    def add_or_update_supplementary_item(self):
        print("\n[🛠️] Add/Update Supplementary Item")
        user_input = input("Enter item_id name and price (e.g., SI4 toothpaste 5.2): ").strip()
        
        # Split allowing multiple whitespaces
        parts = user_input.split()
        
        if len(parts) != 3:
            print("⚠️ Incorrect format! Please use: item_id price")
            return 

        item_id,item_name , price_str = parts 
        price_status =  validate_positive(price_str,"price")
        # If already exists => update; else => add new
        if price_status : 
            price =  float(price_str)
            
            if item_id in R.SupplementaryItems.keys():
                R.SupplementaryItems[item_id].price = price
                print(f"Updated {item_id} with new price: ${price:.2f}")
            else:
                R.SupplementaryItems[item_id] = SupplementaryItem(item_id,item_name,  price)
                print(f"✅ Added new supplementary item: {item_id} (${price:.2f})")



        
        
    def make_booking(self):
        
        
        
        ## validating guest name until it contains only alpha chars 
        while True : 
            
            guest_name = input("Enter guest name: ")
            if guest_name.isalpha() == True:
                self.guest_name= guest_name
                break
            else:
                print("[INFO] Please enter the valid Guest name , it contains non-alpha chars !!")
            
        
        self.num_guests = int(input("Enter number of guests: ") or 4)
        
        
        while True : 
        
            apartment_id = input("Enter apartment ID: ")
              
            if apartment_id[3:] in apt_rates.keys():
                self.apartment_id =  apartment_id
                print(f"[AUTO] The selected Unit rate is ${apt_rates[apartment_id[3:]]}")
                price =  apt_rates[self.apartment_id[3:]]
                break     
                
            else:
                print("[INFO] please enter valid apartment ID , we have 1.swan 2. duck  3. goose")

        # default capacity is already set 
        R.ApartmentUnits[self.apartment_id] = ApartmentUnit(self.apartment_id,f"{self.apartment_id} Building ",price)
        apt_capacity =  R.ApartmentUnits[self.apartment_id].capacity 
        print("Apartment capacity : ",apt_capacity)
        

        
        while True :
            
            check_in = datetime.strptime(input("Enter check-in date (YYYY-MM-DD, default 2025-10-14): ") or "2025-10-17", "%Y-%m-%d")
            check_out = datetime.strptime(input("Enter check-out date (YYYY-MM-DD, default 2025-10-17): ") or "2025-10-19", "%Y-%m-%d")
            booking_date = datetime.now()
            if check_in < booking_date:
                print("[INFO] Check-in date cannot be earlier than booking date ")
            elif check_out < booking_date:
                print("[INFO] Check-out date cannot be earlier than booking date.")
            elif check_out < check_in:
                print("[INFO] Check-out date cannot be earlier than check-in date.")
            elif check_out == check_in:
                print("[INFO] Check-in and check-out dates cannot be the same.")
            else:
                self.check_in = check_in
                self.check_out = check_out
                self.booking_date =  booking_date
                break 
            
            
        while True : 
            ## validating supplementary id 
            supplementary_item_id = input("Enter supplementary item ID or Bundle ID: ")
            if supplementary_item_id  in SupplementaryItems.keys():
                self.supplementary_item_id = supplementary_item_id 
                self.is_bundle=  False
                break
            elif supplementary_item_id in BundleItems.keys():
                self.supplementary_item_id =  supplementary_item_id
                self.is_bundle = True 
                break 
        
            else:
                print("[INFO] You entered incorrect supplementary Item ")
    
        self.supplementary_item_qty =  1 if self.is_bundle ==  True else  int(input("Enter supplementary item quantity: ") or 4 ) 
        user_exist =  R.find_guest(name=self.guest_name)
    
    
        if self.num_guests > apt_capacity:
            print("⚠️ The number of guests exceeds apartment capacity!")
            print("Please consider ordering an extra bed.")
            
            # Calculate how many extra beds are needed
            extra_people = self.num_guests - apt_capacity
            required_beds = (extra_people + 1) // 2  # Each bed for 2 extra people

            if required_beds > 2:
                print("Booking cannot proceed. Even with 2 extra beds, capacity exceeded.")
                print("Returning to main menu...")
                return

            print(f"[INFO] You need at least {required_beds} extra bed(s).")

            # Ask user how many beds they want (cannot exceed 2)
            while True:
                try:
                    extra_bed_input = int(input("Enter number of extra beds you want to order (0–2): "))
                    if extra_bed_input < required_beds:
                        print(f"⚠️ You must order at least {required_beds} bed(s) to fit all guests.")
                    elif extra_bed_input > 2:
                        print("⚠️ You cannot order more than 2 extra beds.")
                    else:
                        break
                except ValueError:
                    print("⚠️ Invalid input. Please enter a number between 0 and 2.")

            # Recalculate total capacity with ordered beds
            total_capacity = apt_capacity + (extra_bed_input * 2)
            if self.num_guests > total_capacity:
                print(f" Even with {extra_bed_input} extra bed(s), total capacity ({total_capacity}) is insufficient.")
                print("Booking cannot proceed. Returning to main menu...")
                return

            # Ensure quantity ordered ≥ nights
            nights = (self.check_out - self.check_in).days
            extra_bed_qty = max(extra_bed_input, nights)

            if "SI_extra_bed" in SupplementaryItems:
                extra_bed_item = SupplementaryItems["SI_extra_bed"]
                extra_bed_price = extra_bed_item.get_price()
                
                # Calculate cost for the number of nights
                extra_bed_cost = extra_bed_price * extra_bed_qty * nights
                
                print(f"✅ {extra_bed_input} extra bed(s) added for {nights} night(s).")
                print(f"Extra bed cost: ${extra_bed_cost:.2f}\n")

            else:
                print("⚠️ Extra Bed item not found in supplementary products list!")
                return
        else:
            extra_bed_cost = 0
            
        
        # --- Car Park Validation ---
        car_park_item = SupplementaryItems["SI1"]
        car_park_price = car_park_item.get_price()

        print("\nOptional: Car Park booking available.")
        want_parking = input("Would you like to book car park(s)? (Y/N): ").strip().lower()

        if want_parking == 'y':  
            car_park_qty =  input_positive_int("Enter number of car parks required: ","Car quantity",0)

            if car_park_qty < nights:
                print(f"⚠️ You must book at least {nights} car park(s) (same as number of nights).")
                car_park_qty = nights
                print(f"✅ Automatically adjusted to {car_park_qty} car park(s).")

            car_park_cost = car_park_price * car_park_qty

            
            print(f"✅ Car Park added for {nights} night(s). Total: ${car_park_cost:.2f}\n")
        else:
            print("XX No car park added. XX")
            car_park_cost = 0
        
        
        
        
        ## Evaluating all 
        ## supp_items_order for 'User_order' class 
        ## supp_item_tuple_  for 'generating receipt' 
        
        supp_items_order = {
            self.apartment_id:1, # A user can only take 1 apartment 
            self.supplementary_item_id:  self.supplementary_item_qty
        }
        
        apt_rate_ =  apt_rates[self.apartment_id[3:]]
        apt_sub_total =  apt_rate_ * nights
        
        supp_item_ =  BundleItems[self.supplementary_item_id] if self.is_bundle else SupplementaryItems[self.supplementary_item_id]
        supp_item_tuple_ = [(self.supplementary_item_id,supp_item_.name,self.supplementary_item_qty,supp_item_.price )]
            
                    
        if extra_bed_cost != 0:
            supp_item_tuple_.append(("SI_extra_bed", " Extra Bed", extra_bed_input * nights, extra_bed_price))
            supp_items_order["SI_extra_bed"] =  extra_bed_input * nights

        
        if car_park_cost != 0:
            supp_item_tuple_.append(("SI1", "Car Park", car_park_qty, car_park_price))
            if "SI1" in supp_items_order.keys():
                supp_items_order["SI1"] += car_park_qty
            else:
                supp_items_order["SI1"] = car_park_qty
                
        ## STORING ACCORDING TO USER EXIST OR NOT 
                    
        if user_exist== None :
            g_id =  str(len(R.Guests) +  1)
            R.Guests[g_id] =  Guest(g_id,self.guest_name,self.num_guests*30)
            
            
            total_cost, discount, new_price =  Order(g_id,[self.supplementary_item_id],self.apartment_id,self.supplementary_item_qty,self.is_bundle).compute_cost()
            total_cost += extra_bed_cost
            total_cost += car_park_cost
            
            earned =  R.Guests[g_id].calculate_reward(apt_rate_ + total_cost)
            R.Guests[g_id].update_reward(earned)
   
            r_points =  Guests[g_id].reward_points 

            R.user_orders[self.guest_name]   = User_Order(
                self.guest_name,
                supp_items_order,
                is_bundle=self.is_bundle,
                total_cost=total_cost +  apt_rate_,
                reward_points=r_points,
                booking_format=self.booking_date  
            )
            
            print(f"User registered succesfully with ID  : {g_id} || Name : {self.guest_name} || apartment ID : {self.apartment_id}")
            
            
            generate_receipt(
                guest_name=self.guest_name,number_of_guests=self.num_guests,
                apartment_name=self.apartment_id[3:],apartment_rate=apt_rate_,
                checkin_date=self.check_in,checkout_date=self.check_out,
                nights=nights,supplementary_items=supp_item_tuple_,
                booking_date=self.booking_date,apartment_sub_total=apt_sub_total,
                supp_sub_total=total_cost,total_cost=total_cost +  apt_sub_total,
                reward_points=r_points,discount=discount,
                final_total= new_price +  apt_sub_total,earned_rewards=earned
            )
            
            
        else:
            
            #  IF THE USER ALREADY EXIST
            r_points =  R.get_guest(self.guest_name).reward_points
            print(f"Hi {self.guest_name} Welcome Back again !")
            print("YOUR CURRENT REWARD POINTS: ", r_points )
             
            total_cost, discount, new_price =  Order(user_exist.id,[self.supplementary_item_id],self.apartment_id,self.supplementary_item_qty,self.is_bundle).compute_cost()
            total_cost += extra_bed_cost
            total_cost += car_park_cost

            earned = user_exist.calculate_reward(apt_rate_ + total_cost)
            user_exist.update_reward(earned)
            
            generate_receipt(
                guest_name=user_exist.name,number_of_guests=self.num_guests,apartment_name=self.apartment_id[3:],
                apartment_rate=apt_rate_,checkin_date=self.check_in,checkout_date=self.check_out,
                nights=nights ,booking_date=self.booking_date,apartment_sub_total=apt_sub_total,
                supplementary_items=supp_item_tuple_,supp_sub_total=total_cost,final_total=new_price,
                reward_points=r_points,discount=discount,total_cost=apt_rate_+total_cost,earned_rewards=earned 
            )
            
            R.user_orders[self.guest_name]   = User_Order(
                self.guest_name,
                supp_items_order,
                is_bundle=self.is_bundle,
                total_cost=total_cost +  apt_rate_,
                reward_points=user_exist.reward_points,
                booking_format=self.booking_date  
            )
            
            
            
    def display_menu(self):
        
        
        menu_items = [
            "Make a booking",
            "Display existing guests",
            "Display existing apartment units",
            "Display existing supplementary items",
            "Display existing products",
            "Add/update information of apartment units",
            "Add/update information of a supplementary item",
            "Add/update information of bundles",
            "Adjust the reward rate of all guests",
            "Adjust the redeem rate of all guests",
            "Display all orders",
            "Generate key statistics",
            "Display a guest order history",
            "Exit"
        ]
                    
                    
        while True:
            print("🏨 Hotel Management System 🏨")
            print("="*40)
            for i, item in enumerate(menu_items, 1):
                print(f"{i}. {item}")
            print("="*40)


            choice = input("Enter your choice (1-11): ").strip()
            
            
            # format {"choice_number" : [function name , function parameters ]}
            
            choice_fnx ={"1":[self.make_booking,None],
                         "2" :[R.list_guest,None],
                         "3": [R.list_products,"apartment"],
                         "4" :[R.list_products,"supplementary"],
                         "5" : [R.display_existing_products,None],
                         "6" :  [self.add_or_update_apartment,None],     
                         "7" : [self.add_or_update_supplementary_item,None]   ,
                         "8" :[self.add_or_update_bundle,None]   ,
                         "9" :  [self.adjust_reward_rate_all_guests,None] ,   
                         "10" :  [self.adjust_redeem_rate_all_guests,None],
                         "11" :[R.display_orders,None],
                         "12":  [R.generate_stats,None],
                         "13": [R.display_guest_order_history,None]
                        
                         }
            
            for choice_id,_  in choice_fnx.items():
                if choice == choice_id:
                    fx =  choice_fnx[choice_id][0]
                    param =  choice_fnx[choice_id][1]
                    if param != None:
                        fx(param)
                    else:
                        fx()
                elif choice == str(len(choice_fnx) +  1):
                    R.save_guests(guest_file)
                    R.save_orders(order_file)
                    R.save_products(product_file)
                    print("Exiting program. Thank you!")
                    sys.exit() 
            if choice not in  choice_fnx.keys():
                print("⚠️ Invalid choice. Please try again.")
                    
                    

    
    
    

    

if __name__ == "__main__":
    Operations().display_menu()

            



