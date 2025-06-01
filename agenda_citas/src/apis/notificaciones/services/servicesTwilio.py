from twilio.rest import Client
from config.config import Config

def send_whatsapp_message(to_number, body):
    try:
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=body,
            from_='whatsapp:' + Config.TWILIO_WHATSAPP_NUMBER,
            to='whatsapp:' + to_number
        )
        print(f"Mensaje enviado: {message.sid}")
        return message
    except Exception as ex:
        print(f"Error al enviar mensaje: {ex}")
        return None
