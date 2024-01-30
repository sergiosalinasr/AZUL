FROM python:3.9.18-alpine3.18

WORKDIR /usr

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/app.py" ]