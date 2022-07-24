FROM python:3.9 
ENV API_KEY='your_api_key'
RUN apt-get update
COPY . .
RUN pip install -r requirements.txt
CMD  python main.py -a ${API_KEY}