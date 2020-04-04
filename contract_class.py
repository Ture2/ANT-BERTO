class Contract:
    def __init__(self, id):
        self.id = id
        self.name = 'contract_' + str(id)
        self.extensions = []

    def get_extensions(self):
        return self.extensions

    def set_extensions(self, extensions):
        self.extensions = extensions

    def set_content_by_extension(self, ext, content):
        self.content[ext] = content
        self.extensions.push(ext)

    def get_content_by_extension(self, ext):
        return self.content.get(ext)

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

    def set_content(self, content):
        self.content = content

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_id(self):
        return self.id

