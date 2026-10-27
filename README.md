# PDF to DOCX Smart Compressor 📄➡️📝

Um aplicativo web local simples, rápido e elegante para converter documentos **PDF complexos em Microsoft Word (.docx)** com **fidelidade visual de diagramação** e **compressão inteligente de imagens**.

Desenvolvido para resolver o problema clássico de conversores PDF -> DOCX (como Pandoc ou conversores simples) que:
1. Perdem margens, capas, caixas e tabelas; OU
2. Extraem imagens brutas não comprimidas, gerando arquivos `.docx` gigantescos (de centenas de megabytes).

---

## 🚀 Principais Recursos

- **Preservação de Layout Visual:** Utiliza o motor avançado do `pdf2docx` (baseado em PyMuPDF) para reconstruir textos, tabelas, caixas, fotos e paginação.
- **Compressão Inteligente de Fotos:** Otimiza e redimensiona imagens internas do documento Word, reduzindo o tamanho em até **95% a 98%** sem perda perceptível de nitidez.
- **Perfis de Compressão Selecionáveis:**
  - ⚖️ **Balanceado (Recomendado):** máx. 1800px, 85% de qualidade (reduz centenas de MB para ~10-25 MB).
  - ⚡ **Leve:** máx. 1400px, 75% de qualidade (perfeito para envio por WhatsApp e e-mail).
  - 🎨 **Alta Resolução:** máx. 2400px, 92% de qualidade (ideal para impressão de alta fidelidade).
  - 📦 **Sem Compressão:** Mantém as imagens originais intactas.
- **Interface Drag & Drop Moderna:** Arraste e solte o PDF, escolha o perfil e acompanhe a conversão com estatísticas do tamanho antes e depois.
- **100% Local e Seguro:** Nenhum arquivo é enviado para a nuvem. Todo o processamento ocorre na sua própria máquina.

---

## 🛠️ Instalação e Execução

### Opção 1: Clique Duplo no macOS (Mais Fácil)
Basta dar um duplo-clique no arquivo executável:
```bash
iniciar.command
```
Ele criará o ambiente virtual automaticamente, instalará as dependências e abrirá o navegador em `http://localhost:5055`.

---

### Opção 2: Pelo Terminal

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/AndreWozniack/pdf-to-docx-compressor.git
   cd pdf-to-docx-compressor
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale os requisitos:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o aplicativo:**
   ```bash
   python app.py
   ```
   Acesse no navegador: **[http://localhost:5055](http://localhost:5055)**

---

## 📦 Tecnologias Utilizadas

- **[Python 3](https://www.python.org/)**
- **[Flask](https://flask.palletsprojects.com/)** (Servidor web local)
- **[pdf2docx](https://dothinking.github.io/pdf2docx/)** (Reconstrução estrutural de layout)
- **[Pillow (PIL)](https://python-pillow.org/)** (Compressão e redimensionamento de imagens)
- **HTML5 / CSS3 / JavaScript moderno** (Interface nativa sem dependências de build)

---

## 📄 Licença

MIT License &copy; 2026 André Wozniack.
