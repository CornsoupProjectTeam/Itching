# app/routes/quotation.py

from flask import Blueprint, render_template, request
from app.services.chat_room_quotation_service import ChatRoomQuotationService
from datetime import datetime

quotation_bp = Blueprint('quotation', __name__)

class QuotationHandler:
    def __init__(self, form):
        self.form = form
        self.data = {}

    def convert_to_datetime(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

    def validate_data(self):
        required_fields = ['estimate_id', 'midterm_check', 'final_deadline', 'estimate', 'number_of_drafts', 'revision_count']
        for field in required_fields:
            if not self.form.get(field):
                raise ValueError(f"{field} is required.")
        return True

    def prepare_data(self):
        self.data = {
            "quotation_id": self.form.get('estimate_id'),
            "chatroom_id": self.form.get('estimate_id'),
            "participants": self.form.getlist('participants'),
            "quotation_status": self.form.get('estimate_status'),
            "requirements_mapping": [
                {
                    "sequence": 1,
                    "requirement": self.form.get('requirement1')
                },
                {
                    "sequence": 2,
                    "requirement": self.form.get('requirement2')
                }
            ],
            "quotation": float(self.form.get('estimate')),
            "number_of_drafts": int(self.form.get('number_of_drafts')),
            "notification_dates": {
                "midterm_check": self.convert_to_datetime(self.form.get('midterm_check')),
                "final_deadline": self.convert_to_datetime(self.form.get('final_deadline'))
            },
            "revision_count": int(self.form.get('revision_count')),
            "additional_revision_purchase_available": self.form.get('additional_revision_purchase_available') == 'on',
            "commercial_use_allowed": self.form.get('commercial_use_allowed') == 'on',
            "high_resolution_file_available": self.form.get('high_resolution_file_available') == 'on',
            "delivery_route": self.form.get('delivery_method')
        }

    def create_quotation(self):
        self.validate_data()
        self.prepare_data()
        ChatRoomQuotationService.create_quotation(self.data)

@quotation_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            quotation_handler = QuotationHandler(request.form)
            quotation_handler.create_quotation()

            return render_template('success.html', data=quotation_handler.data)

        except ValueError as e:
            return f"Error: {str(e)}", 400
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500

    return render_template('index.html')


