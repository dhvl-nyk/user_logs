from django.http import HttpResponse
from django.http import *
from django.conf import settings
import json
from user_insights.models import user,user_log, user_app
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import datetime
from collections import Counter
from django.http import JsonResponse
from collections import OrderedDict
import re
import requests

def upload_app_log_csv(request):
	all_app_log = []
	if request.POST and request.FILES:
		if not request.POST.get('user_name'):
			return JsonResponse({'Error':'user not present'},status=400)

		get_user = user.objects.filter(user_name=request.POST.get('user_name'))
		if not get_user:
			get_user = user.objects.create(user_name=request.POST.get('user_name'))
		else:
			get_user = get_user[0]

		for each_line in request.FILES['csv_file']:
			each_record = each_line.strip().decode('utf-8')

			if each_record:
				record = each_record.split(",")
				app_name = re.sub(r'"','', record[0])
				app_id = re.sub(r'"','', record[1])
				app_record = user_app(app_name=app_name, app_id=app_id, user=get_user)
				all_app_log.append(app_record)

		user_app.objects.bulk_create(all_app_log)
		return JsonResponse({'success':'Uploaded file sucessfully'},status=200)
	else:
		return render(request, "user_insights/upload_app_log_csv.html", locals())

def upload_call_log_csv(request):
	all_call_log = []
	if request.POST and request.FILES:

		if not request.POST.get('user_name'):
			return JsonResponse({'Error':'user not present'},status=400)

		get_user = user.objects.filter(user_name=request.POST.get('user_name'))
		if not get_user:
			get_user = user.objects.create(user_name=request.POST.get('user_name'))
		else:
			get_user = get_user[0]

		first_line_count = 0
		for each_line in request.FILES['csv_file']:
			if first_line_count == 0:
				first_line_count+=1
			else:	
				each_record = each_line.strip().decode('utf-8')
				if each_record:
					record = re.split('\t|,',each_record)
					call_timestamp = datetime.strptime(record[1], '%m/%d/%Y %H:%M')
					call_record = user_log(call_timestamp= call_timestamp, call_duration = record[2], call_type =record[3], phone_number = record[4], user = get_user)
					all_call_log.append(call_record)

		user_log.objects.bulk_create(all_call_log)
		return JsonResponse({'success':'Uploaded file sucessfully'},status=200)
	else:
		return render(request, "user_insights/upload_call_log_csv.html", locals())

def user_call_analytics(request):
	response_payload = {}
	if request.GET:
		user_name = request.GET.get("user_name").strip()
		phone_numbers = []
		call_type = {}
		call_pick_up = []
		call_type_freq = []
		total_call_duration = 0
		user_call_logs = user_log.objects.filter(user__user_name__icontains=user_name)
		for log in user_call_logs.iterator():
			if "-" not in log.call_type:
				phone_numbers.append(log.phone_number)
				call_type_freq.append(log.call_type)

				total_call_duration += int(log.call_duration)

				if log.call_type in call_type.keys():
					call_type[log.call_type]+= int(log.call_duration)
				else:
					call_type[log.call_type] = int(log.call_duration)


		# this gives the logic of percentage distribution of incoming, outgoing and missed calls
		call_type_freuency = Counter(call_type_freq)
		all_calls = sum(call_type_freuency.values())

		for k, v in call_type_freuency.items():
			call_type_freuency[k] = float(call_type_freuency[k]/all_calls)*100

		#converting to phone no format
		friends_family  = OrderedDict() 

		for key,value in Counter(phone_numbers).most_common(5):
			phone_field = str(key)
			phone_number = str(int(float(phone_field)))
			if len(phone_number) > 10:
				phone_number = phone_number[2:]			
			friends_family[phone_number]= value

		response_payload = {
			"friends_family_no_of_calls":friends_family,
			"time_spend_on_call": total_call_duration,
			"total_call_time_distibution": call_type,
			"hit_miss_call_percent": call_type_freuency
		}
		return JsonResponse(response_payload)
	else:
		return render(request, "user_insights/user_call_analytics.html")

def user_app_analytics(request):
	response_payload = {}
	if request.GET:
		user_name = request.GET.get("user_name").strip()
		user_app_logs = user_app.objects.filter(user__user_name__icontains=user_name)[21:50]
		base_url = "https://api.apptweak.com/android/applications/"
		edge_url = "/information.json"
		headers = {'X-Apptweak-Key': 'n6bDkOQr-9r1A2W2Ub5QHDH5K9A'}
		fail = []
		user_app_category = []

		#logic to get app categories
		for log in user_app_logs.iterator():
			if len(log.app_category) == 0:
				url = base_url + log.app_id + edge_url
				try:
					r = requests.get(url, headers=headers)
					print(r.status_code)
					if r.status_code == 200:
						result = r.json()
						if result:
							log.app_category = result['content']['genres'][0]
							log.save()
							user_app_category.append(log.app_category)
					else:
						fail.append(log.app_name)
				except:
					fail.append(log.app_name)	
			else:
				user_app_category.append(log.app_category)

		#user type based on category freq
		user_type = Counter(user_app_category).most_common(1)
		print(Counter(user_app_category).most_common(5))

		response_payload = {
			"user_app_category":user_type,
			"failed_to_get_info": fail
		}
		return JsonResponse(response_payload)
	else:
		return render(request, "user_insights/user_app_analytics.html")