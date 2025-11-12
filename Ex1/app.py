from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import pet_types, pets, pictures

app = FastAPI(title="Pet Store Inventory API")

# Include routers
app.include_router(pet_types.router)
app.include_router(pets.router)
#app.include_router(pictures.router)

@app.get("/")
def read_root():
    return {"message": "Pet Store Inventory API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5001)