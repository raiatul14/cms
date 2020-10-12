from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from app_users.services import RegisterService
import sys
import logging
import traceback

logger = logging.getLogger(__name__)


class RegisterAPI(APIView):
    """
    View to register user in the system.
    Required Fields
    * email
    * password
    * full_name
    * phone
    * pincode
    Optional Fields
    * address
    * city
    * state
    * country
    Request:
    {
        "email":"test@user.com",
        "password":"123",
        "full_name": "FDFD FDS",
        "phone": 3248948951,
        "pincode": 548485
    }
    """
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """
        Registers the user
        """
        try:
            data = request.data
            register_ser_obj = RegisterService()
            status_dict = register_ser_obj.register(data)
            if status_dict.get("status_code") == 400:
                return Response(status_dict, status=HTTP_400_BAD_REQUEST)
            elif status_dict.get("status_code") == 409:
                return Response(status_dict, status=HTTP_409_CONFLICT)
            elif status_dict.get("status_code") == 200:
                return Response(status_dict, status=HTTP_200_OK)
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return Response({'error': 'Something went wrong!', "status_code":500}, status=HTTP_500_INTERNAL_SERVER_ERROR)