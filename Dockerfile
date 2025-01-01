FROM  ultralytics/ultralytics:8.3.3-python

RUN mkdir build

WORKDIR /build

COPY . .

RUN pip install -r requirements.txt

EXPOSE 9003

CMD [ "python", "/build/main.py"]
