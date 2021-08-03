import requests
import os
from melipayamak import Api

# for sms.ir
# def get_sms_provider_token():
#     request_url = "http://RestfulSms.com/api/Token"

#     request_body = {
#         "UserApiKey": os.getenv("SMS_API_KEY"),
#         "SecretKey": os.getenv("SMS_SECRET_KEY")
#     }

#     response = requests.post(url=request_url, data=request_body)

#     return response.json()


# def get_sms_line(token):
#     headers = {"x-sms-ir-secure-token": token}

#     request_url = "http://RestfulSms.com/api/SMSLine"

#     response = requests.request(
#         "GET", request_url, headers=headers)

#     return response.json()


# def send_verifiction_code(code, mobileNumber):

#     token = get_sms_provider_token()

#     headers = {"x-sms-ir-secure-token": token}

#     request_url = "http: // RestfulSms.com/api/VerificationCode"

#     request_body = {
#         "Code": code,
#         "MobileNumber": mobileNumber
#     }

#     response = requests.post(
#         url=request_url, headers=headers, data=request_body)

#     return response.json()


# def send_ultra_fast_message(templateID, mobileNumber, *args, **kwargs):

#     token = get_sms_provider_token()

#     headers = {"x-sms-ir-secure-token": token}

#     request_url = "http: // RestfulSms.com/api/VerificationCode"

#     request_body = {
#         "TemplateId": templateID,
#         "Mobile": mobileNumber,
#         "ParameterArray": [{"Parameter": "Parameters" + key+1, "ParameterValue": value}
#                            for key, value in kwargs.items()]
#     }

#     response = requests.post(
#         url=request_url, headers=headers, data=request_body)

#     return response.json()

# for melipayamak.ir
def send_activation_sms(code, mobile_number):
    username = os.getenv("SMS_API_USER"),
    password = os.getenv("SMS_API_PASSWORD"),
    api = Api(username, password)
    sms_rest = api.sms()
    to = mobile_number
    sended_sms = sms_rest.send_by_base_number(code, to, "52842")
    print(sended_sms)
    return sended_sms["RetStatus"]
