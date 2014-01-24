
import settings

# Logging
import logging
logger = settings.createLog("start_scheduler")


from apscheduler.scheduler import Scheduler
import scraper
import dynamic_pricer
import garbage_collector

if __name__ == "__main__": 
    logger.info("startScheduledJobs file")
    sc = Scheduler(standalone=True)
    # Schedule  to be called every hour
    sc.add_interval_job(scraper.scrape, minutes=1)
    sc.add_interval_job(dynamic_pricer.dynamic_pricing, minutes=1)
    sc.add_interval_job(garbage_collector.garbage_collecting, minutes=1)

    print('Press Ctrl+C to exit')
    try:
        sc.start()
    except (KeyboardInterrupt, SystemExit):
        pass