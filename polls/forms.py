from django import forms
from polls.models import *
from datetime import datetime   
import datetime
from django.forms import BaseFormSet
from polls.views import *

class LoginForm(forms.Form):
	email = forms.EmailField(label='Courriel')
	password = forms.CharField(label='Mot de passe', widget = forms.PasswordInput)
	def clean(self):
		cleaned_data = super (LoginForm, self).clean()
		email = cleaned_data.get("email")
		password = cleaned_data.get("password")

		if email and password:
			result = Personne.objects.filter(mot_de_passe=password, courriel=email)

			if len(result) != 1:
				raise forms.ValidationError("Adresse de courriel ou mot de passe erroné(e).")

		return cleaned_data

class StudentProfileForm(forms.ModelForm):
	class Meta:
		model = Etudiant
		exclude =('amis',)

class EmployeeProfileForm(forms.ModelForm):
	class Meta:
		model = Employe 
		exclude = ('amis',)
			

class AddFriendForm(forms.Form):
	email = forms.EmailField(label='Courriel :')
	def clean(self):
		cleaned_data = super(AddFriendForm, self).clean()
		email = cleaned_data.get("email")

		if email:
			result = Personne.objects.filter(courriel=email)
			if len(result) != 1:
				raise forms.ValidationError("Adresse de courriel erronée.")
		return cleaned_data

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='(max. 42 megabytes)'
    )

class ChampsForm(forms.ModelForm):
	class Meta:
		model = Champs
		fields = ('champs','contenu')
 	
class ReplyForm(forms.ModelForm):

	def __init__(self, page_id, *args,**kwargs):
		super (ReplyForm,self ).__init__(*args,**kwargs)
		self.fields['question'].queryset = Question.objects.filter(page=page_id)
		
	class Meta:
		model = Reply
		exclude = ('user','creationDate')

class EmailForm(forms.Form):
	firstname = forms.CharField(max_length=255)
	lastname = forms.CharField(max_length=255)
	email = forms.EmailField()
	subject = forms.CharField(max_length=255)
	botcheck = forms.CharField(max_length=5)
	message = forms.CharField()

class ReplyBisForm(forms.ModelForm):
	class Meta:
		model = Reply
		fields = ('question','answer','user')

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question 
		fields = ('label','page')

class PageForm(forms.ModelForm):
	class Meta:
		model = Page 
		fields = ('title',)

class NameForm(forms.ModelForm):
	class Meta:
		model = Reply
		fields = ('question','user','answer')

class BaseReplyFormSet(BaseFormSet):
	def add_fields(self, form, index):
		super(BaseReplyFormSet, self).add_fields(form, index)
		form.fields["creationDate"] = forms.CharField()