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
