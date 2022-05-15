WEB=`docker-compose ps | grep gunicorn | cut -d\  -f 1 | head -n 1`
WEBS=`docker-compose ps | grep gunicorn | cut -d\  -f 1 `
FILE=docker-compose.yml
BACKUPS_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../backups/)
ENV_STAGE = ``

#########
#ACTIONS#
#########

build:
	docker-compose -f $(FILE) build

up:
	docker-compose -f $(FILE) up -d

start:
	docker-compose -f $(FILE) start

stop:
	docker-compose -f $(FILE) stop

ps:
	docker-compose -f $(FILE) ps
	@echo "---------------------------"
	@echo "Web:     `ps aux | grep /usr/local/bin/gunicorn | grep -v grep | wc -l` threads running"

clean: stop
	docker-compose -f $(FILE) rm -f

restart: clean build up ps
	@echo "Restarted all containers"

########
#SHELLS#
########

shell-nginx:
	docker exec -ti grafana-wallet-nginx bash

shell-web:
	docker exec -ti $(WEB) bash

shell-db:
	docker exec -ti grafana-wallet-postgres bash

shell-grafana:
	docker exec -ti grafana-wallet-web bash

shell-celeryw:
	docker exec -ti grafana-wallet-celeryworker bash

shell-celeryb:
	docker exec -ti grafana-wallet-celerybeat bash

######
#LOGS#
######

log-nginx:
	docker-compose logs nginx

log-web:
	docker-compose logs web

log-web-live:
	docker logs --tail 50 --follow --timestamps $(WEB)

log-grafana:
	docker-compose logs grafana-wallet-web

log-grafana-live:
	docker logs --tail 50 --follow --timestamps grafana-wallet-web

log-db:
	docker-compose logs db

log-celeryw:
	docker-compose logs celeryworker

log-celeryb:
	docker-compose logs celerybeat

############
#DJANGO OPS#
############

collectstatic:
	@echo $(shell for container in $(WEBS); do\
		docker exec $$container /bin/sh -c "python manage.py collectstatic --noinput" ;\
	done)

migrate:
	docker exec $(WEB) /bin/sh -c "python manage.py migrate"

makemigrations:
	docker exec $(WEB) /bin/sh -c "python manage.py makemigrations"

compilemessages:
	@echo $(shell for container in $(WEBS); do\
		docker exec $$container /bin/sh -c "python manage.py compilemessages" ;\
	done)

set-django: collectstatic migrate compilemessages
	@echo "Django environment setup complete."

#############
#DEVELOPMENT#
#############

clean-nginx-conf:
	rm -f nginx/sites-enabled/nginx.conf

deploy: clean-nginx-conf
	make clean build up set-django FILE=$(FILE)


