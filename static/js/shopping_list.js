// ==========================================
// SHOPPING LIST - BEIM LADEN
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    generateShoppingList();
});

// ==========================================
// EINKAUFSLISTE GENERIEREN
// ==========================================
async function generateShoppingList() {
    const container = document.getElementById('shoppingListContainer');
    const weekPlan = JSON.parse(localStorage.getItem('weekPlan') || '{}');

    // Alle Mahlzeiten sammeln
    const allMeals = [];
    for (const meals of Object.values(weekPlan)) {
        allMeals.push(...meals);
    }

    if (allMeals.length === 0) {
        container.innerHTML = `
            <div class="alert alert-warning text-center">
                <h5>📭 Dein Wochenplan ist leer</h5>
                <p>Füge erst Rezepte zu deinem Wochenplan hinzu, um eine Einkaufsliste zu erstellen.</p>
                <a href="/week-plan" class="btn btn-primary">Zum Wochenplan</a>
            </div>
        `;
        return;
    }

    // Für jede Mahlzeit: Zutaten abrufen
    const allIngredients = [];

    for (const meal of allMeals) {
        try {
            const response = await fetch(`/api/recipe/${meal.id}`);
            const data = await response.json();

            if (data.meals && data.meals.length > 0) {
                const recipe = data.meals[0];

                // Zutaten extrahieren
                for (let i = 1; i <= 20; i++) {
                    const ingredient = recipe[`strIngredient${i}`];
                    const measure = recipe[`strMeasure${i}`];

                    if (ingredient && ingredient.trim()) {
                        allIngredients.push({
                            name: ingredient.trim(),
                            measure: measure ? measure.trim() : '',
                            category: categorizeIngredient(ingredient)
                        });
                    }
                }
            }
        } catch (error) {
            console.error('Error fetching recipe:', error);
        }
    }

    // Nach Kategorien gruppieren
    const grouped = groupByCategory(allIngredients);

    // Anzeigen
    displayShoppingList(grouped);
}

// ==========================================
// ZUTAT KATEGORISIEREN
// ==========================================
function categorizeIngredient(ingredient) {
    const lower = ingredient.toLowerCase();

    // Kategorien-Mapping
    const categories = {
        '🥩 Fleisch & Fisch': ['chicken', 'beef', 'pork', 'fish', 'salmon', 'tuna', 'turkey', 'lamb', 'meat'],
        '🥬 Gemüse & Obst': ['tomato', 'onion', 'garlic', 'pepper', 'carrot', 'potato', 'lettuce', 'apple', 'banana', 'lemon'],
        '🥛 Milchprodukte': ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'egg'],
        '🌾 Getreide & Backwaren': ['rice', 'pasta', 'bread', 'flour', 'noodles'],
        '🧂 Gewürze & Öle': ['salt', 'pepper', 'oil', 'sugar', 'spice', 'herb'],
        '🥫 Konserven': ['tomato paste', 'stock', 'broth']
    };

    for (const [category, keywords] of Object.entries(categories)) {
        if (keywords.some(keyword => lower.includes(keyword))) {
            return category;
        }
    }

    return '📦 Sonstiges';
}

// ==========================================
// NACH KATEGORIE GRUPPIEREN
// ==========================================
function groupByCategory(ingredients) {
    const grouped = {};

    ingredients.forEach(item => {
        if (!grouped[item.category]) {
            grouped[item.category] = [];
        }
        grouped[item.category].push(item);
    });

    return grouped;
}

// ==========================================
// EINKAUFSLISTE ANZEIGEN
// ==========================================
function displayShoppingList(grouped) {
    const container = document.getElementById('shoppingListContainer');
    let html = '';

    // Statistik
    const totalItems = Object.values(grouped).reduce((sum, items) => sum + items.length, 0);

    html += `
        <div class="card mb-4">
            <div class="card-body text-center">
                <h5>📊 Gesamt: <strong>${totalItems} Zutaten</strong></h5>
            </div>
        </div>
    `;

    // Pro Kategorie
    for (const [category, items] of Object.entries(grouped)) {
        html += `
            <div class="card mb-3 print-friendly">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">${category}</h5>
                </div>
                <div class="card-body">
                    <ul class="list-group list-group-flush">
                        ${items.map((item, index) => `
                            <li class="list-group-item">
                                <input type="checkbox" class="form-check-input me-2" id="item-${category}-${index}">
                                <label for="item-${category}-${index}">
                                    ${item.measure ? `<strong>${item.measure}</strong> ` : ''}${item.name}
                                </label>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    container.innerHTML = html;
}

// ==========================================
// MANUELLES ITEM HINZUFÜGEN
// ==========================================
function addManualItem() {
    const input = document.getElementById('manualItem');
    const value = input.value.trim();

    if (!value) {
        alert('⚠️ Bitte gib eine Zutat ein!');
        return;
    }

    // TODO: Item zur Liste hinzufügen
    alert(`✅ "${value}" wurde hinzugefügt (Feature in Entwicklung)`);
    input.value = '';
}

// ==========================================
// LISTE LÖSCHEN
// ==========================================
function clearList() {
    if (confirm('Möchtest du die Einkaufsliste wirklich löschen?')) {
        localStorage.removeItem('weekPlan');
        location.reload();
    }
}