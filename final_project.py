from flask import Flask, render_template, url_for, request, \
    redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()

    def format(self):
        return {'name': self.name, 'id': self.id}
    return jsonify(restaurants=[format(i) for i in restaurants])


@app.route('/restaurants/new/', methods=['get', 'post'])
def newRestaurant():
    if request.method == 'POST':
        r = Restaurant()
        r.name = request.form['name']
        session.add(r)
        session.commit()
        flash('new restaurant %s created!' % r)
        return redirect(url_for('restaurantList'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['get', 'post'])
def editRestaurant(restaurant_id):
    r = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            r.name = request.form['name']
        session.add(r)
        session.commit()
        flash('Restarant %s edited' % r.name)
        return redirect(url_for('restaurantList'))
    else:
        return render_template('editrestaurant.html', restaurant=r)


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['get', 'post'])
def deleteRestaurant(restaurant_id):
    r = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(r)
        session.commit()
        flash('Restarant %s deleted' % r.name)
        return redirect(url_for('restaurantList'))
    else:
        return render_template('deleterestaurant.html', restaurant=r)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template('menu0.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantMenuJSON(restaurant_id):
    r = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

    def format(self):
        return {'name': self.name, 'price': self.price, 'description': self.description}
    return jsonify(menu=[format(i) for i in r])

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON')
def MenuItemJSON(restaurant_id, menu_id):
    r = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).filter_by(id=menu_id).one()

    def format(self):
        return {'name': self.name, 'price': self.price, 'description': self.description}
    return jsonify(menu=format(r))

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['get', 'post'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        r = MenuItem()
        r.name = request.form['name']
        r.description = request.form['description']
        r.price = request.form['price']
        r.restaurant_id = restaurant_id
        session.add(r)
        session.commit()
        flash('new item %s created!' % r)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edititem', methods=['get', 'post'])
def editMenuItem(restaurant_id, menu_id):
    r = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            r.name = request.form['name']
        if request.form['description']:
            r.description = request.form['description']
        if request.form['price']:
            r.price = request.form['price']
        session.add(r)
        session.commit()
        flash('item %s edited!' % r)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=r)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/deleteitem/', methods=['get', 'post'])
def deleteMenuItem(restaurant_id, menu_id):
    r = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(r)
        session.commit()
        flash('Item %s deleted' % r.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=r)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'supa_secret'
    app.run(host='0.0.0.0', port=5000)
