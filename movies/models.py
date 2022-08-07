import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Time_Stamped_Mixin(models.Model):
    created = models.DateTimeField(_('created'),auto_now_add=True)
    modified = models.DateTimeField(_('modified'),auto_now=True)
    class Meta:
        abstract = True


class UUID_Mixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True


class Genre(UUID_Mixin, Time_Stamped_Mixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)


    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        

    def __str__(self):
        return self.name 
        
        
class Filmwork(UUID_Mixin, Time_Stamped_Mixin):
    class MovieType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    type = models.CharField(_('type'), max_length=15, choices=MovieType.choices)
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    genres = models.ManyToManyField(Genre, through='Genre_Filmwork')
    persons = models.ManyToManyField('Person', through='Person_Filmwork')
    certificate = models.CharField(_('certificate'),max_length = 512, blank=True)
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to='movies/')
    
    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film')
        verbose_name_plural = _('films')

    def __str__(self):
        return self.title 
    
    
class Genre_Filmwork(UUID_Mixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "content\".\"genre_film_work" 
        verbose_name = _('genre_filmwork')
        verbose_name_plural = _('genre_filmworks')
        
    def __str__(self):
        return f"{self.film_work.title} - {self.genre.name}"
        
        
        
class Person(UUID_Mixin, Time_Stamped_Mixin):
    full_name = models.CharField(_('full_name'),max_length = 150)
    
    class Meta:
        db_table = "content\".\"person" 
        verbose_name = _('persone')
        verbose_name_plural = _('persones')
        
    def __str__(self):
        return f"{self.full_name}"
        
        
class Person_Filmwork(UUID_Mixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True) 
    
    class Meta:
        db_table = "content\".\"person_film_work" 
        verbose_name = _('Person_Filmwork')
        verbose_name_plural = _('Persons_Filmworks')

    def __str__(self):
        return f"{self.film_work.title} - {self.person.full_name}"