from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache 
from django.core.exceptions import ValidationError
from icare.list import DOCTOR_DEGREE, DOCTOR_SPECIALTY, YEAR 
from django.utils.translation import gettext as _

from icare.exceptions import AlreadyExistsError 
CACHE_TYPES = {
	'friends':'f-%d',
	'requests':'r-%d',
	'sent_requests':'sfr-%d',
	'unread_requests':'fru-%d',
	'unread_request_count':'fruc-%d',
	'rejected_requests':'frj-%d',
	'unrejected_requests':'frur-%d',
	'unrejected_request_count':'frurc-%d'}
	
BUST_CACHES = {
	'friends':['friends'],
	'requests': [
		'requests',
		'unread_request',
		'unread_request_count',
		'rejected_requests',
		'unrejected_requests',
		'unrejected_request_count'],
	'sent_requests':['sent_requests']}

def cache_key(type, user_pk):
	return CACHE_TYPES[type] % user_pk 
	
def bust_cache(type, user_pk):
	busts_key = BUST_CACHES[type] % user_pk 
	keys =[CACHE_TYPES[k] % user_pk for k in busts_key]
	cache.delete_many(keys)
	
# Create your patient model.
GENDER_CHOICES = (
	('Male','Male'),
	('Female','Female'),
	)


ETHNICITY = (
	('Caucasian','Caucasian'),
	('African Ameracan','African American'),
	('Hispanic','Hispanic'),
	('South Asian','South Asian'),
	('East Asian','East Asian'),
	('African','African'),
	('East African','East African'),
	('other','other')
	)
DIETARY_RESTRICTION = (
	('Ovo-Vegetarian','Ove-Vegetarian'),
	('Lacto-Vegetarian','Lacto-Vegetarian'),
	('Vegetarian','Vegetarian'),
	('Vegan','Vegan'),
	('Pescantarian','Pescantarian'),
	('Gluten-Free','Gluten-Free'),
	('Lactoso Intolerant','Lactose Intolerant'),
	('None','None'),
	)
ALCOHOL = (
	('Social Drinker','Social Drinker'),
	('Modearate Drinker','Modearate Drinker'),
	('Heavy Drinker','Heavy Drinker'),
	('Not a Drinker','Not a Drinker'),
	)
SEX_ACTIVE= (
	('Not sexually active','Not sexually active'),
	('Men','Men'),
	('Woman','Woman'),
	('Both','Both'),
	)
TOBACCO = (
	('Never smoker or chewed','Never smokerd or chewed'),
	('Yes, 0-2 packs a month','Yes, 0-2 packs a month'),
	('Yes, 0-2 packs a week','Yes, 0-2 packs a week'),
	('Yes, 0-2 packs a day', 'Yes, 0-2 packs a day'),
	('Yes, more than 2 packs a day','Yes, more than 2 packs a day'),
	('Yes, chewing tobacco','Yes, chewing tobacco'),
	)
RECREATIONAL_DRUGS = (
	('None','None'),
	('Psychedelic Mushrooms','Psychedelic Mushrooms'),
	('Barbiturates','Barbuturates'),
	('Ecstasy','Ecastasy'),
	('Heroin','Heroin'),
	('Methamphetamines','Methmaphetamines'),
	('Cocaine','Cocaine'),
	('Marijuana','Marijuana'),
	('Other','Other')
	)
	
	

# create your doctor models 
certification_CHOICES = (
	('A', 'America Board'),
	('B','Bachelor'),
	)
	
class Doctor(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100)
	specialty = models.CharField(max_length=100, choices=DOCTOR_SPECIALTY)
	gender = models.CharField(max_length=100, choices= GENDER_CHOICES)
	school = models.CharField(max_length=100)
	doctor_image = models.ImageField(null=True, blank=True, upload_to='Doctor_profiles')
	license = models.IntegerField()
	degree = models.CharField(max_length=100,choices=DOCTOR_DEGREE)
	year = models.IntegerField(default=2015, choices=YEAR)
	address = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name
		
class Patient(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100)
	birthday = models.DateField()
	gender = models.CharField(max_length=10, choices= GENDER_CHOICES)
	patient_image = models.ImageField(null=True, blank= True, upload_to='patient_profiles')
	address = models.CharField(max_length=100) 
	advisor = models.ForeignKey(Doctor,null=True,blank=True)
	
	def __unicode__(self):
		return self.name
	
		
class DoctorRecord(models.Model):
	doctor = models.OneToOneField(Doctor)
	doctor_information = models.TextField()
	doctor_recommendation = models.IntegerField(default=0)
	patient_recommendation = models.IntegerField(default=0)
	language = models.CharField(max_length=500)
	number_answer = models.IntegerField(default=0)
	number_create_item_checklist = models.IntegerField(default=0)
	number_create_topic = models.IntegerField(default=0)
	
	def _point_caculation(self):
		return (self.doctor_recommendation*20 + self.patient_recommendation*8 + self.number_answer*40 + self.number_create_item_checklist*20 + self.number_create_topic*90)
	
	total_point = property(_point_caculation)
	
	def _star_ranking(self):
		if self.total_point >=0 and self.total_point<2001:
			return 1 
		elif self.total_point >= 2001 and self.total_point < 4501:
			return 2
		elif self.total_point >= 4501 and self.total_point <7501:
			return 3
		elif self.total_point >= 7501 and self.total_point < 11001:
			return 4 
		else: 
			return 5 
	star = property(_star_ranking)
		
	def __unicode__(self):
		return self.doctor.name 
		
#managing private question from patient 
class AnswerAlert(models.Model):
	to_patient = models.ForeignKey(Patient)
	from_doctor = models.ForeignKey(Doctor)
	created = models.DateTimeField(auto_now_add=True)
	
	viewed_by_patient = models.BooleanField(default=False)
	def __unicode__(self):
		return "answer doctor %s to patient %s"%(self.from_doctor.name, self.to_patient.name)

class QuestionAlert(models.Model):
	to_doctor = models.ForeignKey(Doctor)
	from_patient = models.ForeignKey(Patient)
	create = models.DateTimeField(auto_now_add=True)
	
	view_by_doctor = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "question patient %s to doctor %s "%(self.from_patient.name,self.to_doctor.name)

# managing relation between doctor and patient 
class AdvisorRequest(models.Model):
	from_patient = models.ForeignKey(Patient)
	to_doctor = models.ForeignKey(Doctor)
	
	created = models.DateTimeField(auto_now_add= True)
	rejected = models.BooleanField(default = False)
	viewed_by_patient = models.BooleanField(default= False)
	viewed_by_doctor = models.BooleanField(default= False)
	accepted = models.BooleanField(default = False)
	def __unicode__(self):
		return "patient %s advisor request %s "%(self.from_patient.name,self.to_doctor.name)

		
class FriendShipRequest(models.Model):
	from_user = models.ForeignKey(User, related_name='friendship_request_sent')
	to_user = models.ForeignKey(User, related_name='friendship_requests_received')
	
	created = models.DateTimeField(auto_now_add=True)
	rejected = models.BooleanField(default = False)
	viewed_by_doctor = models.BooleanField(default= False)
	viewed_by_patient = models.BooleanField(default= False)
	accepted = models.BooleanField(default = False )
	
	class Meta:
		verbose_name = _('Friendship Request')
		verbose_name_plural = _('Friendship Requests')
		unique_together = ('from_user','to_user')
		
	def __unicode__(self):
		return "user %s friendship request %s"%(self.from_user.username, self.to_user.username)
	
	def accept(self):
		# accept this friendship request 
		
		self.save() 
		relation1 = Friend.objects.create(
			to_user= self.to_user,
			from_user= self.from_user)
		
		relation2 = Friend.objects.create(
			to_user = self.from_user,
			from_user = self.to_user)
	
		
		self.accepted = True 
		self.save()
		
		
		
	def reject(self):
		# reject a friendship request 
		self.reject = True
		self.save() 
		#friendship_request_rejected.send(sender=self)

class FriendshipManger(models.Manager):
	""
	def friends(self, user):# return a list of friends
		
		qs = Friend.objects.filter(to_user=user).all()
		friends = [u.from_user for u in qs] # return a list of friend related to current user 
		
		return friends 
	
	def request(self, user):
		# display a list of  unrejected friendship request 
		qs = FriendshipRequest.objects.filter(
				to_user=user).all()
		requests = qs 
		
		return requests 
	
	def sent_requests(self, user):
		""" Return a list of friendship requests from user """
		qs = FriendShipRequest.objects.filter(from_user=user).all()
		requests = qs
			

		return requests

	def unread_requests(self, user):
		""" Return a list of unread friendship requests """
		qs = FriendShipRequest.objects.filter(to_user=user,viewed=False).all()
		unread_requests = qs
			

		return unread_requests

	def unread_request_count(self, user):
		""" Return a count of unread friendship requests """
		count = FriendShipRequest.objects.filter(to_user=user,viewed = False).count()
		

		return count

	def read_requests(self, user):
		""" Return a list of read friendship requests """
		qs = FriendShipRequest.objects.filter(to_user=user,viewed=True).all()
		read_requests = qs
			

		return read_requests

	def rejected_requests(self, user):
		""" Return a list of rejected friendship requests """
		qs = FriendShipRequest.objects.filter(to_user=user,rejected=True).all()
		rejected_requests = qs
		return rejected_requests

	def unrejected_requests(self, user):
		""" All requests that haven't been rejected """
		qs = FriendShipRequest.objects.filter(to_user=user,rejected = False).all()
		unrejected_requests = [u.from_user for u in qs] 
		return unrejected_requests

	def unrejected_request_count(self, user):
		""" Return a count of unrejected friendship requests """
		count = FriendShipRequest.objects.filter(to_user=user,rejected=False).count()
		return count
		
	def add_friend(self, from_user, to_user):
		""" Create a friendship request """
		if from_user == to_user:
			raise ValidationError("Users cannot be friends with themselves")
		request, created = FriendShipRequest.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
            
        )
		if created is False:
			raise AlreadyExistsError("Friendship already requested")
		
		#friendship_request_created.send(sender=request)

		return request
	
class Friend(models.Model):
	to_user = models.ForeignKey(User,related_name='friends')
	from_user = models.ForeignKey(User,related_name='_unused_friend_relation')
	created = models.BooleanField(default=False)
	
	objects = FriendshipManger()
	class Meta:
		verbose_name = _('Friend')
		verbose_name_plural = _('Friends')
		unique_together = ('from_user','to_user')
		
	def __unicode__(self):
		return "User %s is friends with %s"%(self.to_user.username,self.from_user.username)
		
	def save(self, *args, **kwargs):
		# Ensure users can't be friends with themselves 
		if self.to_user == self.from_user:
			raise ValidationError("Users cannot be friends with themselves")
		super(Friend, self).save(*args,**kwargs)

PRIORITY_CHOICES = (
	('Low','Low'),
	('Normal','Normal'),
	('High','High'),
	)		
	

class Category(models.Model):
	title = models.CharField(max_length=128, unique=True)
	image = models.ImageField(null = True, blank = True , upload_to = 'category_images')
	
	
	def __unicode__(self):
		return self.title

class Goal(models.Model):
	title = models.CharField(max_length=128, unique = True)
	image = models.ImageField(null= True, blank = True, upload_to = 'goal_images')
	number_of_checklist = models.IntegerField(default = 0)
	def _count_item(self):
		return self.checklists.count()
	count_checklist = property(_count_item)
	related_category = models.ForeignKey(Category, related_name = 'goals')
	
	def __unicode__(self): 
		return self.title 
		
		
class Topic(models.Model):
	related_topic = models.ManyToManyField('self',related_name = 'topics',blank=True)
	title = models.CharField(max_length = 128,unique = True)
	definition = models.TextField()
	image = models.ImageField(null= True , blank = True, upload_to='topic_images')
	image_description = models.CharField(max_length=500,null= True , blank = True)
	related_goal = models.ManyToManyField(Goal,blank=True)
	created_doctor = models.ForeignKey(Doctor,blank=True, null=True)
	create_time = models.DateTimeField(auto_now_add=True)
	agree = models.IntegerField(default=0)
	def __unicode__(self):
		return self.title 
		
class TopicFollow(models.Model):
	user = models.ForeignKey(User)
	topic = models.ForeignKey(Topic)
	created = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return "user %s follow topic %s"%(self.user.username,self.topic.title)
		
class TopicAgree(models.Model):
	doctor = models.ForeignKey(Doctor)
	topic = models.ForeignKey(Topic)
	
	def __unicode__(self):
		return "doctor %s has agree on %s"%(self.doctor.name,self.topic.title)
		
class CheckList(models.Model):
	#title = models.CharField(max_length=128, unique=True)
	use = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	agree= models.IntegerField(default=0)
	related_doctor = models.ForeignKey(Doctor, related_name='checklists')
	related_goal = models.ForeignKey(Goal, related_name='checklists')
	create_time = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.related_goal.title + "'s "  +self.related_doctor.name

class ThanksChecklist(models.Model):
	checklist = models.ForeignKey(CheckList)
	patient = models.ForeignKey(Patient)
	
	def __unicode__(self):
		return self.patient.name
	
class AgreeChecklist(models.Model):
	checklist = models.ForeignKey(CheckList)
	doctor = models.ForeignKey(Doctor)
	
	def __unicode__(self):
		return self.doctor.name 
	
class ListItem(models.Model):
	title = models.TextField()
	priority = models.CharField(max_length=50,choices=PRIORITY_CHOICES)
	frequency = models.CharField(max_length=100)
	related_checklist = models.ForeignKey(CheckList, related_name='items')
	
	
	def __unicode__(self):
		return self.title 
		
	class Meta:
		ordering = ['-priority']


class UserCheckList(models.Model):
	related_doctor = models.ForeignKey(Doctor)
	related_goal = models.ForeignKey(Goal, related_name='userchecklist')
	
	related_patient = models.ForeignKey(Patient, related_name='userchecklist')
	
	def __unicode__(self):
		return self.related_goal.title

		
class UserListItem(models.Model):
	title = models.CharField(max_length=128, unique =True)
	priority = models.CharField(max_length=100,choices= PRIORITY_CHOICES)
	completed = models.BooleanField(default = False)
	frequency = models.CharField(max_length=100)
	related_checklist = models.ForeignKey(UserCheckList, related_name='user_items')
	
	def __unicode__(self):
		 return self.title 
	class Meata:
		ordering = ['-priority']

# storage 		
class UserChecklistIndex(models.Model):
	user = models.ForeignKey(Patient)
	checklist = models.ForeignKey(CheckList)
	
	def __unicode__(self):
		return "Patient %s 's checlist %d"%(self.user.name,self.checklist.id)
		
class Medication(models.Model):
	topic = models.OneToOneField(Topic, primary_key = True)
	
	def __unicode__(self):
		return self.topic.title 

class Vaccination(models.Model):
	medication = models.OneToOneField(Medication, primary_key = True)
	
	def __unicode__(self):
		return self.medication.topic.title 

class Condition(models.Model):
	topic = models.OneToOneField(Topic, primary_key= True)

	def __unicode__(self):
		return self.topic.title 

class Riskfactor(models.Model):
	topic = models.OneToOneField(Topic, primary_key = True)
	family = models.BooleanField(default = False)
	personal = models.BooleanField(default = False)
	
	def __unicode__(self):
		return self.topic.title
		
class Symptom(models.Model):
	topic = models.OneToOneField(Topic, primary_key = True)
	
	def __unicode__(self):
		return self.topic.title
		
class Procedure(models.Model):
	topic = models.OneToOneField(Topic, primary_key = True)
	
	def __unicode__(self):
		return self.topic.title
		

		
class Question(models.Model):
	title = models.CharField(max_length=800)
	created_patient = models.ForeignKey(Patient,null=True,blank=True)
	related_topic = models.ForeignKey(Topic, related_name = 'topic_questions',null=True,blank=True)
	related_goal = models.ForeignKey(Goal,related_name = 'goal_questions',null=True,blank=True)
	created_time = models.DateTimeField(auto_now_add = True)
	to_doctor = models.ForeignKey(Doctor,null=True,blank=True)
	
	privacy = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.title
		
class Answer(models.Model):
	detail = models.TextField() 
	image = models.ImageField(null= True, blank = True, upload_to='answer_images')
	from_doctor = models.ForeignKey(Doctor)
	related_question = models.ForeignKey(Question, related_name='answers')
	thanks = models.IntegerField(default=0)
	agree = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.detail 
		
class AnswerNotification(models.Model):
	doctor = models.ForeignKey(Doctor)
	to_patient = models.ForeignKey(Patient)
	answer = models.ForeignKey(Answer)
	created = models.DateTimeField(auto_now_add=False)
	viewed_by_patient = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "doctor %s answer %d"%(self.doctor.name,self.answer.id)
		
class ThanksAnswer(models.Model):
    answer = models.ForeignKey(Answer)
    patient = models.ForeignKey(Patient)
    
    def __unicode__(self):
        return self.patient.name 

class AgreeAnswer(models.Model):
    answer = models.ForeignKey(Answer)
    doctor = models.ForeignKey(Doctor)
    
    def __unicode__(self):
        return self.doctor.name 

class PatientRecord(models.Model):
	patient = models.OneToOneField(Patient)
	ethnicity = models.CharField(max_length=50,choices=ETHNICITY)
	height = models.FloatField(default=0,blank = True)
	weight = models.FloatField( default=0,blank =True)
	vaccination = models.ManyToManyField(Vaccination)
	dietary_restriction = models.CharField( max_length=50,choices=DIETARY_RESTRICTION)
	alcohol = models.CharField(max_length=50, choices=ALCOHOL)
	tobacco = models.CharField(max_length=50, choices=TOBACCO)
	sexually_active = models.CharField(max_length= 50, choices=SEX_ACTIVE)
	recreational_drug = models.CharField(max_length=50, choices=RECREATIONAL_DRUGS)
	
	def _get_bmi_score(self):
		if self.weight == 0 or self.height == 0:
			return 0
		else:
			return round((self.weight/(self.height*self.height)),1)
			
	bmi = property(_get_bmi_score)
	def __unicode__(self):
		return self.patient.name 

class Notification(models.Model):
	date_time = models.DateTimeField(auto_now_add=True)
	question = models.OneToOneField(Question, null=True,blank=True)
	checklist = models.OneToOneField(CheckList, null=True, blank=True)
	topic = models.OneToOneField(Topic,null=True,blank=True)
	
	def __unicode__(self):
		return "Create on %d" % self.date_time
#add related topic follow notification 
class AddTopicFollowNotification(models.Model):
	user = models.ForeignKey(User)
	from_doctor = models.ForeignKey(Doctor)
	topic = models.ForeignKey(Topic,related_name="origin_topic_follow")
	related_topic = models.ForeignKey(Topic,related_name="related_topic_follow")
	created = models.DateTimeField(auto_now_add=True)
	viewed = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "doctor %s add topic %s to user %s"%(self.from_doctor.name,self.topic.title,self.user.username)

class EditTopicFollowNotification(models.Model):
	user = models.ForeignKey(User)
	from_doctor = models.ForeignKey(Doctor)
	topic = models.ForeignKey(Topic)
	created = models.DateTimeField(auto_now_add=True)
	viewed = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "doctor %s edit topic %s to user %s"%(self.from_doctor.name,self.topic.title,self.user.username)
class AddAnswerTopicFollowNotification(models.Model):
	user = models.ForeignKey(User)
	from_doctor = models.ForeignKey(Doctor)
	topic = models.ForeignKey(Topic)
	answer = models.ForeignKey(Answer)
	created = models.DateTimeField(auto_now_add=True)
	viewed = models.BooleanField(default=False)
	def __unicode__(self):
		return "doctor %s answer %d to topic %s to user %s"%(self.from_doctor.name,self.answer.id,self.topic.title,self.user.username)
		
class AddQuestionTopicFollowNotification(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	topic = models.ForeignKey(Topic)
	created = models.DateTimeField(auto_now_add=True)
	viewed = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "question %s add to topic %s to user %s"%(self.question.title,self.topic.title,self.user.username)		
#handle checklist notification 
class ThankChecklistNotification(models.Model):
	from_patient = models.ForeignKey(Patient)
	to_doctor = models.ForeignKey(Doctor)
	checklist = models.ForeignKey(CheckList)
	viewed_by_doctor = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return "patient %s has thank you on checklist %s"%(self.from_patient.name,self.checklist.related_goal.title)

class AgreeChecklistNotification(models.Model):
	from_doctor = models.ForeignKey(Doctor,related_name="from_doctor_agree")
	to_doctor = models.ForeignKey(Doctor,related_name="to_doctor_view")
	checklist = models.ForeignKey(CheckList)
	viewed_by_doctor = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return "doctor %s has thank you on checklist %s"%(self.from_doctor.name,self.checklist.related_goal.title)
#handle answer interact notification 
class ThankAnswerNotification(models.Model):
	from_patient = models.ForeignKey(Patient)
	to_doctor = models.ForeignKey(Doctor)
	answer = models.ForeignKey(Answer)
	viewed_by_doctor = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return "patient %s has thank your on %d answer "%(self.from_patient.name,self.answer.id)

class AgreeAnswerNotification(models.Model):
	from_doctor = models.ForeignKey(Doctor,related_name="from_doctor_agree_answer")
	to_doctor = models.ForeignKey(Doctor,related_name="to_doctor_view_asnwer")
	answer = models.ForeignKey(Answer)
	viewed_by_doctor = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return "doctor %s has agree your on %d answer "%(self.from_doctor.name,self.answer.id)
# doctor add topic notification 		
class AddTopicNotification(models.Model):
	to_patient = models.ForeignKey(Patient)
	from_doctor = models.ForeignKey(Doctor)
	topic = models.ForeignKey(Topic)
	created = models.DateTimeField(auto_now_add=True)
	viewed_by_patient = models.BooleanField(default=False)
	def __unicode__(self):
		return "doctor %s topic %s add to patient %s"%(self.from_doctor.name,self.topic.title,self.to_patient.name)
		
class EditTopicNotification(models.Model):
	to_patient = models.ForeignKey(Patient)
	from_doctor = models.ForeignKey(Doctor)
	topic = models.ForeignKey(Topic)
	created = models.DateTimeField(auto_now_add=True)
	viewed_by_patient = models.BooleanField(default=False)
	def __unicode__(self):
		return "doctor %s topic %s edit to patient %s"%(self.from_doctor.name,self.topic.title,self.to_patient.name)
		
class DoctorNotification(models.Model):
	 doctor = models.ForeignKey(Doctor)
	 
	 thank_checklist = models.ForeignKey(ThankChecklistNotification,null=True,blank=True)
	 agree_checklist = models.ForeignKey(AgreeChecklistNotification,null=True,blank=True)
	 thank_answer = models.ForeignKey(ThankAnswerNotification,null=True,blank=True)
	 agree_answer = models.ForeignKey(AgreeAnswerNotification,null=True,blank=True)
	 add_topic_follow_topic = models.ForeignKey(AddTopicFollowNotification,null=True,blank=True)
	 edit_topic_follow_topic = models.ForeignKey(EditTopicFollowNotification,null=True,blank=True)
	 add_question_follow_topic = models.ForeignKey(AddQuestionTopicFollowNotification,null=True,blank=True)
	 add_answer_follow_topic = models.ForeignKey(AddAnswerTopicFollowNotification,null=True,blank=True)
	 question_alert = models.ForeignKey(QuestionAlert, null=True,blank=True)
	 advisor_request = models.ForeignKey(AdvisorRequest, null=True,blank=True)
	 friend_request = models.ForeignKey(FriendShipRequest,related_name="doctor_friend_request_notification", null=True,blank=True)
	 friend_accept = models.ForeignKey(FriendShipRequest,related_name="doctor_friend_accept_notification", null=True,blank=True)
	 friend_reject = models.ForeignKey(FriendShipRequest,related_name="doctor_friend_reject_notification", null=True,blank=True)
	 def __unicode__(self):
		 return "doctor %s notification %d"%(self.doctor.name,self.id)
		
class EditChecklistNotification(models.Model):
	to_patient = models.ForeignKey(Patient)
	from_doctor = models.ForeignKey(Doctor)
	checklist = models.ForeignKey(CheckList)
	created = models.DateTimeField(auto_now_add=True)
	viewed_by_patient = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "doctor %s checklist %s add to patient %s"%(self.from_doctor.name,self.checklist.id,self.to_patiet.name)

class AddChecklistNotification(models.Model):
	to_patient = models.ForeignKey(Patient)
	from_doctor = models.ForeignKey(Doctor)
	checklist = models.ForeignKey(CheckList)
	created = models.DateTimeField(auto_now_add=True)
	viewed_by_patient = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "doctor %d checklist %s edit to patient %s"%(self.from_doctor.name,self.checklist.id,self.to_patiet.name)		
		
class PatientNotification(models.Model):
	 patient = models.ForeignKey(Patient)
	 
	 add_topic_follow_topic = models.ForeignKey(AddTopicFollowNotification,null=True,blank=True)
	 edit_topic_follow_topic = models.ForeignKey(EditTopicFollowNotification,null=True,blank=True)
	 add_question_follow_topic = models.ForeignKey(AddQuestionTopicFollowNotification,null=True,blank=True)
	 add_answer_follow_topic = models.ForeignKey(AddAnswerTopicFollowNotification,null=True,blank=True)
	 add_topic = models.ForeignKey(AddTopicNotification, null=True,blank=True)
	 edit_topic = models.ForeignKey(EditTopicNotification, null=True,blank=True)
	 add_checklist = models.ForeignKey(AddChecklistNotification, null=True,blank=True)
	 edit_checklist = models.ForeignKey(EditChecklistNotification, null=True,blank=True)
	 answer_doctor_follow = models.ForeignKey(AnswerNotification, null=True,blank=True) 
	 answer_alert = models.ForeignKey(AnswerAlert, null=True,blank=True)
	 advisor_reject = models.ForeignKey(AdvisorRequest,related_name="patient_advisor_reject", null=True,blank=True)
	 advisor_accept = models.ForeignKey(AdvisorRequest,related_name="patient_advisor_accpet", null=True,blank=True)
	 friend_request = models.ForeignKey(FriendShipRequest,related_name='patient_friend_request_notification', null=True,blank=True)
	 friend_reject = models.ForeignKey(FriendShipRequest,related_name='patient_friend_reject_notification', null=True,blank=True)
	 friend_accept = models.ForeignKey(FriendShipRequest,related_name='patient_friend_accept_notification', null=True,blank=True)
	
	 def __unicode__(self):
		 return "patient %s notification %d"%(self.patient.name,self.id)
		
class Feedback(models.Model):
	detail = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return "feedback %d created one %d"%(self.id,self.created)
		
