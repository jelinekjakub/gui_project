from flask import Flask, jsonify, request, flash, render_template, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from extensions.env import Config  # Assuming this import is correct
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Setup database engine and session
engine = create_engine(Config().get("DB_HOST", ""))
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()

app = Flask(__name__)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    recipes = relationship('Recipe', back_populates='user')

    def start_session(self, user):
        session['auth'] = True
        session['user_id'] = user.id
        session['user'] = {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        return redirect(url_for('route.index'))

    def login(self):
        user = db_session.query(User).filter_by(email=request.form['email']).first()

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            return self.start_session(user)
        else:
            return render_template('login.html', message="Nesprávné jméno nebo heslo"), 401

    def register(self):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if db_session.query(User).filter_by(email=email).first():
            return render_template('register.html', message="Tento email již někdo používá"), 400

        hashed_password = pbkdf2_sha256.hash(password)

        new_user = User(name=name, email=email, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return self.start_session()

    def logout(self):
        session.clear()
        return redirect('/')

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    description = Column(String(500), nullable=False)
    ingredients = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='recipes')

    def create(self):
        name = request.form['name']
        author = db_session.query(User).filter_by(id=session['user_id']).first()
        ingredients = request.form['ingredients']
        description = request.form['description']

        new_recipe = Recipe(
            name=name,
            user=author,
            ingredients=ingredients,
            description=description
        )

        db_session.add(new_recipe)
        db_session.commit()

        return redirect(url_for('route.recipes'))

    def index(self, user_id=None, search=None, latest=None):
        query = db_session.query(Recipe)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if search:
            query = query.filter(Recipe.name.ilike(f"%{search}%"))
        if latest:
            query = query.order_by(Recipe.date.desc()).limit(3)
        else:
            query = query.order_by(Recipe.date.desc())
        return query.all()

    def edit(self, recipe_id):
        recipe = db_session.query(Recipe).get(recipe_id)
        if recipe.user.id == session['user_id']:
            return recipe

    def update(self, recipe_id):
        recipe = db_session.query(Recipe).get(recipe_id)
        recipe.name = request.form['name']
        recipe.ingredients = request.form['ingredients']
        recipe.description = request.form['description']
        recipe.date = datetime.now()
        db_session.commit()

        return redirect(url_for('user_recipes', user_id=session['user_id']))

    def remove(self, recipe_id):
        recipe = db_session.query(Recipe).get(recipe_id)
        if recipe.user.id == session['user_id']:
            db_session.delete(recipe)
            db_session.commit()
        return redirect(url_for('user_recipes', user_id=session['user_id']))

# Ensure the relationships are defined correctly
User.recipes = relationship('Recipe', order_by=Recipe.id, back_populates='user')

# Create tables in the database
Base.metadata.create_all(engine)

# Assuming routes are defined somewhere else
