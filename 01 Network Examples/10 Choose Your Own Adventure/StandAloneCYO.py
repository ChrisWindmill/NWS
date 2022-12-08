from Book import Book
from Page import Page
from Option import Option
import time

book = Book()
page1 = Page(1,"The first page")
page2 = Page(2, "The second page")
page3 = Page(3, "The Third page")

page1.add_option(Option(2, "Move to the second page"))
page1.add_option(Option(3, "Move to the third page"))
page2.add_option(Option(3, "Move to the third page"))
page3.add_option(Option(1, "Move to the first page"))

book.add_page(page1)
book.add_page(page2)
book.add_page(page3)

while True:
    print(book.read_current_page())
    validChoice = False

    while not validChoice:
        choice = input("Please choose an option")
        if book.option_exists(int(choice)):
            validChoice = True

    response = book.action_option(choice)
    print(response)