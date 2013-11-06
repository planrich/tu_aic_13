run_server:
	python wsgi/aic/app.py

run_scraper:
	python wsgi/aic/scraper.py

test:
	python test_aic.py

reset_db:
	sudo -u postgres dropdb aic
	sudo -u postgres createdb aic
	python seed.py