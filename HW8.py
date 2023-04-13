# Your name: Daniel Kates
# Your student id: 02396287
# Your email: dkates@umich.edu
# List who you have worked with on this homework: Aaron Benyamini

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import pprint

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    rest_data = {}
    c.execute('''SELECT restaurants.name AS restaurant_name, categories.category AS category_name, buildings.building AS building_name, restaurants.rating
              FROM restaurants
              INNER JOIN categories ON restaurants.category_id = categories.id
              INNER JOIN buildings ON restaurants.building_id = buildings.id''')
    rows = c.fetchall()

    #pprint.pprint(rows)
    for row in rows:
        rest_name = row[0]
        category = row[1]
        building = row[2]
        rating = row[3]
        rest_data[rest_name] = {"category": category, "building": building, "rating": rating}
    
    conn.close()
    return rest_data
#load_rest_data('South_U_Restaurants.db')


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    # Connect to the database and create a cursor
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    # Execute the query to get the category counts
    cur.execute('''SELECT categories.category, COUNT(restaurants.id)
                   FROM restaurants
                   JOIN categories ON restaurants.category_id = categories.id
                   GROUP BY categories.category
                   ORDER BY COUNT(restaurants.id) DESC''')
    
    # Extract the results and create the dictionary
    cat_data = {}
    for row in cur.fetchall():
        cat_data[row[0]] = row[1]
    
    # Close the database connection
    conn.close()
    
    # Plot the categories using a horizontal bar chart
    plt.barh(list(cat_data.keys()), list(cat_data.values()))
    plt.title('Restaurant Categories')
    plt.xlabel('Count')
    plt.ylabel('Category')
    plt.gca().invert_yaxis()  # Reverse the y-axis to show categories in descending order
    plt.show()

    return cat_data


def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    c = conn.cursor()

    restaurant_list = []
    c.execute('''SELECT restaurants.name, restaurants.rating
                 FROM restaurants
                 INNER JOIN buildings ON restaurants.building_id = buildings.id
                 WHERE buildings.building = ?
                 ORDER BY restaurants.rating DESC''', (building_num,))

    rows = c.fetchall()
    for row in rows:
        restaurant_list.append(row[0])
    
    conn.close()
    return restaurant_list

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''SELECT restaurants.name AS restaurant_name, categories.category AS category_name, buildings.building AS building_name, restaurants.rating
              FROM restaurants
              INNER JOIN categories ON restaurants.category_id = categories.id
              INNER JOIN buildings ON restaurants.building_id = buildings.id''')

    rows = c.fetchall()

    # Create a dictionary to store category and building ratings
    category_ratings = {}
    building_ratings = {}

    # Iterate through the rows and update the dictionaries
    for row in rows:
        name, category, building, rating = row
        if category in category_ratings:
            category_ratings[category].append(rating)
        else:
            category_ratings[category] = [rating]

        if building in building_ratings:
            building_ratings[building].append(rating)
        else:
            building_ratings[building] = [rating]

    # Calculate the average rating for each category and building
    avg_category_ratings = {}
    avg_building_ratings = {}
    for category, ratings in category_ratings.items():
        avg_rating = sum(ratings) / len(ratings)
        avg_category_ratings[category] = avg_rating
    for building, ratings in building_ratings.items():
        avg_rating = sum(ratings) / len(ratings)
        avg_building_ratings[building] = avg_rating

    sorted_categories = sorted(avg_category_ratings.items(), key=lambda x: x[1], reverse=True)
    sorted_buildings = sorted(avg_building_ratings.items(), key=lambda x: x[1], reverse=True)

    # Create the bar charts
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].barh([x[0] for x in sorted_categories], [x[1] for x in sorted_categories])
    axs[0].set_xlabel('Ratings')
    axs[0].set_ylabel('Categories')
    axs[0].invert_yaxis()
    fig.suptitle('Average Restaurant Ratings by Category')

    axs[1].barh([str(x[0]) for x in sorted_buildings if str(x[0]).isnumeric()], [x[1] for x in sorted_buildings if str(x[0]).isnumeric()])
    axs[1].set_xlabel('Ratings')
    axs[1].set_ylabel('Building Number')
    axs[1].set_xlim(0, 5)
    axs[1].invert_yaxis()
    fig.suptitle('Average Restaurant Ratings by Building')

    highest_category = sorted_categories[0][0]
    highest_category_rating = sorted_categories[0][1]
    highest_building = sorted_buildings[0][0]
    highest_building_rating = sorted_buildings[0][1]

    return [(highest_category, highest_category_rating), (highest_building, highest_building_rating)]

#Try calling your functions here
def main():
    db = 'South_U_Restaurants.db'
    rest_data = load_rest_data(db)
    cat_data = plot_rest_categories(db)
    building_num = 1140
    building_restaurants = find_rest_in_building(building_num, db)
    # highest_rating = get_highest_rating(db)
    # print("Restaurant data:", rest_data)
    # print("Category data:", cat_data)
    # print("Restaurants in building {}: {}".format(building_num, building_restaurants))
    # print("Highest rating:", highest_rating)

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
