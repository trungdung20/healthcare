from django.contrib import admin 
from icare.models import Doctor, Patient, PatientRecord, DoctorRecord, FriendShipRequest, Friend, Category, Goal, CheckList, ListItem, UserCheckList, UserListItem, Topic, Condition, Riskfactor, Symptom, Procedure, Medication, Question, Answer, Vaccination, ThanksChecklist, AgreeChecklist, AgreeAnswer, ThanksAnswer,AdvisorRequest,AnswerAlert,QuestionAlert, Notification,UserChecklistIndex,TopicFollow,PatientNotification,DoctorNotification,AddTopicNotification,EditTopicNotification,AddChecklistNotification,EditChecklistNotification,Feedback,ThankChecklistNotification,ThankAnswerNotification,AgreeAnswerNotification,AgreeChecklistNotification,QuestionRelate, QuestionAndTopic,TopicAndGoal,TopicAgree, PatientCondition,PatientMedication,PatientFamilyHistory,PatientAllergy 

class AnswerInline(admin.TabularInline):
	model = Answer 

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline,]
	
class AnswerAdmin(admin.ModelAdmin):
	pass 

class ListItemInline(admin.TabularInline):
	model = ListItem 
	

	
class ChecklistAdmin(admin.ModelAdmin):
	inlines = [ListItemInline,]


class ListItemAdmin(admin.ModelAdmin):
	pass 
	
admin.site.register(AnswerAlert)
admin.site.register(AdvisorRequest)
admin.site.register(AgreeChecklist)
admin.site.register(AgreeChecklistNotification)
admin.site.register(AgreeAnswer)
admin.site.register(AgreeAnswerNotification)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(AddTopicNotification)
admin.site.register(AddChecklistNotification)
admin.site.register(CheckList,ChecklistAdmin)
admin.site.register(Category)
admin.site.register(Condition)

admin.site.register(Doctor)
admin.site.register(DoctorRecord)
admin.site.register(DoctorNotification)
admin.site.register(Goal)

admin.site.register(EditChecklistNotification)
admin.site.register(EditTopicNotification)
admin.site.register(FriendShipRequest)
admin.site.register(Friend)
admin.site.register(Feedback)
admin.site.register(ListItem,ListItemAdmin)
admin.site.register(Medication)
admin.site.register(Notification)

admin.site.register(Patient)
admin.site.register(PatientRecord)
admin.site.register(PatientNotification)
admin.site.register(PatientMedication)
admin.site.register(PatientCondition)
admin.site.register(PatientFamilyHistory)
admin.site.register(PatientAllergy)
admin.site.register(Question,QuestionAdmin)

admin.site.register(Riskfactor)
admin.site.register(Symptom)

admin.site.register(ThanksChecklist)
admin.site.register(ThankChecklistNotification)
admin.site.register(ThanksAnswer)
admin.site.register(ThankAnswerNotification)
admin.site.register(TopicAndGoal)
admin.site.register(Topic)
admin.site.register(TopicFollow)
admin.site.register(TopicAgree)
admin.site.register(UserCheckList)
admin.site.register(UserListItem)
admin.site.register(UserChecklistIndex)
admin.site.register(Vaccination)
admin.site.register(Procedure)

admin.site.register(QuestionAlert)
admin.site.register(QuestionRelate)
admin.site.register(QuestionAndTopic)