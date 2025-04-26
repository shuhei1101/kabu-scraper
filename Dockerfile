FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN rm -rf build dist *.egg-info src/*.egg-info
RUN pip install --no-cache-dir -r requirements.txt

# gitインストール
RUN apt-get update && apt-get install -y git

CMD ["tail", "-f", "/dev/null"]
