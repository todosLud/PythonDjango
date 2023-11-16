from django.db import models
from django.contrib.auth.admin import User 
#Per immagine preview in admin
from django.utils.html import mark_safe
# Create your models here.
from django.dispatch import receiver
from django.db.models.signals import post_save


from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToCover
from django_cleanup import cleanup

from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField

from django.core.validators import RegexValidator



class CategoriaCarousel(models.Model):
    nome = models.CharField("Nome categoria", max_length=150)
    
    def __str__(self):
        return self.nome
    
@cleanup.select   
class Carousel(models.Model):
    titolo = models.CharField("Titolo della slide", max_length=200)
    sottotitolo = models.CharField("Sottotitolo della slide", max_length=250, blank=True, null=True)
    #corpo = models.TextField("Contenuto della slide")
    corpo = RichTextUploadingField("Contenuto dello slide")
    img = models.ImageField("Immagine Slide", upload_to='slide/%Y/%m/', blank=True, null=True)
    img_resize = ImageSpecField(source='img', processors=[ResizeToCover(500, 500)], format='png', options={'quality': 60})
    pubblicato = models.BooleanField("Pubblicato",default=False)
    categoria = models.ForeignKey(CategoriaCarousel, on_delete=models.CASCADE, related_name='categoria', default=None)

    def __str__(self):
        return self.titolo
    
    #Per visualizzare immagine in Admin
    def img_preview(self):
        return mark_safe(f'<img src="{self.img.url}" width="150" />')
    
#Models per utenti, incremento le info di base dei utenti
@cleanup.select
class UserProfile(models.Model):
    
    #le scelte per il campo di tipo select
    ACCOUNT_TYPE_CHOICES =(
        ('admin','Admin'),
        ('developer','Developer'),
        ('cliente','Cliente'),
        ('magazziniere','Magazziniere')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascita = models.DateField("Data di nascita", null=True, blank=True)
    cf = models.CharField("Codice fiscale", max_length=16, null=True, blank=True, unique=True,#r(?i)''
                          validators=[RegexValidator(
                               regex=r'^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$',
                               message='Inserisci un CF valido')])
    tipo_account = models.CharField("Tipologia utente", 
                                    max_length=50, 
                                    default='cliente', 
                                    choices=ACCOUNT_TYPE_CHOICES)
    img_profilo = ProcessedImageField(upload_to='user_profile/%Y/%m/%d/',
                                           processors=[ResizeToCover(64, 64)],
                                           format='PNG',
                                           options={'quality': 60},
                                           default='user_profile/profile_user.png')
    indirizzo = models.CharField(max_length=250, null=True, blank=True)
    comune = models.CharField(max_length=200, null=True, blank=True)
    citta = models.CharField(max_length=150, null=True, blank=True)
    cap = models.CharField("C.A.P.", max_length=5, null=True, blank=True, 
                           validators=[RegexValidator(
                               regex=r'^[0-9]{5}$',
                               message='Inserisci un cap valido')])
    
    def __str__(self):
        return self.user.username
    
    #Metodo per visualizzare preview in admin
    def img_preview(self):
        return mark_safe(f'<img src="{self.img_profilo.url}" width="100"/>')

    def save(self, *args, **kwargs):
        if self.cf:
            self.cf = self.cf.upper()
            super(UserProfile, self).save(*args, **kwargs)
        else:
            return None
    
    #salvo il profilo utente appena si crea un profilo
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance,created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

       
    
    
    
    
    