
from django.shortcuts import render
from django.http import JsonResponse
from .nlp import responder
from .models import Conversa
import json
import logging

logger = logging.getLogger(__name__)


def home(request):
    logger.info(f"Acesso à home.")
    return render(request, 'chat/index.html')


def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")
            usuario = request.user.username if request.user.is_authenticated else "anon"

          
            historico = Conversa.objects.filter(usuario=usuario).order_by("-id")[:5]

    
            reply = responder(message, historico)


            Conversa.objects.create(
                usuario=usuario,
                mensagem=message,
                resposta=reply
            )

            logger.info(f"Usuário {usuario} enviou mensagem: {message}")
            return JsonResponse({"reply": reply})
        except Exception as e:
            logger.error(f"Erro no chat_api: {e}")
            return JsonResponse({"reply": "Erro interno no servidor."}, status=500)
