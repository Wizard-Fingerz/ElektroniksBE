import os
import requests

flw_secret_key = os.getenv('FLUTTERWAVE_SECRET_KEY')
# redirect_url = os.getenv('FLUTTERWAVE_REDIRECT_URL')
redirect_url = 'https://electonics.com'

def generate_flutterwave_payment_link(payment, amount):
    print(amount)
    url = 'https://api.flutterwave.com/v3/payments'
    headers = {
        # 'Authorization': f'Bearer {flw_secret_key}',
        'Authorization': f'Bearer FLWSECK_TEST-e0c97b32a48885a80a52d8509558520c-X',
        'Content-Type': 'application/json',
    }

    tx_ref = payment.id
    customid = payment.order.user.id
    metadata = payment.order.id
    email = payment.order.user.email
    phonenumber = payment.order.user.phone_number
    name = payment.order.user.first_name
    vendor = payment.order.user

    data = {
        'tx_ref': tx_ref,
        'amount': amount,
        'currency': 'NGN',
        'redirect_url': redirect_url,
        'payment_options': 'card, mobilemoneyghana, ussd',
        'meta': {
            'consumer_id': customid,
            'billing_instance': metadata,
        },
        'customer': {
            'email': email,
            'phone_number': phonenumber,
            'name': name,
        },
        'customizations': {
            'title': vendor.first_name,
            'description': 'Payment for a product',
            # 'logo': vendor.profile_image,
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        print(f"Status: {response.status_code}")  # Print the status code
        print(response_data)
        payment_link = response_data['data']['link']
        return payment_link
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None