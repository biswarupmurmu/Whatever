from flask_testing import TestCase

from ourapp import create_app, db
from ourapp.models import CartItem, Category, Customer, Order, OrderedItem, Product


class TestApp(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_app(self):
        app = self.create_app()
        self.assertIsNotNone(app)

    def test_routes_exist(self):
        app = self.create_app()
        client = app.test_client()

        # Test a few routes
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/login")
        self.assertEqual(response.status_code, 200)

        response = client.get("/cart")
        self.assertEqual(
            response.status_code, 308
        )  # Assuming customer requires authentication

    def test_database_operations(self):
        app = self.create_app()
        with app.app_context():
            # Perform database operations
            user = Customer(
                fname="Firstname",
                lname="Lastname",
                email="email",
                password="password",
                verified_email=False,
            )
            db.session.add(user)
            db.session.commit()

            retrieved_customer = Customer.query.filter_by(fname="Firstname").first()
            self.assertIsNotNone(retrieved_customer)

    def test_views(self):
        app = self.create_app()
        client = app.test_client()

        response = client.get("/product/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.data)


if __name__ == "__main__":
    pass
