from fastapi import FastAPI
from routers import pet_types, pets, pictures

app = FastAPI(title="Pet Store Inventory API")

# Include routers
app.include_router(pet_types.router)
app.include_router(pets.router)
app.include_router(pictures.router)

@app.get("/")
def read_root():
    return {"message": "Pet Store Inventory API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)