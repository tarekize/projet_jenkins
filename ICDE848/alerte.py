    def send_alert(self,email):
        """Envoi d'alerte par email"""
        msg = MIMEText(f"""
        🚨 Alerte DDoS - {time.ctime()}
        
        Interfaces surveillées: {', '.join(self.interfaces)}
        Protection: {'Toutes les IPs' if CONFIG['PROTECTED_IPS'] == 'all' else CONFIG['PROTECTED_IPS']}
        Débit total: {rate:.1f} paquets/s
        
        Attaquants bloqués:
        {', '.join(attackers)}
        """)
        
        msg["Subject"] = f"ALERTE erreur"
        msg["From"] = "noreply@ddosguard.com"
        msg["To"] = email

        try:
            with smtplib.SMTP_SSL(
                CONFIG["SMTP_CONFIG"]["server"],
                CONFIG["SMTP_CONFIG"]["port"]
            ) as server:
                server.login(
                    CONFIG["SMTP_CONFIG"]["username"],
                    CONFIG["SMTP_CONFIG"]["password"]
                )
                server.send_message(msg)
            self._print_status("Notification envoyée", "success")
        except Exception as e:
            self._print_status(f"Erreur email: {e}", "error")


