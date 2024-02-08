#!/usr/bin/env python3

from fastapi import FastAPI, requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image
from app import schemas
import uvicorn, os, aiofiles, json
from typing import Optional
from app.s3_acces.get_travel_image import FilesAWSS3

app = FastAPI(
    title="API Travel360    ",
    description="API Travel360 para la generación de viajes personalizados a partir de etiquetas y gestión de usuarios BBDD y mucho más\n\n![logo app](http://apitravel360.homes/logo_app)",
    openapi_url="/openapi.json"
)

# Define cores
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://paumateu.top/",
    "http://apitravel360.homes/",
    "http://185.254.206.129/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Luego si quiero puedo especificar los orígenes exactos en la production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="files"), name="files") # Set static files

# Call classes
image_handler = FilesAWSS3()


############# API ENDPOINTS DEFINITION ################################
@app.get("/", include_in_schema=False)
async def root():
    return {"response":"under construction"}


@app.post("/v1/registrar_usuario", description="", tags=["Aplicación Android"])
async def crear_usuario(user_boddy: schemas.UserCreate):
    return {"response":"under construction"}

@app.post("/v1/login_usuario", description="", tags=["Aplicación Android"])
async def login_usuario(user_boddy: schemas.UserLogin):
    return {"response": "under contruction"}

@app.post("/v1/crear_ticket_ayuda", description="definir schema (id, email[que pone el usuario], asunto, descripción)", tags=["Aplicación Android"])
async def cargar_ticket_ayuda():
    return {"response":"under construction"}

@app.post("/v1/crear_viaje", description="define schema from given tags", tags=["Aplicación Android"])
async def crear_viaje():
    return {"response":"under construction"}

@app.get("/v1/cargar_viajes", include_in_schema=False)
@app.get("/v1/cargar_viajes/{numero_de_viajes}", description="Definición de la pantalla principal y los viajes principales", tags=["Aplicación Android"])
async def crear_viaje(numero_de_viajes: Optional[str] = 8):
    # At this moment, this endpoint will return this
    path = os.path.join(os.path.dirname(__file__), 'JSONS', 'json_prueba.json')
    async with aiofiles.open(path, 'r') as f:
        content = await f.read()

    return JSONResponse(json.loads(content))


# ----


@app.get("/v1/obtener_todos_los_datos_usuario", description="", tags=["Aplicación de escritorio"])
async def obtener_datos():
    return {"response": "under construction"}

@app.get("/v1/cargar_datos_usuario", description="", tags=["Aplicación de escritorio"])
async def get_all_users():
    return {"response":"under construction"}

@app.get("/v1/recivir_tiquets_ayuda", description="", tags=["Aplicación de escritorio"])
async def get_all_tickets():
    return {"response":"under construction"}

@app.get("/v1/recivir_detalles_tiket/{id}", description="", tags=["Aplicación de escritorio"])
async def get_tiket_details():
    return {"response": "under construction"}

@app.post("/v1/responder_tiquet_ayuda", description="", tags=["Aplicación de escritorio"])
async def response_tiquets():
    return {"response":"under construction"}
    
@app.put("/v1/cerrar_tiquet_ayuda/{id}", description="", tags=["Aplicación de escritorio"])
async def close_help_ticket(id: str):

    
    return {"response":"under construction"}


################ ANOTHER THINGS ####################################

@app.get("/logo_app", include_in_schema=False)
async def logo_app():
    original_path = os.path.join(os.path.dirname(__file__), 'files', 'logo_app.png')
    original_image = Image.open(original_path)
    new_width = 200  
    new_height = int(original_image.height * (new_width / original_image.width))
    resized_image = original_image.resize((new_width, new_height))
    resized_path = os.path.join(os.path.dirname(__file__), 'files', 'logo_app_resized.png')
    resized_image.save(resized_path)
    
    return FileResponse(resized_path)

from fastapi.responses import Response, PlainTextResponse

@app.get("/images/{image_name}", include_in_schema=False)
async def get_image_response(image_name: str):
    try:
        image_content = image_handler.get_image(image_name)
        if image_content:
            # Directly read the image bytes since we adjusted the get_image function to read the body
            return Response(content=image_content, media_type="image/png")  # media_type adjusted to 'image/png'
        else:
            # In the future return a default image 
            return PlainTextResponse("Image not found or error occurred", status_code=404)
    except Exception as e:
        # It's a good practice to log the exception here
        # In the future return a default image 
        return PlainTextResponse(f"An error occurred: {e}", status_code=500)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "0.0.0.0",
        port=80,
        reload=True
    )
