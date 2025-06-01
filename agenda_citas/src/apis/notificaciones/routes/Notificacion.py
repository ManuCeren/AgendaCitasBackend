from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime

from apis.notificaciones.models.NotificacionesModels import NotificacionesModels
from apis.notificaciones.models.entities.Notificaciones import Notificaciones
from apis.notificaciones.services.servicesTwilio import send_whatsapp_message
from apis.notificaciones.services.consulta_notificaciones import get_notification_data
from apis.telefonos.models.TelefonosModels import TelefonosModels

main = Blueprint('notificaciones_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_notificaciones():
    try:
        notificaciones = NotificacionesModels.get_all_notificaciones()
        return jsonify(notificaciones), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@main.route('/<id>', methods=['GET'])
def get_notificacion_by_id(id):
    try:
        notificacion = NotificacionesModels.get_notificacion_by_id(id)
        if notificacion:
            return jsonify(notificacion), 200
        else:
            return jsonify({"error": "Notificación no encontrada"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@main.route('/add', methods=['POST'])
def add_notificacion():
    try:
        data = request.get_json()

        required_fields = ['id_cita', 'fecha_envio', 'medio', 'estado']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 400

        # Crear la notificación
        notificacion = Notificaciones(
            id_notificacion=str(uuid.uuid4()),
            id_cita=data['id_cita'],
            fecha_envio=datetime.strptime(data['fecha_envio'], '%Y-%m-%d'),  # formato ISO
            medio=data['medio'],
            estado=data['estado']
        )

        # Insertar en la base de datos
        NotificacionesModels.add_notificacion(notificacion)

        # Obtener datos de la cita/paciente para enviar mensaje
        notification_data = get_notification_data(data['id_cita'])

        if not notification_data:
            return jsonify({"error": "No se encontró información para la notificación"}), 404

        # Obtener los teléfonos de ese paciente
        telefonos = TelefonosModels.get_telefonos_by_paciente(notification_data['id_paciente'])

        # Enviar el mensaje a cada teléfono
        send_results = []
        for tel in telefonos:
            numero = tel['numero_telefono']
            if not numero.startswith('+'):
                numero = f'+503{numero}'  # Código por defecto

            mensaje = (
                f"Estimado/a {notification_data['nombre_paciente']}, "
                f"le recordamos su cita para el día {notification_data['fecha_cita']}.\n"
                f"Motivo: {notification_data['motivo']}.\n"
                f"Gracias por usar nuestra agenda de citas."
            )

            # Enviar con Twilio
            result = send_whatsapp_message(numero, mensaje)
            send_results.append(result.sid if result else 'Error al enviar')

        return jsonify({
            "message": "Notificación registrada y mensajes enviados.",
            "telefonos": [tel['numero_telefono'] for tel in telefonos],
            "envio_resultado": send_results
        }), 201

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
