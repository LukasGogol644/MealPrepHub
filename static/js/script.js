// ==========================================
// GLOBAL VARIABLES
// ==========================================
let currentSearchResults = [];

// ==========================================
// PAGE LOAD
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();

    // Enter-Taste für Suche
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchRecipes();
            }
        });
    }
});

// ==========================================
// KATEGORIEN LADEN
// ==========================================
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();

        const categoriesDiv = document.getElementById('categories');
        if (!categoriesDiv) return;

        categoriesDiv.innerHTML = '';

        if (data.categories && data.categories.length > 0) {
            // Zeige ersten 8 Kategorien
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
        const categoriesDiv = document.getElementById('categories');
        if (categoriesDiv) {
            categoriesDiv.innerHTML = '<div class="col-12"><p class="text-danger">Fehler beim Laden der Kategorien</p></div>';
        }
    }
}

// ==========================================
// REZEPT-SUCHE (NACH NAME)
// ==========================================
async function searchRecipes() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput ? searchInput.value.trim() : '';

    if (!query) {
        alert('⚠️ Bitte gib einen Suchbegriff ein!');
        return;
    }

    showLoading(true);
    hideResults();

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        showLoading(false);

        if (data.meals && data.meals.length > 0) {
            currentSearchResults = data.meals;
            displayRecipes(data.meals);
        } else {
            showNoResults();
        }
    } catch (error) {
        showLoading(false);
        showError(error);
    }
}

// ==========================================
// SUCHE NACH KATEGORIE
// ==========================================
async function searchByCategory(category) {
    showLoading(true);
    hideResults();

    // Scroll to results
    window.scrollTo({ top: 600, behavior: 'smooth' });

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ category: category })
        });

        const data = await response.json();
        showLoading(false);

        if (data.meals && data.meals.length > 0) {
            currentSearchResults = data.meals;
            displayRecipes(data.meals);
        } else {
            showNoResults();
        }
    } catch (error) {
        showLoading(false);
        showError(error);
    }
}

// ==========================================
// ZUFÄLLIGES REZEPT
// ==========================================
async function getRandomRecipe() {
    showLoading(true);
    hideResults();

    try {
        const response = await fetch('/api/random');
        const data = await response.json();

        showLoading(false);

        if (data.meals && data.meals.length > 0) {
            currentSearchResults = data.meals;
            displayRecipes(data.meals);
        }
    } catch (error) {
        showLoading(false);
        showError(error);
    }
}

// ==========================================
// REZEPTE ANZEIGEN
// ==========================================
function displayRecipes(recipes) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsDiv = document.getElementById('results');

    if (!resultsDiv) return;

    resultsDiv.innerHTML = '';
    resultsSection.classList.remove('d-none');

    recipes.forEach(recipe => {
        resultsDiv.innerHTML += `
            <div class="col-lg-3 col-md-4 col-sm-6">
                <div class="card recipe-card h-100">
                    <img src="${recipe.strMealThumb}" class="card-img-top" alt="${recipe.strMeal}">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${recipe.strMeal}</h5>
                        <p class="card-text flex-grow-1">
                            ${recipe.strCategory ? `<span class="badge bg-primary">${recipe.strCategory}</span>` : ''}
                            ${recipe.strArea ? `<span class="badge bg-success">${recipe.strArea}</span>` : ''}
                        </p>
                        <button class="btn btn-primary w-100" onclick="viewRecipe('${recipe.idMeal}')">
                            📖 Details anzeigen
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
}

// ==========================================
// REZEPT ANZEIGEN (DETAIL-SEITE)
// ==========================================
function viewRecipe(mealId) {
    window.location.href = `/recipe/${mealId}`;
}

// ==========================================
// UI HELPER FUNCTIONS
// ==========================================
function showLoading(show) {
    const loadingDiv = document.getElementById('loading');
    if (loadingDiv) {
        loadingDiv.classList.toggle('d-none', !show);
    }
}

function hideResults() {
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.add('d-none');
    }
}

function showNoResults() {
    const resultsDiv = document.getElementById('results');
    const resultsSection = document.getElementById('resultsSection');

    if (resultsDiv && resultsSection) {
        resultsSection.classList.remove('d-none');
        resultsDiv.innerHTML = `
            <div class="col-12">
                <div class="alert alert-warning text-center">
                    <h5>😢 Keine Rezepte gefunden</h5>
                    <p>Versuche es mit einem anderen Suchbegriff!</p>
                </div>
            </div>
        `;
    }
}

function showError(error) {
    const resultsDiv = document.getElementById('results');
    const resultsSection = document.getElementById('resultsSection');

    if (resultsDiv && resultsSection) {
        resultsSection.classList.remove('d-none');
        resultsDiv.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger text-center">
                    <h5>❌ Fehler</h5>
                    <p>${error}</p>
                </div>
            </div>
        `;
    }
}