
deploy:
	make deploy-model
	make deploy-live-service
	make restart

.ONESHELL:
deploy-live-service: minicup_live_service/
	test -d dist || rm -rf dist/*
	npm run build
	.venv/bin/python setup.py sdist
	ssh minicup mkdir -p /tmp/deploy/
	scp dist/* minicup:/tmp/deploy/
	ssh minicup /var/www/html/live-service/.venv/bin/pip install /tmp/deploy/*

	scp conf/live-service.gunicorn.service minicup:/etc/systemd/system/
	ssh minicup systemctl daemon-reload;

	scp conf/live-service.conf minicup:/etc/nginx/sites-available/
	ssh minicup chown www-data:www-data -R /var/www/html/live-service/log/

.ONESHELL:
deploy-model:
	cd ../model/
	test -d dist || rm -rf dist/*
	.venv/bin/python setup.py sdist
	ssh minicup mkdir -p /tmp/deploy/
	scp dist/* minicup:/tmp/deploy/
	ssh minicup /var/www/html/live-service/.venv/bin/pip install /tmp/deploy/*


restart:
	ssh minicup systemctl restart live-service.gunicorn.service;
	ssh minicup service nginx restart;