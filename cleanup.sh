#!/bin/bash

echo "🔧 Cleaning and organizing project structure..."

# Create folders
mkdir -p core/diagnostics core/formatter core/imap gui config utils tests
mkdir -p app/static app/templates

# Move diagnostic and formatter files
mv diagnostics/*.py core/diagnostics/
mv formatter/*.py core/formatter/
rm -r diagnostics formatter

# Move GUI
mv gui_app.py gui/

# Move config
mv .env config/

# Move templates and CSS (ensure they exist)
[ -f email_preview.html ] && mv email_preview.html app/templates/
[ -f style.css ] && mv style.css app/static/

# Remove __pycache__ everywhere
find . -type d -name "__pycache__" -exec rm -r {} +

# Create init files where needed
touch core/__init__.py
touch core/diagnostics/__init__.py
touch core/formatter/__init__.py
touch core/imap/__init__.py
touch gui/__init__.py
touch utils/__init__.py
touch tests/__init__.py

# Update import paths (example: diagnostics → core.diagnostics)
echo "🛠 Updating import paths..."
find app -type f -name "*.py" -exec sed -i 's/from diagnostics/from core.diagnostics/g' {} +
find app -type f -name "*.py" -exec sed -i 's/from formatter/from core.formatter/g' {} +
find main.py -type f -exec sed -i 's/from diagnostics/from core.diagnostics/g' 2>/dev/null
find main.py -type f -exec sed -i 's/from formatter/from core.formatter/g' 2>/dev/null

# Final touch
echo "✅ Project cleaned and reorganized!"
