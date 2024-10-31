class APIResponse:
    def __init__(self, success: bool, data=None, error_message: str = None):
        self.success = success
        self.data = data
        self.error_message = error_message

    def __repr__(self):
        return f"APIResponse(success={self.success}, data={self.data}, error_message={self.error_message})"