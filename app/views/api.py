from datetime import datetime

import json
from flask import g, Response, request

from my_meals.main import app
from my_meals.models import Meal, User
from views import required_roles


@app.route('/api/meals', methods=['GET', 'POST'])
@required_roles('user', 'admin', 'user_manager')
def meals():
    if request.method == 'POST':
        if request.form.get('del'):
            meal = Meal.query.get(request.form.get('id'))
            meal.delete()
        else:    
            timestamp = request.form['timestamp']
            if "/" in timestamp:
                timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
            else:    
                timestamp = float(timestamp) / 1000.0
                timestamp = datetime.fromtimestamp(timestamp)
            text = request.form['text']
            calories = request.form['calories']

            if request.form.get('id'):
                meal = Meal.query.get(request.form.get('id'))
                meal.timestamp = timestamp
                meal.text = text
                meal.calories = calories
                meal.save()
            else:
                new_meal = Meal(timestamp=timestamp, text=text, calories=calories, user=g.user)
                new_meal.save()
    
    meals = Meal.query.filter_by(user=g.user).all()
    meal_list = [dict(meal) for meal in meals]

    return Response(json.dumps(meal_list), mimetype='application/json', headers={'Cache-Control': 'no-cache', 
                                                                                 'Access-Control-Allow-Origin': '*'})

@app.route('/api/users', methods=['GET', 'POST'])
@required_roles('admin', 'user_manager')
def get_users():
    if request.method == 'POST':
        if request.form.get('del'):
            user = User.query.get(request.form.get('id'))
            user.delete()
        else:
            username = request.form.get('username')
            password = request.form.get('password')

            user_id = request.form.get('id')
            if user_id:
                user = User.query.get(user_id)
                user.username = username
                user.save()
            else:
                new_user = User(username, password, 'user')
                new_user.save()

    users = User.query.filter_by(role='user').all()
    users = [dict(user) for user in users]

    return Response(json.dumps(users), mimetype='application/json', headers={'Cache-Control': 'no-cache', 
                                                                             'Access-Control-Allow-Origin': '*'})


@app.route('/api/users/<username>', methods=['GET', 'POST'])
@required_roles('admin')
def get_user_meals(username):
    
    if request.method == 'POST':
        if request.form.get('del'):
            meal = Meal.query.get(request.form.get('id'))
            meal.delete()
        else:    
            timestamp = request.form['timestamp']
            if "/" in timestamp:
                timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
            else:    
                timestamp = float(timestamp) / 1000.0
                timestamp = datetime.fromtimestamp(timestamp)
            text = request.form['text']
            calories = request.form['calories']

            if request.form.get('id'):
                meal = Meal.query.get(request.form.get('id'))
                meal.timestamp = timestamp
                meal.text = text
                meal.calories = calories
                meal.save()
            else:
                user = User.query.filter_by(username=username).first()
                new_meal = Meal(timestamp=timestamp, text=text, calories=calories, user=user)
                new_meal.save()

    user = User.query.filter_by(username=username).first()
    user_meals = Meal.query.filter_by(user=user).all()
    user_meals = [dict(meal) for meal in user_meals]

    return Response(json.dumps(user_meals), mimetype='application/json', headers={'Cache-Control': 'no-cache', 
                                                                             'Access-Control-Allow-Origin': '*'})
