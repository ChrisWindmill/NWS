class Page:
    def __init__(self, id=-1, desc="A blank page"):
        self.id = id
        self.description = desc
        self.options = []

    def add_option(self, option):
        self.options.append(option)

    def option_exists(self, id):
       if int(id) <= len(self.options):
           return True

    def action_option(self, id):
        choice = int(id)
        if choice <= len(self.options):
            return self.options[choice-1].target, self.options[choice-1].description
