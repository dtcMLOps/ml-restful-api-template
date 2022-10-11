FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
# ENV DB_USERNAME DB_PASSWORD DB_HOST DB_NAME DB_PORT
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y netcat && pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --use-deprecated=legacy-resolver -r /code/requirements.txt
COPY . /code
EXPOSE 3100
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
