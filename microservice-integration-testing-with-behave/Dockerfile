FROM python:3.7.4

WORKDIR /app
COPY ./requirements.txt ./
COPY ./time_in_timezone.py ./
RUN pip install -r requirements.txt

EXPOSE 9000
CMD ["python", "time_in_timezone.py"]
