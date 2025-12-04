import os
from flask import render_template, request, jsonify, redirect, url_for, Flask
from flask_mail import Mail, Message
try:
    import psycopg2
    import psycopg2.extras
except Exception:  # module may be missing in test environment
    psycopg2 = None

# Safe import of requests (may be missing in some environments)
try:
    import requests  # type: ignore
except Exception:  # module may be missing in test environment
    requests = None  # type: ignore

# karlab google pass qtmy xsok eegy leww

# --- Load environment from .env (if present) ---
def _load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    # Try python-dotenv if available
    try:
        from dotenv import load_dotenv  # type: ignore
        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            load_dotenv()
    except Exception:
        # Fallback: minimal .env parser so we don't depend on external packages
        if os.path.exists(env_path):
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for raw in f:
                        line = raw.strip()
                        if not line or line.startswith('#'):
                            continue
                        if '=' not in line:
                            continue
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and key not in os.environ:
                            os.environ[key] = value
            except Exception as e:
                print(f"[ENV] Failed to load .env: {e}")

# Load env as early as possible
_load_env()

app = Flask(__name__)

# --- Global CSS injection for dark mode ---
@app.after_request
def _inject_dark_mode_css(response):
    """Inject a link to dark mode stylesheet into HTML responses."""
    try:
        ctype = response.headers.get('Content-Type', '')
        if 'text/html' in ctype and not response.direct_passthrough:
            html = response.get_data(as_text=True)
            # Avoid duplicate injection
            if '</head>' in html and 'href="/static/dark.css"' not in html:
                link_tag = '\n<link rel="stylesheet" href="/static/dark.css">\n'
                html = html.replace('</head>', f'{link_tag}</head>', 1)
                response.set_data(html)
    except Exception as e:
        print(f"[THEME] Injection error: {e}")
    return response

# --- Mail configuration ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')  # Adres serwera SMTP
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))  # Port SMTP
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'  # Użycie TLS
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Adres docelowy/inbox
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Hasło aplikacyjne
# Domyślny nadawca – jeśli nie podano, użyj konta odbiorczego
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])
mail = Mail(app)

# --- Database configuration (PostgreSQL) ---
DB_NAME = os.getenv('PGDATABASE', os.getenv('DB_NAME'))
DB_USER = os.getenv('PGUSER', os.getenv('DB_USER'))
DB_PASSWORD = os.getenv('PGPASSWORD', os.getenv('DB_PASSWORD', ''))
DB_HOST = os.getenv('PGHOST', os.getenv('DB_HOST', 'localhost'))
DB_PORT = int(os.getenv('PGPORT', os.getenv('DB_PORT', '5432')))


def get_db_connection():
    """Return a new psycopg2 connection or None if connection fails or module missing."""
    if psycopg2 is None:
        print("[DB] psycopg2 not installed; skipping DB connection.")
        return None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except Exception as e:
        print(f"[DB] Connection error: {e}")
        return None


def init_db():
    """Create inquiries and newsletter tables if they don't exist."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn, conn.cursor() as cur:
            # Business inquiries table
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS inquiries (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    company TEXT,
                    business_needs TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    budget_range TEXT NOT NULL,
                    timeline TEXT,
                    project_description TEXT NOT NULL,
                    additional_info TEXT,
                    client_ip TEXT,
                    user_agent TEXT
                );
                """
            )
            # Newsletter subscriptions table
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS newsletter_subscriptions (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    email TEXT UNIQUE NOT NULL,
                    source_page TEXT,
                    client_ip TEXT,
                    user_agent TEXT
                );
                """
            )
        return True
    except Exception as e:
        print(f"[DB] Init error: {e}")
        return False
    finally:
        try:
            conn.close()
        except Exception:
            pass


# Initialize database table on startup (best-effort)
init_db()


@app.route('/base.html')
def hello():
    return render_template('base.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/references.html')
def references():
    return render_template('references.html')


@app.route('/certs.html')
def certs():
    return render_template('certs.html')

@app.route('/projects.html')
def projects():
    return render_template('projects.html')

@app.route('/newsletter/thank-you')
def newsletter_thanks():
    """Thank-you page after newsletter subscription."""
    status = (request.args.get('status') or 'subscribed').lower()
    duplicate = status in ('exists', 'duplicate')
    return render_template('subscribe_thanks.html', duplicate=duplicate)


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    submitted = False

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_content = request.form.get('message')

        # 1) Wiadomość do Ciebie
        msg_to_you = Message(
            subject="Nowa wiadomość z formularza kontaktowego",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg_to_you.body = f"""
Imię i nazwisko: {name}
E-mail: {email}

Wiadomość:
{message_content}
        """

        # 2) Wiadomość zwrotna do użytkownika
        msg_to_user = Message(
            subject="Dziękujemy za kontakt!",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email]
        )
        msg_to_user.body = f"""
Cześć {name},

Dziękuję za wiadomość! Odezwę się tak szybko, jak to możliwe.

Twoja wiadomość:
{message_content}

Pozdrawiam,
KARLAB Software
        """

        # wysyłka
        mail.send(msg_to_you)
        mail.send(msg_to_user)

        submitted = True

    return render_template('contact.html', submitted=submitted)



# --- AI Chatbot helpers ---
try:
    # Prefer the new SDK if available
    from openai import OpenAI  # type: ignore
    _HAS_OPENAI_V1 = True
except Exception:
    OpenAI = None  # type: ignore
    _HAS_OPENAI_V1 = False


def get_ai_reply(message: str, history):
    """Return AI-generated reply if OPENAI/AIMLAPI key is configured; otherwise None.
    Uses a concise, safe system prompt with site context (Polish by default).
    """
    # Prefer AIMLAPI creds if provided, fall back to OPENAI_API_KEY for compatibility
    api_key = os.getenv('AIMLAPI_API_KEY') or os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('AIMLAPI_BASE_URL', 'https://api.aimlapi.com/v1')
    if not api_key:
        return None

    # Cap history for token safety
    trimmed = []
    try:
        # convert history [[role, content], ...] to OpenAI format
        for role, content in history[-8:]:
            if role in ("user", "assistant") and isinstance(content, str):
                trimmed.append({"role": role, "content": content[:2000]})
    except Exception:
        trimmed = []

    system_prompt = (
        "Jesteś profesjonalnym asystentem KARLAB Software. Odpowiadasz uprzejmie i konkretnie, po polsku,"
        " chyba że użytkownik używa innego języka. Zakres: rozwój oprogramowania, Python, AI/ML,"
        " automatyzacje, analityka danych, konsulting techniczny. Jeśli pytanie wykracza poza te tematy,"
        " odpowiadasz krótko i rzeczowo. Kiedy ma to sens, zaproponuj dalsze kroki (np. wycenę, rozmowę)."
        " Dane kontaktowe: +48 690 125 306, contact@karlab.com, formularz Kontakt na stronie."
        " Unikaj wrażliwych danych i nie podawaj niezweryfikowanych informacji."
    )

    # Domyślnie użyj modelu gpt-4 (zgodnie z przykładem AIML API); można nadpisać przez ENV
    model = os.getenv('AIMLAPI_MODEL', os.getenv('OPENAI_MODEL', 'gpt-4'))

    messages = [{"role": "system", "content": system_prompt}] + trimmed + [
        {"role": "user", "content": message[:4000]}
    ]

    # Najpierw spróbuj SDK kompatybilnego z OpenAI, jeśli dostępny
    if _HAS_OPENAI_V1:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=512
            )
            return resp.choices[0].message.content.strip() if resp and resp.choices else None
        except Exception as e:
            print(f"[AI] OpenAI SDK error (fallback to requests): {e}")

    # Fallback: bezpośrednie wywołanie AIML API przez requests
    try:
        try:
            import requests as _requests  # lokalny import na wypadek braku globalnego
        except Exception:
            _requests = requests  # użyj modułu importowanego globalnie
        if _requests is None:
            return None

        resp = _requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 512,
            },
            timeout=30,
        )
        data = resp.json()
        choices = data.get("choices") or []
        if choices:
            msg = choices[0].get("message") or {}
            content = msg.get("content") or ""
            return content.strip() if content else None
        return None
    except Exception as e:
        print(f"[AI] AIML API error: {e}")
        return None


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chatbot backend endpoint used by static/chatbot.js
    Accepts JSON: {message: str, history: [[role, content], ...]}
    Returns JSON: {ok: bool, reply: str, history: same_format}
    """
    data = request.get_json(silent=True) or {}
    message = str((data.get('message') or '')).strip()
    history = data.get('history') or []
    if not message:
        return jsonify({"ok": False, "reply": "Brak wiadomości do przetworzenia."}), 400

    # Try to get AI reply; fall back to a deterministic message if unavailable
    reply = get_ai_reply(message, history)  # may be None if no API key or error
    if not reply:
        reply = (
            "Dziękuję za wiadomość! Aktualnie moduł AI jest niedostępny na serwerze. "
            "Możesz opisać krótko swój projekt lub pytanie – odpiszemy mailowo. "
            "Kontakt: contact@karlab.com lub formularz Kontakt na stronie."
        )

    # Update history on the server side for convenience to keep UI simple
    try:
        history = (history + [['user', message], ['assistant', reply]])[-20]
    except Exception:
        history = [['user', message], ['assistant', reply]]

    return jsonify({"ok": True, "reply": reply, "history": history}), 200


@app.route('/inquiry.html', methods=['GET', 'POST'])
def business_inquiry():
    submitted = False
    if request.method == 'POST':
        # Pobieranie danych z formularza
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        company = (request.form.get('company') or '').strip()
        business_needs = (request.form.get('business_needs') or '').strip()
        service_type = (request.form.get('service_type') or '').strip()
        budget_range = (request.form.get('budget_range') or '').strip()
        timeline = (request.form.get('timeline') or '').strip()
        project_description = (request.form.get('project_description') or '').strip()
        additional_info = (request.form.get('additional_info') or '').strip()

        errors = []
        if not name:
            errors.append('Brak imienia i nazwiska.')
        if not email or '@' not in email:
            errors.append('Nieprawidłowy e-mail.')
        if not business_needs:
            errors.append('Brak celu biznesowego.')
        if not service_type:
            errors.append('Brak typu usługi.')
        if not budget_range:
            errors.append('Brak zakresu budżetu.')
        if not project_description:
            errors.append('Brak opisu projektu.')

        if not errors:
            # Zapis do bazy danych (best-effort)
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            user_agent = request.headers.get('User-Agent', '')
            conn = get_db_connection()
            if conn:
                try:
                    with conn, conn.cursor() as cur:
                        cur.execute(
                            """
                            INSERT INTO inquiries
                            (name, email, company, business_needs, service_type, budget_range, timeline,
                             project_description, additional_info, client_ip, user_agent)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (name, email, company, business_needs, service_type, budget_range,
                             timeline, project_description, additional_info, client_ip, user_agent)
                        )
                except Exception as e:
                    print(f"[DB] Insert error: {e}")
                finally:
                    try:
                        conn.close()
                    except Exception:
                        pass

            # 1) Mail do Ciebie (admina)
            try:
                body = (
                    f"Nowe zapytanie biznesowe:\n\n"
                    f"Imię i nazwisko: {name}\n"
                    f"E-mail: {email}\n"
                    f"Firma: {company}\n"
                    f"Typ usługi: {service_type}\n"
                    f"Budżet: {budget_range}\n"
                    f"Termin: {timeline}\n\n"
                    f"Cel biznesowy:\n{business_needs}\n\n"
                    f"Opis projektu:\n{project_description}\n\n"
                    f"Dodatkowe informacje:\n{additional_info}\n\n"
                    f"IP: {request.remote_addr} | UA: {user_agent}"
                )

                msg_to_admin = Message(
                    subject='Nowe zapytanie biznesowe (inquiry.html)',
                    recipients=[app.config['MAIL_USERNAME']],
                    body=body,
                )
                mail.send(msg_to_admin)

            except Exception as e:
                print(f"[MAIL] Send error: {e}")

            # 2) Mail potwierdzający do użytkownika
            try:
                confirmation_body = (
                    f"Cześć {name},\n\n"
                    f"Dziękujemy za przesłanie zapytania biznesowego!\n"
                    f"Odezwę się do Ciebie tak szybko, jak to możliwe.\n\n"
                    f"Twoje zgłoszenie:\n"
                    f"- Usługa: {service_type}\n"
                    f"- Budżet: {budget_range}\n"
                    f"- Firma: {company or '—'}\n\n"
                    f"Opis projektu:\n{project_description}\n\n"
                    f"Pozdrawiam,\nKARLAB Software"
                )

                msg_to_user = Message(
                    subject='Potwierdzenie otrzymania zapytania – KARLAB Software',
                    recipients=[email],
                    body=confirmation_body,
                )
                mail.send(msg_to_user)

            except Exception as e:
                print(f"[MAIL] User confirmation error: {e}")

            submitted = True

        else:
            print(f"[INQUIRY] Validation errors: {errors}")

        print(f"Nowe zapytanie od: {name} ({email}) | Firma: {company} | Usługa: {service_type} | Budżet: {budget_range}")

    return render_template('inquiry.html', submitted=submitted)
