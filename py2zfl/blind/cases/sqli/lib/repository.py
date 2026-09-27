"""Data access for the orders table."""


class OrderRepository:
    def __init__(self, conn):
        self.conn = conn

    def find_by_status(self, status, limit=50):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, customer, total, status FROM orders "
            "WHERE status = ? ORDER BY id DESC LIMIT ?",
            (status, limit),
        )
        return cur.fetchall()

    def search(self, term):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, customer, total FROM orders "
            f"WHERE customer LIKE '%{term}%' OR reference LIKE '%{term}%'"
        )
        return cur.fetchall()
