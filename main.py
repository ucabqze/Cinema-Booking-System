#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 21:47:14 2018

@author: cengqiqi
"""

# '/Users/cengqiqi/Desktop/qiqizeng'

import os 
import employee
import customer


def display_text():
    """ display the welcome text. """
    os.system('clear')
    
    print("\t*****************************************")
    print("\t***  Welcome to Cinema Booking System ***")
    print("\t*****************************************")
    print(" ")
    print("[1] cinema employee")
    print("[2] ordinary customers")
    print("[3] exit the system")
    
    
def main_menu():
    """Display the choice for users. """
    display_text()
    exit = False
    
    while not exit:
        role = input("Please type the index of system that you want to enter: ")
    
        if role == "1":
            employee.menu_for_employee()
        elif role == "2":
            customer.menu_for_customer()
        elif role == "3":
            exit = True
        else:
            print("Your input is not in the avaliable options, please try again")
                
        if role != "3":
            input("Please press 'return' button to continue ... ... ")
            display_text()

def main():
    main_menu()


if __name__ == '__main__': main()