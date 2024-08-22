from fastapi import FastAPI, Depends
from web.routers.image import router as image_router
from service.image_service import ImageService
from service.image_service_interface import ImageServiceInterface
app = FastAPI()

app.include_router(image_router, tags=["image"])
@app.on_event("startup")
def startup_event():
    app.state.image_service = ImageService()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# def get_image_content(guid: str, service: ImageServiceInterface = Depends(lambda: app.state.image_service)):
@app.get("/kumar/shekhar", summary="Retrieve an image file by GUID.")
def get_shekhar(service: ImageServiceInterface = Depends(lambda: app.state.image_service)):
    print("i am working")
    return service.getShekhar()


