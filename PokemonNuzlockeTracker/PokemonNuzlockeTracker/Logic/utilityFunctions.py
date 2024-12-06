from kivymd.uix.textfield import MDTextField

def checkStringEmpty(text: str) -> bool:
    """function that returns True when the given text consists of only whitespace or is empty"""
    return text.isspace() or text == ""

def validateTextInput(text: str) -> str | None:
    """function that validates text, returns None or the supplied Text"""
    return text if not checkStringEmpty(text) else None

def validateField(field: MDTextField) -> bool:
    StringEmpty = checkStringEmpty(field.text)
    if StringEmpty:
        field.error = True
    else:
       field.error = False      
    return not StringEmpty

def validateFields(fields: list[MDTextField]) -> bool:
    """returnes False if one of the fields is empty"""
    return all([validateField(field) for field in fields])
