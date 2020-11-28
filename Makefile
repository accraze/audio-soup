export PG_USERNAME=audiosoup
export PG_PASSWORD=1234
export PG_DATABASE=audiosoup
export PG_CONNECTION_URI=postgres://$(PG_USERNAME):$(PG_PASSWORD)@postgres/$(PG_DATABASE)
export FLASK_APP=src.app

start:
	docker-compose up --build

db-schema:
	docker exec -i postgres psql $(PG_CONNECTION_URI) -t < scripts/db-schema.sql

psql:
	docker exec -it postgres psql $(PG_CONNECTION_URI)

test:
	docker exec -it audiosoup-app sh -c "python -m pytest --disable-pytest-warnings"

migrate:
	docker exec -it audiosoup-app sh -c "cd /src/ && python -m flask db migrate"

upgrade:
	docker exec -it audiosoup-app sh -c "cd /src/ && python -m flask db upgrade"

seed:
	docker exec -it audiosoup-app sh -c "cd /src/ && python -m flask load-dataset -p 'static/dataset/' -n 'foo' -u 'foo.com'"
