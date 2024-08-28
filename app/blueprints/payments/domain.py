class PayPalPayment:
    def __init__(self, items, currency="USD", description="PayPalPayment transaction"):
        self.intent = "CAPTURE"
        self.items = items
        self.total = calculate_total(self.items)
        self.currency = currency
        self.description = description

    def to_paypal_dict(self):
        # PayPal Checkout SDK 결제를 위한 데이터 구조로 변환
        return {
            "intent": self.intent,
            "purchase_units": [{
                "amount": {
                    "currency_code": self.currency,
                    "value": self.total
                },
                "description": self.description
            }],
            "application_context": {
                "return_url": "http://localhost:5000/payment/success",
                "cancel_url": "http://localhost:5000/payment/cancel"
            }
        }

class TossPayment:
    def __init__(self, items, order_id, customer_name, currency="KRW", description="Payment transaction"):
        self.order_id = order_id 
        self.customer_name = customer_name 
        
        self.items = items
        self.total = calculate_total(self.items)
        self.currency = currency
        self.description = description
        
    def to_toss_dict(self):
        # TossPayments 결제를 위한 데이터 구조로 변환
        return {
            "amount": int(float(self.total)),
            "orderId": self.order_id,
            "orderName": self.description,
            "customerName": self.customer_name,
        }

def calculate_total(items):
    # 아이템의 가격과 수량을 기반으로 총액 계산
    return str(sum(float(item['price']) * int(item['quantity']) for item in items))
