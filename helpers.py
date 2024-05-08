import json
import os
from typing import Optional
from uuid import UUID

import openai
from fastapi import Request


def pluck_id(path):
    segments = path.split("/")
    try:
        id = UUID(segments[-1])
        path = "/".join(segments[:-1])
        return id, path
    except ValueError:
        return None, path
        

def build_prompt(
    req: Request, 
    path: str, 
    payload: Optional[dict] = None, 
    custom:  Optional[str] = None
):
    id, path = pluck_id(path)
    
    prompt = f"return the reponse for {req.method} /api/{path}"
    
    if id:
        prompt += f"\nid: {id}"
    if payload:
        prompt += f"\npayload: {payload}"
    if custom:
        prompt += f"\n---\n{custom}"
        
    return prompt


def generate_response(api_context, prompt):
    system_prompt = f"""
    You are a helpful assistant designed to output JSON.
    The JSON should be a valid JSON object.
    The JSON should have the following keys:
    - data: the actual data
    - code: the appropriate HTTP response code based on the request method.
    Here's the context of the full api: {api_context}
    """
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    client = openai.OpenAI()
    
    response = client.chat.completions.create(
      model="gpt-4-turbo",
      # model="gpt-3.5-turbo",
      response_format={ "type": "json_object" },
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
      ],
    )
    
    content = response.choices[0].message.content
    if content is None:
        return {}
    else:
        return json.loads(content)
