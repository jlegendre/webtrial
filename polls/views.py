from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from polls.forms import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
from polls.models import *
from django import forms
from django.core import exceptions
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError

from django.forms import formset_factory
from django.forms.models import modelformset_factory
import datetime
from django.contrib import messages
from django.utils.functional import curry    
from django.forms import inlineformset_factory

from django.forms import modelform_factory
def welcome(request):
	logged_user = get_logged_user_from_request(request)
	if not logged_user is None:
		if 'newMessage' in request.GET and request.GET['newMessage'] != '':
			newMessage = Message(auteur=logged_user, contenu=request.GET['newMessage'], pub_date = datetime.datetime.now())
			newMessage.save()
		friendMessages = Message.objects.filter(auteur__amis=logged_user).order_by('-pub_date')
		return render_to_response('polls/home.html', {'logged_user': logged_user, 'friendMessages': friendMessages})
	else:
		return HttpResponseRedirect('/login/')
	# if logged_user:
	# 	return render(request, 'polls/welcome.html', {'logged_user':logged_user})
	# else:
	# 	return HttpResponseRedirect('/login')




def index(request):
    return HttpResponse("Hello, world. You're at the webtrial index.")


def sendmail(request):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		if request.method == 'POST':
			form = EmailForm(request.POST)
			if form.is_valid():
				firstname = form.cleaned_data['firstname']
				lastname = form.cleaned_data['lastname']
				email = form.cleaned_data['email']
				subject = form.cleaned_data['subject']
				botcheck = form.cleaned_data['botcheck'].lower()
				message = form.cleaned_data['message']
				if botcheck == 'yes' or 'YES' or 'Yes' or 'yEs' or 'yeS' or 'yES' or 'YEs' or 'YeS':
					try:
						fullemail = firstname + " " + lastname + " " + "<" + email + ">"
						send_mail(subject, message, fullemail, [email])
						return HttpResponseRedirect('/email/thankyou/')
					except:
						return HttpResponseRedirect('/email/')
			else:
				return HttpResponseRedirect('/email/')
		else:
			return HttpResponseRedirect('/email/')  
	else:
		return HttpResponseRedirect('/login/')



def register(request):
	# if request.method=="GET":
	if len(request.GET) > 0 and 'profileType' in request.GET:
		studentForm = StudentProfileForm(prefix="st")
		employeeForm = EmployeeProfileForm(prefix="em")
		if request.GET['profileType'] == 'student':
			studentForm = StudentProfileForm(request.GET, prefix="st")
			if studentForm.is_valid():
				studentForm.save(commit=True)
				messages.success(request, "Successfully Created")
				return HttpResponseRedirect('/login/')
		elif request.GET['profileType'] == 'employee':
			employeeForm = EmployeeProfileForm(request.GET, prefix="em")
			if employeeForm.is_valid():
				employeeForm.save(commit=True)
				messages.success(request, "Successfully Created")
				return HttpResponseRedirect('/login/')
			else:
				messages.error(request, "Not Successfully Created")
		return render(request, 'polls/user_profile(bootstrap).html',{'studentForm': studentForm, 'employeeForm': employeeForm},context_instance=RequestContext(request))
	else:

		studentForm = StudentProfileForm(prefix="st")
		employeeForm = EmployeeProfileForm(prefix="em")
		return render(request, 'polls/user_profile(bootstrap).html',{'studentForm': studentForm, 'employeeForm': employeeForm},context_instance=RequestContext(request))

def login(request):
	if request.method=="POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user_email = form.cleaned_data['email']
			logged_user = Personne.objects.get(courriel=user_email)
			request.session['logged_user_id'] = logged_user.id
			return HttpResponseRedirect('/welcome/')
	else:
		form = LoginForm()
		return render(request, 'polls/login.html', {'form':form})
	return render_to_response('polls/login.html', {'form': form},context_instance=RequestContext(request))

def get_logged_user_from_request(request):
	if 'logged_user_id' in request.session:
		logged_user_id = request.session['logged_user_id']
		# On cherche un étudiant ici
		if len(Etudiant.objects.filter(id=logged_user_id)) == 1:
			return Etudiant.objects.get(id=logged_user_id)
		# On cherche un Employe ici
		elif len(Employe.objects.filter(id=logged_user_id)) == 1:
			return Employe.objects.get(id=logged_user_id)
		# Si on trouve rien -->
		else:
			return None
	else:
		return None


def add_friend(request):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		if len(request.GET) > 0:
			form = AddFriendForm(request.GET)
			if form.is_valid():
				new_friend_email = form.cleaned_data['email']
				newFriend = Personne.objects.get(courriel=new_friend_email)
				logged_user.amis.add(newFriend)
				logged_user.save()
				return HttpResponseRedirect('/welcome/')
			else:
				return render_to_response('polls/add_friend(bootstrap).html', {'form': form})
		else:
			form = AddFriendForm()
			return render_to_response('polls/add_friend(bootstrap).html', {'form': form})
	else:
		return HttpResponseRedirect('/login/')



def show_profile(request):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		if 'userToShow' in request.GET and request.GET['userToShow'] != '':
			results = Personne.objects.filter(id=request.GET['userToShow'])
			if len(results) == 1:
				if Etudiant.objects.filter(id=request.GET['userToShow']):
					user_to_show = Etudiant.objects.get(id=request.GET['userToShow'])
				else:
					user_to_show = Employe.objects.get(id=request.GET['userToShow'])
				return render_to_response('polls/show_profile(bootstrap).html', {'user_to_show':user_to_show})
			else:
				return render_to_response('polls/show_profile(bootstrap).html', {'user_to_show':logged_user})
		else:
			return render_to_response('polls/show_profile(bootstrap).html', {'user_to_show':logged_user})
	else:
		return HttpResponseRedirect('/login/')


def modify_profile(request):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		if len(request.GET) > 0:
			if type(logged_user) == Etudiant:
				form = StudentProfileForm(request.GET, instance=logged_user)
			else:
				form = EmployeeProfileForm(request.GET, instance=logged_user)
			if form.is_valid:
				form.save(commit=True)
				return render_to_response('polls/show_profile(bootstrap).html', {'user_to_show':logged_user})
			else:
				return render_to_response('polls/modify_profile(bootstrap).html', {'form':form, 'instance':logged_user})
		else:
			if type(logged_user) == Etudiant:
				form = StudentProfileForm(instance=logged_user)
			else:
				form = EmployeeProfileForm(instance=logged_user)
			return render_to_response('polls/modify_profile(bootstrap).html', {'form':form, 'instance':logged_user})
	else:
		HttpResponseRedirect('/login/')

def upload(request):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
    # Handle file upload
	    if request.method == 'POST':
	        form = DocumentForm(request.POST, request.FILES)
	        if form.is_valid():
	            newdoc = Document(docfile = request.FILES['docfile'])
	            newdoc.save()

	            # Redirect to the document list after POST
	            return HttpResponseRedirect(reverse('polls.views.upload'))
	    else:
	        form = DocumentForm() # A empty, unbound form

	    # Load documents for the list page
	    documents = Document.objects.all()

	    # Render list page with the documents and the form
	    return render_to_response(
	        'polls/upload(bootstrap).html',
	        {'documents': documents, 'form': form},
	        context_instance=RequestContext(request)
	    )

	else: 
		return HttpResponseRedirect('/login/')


def galerie(request):
	logged_user = get_logged_user_from_request(request)
	form = DocumentForm(request.POST, request.FILES)
	documents = Document.objects.all()
	if logged_user:
		return render_to_response('polls/galerie(bootstrap).html', {'documents': documents, 'form': form})
	else:
		return HttpResponseRedirect('/login/')

def champs(request):
	logged_user = get_logged_user_from_request(request)
	champs = Champs.objects.all()
	if logged_user:
		if len(request.GET) > 0:
			form = ChampsForm(request.GET)
			if form.is_valid():
				form.save(commit=True)
				return HttpResponseRedirect('/champs/')
			else:
				return render_to_response('polls/champs.html', {'champs': champs, 'form': form})

		elif request.method == 'DELETE':
			form.delete()
			return HttpResponseRedirect('/champs/')
		else:
			form = ChampsForm()
			return render_to_response('polls/champs.html', {'champs': champs, 'form': form})
	else:
		return HttpResponseRedirect('/login/')

def modify_champs(request, instance):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		if len(request.GET) > 0:
			form = ChampsForm(request.GET, instance=Champs.objects.get(pk=instance))
			if form.is_valid():
				form.save(commit=True)
				return HttpResponseRedirect('/champs/')
			else:
				return render_to_response('polls/modify_champs.html', {'form': form})
		else:
			form = ChampsForm(instance=Champs.objects.get(pk=instance))
			return render_to_response('polls/modify_champs.html', {'form': form})
	else:
		return HttpResponseRedirect('/login/')


  
def delete_champs(request, instance):
	logged_user = get_logged_user_from_request(request)
	form = get_object_or_404(Champs, pk=instance)
	if logged_user:
		if request.method=='POST':
			form.delete()
			return HttpResponseRedirect('/champs/')
		else:
			form.delete()
			return HttpResponseRedirect('/champs/')
	else:
		return HttpResponseRedirect('/login/')



def ajax_check_email_field(request):
	form = LoginForm(request.POST)
	HTML_to_return = ''
	if 'value' in request.GET:
		field = forms.EmailField()
		try:
			field.clean(request.GET['value'])
		except exceptions.ValidationError as ve:
			HTML_to_return = '<ul class="errorList">'
			for message in ve.messages:
				HTML_to_return += '<li>' + message + '</li>'
			HTML_to_return += '</ul>'
	return HttpResponse(HTML_to_return)


def ajax_add_friend(request):
	HTML_to_return = ''
	logged_user = get_logged_user_from_request(request)
	if not logged_user is None:
		if 'email' in request.GET:
			new_friend_email = request.GET['email']
			if len(Personne.objects.filter(courriel=new_friend_email)) == 1:
				new_friend = Personne.objects.get(courriel=new_friend_email)
				logged_user.amis.add(new_friend)
				logged_user.save()

				HTML_to_return = '<li><a href="../showProfile?userToShow='
				HTML_to_return += str(new_friend.id)
				HTML_to_return += '">'
				HTML_to_return += new_friend.prenom + '' +new_friend.nom
				HTML_to_return += '</a></li>'
	return HttpResponse(HTML_to_return)


def reply(request):
	replies = Reply.objects.all()
	questions = Question.objects.all()
	logged_user = get_logged_user_from_request(request)
	pages = Page.objects.all()
	form = ReplyBisForm(request.GET)
	personnes = Personne.objects.all()
	if logged_user:
		if len(request.GET) > 0:
			form = ReplyBisForm(request.GET)
			if form.is_valid():
				form.save(commit=True)
				return HttpResponseRedirect('/reply/')
			else:
				return render_to_response('polls/reply.html', {'personnes': personnes, 'replies': replies, 'questions': questions,'pages':pages, 'form': form})
		else:
			form = ReplyBisForm()
			return render_to_response('polls/reply.html', {'personnes':personnes, 'replies': replies, 'questions': questions, 'pages':pages, 'form': form})
	else:
		return HttpResponseRedirect('/login/')




def baseVisite(request):
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		replies = Reply.objects.all()
		questions = Question.objects.all()
		logged_user = get_logged_user_from_request(request)
		pages = Page.objects.all()
		personnes = Personne.objects.all()
		return render_to_response('polls/baseVisite.html', {'pages':pages})
	else:
		return HttpResponseRedirect('/login/')


# def access(request, page_id):
# 	page = Page.objects.get(pk=page_id)
# 	forms = list()
# 	questions = Question.objects.filter(page=page)
# 	# questions = Question.objects.filter(page=instance)
# 	replies = Reply.objects.filter()
# 	pages = Page.objects.all()
# 	numPages = Page.objects.get(pk=page_id)
# 	length_questions = len(questions)
# 	logged_user = get_logged_user_from_request(request)
# 	instance = {'instance':page_id}
# 	QuestionForm = modelform_factory(Question, fields=('label',))
# 	ReplyInlineFormSet = inlineformset_factory(Question, Reply, extra=1, fields=('answer',))
# 	ReplyFormSet = modelformset_factory(model=Reply, form=ReplyForm, extra=length_questions)
# 	ReplyFormSet.form = staticmethod(curry(ReplyForm, page_id=page_id))
# 	if logged_user:
# 		if request.method == 'POST': 
# 			for question in questions:
# 				q_form = QuestionForm(request.POST, request.FILES, instance=question, prefix='q_'+str(question.id)+'_')
# 				r_formset = ReplyInlineFormSet(request.POST, request.FILES, instance=question, prefix=q_form.prefix)
# 				forms.append((q_form, r_formset))
# 				if all(q_form.is_valid() and r_formset.is_valid() for q_form, r_formset in forms):
# 					for q_form, r_formset in forms:
# 						q_form.save()
# 						r_formset.save() 
# 			# formset = ReplyFormSet(request.POST, request.FILES, initial=[{'instance':page_id,}])		

# 			if formset.is_valid():
# 				new_instances = formset.save(commit=False)
# 				for new_instance in new_instances:
# 					new_instance.user = logged_user
# 					new_instance.save()
				
# 				return render_to_response('polls/access.html', {
# 		 'forms':forms,
# 		 'formset': formset,
# 		 'questions':questions,
# 		 'logged_user':logged_user,
# 		 'numPages' : numPages
# 		 })
# 			else:
# 				messages.add_message(request, messages.INFO, "L'ajout à bien été effectué !")
# 				return render_to_response('polls/access.html', {
# 		 'forms':forms,			
# 		 'formset': formset,
# 		 'questions':questions,
# 		 'logged_user':logged_user,
# 		 'numPages' : numPages
# 		 })
# 		else:
# 			formset = ReplyFormSet(queryset = Reply.objects.none())
# 			for question in questions:
# 				q_form = QuestionForm(instance=question, prefix='q_'+str(question.id)+'_')
# 				r_formset = ReplyInlineFormSet(instance=question, prefix=q_form.prefix)
# 				forms.append((q_form, r_formset))
# 				return render_to_response('polls/access.html', {
# 		 'forms':forms,
# 		 'formset': formset,
# 		 'questions':questions,
# 		 'logged_user':logged_user,
# 		 'numPages' : numPages
# 		 })
# 	else:
# 		return HttpResponseRedirect('/login/')

def access(request, page_id):
	questions = Question.objects.filter(page=page_id)
	pages = Page.objects.all()
	numPages = Page.objects.get(pk=page_id)
	length_questions = len(questions)
	logged_user = get_logged_user_from_request(request)
	instance = {'page_id':page_id}
	replies = Reply.objects.filter(question__in=questions)
	ReplyFormSet = modelformset_factory(model=Reply, form=ReplyForm, extra=length_questions, min_num=length_questions, max_num=length_questions)
	ReplyFormSet.form = staticmethod(curry(ReplyForm, page_id=page_id))
	if logged_user:
		if request.method == 'POST':  
			formset = ReplyFormSet(request.POST, request.FILES, queryset=Reply.objects.filter(question__in=questions, user=logged_user))
			if formset.is_valid():
				new_instances = formset.save(commit=False)
				for new_instance in new_instances:
					new_instance.user = logged_user
					new_instance.save()
				
				return HttpResponseRedirect('../../baseVisite/', {
		 'replies':replies,
		 'formset': formset,
		 'questions':questions,
		 'logged_user':logged_user,
		 'numPages' : numPages
		 })
			else:
				return render_to_response('polls/access.html', {
		 'replies':replies,
		 'formset': formset,
		 'questions':questions,
		 'logged_user':logged_user,
		 'numPages' : numPages
		 })
		else:	
			formset = ReplyFormSet(queryset=Reply.objects.filter(question__in=questions, user=logged_user))
			# formset = ReplyFormSet(queryset=Reply.objects.none())	
			return render(request, 'polls/access.html', {
			'replies':replies,
			'formset': formset,
			'questions':questions,
			'logged_user':logged_user,
			'numPages' : numPages
			})
	else:
		return HttpResponseRedirect('/login/')	


def modify_answer(request, instance):
	questions = Question.objects.filter(page=instance)
	logged_user = get_logged_user_from_request(request)
	if logged_user:
		if len(request.GET)>0:
			formset = ReplyForm(request.GET, instance=Reply.objects.get(page=questions))
			if formset.is_valid:
				formset.save(commit=True)
				return HttpResponseRedirect('/access/{{ page.pk }}/')
			else:
				return render_to_response('polls/modifyAnswer.html', {'formset':formset})
		else:
			formset = ReplyForm(instance=Page.objects.all())
			return render_to_response('polls/modifyAnswer.html', {'formset':formset})
	else:
		return HttpResponseRedirect('/login/')




	# --------------------------------------------

	# replies = Reply.objects.all()
	# pages = Page.objects.all()
	# numPages = Page.objects.get(pk=instance)
	# questions = Question.objects.filter(page=instance)
	# logged_user = get_logged_user_from_request(request)
	# if request.method == 'POST':  
	# 	form = ReplyForm(request.POST)  
	# 	if form.is_valid():
	# 		user = form.cleaned_data['user']
	# 		question = form.cleaned_data['question']
	# 		answer = form.cleaned_data['answer']
	# 		form.save()
	# 		return HttpResponse('Successfully')
	# else:
	# 	form = ReplyForm()
	# return render_to_response('polls/access.html', {'pages':pages,'form': form, 'questions':questions,'logged_user':logged_user,'numPages': numPages,})

	# --------------------------------------------


	# replies = Reply.objects.all()
	# logged_user = get_logged_user_from_request(request)
	# numPages = Page.objects.get(pk=instance)
	# questions = Question.objects.filter(page=instance)
	# pagesfilter = Question.objects.get(pk=1) # PEUT ETRE CHANGER SE FILTRE - A VOIR
	# # pagesfilter = Page.objects.get(pk=instance).reply_set.filter(user=logged_user) # PEUT ETRE CHANGER SE FILTRE - A VOIR
	# form = ReplyForm(request.GET)
	# personnes = Personne.objects.all()
	# if logged_user:
	# 	if len(request.POST) > 0:
	# 		form = ReplyForm(request.POST)
	# 		if form.is_valid():
	# 			user = form.cleaned_data['user']
	# 			question = form.cleaned_data['question']
	# 			answer = form.cleaned_data['answer']
	# 			form.save(commit=True)
	# 			return HttpResponse(form.cleaned_data["user"])
	# 		else:
	# 			return render_to_response('polls/access.html', {'logged_user':logged_user, 'pagesfilter': pagesfilter, 'numPages': numPages, 'personnes': personnes, 'replies': replies, 'questions': questions, 'form': form})
	# 	else:
	# 		form = ReplyForm()
	# 		return render_to_response('polls/access.html', {'logged_user':logged_user, 'pagesfilter': pagesfilter, 'numPages': numPages, 'personnes':personnes, 'replies': replies, 'questions': questions, 'form': form})
	# else:
	# 	return HttpResponseRedirect('/login')


def replyTest(request):
	if request.method == 'POST':
		form = ReplyForm(request.POST)
		if form.is_valid():
			question = form.cleaned_data['question']
			answer = form.cleaned_data['answer']
			user = form.cleaned_data['user']
			form.save(commit=True)
			return HttpResponseRedirect('/baseVisite/')
	else:
		form = ReplyForm()
	return render(request, 'polls/replyTest.html', {'form': form })


def google(request):
	return render_to_response('polls/google.html')



def addQuestion(request):
	logged_user = get_logged_user_from_request(request)
	questions = Question.objects.all()
	if logged_user:
		if len(request.GET) > 0:
			form = QuestionForm(request.GET)
			if form.is_valid():
				form.save(commit=True)
				return HttpResponseRedirect('/reply/')
			else:
				return render_to_response('polls/addQuestion.html', {'questions': questions, 'form': form})
		else:
			form = QuestionForm()
			return render_to_response('polls/addQuestion.html', {'questions': questions, 'form': form})
	else:
		return HttpResponseRedirect('/login/')



def addPage(request):
	logged_user = get_logged_user_from_request(request)
	pages = Page.objects.all()
	if logged_user:
		if len(request.GET) > 0:
			form = PageForm(request.GET)
			if form.is_valid():
				form.save(commit=True)
				return HttpResponseRedirect('/reply/')
			else:
				return render_to_response('polls/addPage.html', {'pages': pages, 'form': form})
		else:
			form = PageForm()
			return render_to_response('polls/addPage.html', {'pages': pages, 'form': form})
	else:
		return HttpResponseRedirect('/login/')

def get_reply(request):
	questions = Question.objects.all()
	length_questions = len(questions)
	NameFormSet = modelformset_factory(model=Reply, form=NameForm, extra=3)
	logged_user = get_logged_user_from_request(request)
	if request.method == 'POST':  
		formset = NameFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save()
			return HttpResponse('Successfully')
		else:
			return HttpResponseRedirect('/get_reply/')
	else:
		formset = NameFormSet()
	return render_to_response('polls/name.html', {'formset': formset, 'questions':questions,'logged_user':logged_user})

