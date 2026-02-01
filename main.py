from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mealprep-secret-key-2026')

# API Configuration
THEMEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1"

# OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# ==========================================
# ROUTE 1: STARTSEITE
# ==========================================
@app.route('/')
def index():
    """Rendert Startseite"""
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
    """Sucht Rezepte nach Name oder Kategorie"""
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
        print(f"Error in search_recipes: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==========================================
# ROUTE 4: FILTER
# ==========================================
@app.route('/api/filter', methods=['POST'])
def filter_recipes():
    """Filtert Rezepte nach Ernährung, Küche oder Kategorie"""
    try:
        data = request.get_json()
        filter_value = data.get('filter', '')

        if not filter_value:
            return jsonify({'error': 'Filter required'}), 400

        # TheMealDB nutzt unterschiedliche Endpoints für verschiedene Filter
        # Versuch 1: Nach Area (Küche)
        url = f"{THEMEALDB_BASE_URL}/filter.php?a={filter_value}"
        response = requests.get(url, timeout=5)
        result = response.json()

        # Falls keine Ergebnisse, versuch Category
        if not result.get('meals'):
            url = f"{THEMEALDB_BASE_URL}/filter.php?c={filter_value}"
            response = requests.get(url, timeout=5)
            result = response.json()

        # Falls immer noch keine Ergebnisse, versuch Ingredient
        if not result.get('meals'):
            url = f"{THEMEALDB_BASE_URL}/filter.php?i={filter_value}"
            response = requests.get(url, timeout=5)
            result = response.json()

        return jsonify(result)

    except Exception as e:
        print(f"Error in filter_recipes: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==========================================
# ROUTE 5: REZEPT-DETAILS
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
# ROUTE 6: REZEPT-DETAIL-SEITE
# ==========================================
@app.route('/recipe/<meal_id>')
def recipe_detail_page(meal_id):
    """Rendert Rezept-Detail-Seite"""
    return render_template('recipe_detail.html', meal_id=meal_id)


# ==========================================
# ROUTE 7: ZUFÄLLIGES REZEPT
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
# ROUTE 8: WOCHENPLAN-SEITE
# ==========================================
@app.route('/week-plan')
def week_plan():
    """Rendert Wochenplan-Seite"""
    return render_template('week_plan.html')


# ==========================================
# ROUTE 9: EINKAUFSLISTE-SEITE
# ==========================================
@app.route('/shopping-list')
def shopping_list():
    """Rendert Einkaufslisten-Seite"""
    return render_template('shopping_list.html')


# ==========================================
# ROUTE 10: AI-PLANNER SEITE
# ==========================================
@app.route('/ai-planner')
def ai_planner():
    """Rendert KI-Planer-Seite"""
    return render_template('ai_planner.html')


# ==========================================
# ROUTE 11: IMPRESSUM
# ==========================================
@app.route('/impressum')
def impressum():
    """Rendert Impressum-Seite"""
    return render_template('impressum.html')


# ==========================================
# ROUTE 12: KI-WOCHENPLAN GENERATOR
# ==========================================
@app.route('/api/generate-ai-plan', methods=['POST'])
def generate_ai_meal_plan():
    """
    Generiert intelligenten Wochenplan basierend auf User-Zielen
    Nutzt OpenAI API + TheMealDB
    """
    try:
        data = request.get_json()
        goal = data.get('goal', 'Gesund essen')
        calories = data.get('calories', 2000)
        protein = data.get('protein', 100)
        dietary_preference = data.get('dietary', '')

        # Hole verfügbare Rezepte basierend auf Präferenz
        search_terms = {
            'Muskelaufbau': 'chicken',
            'Abnehmen': 'salad',
            'Vegan': 'vegan',
            'Vegetarisch': 'vegetarian',
            'Gesund essen': 'healthy',
            'High Protein': 'chicken',
            'Ausgewogen': 'chicken',
            'Energie & Leistung': 'chicken'
        }

        search_term = search_terms.get(goal, 'chicken')

        # Hole Rezepte von TheMealDB
        meals_response = requests.get(
            f"{THEMEALDB_BASE_URL}/search.php?s={search_term}",
            timeout=10
        )
        available_meals = meals_response.json().get('meals', [])

        if not available_meals:
            # Fallback: Random recipes
            meals_response = requests.get(
                f"{THEMEALDB_BASE_URL}/search.php?s=chicken",
                timeout=10
            )
            available_meals = meals_response.json().get('meals', [])

        # Erstelle Meal-Liste für KI
        meal_list = []
        for meal in available_meals[:25]:
            if meal:
                meal_list.append({
                    'id': meal['idMeal'],
                    'name': meal['strMeal'],
                    'category': meal.get('strCategory', 'Unknown'),
                    'area': meal.get('strArea', 'Unknown')
                })

        if not meal_list:
            return jsonify({
                'success': False,
                'error': 'Keine passenden Rezepte gefunden'
            }), 400

        # KI-Prompt erstellen
        prompt = f"""
Du bist ein professioneller Ernährungsberater. Erstelle einen ausgewogenen 7-Tage Wochenplan.

NUTZERZIEL: {goal}
TAGESZIEL KALORIEN: {calories} kcal
TAGESZIEL PROTEIN: {protein}g
ERNÄHRUNGSPRÄFERENZ: {dietary_preference if dietary_preference else 'Keine Einschränkung'}

VERFÜGBARE REZEPTE (nutze NUR diese):
{chr(10).join([f"- {m['name']}" for m in meal_list[:20]])}

AUFGABEN:
1. Wähle für jeden Wochentag (Montag bis Sonntag) genau 3 Mahlzeiten aus
2. Mahlzeiten: Frühstück, Mittagessen, Abendessen
3. Nutze AUSSCHLIESSLICH Rezepte aus der obigen Liste
4. Verteile Protein gleichmäßig über den Tag (Ziel: {protein}g/Tag)
5. Achte auf Abwechslung - kein Rezept mehr als 2x pro Woche
6. Berücksichtige das Ziel "{goal}"

WICHTIG: Antworte AUSSCHLIESSLICH mit folgendem JSON-Format (keine Erklärungen drumherum):

{{
  "monday": {{
    "breakfast": "Exakter Rezeptname aus Liste",
    "lunch": "Exakter Rezeptname aus Liste",
    "dinner": "Exakter Rezeptname aus Liste"
  }},
  "tuesday": {{
    "breakfast": "Exakter Rezeptname aus Liste",
    "lunch": "Exakter Rezeptname aus Liste",
    "dinner": "Exakter Rezeptname aus Liste"
  }},
  "wednesday": {{
    "breakfast": "Exakter Rezeptname aus Liste",
    "lunch": "Exakter Rezeptname aus Liste",
    "dinner": "Exakter Rezeptname aus Liste"
  }},
  "thursday": {{
    "breakfast": "Exakter Rezeptname aus Liste",
    "lunch": "Exakter Rezeptname aus Liste",
    "dinner": "Exakter Rezeptname aus Liste"
  }},
  "friday": {{
    "breakfast": "Exakter Rezeptname aus Liste",
    "lunch": "Exakter Rezeptname aus Liste",
    "dinner": "Exakter Rezeptname aus Liste"
  }},
  "saturday": {{
    "breakfast": "Exakter Rezeptname aus Liste",
    "lunch": "Exakter Rezeptname aus Liste",
    "dinner": "Exakter Rezeptname aus Liste"
  }},
  "sunday": {{
    "breakfast": "Exakter Rezeptname aus Liste",
    "lunch": "Exakter Rezeptname aus Liste",
    "dinner": "Exakter Rezeptname aus Liste"
  }},
  "reasoning": "2-3 Sätze warum dieser Plan optimal für '{goal}' ist"
}}
"""

        # OpenAI API Call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein Ernährungsexperte. Antworte IMMER nur mit validem JSON, keine zusätzlichen Texte."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        # Parse Response
        ai_response = response.choices[0].message.content.strip()

        # Clean JSON (entferne Markdown falls vorhanden)
        json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
        if json_match:
            ai_response = json_match.group(1)

        # Parse JSON
        try:
            plan_data = json.loads(ai_response)
        except json.JSONDecodeError:
            # Fallback: Versuche JSON zu extrahieren
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                ai_response = ai_response[json_start:json_end]
                plan_data = json.loads(ai_response)
            else:
                raise

        # Füge Meal IDs und Bilder hinzu
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        meal_types = ['breakfast', 'lunch', 'dinner']

        for day in days:
            if day in plan_data:
                for meal_type in meal_types:
                    if meal_type in plan_data[day]:
                        meal_name = plan_data[day][meal_type]

                        # Finde passendes Meal
                        matching_meal = None
                        for m in meal_list:
                            if m['name'].lower() == meal_name.lower():
                                matching_meal = m
                                break

                        # Fuzzy Match falls exakter Match fehlt
                        if not matching_meal:
                            for m in meal_list:
                                if meal_name.lower() in m['name'].lower() or m['name'].lower() in meal_name.lower():
                                    matching_meal = m
                                    break

                        if matching_meal:
                            plan_data[day][f'{meal_type}_id'] = matching_meal['id']
                            # Hole Bild
                            try:
                                meal_detail = requests.get(
                                    f"{THEMEALDB_BASE_URL}/lookup.php?i={matching_meal['id']}",
                                    timeout=5
                                ).json()
                                if meal_detail.get('meals'):
                                    plan_data[day][f'{meal_type}_thumb'] = meal_detail['meals'][0].get('strMealThumb',
                                                                                                       '')
                            except:
                                pass

        return jsonify({
            'success': True,
            'plan': plan_data,
            'goal': goal,
            'daily_targets': {
                'calories': calories,
                'protein': protein
            }
        })

    except Exception as e:
        print(f"Error in generate_ai_meal_plan: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Fehler beim Generieren: {str(e)}'
        }), 500


# ==========================================
# ROUTE 13: NÄHRWERTE VON OPEN FOOD FACTS (API 3!)
# ==========================================
@app.route('/api/nutrition/<barcode>')
def get_nutrition_info(barcode):
    """
    Holt Nährwertinformationen von Open Food Facts
    API 3 für Uni-Projekt
    """
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if data.get('status') == 1 and data.get('product'):
            product = data['product']

            # Extrahiere wichtige Nährwerte
            nutrition_info = {
                'product_name': product.get('product_name', 'Unbekannt'),
                'nutriscore': product.get('nutrition_grades', 'Nicht berechnet'),
                'calories': product.get('nutriments', {}).get('energy-kcal_100g', 0),
                'protein': product.get('nutriments', {}).get('proteins_100g', 0),
                'carbs': product.get('nutriments', {}).get('carbohydrates_100g', 0),
                'fat': product.get('nutriments', {}).get('fat_100g', 0),
                'sugar': product.get('nutriments', {}).get('sugars_100g', 0),
                'fiber': product.get('nutriments', {}).get('fiber_100g', 0),
                'salt': product.get('nutriments', {}).get('salt_100g', 0),
                'image_url': product.get('image_url', ''),
                'brands': product.get('brands', ''),
                'categories': product.get('categories', ''),
            }

            return jsonify({
                'success': True,
                'nutrition': nutrition_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Produkt nicht gefunden'
            }), 404

    except Exception as e:
        print(f"Error in get_nutrition_info: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==========================================
# ROUTE 14: PRODUKT NACH NUTRISCORE SUCHEN (API 3!)
# ==========================================
@app.route('/api/search-nutrition', methods=['POST'])
def search_by_nutriscore():
    """
    Sucht Produkte nach Nutriscore
    """
    try:
        data = request.get_json()
        nutriscore = data.get('nutriscore', 'a')  # a, b, c, d, e
        category = data.get('category', '')

        # Open Food Facts Search API
        url = f"https://world.openfoodfacts.org/api/v2/search"
        params = {
            'nutrition_grades_tags': nutriscore,
            'fields': 'code,product_name,nutrition_grades,nutriments,image_url,brands',
            'page_size': 20
        }

        if category:
            params['categories_tags_en'] = category

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        return jsonify(response.json())

    except Exception as e:
        print(f"Error in search_by_nutriscore: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recipe-nutrition/<meal_id>')
def get_recipe_nutrition(meal_id):
    """
    Berechnet geschätzte Nährwerte basierend auf Zutaten
    Nutzt Open Food Facts API
    """
    try:
        # Hole Rezept-Details
        meal_response = requests.get(
            f"{THEMEALDB_BASE_URL}/lookup.php?i={meal_id}",
            timeout=5
        )
        meal_data = meal_response.json()

        if not meal_data.get('meals'):
            return jsonify({'success': False, 'error': 'Rezept nicht gefunden'}), 404

        meal = meal_data['meals'][0]

        # Sammle alle Zutaten
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f'strIngredient{i}', '')
            measure = meal.get(f'strMeasure{i}', '')
            if ingredient and ingredient.strip():
                ingredients.append({
                    'ingredient': ingredient.strip(),
                    'measure': measure.strip()
                })

        # Geschätzte Nährwerte basierend auf typischen Werten
        # (In einer echten App würde man Open Food Facts für jede Zutat abfragen)

        # Einfache Schätzung basierend auf Kategorie
        category = meal.get('strCategory', '').lower()

        # Standard-Nährwerte pro Kategorie (pro Portion)
        nutrition_estimates = {
            'beef': {'calories': 450, 'protein': 35, 'carbs': 25, 'fat': 22},
            'chicken': {'calories': 380, 'protein': 42, 'carbs': 20, 'fat': 12},
            'seafood': {'calories': 320, 'protein': 38, 'carbs': 18, 'fat': 8},
            'pork': {'calories': 420, 'protein': 32, 'carbs': 22, 'fat': 20},
            'vegetarian': {'calories': 320, 'protein': 15, 'carbs': 45, 'fat': 10},
            'vegan': {'calories': 280, 'protein': 12, 'carbs': 48, 'fat': 8},
            'pasta': {'calories': 480, 'protein': 18, 'carbs': 65, 'fat': 14},
            'dessert': {'calories': 350, 'protein': 5, 'carbs': 55, 'fat': 15},
            'breakfast': {'calories': 380, 'protein': 20, 'carbs': 42, 'fat': 12},
            'side': {'calories': 180, 'protein': 5, 'carbs': 28, 'fat': 6},
            'starter': {'calories': 220, 'protein': 8, 'carbs': 25, 'fat': 9},
            'goat': {'calories': 400, 'protein': 30, 'carbs': 20, 'fat': 18},
            'lamb': {'calories': 440, 'protein': 32, 'carbs': 18, 'fat': 24},
            'miscellaneous': {'calories': 350, 'protein': 18, 'carbs': 35, 'fat': 14},
        }

        # Hole passende Schätzung
        nutrition = nutrition_estimates.get(
            category,
            {'calories': 380, 'protein': 22, 'carbs': 35, 'fat': 15}
        )

        return jsonify({
            'success': True,
            'meal_id': meal_id,
            'meal_name': meal.get('strMeal', ''),
            'category': meal.get('strCategory', ''),
            'nutrition': {
                'calories': nutrition['calories'],
                'protein': nutrition['protein'],
                'carbs': nutrition['carbs'],
                'fat': nutrition['fat'],
                'note': 'Geschätzte Werte pro Portion'
            },
            'ingredients_count': len(ingredients)
        })

    except Exception as e:
        print(f"Error in get_recipe_nutrition: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
