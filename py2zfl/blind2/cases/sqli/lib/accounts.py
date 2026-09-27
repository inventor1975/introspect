"""Account data access shared by the admin and self-service blueprints."""


def fetch_account(conn, email):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, email, display_name, status FROM accounts WHERE email = %s",
            (email.lower(),),
        )
        return cur.fetchone()


def accounts_with_status(conn, status):
    with conn.cursor() as cur:
        cur.execute("SELECT id, email FROM accounts WHERE status = '" + status + "' ORDER BY id")
        return cur.fetchall()
