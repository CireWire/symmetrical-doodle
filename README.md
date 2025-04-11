# Recipe Manager

A Python-based recipe management application that allows home chefs to record, edit, save, delete, and scale their recipes.

## Features

- Create and save new recipes
- Edit existing recipes
- Delete recipes
- Scale recipes to different serving sizes
- Persistent storage of recipes
- User-friendly GUI interface
- Input validation and error handling
- Automatic ingredient scaling

## Requirements

- Python 3.8 or higher
- PyQt6

## Installation

1. Clone this repository or download the source code:
   ```bash
   git clone https://github.com/CireWire/symmetrical-doodle.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python recipe_manager.py
   ```

2. To create a new recipe:
   - Click the "New Recipe" button
   - Enter the recipe name
   - Set the number of servings
   - Enter the ingredients (one per line)
   - Enter the cooking instructions
   - Click "Save Recipe"

3. To edit a recipe:
   - Click on the recipe name in the list on the left
   - Make your changes
   - Click "Save Recipe"

4. To delete a recipe:
   - Select the recipe from the list
   - Click "Delete Recipe"
   - Confirm the deletion

5. To scale a recipe:
   - Select the recipe from the list
   - Change the number of servings
   - Click "Scale Recipe"
   - The ingredient amounts will be automatically adjusted

## File Structure

- `recipe_manager.py` - Main application file
- `requirements.txt` - Project dependencies
- `recipes.json` - Recipe storage file (created automatically)

## Data Storage

Recipes are stored in a JSON file (`recipes.json`) with the following structure:
```json
[
  {
    "name": "Recipe Name",
    "ingredients": "Ingredient list",
    "instructions": "Cooking instructions",
    "servings": 4
  }
]
```

## Error Handling

The application includes several validation checks:
- Empty recipe names are not allowed
- Empty ingredients lists are not allowed
- Empty instructions are not allowed
- Servings must be greater than 0
- Duplicate recipe names are not allowed
- Recipe selection is required for scaling and deletion

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

CireWire

## Acknowledgments

- PyQt6 for the GUI framework
- Python standard library for JSON handling 
