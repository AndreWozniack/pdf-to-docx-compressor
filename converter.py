import io
import os
import time
import zipfile
from pdf2docx import Converter
from PIL import Image

PROFILES = {
    "light": {
        "name": "Leve (E-mail / WhatsApp)",
        "max_dim": 1400,
        "quality": 75,
        "desc": "Reduz drasticamente o tamanho mantendo legibilidade ideal para compartilhamento rápido."
    },
    "balanced": {
        "name": "Balanceado (Recomendado)",
        "max_dim": 1800,
        "quality": 85,
        "desc": "Equilíbrio perfeito: fotos com excelente nitidez e tamanho reduzido em até 95%."
    },
    "hd": {
        "name": "Alta Resolução",
        "max_dim": 2400,
        "quality": 92,
        "desc": "Máxima fidelidade visual para impressões ou apresentações formais."
    },
    "original": {
        "name": "Original (Sem Compressão)",
        "max_dim": None,
        "quality": 100,
        "desc": "Mantém as imagens no formato e peso brutos extraídos do PDF."
    }
}


def compress_docx_images(input_docx_path: str, output_docx_path: str, profile_key: str = "balanced") -> int:
    """
    Comprime e otimiza imagens dentro de um arquivo .docx (zip)
    de acordo com o perfil selecionado.
    Retorna o número de imagens otimizadas.
    """
    profile = PROFILES.get(profile_key, PROFILES["balanced"])
    if profile_key == "original":
        if input_docx_path != output_docx_path:
            import shutil
            shutil.copy2(input_docx_path, output_docx_path)
        return 0

    max_dim = profile["max_dim"]
    quality = profile["quality"]
    optimized_count = 0

    temp_out = output_docx_path + ".tmp"

    with zipfile.ZipFile(input_docx_path, "r") as zin:
        with zipfile.ZipFile(temp_out, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.startswith("word/media/"):
                    try:
                        img = Image.open(io.BytesIO(data))
                        needs_rescale = max_dim and max(img.size) > max_dim

                        if needs_rescale:
                            scale = max_dim / max(img.size)
                            new_size = (int(img.size[0] * scale), int(img.size[1] * scale))
                            img = img.resize(new_size, Image.Resampling.LANCZOS)

                        buf = io.BytesIO()
                        # Preserva transparência para imagens PNG com canal alpha
                        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                            img.save(buf, format="PNG", optimize=True)
                        else:
                            if img.mode != "RGB":
                                img = img.convert("RGB")
                            img.save(buf, format="JPEG", quality=quality, optimize=True)

                        data = buf.getvalue()
                        optimized_count += 1
                    except Exception as e:
                        # Em caso de arquivo não-imagem ou corrompido, preserva o dado original
                        pass

                zout.writestr(item, data)

    os.replace(temp_out, output_docx_path)
    return optimized_count


def convert_pdf_to_docx(pdf_path: str, docx_path: str, profile_key: str = "balanced") -> dict:
    """
    Converte um arquivo PDF para DOCX preservando layout e comprimindo imagens.
    """
    start_time = time.time()
    pdf_size = os.path.getsize(pdf_path)

    # 1. Conversão PDF -> DOCX bruto
    temp_docx = docx_path if profile_key == "original" else docx_path + ".raw.docx"
    
    cv = Converter(pdf_path)
    cv.convert(temp_docx, start=0, end=None)
    cv.close()

    raw_docx_size = os.path.getsize(temp_docx)

    # 2. Otimização de imagens se aplicável
    img_count = 0
    if profile_key != "original":
        img_count = compress_docx_images(temp_docx, docx_path, profile_key)
        if os.path.exists(temp_docx):
            try:
                os.remove(temp_docx)
            except OSError:
                pass

    final_size = os.path.getsize(docx_path)
    duration = time.time() - start_time

    saved_bytes = max(0, raw_docx_size - final_size)
    saved_percent = round((saved_bytes / raw_docx_size) * 100, 1) if raw_docx_size > 0 else 0

    return {
        "pdf_size": pdf_size,
        "raw_docx_size": raw_docx_size,
        "final_size": final_size,
        "saved_bytes": saved_bytes,
        "saved_percent": saved_percent,
        "images_optimized": img_count,
        "profile": PROFILES.get(profile_key, PROFILES["balanced"])["name"],
        "duration_seconds": round(duration, 2)
    }
