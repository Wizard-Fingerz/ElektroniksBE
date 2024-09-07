import paystack

def generate_paystack_bank_transfer_payment_link(payment, amount):
    # Create a Paystack bank transfer payment object
    paystack_bank_transfer = paystack.Transfer({
        "amount": amount,
        "currency": "USD",
        "description": "Order #{}".format(payment.order.id)
    })

    # Create the payment and get the payment link
    if paystack_bank_transfer.create():
        payment_link = paystack_bank_transfer.authorization_url
        return payment_link
    else:
        return None