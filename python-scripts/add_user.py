import os
import sys
import json

import pymongo
from pymongo import MongoClient

def main():

    print('Beginning user add program...')

    client = MongoClient('localhost', 27017)
    db = client['dinogram']

    repeat = True
    while repeat:
        first = input('First Name: ')
        last  = input('Last Name: ')
        dob   = input('Date of Birth (format=YYYY-MM-DD): ')
        email = input('Email: ')

        users_collection = db.users

        post_data = {
            "First": first,
            "Last": last,
            "Birthday": dob,
            "Email": email
        }

        insert_result = users_collection.insert_one(post_data)
        print('\nData inserted successfully!\n')

        continue_string = input('Would you like to add another user? (y/n): ')

        if continue_string == 'y':
            repeat = True
        elif continue_string == 'n':
            repeat = False

    print('Closing database connection...')
    client.close()

if __name__ == '__main__':
    main()
