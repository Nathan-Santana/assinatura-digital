from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Signature, VerificationLog
from .crypto_utils import generate_key_pair, sign_message, verify_signature, get_public_key, get_private_key
from django.db.models import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.db import transaction
import base64
import datetime
import traceback
import logging

logger = logging.getLogger(__name__)

def private_page(request):
    """
    Renderiza a página privada para cadastro e assinatura.
    """
    return render(request, 'private.html')

def public_verification_page(request):
    """
    Renderiza a página pública para verificação de assinaturas.
    """
    return render(request, 'public_verification.html')

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """
    Endpoint para cadastro de novo usuário.
    Gera um par de chaves RSA e armazena no banco de dados.
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')

        if not username:
            return JsonResponse({'error': 'Nome de usuário é obrigatório.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Nome de usuário já existe.'}, status=409)

        public_key_pem, private_key_pem = generate_key_pair()
        
        with transaction.atomic():
            user = User.objects.create(
                username=username,
                public_key=public_key_pem,
                private_key=private_key_pem
            )
            
            # Assina uma mensagem de boas-vindas para o usuário
            welcome_message = f"Bem-vindo, {username}! Sua conta foi criada com sucesso."
            signature_bytes = sign_message(welcome_message.encode('utf-8'), private_key_pem)

            return JsonResponse({
                'message': 'Usuário cadastrado com sucesso e chave gerada!',
                'username': user.username,
                'welcome_message': welcome_message,
                'signature': base64.b64encode(signature_bytes).decode('utf-8')
            }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Requisição JSON inválida.'}, status=400)
    except Exception as e:
        logger.error(f"Erro no registro: {e}")
        traceback.print_exc()
        return JsonResponse({'error': 'Ocorreu um erro interno. Tente novamente mais tarde.'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def sign(request):
    """
    Endpoint para assinar uma mensagem.
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        message = data.get('message')

        if not username or not message:
            return JsonResponse({'error': 'Nome de usuário e mensagem são obrigatórios.'}, status=400)

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

        private_key_pem = get_private_key(user)
        signature_bytes = sign_message(message.encode('utf-8'), private_key_pem)

        with transaction.atomic():
            signed_document = Signature.objects.create(
                signer=user,
                text=message,
                signature=base64.b64encode(signature_bytes).decode('utf-8'),
                timestamp=int(datetime.datetime.now().timestamp())
            )

            return JsonResponse({
                'message': 'Mensagem assinada com sucesso!',
                'signature_id': signed_document.id,
                'signature_b64': base64.b64encode(signature_bytes).decode('utf-8')
            }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Requisição JSON inválida.'}, status=400)
    except Exception as e:
        logger.error(f"Erro na assinatura: {e}")
        return JsonResponse({'error': f'Ocorreu um erro: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def verify(request):
    """
    Endpoint para verificar uma assinatura.
    """
    try:
        data = json.loads(request.body)
        
        signature_id = data.get('signature_id')
        original_text = data.get('original_text')
        signature_b64 = data.get('signature')

        if not signature_id and (not original_text or not signature_b64):
            return JsonResponse({
                'is_valid': False,
                'message': 'Por favor, forneça o ID da assinatura ou o texto e a assinatura para verificação.'
            }, status=400)

        try:
            if signature_id:
                signed_document = Signature.objects.get(id=signature_id)
                user = signed_document.signer
                original_text_from_db = signed_document.text
                signature_from_db = signed_document.signature
                public_key_pem = get_public_key(user)

                is_valid = verify_signature(original_text_from_db.encode('utf-8'), base64.b64decode(signature_from_db), public_key_pem)
                
                VerificationLog.objects.create(
                    is_valid=is_valid,
                    timestamp=int(datetime.datetime.now().timestamp()),
                    reason='Verificação por ID da assinatura.'
                )
                
                return JsonResponse({
                    'is_valid': is_valid,
                    'message': f"Assinatura {'VÁLIDA' if is_valid else 'INVÁLIDA'}.",
                    'signer': user.username,
                    'algorithm': 'SHA-256 + RSA',
                    'verification_time': datetime.datetime.fromtimestamp(signed_document.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                })
                
            elif original_text and signature_b64:
                # Caso de verificação offline
                signature_bytes = base64.b64decode(signature_b64)
                all_users = User.objects.all()
                is_valid = False
                signer_name = "Desconhecido"
                
                for user in all_users:
                    public_key_pem = get_public_key(user)
                    if verify_signature(original_text.encode('utf-8'), signature_bytes, public_key_pem):
                        is_valid = True
                        signer_name = user.username
                        break

                VerificationLog.objects.create(
                    is_valid=is_valid,
                    timestamp=int(datetime.datetime.now().timestamp()),
                    reason='Verificação offline.'
                )

                return JsonResponse({
                    'is_valid': is_valid,
                    'message': f"Assinatura {'VÁLIDA' if is_valid else 'INVÁLIDA'}.",
                    'signer': signer_name,
                    'algorithm': 'SHA-256 + RSA',
                    'verification_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        except ObjectDoesNotExist:
            VerificationLog.objects.create(
                is_valid=False,
                timestamp=int(datetime.datetime.now().timestamp()),
                reason='ID da assinatura não encontrado.'
            )
            return JsonResponse({
                'is_valid': False,
                'message': 'ID da assinatura não encontrado.'
            }, status=404)
        
    except json.JSONDecodeError:
        return JsonResponse({'is_valid': False, 'message': 'Requisição JSON inválida.'}, status=400)
    except Exception as e:
        logger.error(f"Erro na verificação: {e}")
        traceback.print_exc()
        return JsonResponse({'is_valid': False, 'message': f'Ocorreu um erro interno: {str(e)}'}, status=500)
