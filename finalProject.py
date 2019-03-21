from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/<int:restaurant_id>/')

@app.route('/restaurant/<int:restaurant_id>/menu/')
def showRestaurantMenu(restaurant_id):
    return render_template('menu.html', restaurant = restaurants[restaurant_id-1], menuItems = items)

@app.route('/restaurant/new/')
def addNewRestaurant():
    return "Here we will add a new restaurant"

@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def addNewMenuItem(restaurant_id):
    return "Here we will add a new menu item"


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return("Edit a restaurant")

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return "Delete Restaurant"

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit/')
def editMenuItem(restaurant_id, menuItem_id):
    menuItem = items[menuItem_id - 1]
    return render_template('editMenuItem.html', restaurant_id = restaurant_id, menuItem_id =menuItem_id, item = menuItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete/')
def deleteMenuItem(restaurant_id, menuItem_id):
    return "Delete Menu Item of Restaurant"



#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
