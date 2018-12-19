from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from polls.forecastUpdater import forecastApi

def start():
	print "at updater start"
	scheduler = BackgroundScheduler()
	scheduler.add_job(forecastApi.update_forecast, 'interval', minutes=5)
	scheduler.start()
	scheduler.get_jobs()