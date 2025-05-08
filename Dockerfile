# Usa imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão do Flask
EXPOSE 8080

# Comando para rodar o bot (ajuste se o seu arquivo principal for diferente)
CMD ["gunicorn", "web:web_app", "--bind", "0.0.0.0:5000"]
