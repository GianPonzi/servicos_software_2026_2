# from werkzeug.datastructures import FileStorage
# from werkzeug.wrappers import response
import gradio as gr
import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8080")

def processar_audio(audio_path):
    if audio_path is None:
        return "Nenhum audio recebido"
    
    with open(audio_path, "rb") as f:
        files = {"file": ("audio.wav", f, "audio/wav")}
        
        try:
            response = requests.post("http://backend-json:8080/transcrever", files=files)
            if response.status_code == 200:
                return response.json().get("texto", "Eerro ao extrair texto")
            else:
                return f"Erro no servidor: {response.status_code}"
        except Exception as e:
            return f"Erro ao conectar ao servidor: {str(e)}"


demo = gr.Interface(
    fn=processar_audio, 
    inputs=gr.Audio(type="filepath", label="Grave sua voz"),
    outputs= gr.Textbox(label="Texto transcrito"),
    title="Assistente de voz com IA",
    description="Grave sua voz e clique em 'Transcrever' para ver o texto"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)