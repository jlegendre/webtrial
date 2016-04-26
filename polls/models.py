from django.db import models
from django.utils import timezone
from datetime import datetime   
import datetime
import django
from django.utils import timezone
class Faculte(models.Model):
	nom = models.CharField(max_length=30)
	couleur = models.CharField(max_length=6)

	def __str__(self):
		if len(self.nom) > 21:
			return self.nom[:20] + "..."
		else:
			return self.nom

class Personne(models.Model):
	matricule = models.CharField(max_length=10)
	nom = models.CharField(max_length=30)
	prenom = models.CharField(max_length=30)
	date_de_naissance = models.DateField()
	courriel = models.EmailField()
	tel_fixe = models.CharField(max_length=20,blank =True)
	tel_mobile = models.CharField(max_length=20)
	mot_de_passe = models.CharField(max_length=32)
	amis = models.ManyToManyField("self",blank =True)
	faculte = models.ForeignKey(Faculte)
	type_de_personne = 'generic'

	def __str__(self):
		return self.prenom + " " + self.nom


class Campus(models.Model):
	nom = models.CharField(max_length=300)
	adresse_postale = models.CharField(max_length=60)
	
	def __str__(self):
		return self.nom

class Fonction(models.Model):
	intitule = models.CharField(max_length=300)

	def __str__(self):
		if len(self.intitule) > 19:
			return self.intitule[:18] + "..."
		else:
			return self.intitule


class Cursus(models.Model):
	intitule = models.CharField(max_length=500)

	def __str__(self):
		if len(self.intitule) > 17:
			return self.intitule[:16] + "..."
		else:
			return self.intitule

class Employe(Personne):
	bureau = models.CharField(max_length=300)
	campus = models.ForeignKey(Campus)
	fonction = models.ForeignKey(Fonction)
	type_de_personne = 'employee'


class Etudiant(Personne):
	Cursus = models.ForeignKey(Cursus)
	annee = models.IntegerField()
	type_de_personne = 'student'

class Message(models.Model):
	auteur = models.ForeignKey(Personne)
	contenu = models.TextField()
	pub_date = models.DateTimeField(default=django.utils.timezone.now) 


	def __str__(self):
		if len(self.contenu) > 20:
			return self.contenu[:19] + "..."
		else:
			return self.contenu

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def __str__(self):
    	return str(self.docfile)

class Champs(models.Model):
	champs = models.CharField(max_length=300, verbose_name="Titre")
	contenu = models.TextField(max_length=10000, verbose_name="Contenu")

	def __str__(self):
		if len(self.contenu) > 17:
			return self.champs[:16] + "..."
		else:
			return self.champs

class Page(models.Model):
	title = models.CharField(max_length=300)
	

	def __str__(self):
		return self.title

class Question(models.Model):
	label = models.CharField(max_length=300)
	page = models.ManyToManyField(Page)

	def __str__(self):
			return self.label

class Reply(models.Model):
	question = models.ForeignKey(Question)
	user = models.ForeignKey(Personne)
	answer = models.CharField(max_length=300)
	creationDate = models.DateTimeField(default=django.utils.timezone.now)
	
	def __str__(self):
		return str(self.answer)





