# Nutrition Tracker

This project is a terminal-based nutrition tracking assistant that utilizes the USDA FoodData Central API and OpenAI's language models. It helps users log meals in natural language and generates structured nutrition data.

## Features

- Ask the user for food intake in natural language
- Uses a GPT model to parse input and search the USDA nutrition database
- Returns structured nutritional information
- Saves:

  - A timestamped JSON log of each entry
  - A daily cumulative nutrition summary

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Set Up a Virtual Environment (venv)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory with the following keys:

```env
USDA_API_KEY=your_usda_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## Running the Script

```bash
python calorie_tracker.py
```

### Sample Run

```text
Type what you ate (or 'done' to finish): 1 bowl of oatmeal and a banana
Type what you ate (or 'done' to finish): grilled chicken and salad
Type what you ate (or 'done' to finish): done
Saved: nutrition_summary_2025-05-20_19-15-22.json and updated daily_nutrition_summary_2025-05-20.json
```

---

## Output

- `nutrition_summary_<timestamp>.json`: Log of each input entry
- `daily_nutrition_summary_<date>.json`: Aggregated summary of the day

---

## How the Code Works

1. **User Interaction Loop**: The script continuously asks the user what they ate until they type "done".
2. **Language Model Parsing**: Each user input is passed to an OpenAI-powered agent that:

   - Breaks the text into recognizable food items.
   - Uses the USDA API to search and fetch nutritional data.

3. **Pydantic Validation**: The returned data is validated and structured using `Pydantic` models.
4. **File Writing**:

   - An individual log is saved with a timestamped filename.
   - A daily summary is updated or created to cumulatively store all inputs for the day.

5. **Error Handling**: Any issues in parsing or data formatting are caught and displayed without breaking the loop.

---

## Code Overview

### `search_food(query: str) -> dict`

Uses the USDA API to search for a food item based on the given text query. Returns the top search result as a dictionary.

### `get_nutrition_info(fdc_id: int) -> dict`

Fetches detailed nutritional information for a food item using its FoodData Central (FDC) ID. Extracts a subset of useful nutrients from the API response.

### `NutritionItem`

A `Pydantic` model defining the structure for a single food item's nutritional data. It includes required fields like `calories`, `carbs`, and `protein`, and optional fields like `fiber`, `sodium`, and `notes`.

### `NutritionSummary`

A container `Pydantic` model that holds a list of `NutritionItem` entries.

### `save_nutrition_data(new_items: List[NutritionItem])`

Saves two types of files:

- A timestamped JSON file for the current input.
- A daily cumulative file that aggregates all inputs for the same date.

### `nutrition_agent`

An OpenAI-powered agent that is given instructions to:

- Interpret meal descriptions.
- Use registered tools (`search_food`, `get_nutrition_info`) to fetch data.
- Return a JSON list of food items with nutritional values.

### `main()`

Runs an asynchronous loop that:

- Takes user input
- Sends it to the agent
- Parses and validates the response
- Calls `save_nutrition_data()` to persist the data
- Repeats until the user types "done"

---

## Requirements

- Python 3.8+
- API keys for USDA and OpenAI

## License

MIT License

## Author

Luis Felipe Gonzalez Guajardo
