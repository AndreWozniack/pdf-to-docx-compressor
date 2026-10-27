import os
import time
import uuid
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from converter import convert_pdf_to_docx, PROFILES

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
CONVERTED_FOLDER = os.path.join(BASE_DIR, "converted")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Limite máximo de arquivo: 500 MB
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024


def cleanup_old_files(max_age_seconds: int = 3600):
    """Remove arquivos com mais de 1 hora para economizar disco."""
    now = time.time()
    for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER]:
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            if os.path.isfile(fpath) and (now - os.path.getmtime(fpath)) > max_age_seconds:
                try:
                    os.remove(fpath)
                except OSError:
                    pass


@app.route("/")
def index():
    cleanup_old_files()
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "pdf" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"error": "Nome de arquivo inválido."}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Apenas arquivos .pdf são suportados."}), 400

    profile = request.form.get("profile", "balanced")
    if profile not in PROFILES:
        profile = "balanced"

    orig_name = os.path.splitext(secure_filename(file.filename))[0] or "documento"
    unique_id = uuid.uuid4().hex[:8]
    pdf_filename = f"{orig_name}_{unique_id}.pdf"
    docx_filename = f"{orig_name}_{unique_id}.docx"

    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    docx_path = os.path.join(CONVERTED_FOLDER, docx_filename)

    file.save(pdf_path)

    try:
        stats = convert_pdf_to_docx(pdf_path, docx_path, profile)
        user_download_name = f"{orig_name}_otimizado.docx"

        response_data = {
            **stats,
            "output_filename": docx_filename,
            "download_name": user_download_name
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": f"Falha na conversão: {str(e)}"}), 500
    finally:
        # Remove PDF de upload para liberar espaço
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except OSError:
                pass


@app.route("/download/<path:filename>")
def download(filename):
    safe_name = os.path.basename(filename)
    file_path = os.path.join(CONVERTED_FOLDER, safe_name)
    if not os.path.exists(file_path):
        return jsonify({"error": "Arquivo não encontrado ou expirado."}), 404

    # Nome limpo para o download do usuário
    clean_name = safe_name.split("_")[0] + ".docx"
    return send_file(file_path, as_attachment=True, download_name=clean_name)


def open_browser():
    webbrowser.open_new("http://localhost:5055")


if __name__ == "__main__":
    print("=" * 60)
    print("  Conversor PDF -> Word com Compressão Inteligente")
    print("  Acesse no navegador: http://localhost:5055")
    print("=" * 60)
    Timer(1.2, open_browser).start()
    app.run(host="0.0.0.0", port=5055, debug=False)
