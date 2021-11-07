compose_build:
	@docker-compose -f docker-compose.yml build

compose_up:
	@docker-compose -f docker-compose.yml up

compose_down:
	@docker-compose -f docker-compose.yml down

migrations:
	@docker-compose exec web python manage.py makemigrations

migrate:
	@docker-compose exec web python manage.py migrate

superuser:
	@docker-compose exec web python manage.py createsuperuser

shell:
	@docker-compose exec web python manage.py shell

app:
	@mkdir -p apps/$(name)
	@docker-compose exec web python manage.py startapp $(name) apps/$(name)

bash:
	@docker-compose exec web bash

