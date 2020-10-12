import sys
import logging
import traceback
from app_content.models import Content, Category
from django.db.models import Q
from django.db.models import F
from .utils import format_content
logger = logging.getLogger(__name__)

class SearchContent:
    def get_all_search_result(self, search_string, user, is_admin):
        if search_string:
            if is_admin:
                all_content = Content.objects.filter(Q(title__icontains=search_string)|Q(body__icontains=search_string)|Q(summary__icontains=search_string)|Q(category__name__icontains=search_string)).values("id", "title", "body", "summary", "document", category_name=F("category__name"))
            else:
                all_content = Content.objects.filter(Q(title__icontains=search_string)|Q(body__icontains=search_string)|Q(summary__icontains=search_string)|Q(category__name__icontains=search_string), user__email=user).values("id", "title", "body", "summary", "document", category_name=F("category__name"))
            res_dict = format_content(all_content)
            return res_dict
        return {}