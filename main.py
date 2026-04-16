from datetime import datetime
from random import randint
from typing import Any
from fastapi import FastAPI, HTTPException, Response

app = FastAPI(root_path="/api/v1")

data: list[Any] = [
    {
        "campaign_id": 1,
        "name": "test",
        "due_date":datetime.now(),
        "created_at": datetime.now()
    },
    {
        "campaign_id": 2,
        "name": "let's go",
        "due_date":datetime.now(),
        "created_at": datetime.now()
    }
    ]

@app.get("/")
async def root():
    return {"message": "hello my first firstapi"}

@app.get('/campaigns')
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: int):
    for campaign in data:
        if campaign.get('campaign_id') == campaign_id:
         return {"campaign": campaign}
        
    raise HTTPException( status_code=404)

@app.post("/campaigns", status_code=201)
async def create_campaign(body : dict[str, Any]): 
   name : Any = body.get("name")
   if not name:
      raise HTTPException(status_code=400, detail="name is required")
   new : Any = {
        "campaign_id": body.get("campaign_id") or randint(1000, 9999),
        "name": body['name'],
        "due_date":body.get("due_date"),
        "created_at": datetime.now() 
   }

   data.append(new)
   return {"campaign": new}

@app.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: int, body: dict[str, Any]):
   for index, campaign in enumerate(data):
     if campaign.get('campaign_id') == campaign_id:
        updated : Any = {
            "campaign_id": campaign_id,
            "name": body.get("name"),
            "due_date":body.get("due_date"),
            "created_at": campaign.get("created_at")
        }

        data[index] = updated
        return{"campaign": updated}
   raise HTTPException(status_code=404, detail="campaign not found")

@app.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int):
   for index, campaign in enumerate(data):
     if campaign.get('campaign_id') == campaign_id:
        data.pop(index)
        return Response(status_code=204)
   raise HTTPException(status_code=404, detail="campaign not found")