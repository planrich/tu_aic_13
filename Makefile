run_server:
	python wsgi/aic/app.py

run_demo:
	python wsgi/aic/app.py --demo

run_scraper:
	python wsgi/aic/scraper.py

run_garbage_collector:
	python wsgi/aic/garbage_collector.py

run_dynamic_pricer:
	python wsgi/aic/dynamic_pricer.py

run_scheduler:
	python wsgi/aic/startScheduler.py

test:
	python test_aic.py

reset_db:
	sudo -u postgres dropdb aic
	sudo -u postgres createdb aic
	python seed.py