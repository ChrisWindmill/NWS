from NetworkServer import Server
from Book import Book
from Page import Page
from Option import Option
import time


class ChooseYourOwnServer:
    def __init__(self, host="127.0.0.1", port=50000):
        self.server = Server(host, port)

        # Variables dealing with state management and state functionality
        self.book = Book()
        self.running = True

    def constructBook(self, title=None):
        if not title:
            page1 = Page(1, "The first page")
            page2 = Page(2, "The second page")
            page3 = Page(3, "The Third page")

            page1.add_option(Option(2, "Move to the second page"))
            page1.add_option(Option(3, "Move to the third page"))
            page2.add_option(Option(3, "Move to the third page"))
            page3.add_option(Option(1, "Move to the first page"))

            self.book.add_page(page1)
            self.book.add_page(page2)
            self.book.add_page(page3)
        else:
            page1 = Page(1, "The first page")
            page2 = Page(2, "The second page")
            page3 = Page(3, "The Third page")

            page1.add_option(Option(2, "Move to the second page"))
            page1.add_option(Option(3, "Move to the third page"))
            page2.add_option(Option(3, "Move to the third page"))
            page3.add_option(Option(1, "Move to the first page"))

            self.book.add_page(page1)
            self.book.add_page(page2)
            self.book.add_page(page3)

    def process(self):
        self.server.process()
        self.constructBook()

        # Termination condition to handle the program shutting down

        while not self.server.hasClient():
            time.sleep(1)

        while self.running:
            # only attempt to process a message if there is a message in the incoming message buffer
            self.server.pushMessage(self.book.read_current_page())
            validChoice = False

            while not validChoice:
                message = self.server.getMessage()
                if message:
                    if message == "Quit":
                        message = "Acknowledge quitting"
                        self.running = False
                        validChoice = True

                    try:
                        value = int(message)
                        if self.book.option_exists(value):
                            validChoice = True
                            message = self.book.action_option(str(value))
                    except ValueError:
                        message = "Error, input must be an integer"
                    self.server.pushMessage(message)

        self.server.quit()


if __name__=="__main__":
    server = ChooseYourOwnServer("127.0.0.1", 50001)
    server.process()