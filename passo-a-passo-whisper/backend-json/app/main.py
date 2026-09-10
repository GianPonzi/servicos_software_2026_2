import os 
import shutil
from unittest import result
import whisper

from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Serviço de Transcrição")

print("Carregando modelo Whisper...")
model = whisper.load_model("base")
print("Modelo carregado!")


@app.get("/")
def status():
    return {"status": "ok"}

@app.post("/transcrever")
async def transcrever_audio(file: UploadFile = File(...)):
    caminho = f'/tmp/{file.filename}'
    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resultado = model.transcribe(caminho, language="pt")
        texto = resultado["text"].strip()
    finally:
        if os.path.exists(caminho):
            os.remove(caminho)
    return {"texto": texto}
