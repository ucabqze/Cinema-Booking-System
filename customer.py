#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 22:17:12 2018

@author: cengqiqi
"""
# '/Users/cengqiqi/Desktop/qiqizeng'


import os
import pickle
import datetime

def display_text():
    """ display the welcome text. """
    os.system('clear')
    
    print("\t******************************************")
    print("\t***  Welcome to Cinema Customer System ***")
    print("\t******************************************")
    print(" ")
    print("[1] Register")
    print("[2] Login")
    print("[3] check current profile and update personal profile")
    print("[4] pick up a date and get a list of films available on the selected date")
    print("[5] book a seat")
    print("[6] delete future booking")
    print("[7] Logout")  
    print("[8] Exit the customer system and return to the main manu")


def menu_for_customer():
    """Display the choice for customers. """
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
            temp = change_login_status(login,logout)
            log_status = temp[0]
            current_username = temp[1]
        elif act == "3":
            if not log_status:
                 print(">>>You have not logged in, please login firstly. ")
            else:
                change_username = update_profile(current_username)
                if change_username:
                    logout = True
                    login = False
                    log_status = False
                    print(">>>You have been logged out, please login again with new name.")
        elif act == "4":
            if not log_status:
                 print(">>>You have not logged in, please login firstly. ")
            else:
                get_day_list()
        elif act == "5":
            if not log_status:
                 print(">>>You have not logged in, please login firstly. ")
            else:
                book_seat(current_username)
        elif act == "6":
            if not log_status:
                 print(">>>You have not logged in, please login firstly. ")
            else:
                delete_future_booking(current_username)
        elif act == "7":
            logout = True
            login = False
            log_status = False
        elif act == "8":
            exit = True
        else:
            print("Your input is not in the avaliable options, please try again")
        
        if act != "8":
            input("Please press 'return' button to continue ... ... ")
            display_text()
            
            
def register():
    """This function is designed to record new customers. """
    register_successful = False
    
    while not register_successful:
        username = input("Please enter your username to sign up: ")
        password = input("Please enter your password to sign up: ")
        password_ensure = input("Please enter your password again: ")
        email = input("please enter your email address: ")
        booking_history = []
        
        try:
            pickle_r = open("customer.pickle","rb")
        except Exception:
            pickle_w = open("customer.pickle", "wb")
            pickle_w.close()
            dic_customer = {}
        else:
            dic_customer = pickle.load(pickle_r)
            
        if username not in dic_customer.keys():   # not existing customer
           if password_ensure == password:   # the passwords match
               dic_customer.update({username: [password,email,booking_history]})
    
               # write new customer list 
               try:
                   pickle_w = open("customer.pickle", "wb")
                   pickle.dump(dic_customer, pickle_w)
                   pickle_w.close()
                   print("\nThanks for registering. I will remember these customers.")
                   register_successful = True
               except Exception as e:
                   print("\nThanks for playing. I won't be able to remember these names.")
                   print(e)
           else:
               print("The password does not match, please try again")
        else:
            print("\nCustomer already exist. ")
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
        pickle_r = open("customer.pickle","rb")
    except Exception:
        print("Cannot read information from data base. Please try register firstly")
        dic_customer = []
        return [False,username]
    else:
        dic_customer = pickle.load(pickle_r)
        
        if username in dic_customer.keys():
            if password == dic_customer[username][0]:
                print("\nYou have successfully logged in. ")    
                return [True,username]
            else:
                print("\nThe password does not correct. ")
                return [False,username]
        else:
            print("\nThis customer does not exist. ")
            return [False, username]
    

def change_login_status(login_,logout):
    """ This function control login and logout. """ 
    
    if logout:
        status = False
        print("Your current status: logged out")
    elif login_:
        login_return = login()
        login_status = login_return[0]
        login_username = login_return[1]
        if login_status:
            status = True
            print("Your current status: logged in")
        else:
            status = False
            print("Your current status: logged out")
        
    return [status, login_username]
   

def update_profile(current_username):
    """ This function allows users to update their personal information. """
    #read customer information from database
    try:
        pickle_r = open("customer.pickle","rb")
    except Exception:
        print("Cannot read information from data base")
        dic_customer = []
    else:
        dic_customer = pickle.load(pickle_r)
        
    print("[1] check current information")    
    print("[2] update password")
    print("[3] update email")
    print("[4] update username")
    
    idx = input("Please enter the index of activity: ")
    
    is_update = False
    change_username =  False
    
    if idx == "1":
        print("---------------------------")
        print(f"Hello, {current_username}, your current detail is showed below: ")
        print(f"password: {dic_customer[current_username][0]}")
        print(f"email: {dic_customer[current_username][1]}")
        print(f"booking history: ")
        if not dic_customer[current_username][2]:
            print("no booking yet")
        for bh in dic_customer[current_username][2]:
            print(f"{bh[0]} '{bh[1]}' seat: {bh[2]}")
            
    elif idx == "2":
        update_pw_successful = False
        while not update_pw_successful:
            pw = input("please enter your new password: ")
            pw_ensure = input("please enter your new password again: ")
            if pw == pw_ensure:
                dic_customer[current_username][0] = pw
                update_pw_successful = True
                is_update = True
            else:
                print("Your passwords do not match, please try again")
    elif idx == "3":
         dic_customer[current_username][1] = input("please enter the new email: ")
         is_update = True
    elif idx == "4":
        new_name = input("please enter the new username: ")
        if new_name not in dic_customer.keys(): 
            dic_customer[new_name] = dic_customer.pop(current_username)
            try:
                pickle_w = open("customer.pickle", "wb")
                pickle.dump(dic_customer, pickle_w)
                pickle_w.close()
                print("\nThanks for updating. I will remember the new information.")
            except Exception as e:
                print("\nThanks for updating. I won't be able to update these information.")
                print(e)
            else:
                change_username = True
        else:
            print("The username has been used, I cannot change it for you.")
    else:
        print("Your input is not in the avaliable options, please try again")
    
    
    # write new customer list 
    if is_update:
        try:
            pickle_w = open("customer.pickle", "wb")
            pickle.dump(dic_customer, pickle_w)
            pickle_w.close()
            print("\nThanks for updating. I will remember the new information.")
        except Exception as e:
            print("\nThanks for updating. I won't be able to update these information.")
            print(e)
        
    return change_username # if idx = 4, user need to login again

def custom_sort(t):
    return t[2]


def get_day_list():
    """ This function produce a list of films which are available on the selected date """
    
    # read infomation
    try:
        pickle_r = open("filmtime.pickle","rb")
    except Exception:
        print("Cannot read the infomation from database. There may be no movie added yet")
        dic_film = []
        date_selected = None
        return [dic_film,date_selected]
    else:
        dic_film = pickle.load(pickle_r)
        #sort the list according to time
        dic_film = sorted(dic_film,key = custom_sort)
        
        # get avaliable date
        avaliable_date=[]
        for i in dic_film:
            avaliable_date.append(i[2].date())
            
        avaliable_date = sorted(set(avaliable_date))
        for (i, item) in enumerate(avaliable_date, start=0):
            print(f"[{i}] '{item}'")
        
        date_choose_successful = False
        while not date_choose_successful:
            try:
                idx = input("Please choose a date: ")
                idx = int(idx)
                date_selected = avaliable_date[idx]
            except Exception:
                print("Your input is not recognised, please enter the avaliable index")
            else:       
                date_choose_successful = True
                
                print(f"The movie show avaliable on {date_selected} is showed below: ")
                for (movie_idx, movie_show) in enumerate(dic_film, start=0):
                    if movie_show[2].date() == date_selected:
                        print(f"[{movie_idx}] {movie_show[2]} '{movie_show[0]}': "
                              f"{movie_show[1]}")
        return [dic_film,date_selected]
       
                 
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
    

def book_seat(current_username):
    """ This function allow users to book a seat on a given date """
    tmp = get_day_list()
    dic_film = tmp[0]
    date_selected = tmp[1]
    
    if date_selected is not None: # in case the is no 'filmtime.pickle' yet
      
        # Choose a movie show
        movie_choose_successful = False
        future_book = False
        while not movie_choose_successful:
            try:    
                movie_selected = input("Please choose the movie show that you want to book: ")
                movie_selected = int(movie_selected)
                test_tmp = dic_film[movie_selected][3]
            except Exception:
                print("Sorry, please choose a valid movie show. ")
            else:
                if dic_film[movie_selected][2].date() != date_selected:
                    print(f">>>WARNING: The movie show you chose is NOT on {date_selected}")
                    print("Please try again")
                elif dic_film[movie_selected][2] < datetime.datetime.now():
                    print(f">>>The date you choose has been past, please choose a futrue date. ")
                    movie_choose_successful = True
                    future_book = False
                else:
                    print(f"{dic_film[movie_selected][2]} '{dic_film[movie_selected][0]}': "
                          f"{dic_film[movie_selected][1]}")
                    print_seat(dic_film[movie_selected][3])
                    movie_choose_successful = True
                    future_book = True
        
        # Choose a seat
        if future_book:    # avoid book a past movie show
            seat_choose_successful = False
            while not seat_choose_successful:
                try:
                    seat_selected = input("Please select yout seat in a "
                                          "character+number format (eg: a3): ")
                    #seat_selected = 'a3'
                    if len(seat_selected) == 2 and seat_selected[1] != "0":
                        x = ord(seat_selected[0])-97
                        y = int(seat_selected[1])-1
                    test_tmp = dic_film[movie_selected][3][x][y]
                except Exception:
                    print("Your input is not recognised, please enter the avaliable index")
                else:       
                    seat_choose_successful = True
                    
       
            # check if seat is avaliable
            if dic_film[movie_selected][3][x][y] == "X" :
                print("Sorry, this seat has been selected, I cannot book it for you. ")  
            else:
                dic_film[movie_selected][3][x][y] = "X"
                # write new seat information to database 
                try:
                    pickle_w = open("filmtime.pickle", "wb")
                    pickle.dump(dic_film, pickle_w)
                    pickle_w.close()
                except Exception as e:
                    print("\nSorry. I won't be able to add this film.")
                    print(e) 
                else:
                    print_seat(dic_film[movie_selected][3])
                    print("Thanks for booking. You have successfully booked a seat. ") 
            
                # Update user booking history 
                # read user information from database
                try:
                    pickle_r = open("customer.pickle","rb")
                except Exception:
                    print("Cannot read information from data base")
                    dic_customer = []
                else:
                    dic_customer = pickle.load(pickle_r)
                    
                # Update user booking history 
                new_book_his = [dic_film[movie_selected][2], dic_film[movie_selected][0], seat_selected]
                new_book_his_text = [f"{dic_film[movie_selected][2]} "
                                f"'{dic_film[movie_selected][0]}' seat: {seat_selected}"]
                dic_customer[current_username][2].append(new_book_his)
                
                # write new customer information 
                try:
                    pickle_w = open("customer.pickle", "wb")
                    pickle.dump(dic_customer, pickle_w)
                    pickle_w.close()
                except Exception as e:
                    print("\nSorry. I won't be able to update these information to database.")
                    print(e)
                else:
                    print("Your booking detail has been added to yout booking history. ")
                    print("-----------------------------------")
                    print("Your booking summary is showed below: ")
                    print(str(new_book_his_text).strip('[]').strip('""'))
                    print(" ")
        
def delete_future_booking(current_username):
    """ This function allows users to delete a future booking."""
    # read user information from database
    try:
        pickle_r = open("customer.pickle","rb")
    except Exception:
        print("Cannot read information from data base")
        dic_customer = []
    else:
        dic_customer = pickle.load(pickle_r)
        
    # select a history   
    for (i, item) in enumerate(dic_customer[current_username][2], start=0):
        if item:    # ensure there is booking detail in item
            print(f"[{i}] {item[0]} {item[1]} seat: {item[2]}")
    
    if not dic_customer[current_username][2]:
        print("You have no booking yet.")
    else:
        booking_choose_successful = False
        while not booking_choose_successful:
            try:
                idx = input("Please choose a booking to delete: ")
                idx = int(idx)
                book_selected = dic_customer[current_username][2][idx]
                if book_selected[0] < datetime.datetime.now():
                    cancel_allowed = False
                else:
                    cancel_allowed = True
            except Exception:
                print("Your input is not recognised, please enter the avaliable index")
            else:       
                booking_choose_successful = True
                
        # check if it is a future booking
        if not cancel_allowed:
            print("The movie show you selected is a past one, you cannot delete it.")
        else: 
            # delete personal profile
            dic_customer[current_username][2].remove(dic_customer[current_username][2][idx])
            try:
                pickle_w = open("customer.pickle", "wb")
                pickle.dump(dic_customer, pickle_w)
                pickle_w.close()
            except Exception as e:
                print("\nSorry. I won't be able to update these information to database.")
                print(e)
            else:
                print("Your booking has been canceled succesfully. ")
            
            # delete seat of the movie show
            # read old information
            try:
                pickle_r = open("filmtime.pickle","rb")
            except Exception:
                print("Cannot read the infomation from database. ")
                dic_film = []
            else:
                dic_film = pickle.load(pickle_r)
            
            # find the correspoding moive show and delete the seat 
            for i in range(0,len(dic_film)):
                if dic_film[i][2] ==  book_selected[0]:
                    x = ord(book_selected[2][0])-97
                    y = int(book_selected[2][1])-1
                    dic_film[i][3][x][y] = " "      
            
            # finally delete the seat
            try:
                pickle_w = open("filmtime.pickle", "wb")
                pickle.dump(dic_film, pickle_w)
                pickle_w.close()
            except Exception as e:
                print("\nSorry. I won't be able to delete the sear for the calceled booking.")
                print(e) 
     
        
def main():
    menu_for_customer()


if __name__ == '__main__': main()