from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class MiPerfilViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="juan",
            email="juan@example.com",
            password="12345",
            es_alumno=True,
            es_profesor=False
        )

    def test_mi_perfil_requiere_login(self):
        url = reverse("mi_perfil")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_mi_perfil_muestra_datos(self):
        self.client.login(username="juan", password="12345")

        url = reverse("mi_perfil")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tareas/mi_perfil.html")

        html = response.content.decode()

        self.assertIn("Mi perfil", html)
        self.assertIn("juan", html)
        self.assertIn("juan@example.com", html)
