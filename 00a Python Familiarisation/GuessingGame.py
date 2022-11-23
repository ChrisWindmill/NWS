""" Module definition """

__version__ = '0.1'
__author__ = 'Christopher Windmill'

import random


class GuessingGame:
    """A simple guessing game demonstrating public, private, and protected methods"""

    __StaticVariable = "This is a static variable across all instances of the class"

    # Private method - constructor equivalent
    def __init__(self):
        self.__InstanceVariable = "This is a value unique to this instance"
        self.__Guesses = 0
        self.__Role = "guess"
        self.__Min = -1
        self.__Max = -1
        self.__Number = -1
        self.__Victory = False

    """Validates that a number is an integer between range_min and range_max inclusive"""
    @staticmethod
    def _get_num_in_range(range_min: int, range_max: int) -> int:
        entered_num = -1
        while entered_num < 0:
            try:
                entered_num = int(input(f"Please enter an integer number between {range_min} and {range_max}: "))
                if entered_num < range_min or entered_num > range_max:
                    entered_num = -1
                    print("That wasn't a number in the range.")
            except (ValueError, TypeError):
                print("That wasn't an integer!")
        return entered_num

    # Public method - entry point to the class
    def run(self):
        self.__Role = self._role()
        if self.__Role == "play":
            self.__Number = self._get_num_in_range(0, 99)
            self.__Min = 0
            self.__Max = 99
            self._play()
        else:
            self.__Min = self._get_num_in_range(0, 1000)
            self.__Max = self._get_num_in_range(self.__Min, 1000)
            self._guess()

    # Protected methods - should not be publically accessible but may be overridden by inheritance
    @staticmethod
    def _role() -> str:
        choice = "-1"
        choices = ["p", "g", "r"]
        print("Please enter a choice of (P)lay, (G)uess, or (R)andom")
        while choice.lower() not in choices:
            choice = input()
        if choice == "p":
            return "play"
        else:
            return "guess"

    def _play(self):
        while not self.__Victory:
            number = random.randint(self.__Min, self.__Max)
            print(f"I choose: {number}")
            if number > self.__Number:
                print("I was too high :(")
                self.__Max = number
            elif number < self.__Number:
                print("I was too low :(")
                self.__Min = number
            else:
                print("I won!")
                self.__Victory = True
        pass

    def _guess(self):
        self.__Number = random.randint(self.__Min, self.__Max)
        choices = []
        while not self.__Victory:
            print(f"Make a guess between {self.__Min} and {self.__Max}")
            choice = int(input())
            if choice in choices:
                print("You picked that number already")
            else:
                    choices.append(choice)
            if choice < self.__Number:
                print("Guess higher")
            elif choice > self.__Number:
                print("Guess lower")
            else:
                print("You got it right!!!")
                self.__Victory = True
        pass

    def _victory(self):
        pass


if __name__ == "__main__":
    game = GuessingGame()
    game.run()
