import random



def generate_random_number(min =0, max_number = 1):
    r = random.randint(min,max_number)
    return r 


print(generate_random_number(0,1))