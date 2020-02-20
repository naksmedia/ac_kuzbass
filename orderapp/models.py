from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class OrderService(models.Model):
    name = models.CharField(u'Имя контакта', max_length=50)
    phone = models.CharField(u'Телефон контакта', max_length=50)
    email = models.EmailField(u'Электронная почта контакта', max_length=254)
    compound = models.CharField(u'Состав заявки', max_length=300, default=None, blank=True, null=True)
    ready = models.BooleanField(u'Вопрос решен', default=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.name


class OrderEmailTemplate(models.Model):
    name = models.CharField(u'Название шаблона', max_length=50)
    html = RichTextField(verbose_name='Текст html', config_name='default')
    text = models.TextField(u'Текст plain', max_length=512)
    active = models.NullBooleanField(u'Активен')

    class Meta:
        verbose_name='Шаблон письма'
        verbose_name_plural='Шаблоны писем'

    def __str__(self):
        return self.name