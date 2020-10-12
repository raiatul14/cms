from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
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
from app_content.services import SearchContent
import sys
import logging
import traceback
from app_content.permissions import IsOwner
from app_content.models import *

logger = logging.getLogger(__name__)


class SearchContentAPI(APIView):
    """
    search contents
    """

    def get(self, request, format=None):
        try:
            search_string = request.GET.get("q")
            user = request.user
            is_admin = request.user.is_staff
            print("search is", search_string)
            search_content_obj = SearchContent()
            resp_dict = search_content_obj.get_all_search_result(search_string, user, is_admin)
            if resp_dict:
                return Response(resp_dict, status=HTTP_200_OK)
            else:
                return Response({"message":"No data found"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return Response({'error': 'Something went wrong!', "status_code":500}, status=HTTP_500_INTERNAL_SERVER_ERROR)