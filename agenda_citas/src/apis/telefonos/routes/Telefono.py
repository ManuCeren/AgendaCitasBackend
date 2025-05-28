from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime

from apis.telefonos.models.TelefonosModels import TelefonosModels
from apis.telefonos.models.entities.Telefonos import Telefonos

main = Blueprint('telefonos_blueprint', __name__)

@main.route('/', methods=['GET'])
def get_all_telefonos():
    try:
        telefonos_list = TelefonosModels.get_all_telefonos() # Necesitarás este método en TelefonosModels
        if telefonos_list:
            return jsonify(telefonos_list), 200
        else:
            return jsonify({"message": "No se encontraron teléfonos."}), 404
    except Exception as ex:
        # Es buena práctica imprimir la excepción real para depuración
        print(f"Error en get_all_telefonos: {ex}")
        import traceback
        traceback.print_exc() # Esto imprimirá el traceback completo en la terminal
        return jsonify({"error": str(ex)}), 500
@main.route('/<id>', methods=['GET'])
def get_telefono_by_id(id):
    try:
        telefono = TelefonosModels.get_telefono_by_id(id)
        if telefono:
            return jsonify(telefono)
        else:
            return jsonify({"error": "Teléfono no encontrado"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@main.route('/add', methods=['POST'])
def add_telefono():
    try:
        data = request.get_json()
        required_fields = ['id_paciente', 'numero_telefono']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 400

        telefono = Telefonos(
            id_telefono=str(uuid.uuid4()),
            id_paciente=data['id_paciente'],
            numero_telefono=data['numero_telefono'],
        )

        rows_affected = TelefonosModels.add_telefono(telefono)
        return jsonify({"mensaje": "Teléfono agregado", "filas_afectadas": rows_affected}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
