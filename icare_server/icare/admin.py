from django.contrib import admin 
from icare.models import Doctor, Patient, PatientRecord, DoctorRecord, FriendShipRequest, Friend, Category, Goal, CheckList, ListItem, UserCheckList, UserListItem, Topic, Condition, Riskfactor, Symptom, Procedure, Medication, Question, Answer, Vaccination, ThanksChecklist, AgreeChecklist, AgreeAnswer, ThanksAnswer,AdvisorRequest,AnswerAlert,QuestionAlert, Notification,UserChecklistIndex 

admin.site.register(AnswerAlert)
admin.site.register(AdvisorRequest)
admin.site.register(AgreeChecklist)
admin.site.register(AgreeAnswer)
admin.site.register(Answer)
admin.site.register(CheckList)
admin.site.register(Category)
admin.site.register(Condition)

admin.site.register(Doctor)
admin.site.register(DoctorRecord)
admin.site.register(Goal)


admin.site.register(FriendShipRequest)
admin.site.register(Friend)

admin.site.register(ListItem)
admin.site.register(Medication)
admin.site.register(Notification)

admin.site.register(Patient)
admin.site.register(PatientRecord)
admin.site.register(Question)

admin.site.register(Riskfactor)
admin.site.register(Symptom)
admin.site.register(ThanksAnswer)
admin.site.register(Topic)

admin.site.register(UserCheckList)
admin.site.register(UserListItem)
admin.site.register(UserChecklistIndex)
admin.site.register(Vaccination)
admin.site.register(Procedure)
admin.site.register(ThanksChecklist)
admin.site.register(QuestionAlert)
