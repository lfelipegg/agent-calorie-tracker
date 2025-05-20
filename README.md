Here’s a `README.md` you can use for your nutrition tracking agent project:

---

````markdown
# 🥗 Nutrition Tracking Assistant

This project implements a nutrition tracking assistant using the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) and the USDA FoodData Central API. It allows users to input meals in natural language and receive a structured nutritional breakdown of the food items they consumed.

## 🚀 Features

- Parses natural language meal descriptions
- Identifies food items and estimates quantities
- Queries USDA FoodData Central API for precise nutrition data
- Returns structured output including:
  - Calories
  - Macronutrients (Carbs, Protein, Fat)
  - Micronutrients (Fiber, Sugar, Sodium, Cholesterol, Calcium, Iron, Potassium)
- Saves results to a JSON file

## 🧠 Built With

- Python 3.10+
- [OpenAI Agents SDK](https://pypi.org/project/openai-agents/)
- Pydantic v2
- USDA FoodData Central API

## 📦 Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
```
````

2. Install dependencies:

```bash
pip install openai-agents requests
```

3. Set your USDA API key:

```bash
export USDA_API_KEY=your_api_key_here  # or use dotenv/put in env variables on Windows
```

## 🧪 Running the Agent

Run the script:

```bash
python calorie_tracker.py
```

You will see the agent parse the input and return detailed nutritional data. It will also save the result in `nutrition_summary.json`.

## 📂 Example Output

```json
{
  "items": [
    {
      "food_name": "Oatmeal (1 bowl)",
      "quantity": "1 bowl",
      "calories": 150.0,
      "carbs": 27.0,
      "protein": 5.0,
      "fat": 3.0,
      "fiber": 4.0,
      "sugar": 1.0,
      "sodium": 0.0,
      "cholesterol": 0.0,
      "calcium": 20.0,
      "iron": 1.5,
      "potassium": 150.0,
      "notes": "General estimate for plain oatmeal."
    },
    ...
  ]
}
```

## 📌 Notes

- Make sure your USDA API key is active and valid.
- The model will estimate serving sizes if not specified.
- All nutrition data is based on USDA records.
