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
        print("document", uploaded_file.get("document"))
        if not uploaded_file.get("document"):
            print("over here")
            error_message.append("PDF document field cannot be empty")
        if uploaded_file.get("document"):
            print(uploaded_file.get("document").name)
            if not uploaded_file.get("document").name.endswith(".pdf"):
                error_message.append("Only pdf document upload is allowed")
        return error_message

    @transaction.atomic()
    def create_content(self, data, user, uploaded_file) -> dict:
        """
        Registers and returns status_code with error/success messages
        * 400 is returned if all required fields are not passed in the request
        * 409 is returned if email already exists
        * 200 is returned if the user is created successfully
        * 500, if an unhandled exception occurs
        #TODO add category field validation 
        """
        try:
            error_messages = []
            error_message_template = ""

            error_messages = self.validate_all_mandatory_fields(error_messages, data)
            if error_messages:
                print(error_messages)
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            error_messages = self.validate_file(uploaded_file, error_messages)
            print("error_messages are", error_messages)
            if error_messages:
                print(error_messages)
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            error_messages = self.validate_field_values_length(error_messages, data)
            if error_messages:
                print(error_messages)
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
        print("is_admin", is_admin)
        if is_admin:
            all_content = Content.objects.all().values('id', 'title', 'summary', 'body', 'document', category_name=F('category__name'))
        else:
            print("user is", user)
            all_content = Content.objects.filter(user__email=user).values('id', 'title', 'summary', 'body', 'document', category_name=F('category__name'))
        #TODO add category_name for many to many fields
        # for content in all_content:
        #     if content.get("categories") != None:
        #         content.get("categories").append(content.)
        # print(all_content)
        res_dict = format_content(list(all_content))
        print('sdfji',res_dict)
        return res_dict

    # def format_content(self, content_list):
    #     dict_to_return = {}
    #     for content in content_list:
    #         if dict_to_return.get(content.get("id")):
    #             # print("fsdiidsij",dict_to_return.get(content.get("id"))["categories"], content.get("category_name"))
    #             # dict_to_return.get(content.get("id"))["categories"] = dict_to_return.get(content.get("id")).get("categories").append(content.get("category_name"))
    #             prev_list_values = dict_to_return.get(content.get("id"))["categories"]
    #             prev_list_values.append(content.get("category_name"))
    #             # print("kjdf", prev_list_values)
    #             dict_to_return.get(content.get("id"))["categories"] = prev_list_values
    #             # print(dict_to_return)
    #         else:
    #             temp_dict = {}
    #             temp_dict["id"] = content.get("id")
    #             temp_dict["title"] = content.get("title")
    #             temp_dict["summary"] = content.get("summary")
    #             temp_dict["body"] = content.get("body")
    #             temp_dict["document"] = content.get("document")
    #             temp_dict["categories"] = [content.get("category_name")]
    #             dict_to_return[content.get("id")] = temp_dict
    #     print(dict_to_return)
    #     return dict_to_return



