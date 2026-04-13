# -*- coding: utf-8 -*-
import smtplib
from email.message import EmailMessage
import sys
import os

def send_alert(status, build_url, job_name):
    email = 'chel65520@gmail.com'
    password = 'vgoh snjg nnmd qgxb'
    
    msg = EmailMessage()
    
    if status == 'failure':
        msg["Subject"] = f"❌ ALERTE : Échec du build {job_name}"
        msg.set_content(f"Le build a échoué pendant l'exécution.\n\nVeuillez vérifier les logs ici : {build_url}")
    elif status == 'fixed':
        msg["Subject"] = f"✅ CORRECTION : Build {job_name} corrigé et stable"
        msg.set_content(f"Le problème du build a été résolu. Le build est de nouveau fonctionnel.\n\nLien : {build_url}")
    else:
        return

    msg["From"] = email
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, password)
            server.send_message(msg)
        print(f"Email envoyé avec succès pour le statut {status}.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python send_email.py <status> <build_url> <job_name>")
        sys.exit(1)
    
    status = sys.argv[1]
    build_url = sys.argv[2]
    job_name = sys.argv[3]
    
    send_alert(status, build_url, job_name)
