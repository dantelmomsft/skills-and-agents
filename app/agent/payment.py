# Payment Agent

class Agent:
    def __init__(self, name: str):
        self.name = name

    def submit_payment(self, payment_request):
        """
        Process a payment submission.
        
        Args:
            payment_request: dict with keys 'id', 'amount', 'date'
        
        Returns:
            dict with status and transaction details
        """
        if not all(k in payment_request for k in ['id', 'amount', 'date']):
            return {"status": "failed", "error": "Missing required fields"}
        
        return {
            "status": "success",
            "transaction_id": payment_request['id'],
            "amount": payment_request['amount'],
            "date": payment_request['date'],
            "message": f"Payment of ${payment_request['amount']} submitted on {payment_request['date']}"
        }

    def act(self, input_data):
        """Payment agent logic."""
        if isinstance(input_data, dict) and 'id' in input_data:
            return self.submit_payment(input_data)
        return f"Agent {self.name} received: {input_data}"
