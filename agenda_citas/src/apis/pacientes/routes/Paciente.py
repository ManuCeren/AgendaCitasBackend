from flask import Blueprint, jsonify, request
import uuid
from apis.pacientes.models.PacientesModels import PacientesModels
from apis.pacientes.models.entities.Pacientes import Pacientes
from datetime import datetime, date

paciente_bd = Blueprint('paciente_blueprint', __name__)

@paciente_bd.route('/', methods=['GET'])
def get_pacientes():
    try:
        pacientes = PacientesModels.get_all_pacientes()
        if pacientes:
            return jsonify(pacientes), 200
        else:
            return jsonify({"error": "No se encontraron pacientes"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@paciente_bd.route('/<id>', methods=['GET'])
def get_paciente_by_id(id):
    try:
        paciente = PacientesModels.get_paciente_by_id(id)
        if paciente:
            return jsonify(paciente)
        else:
            return jsonify({"error": "Paciente no encontrado"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@paciente_bd.route('/add', methods=['POST'])
def add_paciente():
    try:
        data = request.get_json()

        fecha_nac_str = data.get('fecha_nacimiento')
        fecha_nac_obj = date.fromisoformat(fecha_nac_str) if fecha_nac_str else None

        paciente = Pacientes(
            id_paciente=str(uuid.uuid4()),
            nombre=data.get('nombre'),
            fecha_nacimiento=fecha_nac_obj,
            email=data.get('email'),
            telefono=None
        )

        PacientesModels.add_paciente(paciente)

        return jsonify({"message": "Paciente agregado correctamente."}), 201

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@paciente_bd.route('/update/<id>', methods=['PUT'])
def update_paciente(id):
    try:
        data = request.get_json()
        existing_paciente = PacientesModels.get_paciente_by_id(id)
        if not existing_paciente:
            return jsonify({"error": "Paciente no encontrado"}), 404
        
        required_fields = ['nombre', 'fecha_nacimiento', 'email']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 500

        paciente = Pacientes(
            id_paciente=id,
            nombre=data.get('nombre'),
            fecha_nacimiento=date.fromisoformat(data.get('fecha_nacimiento')),  
            email=data.get('email'),
            telefono=None  
        )

        affected_rows = PacientesModels.update_paciente(paciente)
        if affected_rows == 1:
            return jsonify({"message": "Paciente actualizado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el paciente"}), 400
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@paciente_bd.route('/delete/<id>', methods=['DELETE'])
def delete_paciente(id):
    try:
        paciente = Pacientes(
            id_paciente=id,
            nombre="",
            fecha_nacimiento=date.today(), 
            email="",
            telefono=None
        )
        affected_rows = PacientesModels.delete_paciente(paciente)
        if affected_rows == 1:
            return jsonify({"message": f"Paciente {id} eliminado"}), 200
        else:
            return jsonify({"error": "Paciente no encontrado"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
