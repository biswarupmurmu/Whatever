from werkzeug.security import generate_password_hash
from flask_testing import TestCase

from ourapp import create_app
from ourapp.extensions import db
from ourapp.models import CartItem, Category, Customer, Order, OrderedItem, Product


class TestApp(TestCase):

    def create_app(self):        
        app = create_app()
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        return app

    def setUp(self):
        db.create_all()
        #Create a user for testing login
        self.test_user = Customer(
            fname="Test",
            lname="User",
            email="test@gmail.com",
            password=generate_password_hash("1234"),
        )
        db.session.add(self.test_user)
        db.session.commit()


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

    def test_signup(self):
        app = self.create_app()
        client = app.test_client()
        response = client.post('/auth/signup', data = {
            'fname' : 'FirstName',
            'lname' : 'LastName',
            'email' : 'okay@gmaill.com',
            'password' : '1234',
            'confirm_password' : '1234',
            'terms' : True
        }, follow_redirects = True)
        self.assertEqual(response.status_code, 302)

    # def test_login(self):
    #     app = self.create_app()
    #     client = app.test_client()
    #     response = client.post('/auth/login', data = {
    #         'email' : 'test@example.com',
    #         'password' : 'testpassword',
    #     }, follow_redirects = True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b"Welcome Test", response.data)

    def test_login(self):
        app = self.create_app()
        client = app.test_client()
        response = client.post('/auth/login', data={
            'email': 'qtest@example.com',
            'password': '1234',
            
        }, follow_redirects=True)

        print("Response status code:", response.status_code)
        print("Response data:", response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    pass
