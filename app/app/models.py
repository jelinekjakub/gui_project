from random import randint
from flask import Flask, request, render_template, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from app.env import Config
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import json


def db_init(engine):
    print(f"Database {engine.url.database} does not exists. Do you want to create it?")
    if not input("[Y]/n ").lower() == 'y':
        exit()
    print("Creating database, running SQL scripts...")
    create_database(engine.url, encoding="utf8mb4")
    print(f"Do you want to run seeders?")
    if input("[Y]/n ").lower() == 'y':
        print("Running seeders...")
        return True
    return False


app = Flask(__name__)
# Setup database engine and session
engine = create_engine(Config().get("DB_HOST", ""))
run_seeders = False
if not database_exists(engine.url):
    run_seeders = db_init(engine)
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()


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

        return self.start_session(new_user)

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

        return redirect(url_for('route.user_recipes', user_id=session['user_id']))

    def remove(self, recipe_id):
        recipe = db_session.query(Recipe).get(recipe_id)
        if recipe.user.id == session['user_id']:
            db_session.delete(recipe)
            db_session.commit()
        return redirect(url_for('route.user_recipes', user_id=session['user_id']))


# Create tables in the database
Base.metadata.create_all(engine)


def random_date(days_back=365):
    return (datetime.now() - timedelta(days=randint(1, days_back), hours=randint(0, 23),
                                       minutes=randint(0, 59))).isoformat()


def random_user(ses):
    user_count = ses.query(func.count(User.id)).scalar()
    random_offset = randint(0, user_count - 1)
    return ses.query(User).offset(random_offset).first()


def seed_users(ses):
    with open('app/seeders/users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    for user_data in users:
        user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
        user = User(**user_data)
        ses.add(user)

    ses.commit()


def seed_recipes(ses):
    with open('app/seeders/recipes.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)

    for recipe_data in recipes:
        recipe_data["date"] = random_date()
        recipe_data["user"] = random_user(ses)
        recipe = Recipe(**recipe_data)
        ses.add(recipe)

    ses.commit()


if run_seeders:
    seed_users(db_session)
    seed_recipes(db_session)
    print("Database seeded!")
    print("Test credentials were created...")
    print("Email: test@test.cz, Password: 123456789")
    input("Finish installation process by pressing Enter")
