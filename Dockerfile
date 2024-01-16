FROM python:3.7
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "-u", "./app.py" ]