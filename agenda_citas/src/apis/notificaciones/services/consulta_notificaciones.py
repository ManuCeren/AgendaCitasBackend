from database.database import get_connection

def get_notification_data(id_cita):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.id_cita, c.id_paciente, p.nombre, c.fecha_hora, c.motivo
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                WHERE c.id_cita = %s
            """, (id_cita,))
            row = cursor.fetchone()

            if row:
                return {
                    "id_cita": row[0],
                    "id_paciente": row[1],
                    "nombre_paciente": row[2],
                    "fecha_cita": row[3].strftime('%d/%m/%Y'),
                    "motivo": row[4]
                }
            else:
                return None
    except Exception as ex:
        print(f"Error en get_notification_data: {ex}")
        return None
    finally:
        if connection:
            connection.close()
