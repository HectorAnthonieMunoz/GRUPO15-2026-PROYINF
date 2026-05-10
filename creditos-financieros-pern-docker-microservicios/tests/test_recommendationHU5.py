import unittest
import requests
import random

AUTH_URL = "http://127.0.0.1:4001"
RECOMMENDATION_URL = "http://127.0.0.1:3002/api/recommendation"


class TestRecommendationHU5(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Iniciando pruebas HU5")

        random_num = random.randint(1, 100000)

        cls.username = f"user_hu5_{random_num}"
        cls.password = "123456"
        cls.email = f"user_hu5_{random_num}@test.com"

        register_payload = {
            "username": cls.username,
            "email": cls.email,
            "password": cls.password
        }

        requests.post(
            f"{AUTH_URL}/register",
            json=register_payload,
            timeout=10
        )

        login_payload = {
            "username": cls.username,
            "password": cls.password
        }

        login_response = requests.post(
            f"{AUTH_URL}/login",
            json=login_payload,
            timeout=10
        )

        cls.token = login_response.json()["token"]

    @classmethod
    def tearDownClass(cls):
        print("Finalizando pruebas HU5")

    def test_hu5_recommendation_normal(self):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        payload = {
            "ingreso": 1000000
        }

        response = requests.post(
            RECOMMENDATION_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["cuota"], 300000)
        self.assertEqual(data["monto"], 7200000)
        self.assertEqual(data["plazo"], 24)

    def test_hu5_recommendation_lower_income(self):

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        payload = {
            "ingreso": 500000
        }

        response = requests.post(
            RECOMMENDATION_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["cuota"], 150000)
        self.assertEqual(data["monto"], 3600000)
        self.assertEqual(data["plazo"], 24)


if __name__ == "__main__":
    unittest.main()