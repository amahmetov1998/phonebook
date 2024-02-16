venv:
	python3 -m venv venv && source venv/bin/activate

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations && python manage.py migrate

load_data:
	python manage.py loaddata contacts.json

shell:
	python manage.py shell_plus