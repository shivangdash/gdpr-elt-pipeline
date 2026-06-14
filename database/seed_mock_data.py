"""Insert mock customer/order/payment and consent data."""

from __future__ import annotations

from sqlalchemy import text

from database.connection import create_db_engine


def seed() -> None:
    engine = create_db_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO customer_data (customer_id, name, email, phone, ssn, address)
                VALUES
                    ('CUS-1', 'Alice Doe', 'alice@example.com', '+49123456789', '123-45-6789', '1 Main St')
                ON CONFLICT (customer_id) DO NOTHING
                """
            )
        )
        conn.execute(
            text(
                """
                INSERT INTO orders (order_id, customer_id, order_total)
                VALUES ('ORD-1', 'CUS-1', 120.50)
                ON CONFLICT (order_id) DO NOTHING
                """
            )
        )
        conn.execute(
            text(
                """
                INSERT INTO payments (payment_id, order_id, amount, payment_method)
                VALUES ('PAY-1', 'ORD-1', 120.50, 'card')
                ON CONFLICT (payment_id) DO NOTHING
                """
            )
        )
        conn.execute(
            text(
                """
                INSERT INTO consent_events (event_id, customer_id, consent_type, granted)
                VALUES ('CONSENT-1', 'CUS-1', 'marketing_email', TRUE)
                ON CONFLICT (event_id) DO NOTHING
                """
            )
        )


if __name__ == "__main__":
    seed()
