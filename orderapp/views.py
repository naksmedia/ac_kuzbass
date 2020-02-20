from .models import *
from .forms import OrderForm
from django.template.loader import get_template
from django.core.mail import send_mail
from mainapp.models import Profile
from .models import OrderEmailTemplate
from django.template import engines
from django.http import JsonResponse


def accept_order(request):
    if request.method == 'POST':
        data = {
            "name": request.POST.get('name'),
            "phone": request.POST.get('phone'),
            "email": request.POST.get('email'),
            "captcha_1": request.POST.get('captcha_1'),
            "captcha_0": request.POST.get('captcha_0'),
            }
        order_variants = ['attst', 'attso', 'attsvsp', 'attlab', 'attsm', 'qual']
        if any([request.POST.get(order_item) for order_item in order_variants]):
            order_compound = {
                "Аттестация технологий": 'attst' in request.POST,
                "Аттестация оборудования": 'attso' in request.POST,
                "Аттестация персонала": 'attsvsp' in request.POST,
                "Аттестация лаборатории": 'attlab' in request.POST,
                "Аттестация материалов": 'attsm' in request.POST,
                "Оценка квалификации в области сварки": 'qual' in request.POST
            }
            data.update({"compound": "{}".format(order_compound)})
        else:
            order_compound = {'Ничего не заявлено': True}
        form = OrderForm(data)
        if form.is_valid():
            instance = form.save()
            current_absolute_url = request.build_absolute_uri()
            order_arr = []

            for key in order_compound.keys():
                if order_compound[key] is True:
                    order_arr.append(key)

            if Profile.objects.first():
                admin_email_address = Profile.objects.first().org_order_email.split(" ")
            else:
                admin_email_address = ['soft@naks.ru']

            html_template, plain_template = OrderEmailTemplate.objects.first().html, OrderEmailTemplate.objects.first().text

            django_engine = engines['django']
            html_message_template = django_engine.from_string(html_template)
            plain_message_template = django_engine.from_string(plain_template)

            cntxt = {
                "name": instance.name,
                "phone": instance.phone,
                "email": instance.email,
                "order_details": " ".join(order_arr)
            }

            html_content = html_message_template.render(cntxt)
            plain_content = plain_message_template.render(cntxt)

            # import pdb; pdb.set_trace()

            subject = 'Заполнена заявка на сайте {}'.format(current_absolute_url)
            from_email = 'noreply@naks.ru'
            to_ = [instance.email] + admin_email_address

            if not instance.name == 'tolik_make_tests':
                send_mail(
                    subject,
                    plain_content,
                    from_email,
                    to_,
                    fail_silently=False,
                    html_message=html_content
                )
            return JsonResponse({'message': 'ok', 'order_id': instance.pk})
        else:
            return JsonResponse({'errors': form.errors})