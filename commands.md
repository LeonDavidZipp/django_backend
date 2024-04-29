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
  docker-compose run --rm app sh -c "python manage.py test"

## superuser
- email: admin@example.com
- password: test1234