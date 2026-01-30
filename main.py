from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mealprep-secret-key-2024')

# API Configuration
THEMEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')


# ==========================================
# ROUTE 1: STARTSEITE
# ==========================================
@app.route('/')
def index():
    """Rendert Startseite mit Suchfeld und Kategorien"""
    return render_template('index.html')


# ==========================================
# ROUTE 2: KATEGORIEN ABRUFEN
# ==========================================
@app.route('/api/categories')
def get_categories():
    """Holt alle Meal-Kategorien von TheMealDB"""
    try:
        url = f"{THEMEALDB_BASE_URL}/categories.php"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================
# ROUTE 3: REZEPT-SUCHE
# ==========================================
@app.route('/api/search', methods=['POST'])
def search_recipes():
    """
    Sucht Rezepte nach Name oder Kategorie
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        category = data.get('category', '')

        if category:
            url = f"{THEMEALDB_BASE_URL}/filter.php?c={category}"
        elif query:
            url = f"{THEMEALDB_BASE_URL}/search.php?s={query}"
        else:
            return jsonify({'error': 'Query or category required'}), 400

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================
# ROUTE 4: REZEPT-DETAILS
# ==========================================
@app.route('/api/recipe/<meal_id>')
def get_recipe_detail(meal_id):
    """Holt Details zu einem spezifischen Rezept"""
    try:
        url = f"{THEMEALDB_BASE_URL}/lookup.php?i={meal_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================
# ROUTE 5: REZEPT-DETAIL-SEITE
# ==========================================
@app.route('/recipe/<meal_id>')
def recipe_detail_page(meal_id):
    """Rendert Rezept-Detail-Seite"""
    return render_template('recipe_detail.html', meal_id=meal_id)


# ==========================================
# ROUTE 6: ZUFÄLLIGES REZEPT
# ==========================================
@app.route('/api/random')
def get_random_recipe():
    """Gibt ein zufälliges Rezept zurück"""
    try:
        url = f"{THEMEALDB_BASE_URL}/random.php"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================
# ROUTE 7: WOCHENPLAN-SEITE
# ==========================================
@app.route('/week-plan')
def week_plan():
    """Rendert Wochenplan-Seite"""
    return render_template('week_plan.html')


# ==========================================
# ROUTE 8: EINKAUFSLISTE-SEITE
# ==========================================
@app.route('/shopping-list')
def shopping_list():
    """Rendert Einkaufslisten-Seite"""
    return render_template('shopping_list.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)