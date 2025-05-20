import os
import requests
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from dotenv import load_dotenv
load_dotenv()
# Environment variable for the USDA API Key
USDA_API_KEY = os.getenv("USDA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Nutrient ID map for USDA API
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

# Tool: Search food items using USDA API
@function_tool
def search_food(query: str) -> dict:
    response = requests.get(
        "https://api.nal.usda.gov/fdc/v1/foods/search",
        params={"query": query, "api_key": USDA_API_KEY, "pageSize": 1}
    )
    return response.json()

# Tool: Get nutrition info for a specific FDC ID
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

# Structured output for the agent
class NutritionItem(BaseModel):
    food_name: str
    quantity: str
    calories: float = Field(..., description="Estimated calories")
    carbs: float = Field(..., description="Grams of carbohydrates")
    protein: float = Field(..., description="Grams of protein")
    fat: float = Field(..., description="Grams of fat")
    fiber: Optional[float] = Field(None, description="Grams of fiber")
    sugar: Optional[float] = Field(None, description="Grams of sugar")
    sodium: Optional[float] = Field(None, description="Milligrams of sodium")
    cholesterol: Optional[float] = Field(None, description="Milligrams of cholesterol")
    calcium: Optional[float] = Field(None, description="Milligrams of calcium")
    iron: Optional[float] = Field(None, description="Milligrams of iron")
    potassium: Optional[float] = Field(None, description="Milligrams of potassium")
    notes: Optional[str] = Field(description="Any estimation notes")

class NutritionSummary(BaseModel):
    items: List[NutritionItem]

# Agent definition
# Agent definition WITHOUT output_type
nutrition_agent = Agent(
    name="NutritionAssistant",
    instructions=(
        "You are a nutrition tracking assistant. Users describe what they ate in natural language. "
        "1. Parse into food items with estimated quantities. "
        "2. Search USDA database using 'search_food'. "
        "3. Retrieve nutrition info using 'get_nutrition_info'. "
        "4. Return a JSON list of food items with fields: food_name, quantity, calories, carbs, protein, fat, and optional fiber, sugar, sodium, cholesterol, calcium, iron, potassium, and notes. "
        "Example format: [{\"food_name\": \"Banana\", \"quantity\": \"1 medium\", \"calories\": 105, \"carbs\": 27, ...}]. "
        "Do NOT include extra commentary, only the JSON list."
        "Do NOT format the JSON output in Markdown or wrap it in triple backticks."

    ),
    tools=[search_food, get_nutrition_info],
    model="gpt-4o-mini"  # You can use gpt-4-turbo or gpt-3.5 here too
)

# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        user_input = "I had a bowl of oatmeal with banana and a cup of coffee with cream."
        result = await Runner.run(nutrition_agent, user_input)

        try:
            # Attempt to parse the LLM's plain JSON string output into structured Pydantic objects
            parsed_data = json.loads(result.final_output)
            structured = NutritionSummary(items=[NutritionItem(**item) for item in parsed_data])
        except Exception as e:
            print("Error parsing model output:", e)
            print("Raw output:", result.final_output)
            return

        # Show parsed structure
        print(structured)

        # Save to JSON file
        with open("nutrition_summary.json", "w") as f:
            f.write(structured.model_dump_json(indent=2))

    asyncio.run(main())
