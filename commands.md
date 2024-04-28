## important commands
- Build all images from docker-compose file:
  docker-compose build
- Run server:
  docker-compose up
- Kill all containers from docker-compose file:
  docker-compose down
- Create a new subapp:
  docker-compose run --rm app sh -c "python manage.py startapp 'appname'"
- Run tests:
  docker-compose run --rm app sh -c "python manage.py tests"

## superuser
- email: leondavidzipp@gmx.de
- password: test1234