from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.views.generic.base import TemplateView
from .models import Subscription,SingleOrder
from registration.models import User

import stripe


# Create your views here.
class IndexView(TemplateView):
    template_name = 'core/index.html'

class AboutView(TemplateView):
    template_name = 'core/about.html'

class PrivacyView(TemplateView):
    template_name = 'core/privacy_policy.html'

class TermsView(TemplateView):
    template_name = 'core/terms_of_service.html'

class SuccessView(TemplateView):
    template_name = 'core/success.html'

@login_required
def createcustomersession(request):
    user = stripe.Customer.retrieve(request.user.stripe_customer)

    session = stripe.billing_portal.Session.create(
      customer=user.id,
      return_url= 'https://www.urbanseedandrecipe.com',

    )
    return HttpResponseRedirect(session.url)

@require_POST
@csrf_exempt
def webhook_view(request):
    payload=request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload,sig_header, settings.STRIPE_SIGNING_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type']=='customer.subscription.deleted':
        stripe_order = event['data']['object']
        order = Subscription.objects.get(stripe_id=stripe_order['id'])
        order.active = False
        order.save()
        print('Subscription Inactive')

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        order = event['data']['object']

        #create orders
        if order['mode']=='payment':

            # create single order
            new_order=SingleOrder.objects.create(
                email=order['customer_details']['email'],
                name=order['shipping']['name'])
            if order['shipping']:
                new_order.address1=order['shipping']['address']['line1']
                new_order.address2=order['shipping']['address']['line2']
                new_order.city=order['shipping']['address']['city']
                new_order.state=order['shipping']['address']['state']
                new_order.zip=order['shipping']['address']['postal_code']
            new_order.save()
        else:
            #check if user exists
            if User.objects.filter(email=order['customer_details']['email']).exists():
                print('user already exists!')
                user=User.objects.get(email=order['customer_details']['email'])
            else:
                user = User.objects.create_user(
                    email = order['customer_details']['email'],
                    password = None,
                    stripe_customer = str(order['customer'])
                )
                user.save()
            # create subscription order
            new_order=Subscription.objects.create(
                user=user,
                stripe_id=order['subscription'],
                name=order['shipping']['name'],
                active = True)
                if order['shipping']:
                    new_order.address1=order['shipping']['address']['line1']
                    new_order.address2=order['shipping']['address']['line2']
                    new_order.city=order['shipping']['address']['city']
                    new_order.state=order['shipping']['address']['state']
                    new_order.zip=order['shipping']['address']['postal_code']
            new_order.save()


    return HttpResponse(status=200)
