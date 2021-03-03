class DatabaseException(Exception):
    
    
    def __init__(self, error_message, reason):
        self.error_message = error_message
        self.reason = reason
        super().__init__(self.reason)
        
    
    def __str__(self):
        return f"error {self.error_message} -> {self.reason}"