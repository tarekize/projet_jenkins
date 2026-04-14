import smtplib
import sys
from email.mime.text import MIMEText

def envoyer_email(statut, build_url, job_name):
    # --- CONFIGURATION (À MODIFIER PAR L'UTILISATEUR) ---
    expediteur = "testemail272002@gmail.com"
    mot_de_passe = "epsi2026"
    destinataire = "testemail272002@gmail.com"
    # ----------------------------------------------------

    sujet = f"Jenkins Build {statut.upper()} - {job_name}"
    
    if statut == "failure":
        corps = f"Le build Jenkins a échoué.\n\nVous pouvez consulter les logs ici : {build_url}"
    elif statut == "fixed":
        corps = f"Le build Jenkins est de nouveau stable (Corrigé).\n\nConsultez le build ici : {build_url}"
    else:
        corps = f"Statut inconnu : {statut}"

    msg = MIMEText(corps, "plain", "utf-8")
    msg['Subject'] = sujet
    msg['From'] = expediteur
    msg['To'] = destinataire

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(expediteur, mot_de_passe)
        server.sendmail(expediteur, destinataire, msg.as_string())
        server.quit()
        print(f"Email envoyé avec succès pour le statut {statut}.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python send_email.py <statut> <build_url> <job_name>")
        sys.exit(1)
        
    statut = sys.argv[1]
    build_url = sys.argv[2]
    job_name = sys.argv[3]
    
    envoyer_email(statut, build_url, job_name)
