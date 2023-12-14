from flask import Flask, jsonify, request, flash, render_template, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from extensions.db import users_db
from extensions.db import recipes_db
import uuid
import re


class User:

    def start_session(self, user):
        del user['password']
        session['auth'] = True
        session['user'] = user
        return redirect(url_for('route.index'))

    def login(self):
        user = users_db.find_one({
            "email": request.form['email']
        })

        if user and pbkdf2_sha256.verify(request.form['password'], user['password']):
            return self.start_session(user)
        else:
            return render_template('login.html', message="Nesprávné jméno nebo heslo"), 401

    def register(self):
        # Create new user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form['name'],
            "email": request.form['email'],
            "password": request.form['password']
        }

        # Check for existing emails
        if users_db.find_one({ "email": user['email'] }):
            return render_template('register.html', message="Tento email již někdo používá"), 400

        # Password encryption
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        users_db.insert_one(user)

        return self.start_session(user)
    
    def logout(self):
        session.clear()
        return redirect('/')
    
class Recipe:
    def create(self):
        recipe = {
            "_id": uuid.uuid4().hex,
            "name": request.form['name'],
            "date": datetime.now().isoformat(),
            "author": session['user'],
            "ingredients": request.form['ingredients'],
            "description": request.form['description']
        }

        recipes_db.insert_one(recipe)

        return redirect(url_for('route.recipes'))
    
    def index(self, user_id=None, search=None, latest=None):
        if user_id:
            return recipes_db.find({"author._id": user_id}).sort("date", -1)
        elif search:
            recipes_db.create_index([("name", "text")])
            regex_pattern = f".*{re.escape(search)}.*"
            return recipes_db.find({"name": {"$regex": regex_pattern, "$options": "i"}}).sort("date", -1)
        elif latest:
            return recipes_db.find().sort("date", -1).limit(3)
        else:
            return recipes_db.find().sort("date", -1)

    def edit(self, id):
        recipe = recipes_db.find_one({"_id": id})
        if recipe['author']['_id'] == session['user']['_id']:
            return recipe
        
    def update(self, id):
        updated = { "$set": {
            "name": request.form['name'],
            "ingredients": request.form['ingredients'],
            "description": request.form['description'],
            "date": datetime.now().isoformat(),
        }}
        recipes_db.update_one({"_id": id}, updated)
        return redirect(url_for('route.user_recipes', user_id = session['user']['_id']))

    def remove(self, id):
        recipe = recipes_db.find_one({"_id": id})
        if recipe['author']['_id'] == session['user']['_id']:
            recipes_db.delete_one(recipe)
        return redirect(url_for('route.user_recipes', user_id = session['user']['_id']))
