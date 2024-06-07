from flask import Blueprint, request, render_template
from app.models import User, Recipe
from extensions.auth import auth
from datetime import datetime
bp = Blueprint('route', __name__)


# Default routes
@bp.route('/')
def index():
    return render_template('index.html', recipes=Recipe().index(latest=3), datetime=datetime)


@bp.errorhandler(404)
def not_found(e):
    return render_template("404.html") 


# User routes
@bp.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return User().login()
    else:
        return render_template('login.html')


@bp.route('/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return User().register()
    else:
        return render_template('register.html')


@bp.route('/user/logout')
def logout():
    return User().logout()


# Recipes routes
@bp.route('/recipes')
def recipes():
    if request.args.get('search'):
        search = request.args.get('search')
        recipes_list = Recipe().index(search=search)
        return render_template('recipes.html', recipes=recipes_list, datetime=datetime)
    recipes_list = Recipe().index()
    return render_template('recipes.html', recipes=recipes_list, datetime=datetime)


@bp.route('/add-recipe', methods=["GET", "POST"])
@auth
def add_recipe():
    if request.method == "POST":
        return Recipe().create()
    else:
        return render_template('add-recipe.html')


@bp.route('/edit-recipe/<id>', methods=['GET', 'POST'])
@auth
def edit_recipe(id):
    if request.method == "GET":
        return render_template('edit-recipe.html', recipe=Recipe().edit(id))
    else:
        return Recipe().update(id)


@bp.route('/remove-recipe/<id>')
@auth
def remove_recipe(id):
    if request.method == "GET":
        return Recipe().remove(id)


@bp.route('/user-recipes/<user_id>')
def user_recipes(user_id):
    return render_template('user_recipes.html', recipes=Recipe().index(user_id=user_id), datetime=datetime, user_id=user_id)