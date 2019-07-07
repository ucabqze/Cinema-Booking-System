#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 17:11:09 2018

@author: cengqiqi
"""

# '/Users/cengqiqi/Desktop/qiqizeng'

import os 
import pickle
import datetime
import csv
from collections import Counter
from itertools import chain


def display_text():
    """ display the welcome text. """
    os.system('clear')
    
    print("\t******************************************")
    print("\t***  Welcome to Cinema Employee System ***")
    print("\t******************************************")
    print(" ")
    print("[1] Register")
    print("[2] Login")
    print("[3] add films ")
    print("[4] see the cinema room setting and the number of available seats")
    print("[5] export a list of films as csv file")
    print("[6] Logout")  
    print("[7] Exit the employee system and return to the main menu")


def menu_for_employee():
    """Display the choice for employees. """
    display_text()
    log_status = False
    exit = False
    
    while not exit:
        act = input(">>>Please enter what would you like to do: ")
        
        # login and logout
        if act == "1":
            register()
        elif act == "2":
            login = True
            logout = False 
            log_status = change_login_status(login,logout)
        elif act == "3":
            if not log_status:
                 print(">>>You have not logged in, please login firstly. ")
            else:
                add_films()
        elif act == "4":
            if not log_status:
                 print(">>>You have not logged in, please login firstly. ")
            else:
                show_room_setting()
        elif act == "5":
            if not log_status:
                 print(">>>You have not logged in, please login firstly. ")
            else:
                displat_list_of_film()
        elif act == "6":
            logout = True
            login = False
            log_status = change_login_status(login,logout)
        elif act == "7":
            exit = True
        else:
            print("Your input is not in the avaliable options, please try again")
        
        if act != "7":
            input("Please press 'return' button to continue ... ... ")
            display_text()


def register():
    """This function is designed to record new employees. """
    
    register_successful = False
    
    while not register_successful:
        username = input("Please enter your username to sign up: ")
        password = input("Please enter your password to sign up: ")
        password_ensure = input("Please enter your password again: ")
    
        # read information from existing list
        try:
            pickle_r = open("employee.pickle","rb")
        except Exception:
            dic_employee = {}
        else:
            dic_employee = pickle.load(pickle_r)
    
    
        if username not in dic_employee.keys():   # not existing empoyee
            if password_ensure == password:   # the passwords match
                dic_employee.update({username: password})
        
                # write new employee list 
                try:
                    pickle_w = open("employee.pickle", "wb")
                    pickle.dump(dic_employee, pickle_w)
                    pickle_w.close()
                    print("\nThanks for registering. I will remember these employees.")
                    register_successful = True
                except Exception as e:
                    print("\nThanks for playing. I won't be able to remember these names.")
                    print(e)
            else:
                print("The password does not match, please try again")
        else:
            print("\nEmployee already exist. ")
            exit_ =  input("If you want to exist register process, "
                           "please enter 'Y' for exit, "
                           "otherwise enter 'N' to register again: ")
            if exit_ == "Y":
                register_successful = True
    
    
def login():
    """This function is designed for logining. """
    
    username = input("Please enter your username to login: ")
    password = input("Please enter your password to login: ")
    
    try:
        pickle_r = open("employee.pickle","rb")
    except Exception:
        print("Cannot read information from data base, you can try  register firstly. ")
        dic_employee = []
        return False
    else:
        dic_employee = pickle.load(pickle_r)
    
        if username in dic_employee.keys():
            if password == dic_employee[username]:
                print("\nYou have successfully logged in. ")
                return True
            else:
                print("\nThe password does not correct. ")
                return False
        else:
            print("\nThis employee does not exist. ")
            return False


def change_login_status(login_,logout):
    """ This function control login and logout. """ 
    
    if logout:
        status = False
        print("Your current status: logged out")
    elif login_:
        if login():
            status = True
            print("Your current status: logged in")
        else:
            status = False
            print("Your current status: logged out")
        
    return status
        
  
def check_time_overlap(time_a,time_b):
    """ This function checks if the time_a is overlapping with time_b. """
    # a film lasts exactly one hour.
    start_a = time_a
    end_a = time_a + datetime.timedelta(hours=1)
    start_b = time_b
    end_b = time_b + datetime.timedelta(hours=1)
    
    if start_a < end_b and end_a > start_b:
        return True
    else:
        return False
    
     
def add_films():
    """This fuction allowa employees to add films with their respective dates and screening times."""
    # get user input
    title = input("Please enter the NAME of the film: ")
    description = input("Please enter a brief DESCRIPTION of the film: ")
           
    date_time_successful = False
    while not date_time_successful: 
        date_input = input("Please enter a date in DD-MM-YYYY format: ")
        time_input = input("Please enter the starting time in HH:MM format: ")
        try:
            day, month, year = map(int, date_input.split("-"))
            hour, minute = map(int, time_input.split(":"))
            screening_date_time = datetime.datetime(year, month, day, hour, minute)
        except:
            print("Date format should be DD-MM-YYYY, and the time should "
                  "be HH:MM format. ")
        else:
            date_time_successful = True
   
    # seat setting
    seat = [[" "," "," "," "," "," "," "," "],
             [" "," "," "," "," "," "," "," "],
             [" "," "," "," "," "," "," "," "],
             [" "," "," "," "," "," "," "," "],
             [" "," "," "," "," "," "," "," "],
             [" "," "," "," "," "," "," "," "],
             [" "," "," "," "," "," "," "," "],
             [" "," "," "," "," "," "," "," "]]
    # get information of existing film
    try:
        pickle_r = open("filmtime.pickle","rb")
    except Exception:
        dic_film = []
    else:
        dic_film = pickle.load(pickle_r)
    
    # check if the new screening time overlap with existing ones
    check_overlap = False
    for exist_film in dic_film:
        if check_time_overlap(exist_film[2],screening_date_time):
            check_overlap = True
          
    if not check_overlap and screening_date_time >= datetime.datetime.now():
        # write new films and time 
        try:
            dic_film.append([title, description, screening_date_time,seat])
            pickle_w = open("filmtime.pickle", "wb")
            pickle.dump(dic_film, pickle_w)
            pickle_w.close()
            print("\nThanks. The new film has been added. ")
        except Exception as e:
            print("\nSorry. I won't be able to add this film.")
            print(e)  
    elif screening_date_time < datetime.datetime.now():
        print("Sorry. The screening time is a past time. "
              "Please choose a future time. ")
    else:
        print("Sorry. The screening time is overlapping with existing films, "
              "I won't be able to add this film. ")


def print_seat(seat):
    """ This function visualize the cinema room setting. """
    print(" ")
    print("**********************************************************")
    print("The cinema room setting for this film show is showed below: ")
    
    print("--+---+---+---+---+---+---+---+---+")
    print("h","|",seat[7][0],"|",seat[7][1],"|",seat[7][2],"|",seat[7][3],"|",
              seat[7][4],"|",seat[7][5],"|",seat[7][6],"|",seat[7][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print("g","|",seat[6][0],"|",seat[6][1],"|",seat[6][2],"|",seat[6][3],"|",
              seat[6][4],"|",seat[6][5],"|",seat[6][6],"|",seat[6][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print("f","|",seat[5][0],"|",seat[5][1],"|",seat[5][2],"|",seat[5][3],"|",
              seat[5][4],"|",seat[5][5],"|",seat[5][6],"|",seat[5][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print("e","|",seat[4][0],"|",seat[4][1],"|",seat[4][2],"|",seat[4][3],"|",
              seat[4][4],"|",seat[4][5],"|",seat[4][6],"|",seat[4][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print("d","|",seat[3][0],"|",seat[3][1],"|",seat[3][2],"|",seat[3][3],"|",
              seat[3][4],"|",seat[3][5],"|",seat[3][6],"|",seat[3][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print("c","|",seat[2][0],"|",seat[2][1],"|",seat[2][2],"|",seat[2][3],"|",
              seat[2][4],"|",seat[2][5],"|",seat[2][6],"|",seat[2][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print("b","|",seat[1][0],"|",seat[1][1],"|",seat[1][2],"|",seat[1][3],"|",
              seat[1][4],"|",seat[1][5],"|",seat[1][6],"|",seat[1][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print("a","|",seat[0][0],"|",seat[0][1],"|",seat[0][2],"|",seat[0][3],"|",
              seat[0][4],"|",seat[0][5],"|",seat[0][6],"|",seat[0][7],"|")
    print("--+---+---+---+---+---+---+---+---+")
    print(" ","|","1","|","2","|","3","|","4","|",
              "5","|","6","|","7","|","8","|")

def custom_sort(t):
    return t[2]


def show_room_setting():
    """This function can shows textual representation of the cinema room setting. """
    print("The avaliable movie show are showed below: ")

    # read information
    try:
        pickle_r = open("filmtime.pickle","rb")
    except Exception:
        print("Cannot read the infomation from database. There may be no film added yet.")
        dic_film = []
    else:
        dic_film = pickle.load(pickle_r)
        #sort the list according to time
        dic_film = sorted(dic_film,key = custom_sort)
    
        for (i, item) in enumerate(dic_film, start=0):
            print(f"[{i}] '{item[0]}': {item[2]}")
        
        check_choice = False
        while not check_choice:
            try:
                ind = input("Please choose the index to see the respective "
                      "textual representation of the cinema room setting: ")
                ind = int(ind)
                print_seat(dic_film[ind][3])
            except Exception:
                print("Your input is not recognised, please enter the avaliable index")
            else:
                # count avaliable seat
                merge_seat = list(chain(*dic_film[ind][3]))   # merge seat list into one list
                count = Counter(merge_seat)
                avaliable_seat = count[" "]
                booked_seat = count["X"]
                
                print(" ")
                print("------------------------")
                print(f"total number of seat: {avaliable_seat+booked_seat}")
                print(f"Avaliable: {avaliable_seat}")
                print(f"Booked: {booked_seat}")
                
                check_choice = True


def displat_list_of_film():
    """This function can export a list of films. """
    # read infomation
    try:
        pickle_r = open("filmtime.pickle","rb")
    except Exception:
        print("Cannot read the infomation from database. There may be no film added yet.")
        dic_film = []
    else:
        dic_film = pickle.load(pickle_r)
        #sort the list according to time
        dic_film = sorted(dic_film,key = custom_sort)
        
        csv_file = open('export_film.csv','w',newline = '')
        csv_r = csv.writer(csv_file)
        csv_r.writerows([('title','date and time', 'avaliable seat', 'booked seat')])
        
            
        for (i, item) in enumerate(dic_film, start=0):
            merge_seat = list(chain(*dic_film[i][3]))   # merge seat list into one list
            count = Counter(merge_seat)
            avaliable_seat = count[" "]
            booked_seat = count["X"]
            print(f"'{item[0]}', {item[2]}, avaliable seat: {avaliable_seat}, "
                  f"booked seat: {booked_seat}")
            csv_r.writerows([(str(item[0]),str(item[2]), str(avaliable_seat), str(booked_seat))])
            
        print("The information list has been export to csv file.")
        
   
def main():
    menu_for_employee()


if __name__ == '__main__': main()