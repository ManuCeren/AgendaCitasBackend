from flask import Blueprint, jsonify, request
import uuid 
from apis.citas.models.CitasModels import CitaModel
from apis.citas.models.entities.Citas import Cita
from datetime import datetime 

main = Blueprint('cita_blueprint', __name__)

@main.route('/', methods=[ 'GET' ])
def get_citas():
    try:
        citas = CitaModel.get_all_citas()
        if citas:
             return jsonify(citas), 200
        else:
             return jsonify({"error": "No se encontraron citas"}), 404
    except Exception as ex:
     return jsonify({"error": str(ex)}), 500

@main. route('/<id>', methods=[ 'GET' ])
def get_citas_by_id(id):
    try:
        citas = CitaModel.get_citas_by_id(id)
        if citas:
             return jsonify(citas)
        else:
             return jsonify({"error": "Empleado no encontrado"}), 404
    except Exception as ex:
     return jsonify({"error": str(ex)}), 500
    
@main.route('/add', methods=['POST'])
def add_cita():
    try:
        data = request.get_json()
        required_fields = ['id_paciente', 'fecha_hora', 'motivo', 'estado']
        missing_fields = [field for field in required_fields if field not in data]            
        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 400

        cita_id = str(uuid.uuid4())

        citas = Cita(
            id_cita=cita_id,
            id_paciente=data.get('id_paciente'),
            fecha_hora=data.get('fecha_hora'),  
            motivo=data.get('motivo'),
            estado=data.get('estado')
        )
        CitaModel.add_cita(citas)

        return jsonify({"message": "Cita agregada", "id": cita_id}), 201

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@main.route('/<id>', methods=['PUT'])
def update_cita(id):
    try:
        data = request.get_json()

        # Convertir fecha_hora
        fecha_hora = datetime.fromisoformat(data.get('fecha_hora'))

        cita = Cita(
            id_cita=id,
            id_paciente=data.get('id_paciente'),
            fecha_hora=fecha_hora,
            motivo=data.get('motivo'),
            estado=data.get('estado')
        )

        affected_rows = CitaModel.update_cita(cita)

        if affected_rows == 1:
            return jsonify({"message": "Cita actualizada correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar la cita"}), 400

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    
@main.route('/<id>', methods=['DELETE'])
def delete_cita(id):
    try:
        affected_rows = CitaModel.delete_cita_by_id(id)
        if affected_rows == 1:
            return jsonify({"message": f"Cita {id} eliminada"}), 200
        else:
            return jsonify({"error": "Cita no encontrada"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
