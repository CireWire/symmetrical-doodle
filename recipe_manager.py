#!/usr/bin/env python3
"""
Recipe Manager - A GUI application for managing cooking recipes

This application allows users to create, edit, save, delete and scale recipes.
It provides a user-friendly interface built with PyQt6 for home chefs to
manage their recipe collection.

Author: CireWire
License: MIT
"""


import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLineEdit, QTextEdit, 
                            QListWidget, QLabel, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt

class Recipe:
    def __init__(self, name="", ingredients="", instructions="", servings=1):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.servings = servings

class RecipeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.recipes = []
        self.current_recipe = None
        self.initUI()
        self.load_recipes()

    def initUI(self):
        self.setWindowTitle('Recipe Manager')
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Left panel - Recipe list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.recipe_list = QListWidget()
        self.recipe_list.itemClicked.connect(self.select_recipe)
        left_layout.addWidget(QLabel("Recipes:"))
        left_layout.addWidget(self.recipe_list)

        # New recipe button
        new_recipe_button = QPushButton("New Recipe")
        new_recipe_button.clicked.connect(self.new_recipe)
        left_layout.addWidget(new_recipe_button)

        # Right panel - Recipe details
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Recipe name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Recipe Name:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        right_layout.addLayout(name_layout)

        # Servings
        servings_layout = QHBoxLayout()
        servings_layout.addWidget(QLabel("Servings:"))
        self.servings_spin = QSpinBox()
        self.servings_spin.setRange(1, 100)
        servings_layout.addWidget(self.servings_spin)
        right_layout.addLayout(servings_layout)

        # Ingredients
        right_layout.addWidget(QLabel("Ingredients:"))
        self.ingredients_edit = QTextEdit()
        right_layout.addWidget(self.ingredients_edit)

        # Instructions
        right_layout.addWidget(QLabel("Instructions:"))
        self.instructions_edit = QTextEdit()
        right_layout.addWidget(self.instructions_edit)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Recipe")
        self.save_button.clicked.connect(self.save_recipe)
        self.delete_button = QPushButton("Delete Recipe")
        self.delete_button.clicked.connect(self.delete_recipe)
        self.scale_button = QPushButton("Scale Recipe")
        self.scale_button.clicked.connect(self.scale_recipe)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.scale_button)
        right_layout.addLayout(button_layout)

        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)

    def load_recipes(self):
        try:
            with open('recipes.json', 'r') as f:
                data = json.load(f)
                self.recipes = [Recipe(**recipe) for recipe in data]
                self.update_recipe_list()
        except FileNotFoundError:
            self.recipes = []

    def save_recipes(self):
        with open('recipes.json', 'w') as f:
            json.dump([vars(recipe) for recipe in self.recipes], f)

    def update_recipe_list(self):
        self.recipe_list.clear()
        for recipe in self.recipes:
            self.recipe_list.addItem(recipe.name)

    def select_recipe(self, item):
        recipe_name = item.text()
        for recipe in self.recipes:
            if recipe.name == recipe_name:
                self.current_recipe = recipe
                self.name_edit.setText(recipe.name)
                self.servings_spin.setValue(recipe.servings)
                self.ingredients_edit.setText(recipe.ingredients)
                self.instructions_edit.setText(recipe.instructions)
                break

    def save_recipe(self):
        name = self.name_edit.text().strip()
        ingredients = self.ingredients_edit.toPlainText().strip()
        instructions = self.instructions_edit.toPlainText().strip()
        servings = self.servings_spin.value()

        if not name:
            QMessageBox.warning(self, "Error", "Recipe name cannot be empty!")
            return
        
        if not ingredients:
            QMessageBox.warning(self, "Error", "Ingredients cannot be empty!")
            return

        if not instructions:
            QMessageBox.warning(self, "Error", "Instructions cannot be empty!")
            return

        if servings <= 0:
            QMessageBox.warning(self, "Error", "Servings must be greater than 0!")
            return

        # Check for duplicate names (only for new recipes)
        if not self.current_recipe and any(r.name == name for r in self.recipes):
            QMessageBox.warning(self, "Error", "A recipe with this name already exists!")
            return

        if self.current_recipe:
            # Update existing recipe
            self.current_recipe.name = name
            self.current_recipe.servings = servings
            self.current_recipe.ingredients = ingredients
            self.current_recipe.instructions = instructions
        else:
            # Create new recipe
            new_recipe = Recipe(
                name=name,
                servings=servings,
                ingredients=ingredients,
                instructions=instructions
            )
            self.recipes.append(new_recipe)
            self.current_recipe = new_recipe

        self.save_recipes()
        self.update_recipe_list()
        QMessageBox.information(self, "Success", "Recipe saved successfully!")

    def delete_recipe(self):
        if not self.current_recipe:
            return

        reply = QMessageBox.question(self, 'Confirm Delete',
                                   'Are you sure you want to delete this recipe?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.recipes.remove(self.current_recipe)
            self.current_recipe = None
            self.clear_form()
            self.save_recipes()
            self.update_recipe_list()

    def scale_recipe(self):
        if not self.current_recipe:
            QMessageBox.warning(self, "Error", "Please select a recipe first!")
            return

        if self.current_recipe.servings <= 0:
            QMessageBox.warning(self, "Error", "Original recipe must have at least 1 serving!")
            return

        current_servings = self.servings_spin.value()
        original_servings = self.current_recipe.servings
        scale_factor = current_servings / original_servings

        # Scale ingredients
        ingredients = self.ingredients_edit.toPlainText()
        scaled_ingredients = []
        for line in ingredients.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                # Improved number detection
                parts = line.split()
                first_part = parts[0].replace('.', '').replace(',', '')
                if first_part.isdigit() or (first_part.startswith('-') and first_part[1:].isdigit()):
                    amount = float(parts[0].replace(',', '')) * scale_factor
                    scaled_ingredients.append(f"{amount:.2f} {' '.join(parts[1:])}")
                else:
                    scaled_ingredients.append(line)
            except (IndexError, ValueError):
                scaled_ingredients.append(line)
        
        self.ingredients_edit.setText('\n'.join(scaled_ingredients))
        self.current_recipe.servings = current_servings

    def clear_form(self):
        self.name_edit.clear()
        self.servings_spin.setValue(1)
        self.ingredients_edit.clear()
        self.instructions_edit.clear()

    def new_recipe(self):
        self.current_recipe = None
        self.clear_form()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RecipeManager()
    ex.show()
    sys.exit(app.exec()) 
