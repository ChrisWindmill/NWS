class Book:
    def __init__(self):
        self.start = None
        self.currentPage = None
        self.pages = []
        self.inventory = []

    def page_exists(self, id):
        for page in self.pages:
            if page.id == id:
                return True
        return False

    def option_exists(self, id):
        return self.currentPage.option_exists(id)

    def add_page(self, page):
        self.pages.append(page)
        if self.currentPage == None:
            self.currentPage = page

    def action_option(self, id):
        nextPage, response = self.currentPage.action_option(id)
        self.set_page(nextPage)
        return response

    def set_page(self, id):
        for page in self.pages:
            if page.id == id:
                self.currentPage = page

    def read_current_page(self):
        counter = 1
        optionList = ""
        for option in self.currentPage.options:
            optionList += f"[{counter}] {option.description}\n"
            counter = counter + 1
        message = f"Page {self.currentPage.id}\n" + self.currentPage.description + f"Options\n{optionList}"
        return message

    def read_page(self, id):
        message = ""
        for page in self.pages:
            if page.id == id:
                counter = 1
                optionList = ""
                for option in page.options:
                    optionList += f"[{counter}] {option.description}\n"
                    counter = counter + 1

                message = f"Page {page.id}\n" + page.description + f"\n\nOptions\n{optionList}"
        return message
