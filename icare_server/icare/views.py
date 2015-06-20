# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext ,loader, Context
from django.shortcuts import render_to_response, get_object_or_404, render 
from django.contrib.auth import authenticate, login, logout 
from models import Patient, Doctor, PatientRecord, DoctorRecord, FriendShipRequest, Friend, Category, Goal, CheckList,ThanksChecklist, AgreeChecklist, ListItem, UserCheckList, UserListItem, Topic, Vaccination, Condition, Riskfactor, Symptom, Procedure,Medication,Question,Answer, ThanksAnswer, AgreeAnswer,AnswerAlert,QuestionAlert,AdvisorRequest,Notification,UserChecklistIndex,TopicFollow
from forms import UserForm, PatientForm,  PatientRecordWeightForm, PatientRecordHeightForm, PatientRecordEthnicityForm,PatientRecordVaccinationForm, PatientRecordDietaryForm, PatientRecordAlcoholForm, PatientRecordTobaccoForm, PatientRecordSexForm, PatientRecordDrugForm, DoctorForm, DoctorRecordForm, QuestionForm, AnswerForm, TopicForm, ItemListForm,DoctorImageForm
from endless_pagination.decorators import page_template 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#return list of parameter for navbar
import itertools
import time	

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

@login_required		

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
		
	
	notifications = Notification.objects.all().order_by('-date_time')
	
	list = []
	for notification in notifications:
		dict = {} 
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
	print "Hello first"
	try:
		patient = get_patient(request.user)
	except:
		patient= None
	if patient: 
		if request.method =='POST':
			ask_form = QuestionForm(data = request.POST)
			if ask_form.is_valid():	
				question = ask_form.save(commit=False)
				question.created_patient = patient
				question.save() 
				print "Hello"
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
			return render_to_reponse('icare/content/question_index.html', context_dict, context)
	
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
	can_answer = False 
	is_doctor = False
	is_patient = False 
	if doctor:
		can_answer = True 
		is_doctor = True
	if patient:
		is_patient = True
		
	question = Question.objects.get(id=question_id)
	answers = Answer.objects.filter(related_question = question).order_by('-thanks','-agree')
	list = []
	for answer in answers:
		dict = {} 
		dict['answer'] = answer 
		if is_patient:
			is_thanked = False
			thank = ThanksAnswer.objects.filter(answer=answer,patient=patient)
			if thank:
				is_thanked = True 
			dict['is_thanked'] = is_thanked 	
		if is_doctor:
			is_agreed = False
			agree = AgreeAnswer.objects.filter(answer=answer,doctor=doctor)
			if agree:
				is_agreed = True 
			dict['is_agreed'] = is_agreed 	
		list.append(dict)	
		
	context_dict['can_answer'] = can_answer
	context_dict['question']= question
	context_dict['answers'] = list 
	context_dict['is_doctor'] = is_doctor
	context_dict['is_patient'] = is_patient
	#context_dict['page_template'] = page_template
	
	if can_answer:
		answer_form = AnswerForm()
		context_dict['answer_form'] = answer_form 
	
	if extra_context is not None:
		context_dict.update(extra_context)
		
	return render_to_response(template, context_dict, context)

@login_required 
def question_answer(request,question_id):
	print "Hello"
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
				print "save"
				doctor_record.number_answer = doctor_record.number_answer + 1
				doctor_record.save()
				
				return HttpResponseRedirect('/icare/question/show/'+str(question_id)+'/')
			else:
				print answer_form.errors 
		else:
			answer_form = AnswerForm()
			
			context_dict['answer_form'] = answer_form 
			return render_to_reponse('icare/content/question_show.html',context_dict,context)
			
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
		agree = answer.agree 
		created_doctor_record.doctor_recommendation = created_doctor_record.doctor_recommendation + 1 
		created_doctor_record.save()
		
        
	return HttpResponse(agree)
	
    
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
    
	if thanks_check == 1:
		past_thanks = ThanksAnswer.objects.filter(answer=answer, patient=patient)
		past_thanks.delete()
		answer.thanks = answer.thanks -1 
		answer.save()
		thanks = answer.thanks
		created_doctor_record.patient_recomemdation = created_doctor_record.patient_recommendation - 1 
		created_doctor_record.save()
	else:
		answer.thanks = answer.thanks + 1
		answer.save()
		ThanksAnswer.objects.get_or_create(answer=answer, patient=patient)
		thanks = answer.thanks
		created_doctor_record.patient_recommendation = created_doctor_record.patient_recommendation + 1
		created_doctor_record.save()
	
	return HttpResponse(thanks)
	
@login_required 
def category_show(request):
	context = RequestContext(request)
	context_dict = {}
	
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
	category_list = []
	
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
		
	user_patient = get_patient(request.user)
	
	
	
	goal = Goal.objects.get(id = goal_id)
	checklists =  CheckList.objects.filter(related_goal = goal_id)
	
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
			if agree:
				is_agreed = True 
			checklist_dict['is_agreed'] = is_agreed
		if patient:
			is_thanked = False 
			thank = ThanksChecklist.objects.filter(checklist=checklist,patient=user_patient)
			if thank:
				is_thanked = True 
			checklist_dict['is_thanked'] = is_thanked
		checklist_list.append(checklist_dict)
	
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
	
	goal = Goal.objects.get(id = int(topic_id))
	if doctor:
		checklist = CheckList() 
		checklist.related_doctor = doctor  
		checklist.related_goal = goal 
		checklist.save()
		notification = Notification(checklist = checklist)
		notification.save()
	else:	
		return HttpReponse('You need to be a doctor to add a new checklist')
	
	return HttpResponseRedirect('/icare/' +str(goal.id)+'/check_lists/')
	
def doctor_edit_checklist(request,checklist_id):
	context = RequestContext(request)
	context_dict = {}
	checklist = CheckList.objects.get(id=int(checklist_id))
	items = ListItem.objects.filter(related_checklist=checklist)
	doctor = checklist.related_doctor
	context_dict = {'checklist':checklist,'items':items,'doctor':doctor}
	
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
	
	if checklist_count==1:
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
		checklist_old = AgreeChecklist.objects.get(checklist=checklist, doctor= doctor).count()
		checklist.agree = checklist.agree - 1 
		checklist.save()
		checklist_old.delete()
		related_doctor_record.doctor_recommendation = related_doctor_record.doctor_recommendation - 1 
		related_doctor_record.save()
	else:
		AgreeChecklist.objects.get_or_create(checklist= checklist, doctor= doctor)
		checklist.agree = checklist.agree + 1 
		checklist.save()
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
	index = UserChecklistIndex.objects.get(user=patient, checklist=user_checklist)
	
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
	
	done = False
	if request.method == 'GET':
		condition = request.GET['condition']
		done = True 
	if done: 
		#page_template = result_template 
		result_list = Condition.objects.filter(title__icontains=condition).order_by('-topic__title')
	
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
	
	done=False
	if request.method == 'GET':
		doctor = request.GET['doctor']
		done = True 
	if done: 
		#page_template = result_template 
		result_list = Doctor.objects.filter(name__icontains = doctor).order_by('name')
	
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
	
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
	#template = 'icare/content/topic_show.html'
	#page_template ='icare/content/topic_show_page.html'
	print type(topic_id)
	topic_id = int(topic_id)
	topic_main = Topic.objects.get(id=topic_id)
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
	if topics_follow:
		is_follow = True 
	print "is_follow:",is_follow	
	topic_form = TopicForm()			
	question_form = QuestionForm()
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
	if request.method == 'POST':
		question_form = QuestionForm(data=request.POST)
		if question_form.is_valid():
			question = question_form.save(commit=False)
			question.save() 
			question.related_topic.add(topic) 
			question.save() 
			return HttpResponseRedirect('/icare/topic/show/'+str(topic_id)+'/')
		else:
			return HttpResponse(question_form.errors)
@login_required 
def profile_doctor(request, doctor_id): 
	context = RequestContext(request)
	context_dict = {} 
	
	parameter_index = get_user_list(request.user)
	
	print parameter_index['is_doctor']
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
	curruser = request.user
	currdoctor = get_doctor(request.user)
	
	doctor_user = User.objects.get(id = int(doctor_id))
	doctor = Doctor.objects.get(user = doctor_user)
	myaccount = False 
	
	is_patient = True  
	
	if currdoctor:
		is_patient = False 
		if currdoctor.id == doctor.id:
			myaccount = True 
			
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
	except:
		request = None
	try:
		request_re = FriendShipRequest.object.filter(from_user=doctor_user, to_user = curruser)
	except:
		request_re = None
		
	if request or request_re:
		is_request = True
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
	
	if is_patient:
		patient_curr = get_patient(curruser)
		
		advisor_request = AdvisorRequest.objects.filter(from_patient=patient_curr)
		if advisor_request:
			is_request_advisor = True
		
		
		if patient_curr.advisor == doctor:
			is_advisor = True 
			
	if is_patient and not myaccount and not is_advisor and not is_request_advisor:
		can_be_advisor = True
		
	print "can_be_advisor",can_be_advisor	
	
	doctor_record_form = DoctorRecordForm(instance=doctor_record)
	topic_form = TopicForm()
	doctor_image_form = DoctorImageForm(instance=currdoctor)
	context_dict = {'is_friend':is_friend,'is_advisor': is_advisor,'can_be_advisor':can_be_advisor,'doctor': doctor, 'doctor_record': doctor_record, 'myaccount': myaccount, 'can_request': can_request,'topic_list':topic_list,'doctor_record_form':doctor_record_form,'topic_form':topic_form,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor'],'doctor_image_form':doctor_image_form}
	
	return render_to_response('icare/doctor/doctor_profile.html',context_dict, context)
	
def profile_patient(request, patient_id): 
	context = RequestContext(request)
	context_dict = {} 
	
	parameter_index = get_user_list(request.user)
	currpatient = get_patient(request.user)
	
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
	
	friend = Friend.objects.filter(to_user = request.user , from_user = patient.user)
	friend_re = Friend.objects.filter(to_user = patient.user, from_user = request.user)
	if friend or friend_re:	
		is_friend = True
	
	request = FriendShipRequest.objects.filter(to_user = request.user, from_user = patient.user)
	try:
		request_re = FriendShipRequest.objects.filter(to_user = patient.user, from_user = request.user)
	except:
		request_re = None 
	if request or request_re:
		is_request = True 
		
	can_request = False 
	if is_doctor and not myaccount and not is_friend and not is_request: 
		can_request = True

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
		
	context_dict = {'patient':patient ,'is_underweight':is_underweight,'is_healthy':is_healthy,'is_slightly':is_slightly,'is_overweight':is_overweight ,'patient_record': patient_record, 'myaccount': myaccount, 'can_request' : can_request,'vaccinations':vaccinations,'user_checklist':user_checklist,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']}
	
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
	return HttpResponse('success')
	
def patient_send_request(request): # doctor send request to specific patient
	context = RequestContext(request)
	
	patient_id = None
	if request.method == 'GET':
		patient_id = request.GET['patientid']
	
	requested_patient = Patient.objects.get(id = int(patient_id))
	to_patient = requested_patient.user 
	from_doctor = request.user 
	Friend.objects.add_friend(from_doctor, to_patient) 
	
	return HttpResponse('success')

def doctor_send_request(request): # patient send request to specific doctor 
	context = RequestContext(request)
	
	doctor_id = None 
	if request.method == 'GET':
		doctor_id = request.GET['doctorid']
	
	requested_doctor =  Doctor.objects.get(id = int(doctor_id))
	to_doctor = requested_doctor.user 
	from_patient = request.user 
	Friend.objects.add_friend(from_patient, to_doctor)
	
	return HttpResponse('sucess')

def patient_friend_list(request): #display friend list of patient 
	context = RequestContext(request)
	context_dict = {} 
	
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
	user = request.user 
	patient = Patient.objects.get(user = user)
	
	user_friend_list = Friend.objects.friends(user) 
	
	context_dict = {'patient': patient , 'user_friend_list': user_friend_list,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']}
	
	return render_to_response('icare/patient/patient_friend_list.html', context_dict, context)
	
def doctor_friend_list(request): #display friend list of doctor 
	context = RequestContext(request)
	context_dict = {} 
	
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
	user = request.user 
	doctor = Doctor.objects.get(user = user)

	user_friend_list = Friend.objects.friends(user)

	context_dict = {'doctor': doctor, 'user_friend_list':user_friend_list,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']}

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
	doctor_unrejected_request_list = FriendShipRequest.objects.filter(to_user=patient_user,rejected=False,viewed_by_patient= False).order_by('-created') # return a friend list of doctor
	doctor_rejected_request_list = FriendShipRequest.objects.filter(from_user=patient_user,rejected=True,viewed_by_patient = False).order_by('-created')
	doctor_accepted_request_list = FriendShipRequest.objects.filter(from_user=patient_user,accepted=True,viewed_by_patient=False).order_by('-created')
	
	advisor_accepted_list = AdvisorRequest.objects.filter(from_patient = patient_account,accepted=True, viewed_by_patient = False).order_by('-created')
	advisor_rejected_list = AdvisorRequest.objects.filter(from_patient = patient_account,rejected=True,viewed_by_patient=False).order_by('-created')
	answer_alert_list = AnswerAlert.objects.filter(to_patient=patient_account , viewed_by_patient=False).order_by('-created')
	list = []
	for doctor_unrejected_request, doctor_rejected_request, doctor_accepted_request, advisor_accepted,advisor_rejected, answer_alert in itertools.izip_longest(doctor_unrejected_request_list,doctor_rejected_request_list,doctor_accepted_request_list,advisor_accepted_list,advisor_rejected_list,answer_alert_list):
		dict = {}
		is_unrejected_request = False 
		if doctor_unrejected_request:
			is_unrejected_request = True 
			dict['unrejected_request'] = get_doctor(doctor_unrejected_request.from_user) 
		dict['is_unrejected_request'] = is_unrejected_request
		
		is_rejected_request = False 
		if doctor_rejected_request:
			is_rejected_request = True 
			dict['rejected_request'] = get_doctor(doctor_rejected_request.to_user)
		dict['is_rejected_request'] = is_rejected_request	
		
		is_accepted_request = False 
		if doctor_accepted_request:
			is_accepted_request = True
			dict['accepted_request'] = get_doctor(doctor_accepted_request.to_user)
		dict['is_accepted_request'] = is_accepted_request
		
		is_advisor_accepted = False 
		if advisor_accepted:
			is_advisor_accepted = True 
			dict['advisor_accepted'] = advisor_accepted.to_doctor
		dict['is_advisor_accepted'] = is_advisor_accepted
		 
		is_advisor_rejected = False 
		if advisor_rejected:
			is_advisor_rejected = True 
			dict['advisor_rejected'] = advisor_rejected.to_doctor
		dict['is_advisor_rejected'] = is_advisor_rejected
		
		is_answer_alert = False 
		if answer_alert:
			is_answer_alert = True 
			dict['answer_alert'] = answer_alert
			
		dict['is_answer_alert'] = is_answer_alert 
		list.append(dict)
	
	context_dict['list'] = list 
	#context_dict = {'patient_user': to_user , 'doctor_request_users': from_user,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']}
	
	return render_to_response('icare/patient/notification_patient.html', context_dict, context)
	
def doctor_notification_request(request):# display friend request from patient to doctor 
	context = RequestContext(request)
	context_dict = {} 
	
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
	doctor_user = request.user # return doctor user 
	doctor_account = get_doctor(doctor_user)
	patient_unrejected_request_list = FriendShipRequest.objects.filter(to_user=doctor_user,rejected=False,viewed_by_doctor= False).order_by('-created') # return a friend list of doctor
	patient_rejected_request_list = FriendShipRequest.objects.filter(from_user=doctor_user,rejected=True,viewed_by_doctor= False).order_by('-created')
	patient_accepted_request_list = FriendShipRequest.objects.filter(from_user=doctor_user,accepted=True,viewed_by_doctor=False).order_by('-created')
	
	advisor_request_list = AdvisorRequest.objects.filter(to_doctor = doctor_account,accepted=False,viewed_by_doctor = False).order_by('-created')
	question_alert_list = QuestionAlert.objects.filter(to_doctor=doctor_account, view_by_doctor=False).order_by('-create')
	
	list = []
	for patient_unrejected_request, patient_rejected_request, patient_accepted_request, advisor_request, question_alert in itertools.izip_longest(patient_unrejected_request_list,patient_rejected_request_list,patient_accepted_request_list,advisor_request_list,question_alert_list):
		dict = {}
		is_unrejected_request = False 
		if patient_unrejected_request:
			is_unrejected_request = True 
			patient_user_unrejected_request=get_patient(patient_unrejected_request.from_user)
			dict['unrejected_request'] = patient_user_unrejected_request
		
		dict['is_unrejected_request'] = is_unrejected_request
		
		is_rejected_request = False 
		if patient_rejected_request:
			is_rejected_request = True 
			patient_user_rejected_request =get_patient(patient_rejected_request.to_user)
			dict['rejected_request'] = patient_user_rejected_request
			
		dict['is_rejected_request'] = is_rejected_request	
		
		is_accepted_request = False 
		if patient_accepted_request:
			is_accepted_request = True
			patient_user_accepted_request=get_patient(patient_accepted_request.to_user)
			dict['accepted_request'] = patient_user_accepted_request
		
		dict['is_accepted_request'] = is_accepted_request
		
		is_advisor_request = False 
		if advisor_request:
			is_advisor_request = True 
			dict['advisor_request'] = advisor_request.from_patient 
		
		dict['is_advisor_request'] = is_advisor_request
		
		
		is_question_alert = False 
		if question_alert:
			is_question_alert = True 
			dict['question_alert'] = question_alert
			
		dict['is_question_alert'] = is_question_alert 
		list.append(dict)
	
	context_dict['list'] = list 
	#context_dict = {'doctor_user':to_user, 'patient_request_users': from_user,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']}
	
	return render_to_response('icare/doctor/notification_doctor.html', context_dict, context)
	
def doctor_friend_accept(request): #  patient accept friend request from doctor
	context = RequestContext(request)
	doctor_id = None 
	if request.method == 'GET':
		doctorid = request.GET['doctorid']
		
	patient_user = User.objects.get(username = request.user)
	doctor_user = Doctor.objects.get(id = int(doctorid))
	
	f_request = FriendShipRequest.objects.get(from_user = doctor_user.user, to_user = patient_user)
	f_request.accepted = True 
	f_request.viewed_by_patient = True
	f_request.save() 
	
	if f_request.viewed_by_doctor:
		f_request.delete()
	
	relation1 = Friend.objects.get_or_create(to_user= patient_user,from_user= doctor_user.user)
	relation2 = Friend.objects.get_or_create(to_user = doctor_user.user,from_user = patient_user)
	
	return HttpResponse('success')
	
	
#patient viewd their accepted request 
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
	if a_request.viewed_by_doctor:
		a_request.delete()
		
	return HttpResponse('success')

	
#patinet view advisor answer 

def patient_doctor_answer_alert(request):
	context = RequestContext(request)
	answerid = None 
	if request.method == 'GET':
		answerid = request.GET['answerid']

	a_answer = AnswerAlert.objects.get( id=answerid )
	a_answer.viewed_by_patient = True 
	a_answer.save() 
	
	
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
	if f_request.viewed_by_patient:
		f_request.delete()
		
	relation1 = Friend.objects.get_or_create(to_user= patient_user.user,from_user= doctor_user.user)
	relation2 = Friend.objects.get_or_create(to_user = doctor_user.user,from_user = patient_user.user)
	
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
	if f_request.viewed_by_patient:
		f_request.delete()
	return HttpReponse('success ')
	
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
	if f_request.viewed_by_patient:
		f_request.delete()
		
	return HttpReponse('success ')	
	
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
	
	return HttpResponse('success')	
	
def doctor_view_question_alert(request):
	context = RequestContext(request)
	questionid = None 
	if request.method == 'GET':
		questionid = request.GET['questionid']
		
	
	a_question = QuestionAlert.objects.get(id=questionid)
	a_question.viewed_by_doctor = True 
	a_question.save() 
	
	return HttpResponse('success')
		
def user_changepass(request):
	context = RequestContext(request)
	context_dict = {}
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
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
	print "helo"
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
	print html
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
				doctor_record.number_create_topic = doctor_record.number_create_topic + 1 
				return HttpResponseRedirect('/icare/profile/doctor/'+str(request.user.id)+'/')
			else:
				print topic_form.errors 
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
				doctor_record.number_create_topic = doctor_record.number_create_topic + 1 
				return HttpResponseRedirect('/icare/topic/show/'+str(topic.id)+'/')
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
		if topic.created_doctor != doctor:
			return HttpResponseForbidden() 
		if request.method == 'POST':
			topic_form = TopicForm(request.post, request.FILES, instance=topic) 
			if topic_form.is_valid():
				if 'image' in request.FILES:	
					topic.image = request.FILES['image']
				topic_form.save() 
				return HttpResponseRedirect('/icare/topic/'+str(topic_id)+'/')
			else:	
				print topic_form.errors
		else:	
			topic_form = TopicForm(instance=topic)
			
		return render_to_response('icare/content/topic_edit.html',{'topic_form':topic_form,'topic_id':topic_id,'curruserid':parameter_index['curruserid'],'is_navbar_doctor':parameter_index['is_doctor']},context)
	else:	
		return HttpResponse('You need to be a doctor to edit')
#delete userchecklist 

#doctor edit profile 

def doctor_edit_profile(request,doctor_record_id):
	context = RequestContext(request)
	context_dict = {} 
	doctor_record = get_object_or_404(DoctorRecord,pk=doctor_record_id)
	doctor = doctor_record.doctor
	
	if request.method == 'POST':
		doctor_record_form = DoctorRecordForm(request.POST, instance=doctor_record)
		doctor_image_form = DoctorImageForm(request.FILES,instance=doctor)
		if doctor_record_form.is_valid() and doctor_image_form.is_valid():	
			doctor_record_form.save() 
			doctor_image = doctor_image_form.save(commit=False)
			if 'doctor_image' in request.FILES:
				doctor_image.doctor_image = request.FILES['doctor_image']

			doctor_image.save()
			
			return HttpResponseRedirect('/icare/profile/doctor/'+str(doctor.user.id)+'/')
		else:
			print doctor_record_form.errors
	else:
		doctor_record_form = DoctorRecordForm(instance=doctor_record)
		context_dict['doctor_record_form'] = doctor_record_form
		return render_to_response('icare/doctor/doctor_profile.html',context_dict,context)

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
	return{'curruserid':userid, 'is_doctor': is_doctor}
	
#view advisor doctor 
def patient_view_advisor(request,patient_id,template=None, extra_context=None):
	context = RequestContext(request)
	context_dict = {}
	
	parameter_index = get_user_list(request.user)
	context_dict['curruserid'] = parameter_index['curruserid']
	context_dict['is_navbar_doctor'] = parameter_index['is_doctor']
	
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
	
	topic_follow = TopicFollow.objects.get_or_create(user=user,topic=topic)

	
	return HttpResponse('Success')