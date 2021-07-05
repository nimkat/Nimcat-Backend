# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from zeep import Client

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify_payment/'


def send_payment_request(amount):
    result = client.service.PaymentRequest(
        MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)
    else:
        return str(result.Status)


def verify_payment(request):
    payment_message = ""
    payment_status = False
    ref_id = ""
    status = ""
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(
            MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            payment_status = True
            payment_message = "تراکنش شما با موفقیت انجام شد."
            ref_id = str(result.RefID)
            status = str(result.Status)
        elif result.Status == 101:
            payment_status = False
            payment_message = "تراکنش شما ثبت گردید."
            ref_id = str(result.RefID)
            status = str(result.Status)
        else:
            payment_status = False
            payment_message = "تراکنش شما انجام نشد."
            ref_id = str(result.RefID)
            status = str(result.Status)
    else:
        payment_status = False
        payment_message = "تراکنش توسط کاربر لغو شد، یا اینکه موفقیت امیز نبود."

    context = {'ref_id': ref_id,
               'status': status,
               'payment_status': payment_status,
               'payment_message': payment_message
               }
    return render(request, 'verify_payment.html', context)
