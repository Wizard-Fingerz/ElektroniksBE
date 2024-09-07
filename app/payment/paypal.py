import paypalrestsdk

def generate_paypal_payment_link(payment, amount):
    # Create a PayPal payment object
    paypal_payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "https://example.com/return",
            "cancel_url": "https://example.com/cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Order #{}".format(payment.order.id),
                    "sku": "ORDER-{}".format(payment.order.id),
                    "price": amount,
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "currency": "USD",
                "total": amount
            },
            "description": "Order #{}".format(payment.order.id)
        }]
    })

    # Create the payment and get the approval URL
    if paypal_payment.create():
        approval_url = paypal_payment.transactions[0].related_resources[0].approval_url
        return approval_url
    else:
        return None