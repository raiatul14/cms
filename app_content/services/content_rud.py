import sys
import logging
import traceback
from app_content.models import Content, Category
from django.db import transaction
from django.db.models import F
from .utils import format_content

logger = logging.getLogger(__name__)

class ContentRUD:

    def get_content_by_id(self, content_id, user, is_admin):
        # try:
            
        # except Exception as e:
        #     print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
        #     logger.exception(traceback.print_exc())
        # return {"error":"Something went wrong!", "status_code":500}
        if is_admin:
            content_dict = Content.objects.filter(id=content_id).values("id", "title", "summary", "body", "document", category_name=F("category__name"))
        else:
            content_dict = Content.objects.filter(id=content_id, user__email=user).values("id", "title", "summary", "body", "document", category_name=F("category__name"))
        res_dict = format_content(content_dict)
        return res_dict

    def delete_content_by_id(self, content_id, user, is_admin):
        if is_admin:
            total_deletion, objects_deleted = Content.objects.filter(id=content_id).delete()
        else:
            total_deletion, objects_deleted = Content.objects.filter(id=content_id, user__email=user).delete()
        return total_deletion

    def edit_content_by_id(self, content_id, data, upload_file, user, is_admin):
        if is_admin:
            content_obj = Content.objects.filter(id=content_id).first()
        else:
            content_obj = Content.objects.filter(id=content_id, user__email=user).first()
        if content_obj:
            error_messages = []
            if upload_file.get("document"):
                if upload_file.get("document").name.endswith('.pdf'):
                    content_obj.document = upload_file.get("document")
                else:
                    error_messages.append("Document should be pdf format")
            if data.get("title"):
                if len(data.get("title")) <= 30:
                    content_obj.title = data.get("title")
                else:
                    error_messages.append("Title length should be less than or equal to 30")
            if data.get("body"):
                if len(data.get("body")) <= 300:
                    content_obj.body = data.get("body")
                else:
                    error_messages.append("Body length should be less than or equal to 300")
            if data.get("summary"):
                if len(data.get("summary")) <= 60:
                    content_obj.summary = data.get("summary")
                else:
                    error_messages.append("Summary length should be less than or equal to 60")
            content_obj.save()
            if data.getlist("categories"):
                for category in data.getlist("categories"):
                    created_obj, created = Category.objects.get_or_create(name = str(category).lower())
                    content_obj.category.add(created_obj)
            if error_messages:
                print(error_messages)
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            return {"message":"Record edited successfully", "status_code":200}
        return {"error":"No record found/Unauthorized access for given id", "status_code":404}