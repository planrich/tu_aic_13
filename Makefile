run:
	python wsgi/aic/app.py

demo_run:
	python wsgi/aic/app.py --demo

test:
	python test_aic.py

reset_db:
	sudo -u postgres dropdb aic
	sudo -u postgres createdb -O aic aic
	python seed.py

create_db:
	sudo -u postgres createdb -O aic aic

demo_set_db:
	sudo -u postgres psql aic < aic_main_dump
	sudo -u postgres psql aic < update_times

demo_run_scraper:
	python wsgi/aic/scraper.py

demo_run_garbage_collector:
	python wsgi/aic/garbage_collector.py

demo_run_dynamic_pricer:
	python wsgi/aic/dynamic_pricer.py

demo_run_scheduler:
	python wsgi/aic/startScheduler.py
