import uuid

def generate_chat_room_id():
    return f"CH{uuid.uuid4()}"

def generate_quotation_id():
    return f"QUO{uuid.uuid4()}"

def generate_favorite_list_id():
    return f"FAV{uuid.uuid4()}"

def generate_faq_id():
    return f"FAQ{uuid.uuid4()}"

def generate_post_id():
    return f"PST{uuid.uuid4()}"

def generate_public_profile_id():
    return f"PP{uuid.uuid4()}"

def generate_project_id():
    return f"PROJ{uuid.uuid4()}"

def generate_client_post_id():
    return f"CP{uuid.uuid4()}"