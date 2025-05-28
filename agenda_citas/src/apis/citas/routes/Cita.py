from flask import Blueprint, jsonify, request
import uuid #que lo usarmemos para generarlos en Postgres
from apis.citas.models.CitasModels import CitaModel
from apis.citas.models.entities.Citas import Cita
from datetime import datetime #para manejar las fechas

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
        required_fields = ['id_paciente', 'motivo', 'estado']
        missing_fields = [field for field in required_fields if field not in data]            
        if missing_fields:
               return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 400
        
        citas = Cita(
            id_cita=cita_id, # type: ignore
            id_paciente=data.get('id_paciente' ),
            fecha_hora=datetime.now(),
            motivo=data.get('motivo'),
            estado=data.get('estado')
        )
        CitaModel.add_cita(citas)

        return jsonify({"message": "Cita agregada", "id": cita_id}), 201 # type: ignore

    except Exception as ex:
            return jsonify({"error": str(ex)}), 500

@main.route('/update/<id>', methods=['PUT' ])
def update_categoria(id): 
    try:
        data = request.get_json()
        existing_cita = CitaModel.get_cita_by_id(id)
        if not existing_cita:
            return jsonify({"error": "Cita no encontrada"}), 404
        required_fields = ['id_paciente', 'motivo', 'estado']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}),500
        
        citas = Cita(
            id_cita=id,
            id_paciente=data.get('id_paciente' ),
            fecha_hora=datetime.now(),
            motivo=data.get('motivo'),
            estado=data.get('estado')
        )
        affected_rows = CitaModel. update_cita(citas)
        if affected_rows == 1:
            return jsonify({"message": "Cita actualizada correctamente"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar la cita"}), 400
    except Exception as ex:
            return jsonify({"error": str(ex)}), 500

@main.route('/delete/<id>', methods=['DELETE' ])
def delete_cita(id):
    try:
        citas = Cita(
            id_cita=id,
            id_paciente="", 
            fecha_hora=datetime.now(),
            motivo="",
            estado=""
        )
        affected_rows = CitaModel. delete_cita(citas)
        if affected_rows == 1:
            return jsonify({"message": f"Cita {id} eliminada"}), 200
        else:
            return jsonify({"error": "Cita no encontrada"}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
