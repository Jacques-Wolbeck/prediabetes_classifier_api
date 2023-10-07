# Um dockerfile sempre deve começar importando a imagem de base.
# Usamos a palavra-chave 'FROM' para isso.
# Em nosso exemplo, queremos importar a imagem do python.
# Assim, escrevemos 'python' para o nome da imagem

# Base image
FROM python:3.11.4

# set working directory
WORKDIR /app

# Para lançar nosso código em Python, devemos importá-lo em nossa imagem.
# Usamos para isso a palavra-chave 'COPY'.
# O primeiro parâmetro, 'main.py', é o nome do arquivo no host.
# O segundo parâmetro, '/', é o caminho onde colocar o arquivo na imagem.
# Aqui, colocamos o arquivo na pasta raiz da imagem.
# Copy file
COPY main.py /app
COPY requirements.txt /app
COPY model /app/model
COPY ms /app/ms

# Install dependencies
RUN pip install -r requirements.txt

# Precisamos definir o comando para lançar quando rodarmos a imagem.
# Usamos a palavra-chave 'CMD' para isso.
# O comando a seguir executará "uvicorn main:app --host 0.0.0.0 --port 8000".
# Run application
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]