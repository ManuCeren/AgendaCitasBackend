from database.database import get_connection

def get_notification_data(paciente_id):
    connection = get_connection()
    query = """
        SELECT nombre, fecha_nacimiento, email
        FROM pacientes WHERE id_paciente = %s
    """
    results = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (paciente_id,))
            rows = cursor.fetchall()
            for row in rows:
                results.append({
                    "nombre": row[0],
                    "fecha_nacimiento": row[1],
                    "email": row[2]
                })
    except Exception as e:
        raise Exception(f"Error al ejecutar get_notification_data: {str(e)}")
    finally:
        connection.close()

    return results
