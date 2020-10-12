import sys
import logging
import traceback
from django.contrib.auth import get_user_model # If used custom user model

logger = logging.getLogger(__name__)

UserModel = get_user_model()

class RegisterService:

    def validate_all_mandatory_fields(self, error_messages, data) -> list:
        """
        validate all the mandatory fields if present or not
        Mandatory Fields:
        * email
        * password
        * full_name
        * phone
        * pincode
        """
        if not data.get("email"):
            error_message.append("User must have an email")
        if not data.get("password"):
            error_messages.append("User must have a password")
        if not data.get("full_name"):
            error_messages.append("User must have a full_name")
        if not data.get("phone"):
            error_messages.append("User must have a phone number")
        if not data.get("pincode"):
            error_messages.append("User must have a pincode number")

        return error_messages
    
    def validate_field_values_length(self, error_message, data):
        """
        Validate length of the fields
        """

        if len(data["email"]) > 30:
            error_message.append("Email length should be less than or equal to 30")
        if len(data["password"]) > 300:
            error_message.append("Password length should be less than or equal to 300")
        if str(data["pincode"]).isdigit() == False or len(str(data["pincode"])) != 6:
            error_message.append("Pincode length should be equal to 6 and should be numeric.")
        if len(str(data["phone"])) != 10 or str(data["phone"]).isdigit() == False:
            print("over here")
            error_message.append("Phone length should be equal to 10 and should be numeric.")
        if "address" in data.keys():
            if len(data["address"]) > 160:
                error_message.append("Address length should be less than or equal to 160")
        if "city" in data.keys():
            if len(data["city"]) > 50:
                error_message.append("City length should be less than or equal to 50")
        if "state" in data.keys():
            if len(data["state"]) > 50:
                error_message.append("State length should be less than or equal to 50")
        if "country" in data.keys():
            if len(data["country"]) > 50:
                error_message.append("Country length should be less than or equal to 50")
        full_name = data["full_name"].split()
        if len(full_name) >= 2:
            if len(full_name[0]) > 20:
                error_message.append("First Name length should be less than or equal to 20")
            if len(full_name[1]) > 15 or len(full_name[1]) == 0:
                error_message.append("Last Name length should be less than or equal to 15 and should not be empty")
        if len(full_name) == 1:
            error_message.append("Last Name length should be less than or equal to 15")
        
        
        return error_message

    def validate_password(self, password, error_message):
        if len(password) >= 8:
            upp_count = 0
            low_count = 0
            for char in password:
                if upp_count == 1 and low_count == 1:
                    return error_message
                if char.isupper():
                    upp_count += 1
                if char.islower():
                    low_count += 1
        error_message.append("Password should have minimumn length of 8 and 1 upper case character and 1 lower case character")

    def register(self, data) -> dict:
        """
        Registers and returns status_code with error/success messages
        * 400 is returned if all required fields are not passed in the request
        * 409 is returned if email already exists
        * 200 is returned if the user is created successfully
        * 500, if an unhandled exception occurs 
        """
        try:
            error_messages = []
            error_message_template = ""
            error_messages = self.validate_all_mandatory_fields(error_messages, data)
            if error_messages:
                print(error_messages)
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            error_messages = self.validate_field_values_length(error_messages, data)
            if error_messages:
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}
            error_messages = self.validate_password(data["password"], error_messages)
            if error_messages:
                error_message_template = ', '.join(error_messages)
                return {"error":error_message_template, "status_code":400}

            check_user_exist = UserModel.objects.filter(email=data["email"])

            if check_user_exist:
                return {"error":"Email address already exists.", "status_code":409}
            first_name, last_name = data["full_name"].split()
            user = UserModel()
            user.email = data.get("email")
            user.first_name = first_name
            user.last_name = last_name
            user.phone = int(data.get("phone"))
            user.address = data.get("address")
            user.city = data.get("city")
            user.state = data.get("state")
            user.country = data.get("country")
            user.pincode = int(data.get("pincode"))
            user.set_password(data.get("password"))  # change password to hash
            user.admin = False
            user.staff = False
            user.active = True
            user.save()
            return {"message":"User Created Successfully", "status_code":200}
        except Exception as e:
            print("Unhandled Exception occured at "+__file__+" on line number {} raised Exception is -> ".format(sys.exc_info()[2].tb_lineno), e)
            logger.exception(traceback.print_exc())
        return {"error":"Something went wrong!", "status_code":500}

