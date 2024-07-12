import mercadopago
import asyncio
from verificar import get_credenciais

APIMERCADO = get_credenciais()['mercadopago_api']
credentials = {'access_token' : APIMERCADO  }


def get_payment(price, description):
    sdk = mercadopago.SDK(APIMERCADO)
    payment_data = { 
        "payer" : { 
            "email": f"test@gmail.com", 
        }, 
        "transaction_amount": float(price),
        "description": str(description),
        'payment_method_id': 'pix', 
        "date_of_expiration": expiration, 
    }   
    payment_response = sdk.payment().create(payment_data)
    if payment_response['status'] == 201:
        payment = payment_response["response"]
        data = payment['point_of_interaction']['transaction_data']
        return [str(data['qr_code']),str(payment['id'])]
    else:
        return None, payment_response['response']['message']


async def verify_payment(payment_id):
    sdk = mercadopago.SDK(APIMERCADO)
    await asyncio.sleep(15)
    payment_response = await asyncio.to_thread(sdk.payment().get, int(payment_id))
    payment = payment_response["response"]
    if payment['status'] == "approved" and payment['status_detail'] == "accredited":
        return True
    else:
        return await verify_payment(payment_id)
        
