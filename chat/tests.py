
from django.test import TestCase, Client
from . import nlp
from .models import Conversa
from django.urls import reverse

class NLPTests(TestCase):
	def test_obter_hora(self):
		hora = nlp.obter_hora()
		self.assertIn("Agora são", hora)

	def test_buscar_wikipedia(self):
		resultado = nlp.buscar_wikipedia("Python (linguagem de programação)")
		self.assertTrue(resultado is None or isinstance(resultado, str))

	def test_calcular(self):
		self.assertEqual(nlp.calcular("2+2"), 4)
		self.assertEqual(nlp.calcular("2*3"), 6)
		self.assertIsNone(nlp.calcular("2/0"))

	def test_responder_hora(self):
		resposta = nlp.responder("Que horas são?", [])
		self.assertIn("Agora são", resposta)

	def test_responder_nome(self):
		historico = [type('obj', (object,), {'mensagem': 'Meu nome é Ana'})()]
		resposta = nlp.responder("qual meu nome", historico)
		self.assertIn("Seu nome é ana", resposta)

from django.contrib.auth.models import User

class ChatViewTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass')

	def test_home_view_requires_login(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 302)  # Redireciona para login

	def test_home_view_authenticated(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Chatbot")

	def test_chat_api_requires_login(self):
		response = self.client.post(reverse('chat_api'), data='{"message": "oi"}', content_type='application/json')
		self.assertEqual(response.status_code, 302)

	def test_chat_api_authenticated(self):
		self.client.login(username='testuser', password='testpass')
		response = self.client.post(reverse('chat_api'), data='{"message": "oi"}', content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertIn('reply', response.json())
		# Verifica histórico personalizado
		Conversa.objects.create(usuario='testuser', mensagem='Meu nome é Teste', resposta='Prazer, Teste!')
		response2 = self.client.post(reverse('chat_api'), data='{"message": "qual meu nome"}', content_type='application/json')
		self.assertIn('Seu nome é teste', response2.json()['reply'])
