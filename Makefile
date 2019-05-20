deploy:
	make deploy-model
	make deploy-live-service
	make restart

deploy-test:
	make deploy-test-model
	make deploy-test-live-service
	make restart-test

.ONESHELL:
deploy-live-service: minicup_live_service/
	test -d dist || rm -rf dist/*
	npm run build
	.venv/bin/python setup.py sdist
	ssh minicup rm -rf /tmp/deploy/
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
	ssh minicup rm -rf /tmp/deploy/*
	ssh minicup mkdir -p /tmp/deploy/
	scp dist/* minicup:/tmp/deploy/
	ssh minicup /var/www/html/live-service/.venv/bin/pip install /tmp/deploy/*

restart:
	ssh minicup systemctl restart live-service.gunicorn.service;
	ssh minicup service nginx reload;

.ONESHELL:
deploy-test-live-service: minicup_live_service/
	test -d dist || rm -rf dist/*
	# npm run build
	.venv/bin/python setup.py sdist
	ssh minicup rm -rf /tmp/deploy/*
	scp dist/* minicup:/tmp/deploy
	ssh minicup /var/www/html/live-service-test/.venv/bin/pip install --upgrade /tmp/deploy/*

	scp conf/live-service-test.gunicorn.service minicup:/etc/systemd/system/
	ssh minicup systemctl daemon-reload;

	scp conf/live-service-test.conf minicup:/etc/nginx/sites-available/
	ssh minicup chown www-data:www-data -R /var/www/html/live-service-test/log/

.ONESHELL:
deploy-test-model:
	cd ../model/
	test -d dist || rm -rf dist/*
	.venv/bin/python setup.py sdist
	ssh minicup rm -rf /tmp/deploy/*
	ssh minicup mkdir -p /tmp/deploy/
	scp dist/* minicup:/tmp/deploy/
	ssh minicup /var/www/html/live-service-test/.venv/bin/pip install --upgrade /tmp/deploy/*

restart-test:
	ssh minicup systemctl restart live-service-test.gunicorn.service;
	ssh minicup service nginx reload;