// Load categories on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
});

// ==========================================
// KATEGORIEN LADEN
// ==========================================
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();

        const categoriesDiv = document.getElementById('categories');
        categoriesDiv.innerHTML = '';

        if (data.categories && data.categories.length > 0) {
            data.categories.slice(0, 8).forEach(category => {
                categoriesDiv.innerHTML += `
                    <div class="col-lg-3 col-md-4 col-sm-6">
                        <div class="card category-card h-100" onclick="searchByCategory('${category.strCategory}')">
                            <img src="${category.strCategoryThumb}" class="card-img-top" alt="${category.strCategory}">
                            <div class="card-body text-center">
                                <h6 class="mb-0">${category.strCategory}</h6>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// ==========================================
// REZEPTE SUCHEN
// ==========================================
async function searchRecipes() {
    const query = document.getElementById('searchInput').value.trim();

    if (!query) {
        alert('Bitte gib einen Suchbegriff ein');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        displayRecipes(data.meals);
    } catch (error) {
        alert('Fehler bei der Suche: ' + error);
    } finally {
        hideLoading();
    }
}

// ==========================================
// NACH KATEGORIE SUCHEN
// ==========================================
async function searchByCategory(category) {
    showLoading();

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category: category })
        });

        const data = await response.json();
        displayRecipes(data.meals);

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        alert('Fehler beim Laden der Kategorie: ' + error);
    } finally {
        hideLoading();
    }
}

// ==========================================
// ZUFÄLLIGES REZEPT
// ==========================================
async function getRandomRecipe() {
    showLoading();

    try {
        const response = await fetch('/api/random');
        const data = await response.json();

        if (data.meals && data.meals.length > 0) {
            window.location.href = `/recipe/${data.meals[0].idMeal}`;
        }
    } catch (error) {
        alert('Fehler beim Laden: ' + error);
    } finally {
        hideLoading();
    }
}

// ==========================================
// REZEPTE ANZEIGEN
// ==========================================
function displayRecipes(meals) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsDiv = document.getElementById('searchResults');

    if (!meals || meals.length === 0) {
        resultsDiv.innerHTML = '<div class="col-12 text-center"><p class="text-muted">Keine Rezepte gefunden</p></div>';
        resultsSection.classList.remove('d-none');
        return;
    }

    resultsDiv.innerHTML = '';

    meals.forEach(meal => {
        resultsDiv.innerHTML += `
            <div class="col-lg-3 col-md-4 col-sm-6">
                <div class="card recipe-card h-100" onclick="viewRecipe('${meal.idMeal}')">
                    <img src="${meal.strMealThumb}" class="card-img-top" alt="${meal.strMeal}">
                    <div class="card-body">
                        <h6 class="card-title">${meal.strMeal}</h6>
                        <span class="badge bg-primary">${meal.strCategory || 'Rezept'}</span>
                    </div>
                </div>
            </div>
        `;
    });

    resultsSection.classList.remove('d-none');
}

// ==========================================
// ZU REZEPT-DETAIL NAVIGIEREN
// ==========================================
function viewRecipe(mealId) {
    window.location.href = `/recipe/${mealId}`;
}

// ==========================================
// LOADING STATES
// ==========================================
function showLoading() {
    document.getElementById('loadingSection').classList.remove('d-none');
}

function hideLoading() {
    document.getElementById('loadingSection').classList.add('d-none');
}