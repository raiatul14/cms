from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_404_NOT_FOUND
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from app_content.services import ContentRUD
import sys
import logging
import traceback
from app_content.permissions import IsOwner


logger = logging.getLogger(__name__)


class ContentRUDAPI(APIView):
    """
    create and view all the contents
    """
    # permission_classes = (permissions.IsAdminUser|IsOwner,)
    permission_classes = [IsOwner]

    def put(self, request, content_id, format=None):
        """
        Registers the content
        """
        try:
            data = request.data
            user = request.user
            is_admin = request.user.is_staff
            content_ser_obj = ContentRUD()
            status_dict = content_ser_obj.edit_content_by_id(content_id, data, request.FILES, user, is_admin)
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

    def get(self, request, content_id, format=None):
        try:
            content_ser_obj = ContentRUD()
            user = request.user
            is_admin = request.user.is_staff
            resp_dict = content_ser_obj.get_content_by_id(content_id, user, is_admin)
            if resp_dict:
                return Response(resp_dict, status=HTTP_200_OK)
            else:
                return Response({"message":"Unauthorized/No data found"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return Response({'error': 'Something went wrong!', "status_code":500}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, content_id, format=None):
        try:
            content_ser_obj = ContentRUD()
            user = request.user
            is_admin = request.user.is_staff
            deleted_num = content_ser_obj.delete_content_by_id(content_id, user, is_admin)
            if deleted_num > 0:
                return Response({"message":"Deleted successfully!"}, status=HTTP_200_OK)
            else:
                return Response({"message":"Unauthorized/Incorrect ID requested"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return Response({'error': 'Something went wrong!', "status_code":500}, status=HTTP_500_INTERNAL_SERVER_ERROR)