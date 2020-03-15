def format_enum_for_display(enum):
    if "." not in enum:
        return enum
    return enum.split(".")[1].lower()
