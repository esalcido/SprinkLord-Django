# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404 , render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from SprinklerLord.Station import Station

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	
	def home(request):
		# https://impythonist.wordpress.com/2015/06/16/django-with-ajax-a-modern-client-server-communication-practise/
		#template = loader.get_template('polls/base.html')
		#context = {}

		if request.method == 'POST':
			if request.is_ajax():
				email = request.POST.get('email') 
				password = request.POST.get('password')          
				data = {"email":email , "password" : password}
				print data['email']
				return JsonResponse(data)

		#return render(request,'polls/base.html')

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]

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

# def home(request):
# 	# https://impythonist.wordpress.com/2015/06/16/django-with-ajax-a-modern-client-server-communication-practise/
# 	template = loader.get_template('polls/base.html')
# 	context = {}




# 	if request.method == 'POST':
# 		if request.is_ajax():
# 			email = request.POST.get('email') 
# 			password = request.POST.get('password')          
# 			data = {"email":email , "password" : password}
# 			print data['email']
# 			return JsonResponse(data)

# 	return render(request,'polls/base.html')




            