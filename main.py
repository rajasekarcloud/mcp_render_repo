from typing import Any, Dict, List, Optional
from mcp.server.mcpserver import MCPServer as FastMCP
import sqlite3
from datetime import datetime, timezone
import requests
import json
import os
import sys
port = int(os.environ.get("PORT", 8000))
mcp = FastMCP("Food Server")
# Adding Port and Host for Deployment

@mcp.tool()
def get_random_recipe() -> str:
    """
    Get a random recipe from TheMealDB.

    Returns:
        JSON string with random recipe information
    """
    try:
        base_url = "https://www.themealdb.com/api/json/v1/1"
        search_url = f"{base_url}/random.php"

        response = requests.get(search_url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("meals"):
            return "No random recipe found"

        meal = data["meals"][0]

        # Extract ingredients
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ingredient and ingredient.strip():
                ingredients.append(
                    {
                        "ingredient": ingredient.strip(),
                        "measure": measure.strip() if measure else "",
                    }
                )

        recipe_info = {
            "id": meal.get("idMeal"),
            "name": meal.get("strMeal", "Unknown"),
            "cuisine": meal.get("strArea", "Unknown"),
            "category": meal.get("strCategory", "Unknown"),
            "instructions": meal.get("strInstructions", "No instructions available"),
            "image_url": meal.get("strMealThumb", ""),
            "youtube_url": meal.get("strYoutube", ""),
            "source_url": meal.get("strSource", ""),
            "ingredients": ingredients,
            "tags": meal.get("strTags", "").split(",") if meal.get("strTags") else [],
        }

        return json.dumps(recipe_info, indent=2)

    except requests.RequestException as e:
        return f"Error getting random recipe: {str(e)}"
    except Exception as e:
        return f"Error in get_random_recipe: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
