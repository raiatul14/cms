from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import sys
import logging
import traceback

logger = logging.getLogger(__name__)

class LoginService:

    def authenticate_user(self, email, password) -> dict:
        """
        Authenticates and returns status_code with error messages/token
        * 400 is returned if email or password or both the fields are not passed in the request
        * 404, if the credentials provided does not match in the database
        * 500, if an unhandled exception occurs 
        """
        try:
            if email is None or password is None:
                return {'error': 'Please provide both email and password', "status_code":400}
            #Returns User object if found
            user = authenticate(email=email, password=password)
            if not user:
                return {"error":"Invalid Credentials", "status_code":404}
            token, _ = Token.objects.get_or_create(user=user)
            return {"token":token.key, "status_code":200}
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return {"error":"Something went wrong!", "status_code":500}

