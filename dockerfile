# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Actualiza pip, setuptools y wheel a versiones compatibles
RUN pip install --upgrade "pip<22" "setuptools<60" "wheel<0.36"

# Instala las dependencias
RUN pip install --no-binary :all: git+https://github.com/areski/python-nvd3.git

# Comando por defecto
CMD ["bash"]
