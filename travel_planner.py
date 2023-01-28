from format import *

class TravelPlanner:

    def __init__(self) -> None:
        """Initialize."""
        self._trip_name = None
        self._start_date = None
        self._end_date = None
        self._from_location = None
        self._to_location = None
        self._travel_itinerary = {}
        self._packing_list = {}
        self._travel_budget = {}

    def get_user_input(self, choices) -> str:
        """
        Gets input from the user for their choice of Yes or No
        :param: none
        :return: string value of choice (1 or 2)
        """
        # store the numbered options that the user can enter
        index_list = []

        # create the options based on the provided choices
        for index, choice in enumerate(choices):
            index_list.append(str(index + 1))
            print(f'{index + 1}: {choice}')

        # keep checking for valid input
        while True:
            # get the user input and first see if they typed quit
            user_input = input(f'{shellColors.BLUE}Please Enter The Number: {shellColors.ENDCOLOR}')
            self.check_quit(user_input)
            # if the user input is invalid
            if user_input not in index_list:
                print(f'Sorry, your answer should be between {1} and {len(choices)}')
                continue
            else:
                return user_input

    def check_quit(self, input):
        """Checks if the user typed quit to """
        if input == "quit":
            self.quit_process()

    def quit_process(self):
        """Quits the process"""
        print('Quitting process...Bye!')
        return








# start process
travel_planner = TravelPlanner()

