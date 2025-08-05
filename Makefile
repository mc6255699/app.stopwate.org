dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

prod:
	docker compose up --build

down:
	docker compose down


shell:
	docker compose exec web python app/manage.py shell

makemigrations:
	docker compose exec web python manage.py makemigrations

migrate:
	docker compose exec web python manage.py migrate

debug:
	docker compose exec web bash
