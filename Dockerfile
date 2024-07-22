# Use uma imagem base oficial do Python
FROM python:3.8-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Defina a variável de ambiente para produção
ENV FLASK_ENV=production

# Exponha a porta que a aplicação Flask vai rodar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
