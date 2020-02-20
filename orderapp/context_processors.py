from orderapp.forms import OrderForm

def order_form(request):
    order_form = OrderForm()
    return {'order_form': order_form}