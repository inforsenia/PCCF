#!/usr/bin/env python3

"""
Enviament opcional de notificacions per correu (SMTP).

Disseny no invasiu: només envia res si es compleixen totes dues condicions:
  1. Variables d'entorn SMTP_HOST i SMTP_FROM configurades (stack Portainer).
  2. El destinatari existeix a `department_emails.json` (vore
     `get_department_email`).

Si falta qualsevol de les dues, `send_report_email` no fa res i torna
`False` -- cap excepció, cap canvi de comportament respecte a abans que
existira este mòdul. Els errors d'enviament (SMTP caigut, credencials
incorrectes, etc.) es capturen i es registren per stdout, mai interrompen
qui l'invoca (poller/publicació).

**Les adreces mai van en git.** El repositori és públic, així que els
correus dels caps de departament (dades personals) viuen exclusivament a
`department_emails.json`, un fitxer fora del repositori (bind mount al
servidor, path per defecte `/data/department_emails.json` via
`DEPARTMENT_EMAILS_FILE`; en local per defecte `temp/department_emails.json`,
ja gitignorat). Format:
    {"ESOBAT": {"ECONOMIA": "cap.economia@..."}, "FP": {"INF": "..."}}
Si el fitxer no existeix o el departament no hi apareix, no s'envia res
-- els JSON de currículum (`memoriaESOBAT/memories_*.json` etc.) no es
toquen mai per a este propòsit.

`SMTP_REPLY_TO` (opcional): si es defineix, s'afig una capçalera `Reply-To`
independent del remitent (`SMTP_FROM`) -- útil per a enviar amb un compte
tècnic tipus `notreply@...` mentre les respostes van a una bústia vigilada
(o per fer justament el contrari, un remitent "humà" amb respostes a un
`notreply@...`). Sense esta variable, el comportament és l'habitual: qui
respon ho fa a `SMTP_FROM`.
"""

import json
import os
import smtplib
import ssl
from email.message import EmailMessage

from memories_utils import PROJECT_DIR


def smtp_configured():
    return bool(os.environ.get("SMTP_HOST")) and bool(os.environ.get("SMTP_FROM"))


def get_department_email(tipus, familia):
    """Torna l'email del cap de departament, o None si no n'hi ha.

    Llig `department_emails.json` (mai en git -- vore docstring del mòdul).
    Qualsevol problema de lectura (fitxer absent, JSON malformat) es tracta
    com "sense email" -- mai llança excepció.
    """
    path = os.environ.get(
        "DEPARTMENT_EMAILS_FILE",
        os.path.join(PROJECT_DIR, "temp", "department_emails.json"),
    )
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            emails = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"[mailer] AVÍS: no s'ha pogut llegir {path}: {e}", flush=True)
        return None
    return emails.get(tipus, {}).get(familia)


def send_report_email(to_addr, subject, body, attachments=None):
    """Envia un correu si SMTP està configurat i hi ha destinatari.

    Torna True si s'ha enviat, False si s'ha omès (no configurat, sense
    destinatari) o si ha fallat l'enviament.
    """
    if not smtp_configured() or not to_addr:
        return False

    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    sender = os.environ["SMTP_FROM"]
    reply_to = os.environ.get("SMTP_REPLY_TO")
    use_tls = os.environ.get("SMTP_USE_TLS", "1") != "0"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    if reply_to:
        msg["Reply-To"] = reply_to
    msg["To"] = to_addr
    msg.set_content(body)

    for path in attachments or []:
        if not path or not os.path.isfile(path):
            continue
        with open(path, "rb") as f:
            data = f.read()
        if path.endswith(".pdf"):
            maintype, subtype = "application", "pdf"
        elif path.endswith(".txt"):
            maintype, subtype = "text", "plain"
        else:
            maintype, subtype = "application", "octet-stream"
        msg.add_attachment(data, maintype=maintype, subtype=subtype,
                            filename=os.path.basename(path))

    try:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            if use_tls:
                smtp.starttls(context=ssl.create_default_context())
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"[mailer] ERROR enviant correu a {to_addr}: {e}", flush=True)
        return False
