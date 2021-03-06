import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from .models import Product
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from accounts.models import Payment
from users.models import Host, Worker

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
#The below is created following a tutorial that can be found here: https://www.youtube.com/watch?v=722A27IoQnk&t=716s


def Success(request):
    return render(request, "products/success.html")


def Cancel(request):
    return render(request, "products/cancel.html")

# inspired by https://www.youtube.com/watch?v=722A27IoQnk&t=2539s
# This creates the page in which users fill in their details
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        # get the product stored in the db
        product_id = Product.objects.get(name="subscription").id
        product = Product.objects.get(id=product_id)
        # define where you would like Stripe to redirect to post payment
        YOUR_DOMAIN = "https://language-stay.herokuapp.com"
        checkout_session = stripe.checkout.Session.create(
            # create a dictionary to pass through to Stripe checjout
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': product.price_id,
                    'quantity': 1,
                },
            ],
            # This is used to identify the user in the webhook view post payment
            metadata={
                "user_id": request.user.id,
                "user_role": request.user.role 
            },
            mode='payment',
            # The exact URL to redirect to depending on success or failure
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return redirect(checkout_session.url, code=303)

# This recieves the request that is send back from Stripe on successful payment
@csrf_exempt
def StripeWebhook(request):
    payload = request.body
    # required to verify request is coming from Stripe
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    # checking request does have correct header
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # If the request is correct
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # update the payment_status attribute in the Host/Worker model to paid
        customer_id = session["metadata"]["user_id"]
        customer_role = session["metadata"]["user_role"]
        if customer_role == "host":
            obj = Host.objects.get(user=customer_id)
            obj.payment_status = 'paid'
            obj.save()
        elif customer_role == "worker":
            obj = Worker.objects.get(user=customer_id)
            obj.payment_status = 'paid'
            obj.save()
            
    # Passed signature verification
    return HttpResponse(status=200)
