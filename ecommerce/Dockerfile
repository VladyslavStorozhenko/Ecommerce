FROM        python:3.10

LABEL       author="Vlad Storozhenko"



WORKDIR     /app
COPY        ./ecommerce/requirements.txt .
RUN         pip install -r requirements.txt

COPY        . .

ENV         PYTHONPATH="${PYTHONPATH}:/app/ecommerce"