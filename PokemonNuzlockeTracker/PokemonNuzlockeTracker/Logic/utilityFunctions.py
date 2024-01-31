


def checkString(text: str) -> bool:
    """function that returns True when the given text consists of only whitespace or is empty"""
    return text.isspace() or text == ""

def validateTextInput(text: str) -> str | None:
    """function that validates text, returns None or the supplied TextInput is the input is not empty"""
    return text if not checkString(text) else None