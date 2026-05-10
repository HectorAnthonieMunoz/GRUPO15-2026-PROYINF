import unittest
import requests
import random

AUTH_URL = "http://127.0.0.1:4001"
RECOMMENDATION_URL = "http://127.0.0.1:3002/api/recommendation"


class TestRecommendation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Iniciando pruebas de recommendation")

        random_num = random.randint(1, 100000)

        cls.username = f"user_reco_{random_num}"
        cls.password = "123456"
        cls.email = f"user_reco_{random_num}@test.com"

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
        print("Finalizando pruebas de recommendation")

    def test_recommendation_success(self):
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

    def test_recommendation_without_token(self):
        payload = {
            "ingreso": 1000000
        }

        response = requests.post(
            RECOMMENDATION_URL,
            json=payload,
            timeout=10
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn("Usuario no autenticado", response.text)


if __name__ == "__main__":
    unittest.main()