from generate_csv.celery import app

from .views import generate_csv

@app.task
def generate_fake_csv():
    generate_csv()