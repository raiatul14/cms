def format_content(content_list):
    """To combine and merge different objects with different category name but same content id"""
    dict_to_return = {}
    for content in content_list:
        if dict_to_return.get(content.get("id")):
            prev_list_values = dict_to_return.get(content.get("id"))["categories"]
            prev_list_values.append(content.get("category_name"))
            dict_to_return.get(content.get("id"))["categories"] = prev_list_values
        else:
            temp_dict = {}
            temp_dict["id"] = content.get("id")
            temp_dict["title"] = content.get("title")
            temp_dict["summary"] = content.get("summary")
            temp_dict["body"] = content.get("body")
            temp_dict["document"] = "http://127.0.0.1:8000/media/"+content.get("document")
            temp_dict["categories"] = [content.get("category_name")]
            dict_to_return[content.get("id")] = temp_dict
    return dict_to_return