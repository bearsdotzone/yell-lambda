FROM python:3
COPY test.py .
RUN pip install requests
EXPOSE 8080
CMD python3 test.py