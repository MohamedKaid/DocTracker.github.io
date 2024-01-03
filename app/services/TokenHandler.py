from flask import current_app, flash
from itsdangerous import URLSafeTimedSerializer

"""      Handle tokenization for recovery link emailed to user      """

class TokenHandler:
    
    # Email to token
    def generateToken(email):
        secret_key = current_app.config['SECRET_KEY']
        serializer = URLSafeTimedSerializer(secret_key)

        return serializer.dumps(email)
    
    # Token to email
    def retrieveEmail(token):
        secret_key = current_app.config['SECRET_KEY']

        try:
            serializer = URLSafeTimedSerializer(secret_key)
            email = serializer.loads(token, max_age=3600)

            return email
        except:
            flash('The reset link is invalid or has expired')