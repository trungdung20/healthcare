from django import template 
from icare.models import Doctor, Patient

register = template.Library()

@register.inclusion_tag("icare/nav_bar.html")
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
	
