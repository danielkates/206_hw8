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

    # get highest rated category
    c.execute('SELECT category, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY category ORDER BY avg_rating DESC LIMIT 1')
    highest_category = c.fetchone()

    # plot bar chart for category ratings
    plt.subplot(211)
    c.execute('SELECT category, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY category ORDER BY avg_rating ASC')
    categories = c.fetchall()
    category_names = [category[0] for category in categories]
    avg_ratings = [category[1] for category in categories]
    plt.barh(category_names, avg_ratings)
    plt.title('Average Restaurant Ratings by Category')
    plt.xlabel('Rating')
    plt.ylabel('Category')
    plt.xlim(0, 5)

    # get highest rated building
    c.execute('SELECT building, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id GROUP BY building ORDER BY avg_rating DESC LIMIT 1')
    highest_building = c.fetchone()

    # plot bar chart for building ratings
    plt.subplot(212)
    c.execute('SELECT building, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id GROUP BY building ORDER BY avg_rating ASC')
    buildings = c.fetchall()
    building_names = [str(building[0]) for building in buildings] # convert building numbers to strings
    avg_ratings = [building[1] for building in buildings]
    plt.barh(building_names, avg_ratings)
    plt.title('Average Restaurant Ratings by Building')
    plt.xlabel('Rating')
    plt.ylabel('Building')
    plt.xlim(0, 5)

    plt.subplots_adjust(hspace=0.4)
    plt.show()

    return [(highest_category[0], highest_category[1]), (highest_building[0], highest_building[1])]

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
