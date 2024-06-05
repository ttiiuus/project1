FROM python:3.12

WORKDIR /bot

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /bot

CMD ["python", "bot.py"]
