from flask import Blueprint, jsonify, request
import uuid #que lo usarmemos para generarlos en Postgres
from apis.pacientes.models.PacientesModels import PacientesModels
from apis.pacientes.models.entities.Pacientes import Pacientes
from datetime import datetime #para manejar las fechas

paciente_bd = Blueprint('paciente_blueprint', __name__)

@paciente_bd.route('/', methods=[ 'GET' ])
def get_pacientes():
    try:
        pacientes = PacientesModels.get_all_pacientes()
        if pacientes:
             return jsonify(pacientes), 200
        else:
             return jsonify({"error": "No se encontraron pacientes"}), 404
    except Exception as ex:
     return jsonify({"error": str(ex)}), 500
    
@paciente_bd.route('/<id>', methods=[ 'GET' ])
def get_paciente_by_id(id):
    try:
        pacientes = PacientesModels.get_paciente_by_id(id)
        if pacientes:
             return jsonify(pacientes)
        else:
             return jsonify({"error": "Paciente no encontrado"}), 404
    except Exception as ex:
     return jsonify({"error": str(ex)}), 500
    
@paciente_bd.route('/add', methods=['POST'])
def add_paciente():
    try:
        data = request.get_json()
        required_fields = ['nombre', 'fecha_nacimiento', 'email']
        missing_fields = [field for field in required_fields if field not in data]            
        if missing_fields:
               return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 400
        fecha_nac_str = data.get('fecha_nacimiento')
        fecha_nac_obj = datetime.strptime(fecha_nac_str, '%d/%m/%Y')
        
        pacientes = Pacientes(
            id_paciente=paciente_id, # type: ignore
            nombre=data.get('nombre' ),
            fecha_nacimiento=fecha_nac_obj,
            email=data.get('email')
        )
        PacientesModels.add_paciente(pacientes)

        return jsonify({"message": "Paciente agregado", "id": paciente_id}), 201 # type: ignore

    except Exception as ex:
            return jsonify({"error": str(ex)}), 500

@paciente_bd.route('/update/<id>', methods=['PUT' ])
def update_paciente(id): 
    try:
        data = request.get_json()
        existing_paciente = PacientesModels.get_paciente_by_id(id)
        if not existing_paciente:
            return jsonify({"error": "Paciente no encontrado"}), 404
        
        required_fields = ['nombre', 'fecha_nacimiento', 'email']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}),500
        fecha_nac_str = data.get('fecha_nacimiento')
        fecha_nac_obj = datetime.strptime(fecha_nac_str, '%d/%m/%Y')

        pacientes = Pacientes(
            id_paciente=id,
            nombre=data.get('nombre' ),
            fecha_nacimiento=fecha_nac_obj,
            email=data.get('email')
        )
        affected_rows = PacientesModels. update_paciente(pacientes)
        if affected_rows == 1:
            return jsonify({"message": "Paciente actualizado correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar el paciente"}), 400
    except Exception as ex:
            return jsonify({"error": str(ex)}), 500

@paciente_bd.route('/delete/<id>', methods=['DELETE' ])
def delete_paciente(id):
    try:
        pacientes = Pacientes(
            id_paciente=id,
            nombre="", 
            fecha_nacimiento=datetime.now(),
            email=""
        )
        affected_rows = PacientesModels. delete_paciente(pacientes)
        if affected_rows == 1:
            return jsonify({"message": f"Paciente {id} eliminado"}), 200
        else:
            return jsonify({"error": "Paciente no encontrado"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
