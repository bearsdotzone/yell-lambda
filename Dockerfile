FROM python:3
COPY lambda.py .
RUN pip install requests
EXPOSE 8080
CMD python3 lambda.py