# -*- coding: utf-8 -*-
import os 
from django.core.files import File
from PIL import Image
def populate():
	image1 = 'D:\code\ICare_Project\icare_server\image\images1.jpg'
	image2 = 'D:\code\ICare_Project\icare_server\image\images2.jpg'
	image3 = 'D:\code\ICare_Project\icare_server\image\images3.jpg'
	image4 = 'D:\code\ICare_Project\icare_server\image\images4.jpg'
	image5 = 'D:\code\ICare_Project\icare_server\image\images5.jpg'
	email = 'dungbme10@gmail.com'
	password = '16041992'
	school = 'Test University'
	doctor1 = add_doctor('test1',email,password,'John Smith','Addiction Medicine','Male',school,image1,'1234','MD',2010,'Test Address') 
	doctor2 = add_doctor('test2',email,password,'John Kennerdy','Cancer Surgery','Male',school,image2,'12345','DO',2009,'Test Address') 
	doctor3 = add_doctor('test3',email,password,'Eva Braun','Radiation Oncology','Female',school,image3,'123456','PharmD',2011,'Test Address') 
	doctor4 = add_doctor('test4',email,password,'Elizabeth Smith','Pediatric Cardiology','Female',school,image4,'12345','MBBS',2011,'Test Address') 
	doctor5 = add_doctor('test5',email,password,'Christian Grey','Vascular Surgery','Female',school,image5,'123455','MBBS',2011,'Test Address') 
	
def add_user(username, email,password):
	u = User.objects.get_or_create(username=username, email=email)[0]
	u.set_password(password)
	u.save()
	return u 
def add_doctor(username,email,password,name,specialty,gender,school,doctor_image,license,degree,year,address):
	user = add_user(username,email,password)
	#f = open(doctor_image,'w')
	#image = File(f)
	\
	doctor = Doctor.objects.get_or_create(user=user,name=name,specialty=specialty,gender=gender,school=school,doctor_image=doctor_image,license=license,degree=degree,year=year,address=address)[0]
	doctor_record = DoctorRecord.objects.get_or_create(doctor=doctor)
	#image.closed
	#f.closed
	return doctor

	
if __name__ == '__main__':
	print "starting population script...."
	
	
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','icare_server.settings')
	from django.contrib.auth.models import User
	from icare.models import Category, Goal, Topic, Medication, Vaccination, Condition , Symptom , Procedure, Riskfactor,Doctor
	populate() 