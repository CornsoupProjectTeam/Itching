#payment_authentication_domain.py

from app.repositories.payment_authentication_repository import PaymentRepository
from app.repositories.login_repository import LoginRepository

class AuthenticationDomain:

    @staticmethod
    def verify_card_name(user_name):
        return PaymentRepository.verify_card_name(user_name)

    @staticmethod
    def verify_user_name(user_name):
        payment = PaymentRepository.find_by_user_name(user_name)
        return payment is not None

    @staticmethod
    def verify_user_id(client_user_id):
        payment = PaymentRepository.find_by_client_user_id(client_user_id)
        return payment is not None

    @staticmethod
    def verify_password(client_user_id, password):
        return LoginRepository.verify_password(client_user_id, password)
    
    @staticmethod
    def insert_user_name(chat_room_id, user_name):
        PaymentRepository.insert_user_name(chat_room_id, user_name)

   