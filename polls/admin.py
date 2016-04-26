from django.contrib import admin
from polls.models import *
# Register your models here.

class MessageAdmin(admin.ModelAdmin):
	list_display = ["__str__", "pub_date"]
	list_display_links = ["pub_date"]
	search_fields = ["contenu"]
	class Meta:
		model = Message



class PersonneAdmin(admin.ModelAdmin):
	list_display = ['__str__',"courriel"]
	search_fields = ["nom","prenom","courriel","matricule","tel_mobile"]

	class Meta:
		model = Personne

class FaculteAdmin(admin.ModelAdmin):
	search_fields = ["nom"]
	class Meta:
		model = Faculte

class FonctionAdmin(admin.ModelAdmin):
	search_fields = ["intitule"]
	class Meta:
		model = Fonction

class CampusAdmin(admin.ModelAdmin):
	search_fields = ["nom"]
	class Meta:
		model = Campus

class CursusAdmin(admin.ModelAdmin):
	search_fields = ["intitule"]
	class Meta:
		model = Cursus

class DocumentAdmin(admin.ModelAdmin):
	search_fields = ["docfile"]
	class Meta:
		model = Document
			
class ChampsAdmin(admin.ModelAdmin):
	list_display = ["__str__", "champs", "contenu"]
	class Meta:
		model = Champs	


class QuestionAdmin(admin.ModelAdmin):
	list_display = ["__str__", "pages"]

	def pages(self, obj):
		return "\n".join([str(page) +'  /' for page  in obj.page.all()]) 



class ReplyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "question", "creationDate", "page",]

    def page(self, obj):
        return "\n".join([page.title +' /' for page  in obj.question.page.all()]) 




admin.site.register(Faculte,FaculteAdmin)
admin.site.register(Campus,CampusAdmin)
admin.site.register(Fonction,FonctionAdmin)
admin.site.register(Cursus,CursusAdmin)
admin.site.register(Employe,PersonneAdmin)
admin.site.register(Etudiant,PersonneAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Document,DocumentAdmin)
admin.site.register(Champs, ChampsAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Page)
