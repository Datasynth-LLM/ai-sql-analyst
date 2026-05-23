#main.py contains the main method
from car_rental import *

def __main__():
    Options = ['1-list Of Available cars', '2-Rental Modes', '3-Returning Vehicle', 'Exit']
    
#To display the menu choice to customer
    print('\t\tWelcome to car Rentals')
    print('\t\t=======================')
    #print(*options, sep='\n')
    
#Defining objects to classes in car _rental.py
    rent = renting()
    custum =customer()
    
#invoking/calling respective methods inside those classes bases on User input
while True:
    print('\n', *Options,sep="\n")
    user_input = int(input("\nPlease Enter your choice(or 0 to exit): "))
    if user_input !=0:
        if user_input == 1:
            rent.cars_display()
        elif user_input == 2:
            rent.sale_module()
        elif user_input == 3:
            custum.vehicle_return()
        else:
            print("Please enter the valid option!")
    
    else:
        break
        
_main_()        
        
    
    
    