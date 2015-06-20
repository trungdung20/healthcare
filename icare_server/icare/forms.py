from django.contrib.auth.models import User 
from django import forms 
from models import Doctor, Patient, certification_CHOICES, GENDER_CHOICES, Question, Answer, CheckList, PatientRecord, DoctorRecord, Topic, ListItem, Vaccination, ETHNICITY, DIETARY_RESTRICTION, ALCOHOL,SEX_ACTIVE, RECREATIONAL_DRUGS, TOBACCO
from icare.list import DOCTOR_SPECIALTY, DOCTOR_DEGREE, YEAR 
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	username = forms.CharField(help_text="Please enter your username")
	email = forms.EmailField(help_text="Please enter your email address")
	
	class Meta:
		model = User
		fields = ('username', 'email','password') 
		
class PatientForm(forms.ModelForm):
	name = forms.CharField('Patient Name')
	birthday = forms.DateField(label="Patient'sBirthday",widget=forms.DateInput(format='%d/%m/%Y'))
	gender = forms.ChoiceField(label='Patient Gender',choices=GENDER_CHOICES)
	patient_image = forms.ImageField(label='image of patient')
	address = forms.CharField("Patient's Address")
	class Meta:
		model = Patient 
		exclude = ('user','advisor')



class PatientRecordWeightForm(forms.ModelForm):
	
	class Meta:
		model = PatientRecord 
		fields = ('weight',)

class PatientRecordHeightForm(forms.ModelForm):
	
	class Meta:
		model = PatientRecord 
		fields = ('height',)
		
class PatientRecordEthnicityForm(forms.ModelForm):
	ethnicity = forms.ChoiceField(choices=ETHNICITY)
	
	class Meta:
		model = PatientRecord 
		fields = ('ethnicity',)

class PatientRecordVaccinationForm(forms.ModelForm):
	vaccination = forms.ModelMultipleChoiceField(queryset= Vaccination.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'rows':5,'col':10}))
	class Meta:
		model = PatientRecord 
		fields = ('vaccination',)

class PatientRecordDietaryForm(forms.ModelForm):
	dietary_restriction = forms.ChoiceField(choices=DIETARY_RESTRICTION)
	
	class Meta:
		model = PatientRecord 
		fields = ('dietary_restriction',)

class PatientRecordAlcoholForm(forms.ModelForm):
	alcohol = forms.ChoiceField(choices=ALCOHOL)
	class Meta:
		model = PatientRecord 
		fields = ('alcohol',)			

class PatientRecordTobaccoForm(forms.ModelForm):
	tobacco = forms.ChoiceField(choices=TOBACCO)
	class Meta:
		model = PatientRecord 
		fields = ('tobacco',)

class PatientRecordSexForm(forms.ModelForm):
	sexually_active =forms.ChoiceField(choices=SEX_ACTIVE)
	class Meta:
		model = PatientRecord 
		fields = ('sexually_active',)
		
class PatientRecordDrugForm(forms.ModelForm):
	recreational_drug = forms.ChoiceField(choices=RECREATIONAL_DRUGS)
	class Meta:
		model = PatientRecord 
		fields = ('recreational_drug',)
				
class DoctorForm(forms.ModelForm):
	name = forms.CharField(label="Name")
	
	gender = forms.ChoiceField(label="Gender",choices=GENDER_CHOICES)
	doctor_image = forms.ImageField(label='image of doctor')
	
	specialty = forms.ChoiceField(label="specialty", choices=DOCTOR_SPECIALTY)
	school = forms.CharField(label="Graduated School")
	license = forms.IntegerField(label="License Number")
	year = forms.ChoiceField(choices=YEAR)
	address = forms.CharField(label="Address")
	class Meta: 
		model = Doctor 
		exclude = ('user',)

class DoctorRecordForm(forms.ModelForm):
	
	class Meta: 
		model = DoctorRecord 
		fields = ('doctor_information','language')
		
class DoctorImageForm(forms.ModelForm):
	doctor_image = forms.ImageField(label='image of doctor')
	class Meta:
		model = Doctor 
		fields = ('doctor_image',)
	
class QuestionForm(forms.ModelForm):
	
	
	
	class Meta: 
		model = Question 
		widgets = {
          'title': forms.Textarea(attrs={'rows':6, 'cols':90}),
        }
		fields = ('title',)
		
class AnswerForm(forms.ModelForm):
	
	
	class Meta:
		model = Answer
		widgets = {
          'detail': forms.Textarea(attrs={'rows':6, 'cols':90}),
        }
		fields = ('detail',)

class TopicForm(forms.ModelForm):
	image = forms.ImageField(required=False)
	image_description = forms.CharField(required=False)
	class Meta:
		model = Topic 
		fields = ('title','definition','image','image_description')
		
class ItemListForm(forms.ModelForm):
	
	class Meta:	
		model = ListItem 
		widgets = {
          'title': forms.Textarea(attrs={'rows':6, 'cols':40}),
        }
		fields = ('title','priority','frequency')