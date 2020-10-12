from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from app_users.services import LoginService
import sys
import logging
import traceback

logger = logging.getLogger(__name__)


class LoginAPI(APIView):
    """
    View to login user in the system.

    * Requires email and password.
    """
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """
        Authenticates and returns token to user
        """
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            login_ser_obj = LoginService()
            status_dict = login_ser_obj.authenticate_user(email, password)
            if status_dict.get("status_code") == 400:
                return Response(status_dict, status=HTTP_400_BAD_REQUEST)
            elif status_dict.get("status_code") == 404:
                return Response(status_dict, status=HTTP_404_NOT_FOUND)
            elif status_dict.get("status_code") == 200:
                return Response(status_dict, status=HTTP_200_OK)
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return Response({'error': 'Something went wrong!', "status_code":500}, status=HTTP_500_INTERNAL_SERVER_ERROR)