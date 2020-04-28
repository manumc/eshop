from datetime import date

from data.load_data import con, cur

class Metrics:
    def total_items_sold(self, given_date):
        """
        The total number of items sold on a given day.
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"

        # get quantity from order_lines for given_date
        quantities = [
            i[0]
            for i in cur.execute("""
            SELECT quantity
            FROM orders
            INNER JOIN order_lines ON orders.id=order_lines.order_id
            WHERE created_at LIKE ?
            """, (given_date.isoformat()+'%',))
        ]

        # sum quantity
        return sum(quantities)


    def total_customers(self, given_date):
        """
        The total number of customers that made an order that day.
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"

        customer_ids = [
            i[0]
            for i in cur.execute("""
            SELECT customer_id
            FROM orders
            WHERE created_at LIKE ?
            """, (given_date.isoformat()+'%',))
        ]

        # return total number of customers without duplicates
        return len(set(customer_ids))

    def total_discount(self, given_date):
        """
        The total amount of discount given that day.
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"

        discounts = [
            i[0]
            for i in cur.execute("""
            SELECT discounted_amount
            FROM orders
            INNER JOIN order_lines ON orders.id=order_lines.order_id
            WHERE created_at LIKE ?
            """, (given_date.isoformat()+'%',))
        ]

        return sum(discounts)

    def average_discount_rate(self, given_date):
        """
        The average discount rate applied to the items sold that day.
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"

        discount_rates = [
            i[0]
            for i in cur.execute("""
            SELECT discount_rate
            FROM orders
            INNER JOIN order_lines ON orders.id=order_lines.order_id
            WHERE created_at LIKE ?
            """, (given_date.isoformat()+'%',))
        ]

        if len(discount_rates) == 0:
            return 0
        else:
            return sum(discount_rates)/len(discount_rates)

    def average_order_total(self, given_date):
        """
        The average order total for that day.
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"

        order_totals = [
            i[0]
            for i in cur.execute("""
            SELECT Sum(total_amount)
            FROM orders
            INNER JOIN order_lines ON orders.id=order_lines.order_id
            WHERE created_at LIKE ?
            GROUP BY order_id
            """, (given_date.isoformat()+'%',))
        ]

        if len(order_totals) == 0:
            return 0
        else:
            return sum(order_totals)/len(order_totals)

    def total_amount_commissions(self, given_date):
        """
        The total amount of commissions generated that day.

        Assumption made -> commission rate apply to product_price * quantity
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"

        amount_commissions = [
            i
            for i in cur.execute("""
            SELECT product_price, quantity, rate
            FROM orders
            INNER JOIN order_lines ON orders.id=order_lines.order_id
            INNER JOIN vendor_commissions
            ON orders.vendor_id=vendor_commissions.vendor_id
            AND date LIKE ?
            WHERE created_at LIKE ?
            """,
                (
                    given_date.isoformat()+'%',
                    given_date.isoformat()+'%'
                )
            )
        ]

        return sum([i[0] * i[1] * i[2] for i in amount_commissions])

    def average_amount_commissions(self, given_date):
        """
        The average amount of commissions per order for that day.
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"

        average_commissions = [
            i[0]
            for i in cur.execute("""
            SELECT Sum(product_price * quantity * rate)
            FROM orders
            INNER JOIN order_lines ON orders.id=order_lines.order_id
            INNER JOIN vendor_commissions
            ON orders.vendor_id=vendor_commissions.vendor_id
            AND date LIKE ?
            WHERE created_at LIKE ?
            GROUP BY order_id
            """,
                (
                    given_date.isoformat()+'%',
                    given_date.isoformat()+'%'
                )
            )
        ]

        if len(average_commissions) == 0:
            return 0
        else:
            return sum(average_commissions)/len(average_commissions)

    def commissions_per_promotion(self, given_date):
        """
        The total amount of commissions earned per promotion that day.
        """
        # ensure given_date is a date
        assert isinstance(given_date, date), "given_date must be datetime.date()"


        total_commission_per_promotion = [
            i
            for i in cur.execute("""
            SELECT promotion_id, Sum(product_price * quantity * rate)
            FROM orders
            INNER JOIN order_lines ON orders.id=order_lines.order_id
            INNER JOIN vendor_commissions
            ON orders.vendor_id=vendor_commissions.vendor_id
            AND vendor_commissions.date LIKE ?
            INNER JOIN product_promotions
            ON order_lines.product_id=product_promotions.product_id
            AND product_promotions.date LIKE ?
            WHERE created_at LIKE ?
            GROUP BY promotion_id
            """,
                (
                    given_date.isoformat()+'%',
                    given_date.isoformat()+'%',
                    given_date.isoformat()+'%'
                )
            )
        ]

        return { i[0]: i[1] for i in total_commission_per_promotion }

    def create_report(self, given_date):
        report = {
            "customers": self.total_customers(given_date),
            "total_discount_amount": self.total_discount(given_date),
            "items": self.total_items_sold(given_date),
            "order_total_avg": self.average_order_total(given_date),
            "discount_rate_avg": self.average_discount_rate(given_date),
            "commissions": {
                "promotions": self.commissions_per_promotion(given_date),
                "total": self.total_amount_commissions(given_date),
                "average": self.average_amount_commissions(given_date),
            },
        }

        return report
