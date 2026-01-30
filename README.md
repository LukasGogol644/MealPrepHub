# 🍱 MealPrep Hub

Eine umfassende Webanwendung zur Essensplanung und Rezeptsuche, entwickelt mit Flask. MealPrep Hub hilft Nutzern bei der Planung ihrer wöchentlichen Mahlzeiten, beim Entdecken von Rezepten, beim Erstellen von Einkaufslisten und beim Generieren von KI-gestützten Essensplänen, die auf ihre Ernährungsziele zugeschnitten sind.

## 📋 Inhaltsverzeichnis

- [Funktionen](#funktionen)
- [Verwendete Technologien](#verwendete-technologien)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [API-Endpunkte](#api-endpunkte)
- [Screenshots](#screenshots)
- [Lizenz](#lizenz)

## ✨ Funktionen

- **🔍 Rezeptsuche**: Durchsuche tausende Rezepte von der TheMealDB API
- **📂 Kategorie-Browsen**: Stöbere durch Rezepte nach Kategorien (Rind, Hähnchen, Dessert, etc.)
- **📅 Wöchentliche Essensplanung**: Erstelle und verwalte wöchentliche Essenspläne
- **🛒 Einkaufsliste**: Generiere Einkaufslisten aus deinen Essensplänen
- **🤖 KI-gestützte Essensplanung**: Erhalte personalisierte wöchentliche Essenspläne mit OpenAI GPT-4
  - Anpassbare Ziele (Muskelaufbau, Gewichtsverlust, Gesunde Ernährung, etc.)
  - Kalorien- und Proteinziele
  - Ernährungspräferenzen (Vegan, Vegetarisch, etc.)
- **🎲 Zufällige Rezeptentdeckung**: Lass dich von zufälligen Rezeptvorschlägen inspirieren
- **📱 Responsives Design**: Mobile-freundliche Benutzeroberfläche mit Bootstrap 5

## 🛠 Verwendete Technologien

### Backend
- **Python 3.x**
- **Flask 3.0.0** - Web-Framework
- **OpenAI API** - KI-gestützte Essensplanung
- **Requests** - HTTP-Bibliothek für API-Aufrufe
- **python-dotenv** - Verwaltung von Umgebungsvariablen

### Frontend
- **HTML5/CSS3**
- **Bootstrap 5.3.0** - UI-Framework
- **JavaScript** - Dynamische Inhalte und API-Interaktion

### Externe APIs
- **TheMealDB API** - Rezeptdatenbank
- **OpenAI GPT-4** - Intelligente Essensplanung

## 📦 Voraussetzungen

Bevor du dieses Projekt ausführst, stelle sicher, dass Folgendes installiert ist:

- Python 3.8 oder höher
- pip (Python Package Manager)
- Ein OpenAI API-Schlüssel (für die KI-Essensplanungsfunktion)

## 🚀 Installation

1. **Repository klonen**
   ```bash
   git clone https://github.com/LukasGogol644/MealPrepHub.git
   cd MealPrepHub
   ```

2. **Virtuelle Umgebung erstellen** (empfohlen)
   ```bash
   python -m venv .venv
   
   # Unter Windows
   .venv\Scripts\activate
   
   # Unter macOS/Linux
   source .venv/bin/activate
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Konfiguration

1. **Erstelle eine `.env` Datei** im Hauptverzeichnis (oder kopiere von `.env.example`, falls vorhanden)

2. **Füge deine API-Schlüssel hinzu**:
   ```env
   # OpenAI API-Schlüssel (erforderlich für KI-Essensplanung)
   OPENAI_API_KEY=dein_openai_api_schlüssel_hier
   
   # TheMealDB API-Schlüssel (kostenlose Version verwendet "1")
   THEMEALDB_API_KEY=1
   
   # Flask-Konfiguration
   FLASK_APP=main.py
   FLASK_ENV=development
   SECRET_KEY=dein_geheimer_schlüssel_hier
   ```

3. **OpenAI API-Schlüssel erhalten**:
   - Besuche [OpenAI Platform](https://platform.openai.com/)
   - Erstelle ein Konto oder melde dich an
   - Navigiere zum Bereich API-Schlüssel
   - Erstelle einen neuen API-Schlüssel
   - Kopiere ihn und füge ihn in deine `.env` Datei ein

## 🎮 Verwendung

1. **Starte den Flask-Entwicklungsserver**:
   ```bash
   python main.py
   ```
   
   Die Anwendung ist unter `http://localhost:5000` verfügbar

2. **Für Produktionsbereitstellung**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```

3. **Navigiere durch die Anwendung**:
   - **Startseite** (`/`) - Rezepte suchen und durchstöbern
   - **KI-Planer** (`/ai-planner`) - KI-gestützte Essenspläne generieren
   - **Wochenplan** (`/week-plan`) - Wöchentliche Essenspläne erstellen und verwalten
   - **Einkaufsliste** (`/shopping-list`) - Einkaufslisten generieren

## 📁 Projektstruktur

```
MealPrepHub/
├── main.py                 # Flask-Anwendung mit allen Routen
├── requirements.txt        # Python-Abhängigkeiten
├── .env                   # Umgebungsvariablen (nicht in Git)
├── templates/             # HTML-Templates
│   ├── index.html        # Startseite
│   ├── ai_planner.html   # KI-Essensplanungsseite
│   ├── week_plan.html    # Wöchentlicher Essensplaner
│   ├── shopping_list.html # Einkaufslistenseite
│   └── recipe_detail.html # Rezeptdetailseite
├── static/               # Statische Dateien
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript-Dateien
└── README.md            # Diese Datei
```

## 🌐 API-Endpunkte

### Rezept-Endpunkte

| Methode | Endpunkt | Beschreibung |
|---------|----------|--------------|
| GET | `/` | Startseite |
| GET | `/api/categories` | Alle Mahlzeitenkategorien abrufen |
| POST | `/api/search` | Rezepte nach Name oder Kategorie suchen |
| GET | `/api/recipe/<meal_id>` | Rezeptdetails nach ID abrufen |
| GET | `/api/random` | Zufälliges Rezept abrufen |
| GET | `/recipe/<meal_id>` | Rezeptdetailseite |

### Planungs-Endpunkte

| Methode | Endpunkt | Beschreibung |
|---------|----------|--------------|
| GET | `/week-plan` | Wöchentliche Essensplanungsseite |
| GET | `/shopping-list` | Einkaufslistenseite |
| GET | `/ai-planner` | KI-Essensplanerseite |
| POST | `/api/generate-ai-plan` | KI-gestützten Essensplan generieren |

### KI-Essensplan Request Body

```json
{
  "goal": "Muskelaufbau",
  "calories": 2500,
  "protein": 150,
  "dietary": "vegetarian"
}
```

**Verfügbare Ziele:**
- Muskelaufbau
- Abnehmen
- Vegan
- Vegetarisch
- Gesund essen
- Energie & Leistung

## 📸 Screenshots

### Startseite
Die Startseite bietet eine Suchleiste, Kategorie-Browsing und zufällige Rezeptentdeckung.

### KI-Essensplaner
Personalisierte wöchentliche Essenspläne basierend auf deinen Zielen, Kalorienzielen und Ernährungspräferenzen.

### Wochenplaner
Organisiere deine Mahlzeiten für die ganze Woche mit Drag-and-Drop-Funktionalität.

### Einkaufsliste
Automatisch generierte Einkaufslisten basierend auf deinem Essensplan.

## 🎓 Universitätsprojekt

Dieses Projekt wurde als Universitätsaufgabe erstellt, um Folgendes zu demonstrieren:
- Webanwendungsentwicklung mit Flask
- RESTful-API-Integration
- KI/ML-Integration (OpenAI GPT-4)
- Frontend-Entwicklung mit modernen Frameworks
- Benutzeroberflächendesign
- Datenverwaltung und Zustandsbehandlung

## 🤝 Beiträge

Dies ist ein Universitätsprojekt, aber Vorschläge und Verbesserungen sind willkommen! Du kannst gerne:
1. Das Repository forken
2. Einen Feature-Branch erstellen
3. Deine Änderungen committen
4. Zum Branch pushen
5. Einen Pull Request öffnen

## 📝 Lizenz

Dieses Projekt wurde für Bildungszwecke als Teil einer Universitätsaufgabe erstellt.

## 👨‍💻 Autor

**Lukas Gogol**
- GitHub: [@LukasGogol644](https://github.com/LukasGogol644)

## 🙏 Danksagungen

- [TheMealDB](https://www.themealdb.com/) - Kostenlose Rezept-API
- [OpenAI](https://openai.com/) - GPT-4 API für intelligente Essensplanung
- [Bootstrap](https://getbootstrap.com/) - Frontend-Framework
- [Flask](https://flask.palletsprojects.com/) - Python-Web-Framework

---

**Mit ❤️ für gesunde Essensplanung erstellt**
