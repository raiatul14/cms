import sys
import logging
import traceback
from app_content.models import Content, Category
from django.db import transaction
from django.db.models import F
from .utils import format_content

logger = logging.getLogger(__name__)


class ContentCreateRetrieve:

    def validate_all_mandatory_fields(self, error_messages, data) -> list:
        """
        validate all the mandatory fields if present or not
        Mandatory Fields:
        * title
        * body
        * summary
        * document
        * categories
        """
        if not data.get("title"):
            error_messages.append("Content must have a title")
        if not data.get("body"):
            error_messages.append("Content must have a body")
        if not data.get("summary"):
            error_messages.append("Content must have a summary")
        if not data.getlist("categories"):
            error_messages.append("Content must have a categories")

        return error_messages
    
    def validate_field_values_length(self, error_message, data):
        """
        Validate length of the fields
        """

        if len(data["title"]) > 30:
            error_message.append("Title length should be less than or equal to 30")
        if len(data["body"]) > 300:
            error_message.append("Body length should be less than or equal to 300")
        if len(data["summary"]) > 60:
            error_message.append("Summary length should be less than or equal to 300")
        for category in data.getlist("categories"):
            if len(category) > 100:
                error_message.append("Category length should be less than or equal to 100")
                break
        
        return error_message

    def validate_file(self, uploaded_file, error_message):
        """
        validate file, form.data should have document field and document extension should be pdf
        """
        if not uploaded_file.get("document"):
            error_message.append("PDF document field cannot be empty")
        if uploaded_file.get("document"):
            if not uploaded_file.get("document").name.endswith(".pdf"):
                error_message.append("Only pdf document upload is allowed")
        return error_message

    @transaction.atomic()
    def create_content(self, data, user, uploaded_file) -> dict:
        """
        Creates Content and returns status_code with error/success messages
        * 400 is returned if all required fields are not passed in the request
        * 200 is returned if the content is created successfully
        * 500, if an unhandled exception occurs
        """
        try:
            error_messages = []
            error_message_template = ""

            error_messages = self.validate_all_mandatory_fields(error_messages, data)
            if error_messages:
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            error_messages = self.validate_file(uploaded_file, error_messages)
            if error_messages:
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            error_messages = self.validate_field_values_length(error_messages, data)
            if error_messages:
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            category_obj = Category()
            content_obj = Content()
            content_obj.title = data.get("title")
            content_obj.body = data.get("body")
            content_obj.summary = data.get("summary")
            content_obj.user = user
            content_obj.document = uploaded_file.get("document")
            content_obj.save()
            for category in data.getlist("categories"):
                created_obj, created = Category.objects.get_or_create(name = str(category).lower())
                content_obj.category.add(created_obj)
            return {"message":"Content Created Successfully", "status_code":200}
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return {"error":"Something went wrong!", "status_code":500}


    def get_all_content(self, user, is_admin):
        """
        Return dict with for author as well as admin. If admin, then return all contents.
        If author is user then only his content is fetched.
        """
        if is_admin:
            all_content = Content.objects.all().values('id', 'title', 'summary', 'body', 'document', category_name=F('category__name'))
        else:
            all_content = Content.objects.filter(user__email=user).values('id', 'title', 'summary', 'body', 'document', category_name=F('category__name'))
        res_dict = format_content(list(all_content))
        return res_dict



