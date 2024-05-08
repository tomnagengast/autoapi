import inspect
from typing import List, Optional
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import helpers


class Recipe(BaseModel):
    """
    One Recipe should not have a description.
    """
    id: Optional[UUID] = None
    name: str
    description: Optional[str]

class Meal(BaseModel):
    """
    All Meals have between 2 and 4 related Recipes.
    One Meals should have 1 Recipe.
    """
    id: Optional[UUID] = None
    name: str
    description: str
    recipes: List[Recipe]
    
class MealUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    

API_CONTEXT = f"""
This a meal planning API.
Any /api/{{resource}} list should contain between 5 and 8 records.

Types:
{inspect.getsource(Recipe)}
{inspect.getsource(Meal)}
{inspect.getsource(MealUpdate)}
"""

app = FastAPI()

@app.api_route("/api/{p:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def catch_all(req: Request, p: str, payload: Optional[dict] = None):
    custom = None
    prompt = helpers.build_prompt(req, p, payload, custom)
    print(API_CONTEXT, prompt)
    
    res = helpers.generate_response(API_CONTEXT, prompt)
    return JSONResponse(content=res["data"], status_code=res["code"])
