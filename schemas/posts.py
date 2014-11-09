

post_multiple = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
            "body": {"type": "string"},
            "email": {"type": "string"}
        }
    }
}


post_single = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "email": {"type": "string"}
    }
}