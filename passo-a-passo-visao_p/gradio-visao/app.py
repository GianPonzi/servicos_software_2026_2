import os
import gradio as gr 
import requests

ANALISE_URL = os.getenv("ANALISE_URL", "http://analise-service:8081")

def analisa_imagem(imagem_path):
    if imagem_path is None:
        return "Nenhuma imagem enviada"
    nome = os.path.basename(imagem_path)
    with open(imagem_path, "rb") as f:
        files = {"file:" (nome, f, "imagem/png")}
        try:
            r = request.post(f"{ANALISE_URL}/analisar", files=files, timeout=600)
        except requests.RequestException as e:
            return f"Erro de conexao: {e}"
    if r.status_code != 200:
        return f"Erro no servidor: {r.status_code}"
    dados = r.json()
    return f"Rotulo: {dados.get('rotulo')}\nBanco: {dados.get('status_db')}"

demo = gr.Interface(
    fn= analise_imagem,
    inputs = gr.Image(type="filepath", label = "Envie uma imagem"),
    outputs = gr.Textbox(label="Resultado da IA e do banco"),
)

if __name__ == "__main__":
    demo.launch(server_name = "0.0.0.0", server_port)