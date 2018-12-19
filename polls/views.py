# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404 , render

# Create your views here.

import time
import decimal
from datetime import datetime
import logging

from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Choice, Question, Forecast
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
#from django.utils import timezone
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from SprinklerLord.Station import Station

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job



logging.basicConfig(filename='sprinklerLog.log',format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')

class IndexView(TemplateView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'


	def get_queryset(self):
		return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]


	def get(self, request, **kwargs):
	
		latest_forecast = Forecast.objects.latest('timestamp')
		city= latest_forecast.city
		temperature_in_c = latest_forecast.temperature
		temperature_in_f = (latest_forecast.temperature * decimal.Decimal(1.8))+32
		description = latest_forecast.description.capitalize
		timestamp = "{t.year}/{t.month:02d}/{t.day:02d} - {t.hour:02d}:{t.minute:02d}:{t.second:02d}".format(t=latest_forecast.timestamp)
		#timestamp = "2018/12/11 - 12:12:00"
		#print "timestamp= "+ latest_forecast.timestamp
		return render(
			request,
			'polls/index.html',
			{
				'city': city,
				'temperature_in_c':temperature_in_c,
				'temperature_in_f':temperature_in_f,
				'description':description,
				'utc_update_time':timestamp
			})

class DetailView(generic.DetailView):
	model = Question
	template_name='polls/detail.html'

	

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now() )

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'


def vote(request,question_id):
	question = get_object_or_404(Question,pk=question_id)
	
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])

	except(KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {'question':question,'error_message':"You didn't select a choice.",})
	else:
		selected_choice.votes +=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

def station(request):
	# https://impythonist.wordpress.com/2015/06/16/django-with-ajax-a-modern-client-server-communication-practise/
	# template = loader.get_template('polls/base.html')
	# context = {}
	


	if request.method == 'POST':
		if request.is_ajax():

			station = request.POST.get('stn') 
			state = request.POST.get('state')          
			data = {"stn":station , "state" : state}
			
			print data['stn']
			print state
			stn = Station("Station 1",station)
			stn.setup()
			
			if state == '0':
				print "state is 0"+state
				stn.off()
				sleep(1)
			else:
				print "state is 1"+state
				stn.on()
				sleep(1)	

			return JsonResponse(data)

	#return render(request,'polls/base.html')



scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def myjob():
	time.sleep(4)
	print("hello")


#scheduler.add_job(myjob,'cron',minute='*')
#scheduler.start()
jobs = scheduler.get_jobs()
print jobs

