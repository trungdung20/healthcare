# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext ,loader, Context
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from models import Patient, Doctor, PatientRecord, DoctorRecord, FriendShipRequest, Friend, Category, Goal, CheckList,ThanksChecklist, AgreeChecklist, ListItem, UserCheckList, UserListItem, Topic, Vaccination, Condition, Riskfactor, Symptom, Procedure,Medication,Question,Answer, ThanksAnswer, AgreeAnswer,AnswerAlert,QuestionAlert,AdvisorRequest,Notification,UserChecklistIndex,TopicFollow, AnswerNotification, AddTopicNotification, EditTopicNotification, DoctorNotification, PatientNotification,AddChecklistNotification,EditChecklistNotification,AddTopicFollowNotification,EditTopicFollowNotification,AddAnswerTopicFollowNotification,AddQuestionTopicFollowNotification,ThankChecklistNotification,ThankAnswerNotification,AgreeAnswerNotification,AgreeChecklistNotification,Feedback,TopicAgree,PatientAllergy, PatientCondition, PatientMedication, PatientFamilyHistory,QuestionRelate,QuestionAndTopic,TopicAndGoal
from forms import UserForm, PatientForm,  PatientRecordWeightForm, PatientRecordHeightForm, PatientRecordEthnicityForm,PatientRecordVaccinationForm, PatientRecordDietaryForm, PatientRecordAlcoholForm, PatientRecordTobaccoForm, PatientRecordSexForm, PatientRecordDrugForm, DoctorForm, DoctorRecordForm, QuestionForm, AnswerForm, TopicForm, ItemListForm,DoctorImageForm,FeedbackForm, PatientAllergyForm, PatientConditionForm, PatientMedicationForm, PatientFamilyHistoryForm
from endless_pagination.decorators import page_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from random import sample
from django.http import JsonResponse 
from django.core import serializers
import json
#return list of parameter for navbar
import itertools
import time
from operator import itemgetter
def add_isdoctor_to_context_dict(context_dict, doctor):
	if doctor:
		context_dict['isdoctor'] = True
	else :
		context_dict['isdoctor'] = False

def get_doctor(user):
	if user.is_anonymous():
		return None
	doctor = Doctor.objects.filter(user=user)
	if len(doctor) == 1:
		return doctor[0]
	else:
		return None



def get_patient(user):
	if user.is_anonymous():
		return None
	patient = Patient.objects.filter(user=user)
	if len(patient) == 1:
		return patient[0]
	else:
		return None

def add_checklist_to_context_dict(context_dict, id = None):
	if id:
		check_list = CheckList.objects.filter(related_goal = id)
	else:
		check_list = CheckList.objects.all()

	check_list = sorted(checklist, key = lambda c: c.likes, reverse = True)

	if len(check_list) >= 1:
		most_like = check_list[0]
		check_list = check_list[1:]
		context_dict['most_like'] = most_like
		context_dict['check_list'] = check_list
	else:
		context_dict['most_like'] = None
		context_dict['check_list'] = check_list

def intro(request):
	context = RequestContext(request)
	context_dict = {}

	return render_to_response('icare/login/intro.html', context_dict, context)

def intro_login(request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/icare/index/')
			else:
				return HttpResponse("Your icare account has been disabled")
		else:
			print "Invalid login details: {0}, {1}".format(username,password)
			return HttpResponse("Invalid login details is supplied")
	else:
		return render_to_response('icare/login/login.html', {}, context)


def register(request):
	context = RequestContext(request)
	context_dict = {}

	return render_to_response('icare/login/register.html', context_dict, context)

def register_doctor(request):
	context = RequestContext(request)
	registered = False
	context_dict = {}
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		doctor_form = DoctorForm(request.POST,request.FILES)

		if user_form.is_valid() and doctor_form.is_valid():
			user = user_form.save(commit=False)
			password = user.password
			user.set_password(user.password)
			user.save()

			doctor = doctor_form.save(commit=False)
			doctor.user = user
			if 'doctor_image' in request.FILES:
				doctor.doctor_image = request.FILES['doctor_image']

			doctor.save()
			registered = True
			doctor_record = DoctorRecord(doctor=doctor)
			doctor_record.save()
			user = authenticate(username=user.username,password=password)
			login(request, user)


			return HttpResponseRedirect('/icare/index/')
		else:
			print user_form.errors, doctor_form.errors
	else:
		user_form = UserForm()
		doctor_form = DoctorForm()

	context_dict["user_form"]= user_form
	context_dict["doctor_form"] = doctor_form
	context_dict["registered"] = registered

	return render_to_response('icare/login/doctor_register.html', context_dict, context)

def register_patient(request):
	context = RequestContext(request)
	registered = False
	context_dict = {}
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		patient_form = PatientForm(request.POST,request.FILES)
		if user_form.is_valid() and patient_form.is_valid():
			user = user_form.save()
			password = user.password
			user.set_password(user.password)
			user.save()

			patient = patient_form.save(commit=False)
			patient.user = user

			if 'patient_image' in request.FILES:
				patient.patient_image = request.FILES['patient_image']

			patient.save()
			registered = True

			user = authenticate(username= user.username, password= password)
			login(request, user)
			patient_record = PatientRecord(patient=patient)
			patient_record.save()
			return HttpResponseRedirect('/icare/index/')
		else:
			print user_form.errors, patient_form.errors

	else:
		user_form = UserForm()
		patient_form = PatientForm()


	context_dict['user_form'] = user_form
	context_dict['patient_form'] = patient_form
	context_dict['registered'] = registered
	return render_to_response('icare/login/patient_register.html', context_dict, context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/icare/')



def index(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}
	user = request.user
	parameter_index = get_user_list(request.user)
	print parameter_index['curruserid']
	print parameter_index['is_doctor']
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	try:
		doctor = get_doctor(user)
	except:
		doctor = None
	try:
		patient = get_patient(user)
	except:
		patient = None
	if patient:

		count = Doctor.objects.all().count()
		if count > 5:
			rand_ids = sample(xrange(1,count),5)
			doctor_suggestion_list = Doctor.objects.filter(id__in=rand_ids)
			context_dict['doctor_suggestion_list'] = doctor_suggestion_list
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()

	notifications = Notification.objects.all().order_by('-date_time')

	list = []
	for notification in notifications:
		dict = {}
		dict['notification_object'] = notification
		#add question
		question = notification.question
		is_question = False
		if question:
			is_question = True
			is_answer = False
			is_private = False
			if question.privacy:
				is_private = True
			dict['is_private'] = is_private
			dict['question_object'] = question
			dict['answer_count'] = question.answers.count()
			question_answer_set = Answer.objects.filter(related_question=question).order_by('-thanks','-agree')#change name
			if question_answer_set:
				is_answer = True
				dict['hero'] = question_answer_set[0]
			dict['is_answer'] = is_answer
		dict['is_question'] = is_question
		#add topic
		topic = notification.topic
		is_topic = False
		if topic:
			is_topic = True
			is_topic_created = False
			dict['topic_object'] = topic
			topic_doctor = topic.created_doctor
			if topic_doctor:
				is_topic_created = True
			dict['is_topic_created'] = is_topic_created
		dict['is_topic'] = is_topic

		checklist = notification.checklist
		is_checklist = False
		if checklist:
			is_checklist = True
			dict['checklist_object'] = checklist
			checklist_item = ListItem.objects.filter(related_checklist=checklist)
			dict['items'] = checklist_item
		dict['is_checklist'] = is_checklist

		list.append(dict)


	is_doctor = False
	if doctor:
		is_doctor = True
		context_dict['doctor'] = doctor

	can_ask = False
	is_patient = False
	if patient:
		can_ask = True
		is_patient = True
		context_dict['patient'] = patient
	if can_ask:
		ask_form = QuestionForm()
		context_dict['ask_form'] = ask_form

	context_dict['can_ask'] = can_ask
	context_dict['list'] = list
	context_dict['unread_notification'] = unread_notification
	#context_dict['page_template'] = page_template
	if extra_context is not None:
		context_dict.update(extra_context)

	return render(request,template,context_dict)

@login_required
def question_post(request):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	try:
		patient = get_patient(request.user)
	except:
		patient= None
		doctor = get_doctor(request.user)
	if patient:
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()

	if patient:
		if request.method =='POST':
			ask_form = QuestionForm(data = request.POST)
			if ask_form.is_valid():
				question = ask_form.save(commit=False)
				question.created_patient = patient
				question.save()
				notification  = Notification(question=question)
				notification.save()
				new_template = loader.get_template('icare/content/new_question.html')
				c = RequestContext(request,{'new_question':question})
				html = new_template.render(c)
				print html
				return HttpResponse(html)
			else:
				print ask_form.errors
		else:
			ask_form = QuestionForm()
			context_dict['ask_form'] = ask_form
			context_dict['unread_notification'] = unread_notification
			return render_to_response('icare/content/question_index.html', context_dict, context)

@login_required
def question_show(request, question_id, extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/content/question_show.html'
	#page_template = 'icare/content/question_show_page.html'

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	try:
		patient = get_patient(request.user)
	except:
		patient = None
	try:
		doctor = get_doctor(request.user)
	except:
		doctor = None
	if patient:
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()

	can_answer = False
	is_doctor = False
	is_patient = False
	already_answer = False
	question = Question.objects.get(id=question_id)
	answers = Answer.objects.filter(related_question = question).order_by('-thanks','-agree')
	question.viewed +=  1
	question.save()
	list = []
	if doctor:
		if not already_answer:
			can_answer = True
		is_doctor = True
	if patient:
		is_patient = True

	for answer in answers:
		dict = {}
		dict['answer'] = answer
		if answer.from_doctor == doctor:
			already_answer = True
		if is_patient:
			is_thanked = False
			thank = ThanksAnswer.objects.filter(answer=answer,patient=patient)
			agree_list = AgreeAnswer.objects.filter(answer=answer)
			if agree_list:
				dict['agree_doctor_list'] = agree_list
			if thank:
				is_thanked = True
			dict['is_thanked'] = is_thanked
		if is_doctor:
			is_agreed = False
			curr_doctor = get_doctor(request.user)
			agree = AgreeAnswer.objects.filter(answer=answer,doctor=curr_doctor)
			agree_list = AgreeAnswer.objects.filter(answer=answer)

			if agree_list:
				dict['agree_doctor_list'] = agree_list
			if agree:
				is_agreed = True

			dict['is_agreed'] = is_agreed

		list.append(dict)

	if doctor:
		if not already_answer:
			can_answer = True


	question_related = QuestionRelate.objects.filter(question=question)
	#topic_related = QuestionAndTopic.objects.filter(question=question)
	question_form = QuestionForm()
	context_dict['question_related_list'] = question_related
	context_dict['question_form'] = question_form
	context_dict['can_answer'] = can_answer
	context_dict['question']= question
	context_dict['answers'] = list
	context_dict['is_doctor'] = is_doctor
	context_dict['is_patient'] = is_patient
	context_dict['unread_notification'] = unread_notification

	if can_answer:
		answer_form = AnswerForm()
		context_dict['answer_form'] = answer_form

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

@login_required
#doctor answer normal question
def question_answer(request,question_id):

	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	try:
		doctor = get_doctor(request.user)
	except:
		doctor = None

	doctor_record = DoctorRecord.objects.get(doctor=doctor)
	if doctor:
		if request.method == 'POST':
			answer_form = AnswerForm(data = request.POST)
			if answer_form.is_valid():
				question = Question.objects.get(id=question_id)

				counting_check = Answer.objects.filter(from_doctor = doctor, related_question = question).count()
				if counting_check == 1:
					past_answer = Answer.objects.get(from_doctor = doctor, related_question = question)
					past_answer.delete()
					doctor_record.number_answer = doctor_record.number_answer - 1
					doctor_record.save()
				answer = answer_form.save(commit = False)
				answer.from_doctor = doctor
				answer.related_question = question
				answer.save()
				#handles user follow topic
				related_topic = question.related_topic
				users_topic_follow = TopicFollow.objects.filter(topic=related_topic)
				for user_topic_follow in users_topic_follow:
					user = user_topic_follow.user
					answer_topic_follow_notification = AddAnswerTopicFollowNotification(user=user,answer=answer,from_doctor=doctor,topic=related_topic)
					answer_topic_follow_notification.save()
					patient_follow_topic = get_patient(user)
					if patient_follow_topic:
						patient_notification = PatientNotification(patient=patient_follow_topic,add_answer_follow_topic=answer_topic_follow_notification)
						patient_notification.save()
					else:
						doctor_follow_topic = get_doctor(user)
						doctor_notification = DoctorNotification(doctor=doctor_follow_topic,add_answer_follow_topic=answer_topic_follow_notification)
						doctor_notification.save()
				patient = question.created_patient

				if patient:
					answer_notification = AnswerNotification(doctor=doctor,answer=answer,to_patient=patient)
					answer_notification.save()
					patient_ask_answer_notification = PatientNotification(patient=patient,answer_doctor_follow=answer_notification)
					patient_ask_answer_notification.save()
				friends = Friend.objects.filter(to_user=doctor.user)
				#handles patient follow doctor
				for friend in friends:
					patient_friend = get_patient(friend.from_user)
					if patient_friend != patient:
						patient_notification = AnswerNotification(doctor=doctor,to_patient=patient_friend,answer=answer)
						patient_notification.save()
						patient_answer_follow_notification = PatientNotification(patient=patient_friend,answer_doctor_follow=patient_notification)
						patient_answer_follow_notification.save()

				doctor_record.number_answer = doctor_record.number_answer + 1
				doctor_record.save()

				return HttpResponseRedirect('/icare/question/show/'+str(question_id)+'/')
			else:
				print answer_form.errors
		else:
			answer_form = AnswerForm()

			context_dict['answer_form'] = answer_form
			return render_to_response('icare/content/question_show.html',context_dict,context)

	return HttpResponseRedirect('/icare/question/show/'+str(question_id)+'/')

def answer_agree(request):
	context = RequestContext(request)
	answer_agree_id = None
	try:
		doctor = get_doctor(request.user)
	except:
		doctor = None
	if request.method == 'GET':
		answer_agree_id = request.GET['answer_agree_id']

	agree = 0
	answer = Answer.objects.get(id= int(answer_agree_id))
	created_doctor = answer.from_doctor
	created_doctor_record = DoctorRecord.objects.get(doctor=created_doctor)
	is_agreed = False 
	agree_check = AgreeAnswer.objects.filter(answer=answer,doctor=doctor).count()
	if agree_check == 1:
		past_agree = AgreeAnswer.objects.filter(answer=answer, doctor=doctor)
		answer.agree = answer.agree - 1
		past_agree.delete()
		answer.save()
		agree = answer.agree
		created_doctor_record.doctor_recommendation = created_doctor_record.doctor_recommendation - 1
		created_doctor_record.save()
	else:
		answer.agree = answer.agree + 1
		answer.save()
		AgreeAnswer.objects.get_or_create(answer =answer,doctor=doctor)
		is_agreed = True
		agree = answer.agree
		agree_answer_notification = AgreeAnswerNotification(from_doctor=doctor,to_doctor=created_doctor,answer=answer)
		agree_answer_notification.save()
		doctor_notification = DoctorNotification(doctor=created_doctor,agree_answer=agree_answer_notification)
		doctor_notification.save()
		created_doctor_record.doctor_recommendation = created_doctor_record.doctor_recommendation + 1
		created_doctor_record.save()
		
	data = {'count':agree,'is_agreed': is_agreed}
	
	
	return HttpResponse(json.dumps(data), content_type='application/json')


def answer_thanks(request):
	context = RequestContext(request)
	answer_thanks_id = None
	if request.method == 'GET':
		answer_thanks_id = request.GET['answer_thanks_id']

	thanks = 0
	try:
		patient = get_patient(request.user)
	except:
		patient = None
	answer = Answer.objects.get(id = int(answer_thanks_id))
	created_doctor = answer.from_doctor
	created_doctor_record = DoctorRecord.objects.get(doctor=created_doctor)
	thanks_check = ThanksAnswer.objects.filter(answer = answer, patient=patient).count()
	is_thanked = False 
	if thanks_check == 1:
		past_thanks = ThanksAnswer.objects.filter(answer=answer, patient=patient)
		past_thanks.delete()
		answer.thanks = answer.thanks -1
		answer.save()
		is_thanked = False 
		thanks = answer.thanks
		created_doctor_record.patient_recomemdation = created_doctor_record.patient_recommendation - 1
		created_doctor_record.save()
	else:
		answer.thanks = answer.thanks + 1
		answer.save()
		ThanksAnswer.objects.get_or_create(answer=answer, patient=patient)
		is_thanked = True 
		thanks_answer_notification = ThankAnswerNotification(from_patient=patient,to_doctor=created_doctor,answer=answer)
		thanks_answer_notification.save()

		doctor_notification = DoctorNotification(doctor=created_doctor,thank_answer=thanks_answer_notification)
		doctor_notification.save()
		created_doctor_record.patient_recommendation = created_doctor_record.patient_recommendation + 1
		created_doctor_record.save()

	data = {'count':answer.thanks,'is_thanked': is_thanked}
	
	
	return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def category_show(request):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	try:
		patient = get_patient(request.user)
	except:
		patient = None
		doctor = get_doctor(request.user)

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()

	context_dict['unread_notification'] = unread_notification

	category_list = []
	goal_count = Goal.objects.all().count()
	if goal_count > 5:
		rand_ids = sample(xrange(0,goal_count),5)
		suggested_goal_list = Goal.objects.filter(id__in=rand_ids)
		context_dict['suggested_goal_list'] = suggested_goal_list
	for category in Category.objects.all():
		category_dict = {}
		category_dict['category'] = category

		category_dict['goals'] = category.goals.all()
		category_list.append(category_dict)

	context_dict['category_list'] = category_list
	return render_to_response('icare/content/category_index.html',context_dict, context)

@login_required
def checklist_index(request, goal_id,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/content/checklist_index.html'
	#page_template = 'icare/content/checklist_index_page.html'

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification

	try:
		user_doctor = get_doctor(request.user)
	except:
		user_doctor = None

	doctor = False
	patient = False

	if user_doctor:
		doctor = True

	else:
		patient = True
		context_dict['question_form'] = QuestionForm()
	user_patient = get_patient(request.user)

	goal = Goal.objects.get(id = goal_id)
	topic_list = TopicAndGoal.objects.filter(goal=goal)
	checklists =  CheckList.objects.filter(related_goal = goal_id)
	questions = Question.objects.filter(related_goal=goal)
	question_list = []
	for question in questions:
		question_dict = {}
		answer_count = Answer.objects.filter(related_question=question).count()
		answers = Answer.objects.filter(related_question=question).order_by("-thanks","-agree")
		is_answer = False
		if answers:
			answer = answers[0]
			question_dict['answer'] = answer
			is_answer =True
		question_dict['answer_count'] = answer_count
		question_dict['question'] = question

		question_dict['is_answer'] = is_answer
		question_list.append(question_dict)

	checklist_list = []
	for checklist in checklists:
		checklist_dict = {}
		is_doctor_creator = False
		doctor_checklist= checklist.related_doctor
		if doctor_checklist == user_doctor:
			is_doctor_creator = True
		user_checklist_index = UserChecklistIndex.objects.filter(user = user_patient, checklist = checklist)
		is_used = False
		if user_checklist_index:
			is_used = True
		checklist_dict['is_used'] = is_used
		checklist_dict['is_doctor_creator'] = is_doctor_creator
		checklist_dict['checklist_object'] = checklist
		checklist_dict['items'] = checklist.items.all()
		if doctor:
			is_agreed = False
			agree = AgreeChecklist.objects.filter(checklist=checklist,doctor=user_doctor)
			if checklist.agree:
				agree_list = AgreeChecklist.objects.filter(checklist=checklist)
				checklist_dict['agree_doctor_list'] = agree_list
			if agree:
				is_agreed = True

			checklist_dict['is_agreed'] = is_agreed
		if patient:
			is_thanked = False
			thank = ThanksChecklist.objects.filter(checklist=checklist,patient=user_patient)
			if checklist.agree:
				agree_list = AgreeChecklist.objects.filter(checklist=checklist)
				checklist_dict['agree_doctor_list'] = agree_list
			if thank:
				is_thanked = True
			checklist_dict['is_thanked'] = is_thanked
		checklist_list.append(checklist_dict)
	topic_form = TopicForm()
	context_dict['topic_list'] = topic_list
	context_dict['topic_form'] = topic_form
	context_dict['question_list'] = question_list
	context_dict['checklist_list'] = checklist_list
	context_dict['goal'] = goal
	context_dict['doctor'] = doctor
	context_dict['patient'] = patient

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def checklist_doctor_add(request,topic_id):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	try:
		doctor = get_doctor(request.user)
	except:
		doctor = None
	doctor_record = DoctorRecord.objects.get(doctor=doctor)
	goal = Goal.objects.get(id = int(topic_id))
	if doctor:
		checklist = CheckList()
		checklist.related_doctor = doctor
		checklist.related_goal = goal
		checklist.save()
		notification = Notification(checklist = checklist)
		notification.save()
		friends = Friend.objects.filter(to_user=doctor.user)
		for friend in friends:
			patient_friend = get_patient(friend.from_user)
			add_checklist_notification = AddChecklistNotification(to_patient=patient_friend,from_doctor=doctor,checklist=checklist)
			add_checklist_notification.save()
			patient_notification = PatientNotification(patient=patient_friend,add_checklist=add_checklist_notification)
			patient_notification.save()

	else:
		return HttpResponse('You need to be a doctor to add a new checklist')

	return HttpResponseRedirect('/icare/' +str(goal.id)+'/check_lists/')

def doctor_edit_checklist(request,checklist_id):
	context = RequestContext(request)
	context_dict = {}
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	checklist = CheckList.objects.get(id=int(checklist_id))
	items = ListItem.objects.filter(related_checklist=checklist)
	doctor = checklist.related_doctor
	friends = Friend.objects.filter(to_user=doctor.user)
	unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification

	for friend in friends:
		patient_friend = get_patient(friend.from_user)
		edit_checklist_notification = EditChecklistNotification(to_patient=patient_friend,from_doctor=doctor,checklist=checklist)
		edit_checklist_notification.save()
		patient_notification = PatientNotification(patient=patient_friend,edit_checklist=edit_checklist_notification)
		patient_notification.save()
	context_dict['checklist'] =checklist
	context_dict['items'] = items
	context_dict['doctor'] = doctor
	return render_to_response('icare/content/edit_checklist.html',context_dict,context)

def item_add(request):
	context = RequestContext(request)

	context_dict = {}
	checklist_id = None
	if request.method == 'GET':
		checklist_id = request.GET['checklist_id']
		item_form = ItemListForm()
	new_template = loader.get_template('icare/content/item_add.html')
	c = RequestContext(request,{'item_form':item_form,'checklist_id':checklist_id})
	html = new_template.render(c)

	return HttpResponse(html)

def item_delete(request):
	context = RequestContext(request)
	item_id = None
	if request.method == 'GET':
		item_id = request.GET['item_id']
	item = ListItem.objects.get(id=int(item_id))
	item.delete()

	return HttpResponse('success')

def item_submit(request,checklist_id):
	context = RequestContext(request)
	checklist = CheckList.objects.get(id=int(checklist_id))

	try:
		doctor = get_doctor(request.user)
	except:
		doctor = None
	doctor_record = DoctorRecord.objects.get(doctor=doctor)
	doctor_record.number_create_item_checklist = doctor_record.number_create_item_checklist + 1
	doctor_record.save()
	if request.method == "POST":
		item_form = ItemListForm(data=request.POST)
		if item_form.is_valid():
			item = item_form.save(commit=False)
			item.related_checklist = checklist
			item.save()
			success = 'success'
			new_template = loader.get_template('icare/item_success_save.html')
			c = RequestContext(request,{})
			html = new_template.render(c)

			return HttpResponse(html)
		else:
			print item_form.errors
			HttpResponse("You Request Cannot be executed!")

def thanks_checklist(request):
	context = RequestContext(request)
	checklist_thanks_id = None
	if request.method == 'GET':
		checklist_thanks_id = request.GET['checklist_thanks_id']
	try:
		patient = get_patient(request.user)
	except:
		patient = None

	checklist = CheckList.objects.get(id= int(checklist_thanks_id))
	checklist_count = ThanksChecklist.objects.filter(checklist=checklist, patient= patient).count()
	related_doctor = checklist.related_doctor
	related_doctor_record = DoctorRecord.objects.get(doctor = related_doctor)
	likes = 0

	if checklist_count == 1:
		checklist_old = ThanksChecklist.objects.get(checklist=checklist, patient=patient)
		checklist.likes = checklist.likes - 1
		checklist_old.delete()
		checklist.save()
		related_doctor_record.patient_recommendation = related_doctor_record.patient_recommendation - 1
		related_doctor_record.save()
	else:
		ThanksChecklist.objects.get_or_create(checklist=checklist, patient= patient)
		checklist.likes = checklist.likes + 1
		checklist.save()
		checklist_thank_notification = ThankChecklistNotification(from_patient=patient,to_doctor=related_doctor,checklist=checklist)
		checklist_thank_notification.save()
		
		doctor_notification = DoctorNotification(doctor= related_doctor,thank_checklist = checklist_thank_notification)
		doctor_notification.save()
	
		likes = checklist.likes
		related_doctor_record.patient_recommendation = related_doctor_record.patient_recommendation + 1
		related_doctor_record.save()

	return HttpResponse(likes)

def agree_checklist(request):
	context = RequestContext(request)
	checklist_agree_id = None
	if request.method == 'GET':
		checklist_agree_id = request.GET['checklist_agree_id']
	try:
		doctor = get_doctor(request.user)
	except:
		doctor = None
	checklist = CheckList.objects.get(id=int(checklist_agree_id))
	related_doctor = checklist.related_doctor
	related_doctor_record = DoctorRecord.objects.get(doctor=related_doctor)
	checklist_count = AgreeChecklist.objects.filter(checklist=checklist, doctor=doctor).count()

	agree = 0
	if checklist_count==1:
		checklist_old = AgreeChecklist.objects.get(checklist=checklist, doctor= doctor)
		checklist.agree = checklist.agree - 1
		checklist.save()
		checklist_old.delete()
		related_doctor_record.doctor_recommendation = related_doctor_record.doctor_recommendation - 1
		related_doctor_record.save()
	else:
		AgreeChecklist.objects.get_or_create(checklist= checklist, doctor= doctor)
		checklist.agree = checklist.agree + 1
		checklist.save()
		agree_checklist_notification = AgreeChecklistNotification(from_doctor=doctor,to_doctor=related_doctor,checklist=checklist)
		agree_checklist_notification.save()
		doctor_notification = DoctorNotification(doctor=related_doctor,agree_checklist=agree_checklist_notification)
		doctor_notification.save()
		agree = checklist.agree
		related_doctor_record.doctor_recommendation = related_doctor_record.doctor_recommendation + 1
		related_doctor_record.save()

	return HttpResponse(agree)

def add_checklist(request):
	context = RequestContext(request)
	checklist_add_id = None
	if request.method == 'GET':
		checklist_add_id = request.GET['checklist_add_id']
	patient = get_patient(request.user)
	use = 0
	if checklist_add_id:
		checklist = CheckList.objects.get(id=int(checklist_add_id))
		if checklist:
			use = checklist.use + 1
			checklist.use = use
			checklist.save()
			user_index = UserChecklistIndex(user=patient,checklist=checklist)
			user_index.save()
	#model migration
	user_checklist = UserCheckList()
	user_checklist.related_doctor = checklist.related_doctor
	user_checklist.related_goal = checklist.related_goal

	patient = Patient.objects.get(user = request.user)
	user_checklist.related_patient = patient
	user_checklist.save()
	list_items = checklist.items.all()
	for listitem in list_items:
		user_listitem = UserListItem()
		user_listitem.related_checklist = user_checklist
		user_listitem.title = listitem.title
		user_listitem.priority = listitem.priority
		user_listitem.frequency = listitem.frequency
		user_listitem.save()

	return HttpResponse(use)

def checklist_person(request, user_id,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/patient/user_checklist_index.html'
	#page_template = 'icare/patient/user_checklist_index_page.html'

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	try:
		patient = get_patient(request.user)
	except:
		patient = None
	unread_notification = PatientNotification.objects.filter(patient=patient).count()
	context_dict['unread_notification'] = unread_notification
	user_checklists = UserCheckList.objects.filter(related_patient=patient)

	user_checklist_list = []
	for user_checklist in user_checklists:
		checklist_dict = {}
		checklist_dict['user_checklist'] = user_checklist
		checklist_dict['items'] = user_checklist.user_items.all().order_by('-priority')
		percent_complete = int(float(user_checklist.user_items.filter(completed= True).count())/user_checklist.user_items.count() * 100 )
		checklist_dict['percent_complete'] = percent_complete
		user_checklist_list.append(checklist_dict)

	context_dict['user_checklist_list'] = user_checklist_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def item_complete(request):
	context = RequestContext(request)
	item_id = None
	if request.method == 'GET':
		item_id = request.GET['item_id']
	item = UserListItem.objects.get(id=int(item_id))
	item.completed = True
	item.save()
	done = "Done"
	return HttpResponse(done)

def checklist_delete(request):
	context = RequestContext(request)
	user_checklist_id = None
	if request.method == 'GET':
		user_checklist_id = request.GET['user_checklist_id']
	user_checklist = UserCheckList.objects.get(id=int(user_checklist_id))
	patient = user_checklist.related_patient
	doctor = user_checklist.related_doctor
	goal = user_checklist.related_goal
	checklist = CheckList.objects.get(related_doctor=doctor,related_goal=goal)
	index = UserChecklistIndex.objects.get(user=patient,checklist=checklist)

	user_checklist.delete()
	index.delete()

	return HttpResponse('success')

#search index
def search_index(request):
	context = RequestContext(request)
	context_dict = {}
	user = request.user

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	try:
		doctor = get_doctor(user)
	except:
		doctor = None
	try:
		patient = get_patient(user)
	except:
		patient = None
	if patient:
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	is_doctor = False
	is_patient = False

	if doctor:
		is_doctor = True

	if patient:
		is_patient = True

	context_dict['is_patient'] = is_patient
	context_dict['is_doctor'] = is_doctor

	return render_to_response('icare/search/search_index.html',context_dict, context)

def search_condition(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}
	#template ='icare/search/search_condition.html'
	#result_template = 'icare/search/search_condition_page.html'
	#all_template = 'icare/search/search_condition_all_page.html'

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	#page_template = all_template
	result_list = Condition.objects.all().order_by('topic__title')


	context_dict['result_list'] = result_list
	#context_dict['page_template'] = page_template

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def search_condition_result(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification

	done = False

	if request.method == 'GET':
		condition = request.GET['condition']
		done = True
	if done:
		#page_template = result_template
		result_list = Topic.objects.filter(title__icontains=condition).order_by('title')

	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template,context_dict, context)

def search_symptom(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/search/search_symptom.html'
	#result_template = 'icare/search/search_symptom_page.html'
	#all_template = 'icare/search/search_symptom_all_page.html'
	#page_template = ''

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	result_list = Symptom.objects.all().order_by('-topic__title')
	#context_dict['page_template'] = page_template
	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def search_symptom_result(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	done=False
	if request.method == 'GET':
		symptom = request.GET['symptom']
		done = True
	if done:
		#page_template = result_template
		result_list = Topic.objects.filter(title__icontains=symptom).order_by('title')

	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template,context_dict, context)

def search_medication(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/search/search_medication.html'
	#result_page = 'icare/search/search_medication_page.html'
	#all_page = 'icare/search/search_medication_all_page.html'
	#page_template = ''
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	result_list = Medication.objects.all().order_by('-topic__title')

	#context_dict['page_template'] = page_template
	context_dict['result_list'] = result_list

	if extra_context is not None :
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def search_medication_result(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	done=False
	if request.method == 'GET':
		medication = request.GET['medication']
		done = True
	if done:
		#page_template = result_template
		result_list = Topic.objects.filter(title__icontains=medication).order_by('title')

	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)
	return render_to_response(template,context_dict, context)

def search_procedure(request,template=None,extra_context=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/search/search_procedure.html'
	#result_template = 'icare/search/search_procedure_page.html'
	#all_template  = 'icare/search/search_procedure_all_page.html'
	#page_template = ''

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	result_list = Medication.objects.all().order_by('topic__title')


	#context_dict['page_template'] = page_template
	context_dict['result_list'] = result_list


	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def search_procedure_result(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	done=False
	if request.method == 'GET':
		procedure = request.GET['procedure']
		done = True
	if done:
		#page_template = result_template
		result_list = Topic.objects.filter(title__icontains=procedure).order_by('title')

	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template,context_dict, context)

def search_doctor(request, template=None, extra_context=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/search/search_doctor.html'
	#result_template = 'icare/search/search_doctor_page.html'
	#all_template = 'icare/search/search_doctor_all_page.html'
	#page_template = ''

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	result_list = Doctor.objects.all().order_by('name')
	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def search_doctor_result(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	done=False
	if request.method == 'GET':
		doctor = request.GET['doctor']
		done = True
	if done:
		#page_template = result_template
		result_list = Doctor.objects.filter(Q(name__icontains=doctor) | Q(specialty__icontains=doctor)).order_by('name')

	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)

def search_patient(request, template=None, extra_context=None):
	context = RequestContext(request)
	context_dict = {}
	#template = 'icare/search/search_patient.html'
	#result_template = 'icare/search/search_patient_page.html'
	#all_template = 'icare/search/search_patient_all_page.html'
	#page_template = ''

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	result_list = Patient.objects.all().order_by('name')
	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)
	return render_to_response(template, context_dict, context)

def search_patient_result(request,extra_context=None, template=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	done=False
	if request.method == 'GET':
		patient = request.GET['patient']
		done = True
	if done:
		#page_template = result_template
		result_list = Patient.objects.filter(name__icontains=patient).order_by('name')

	context_dict['result_list'] = result_list

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template,context_dict, context)

def topic_show(request, topic_id , template=None, extra_context=None):
	context = RequestContext(request)
	context_dict = {}
	topic_id = int(topic_id)
	topic_main = Topic.objects.get(id=topic_id)
	topic_main.viewed += 1
	topic_main.save()
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	is_agreed = False
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		doctor_agree_check = TopicAgree.objects.filter(doctor=doctor,topic=topic_main)
		if doctor_agree_check:
			is_agreed = True
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	#template = 'icare/content/topic_show.html'
	#page_template ='icare/content/topic_show_page.html'
	print type(topic_id)

	related_questions = topic_main.topic_questions.all()

	question_list = []
	for question in related_questions:
		question_dict = {}
		question_dict['question_object'] = question
		question_dict['answer_count'] = question.answers.count()
		answers = question.answers.all().order_by('-thanks','-agree')
		if answers:
			question_dict['hero'] = answers[0]
		question_list.append(question_dict)


	condition_list = []
	symptom_list = []
	medication_list = []
	procedure_list = []
	other_topic_list = []
	related_topics = topic_main.related_topic.all()
	patient = get_patient(request.user)
	is_patient = False

	if patient:
		is_patient = True

	if related_topics:
		for related_topic in related_topics:
			topic = related_topic
			condition = Condition.objects.filter(topic=topic)
			symptom = Symptom.objects.filter(topic=topic)
			medication = Medication.objects.filter(topic = topic)
			procedure = Procedure.objects.filter(topic = topic)
			if condition:
				condition_list.append(topic)
			elif symptom:
				symptom_list.append(topic)
			elif medication:
				medication_list.append(topic)
			elif procedure:
				procedure_list.append(topic)
			else:
				other_topic_list.append(topic)
	is_follow = False

	topics_follow = TopicFollow.objects.filter(user=request.user,topic=topic_main)
	number_user_follow = TopicFollow.objects.filter(user=request.user,topic=topic_main).count()
	if topics_follow:
		is_follow = True
	number_doctor_agree = TopicAgree.objects.filter(topic=topic_main).count()
	doctor_agree_list = TopicAgree.objects.filter(topic=topic_main)
	topic_form = TopicForm()
	question_form = QuestionForm()
	context_dict['is_agreed'] = is_agreed
	context_dict['number_doctor_agree'] = number_doctor_agree
	context_dict['doctor_agree_list'] = doctor_agree_list
	context_dict['number_user_follow'] = number_user_follow
	context_dict['is_follow'] = is_follow
	context_dict['is_patient'] = is_patient
	context_dict['question_form'] = question_form
	context_dict['topic_form']= topic_form
	context_dict['topic'] = topic_main
	context_dict['condition_list'] = condition_list
	context_dict['symptom_list'] = symptom_list
	context_dict['medication_list'] = medication_list
	context_dict['procedure_list'] = procedure_list
	context_dict['question_list'] = question_list
	context_dict['other_topic_list'] = other_topic_list
	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template, context_dict, context)
#post question in topic
def post_question_topic(request,topic_id):
	context = RequestContext(request)
	topic = Topic.objects.get(id=int(topic_id))
	patient_post = get_patient(request.user)
	users_follow_topic = TopicFollow.objects.filter(topic=topic)
	if request.method == 'POST':
		question_form = QuestionForm(data=request.POST)
		if question_form.is_valid():
			question = question_form.save(commit=False)
			question.created_patient = patient_post
			question.save()
			question.related_topic=topic
			question.save()
			for user_follow_topic in users_follow_topic:
				user = user_follow_topic.user
				question_topic_follow_notification = AddQuestionTopicFollowNotification(user=user,question=question,topic=topic)
				question_topic_follow_notification.save()
				patient_follow_topic = get_patient(user)

				if patient_follow_topic:
					patient_notification = PatientNotification(patient=patient_follow_topic,add_question_follow_topic=question_topic_follow_notification)
					patient_notification.save()
				else:
					doctor_follow_topic = get_doctor(user)
					doctor_notification = DoctorNotification(doctor=doctor_follow_topic,add_question_follow_topic=question_topic_follow_notification)
					doctor_notification.save()
			return HttpResponseRedirect('/icare/topic/show/'+str(topic_id)+'/')
		else:
			return HttpResponse(question_form.errors)

@login_required
def profile_doctor(request, doctor_id,template=None, extra_context=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)


	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	curruser = request.user
	currdoctor = get_doctor(request.user)

	doctor_user = User.objects.get(id = int(doctor_id))

	doctor_friend_count = Friend.objects.filter(to_user=doctor_user).count()
	doctor = Doctor.objects.get(user = doctor_user)

	myaccount = False
	is_patient = True
	if currdoctor:
		is_patient = False
		if currdoctor.id == doctor.id:
			myaccount = True
	#add doctor history content
	history_answer_list = Answer.objects.filter(from_doctor=doctor).order_by("-created_time")
	history_topic_list = Topic.objects.filter(created_doctor=doctor).order_by("-create_time")
	history_checklist_list = CheckList.objects.filter(related_doctor=doctor).order_by("-create_time")
	history_list = []
	#for history_answer,history_topic,history_checklist in itertools.izip_longest(history_answer_list,history_topic_list,history_checklist_list):
	for history_answer in history_answer_list:
		history_dict ={}
		is_history_answer = False
		is_public = False
		if history_answer:
			if not history_answer.related_question.privacy:
				is_public = True
		if history_answer and is_public:
			is_history_answer = True
			history_dict['history_answer'] = history_answer
		history_dict['created'] = history_answer.created_time 	
		history_dict['is_history_answer'] = is_history_answer
		history_list.append(history_dict)
	
	for history_topic in history_topic_list:
		history_dict = {} 
		is_history_topic = False
		if history_topic:
			is_history_topic = True
			history_dict['history_topic'] = history_topic
			history_dict['created'] = history_topic.create_time 
		history_dict['is_history_topic'] = is_history_topic
		history_list.append(history_dict)
		
	for history_checklist in history_checklist_list:
		history_dict = {} 
		is_history_checklist = False
		if history_checklist:
			history_dict['created'] = history_checklist.create_time
			is_history_checklist= True
			history_dict['history_checklist'] = history_checklist
			items = ListItem.objects.filter(related_checklist=history_checklist)
			history_dict['items'] = items
		history_dict['is_history_checklist'] = is_history_checklist
		history_list.append(history_dict)
	history_list = sorted(history_list, key=itemgetter('created'),reverse=True) 
	doctor_record = DoctorRecord.objects.get(doctor=doctor)
	topics = Topic.objects.filter(created_doctor=doctor)
	topic_list = []
	for topic in topics:
		topic_dict = {}
		topic_dict['topic'] = topic
		topic_dict['topic_edit_form'] = TopicForm(instance=topic)
		topic_list.append(topic_dict)

	is_friend = False
	
	is_request = False
	try:
		request = FriendShipRequest.objects.filter(from_user=curruser ,to_user = doctor_user)
	except FriendShipRequest.DoesNotExist:
		request = None
		
	try:
		request_re = FriendShipRequest.objects.filter(from_user=doctor_user, to_user = curruser)
	except FriendShipRequest.DoesNotExist:
		request_re = None
		
	is_request_re =False 	
	if request:
		is_request_re = True
		
	if request or request_re:
		is_request = True
	print "is_request", is_request
	friend = Friend.objects.filter(from_user=curruser ,to_user = doctor_user)
	friend_re = Friend.objects.filter(from_user=doctor_user, to_user = curruser)
	if friend or friend_re:
		is_friend = True
	can_request = False

	if is_patient and not myaccount and not is_friend and not is_request:
		can_request = True

	can_be_advisor = False
	is_advisor = False
	is_request_advisor = False
	is_already_had_advisor = False
	if is_patient:
		patient_curr = get_patient(curruser)

		advisor_request = AdvisorRequest.objects.filter(from_patient=patient_curr)
		if advisor_request:
			is_request_advisor = True
		if patient_curr.advisor:
			is_already_had_advisor = True
		if patient_curr.advisor == doctor:
			is_advisor = True

	if is_patient and not myaccount and not is_advisor and not is_request_advisor and not is_already_had_advisor:
		can_be_advisor = True

	doctor_record_form = DoctorRecordForm(instance=doctor_record)
	topic_form = TopicForm()
	doctor_image_form = DoctorImageForm(instance=currdoctor)

	context_dict = {'is_friend':is_friend,'is_advisor': is_advisor,'can_be_advisor':can_be_advisor,'doctor': doctor, 'doctor_record': doctor_record, 'myaccount': myaccount, 'can_request': can_request,'topic_list':topic_list,'doctor_record_form':doctor_record_form,'topic_form':topic_form,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor'],'doctor_image_form':doctor_image_form,'unread_notification':unread_notification,'history_list':history_list}
	context_dict['friend_count'] = doctor_friend_count
	context_dict['is_request_re'] = is_request_re
	context_dict['is_friend'] = is_friend
	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template,context_dict, context)

def profile_patient(request, patient_id):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	currpatient = get_patient(request.user)

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	patient_user = User.objects.get(id = int(patient_id))
	patient = Patient.objects.get(user = patient_user)
	patient_record = PatientRecord.objects.get(patient=patient)

	myaccount = False
	is_doctor = True
	if currpatient:
		is_doctor = False
		if patient.id == currpatient.id:
			myaccount = True
	is_friend = False
	is_request = False

	friend = Friend.objects.filter(to_user = request.user , from_user = patient_user)
	friend_re = Friend.objects.filter(to_user = patient_user, from_user = request.user)
	if friend or friend_re:
		is_friend = True
	context_dict['is_friend'] = is_friend
	user = request.user
	request = FriendShipRequest.objects.filter(to_user =user, from_user = patient_user)

	request_re = FriendShipRequest.objects.filter(to_user = patient_user, from_user =user)
	is_request_re = False
	if request_re:
		is_request_re = True
	if request or request_re:
		is_request = True
	context_dict['is_request_re'] = is_request_re
	is_advisor = False
	advisor = patient.advisor

	if is_doctor:
	    if advisor == doctor:
		    is_advisor = True

	context_dict['is_advisor'] = is_advisor
	print "friend ship request",is_request
	can_request = False
	if is_doctor and not myaccount and not is_friend and not is_request:
		can_request = True

	print "patient" ,can_request
	vaccinations = patient_record.vaccination.all()
	user_checklist = UserCheckList.objects.filter(related_patient=patient)
	topics_follow = TopicFollow.objects.filter(user=patient.user)

	is_underweight = False
	is_healthy = False
	is_slightly = False
	is_overweight = False
	bmi = patient_record.bmi

	if bmi<=18:
		is_underweight = True
	elif bmi>18 and bmi<=25:
		is_healthy = True
	elif bmi>25 and bmi<=30:
		is_slightly = True
	else:
		is_overweight = True
	current_medication_list = PatientMedication.objects.filter(patient=patient,active=True)
	past_medication_list = PatientMedication.objects.filter(patient=patient,active=False)

	current_condition_list = PatientCondition.objects.filter(patient=patient,active=True)
	past_condition_list = PatientCondition.objects.filter(patient=patient,active=False)

	current_allergy_list = PatientAllergy.objects.filter(patient=patient,active=True)
	past_allergy_list = PatientAllergy.objects.filter(patient=patient,active=False)

	current_family_list = PatientFamilyHistory.objects.filter(patient=patient)
	context_dict['current_medication_list'] = current_medication_list
	context_dict['past_medication_list'] = past_medication_list
	context_dict["current_condition_list"] = current_condition_list
	context_dict['past_condition_list'] = past_condition_list
	context_dict['current_allergy_list'] = current_allergy_list
	context_dict['past_allergy_list'] = past_allergy_list
	context_dict['current_family_list'] = current_family_list
	context_dict['topics_follow'] = topics_follow
	context_dict['patient'] = patient
	context_dict['is_underweight'] = is_underweight
	context_dict['is_healthy'] = is_healthy
	context_dict['is_slightly'] = is_slightly
	context_dict["is_overweight"] = is_overweight
	context_dict["patient_record"] = patient_record
	context_dict["myaccount"] = myaccount
	context_dict["can_request"] = can_request
	context_dict["vaccinations"] = vaccinations
	context_dict["user_checklist"] = user_checklist
	context_dict["curruserid"] = parameter_index['curruserid']
	context_dict["is_navbar_doctor"] = parameter_index['is_doctor']
	context_dict["unread_notification"] = unread_notification
	return render_to_response('icare/patient/patient_profile.html', context_dict, context)

#send advisor request to doctor
def patient_advisor_request(request):
	context = RequestContext(request)
	doctor_id = None

	if request.method == 'GET':
		doctor_id = request.GET['doctor_id']

	requested_doctor = Doctor.objects.get(id = int(doctor_id))
	request_patient = get_patient(request.user)
	request_advisor = AdvisorRequest(from_patient=request_patient,to_doctor = requested_doctor)

	request_advisor.save()
	doctor_notification = DoctorNotification(doctor=requested_doctor,advisor_request=request_advisor)
	doctor_notification.save()
	return HttpResponse('success')

def patient_send_request(request): # doctor send request to specific patient
	context = RequestContext(request)

	patient_id = None
	if request.method == 'GET':
		patient_id = request.GET['patientid']

	requested_patient = Patient.objects.get(id = int(patient_id))
	to_patient = requested_patient.user
	from_doctor = request.user
	f_request=Friend.objects.add_friend(from_doctor, to_patient)
	patient_friend_notification = PatientNotification(patient=requested_patient,friend_request=f_request)
	patient_friend_notification.save()
	return HttpResponse('success')
	
def patient_reject_friend_request(request):
	patient_id = None 
	if request.method == "GET":
		patient_id = request.GET['patientid']
		
	requested_patient = Patient.objects.get(id=int(patient_id))
	to_patient = requested_patient.user 
	from_doctor = request.user 
	f_request = FriendShipRequest.objects.get(from_user=from_doctor,to_user=to_patient)
	try:
		patient_friend_notification = PatientNotification.objects.get(patient=requested_patient,friend_request=f_request)
	except PatientNotification.DoesNotExist:
		patient_friend_notification = None 
	if patient_friend_notification:	
		patient_friend_notification.delete()
	
	f_request.delete()
	return HttpResponse('success')
	
def doctor_send_request(request): # patient send request to specific doctor
	context = RequestContext(request)

	doctor_id = None
	if request.method == 'GET':
		doctor_id = request.GET['doctorid']

	requested_doctor =  Doctor.objects.get(id = int(doctor_id))
	to_doctor = requested_doctor.user
	from_patient = request.user
	f_request=Friend.objects.add_friend(from_patient, to_doctor)
	doctor_friend_notification = DoctorNotification(doctor=requested_doctor,friend_request=f_request)
	doctor_friend_notification.save()
	return HttpResponse('sucess')

def doctor_reject_friend_request(request):
	doctor_id = None 
	if request.method == "GET":
		doctor_id = request.GET['doctorid']
	requested_doctor =  Doctor.objects.get(id = int(doctor_id))
	to_doctor = requested_doctor.user
	from_patient = request.user
	f_request=FriendShipRequest.objects.get(from_user=from_patient,to_user=to_doctor)
	try:
		doctor_friend_notification = DoctorNotification.objects.get(doctor=requested_doctor,friend_request=f_request)
	except DoctorNotification.DoesNotExist:
		doctor_friend_notification = None 
	if doctor_friend_notification:
		doctor_friend_notification.delete()
	f_request.delete()
	return HttpResponse('sucess')

def patient_friend_list(request): #display friend list of patient
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	user = request.user
	patient = Patient.objects.get(user = user)

	user_friend_list = Friend.objects.friends(user)

	context_dict = {'patient': patient , 'user_friend_list': user_friend_list,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor'],"unread_notification":unread_notification}

	return render_to_response('icare/patient/patient_friend_list.html', context_dict, context)

def doctor_friend_list(request): #display friend list of doctor
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	user = request.user
	doctor = Doctor.objects.get(user = user)

	user_friend_list = Friend.objects.friends(user)

	context_dict = {'doctor': doctor, 'user_friend_list':user_friend_list,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor'],"unread_notification":unread_notification}

	return render_to_response('icare/doctor/doctor_friend_list.html',context_dict, context)

def patient_notification_request(request): # display friend request from doctor to patient
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	notification_list = []

	patient_user= request.user  # return patient user
	patient_account = get_patient(patient_user)
	unread_notification = PatientNotification.objects.filter(patient=patient_account).count()
	doctor_unrejected_request_list = FriendShipRequest.objects.filter(to_user=patient_user,rejected=False,viewed_by_patient= False).order_by('-created') # return a friend list of doctor
	doctor_rejected_request_list = FriendShipRequest.objects.filter(from_user=patient_user,rejected=True,viewed_by_patient = False).order_by('-created')
	doctor_accepted_request_list = FriendShipRequest.objects.filter(from_user=patient_user,accepted=True,viewed_by_patient=False).order_by('-created')
	#view topic follow
	add_related_topic_follow_list = AddTopicFollowNotification.objects.filter(user=patient_user,viewed=False).order_by("-created")
	edit_topic_follow_list= EditTopicFollowNotification.objects.filter(user=patient_user,viewed=False).order_by("-created")
	add_answer_topic_follow_list = AddAnswerTopicFollowNotification.objects.filter(user=patient_user,viewed=False).order_by("-created")
	add_question_topic_follow_list = AddQuestionTopicFollowNotification.objects.filter(user=patient_user,viewed=False).order_by("-created")

	advisor_accepted_list = AdvisorRequest.objects.filter(from_patient = patient_account,accepted=True, viewed_by_patient = False).order_by('-created')
	advisor_rejected_list = AdvisorRequest.objects.filter(from_patient = patient_account,rejected=True,viewed_by_patient=False).order_by('-created')
	answer_alert_list = AnswerAlert.objects.filter(to_patient=patient_account , viewed_by_patient=False).order_by('-created')
	patient_answer_follow_list = AnswerNotification.objects.filter(to_patient=patient_account,viewed_by_patient=False).order_by('-created')
	patient_doctor_add_topic_list = AddTopicNotification.objects.filter(to_patient=patient_account,viewed_by_patient=False).order_by('-created')
	patient_doctor_edit_topic_list = EditTopicNotification.objects.filter(to_patient=patient_account,viewed_by_patient=False).order_by('-created')
	patient_doctor_add_checklist_list = AddChecklistNotification.objects.filter(to_patient=patient_account,viewed_by_patient=False).order_by('-created')
	patient_doctor_edit_checklist_list = EditChecklistNotification.objects.filter(to_patient=patient_account,viewed_by_patient=False).order_by('-created')
	list = []
	#for ,edit_topic_follow,add_answer_topic_follow,add_question_topic_follow in itertools.izip_longest(doctor_unrejected_request_list,doctor_rejected_request_list,doctor_accepted_request_list,advisor_accepted_list,advisor_rejected_list,answer_alert_list,patient_answer_follow_list, patient_doctor_add_topic_list, patient_doctor_edit_topic_list, patient_doctor_add_checklist_list , patient_doctor_edit_checklist_list,add_related_topic_follow_list,edit_topic_follow_list,add_answer_topic_follow_list,add_question_topic_follow_list):
	for doctor_unrejected_request in doctor_unrejected_request_list:	
		dict = {}
		is_unrejected_request = False
		if doctor_unrejected_request:
			is_unrejected_request = True
			dict['unrejected_request'] = get_doctor(doctor_unrejected_request.from_user)
			try:
				notification = PatientNotification.objects.get(friend_request=doctor_unrejected_request)
			except PatientNotification.DoesNotExist:
				notification = None 
				
			dict['notification'] = notification 
			dict['created'] = doctor_unrejected_request.created
		dict['is_unrejected_request'] = is_unrejected_request
		list.append(dict)
		
	for doctor_rejected_request in doctor_rejected_request_list:
		dict = {} 
		is_rejected_request = False
		if doctor_rejected_request:
			is_rejected_request = True
			dict['created'] = doctor_rejected_request.created
			dict['rejected_request'] = get_doctor(doctor_rejected_request.to_user)
			try:
				notification = PatientNotification.objects.get(friend_reject=doctor_rejected_request)
			except PatientNotification.DoesNotExist:	
				notification = None 
			dict['notification'] = notification 
		dict['is_rejected_request'] = is_rejected_request
		list.append(dict)
		
	for doctor_accepted_request in doctor_accepted_request_list:
		dict = {} 
		is_accepted_request = False
		if doctor_accepted_request:
			is_accepted_request = True
			dict['created'] = doctor_accepted_request.created
			dict['accepted_request'] = get_doctor(doctor_accepted_request.to_user)
			try:
				notification = PatientNotification.objects.get(friend_accept=doctor_accepted_request)  
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification
		dict['is_accepted_request'] = is_accepted_request
		list.append(dict)
		
	for advisor_accepted in advisor_accepted_list:
		dict = {} 
		is_advisor_accepted = False
		if advisor_accepted:
			is_advisor_accepted = True
			dict['created'] = advisor_accepted.created
			dict['advisor_accepted'] = advisor_accepted.to_doctor
			try:
				notification  = PatientNotification.objects.get(advisor_accept=advisor_accepted)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification  
		dict['is_advisor_accepted'] = is_advisor_accepted
		list.append(dict)
		
	for advisor_rejected in advisor_rejected_list:
		dict = {} 
		is_advisor_rejected = False
		if advisor_rejected:
			dict['created'] = advisor_rejected.created
			is_advisor_rejected = True
			dict['advisor_rejected'] = advisor_rejected.to_doctor
			try:
				notification = PatientNotification.objects.get(advisor_reject=advisor_rejected)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification
		dict['is_advisor_rejected'] = is_advisor_rejected
		list.append(dict)
		
	for answer_alert in answer_alert_list:
		dict = {}
		is_answer_alert = False
		if answer_alert:
			is_answer_alert = True
			dict['created'] = answer_alert.created
			dict['answer_alert'] = answer_alert
			try:
				notification = PatientNotification.objects.get(answer_alert=answer_alert)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification
		dict['is_answer_alert'] = is_answer_alert
		list.append(dict)
	
	for patient_answer_follow in patient_answer_follow_list:
		dict = {} 
		is_answer_follow = False
		if patient_answer_follow:
			is_answer_follow = True
			dict['created'] = patient_answer_follow.created
			dict['answer_follow'] = patient_answer_follow
			try:
				notification = PatientNotification.objects.get(answer_doctor_follow=patient_answer_follow)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification
		dict['is_answer_follow'] = is_answer_follow
		list.append(dict)
		
	for patient_doctor_add_topic in patient_doctor_add_topic_list:
		dict = {}
		is_add_topic = False
		if patient_doctor_add_topic:
			is_add_topic = True
			dict['created'] = patient_doctor_add_topic.created
			dict['add_topic'] = patient_doctor_add_topic
			try:
				notification = PatientNotification.objects.get(add_topic=patient_doctor_add_topic)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
		dict['is_add_topic'] = is_add_topic
		list.append(dict)
		
	for patient_doctor_edit_topic in patient_doctor_edit_topic_list:
		dict = {} 
		is_edit_topic = False
		if patient_doctor_edit_topic:
			is_edit_topic =True
			dict['created'] = patient_doctor_edit_topic.created
			dict['edit_topic'] = patient_doctor_edit_topic
			try:
				notification = PatientNotification.objects.get(edit_topic=patient_doctor_edit_topic)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification  
		dict['is_edit_topic'] = is_edit_topic
		list.append(dict)
	
	for patient_doctor_add_checklist in patient_doctor_add_checklist_list:
		dict = {} 
		is_add_checklist = False
		if patient_doctor_add_checklist:
			is_add_checklist = True
			dict['created'] = patient_doctor_add_checklist.created
			dict['add_checklist'] = patient_doctor_add_checklist
			try:
				notification = PatientNotification.objects.get(add_checklist=patient_doctor_add_checklist)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
		dict['is_add_checklist'] = is_add_checklist
		list.append(dict)
	
	for patient_doctor_edit_checklist in patient_doctor_edit_checklist_list:
		dict = {} 
		is_edit_checklist = False
		if patient_doctor_edit_checklist:
			is_edit_checklist = True
			dict['created'] = patient_doctor_edit_checklist.created
			dict['edit_checklist'] = patient_doctor_edit_checklist
			try:
				notification = PatientNotification.objects.get(edit_checklist=patient_doctor_edit_checklist)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification']=notification
		dict['is_edit_checklist'] = is_edit_checklist
		list.append(dict)
	
	for add_related_topic_follow in add_related_topic_follow_list:
		dict = {} 
		is_add_related_topic_follow = False
		if add_related_topic_follow:
			is_add_related_topic_follow = True
			dict['add_related_topic_follow'] = add_related_topic_follow
			dict['created'] = add_related_topic_follow.created
			try:
				notification = PatientNotification.objects.get(add_topic_follow_topic=add_related_topic_follow)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
		dict["is_add_related_topic_follow"] = is_add_related_topic_follow
		list.append(dict)
	
	for edit_topic_follow in edit_topic_follow_list:
		dict = {}
		is_edit_topic_follow = False
		if edit_topic_follow:
			is_edit_topic_follow = True
			dict['edit_topic_follow'] = edit_topic_follow
			dict['created'] = edit_topic_follow.created
			try:
				notification = PatientNotification.objects.get(edit_topic_follow_topic=edit_topic_follow)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict["notification"] = notification 
		dict["is_edit_topic_follow"] = is_edit_topic_follow
		list.append(dict)
	
	for add_answer_topic_follow in add_answer_topic_follow_list:
		dict = {} 
		is_add_answer_topic_follow = False
		if add_answer_topic_follow:
			is_add_answer_topic_follow = True
			dict['create'] = add_answer_topic_follow.created
			dict["add_answer_topic_follow"] = add_answer_topic_follow
			try:
				notification = PatientNotification.objects.get(add_answer_follow_topic=add_answer_topic_follow)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
		dict["is_add_answer_topic_follow"] = is_add_answer_topic_follow
		list.append(dict)
	
	for add_question_topic_follow in add_question_topic_follow_list:
		dict = {}
		is_add_question_topic_follow = False
		if add_question_topic_follow:
			is_add_question_topic_follow = True
			dict['created'] = add_question_topic_follow.created
			dict["add_question_topic_follow"] = add_question_topic_follow
			try:
				notification = PatientNotification.objects.get(add_question_follow_topic=add_question_topic_follow)
			except PatientNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
		dict["is_add_question_topic_follow"] = is_add_question_topic_follow
		list.append(dict)
		
	newlist = sorted(list, key=itemgetter('created'),reverse=True) 
	context_dict['list'] = newlist
	context_dict['unread_notification'] = unread_notification
	#context_dict = {'patient_user': to_user , 'doctor_request_users': from_user,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']}

	return render_to_response('icare/patient/notification_patient.html', context_dict, context)

def patient_mark_notification(request):
	notification_id = None 
	
	if request.method == "GET":
		notification_id = request.GET['notification_id']
		
	patient_notification = PatientNotification.objects.get(id=int(notification_id))
	patient_notification.delete() 
	patient = get_patient(request.user)
	count = PatientNotification.objects.filter(patient=patient).count()
	
	return HttpResponse(count)
	
def doctor_mark_notification(request):
	notification_id = None 
	
	if request.method == "GET":
		notification_id = request.GET['notification_id']
		
	doctor_notification = DoctorNotification.objects.get(id=int(notification_id))
	doctor_notification.delete() 
	doctor = get_doctor(request.user)
	count = DoctorNotification.objects.filter(doctor=doctor).count()
	
	return HttpResponse(count)	
	
def doctor_notification_request(request):# display friend request from patient to doctor
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	doctor_user = request.user # return doctor user
	doctor_account = get_doctor(doctor_user)
	unread_notification = DoctorNotification.objects.filter(doctor=doctor_account).count()
	patient_unrejected_request_list = FriendShipRequest.objects.filter(to_user=doctor_user,rejected=False,viewed_by_doctor= False).order_by('-created') # return a friend list of doctor
	patient_rejected_request_list = FriendShipRequest.objects.filter(from_user=doctor_user,rejected=True,viewed_by_doctor= False).order_by('-created')
	patient_accepted_request_list = FriendShipRequest.objects.filter(from_user=doctor_user,accepted=True,viewed_by_doctor=False).order_by('-created')
	#view topic follow notification
	add_related_topic_follow_list = AddTopicFollowNotification.objects.filter(user=doctor_user,viewed=False).order_by("-created")
	edit_topic_follow_list= EditTopicFollowNotification.objects.filter(user=doctor_user,viewed=False).order_by("-created")
	add_answer_topic_follow_list = AddAnswerTopicFollowNotification.objects.filter(user=doctor_user,viewed=False).order_by("-created")
	add_question_topic_follow_list = AddQuestionTopicFollowNotification.objects.filter(user=doctor_user,viewed=False).order_by("-created")
	#handels thanks, agree
	thanks_answer_list = ThankAnswerNotification.objects.filter(to_doctor=doctor_account,viewed_by_doctor=False).order_by("-created")
	agree_answer_list = AgreeAnswerNotification.objects.filter(to_doctor=doctor_account,viewed_by_doctor=False).order_by("-created")
	thanks_checklist_list = ThankChecklistNotification.objects.filter(to_doctor=doctor_account,viewed_by_doctor=False).order_by("-created")
	agree_checklist_list = AgreeChecklistNotification.objects.filter(to_doctor=doctor_account,viewed_by_doctor=False).order_by("-created")

	advisor_request_list = AdvisorRequest.objects.filter(to_doctor = doctor_account,accepted=False,viewed_by_doctor = False).order_by('-created')
	question_alert_list = QuestionAlert.objects.filter(to_doctor=doctor_account, view_by_doctor=False).order_by('-create')

	list = []
	#for patient_unrejected_request, patient_rejected_request, patient_accepted_request, advisor_request, question_alert,add_related_topic_follow,edit_topic_follow,add_answer_topic_follow,add_question_topic_follow,thanks_answer,agree_answer,thanks_checklist,agree_checklist in itertools.izip_longest(patient_unrejected_request_list,patient_rejected_request_list,patient_accepted_request_list,advisor_request_list,question_alert_list,add_related_topic_follow_list,edit_topic_follow_list,add_answer_topic_follow_list,add_question_topic_follow_list,thanks_answer_list,agree_answer_list,thanks_checklist_list,agree_checklist_list):
	for thanks_answer in thanks_answer_list:
		dict = {}
		is_thanks_answer = False
		if thanks_answer:
			is_thanks_answer = True
			dict['created'] = thanks_answer.created
			dict["thanks_answer"] = thanks_answer
			try:
				notification = DoctorNotification.objects.get(thank_answer=thanks_answer)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 	
		dict["is_thanks_answer"] = is_thanks_answer
		list.append(dict)
		
	for agree_answer in agree_answer_list:
		dict = {}
		is_agree_answer = False
		if agree_answer:
			dict['created'] = agree_answer.created 
			is_agree_answer = True
			try:	
				notification = DoctorNotification.objects.get(agree_answer=agree_answer)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 	
			dict["agree_answer"] = agree_answer
		dict["is_agree_answer"] = is_agree_answer
		list.append(dict)
	for thanks_checklist in thanks_checklist_list:
		dict = {} 
		is_thanks_checklist = False
		if thanks_checklist:
			is_thanks_checklist = True
			dict["created"] = thanks_checklist.created
			try:
				notification = DoctorNotification.objects.get(thank_checklist=thanks_checklist)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
			dict["thanks_checklist"] = thanks_checklist
		dict["is_thanks_checklist"] = is_thanks_checklist
		list.append(dict)
	for agree_checklist in agree_checklist_list:
		dict = {} 
		is_agree_checklist = False
		if agree_checklist:
			dict['created'] = agree_checklist.created
			is_agree_checklist = True
			try:
				notification = DoctorNotification.objects.get(agree_checklist= agree_checklist)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
			dict["agree_checklist"] = agree_checklist
		dict["is_agree_checklist"] = is_agree_checklist
		list.append(dict)
	
	for add_related_topic_follow in add_related_topic_follow_list:
		is_add_related_topic_follow = False
		if add_related_topic_follow:
			is_add_related_topic_follow = True
			dict['created'] = add_related_topic_follow.created 
			try:
				notification =DoctorNotification.objects.get(add_topic_follow_topic=add_related_topic_follow)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
			dict['add_related_topic_follow'] = add_related_topic_follow
		dict["is_add_related_topic_follow"] = is_add_related_topic_follow
		list.append(dict)
		
	for edit_topic_follow in edit_topic_follow_list:
		dict = {}
		is_edit_topic_follow = False
		if edit_topic_follow:
			is_edit_topic_follow = True
			dict['created'] = edit_topic_follow.created 
			try:
				notification = DoctorNotification.objects.get(edit_topic_follow_topic=edit_topic_follow)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
			dict['edit_topic_follow'] = edit_topic_follow
		dict["is_edit_topic_follow"] = is_edit_topic_follow
		list.append(dict)
	
	for add_answer_topic_follow in add_answer_topic_follow_list:
		dict = {} 
		is_add_answer_topic_follow = False
		if add_answer_topic_follow:
			is_add_answer_topic_follow = True
			dict['created'] = add_answer_topic_follow.created 
			try:
				notification = DoctorNotification.objects.get(add_answer_follow_topic = add_answer_topic_follow)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 	
			dict["add_answer_topic_follow"] = add_answer_topic_follow
		dict["is_add_answer_topic_follow"] = is_add_answer_topic_follow
		list.append(dict)
	
	for add_question_topic_follow in add_question_topic_follow_list:
		dict = {} 
		is_add_question_topic_follow = False
		if add_question_topic_follow:
			is_add_question_topic_follow = True
			dict['created'] = add_question_topic_follow.created 
			try:
				notification = DoctorNotification.objects.get(add_question_follow_topic=add_question_topic_follow)
			except:	
				notification = None 
			dict['notification'] = notification 
			dict["add_question_topic_follow"] = add_question_topic_follow
		dict["is_add_question_topic_follow"] = is_add_question_topic_follow
		list.append(dict)
	for patient_unrejected_request in patient_unrejected_request_list:
		dict = {} 
		is_unrejected_request = False
		if patient_unrejected_request:
			dict['created'] = patient_unrejected_request.created
			is_unrejected_request = True
			patient_user_unrejected_request=get_patient(patient_unrejected_request.from_user)
			try:	
				notification = DoctorNotification.objects.get(friend_request=patient_unrejected_request)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification
			dict['unrejected_request'] = patient_user_unrejected_request
		
		dict['is_unrejected_request'] = is_unrejected_request
		list.append(dict)
	
	for patient_rejected_request in patient_rejected_request_list:
		dict = {} 
		is_rejected_request = False
		if patient_rejected_request:
			is_rejected_request = True
			patient_user_rejected_request =get_patient(patient_rejected_request.to_user)
			dict['created'] = patient_rejected_request.created
			dict['rejected_request'] = patient_user_rejected_request
			try:
				notification = DoctorNotification.objects.get(friend_reject=patient_rejected_request)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
		dict['is_rejected_request'] = is_rejected_request
		list.append(dict)
	
	for patient_accepted_request in patient_accepted_request_list:
		dict = {}
		is_accepted_request = False
		if patient_accepted_request:
			is_accepted_request = True
			dict['created'] = patient_accepted_request.created 
			try:
				notification = DoctorNotification.objects.get(friend_accept=patient_accepted_request)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = None 
			patient_user_accepted_request=get_patient(patient_accepted_request.to_user)
			dict['accepted_request'] = patient_user_accepted_request
		dict['is_accepted_request'] = is_accepted_request
		list.append(dict)
		
	for advisor_request in advisor_request_list:
		dict = {} 
		is_advisor_request = False
		if advisor_request:
			is_advisor_request = True
			try:
				notification = DoctorNotification.objects.get(advisor_request=advisor_request)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
			dict['created'] = advisor_request.created
			dict['advisor_request'] = advisor_request.from_patient
		dict['is_advisor_request'] = is_advisor_request
		list.append(dict)
		
	for question_alert in question_alert_list:
		dict = {}
		is_question_alert = False
		if question_alert:
			dict['created'] = question_alert.create
			is_question_alert = True
			dict['question_alert'] = question_alert
			try:
				notification = DoctorNotification.objects.get(question_alert=question_alert)
			except DoctorNotification.DoesNotExist:
				notification = None 
			dict['notification'] = notification 
		dict['is_question_alert'] = is_question_alert
		list.append(dict)
		
	newlist = sorted(list, key=itemgetter('created'),reverse=True) 
	context_dict['list'] = newlist
	context_dict['unread_notification'] = unread_notification
	#context_dict = {'doctor_user':to_user, 'patient_request_users': from_user,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']}

	return render_to_response('icare/doctor/notification_doctor.html', context_dict, context)

def doctor_friend_accept(request): #  patient accept friend request from doctor
	context = RequestContext(request)
	doctor_id = None
	if request.method == 'GET':
		doctorid = request.GET['doctorid']

	patient_user = User.objects.get(username = request.user)
	doctor_user = Doctor.objects.get(id = int(doctorid))
	patient = get_patient(request.user)
	f_request = FriendShipRequest.objects.get(from_user = doctor_user.user, to_user = patient_user)
	f_request.accepted = True
	f_request.viewed_by_patient = True
	f_request.save()
	doctor_friend_accept_notification = DoctorNotification(doctor=doctor_user,friend_accept=f_request)
	doctor_friend_accept_notification.save()
	try:
		patient_friend_request_notification = PatientNotification.objects.get(patient=patient,friend_request=f_request)
	except PatientNotification.DoesNotExist:
		patient_friend_request_notification = None 
	if patient_friend_request_notification:
		patient_friend_request_notification.delete()
	if f_request.viewed_by_doctor:
		f_request.delete()
		#doctor_friend_accept_notification.delete()
	relation1 = Friend(to_user= patient_user,from_user= doctor_user.user)
	relation1.save()
	relation2 = Friend(to_user = doctor_user.user,from_user = patient_user)
	relation2.save()

	return HttpResponse('success')


#patient viewed their accepted request
def patient_view_accepted_request(request):
	context = RequestContext(request)
	doctorid = None
	if request.method == 'GET':
		doctorid = request.GET['doctorid']

	patient_user = User.objects.get(username = request.user)
	doctor_user = Doctor.objects.get(id = int(doctorid))

	f_request = FriendShipRequest.objects.get(from_user = patient_user, to_user = doctor_user.user)
	f_request.viewed_by_patient = True
	f_request.save()
	patient = get_patient(patient_user)
	try:
		patient_friend_accept_notification = PatientNotification.objects.get(patient=patient,friend_accept=f_request)
	except PatientNotification.DoesNotExist:
		patient_friend_accept_notification = None 
	if patient_friend_accept_notification:
		patient_friend_accept_notification.delete()
	if f_request.viewed_by_doctor:
		f_request.delete()

	return HttpResponse('success')



#patient viewd their accepted request
def patient_view_rejected_request(request):
	context = RequestContext(request)
	doctorid = None
	if request.method == 'GET':
		doctorid = request.GET['doctorid']

	patient_user = User.objects.get(username = request.user)
	doctor_user = Doctor.objects.get(id = int(doctorid))

	f_request = FriendShipRequest.objects.get(from_user = patient_user, to_user = doctor_user.user)
	f_request.viewed_by_patient = True
	f_request.save()
	patient = get_patient(patient_user)
	try:
		patient_friend_reject_notification = PatientNotification.objects.get(patient=patient,friend_reject=f_request)
	except PatientNotification.DoesNotExist:
		patient_friend_reject_notification = None 
	if patient_friend_reject_notification:
		patient_friend_reject_notification.delete()

	if f_request.viewed_by_doctor:
		f_request.delete()

	return HttpResponse('success')

#patient view accept advisor request
def patient_accepted_advisor_request(request):
	context = RequestContext(request)
	doctorid = None
	if request.method == 'GET':
		doctorid = request.GET['doctorid']
	patient = Patient.objects.get(user=request.user)
	doctor = Doctor.objects.get(id=int(doctorid))

	a_request = AdvisorRequest.objects.get(from_patient=patient, to_doctor=doctor)
	a_request.viewed_by_patient = True
	a_request.save()
	try:
		patient_advisor_accept_notification = PatientNotification.objects.get(patient=patient,advisor_accept=a_request)
	except PatientNotification.DoesNotExist:
		patient_advisor_accept_notification = None 
	if patient_advisor_accept_notification:
		patient_advisor_accept_notification.delete()
	if a_request.viewed_by_doctor:
		a_request.delete()
	return HttpResponse('success')


#patient view rejected advisor request
def patient_rejected_advisor_request(request):
	context = RequestContext(request)
	doctorid = None
	if request.method == 'GET':
		doctorid = request.GET['doctorid']

	patient = Patient.objects.get(user=request.user)
	doctor = Doctor.objects.get(id=int(doctorid))

	a_request = AdvisorRequest.objects.get(from_patient=patient, to_doctor=doctor)
	a_request.viewed_by_patient = True
	a_request.save()
	try:
		patient_advisor_reject_notification = PatientNotification.objects.get(patient=patient,advisor_reject=a_request)
	except PatientNotification.DoesNotExist:
		patient_advisor_reject_notification = None 
	if patient_advisor_reject_notification:
		patient_advisor_reject_notification.delete()
	if a_request.viewed_by_doctor:
		a_request.delete()

	return HttpResponse('success')


#patient view advisor answer

def patient_doctor_answer_alert(request):
	context = RequestContext(request)
	answerid = None
	if request.method == 'GET':
		answerid = request.GET['answerid']

	a_answer = AnswerAlert.objects.get( id=answerid )
	a_answer.viewed_by_patient = True
	a_answer.save()

	patient = get_patient(request.user)
	try:
		patient_answer_alert_notification = PatientNotification.objects.get(patient=patient,answer_alert=a_answer)
	except PatientNotification.DoesNotExist: 
		patient_answer_alert_notification = None 
	if patient_answer_alert_notification:
		patient_answer_alert_notification.delete()

	return HttpResponse('success')

#patient reject current advisor
def patient_reject_current_advisor(request):
	context = RequestContext(request)

	patient_id = None
	if request.method == 'GET':
		patient_id = request.GET['patient_id']

	patient = Patient.objects.get(id=int(patient_id))
	patient.advisor = None
	patient.save()

	return HttpResponse('success')

def doctor_friend_reject(request): # patient reject friend request from doctor
	context = RequestContext(request)
	doctor_id = None
	if request.method == 'GET':
		doctorid = request.GET['doctorid']

	patient_user = User.objects.get(username = request.user)
	doctor_user = Doctor.objects.get(id = int(doctorid))

	f_request = FriendShipRequest.objects.get(from_user = doctor_user.user, to_user = patient_user )
	f_request.rejected = True
	f_request.viewed_by_doctor = True
	f_request.save()
	doctor_friend_reject_notification = DoctorNotification(doctor=doctor_user,friend_reject=f_request)
	doctor_friend_reject_notification.save()
	try:
		patient_friend_request_notification = PatientNotification.objects.get(patient=patient_user,friend_request=f_request)
	except PatientNotification.DoesNotExist:
		patient_friend_request_notification = None 
	if patient_friend_request_notification:
		patient_friend_request_notification.delete()

	if f_request.viewed_by_patient:
		f_request.delete()

	return HttpResponse('success')

def patient_friend_accept(request): # doctor accept friend request from patient
	context = RequestContext(request)
	patient_id = None
	if request.method =='GET':
		patientid = request.GET['patientid']

	patient_user = Patient.objects.get(id=int(patientid))
	doctor_user = Doctor.objects.get(user = request.user)

	f_request = FriendShipRequest.objects.get(from_user = patient_user.user, to_user=doctor_user.user)
	f_request.accepted = True
	f_request.viewed_by_doctor = True

	f_request.save()
	patient_friend_accept_notification = PatientNotification(patient=patient_user,friend_accept=f_request)
	patient_friend_accept_notification.save()
	try:
		doctor_friend_request_notification = DoctorNotification.objects.get(doctor=doctor_user,friend_request=f_request)
	except DoctorNotification.DoesNotExist:
		doctor_friend_request_notification = None 
	if doctor_friend_request_notification:
		doctor_friend_request_notification.delete()
	if f_request.viewed_by_patient:
		f_request.delete()

	relation1 = Friend(to_user= patient_user.user,from_user= doctor_user.user)
	relation1.save()
	relation2 = Friend(to_user = doctor_user.user,from_user = patient_user.user)
	relation2.save()

	return HttpResponse('success')

def patient_friend_reject(request): # doctor reject friend request from patient
	context = RequestContext(request)
	patient_id = None
	if request.method == 'GET':
		patientid = request.GET['patientid']

	patient_user = Patient.objects.get(id=int(patientid))
	doctor_user = User.objects.get(username = request.user)

	f_request = FriendShipRequest.objects.get(from_user = patient_user.user, to_user = doctor_user)
	f_request.rejected = True
	f_request.viewed_by_doctor = True
	f_request.save()
	patient_friend_reject_notification = PatientNotification(patient=patient_user,friend_reject=f_request)
	patient_friend_reject_notification.save()
	try:
		doctor_friend_request_notification = DoctorNotification.objects.get(doctor=doctor_user,friend_request=f_request)
	except DoctorNotification.DoesNotExist:
		doctor_friend_request_notification = None 
	if doctor_friend_request_notification:
		doctor_friend_request_notification.delete()
	if f_request.viewed_by_patient:
		f_request.delete()

	return HttpResponse('success')

	#doctor view patient accept request
def doctor_view_accepted_request(request):
	context = RequestContext(request)
	patient_id = None
	if request.method == 'GET':
		patientid = request.GET['patientid']

	patient_user = Patient.objects.get(id=int(patientid))
	doctor_user = User.objects.get(username = request.user)

	f_request = FriendShipRequest.objects.get(to_user = patient_user.user, from_user = doctor_user)
	f_request.viewed_by_doctor = True
	f_request.save()
	doctor = get_doctor(doctor_user)
	try:
		doctor_friend_accept_notification = DoctorNotification.objects.get(doctor=doctor,friend_accept=f_request)
	except DoctorNotification.DoesNotExist:
		doctor_friend_accept_notification = None 
	if doctor_friend_accept_notification:
		doctor_friend_accept_notification.delete()
	if f_request.viewed_by_patient:
		f_request.delete()
	return HttpResponse('success ')

	#doctor view patient rejected request
def doctor_view_rejected_request(request):
	context = RequestContext(request)
	patient_id = None
	if request.method == 'GET':
		patientid = request.GET['patientid']

	patient_user = Patient.objects.get(id=int(patientid))
	doctor_user = User.objects.get(username = request.user)

	f_request = FriendShipRequest.objects.get(to_user = patient_user.user, from_user = doctor_user)
	f_request.viewed_by_doctor = True
	f_request.save()

	doctor = get_doctor(doctor_user)
	try:
		doctor_friend_reject_notification = DoctorNotification.objects.get(doctor=doctor,friend_reject=f_request)
	except DoctorNotification.DoesNotExist:
		doctor_friend_reject_notification = None 
	if doctor_friend_reject_notification:
		doctor_friend_reject_notification.delete()
	if f_request.viewed_by_patient:
		f_request.delete()

	return HttpResponse('success ')

#doctor accept advisor request
def doctor_view_advisor_accept(request):
	context = RequestContext(request)
	patientid = None
	if request.method == 'GET':
		patientid = request.GET['patientid']

	doctor = get_doctor(request.user)

	patient = Patient.objects.get(id=int(patientid))

	a_request = AdvisorRequest.objects.get(from_patient=patient, to_doctor=doctor)
	a_request.viewed_by_doctor = True
	a_request.accepted = True
	a_request.save()
	try:
		doctor_advisor_request_notification = DoctorNotification.objects.get(doctor=doctor,advisor_request=a_request)
	except DoctorNotification.DoesNotExist:
		doctor_advisor_request_notification = None 
	if doctor_advisor_request_notification:
		doctor_advisor_request_notification.delete()
	patient_advisor_accept_notification = PatientNotification(patient=patient,advisor_accept=a_request)
	patient_advisor_accept_notification.save()
	patient.advisor = doctor
	patient.save()

	return HttpResponse('success')

#doctor reject advisor request
def doctor_view_advisor_reject(request):
	context = RequestContext(request)
	patientid = None

	if request.method == 'GET':
		patientid = request.GET['patientid']
	doctor = get_doctor(request.user)

	patient = Patient.objects.get(id=int(patientid))

	a_request = AdvisorRequest.objects.get(from_patient=patient, to_doctor=doctor)
	a_request.viewed_by_doctor = True
	a_request.rejected = True
	a_request.save()
	try:
		doctor_advisor_request_notification = DoctorNotification.objects.get(doctor=doctor,advisor_request=a_request)
	except DoctorNotification.DoesNotExist:
		doctor_advisor_request_notification = None 
	if doctor_advisor_request_notification:
		doctor_advisor_request_notification.delete()
	patient_advisor_reject_notification = PatientNotification(patient=patient,advisor_reject= a_request)
	patient_advisor_reject_notification.save()

	return HttpResponse('success')
#doctor view question send by patient
def doctor_view_question_alert(request):
	context = RequestContext(request)
	questionid = None
	doctor = get_doctor(request.user)
	if request.method == 'GET':
		questionid = request.GET['questionid']


	a_question = QuestionAlert.objects.get(id=questionid)
	a_question.view_by_doctor = True
	a_question.save()
	try:
		doctor_question_alert_notification = DoctorNotification.objects.get(doctor=doctor,question_alert=a_question)
	except DoctorNotification.DoesNotExist:
		doctor_question_alert_notification = None 
	if doctor_question_alert_notification:
		doctor_question_alert_notification.delete()
	return HttpResponse('success')

def user_changepass(request):
	context = RequestContext(request)
	context_dict = {}
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	if request.method == 'POST':

		new_username = request.POST['user_name']
		new_pass = request.POST['new_password']
		con_pass = request.POST['confirm_password']

		if new_pass != con_pass:
			errors = "password you enter didn't match!"
			context_dict['errors'] = errors
		else:
			user = request.user
			user.username = new_username
			user.set_password(new_pass)
			user.save()


	return render_to_response('icare/change_pass.html', context_dict, context)

def patient_edit_weight(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()


	patient_record_form = PatientRecordWeightForm(instance=patient_record)
	new_template = loader.get_template('icare/patient_edit/patient_weight_form.html')
	c = RequestContext(request,{'patient_record_form': patient_record_form,'patient_record_id':patient_record_id})
	html = new_template.render(c)
	print html
	return HttpResponse(html)
#patient_weight
def patient_edit_submit_weight(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)

	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordWeightForm(request.POST, instance=patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			weight = patient_record.weight

			new_template = loader.get_template('icare/patient_recall_object/weight_recall.html')
			c = RequestContext(request,{'patient_new_record':weight})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors
#patient_height
def patient_edit_height(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	patient_record_form = PatientRecordHeightForm(instance=patient_record)
	new_template = loader.get_template('icare/patient_edit/patient_height_form.html')
	c =RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})
	html = new_template.render(c)

	return HttpResponse(html)

def patient_edit_submit_height(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordHeightForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			height = patient_record.height
			new_template = loader.get_template('icare/patient_recall_object/height_recall.html')
			c = RequestContext(request,{'patient_new_record':height})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors

			return HttpResponse(patient_record_form.errors)

#seach for all database
def main_search(request):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	try:
		patient = get_patient(request.user)
	except:
		patient = None
	try:
		doctor = get_doctor(request.user)
	except:
		doctor = None
	if patient:
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	search_content = None
	if request.method == "GET":
		search_index = request.GET['search_main']

	patient = get_patient(request.user)
	doctor = get_doctor(request.user)
	if patient:
		doctor_result_list = Doctor.objects.filter(Q(name__icontains=search_index)|Q(specialty__icontains=search_index))
		doctor_result_count = Doctor.objects.filter(Q(name__icontains=search_index)|Q(specialty__icontains=search_index)).count()
	else:
		doctor_result_list = []
		doctor_result_count = 0
	if doctor:
		patient_result_list = Patient.objects.filter(name__icontains=search_index)
		patient_result_count = Patient.objects.filter(name__icontains=search_index).count()
	else:
		patient_result_list = []
		patient_result_count = 0
	topic_result_list = Topic.objects.filter(title__icontains=search_index)
	topic_result_count = Topic.objects.filter(title__icontains=search_index).count()
	question_result_list = Question.objects.filter(title__icontains=search_index,privacy=False)
	question_result_count = Question.objects.filter(title__icontains=search_index,privacy=False).count()

	result_count = question_result_count + topic_result_count + patient_result_count + doctor_result_count
	list = []
	for doctor_result, patient_result, topic_result, question_result in itertools.izip_longest(doctor_result_list,patient_result_list,topic_result_list,question_result_list):
		dict = {}
		is_doctor_result = False
		if doctor_result:
			is_doctor_result = True
			dict['doctor_result'] = doctor_result
		dict['is_doctor_result'] = is_doctor_result

		is_patient_result = False
		if patient_result:
			is_patient_result = True
			dict['patient_result'] = patient_result
		dict['is_patient_result'] = is_patient_result

		is_topic_result = False
		if topic_result:
			is_topic_result = True
			dict['topic_result'] = topic_result
		dict['is_topic_result'] = is_topic_result

		is_question_result = False
		if question_result:
			is_question_result = True
			dict['question_result'] = question_result
			answer_count = Answer.objects.filter(related_question=question_result).count()
			answer = Answer.objects.filter(related_question=question_result).order_by('-thanks','-agree')
			if answer:
				answer_most = answer[0]
				dict['answer_most'] = answer_most
			dict['answer_count'] = answer_count

		dict['is_question_result'] = is_question_result
		list.append(dict)
	context_dict['result_count'] = result_count
	context_dict['search_result_list'] = list
	return render_to_response('icare/search/search_main.html',context_dict,context)
# patient ethnicity

def patient_edit_ethnicity(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']
	print patient_record_id
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	patient_record_form = PatientRecordEthnicityForm(instance=patient_record)
	new_template = loader.get_template('icare/patient_edit/patient_ethnicity_form.html')

	c = RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})

	html = new_template.render(c)

	return HttpResponse(html)

def patient_edit_submit_ethnicity(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordEthnicityForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			ethnicity = patient_record.ethnicity
			new_template = loader.get_template('icare/patient_recall_object/ethnicity_recall.html')
			c = RequestContext(request,{'patient_new_record':ethnicity})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors

#patient vaccination

def patient_edit_vaccination(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None

	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	patient_record_form = PatientRecordVaccinationForm(instance=patient_record)
	new_template = loader.get_template('icare/patient_edit/patient_vaccination_form.html')
	c = RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})

	html = new_template.render(c)

	return HttpResponse(html)

def patient_edit_submit_vaccination(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordVaccinationForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			vaccination = patient_record.vaccination.all()
			new_template = loader.get_template('icare/patient_recall_object/vaccination_recall.html')
			c = RequestContext(request,{'new_vaccinations':vaccination})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors
#patient dietary restriction

def patient_edit_dietary(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	patient_record_form = PatientRecordDietaryForm(instance=patient_record)
	new_template = loader.get_template('icare/patient_edit/patient_dietary_form.html')
	c = RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})

	html = new_template.render(c)

	return HttpResponse(html)

def patient_edit_submit_dietary(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordDietaryForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			dietary_restriction = patient_record.dietary_restriction

			new_template = loader.get_template('icare/patient_recall_object/dietary_restriction_recall.html')
			c = RequestContext(request,{'patient_new_record':dietary_restriction})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors

# patient alcohol
def patient_edit_alcohol(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	patient_record_form = PatientRecordAlcoholForm(instance=patient_record)
	new_template = loader.get_template('icare/patient_edit/patient_alcohol_form.html')

	c = RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})

	html = new_template.render(c)

	return HttpResponse(html)

def patient_edit_submit_alcohol(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordAlcoholForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			alcohol = patient_record.alcohol
			new_template = loader.get_template('icare/patient_recall_object/alcohol_recall.html')
			c = RequestContext(request,{'patient_new_record':alcohol})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors
#patient tobacco
def patient_edit_tobacco(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	patient_record_form = PatientRecordTobaccoForm(instance=patient_record)
	new_template = loader.get_template('icare/patient_edit/patient_tobacco_form.html')

	c = RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})

	html = new_template.render(c)

	return HttpResponse(html)

def patient_edit_submit_tobacco(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordTobaccoForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			tobacco = patient_record.tobacco
			new_template = loader.get_template('icare/patient_recall_object/tobacco_recall.html')
			c = RequestContext(request,{'patient_new_record':tobacco})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors
#patient sex
def patient_edit_sex(request):
	context = RequestContext(request)
	context_dict = {}
	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	patient_record_form = PatientRecordSexForm(instance=patient_record)

	new_template = loader.get_template('icare/patient_edit/patient_sex_form.html')

	c = RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})

	html = new_template.render(c)

	return HttpResponse(html)

def patient_edit_submit_sex(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}

	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordSexForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			sex = patient_record.sexually_active
			new_template = loader.get_template('icare/patient_recall_object/sexually_recall.html')
			c = RequestContext(request,{'patient_new_record':sex})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors
#patient add allergy
def patient_add_allergy(request):
	context = RequestContext(request)

	patient_id = None
	if request.method == 'GET':
		patient_id = request.GET['patient_id']
	patient = Patient.objects.get(id=int(patient_id))

	if patient.user != request.user:
		return HttpResponseForbidden()
	patient_allergy_form = PatientAllergyForm()

	new_template = loader.get_template('icare/patient_edit/patient_allergy_form.html')
	c = RequestContext(request,{'patient_allergy_form':patient_allergy_form,'patient_id':patient_id,'add':True})
	html = new_template.render(c)

	return HttpResponse(html)
#patient submit allergy
def patient_submit_add_allergy(request,patient_id):
	context = RequestContext(request)
	patient = Patient.objects.get(id=int(patient_id))

	if patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == "POST":
		patient_allergy_form = PatientAllergyForm(data=request.POST)
		if patient_allergy_form.is_valid():
			patient_allergy = patient_allergy_form.save(commit=False)
			patient_allergy.patient = patient
			patient_allergy.save()
			current_allergy_list = PatientAllergy.objects.filter(patient=patient,active=True)
			past_allergy_list = PatientAllergy.objects.filter(patient=patient,active=False)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_allergy.html')
			c = RequestContext(request,{'current_allergy_list':current_allergy_list,'past_allergy_list':past_allergy_list})
			html=new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_allergy_form.errors

#patient edit allergy
def patient_edit_allergy(request):
	context = RequestContext(request)
	patient_allergy_id = None

	if request.method == "GET":
		patient_allergy_id = request.GET['patient_allergy_id']
	patient_allergy = PatientAllergy.objects.get(id=int(patient_allergy_id))

	if patient_allergy.patient.user != request.user:
		return HttpResponseForbidden()
	patient_allergy_form = PatientAllergyForm(instance=patient_allergy)
	new_template = loader.get_template('icare/patient_edit/patient_allergy_form.html')
	c = RequestContext(request,{'patient_allergy_form':patient_allergy_form,'allergy_id':patient_allergy_id})
	html = new_template.render(c)

	return HttpResponse(html)

#patient submit edit allergy
def patient_submit_edit_allergy(request,patient_allergy_id):
	context = RequestContext(request)
	patient_allergy = PatientAllergy.objects.get(id=int(patient_allergy_id))
	patient = patient_allergy.patient
	if request.method == "POST":
		patient_allergy_form = PatientAllergyForm(data=request.POST, instance=patient_allergy)
		if patient_allergy_form.is_valid():
			patient_allergy = patient_allergy_form.save()
			current_allergy_list = PatientAllergy.objects.filter(patient=patient,active=True)
			past_allergy_list = PatientAllergy.objects.filter(patient=patient,active=False)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_allergy.html')
			c = RequestContext(request,{'past_allergy_list':past_allergy_list,'current_allergy_list':current_allergy_list})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_allergy_form.errors
#patient add condition or symptom
def patient_add_condition(request):
	context = RequestContext(request)

	patient_id = None
	if request.method == 'GET':
		patient_id = request.GET['patient_id']
	patient = Patient.objects.get(id=int(patient_id))

	if patient.user != request.user:
		return HttpResponseForbidden()
	patient_condition_form = PatientConditionForm()

	new_template = loader.get_template('icare/patient_edit/patient_condition_form.html')
	c = RequestContext(request,{'patient_condition_form':patient_condition_form,'patient_id':patient_id,'add':True})
	html = new_template.render(c)

	return HttpResponse(html)

#patient submit add condition
def patient_submit_add_condition(request,patient_id):
	context = RequestContext(request)
	patient = Patient.objects.get(id=int(patient_id))

	if patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == "POST":
		patient_condition_form = PatientConditionForm(data=request.POST)
		if patient_condition_form.is_valid():
			patient_condition = patient_condition_form.save(commit=False)
			patient_condition.patient = patient
			patient_condition.save()
			current_condition_list = PatientCondition.objects.filter(patient=patient,active=True)
			past_condition_list = PatientCondition.objects.filter(patient=patient,active=False)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_condition.html')
			c = RequestContext(request,{'current_condition_list':current_condition_list,'past_condition_list':past_condition_list})
			html=new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_condition_form.errors

#patient edit allergy
def patient_edit_condition(request):
	context = RequestContext(request)
	patient_condition_id = None

	if request.method == "GET":
		patient_condition_id = request.GET['patient_condition_id']
	print "Hello", patient_condition_id
	patient_condition = PatientCondition.objects.get(id=int(patient_condition_id))

	if patient_condition.patient.user != request.user:
		return HttpResponseForbidden()
	patient_condition_form = PatientConditionForm(instance=patient_condition)
	new_template = loader.get_template('icare/patient_edit/patient_condition_form.html')
	c = RequestContext(request,{'patient_condition_form':patient_condition_form,'condition_id':patient_condition_id})
	html = new_template.render(c)

	return HttpResponse(html)

#patient submit edit condition
def patient_submit_edit_condition(request,patient_condition_id):
	context = RequestContext(request)
	patient_condition = PatientCondition.objects.get(id=int(patient_condition_id))
	patient = patient_condition.patient
	if request.method == "POST":
		patient_condition_form = PatientConditionForm(data=request.POST, instance=patient_condition)
		if patient_condition_form.is_valid():
			patient_condition = patient_condition_form.save()
			current_condition_list = PatientCondition.objects.filter(patient=patient,active=True)
			past_condition_list = PatientCondition.objects.filter(patient=patient,active=False)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_condition.html')
			c = RequestContext(request,{'past_condition_list':past_condition_list,'current_condition_list':current_condition_list})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_allergy_form.errors

#patient edit medication
def patient_edit_medication(request):
	context = RequestContext(request)
	patient_medication_id = None

	if request.method == "GET":
		patient_medication_id = request.GET['patient_medication_id']

	patient_medication = PatientMedication.objects.get(id=int(patient_medication_id))

	if patient_medication.patient.user != request.user:
		return HttpResponseForbidden()
	patient_medication_form = PatientMedicationForm(instance=patient_medication)
	new_template = loader.get_template('icare/patient_edit/patient_medication_form.html')
	c = RequestContext(request,{'patient_medication_form':patient_medication_form,'medication_id':patient_medication_id})
	html = new_template.render(c)

	return HttpResponse(html)

#patient submit edit medication
def patient_submit_edit_medication(request,patient_medication_id):
	context = RequestContext(request)
	patient_medication = PatientMedication.objects.get(id=int(patient_allergy_id))
	patient = patient_medication.patient
	if request.method == "POST":
		patient_medication_form = PatientMedicationForm(data=request.POST, instance=patient_medication)
		if patient_medication_form.is_valid():
			patient_medication = patient_medication_form.save()
			current_medication_list = PatientMedication.objects.filter(patient=patient,active=True)
			past_medication_list = PatientMedication.objects.filter(patient=patient,active=False)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_medication.html')
			c = RequestContext(request,{'past_medication_list':past_medication_list,'current_medication_list':current_medication_list})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_medication_form.errors

#patient add medication
def patient_add_medication(request):
	context = RequestContext(request)

	patient_id = None
	if request.method == 'GET':
		patient_id = request.GET['patient_id']
	patient = Patient.objects.get(id=int(patient_id))

	if patient.user != request.user:
		return HttpResponseForbidden()
	patient_medication_form = PatientMedicationForm()

	new_template = loader.get_template('icare/patient_edit/patient_medication_form.html')
	c = RequestContext(request,{'patient_medication_form':patient_medication_form,'patient_id':patient_id,'add':True})
	html = new_template.render(c)

	return HttpResponse(html)

#patient submit medication
def patient_submit_add_medication(request,patient_id):
	context = RequestContext(request)
	patient = Patient.objects.get(id=int(patient_id))

	if patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == "POST":
		patient_medication_form = PatientMedicationForm(data=request.POST)
		if patient_medication_form.is_valid():
			patient_medication = patient_medication_form.save(commit=False)
			patient_medication.patient = patient
			patient_medication.save()
			current_medication_list = PatientMedication.objects.filter(patient=patient,active=True)
			past_medication_list = PatientMedication.objects.filter(patient=patient,active=False)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_medication.html')
			c = RequestContext(request,{'current_medication_list':current_medication_list,'past_medication_list':past_medication_list})
			html=new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_medication_form.errors

#patient edit allergy
def patient_edit_family(request):
	context = RequestContext(request)
	patient_family_id = None

	if request.method == "GET":
		patient_family_id = request.GET['patient_family_id']
	patient_family = PatientFamilyHistory.objects.get(id=int(patient_family_id))

	if patient_family.patient.user != request.user:
		return HttpResponseForbidden()
	patient_family_form = PatientFamilyHistoryForm(instance=patient_family)
	new_template = loader.get_template('icare/patient_edit/patient_family_form.html')
	c = RequestContext(request,{'patient_family_form':patient_family_form,'family_id':patient_family_id})
	html = new_template.render(c)

	return HttpResponse(html)

#patient submit edit allergy
def patient_submit_edit_family(request,patient_family_id):
	context = RequestContext(request)
	patient_family = PatientFamilyHistory.objects.get(id=int(patient_family_id))
	patient = patient_family.patient
	if request.method == "POST":
		patient_family_form = PatientFamilyHistoryForm(data=request.POST, instance=patient_family)
		if patient_family_form.is_valid():
			patient_family = patient_family_form.save()
			current_family_list = PatientFamilyHistory.objects.filter(patient=patient)
			#past_allergy_list = PatientAllergy.objects.filter(patient=patient,active=False)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_family.html')
			c = RequestContext(request,{'current_allergy_list':current_allergy_list})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_family_form.errors


#patient add family
def patient_add_family(request):
	context = RequestContext(request)
	patient_id = None
	if request.method == 'GET':
		patient_id = request.GET['patient_id']

	patient = Patient.objects.get(id=int(patient_id))
	#patient = get_patient(request.user)

	patient_family_form = PatientFamilyHistoryForm()

	new_template = loader.get_template('icare/patient_edit/patient_family_form.html')
	c = RequestContext(request,{'patient_family_form':patient_family_form,'patient_id':patient_id,'add':True})
	html = new_template.render(c)

	return HttpResponse(html)

#patient submit family
def patient_submit_add_family(request,patient_id):
	context = RequestContext(request)
	patient = Patient.objects.get(id=int(patient_id))

	if patient.user != request.user:
		return HttpResponseForbidden()
	print "patient submit family"
	if request.method == "POST":
		patient_family_form = PatientFamilyHistoryForm(data=request.POST)
		if patient_family_form.is_valid():
			patient_family = patient_family_form.save(commit=False)
			patient_family.patient = patient
			patient_family.save()
			current_family_list = PatientFamilyHistory.objects.filter(patient=patient)
			new_template = loader.get_template('icare/patient_recall_object/patient_new_family.html')
			c = RequestContext(request,{'current_family_list':current_family_list})
			html=new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_family_form.errors

#patient drug
def patient_edit_drug(request):
	context = RequestContext(request)
	context_dict = {}

	patient_record_id = None
	if request.method == 'GET':
		patient_record_id = request.GET['patient_record_id']
	print patient_record_id
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()

	patient_record_form = PatientRecordDrugForm(instance=patient_record)

	new_template = loader.get_template('icare/patient_edit/patient_drug_form.html')

	c = RequestContext(request,{'patient_record_form':patient_record_form,'patient_record_id':patient_record_id})

	html = new_template.render(c)
	#print html
	return HttpResponse(html)

def patient_edit_submit_drug(request, patient_record_id):
	context = RequestContext(request)
	context_dict = {}
	patient_record = get_object_or_404(PatientRecord, pk=patient_record_id)
	if patient_record.patient.user != request.user:
		return HttpResponseForbidden()
	if request.method == 'POST':
		patient_record_form = PatientRecordDrugForm(request.POST, instance = patient_record)
		if patient_record_form.is_valid():
			patient_record = patient_record_form.save()
			recreational_drug = patient_record.recreational_drug
			new_template = loader.get_template('icare/patient_recall_object/drug_recall.html')
			c = RequestContext(request,{'patient_new_record':recreational_drug})
			html = new_template.render(c)
			return HttpResponse(html)
		else:
			print patient_record_form.errors

# Doctor create topic
def topic_add(request):
	context = RequestContext(request)
	context_dict = {}
	doctor = get_doctor(request.user)

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	print "Hello"
	if doctor:
		doctor_record = DoctorRecord.objects.get(doctor=doctor)
		if request.method == 'POST':
			category = request.POST['select_category']

			topic_form = TopicForm(request.POST,request.FILES)
			if topic_form.is_valid():
				topic = topic_form.save(commit=False)
				topic.created_doctor = doctor
				if 'image' in request.FILES:
					topic.image = request.FILES['image']

				topic.save()
				print "Topic Create"
				if category == "condition":
					condition = Condition(topic=topic)
					condition.save()
				elif category == "medication":
					medication = Medication(topic=topic)
					medication.save()
				elif category == "symptom":
					symptom = Symptom(topic=topic)
					symptom.save()
				else:
					procedure = Procedure(topic=topic)
					procedure.save()

				notification = Notification(topic = topic)
				notification.save()
				friends = Friend.objects.filter(to_user=doctor.user)
				for friend in friends:
					patient = get_patient(friend.from_user)
					add_topic_notification = AddTopicNotification(to_patient=patient,from_doctor=doctor,topic=topic)
					add_topic_notification.save()
					patient_add_topic_notification = PatientNotification(patient=patient,add_topic=add_topic_notification)
					patient_add_topic_notification.save()
				doctor_record.number_create_topic = doctor_record.number_create_topic + 1
				doctor_record.save()
				return HttpResponseRedirect('/icare/topic/show/'+str(topic.id)+'/')
			else:
				print topic_form.errors

				return HttpResponseRedirect('/icare/topic/show/'+str(topic.id)+'/')
		else:
			topic_form = TopicForm()
			context_dict['topic_form']=topic_form
			return render_to_response('icare/content/topic_add.html',context_dict, context)

	else:
		return HttpResponse('You need to be a doctor to add topic')

def add_related_topic(request,topic_id):
	context = RequestContext(request)
	context_dict = {}
	doctor = get_doctor(request.user)
	related_topic = Topic.objects.get(id=int(topic_id))
	users_topic_follow = TopicFollow.objects.filter(topic=related_topic)

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if doctor:
		doctor_record = DoctorRecord.objects.get(doctor=doctor)
		if request.method == 'POST':

			category = request.POST['select_category']
			topic_form = TopicForm(request.POST,request.FILES)
			if topic_form.is_valid():
				topic = topic_form.save(commit=False)
				topic.created_doctor = doctor
				if 'image' in request.FILES:
					topic.image = request.FILES['image']
				topic.save()
				topic.related_topic.add(related_topic)
				topic.save()
				if category == "condition":
					condition = Condition(topic=topic)
					condition.save()
				elif category == "medication":
					medication = Medication(topic=topic)
					medication.save()
				elif category == "symptom":
					symptom = Symptom(topic=topic)
					symptom.save()
				else:
					procedure = Procedure(topic=topic)
					procedure.save()

				notification = Notification(topic = topic)
				notification.save()
				friends = Friend.objects.filter(to_user=doctor.user)
				#follow by doctor
				for friend in friends:
					patient = get_patient(friend.from_user)
					edit_topic_notification = EditTopicNotification(to_patient=patient,from_doctor=doctor,topic=topic)
					edit_topic_notification.save()
					patient_edit_topic_notification = PatientNotification(patient=patient,edit_topic=edit_topic_notification)
					patient_edit_topic_notification.save()
				#follow by topic
				for user_topic_follow in users_topic_follow:
					user = user_topic_follow.user
					add_topic_related_notification = AddTopicFollowNotification(user=user,from_doctor=doctor,topic=topic,related_topic=related_topic)
					add_topic_related_notification.save()
					patient_follow_topic = get_patient(user)
					if patient_follow_topic:
						patient_notification = PatientNotification(add_topic_follow_topic=add_topic_related_notification,patient=patient_follow_topic)
						patient_notification.save()
					else:
						doctor_follow_topic = get_doctor(user)
						doctor_notification = DoctorNotification(add_topic_follow_topic=add_topic_related_notification,doctor=doctor_follow_topic)
						doctor_notification.save()
				doctor_record.number_create_topic = doctor_record.number_create_topic + 1
				doctor_record.save()

				return HttpResponseRedirect('/icare/topic/show/'+str(related_topic.id)+'/')
			else:
				print topic_form.errors
		else:
			topic_form = TopicForm()
			context_dict['topic_form']=topic_form
			return render_to_response('icare/content/topic_show.html',context_dict, context)

	else:
		return HttpResponse('You need to be a doctor to add topic')
#doctor edit topic

def topic_edit(request,topic_id):
	context = RequestContext(request)
	context_dict = {}
	doctor = get_doctor(request.user)

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if doctor:
		topic = Topic.objects.get(id=int(topic_id))
		users_topic_follow = TopicFollow.objects.filter(topic=topic)
		if topic.created_doctor != doctor:
			return HttpResponseForbidden()
		if request.method == 'POST':
			topic_form = TopicForm(request.POST, request.FILES, instance=topic)
			if topic_form.is_valid():
				if 'image' in request.FILES:
					topic.image = request.FILES['image']
				topic = topic_form.save()
				friends = Friend.objects.filter(to_user=doctor.user)
				#handle patient follow doctor
				for friend in friends:
					patient = get_patient(friend.from_user)
					edit_topic_notification = EditTopicNotification(to_patient=patient,from_doctor=doctor,topic=topic)
					edit_topic_notification.save()
					patient_edit_topic_notification = PatientNotification(patient=patient,edit_topic=edit_topic_notification)
					patient_edit_topic_notification.save()
				#handles user follow topic
				for user_topic_follow in users_topic_follow:
					user = user_topic_follow.user
					edit_topic_follow_notification = EditTopicFollowNotification(user=user,from_doctor=doctor,topic=topic)
					edit_topic_follow_notification.save()
					patient_topic_follow = get_patient(user)
					if patient_topic_follow:
						patient_notification = PatientNotification(patient=patient_topic_follow,edit_topic_follow_topic=edit_topic_follow_notification)
						patient_notification.save()
					else:
						doctor_topic_follow = get_doctor(user)
						doctor_notification = DoctorNotification(doctor=doctor_topic_follow,edit_topic_follow_topic=edit_topic_follow_notification)
						doctor_notification.save()
				return HttpResponseRedirect('/icare/topic/show/'+str(topic_id)+'/')
			else:
				print topic_form.errors
		else:
			topic_form = TopicForm(instance=topic)

		return render_to_response('icare/content/topic_edit.html',{'topic_form':topic_form,'topic_id':topic_id,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']},context)
	else:
		return HttpResponse('You need to be a doctor to edit')


#doctor edit profile

def doctor_edit_profile(request,doctor_record_id):
	context = RequestContext(request)
	context_dict = {}
	doctor_record = get_object_or_404(DoctorRecord,pk=doctor_record_id)
	doctor = doctor_record.doctor

	if request.method == 'POST':
		doctor_record_form = DoctorRecordForm(request.POST, instance=doctor_record)
		#doctor_image_form = DoctorImageForm(request.FILES,instance=doctor)
		if doctor_record_form.is_valid():
			doctor_record_form.save()

			return HttpResponseRedirect('/icare/profile/doctor/'+str(doctor.user.id)+'/')
		else:
			print doctor_record_form.errors
	else:
		doctor_record_form = DoctorRecordForm(instance=doctor_record)
		context_dict['doctor_record_form'] = doctor_record_form
		return render_to_response('icare/doctor/doctor_profiledoctor_profile.html',context_dict,context)

def get_user_list(curruser):
	try:
		doctor = Doctor.objects.get(user = curruser)
	except:
		doctor = None
	try:
		patient = Patient.objects.get(user = curruser)
	except:
		patient = None

	if doctor:
		is_doctor = True
		userid = doctor.user.id
	if patient:
		is_doctor = False
		userid = patient.user.id


	return {'curruserid':userid, 'is_doctor': is_doctor}

#view advisor doctor
def patient_view_advisor(request,patient_id,template=None, extra_context=None):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	currpatient = get_patient(request.user)
	patient_user = User.objects.get(id=patient_id)

	patient = Patient.objects.get(user=patient_user)

	if currpatient != patient:
		return HttpResponseForbidden()
	has_advisor = False
	try:
		doctor_advisor = patient.advisor
	except:
		doctor_advisor = None

	if doctor_advisor:
		has_advisor = True

	doctor_record = DoctorRecord.objects.filter(doctor=doctor_advisor)
	consult_question = QuestionForm()
	question_list = Question.objects.filter(created_patient=patient).order_by('-created_time')
	has_question = False
	if question_list:
		has_question = True
	list = []
	for question in question_list:
		dict = {}
		dict['question'] = question
		answers = Answer.objects.filter(related_question = question)
		print answers
		is_answer = False
		if answers:
			is_answer = True
			dict['answers'] = answers
		dict['is_answer'] = is_answer
		list.append(dict)

	context_dict['has_question'] = has_question
	context_dict['consult_question'] = consult_question
	context_dict['question_list'] = list
	context_dict['has_advisor'] = has_advisor
	context_dict['advisor'] = doctor_advisor
	context_dict['doctor_record'] = doctor_record
	context_dict['patient'] = patient

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template,context_dict,context)
#post question to advisor
def question_post_to_advisor(request,doctor_id):
	context = RequestContext(request)
	context_dict = {}

	patient = get_patient(request.user)
	doctor = Doctor.objects.get(id = int(doctor_id))
	if request.method == 'POST':
		question_form = QuestionForm(data=request.POST)
		if question_form.is_valid():
			question = question_form.save(commit=False)
			question.created_patient = patient
			question.to_doctor = doctor
			question.privacy = True
			question.save()
			notification = Notification(question = question )
			notification.save()
			question_alert = QuestionAlert(to_doctor=doctor,from_patient=patient)
			question_alert.save()
			doctor_question_notification = DoctorNotification(doctor=doctor,question_alert=question_alert)
			doctor_question_notification.save()

			return HttpResponseRedirect('/icare/patient/doctor/advisor/'+str(patient.user.id)+'/')
		else:
			print question_form.errors
			return HttpResponse('form errors')
	else:
		return HttpResponseRedirect('/icare/patient/doctor/advisor/'+str(patient.user.id)+'/')

def doctor_advisor_tab_manage(request,doctor_id):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	doctor_user = User.objects.get(id=int(doctor_id))
	doctor = Doctor.objects.get(user=doctor_user)
	patient_list = Patient.objects.filter(advisor=doctor)
	has_patient = False
	if patient_list:
		has_patient = True

	context_dict['has_patient'] = has_patient
	context_dict['doctor'] = doctor
	context_dict['patient_list'] = patient_list
	#context_dict={'has_patient':has_patient,'doctor':doctor,'patient_list':patient_list}

	return render_to_response('icare/doctor/doctor_advised_tab.html/',context_dict,context)

def doctor_manage_advised_patient(request,patient_id):
	context = RequestContext(request)
	context_dict = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']

	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	doctor = get_doctor(request.user)

	patient = Patient.objects.get(id=int(patient_id))
	has_question = False

	question_list = Question.objects.filter(created_patient= patient ,to_doctor= doctor).order_by('-created_time')

	if question_list:
		has_question = True
	list = []
	for question in question_list:
		dict= {}
		is_answer = False
		try:
			answer = Answer.objects.get(related_question = question,from_doctor=doctor)
		except Answer.DoesNotExist:
			answer = None

		if answer:
			is_answer = True

		dict['question'] = question
		dict['answer'] = answer
		dict['is_answer'] = is_answer
		list.append(dict)

	answer_form = AnswerForm()

	context_dict['question_list'] = list
	context_dict['patient'] = patient
	context_dict['answer_form'] = answer_form
	context_dict['has_question'] = has_question

	return render_to_response('icare/doctor/doctor_advised_patient_list.html',context_dict,context)

def doctor_answer_to_advisor(request,question_id):
	context = RequestContext(request)
	context_dict = {}

	doctor = get_doctor(request.user)
	question = Question.objects.get(id = int(question_id))
	patient = question.created_patient

	if request.method == 'POST':
		answer_form = AnswerForm(data=request.POST)
		if answer_form.is_valid():
			answer = answer_form.save(commit=False)
			answer.from_doctor = doctor
			answer.related_question = question
			answer.save()
			answer_noti = AnswerAlert(from_doctor=doctor, to_patient=patient)
			answer_noti.save()
			patient_answer_notification = PatientNotification(patient=patient,answer_alert=answer_noti)
			patient_answer_notification.save()
			return HttpResponseRedirect('/icare/doctor/advised/patient/profile/'+str(patient.id)+'/')

		else:
			print answer_form.errors
			return HttpResponse('form errors')
	else:
		return HttpResponseRedirect('/icare/doctor/advised/patient/profile/'+str(patient.id)+'/')

#patient send advisor reqeust
def handle_patient_advisor_request(request):
	context = RequestContext(request)
	doctorid = None
	if request.method == 'GET':
		doctorid =request.GET['doctorid']
	patient = get_patient(request.user)
	doctor = Doctor.objects.get(id=int(doctorid))

	a_request = AdvisorRequest(from_patient=patient, to_doctor=doctor)
	a_request.save()
	doctor_advisor_request_notification = DoctorNotification(doctor=doctor,advisor_request=a_request)
	doctor_advisor_request_notification.save()
	return HttpResponse('success')

#change question privacy
def patient_question_private(request):
	context = RequestContext(request)
	question_id = None
	if request.method == 'GET':
		question_id = request.GET['question_id']
	question = Question.objects.get(id=int(question_id))
	question.privacy = True
	question.save()

	return HttpResponse('success')

def patient_question_public(request):
	context = RequestContext(request)
	question_id = None

	if request.method == 'GET':
		question_id = request.GET['question_id']
	question = Question.objects.get(id=int(question_id))
	question.privacy = False
	question.save()

	return HttpResponse('success')

def topic_follow(request):
	context = RequestContext(request)

	topic_id = None
	if request.method == 'GET':
		topic_id = request.GET['topic_id']

	user = request.user
	topic = Topic.objects.get(id=int(topic_id))

	topic_follow = TopicFollow(user=user,topic=topic)
	topic_follow.save()
	count = TopicFollow.objects.filter(topic=topic).count()
	return HttpResponse(count)

def topic_unfollow(request):
	context = RequestContext(request)
	print "Hello"
	topic_id = None
	if request.method == "GET":
		topic_id = request.GET['topic_id']

	user =request.user
	topic = Topic.objects.get(id=int(topic_id))

	topic_follow = TopicFollow.objects.get(user=user,topic=topic)
	topic_follow.delete()
	count = TopicFollow.objects.filter(topic=topic).count()

	return HttpResponse(count)

def answer_follow_handles(request):
	context = RequestContext(request)
	answer_follow_id = None
	if request.method =='GET':
		answer_follow_id = request.GET['answer_follow_id']
	answer_follow = AnswerNotification.objects.get(id=int(answer_follow_id))
	answer_follow.viewed_by_patient = True
	answer_follow.save()
	patient = get_patient(request.user)
	try:
		patient_answer_follow_notification = PatientNotification.objects.get(answer_doctor_follow=answer_follow,patient=patient)
	except PatientNotification.DoesNotExist:
		patient_answer_follow_notification = None 
	if patient_answer_alert_notification:
		patient_answer_follow_notification.delete()

	return HttpResponse("Success")

def add_topic_handles(request):
	context = RequestContext(request)
	add_topic_id = None
	if request.method == 'GET':
		add_topic_id = request.GET['add_topic_id']

	add_topic = AddTopicNotification.objects.get(id=int(add_topic_id))
	add_topic.viewed_by_patient = True
	add_topic.save()
	patient = get_patient(request.user)
	try:
		add_topic_notification = PatientNotification.objects.get(patient=patient,add_topic=add_topic)
	except PatientNotification.DoesNotExist:
		add_topic_notification = None 
	if add_topic_notification:
		add_topic_notification.delete()

	return HttpResponse("success")

def edit_topic_handles(request):
	context = RequestContext(request)
	edit_topic_id = None
	if request.method == 'GET':
		edit_topic_id = request.GET['edit_topic_id']

	edit_topic = EditTopicNotification.objects.get(id=int(edit_topic_id))
	edit_topic.viewed_by_patient = True
	edit_topic.save()
	patient = get_patient(request.user)
	try:
		edit_topic_notification = PatientNotification.objects.get(patient=patient,edit_topic=edit_topic)
	except PatientNotification.DoesNotExist:
		edit_topic_notification = None 
	
	if edit_topic_notification:
		edit_topic_notification.delete()

	return HttpResponse("success")

def add_checklist_handles(request):
	context = RequestContext(request)
	add_checklist_id = None
	if request.method == 'GET':
		add_checklist_id = request.GET['add_checklist_id']

	add_checklist = AddChecklistNotification.objects.get(id=int(add_checklist_id))
	add_checklist.viewed_by_patient = True
	add_checklist.save()
	patient = get_patient(request.user)
	try:
		add_checklist_notification = PatientNotification.objects.get(patient=patient,add_checklist=add_checklist)
	except PatientNotification.DoesNotExist:
		add_checklist_notification = None 
		
	if add_checklist_notification:
		add_checklist_notification.delete()

	return HttpResponse("success")

def edit_checklist_handles(request):
	context = RequestContext(request)
	edit_checklist_id = None
	if request.method == 'GET':
		edit_checklist_id = request.GET['edit_checklist_id']

	edit_checklist =EditChecklistNotification.objects.get(id=int(edit_checklist_id))
	edit_checklist.viewed_by_patient = True
	edit_checklist.save()
	patient = get_patient(request.user)
	try:
		edit_checklist_notification = PatientNotification.objects.get(patient=patient,edit_checklist=edit_checklist)
	except PatientNotification.DoesNotExist:
		edit_checklist_notification = None 
	if edit_checklist_notification:	
		edit_checklist_notification.delete()

	return HttpResponse("success")

def unanswer_question(request,extra_context=None,template=None):
	context = RequestContext(request)
	context_dict  = {}

	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification

	questions = Question.objects.filter(privacy=False).order_by('-created_time')
	list = []
	for question in questions:
		dict = {}
		answered = Answer.objects.filter(related_question=question)
		if not answered:

			dict['question'] = question
			list.append(dict)

	context_dict['question_index'] = list
	answer_form = AnswerForm()
	context_dict['answer_form'] = answer_form

	if extra_context is not None:
		context_dict.update(extra_context)

	return render_to_response(template,context_dict,context)

def answer_first_time(request,question_id):
	context = RequestContext(request)
	question = Question.objects.get(id=int(question_id))
	doctor = get_doctor(request.user)

	if request.method == 'POST':
		answer_form = AnswerForm(data=request.POST)
		if answer_form.is_valid():
			answer = answer_form.save(commit = False)
			answer.from_doctor = doctor
			answer.related_question = question
			answer.save()
			doctor_record = doctor.doctorrecord
			doctor_record.number_answer += 1
			doctor_record.save()

			#handles user follow topic
			related_topic = question.related_topic
			users_topic_follow = TopicFollow.objects.filter(topic=related_topic)
			for user_topic_follow in users_topic_follow:
				user = user_topic_follow.user
				answer_topic_follow_notification = AddAnswerTopicFollowNotification(user=user,answer=answer,from_doctor=doctor,topic=related_topic)
				answer_topic_follow_notification.save()
				patient_follow_topic = get_patient(user)
				if patient_follow_topic:
					patient_notification = PatientNotification(patient=patient_follow_topic,add_answer_follow_topic=answer_topic_follow_notification)
					patient_notification.save()
				else:
					doctor_follow_topic = get_doctor(user)
					doctor_notification = DoctorNotification(doctor=doctor_follow_topic,add_answer_follow_topic=answer_topic_follow_notification)
					doctor_notification.save()
			patient = question.created_patient

			if patient:
				answer_notification = AnswerNotification(doctor=doctor,answer=answer,to_patient=patient)
				answer_notification.save()
				patient_ask_answer_notification = PatientNotification(patient=patient,answer_doctor_follow=answer_notification)
				patient_ask_answer_notification.save()
			friends = Friend.objects.filter(to_user=doctor.user)

				#handles patient follow doctor
			for friend in friends:
				patient_friend = get_patient(friend.from_user)
				if patient_friend != patient:
					patient_notification = AnswerNotification(doctor=doctor,to_patient=patient_friend,answer=answer)
					patient_notification.save()
					patient_answer_follow_notification = PatientNotification(patient=patient_friend,answer_doctor_follow=patient_notification)
					patient_answer_follow_notification.save()

			return HttpResponseRedirect('/icare/question/unanswer/')

		else:
			print answer_form.errors
	else:
		return HttpResponseRedirect('/icare/question/unanswer_question/')

def doctor_view_thanks_answer_follow(request):
	context = RequestContext(request)
	doctor_thanks_answer_follow_id = None


	if request.method == "GET":
		doctor_thanks_answer_follow_id = request.GET['doctor_thanks_answer_follow_id']

	thanks_answer = ThankAnswerNotification.objects.get(id=int(doctor_thanks_answer_follow_id))
	thanks_answer.viewed_by_doctor = True
	thanks_answer.save()

	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,thank_answer=thanks_answer)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()

	return HttpResponse('success')

def doctor_view_agree_answer_follow(request):
	context = RequestContext(request)
	doctor_agree_answer_follow_id = None


	if request.method == "GET":
		doctor_agree_answer_follow_id = request.GET['doctor_agree_answer_follow_id']

	agree_answer = AgreeAnswerNotification.objects.get(id=int(doctor_agree_answer_follow_id))
	agree_answer.viewed_by_doctor = True
	agree_answer.save()

	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,agree_answer=agree_answer)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()

	return HttpResponse('success')

def doctor_view_thanks_checklist_follow(request):
	context = RequestContext(request)
	doctor_thanks_checklist_follow_id = None


	if request.method == "GET":
		doctor_thanks_checklist_follow_id = request.GET['doctor_thanks_checklist_follow_id']

	thanks_checklist = ThankChecklistNotification.objects.get(id=int(doctor_thanks_checklist_follow_id))
	thanks_checklist.viewed_by_doctor = True
	thanks_checklist.save()

	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,thank_checklist=thanks_checklist)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()

	return HttpResponse('success')

def doctor_view_agree_checklist_follow(request):
	context = RequestContext(request)
	doctor_agree_checklist_follow_id = None


	if request.method == "GET":
		doctor_agree_checklist_follow_id = request.GET['doctor_agree_checklist_follow_id']

	agree_checklist = AgreeChecklistNotification.objects.get(id=int(doctor_agree_checklist_follow_id))
	agree_checklist.viewed_by_doctor = True
	agree_checklist.save()

	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,agree_checklist=agree_checklist)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()
	return HttpResponse('success')

def doctor_view_add_topic_to_topic_follow(request):
	context = RequestContext(request)
	doctor_add_related_topic_follow_id = None
	if request.method == "GET":
		doctor_add_related_topic_follow_id = request.GET['doctor_add_related_topic_follow_id']
	add_topic_follow = AddTopicFollowNotification.objects.get(id=int(doctor_add_related_topic_follow_id))
	add_topic_follow.viewed = True
	add_topic_follow.save()

	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,add_topic_follow_topic=add_topic_follow)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()

	return HttpResponse("success")

def doctor_view_edit_topic_follow(request):
	context = RequestContext(request)
	doctor_edit_topic_follow_id = None
	if request.method =="GET":
		doctor_edit_topic_follow_id = request.GET["doctor_edit_topic_follow_id"]
	edit_topic_follow = EditTopicFollowNotification.objects.get(id=int(doctor_edit_topic_follow_id))
	edit_topic_follow.viewed = True
	edit_topic_follow.save()
	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,edit_topic_follow_topic=edit_topic_follow)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()


	return HttpResponse("Success")

def doctor_view_add_answer_topic_follow(request):
	context = RequestContext(request)
	doctor_add_answer_topic_follow_id = None
	if request.method == "GET":
		doctor_add_answer_topic_follow_id = request.GET["doctor_add_answer_topic_follow_id"]
	add_answer_topic_follow = AddAnswerTopicFollowNotification.objects.get(id=int(doctor_add_answer_topic_follow_id))
	add_answer_topic_follow.viewed = True
	add_answer_topic_follow.save()
	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,add_answer_follow_topic=add_answer_topic_follow)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()

	return HttpResponse("success")

def doctor_view_add_question_topic_follow(request):
	context = RequestContext(request)
	doctor_add_question_topic_follow_id = None
	if request.method=="GET":
		doctor_add_question_topic_follow_id = request.GET["doctor_add_question_topic_follow_id"]
	add_question_topic_follow = AddQuestionTopicFollowNotification.objects.get(id=int(doctor_add_question_topic_follow_id))
	add_question_topic_follow.viewed =True
	add_question_topic_follow.save()
	doctor = get_doctor(request.user)
	try:
		doctor_notification = DoctorNotification.objects.get(doctor=doctor,add_question_follow_topic=add_question_topic_follow)
	except DoctorNotification.DoesNotExist:
		doctor_notification = None 
	if doctor_notification:
		doctor_notification.delete()

	return HttpResponse("Success")

#hanlde patient topic follow notification
def patient_view_add_topic_to_topic_follow(request):
	context = RequestContext(request)
	patient_add_related_topic_follow_id = None
	if request.method == "GET":
		patient_add_related_topic_follow_id = request.GET['patient_add_related_topic_follow_id']
	add_topic_follow = AddTopicFollowNotification.objects.get(id=int(patient_add_related_topic_follow_id))
	add_topic_follow.viewed = True
	add_topic_follow.save()

	patient = get_patient(request.user)
	try:
		patient_notification = PatientNotification.objects.get(patient=patient,add_topic_follow_topic=add_topic_follow)
	except PatientNotification.DoesNotExist:
		patient_notification = None 
	if patient_notification:
		patient_notification.delete()

	return HttpResponse("success")

def patient_view_edit_topic_follow(request):
	context = RequestContext(request)
	patient_edit_topic_follow_id = None
	if request.method =="GET":
		patient_edit_topic_follow_id = request.GET["patient_edit_topic_follow_id"]
	edit_topic_follow = EditTopicFollowNotification.objects.get(id=int(patient_edit_topic_follow_id))
	edit_topic_follow.viewed = True
	edit_topic_follow.save()
	patient = get_patient(request.user)
	try:
		patient_notification = PatientNotification.objects.get(patient=patient,edit_topic_follow_topic=edit_topic_follow)
	except PatientNotification.DoesNotExist:
		patient_notification = None 
	if patient_notification:	
		patient_notification.delete()


	return HttpResponse("Success")

def patient_view_add_answer_topic_follow(request):
	context = RequestContext(request)
	patient_add_answer_topic_follow_id = None
	if request.method == "GET":
		patient_add_answer_topic_follow_id = request.GET["patient_add_answer_topic_follow_id"]
	add_answer_topic_follow = AddAnswerTopicFollowNotification.objects.get(id=int(patient_add_answer_topic_follow_id))
	add_answer_topic_follow.viewed = True
	add_answer_topic_follow.save()
	patient = get_patient(request.user)
	try:
		patient_notification = PatientNotification.objects.get(patient=patient,add_answer_follow_topic=add_answer_topic_follow)
	except PatientNotification.DoesNotExist:
		patient_notification = None 
	if patient_notification:
		patient_notification.delete()

	return HttpResponse("success")

def patient_view_add_question_topic_follow(request):
	context = RequestContext(request)
	patient_add_question_topic_follow_id = None
	if request.method=="GET":
		patient_add_question_topic_follow_id = request.GET["patient_add_question_topic_follow_id"]
	add_question_topic_follow = AddQuestionTopicFollowNotification.objects.get(id=int(patient_add_question_topic_follow_id))
	add_question_topic_follow.viewed =True
	add_question_topic_follow.save()
	patient = get_patient(request.user)
	try:
		patient_notification = PatientNotification.objects.get(patient=patient,add_question_follow_topic=add_question_topic_follow)
	except PatientNotification.DoesNotExist:
		patient_notification = None 
	if patient_notification:
		patient_notification.delete()

	return HttpResponse("Success")

def feedback(request):
	context = RequestContext(request)
	context_dict = {}
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	if not parameter_index['is_doctor']:
		patient = get_patient(request.user)
		unread_notification = PatientNotification.objects.filter(patient=patient).count()
	else:
		doctor = get_doctor(request.user)
		unread_notification = DoctorNotification.objects.filter(doctor=doctor).count()
	context_dict['unread_notification'] = unread_notification
	if request.method == "POST":
		feedback_form = FeedbackForm(data=request.POST)
		if feedback_form.is_valid():
			feedback_form.save()
			return HttpResponseRedirect("/icare/about/")
		else:
			print feedback_form.errors
	else:
		feedback_form = FeedbackForm()
		context_dict['feedback_form'] = feedback_form
		return render_to_response('icare/content/about.html',context_dict,context)

def agree_topic(request):
	topic_id = None
	if request.method == "GET":
		topic_id = request.GET['topic_id']
	doctor = get_doctor(request.user)
	topic = Topic.objects.get(id=topic_id)
	topic_agree_check = TopicAgree.objects.filter(topic=topic,doctor=doctor).count()

	if topic_agree_check == 1:
		topic_agree_old = TopicAgree.objects.get(topic=topic,doctor=doctor)
		topic_agree_old.delete()
		topic.agree = topic.agree - 1
		topic.save()
		data = False 
	else:
		topic.agree = topic.agree+1
		topic.save()
		topic_agree = TopicAgree.objects.get_or_create(doctor=doctor,topic=topic)
		data = True
	response = {'is_agreed':data}	
	return HttpResponse(json.dumps(response),content_type='application/json')

#ask question related to goal health
def goal_question_add(request,goal_id):
	context = RequestContext(request)
	goal = Goal.objects.get(id=int(goal_id))

	if request.method == "POST":
		question_form = QuestionForm(data=request.POST)
		if question_form.is_valid():
			question = question_form.save(commit=False)
			question.related_goal = goal
			question.save()

			return HttpResponseRedirect('/icare/' +str(goal_id)+'/check_lists/')
	else:
		return HttpResponseRedirect('/icare/' +str(goal_id)+'/checks_lists/')

def add_topic_related_goal(request,goal_id):
	goal = Goal.objects.get(id=int(goal_id))
	doctor = get_doctor(request.user)
	if request.method == "POST":
		category = request.POST['select_category']
		topic_form = TopicForm(data=request.POST)
		if topic_form.is_valid():
			topic = topic_form.save(commit=False)
			topic.created_doctor = doctor
			topic.save()
			topic_and_goal = TopicAndGoal.objects.get_or_create(topic=topic,goal=goal)

			if category == "condition":
				condition = Condition(topic=topic)
				condition.save()
			elif category == "medication":
				medication = Medication(topic=topic)
				medication.save()
			elif category == "symptom":
				symptom = Symptom(topic=topic)
				symptom.save()
			elif category == "procedure":
				procedure = Procedure(topic=topic)
				procedure.save()
			else:
				pass
			notification = Notification(topic=topic)
			notification.save()
			doctor_record = DoctorRecord.objects.get(doctor=doctor)
			doctor_record.number_create_topic += 1
			doctor_record.save()
			return HttpResponseRedirect('/icare/'+str(goal_id)+'/check_lists/')
		else:
			print topic_form.errors

def add_question_related(request,question_id):
	question_related = Question.objects.get(id=int(question_id))
	patient = get_patient(request.user)
	if request.method == "POST":
		print "Hello"
		question_form = QuestionForm(request.POST)
		if question_form.is_valid():
			print "Success"
			question = question_form.save(commit=False)
			question.create_patient = patient
			question.save()
			relation1 = QuestionRelate.objects.get_or_create(question=question,question_related=question_related)
			relation2 = QuestionRelate.objects.get_or_create(question=question_related,question_related=question)

			return HttpResponseRedirect('/icare/question/show/'+str(question_id)+'/')
		else:
			print "False"
			print question_form.errors
