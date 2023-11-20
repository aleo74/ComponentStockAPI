FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PORT 50001
EXPOSE 50001
EXPOSE 27017

CMD ["python", "-u", "run.py"]