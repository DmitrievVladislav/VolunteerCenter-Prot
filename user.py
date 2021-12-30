class User:
    def __init__(self, id, user_lvl, name, surname, email, phone, is_ready):
        self.id = id
        self.user_lvl = user_lvl
        self.gate = None
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.is_ready = is_ready;
        self.in_process = False;
        self.connected_id = 0;