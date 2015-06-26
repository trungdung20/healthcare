from django.contrib.auth.models import User 
from django import forms 
from models import Doctor, Patient, certification_CHOICES, GENDER_CHOICES, Question, Answer, CheckList, PatientRecord, DoctorRecord, Topic, ListItem, Vaccination, ETHNICITY, DIETARY_RESTRICTION, ALCOHOL,SEX_ACTIVE, RECREATIONAL_DRUGS, TOBACCO,Feedback
from icare.list import DOCTOR_SPECIALTY, DOCTOR_DEGREE, YEAR
from bootstrap_toolkit.widgets import BootstrapTextInput

class UserForm(forms.ModelForm):
	#password = forms.CharField(widget=forms.PasswordInput)
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Please enter your username'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your email'}))

	class Meta:
		model = User
		widgets = {
          #'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Please enter your username'}),
		  #'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your email'}),
		  'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Please enter your password'}),
        }
		fields = ('username', 'email','password') 
		
class PatientForm(forms.ModelForm):
	#name = forms.CharField('Full name')
	birthday = forms.DateField(label="Patient's Birthday",widget=forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control','placeholder': 'mm/dd/yy'}))
	gender = forms.ChoiceField(label='Patient Gender',choices=GENDER_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
	patient_image = forms.ImageField(label='Image of patient',widget=forms.ClearableFileInput())
	#address = forms.CharField(label='Address')
	class Meta:
		model = Patient 
		widgets = {
		'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter your full name'}),
		#'birthday': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control','placeholder': 'dd/mm/yy'}),
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your adress'}),
		}
		exclude = ('user','advisor')

class PatientRecordWeightForm(forms.ModelForm):
	
	class Meta:
		model = PatientRecord 
		widgets = {
		'weight': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your weight (kg)'}),
		#'birthday': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control','placeholder': 'dd/mm/yy'}),
		#'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your adress'}),
		}
		fields = ('weight',)

class PatientRecordHeightForm(forms.ModelForm):
	
	class Meta:
		model = PatientRecord 
		widgets = {
		'height': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your height (meter)'}),
		#'birthday': forms.DateInput(format='%d/%m/%Y',attrs={'class': 'form-control','placeholder': 'dd/mm/yy'}),
		#'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your adress'}),
		}
		fields = ('height',)
		
class PatientRecordEthnicityForm(forms.ModelForm):
	ethnicity = forms.ChoiceField(choices=ETHNICITY,widget=forms.Select(attrs={'class': 'form-control'}))
	
	class Meta:
		model = PatientRecord 
		fields = ('ethnicity',)

class PatientRecordVaccinationForm(forms.ModelForm):
	vaccination = forms.ModelMultipleChoiceField(queryset= Vaccination.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={}))
	class Meta:
		model = PatientRecord 
		fields = ('vaccination',)

class PatientRecordDietaryForm(forms.ModelForm):
	dietary_restriction = forms.ChoiceField(choices=DIETARY_RESTRICTION,widget=forms.Select(attrs={'class': 'form-control'}))
	
	class Meta:
		model = PatientRecord 
		fields = ('dietary_restriction',)

class PatientRecordAlcoholForm(forms.ModelForm):
	alcohol = forms.ChoiceField(choices=ALCOHOL,widget=forms.Select(attrs={'class': 'form-control'}))
	class Meta:
		model = PatientRecord 
		fields = ('alcohol',)			

class PatientRecordTobaccoForm(forms.ModelForm):
	tobacco = forms.ChoiceField(choices=TOBACCO,widget=forms.Select(attrs={'class': 'form-control'}))
	class Meta:
		model = PatientRecord 
		fields = ('tobacco',)

class PatientRecordSexForm(forms.ModelForm):
	sexually_active =forms.ChoiceField(choices=SEX_ACTIVE,widget=forms.Select(attrs={'class': 'form-control'}))
	class Meta:
		model = PatientRecord 
		fields = ('sexually_active',)
		
class PatientRecordDrugForm(forms.ModelForm):
	recreational_drug = forms.ChoiceField(choices=RECREATIONAL_DRUGS,widget=forms.Select(attrs={'class': 'form-control'}))
	class Meta:
		model = PatientRecord 
		fields = ('recreational_drug',)
				
class DoctorForm(forms.ModelForm):
	#name = forms.CharField(label="Name")
	
	gender = forms.ChoiceField(label="Gender",choices=GENDER_CHOICES,widget=forms.Select(attrs={'class': 'form-control'}))
	doctor_image = forms.ImageField(label='Image of doctor',widget=forms.ClearableFileInput())
	degree = forms.ChoiceField(choices=DOCTOR_DEGREE,widget=forms.Select(attrs={'class': 'form-control'}))
	specialty = forms.ChoiceField(label="specialty", choices=DOCTOR_SPECIALTY,widget=forms.Select(attrs={'class':'form-control'}))
	#school = forms.CharField(label="Graduated School")
	license = forms.IntegerField(label="License Number",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your license number'}))
	year = forms.ChoiceField(choices=YEAR,widget=forms.Select(attrs={'class': 'form-control'}))
	#address = forms.CharField(label="Address")
	class Meta: 
		model = Doctor 
		
		widgets = {
		'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please enter your full name'}),
		'school': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please enter your graduated school'}),
		#'license':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your license number'}),
		
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your adress'}),
		}
		exclude = ('user',)

class DoctorRecordForm(forms.ModelForm):
	
	class Meta: 
		model = DoctorRecord 
		widgets = {
		'doctor_information': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write something to introduce about yourself'}),
		'language': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your spoken language'}),
		#'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your adress'}),
		}
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
          'title': forms.Textarea(attrs={'rows':6,'class': 'form-control','placeholder': 'Please enter your question here'}),
        }
		fields = ('title',)
		
class FeedbackForm(forms.ModelForm):
	class Meta:	
		model = Feedback 
		widgets = {
		'detail': forms.Textarea(attrs={'rows':6,'class':'form-control','placeholder':'Please enter your feedback here'}),
		}
		fields = ('detail',)
class AnswerForm(forms.ModelForm):
	
	
	class Meta:
		model = Answer
		widgets = {
          'detail': forms.Textarea(attrs={'class': 'form-control','rows':6,'placeholder':'Please enter your answer here'}),
        }
		fields = ('detail',)

class TopicForm(forms.ModelForm):
	image = forms.ImageField(required=False)
	
	class Meta:
		model = Topic 
		widgets = {
		'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter topic title'}),
		'image_description': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter short description of your image'}),
		'definition': forms.Textarea(attrs={'class': 'form-control','rows':6,'placeholder':'Please topic definition'}),
		#'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Please enter your adress'}),
		}
		fields = ('title','definition','image','image_description')
		
class ItemListForm(forms.ModelForm):

	class Meta:	
		model = ListItem 
		widgets = {
          'title': forms.TextInput(attrs={'class': 'form-control',}),
		  'priority': forms.Select(attrs={'class':'form-control'}),
		  'frequency': forms.TextInput(attrs={'class':'form-control'})
        }
		fields = ('title','priority','frequency')