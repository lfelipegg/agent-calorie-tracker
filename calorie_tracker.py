import os
import requests
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from dotenv import load_dotenv
from datetime import datetime
import asyncio

load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

NUTRIENT_IDS = {
    "calories": 1008,
    "protein": 1003,
    "fat": 1004,
    "carbs": 1005,
    "fiber": 1079,
    "sugar": 2000,
    "sodium": 1093,
    "cholesterol": 1253,
    "calcium": 1087,
    "iron": 1089,
    "potassium": 1092
}

@function_tool
def search_food(query: str) -> dict:
    response = requests.get(
        "https://api.nal.usda.gov/fdc/v1/foods/search",
        params={"query": query, "api_key": USDA_API_KEY, "pageSize": 1}
    )
    return response.json()

@function_tool
def get_nutrition_info(fdc_id: int) -> dict:
    response = requests.get(
        f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}",
        params={"api_key": USDA_API_KEY}
    )
    data = response.json()
    nutrients = {n['nutrient']['id']: n['amount'] for n in data.get('foodNutrients', [])}
    return {
        "food_name": data.get("description"),
        "calories": nutrients.get(NUTRIENT_IDS["calories"]),
        "carbs": nutrients.get(NUTRIENT_IDS["carbs"]),
        "protein": nutrients.get(NUTRIENT_IDS["protein"]),
        "fat": nutrients.get(NUTRIENT_IDS["fat"]),
        "fiber": nutrients.get(NUTRIENT_IDS["fiber"]),
        "sugar": nutrients.get(NUTRIENT_IDS["sugar"]),
        "sodium": nutrients.get(NUTRIENT_IDS["sodium"]),
        "cholesterol": nutrients.get(NUTRIENT_IDS["cholesterol"]),
        "calcium": nutrients.get(NUTRIENT_IDS["calcium"]),
        "iron": nutrients.get(NUTRIENT_IDS["iron"]),
        "potassium": nutrients.get(NUTRIENT_IDS["potassium"])
    }

class NutritionItem(BaseModel):
    food_name: str
    quantity: str
    calories: float = Field(...)
    carbs: float = Field(...)
    protein: float = Field(...)
    fat: float = Field(...)
    fiber: Optional[float] = Field(None)
    sugar: Optional[float] = Field(None)
    sodium: Optional[float] = Field(None)
    cholesterol: Optional[float] = Field(None)
    calcium: Optional[float] = Field(None)
    iron: Optional[float] = Field(None)
    potassium: Optional[float] = Field(None)
    notes: Optional[str] = Field(default=None)

class NutritionSummary(BaseModel):
    items: List[NutritionItem]

def save_nutrition_data(new_items: List[NutritionItem]):
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    date_str = now.strftime("%Y-%m-%d")

    # Write individual file
    individual_filename = f"nutrition_summary_{timestamp_str}.json"
    with open(individual_filename, "w") as f:
        f.write(NutritionSummary(items=new_items).model_dump_json(indent=2))

    # Append to daily summary
    daily_filename = f"daily_nutrition_summary_{date_str}.json"
    if os.path.exists(daily_filename):
        with open(daily_filename, "r") as f:
            daily_data = NutritionSummary.model_validate_json(f.read()).items
    else:
        daily_data = []

    daily_data.extend(new_items)
    with open(daily_filename, "w") as f:
        f.write(NutritionSummary(items=daily_data).model_dump_json(indent=2))

    print(f"Saved: {individual_filename} and updated {daily_filename}")

nutrition_agent = Agent(
    name="NutritionAssistant",
    instructions=(
        "You are a nutrition tracking assistant. Users describe what they ate in natural language. "
        "1. Parse into food items with estimated quantities. "
        "2. Search USDA database using 'search_food'. "
        "3. Retrieve nutrition info using 'get_nutrition_info'. "
        "4. Return a JSON list of food items with fields: food_name, quantity, calories, carbs, protein, fat, and optional fiber, sugar, sodium, cholesterol, calcium, iron, potassium, and notes. "
        "Do NOT include extra commentary, only the JSON list."
        "Do NOT format the JSON output in Markdown or wrap it in triple backticks."
    ),
    tools=[search_food, get_nutrition_info],
    model="gpt-4o-mini"
)

async def main():
    while True:
        user_input = input("Type what you ate (or 'done' to finish): ")
        if user_input.strip().lower() == "done":
            break

        result = await Runner.run(nutrition_agent, user_input)

        try:
            parsed_data = json.loads(result.final_output)
            structured = [NutritionItem(**item) for item in parsed_data]
            save_nutrition_data(structured)
        except Exception as e:
            print("Error parsing model output:", e)
            print("Raw output:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
