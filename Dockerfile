FROM python:3.8
ADD main.py .
RUN pip install walrus
CMD ["python", "./main.py"]
