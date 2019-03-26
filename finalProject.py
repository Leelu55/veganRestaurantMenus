from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant)
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showRestaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, menuItems = menuItems)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def addNewRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def addNewMenuItem(restaurant_id):
    if request.method == 'POST':
        newMenuItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newMenuItem)
        session.commit()
        return redirect(url_for('showRestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/edit/',  methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id = restaurant_id, restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
         return render_template('deleteRestaurant.html', restaurant_id = restaurant_id, restaurant = restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuItem_id):
    menuItem = session.query(MenuItem).filter_by(id = menuItem_id).one()
    if request.method == 'POST':
        if request.form['name']:
            menuItem.name = request.form['name']
        if request.form['description']:
            menuItem.description = request.form['description']
        if request.form['price']:
            menuItem.price = request.form['price']
        if request.form['course']:
            menuItem.course = request.form['course']
        session.add(menuItem)
        session.commit()
        return redirect(url_for('showRestaurantMenu', restaurant_id = restaurant_id))

    return render_template('editMenuItem.html', restaurant_id = restaurant_id, menuItem_id = menuItem_id, item = menuItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuItem_id):
    menuItemToDelete = session.query(MenuItem).filter_by(id = menuItem_id).one()
    if request.method == 'POST':
        session.delete(menuItemToDelete)
        session.commit()
        return redirect(url_for('showRestaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menuItem_id = menuItem_id,menuItem = menuItemToDelete)

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant)
    return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [menuItem.serialize for menuItem in menuItems])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/JSON')
def menuItemJSON(restaurant_id, menuItem_id):
    menuItem = session.query(MenuItem).filter_by(id = menuItem_id, restaurant_id = restaurant_id).one()
    return jsonify(MenuItem = [menuItem.serialize])

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
