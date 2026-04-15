import os
import resend
from app.tasks.celery_app import celery

resend.api_key = os.getenv("RESEND_API_KEY")


@celery.task
def enviar_notificacion_tarea(email: str, titulo: str, fecha_limite: str):
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": f"Recordatorio: {titulo}",
            "html": f"""
                <h2>Recordatorio de tarea</h2>
                <p>Tu tarea <strong>{titulo}</strong> vence el <strong>{fecha_limite}</strong>.</p>
                <p>No te olvides de completarla a tiempo.</p>
            """
        })
        return {"status": "enviado", "email": email}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}