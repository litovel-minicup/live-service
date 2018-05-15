
deploy: deploy-model deploy-live-service

.ONESHELL:
deploy-live-service: minicup_live_service/
	test -d dist || rm -rf dist/*
	# npm run build
	.venv/bin/python setup.py sdist
	ssh minicup mkdir -p /tmp/deploy/
	scp dist/* minicup:/tmp/deploy/
	ssh minicup /var/www/html/live-service/.venv/bin/pip install /tmp/deploy/*

	scp conf/live-service.gunicorn.service minicup:/etc/systemd/system/
	ssh minicup systemctl daemon-reload;

	scp conf/live-service.conf minicup:/etc/nginx/sites-available/
	make restart

.ONESHELL:
deploy-model: ../litovel-minicup-django-administration/
	cd ../litovel-minicup-django-administration/
	test -d dist || rm -rf dist/*
	.venv/bin/python setup.py sdist
	ssh minicup mkdir -p /tmp/deploy/
	scp dist/* minicup:/tmp/deploy/
	ssh minicup /var/www/html/live-service/.venv/bin/pip install /tmp/deploy/*


restart:
	ssh minicup systemctl reload live-service.gunicorn.service;
	ssh minicup service nginx restart;