from format import *
import csv
import time


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
        self._target_budget = None
        self._currency_pair = {'Base': None, 'Quote': None}
        self._travel_budget_converted = {}
        self._fx_rate = None
        self._target_budget_converted = None

    def get_user_choice(self, choices) -> str:
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
                print(f'{shellColors.YELLOW}Sorry, your answer should be between {shellColors.BOLD}{1} and {len(choices)}{shellColors.ENDCOLOR}')
                continue
            else:
                return user_input

    def check_quit(self, input):
        """Checks if the user typed quit to """
        if input.lower() == "quit":
            self.quit_process()

    def quit_process(self):
        """Quits the process"""
        print('Quitting process...Bye!')
        exit()

    def start_process(self):
        print('Starting Application...\n')
        print(Format.APPNAME)
        print(Format.LINE)
        # TODO: update this because user has to enter number within bounds
        print(f'{shellColors.GREEN}|{shellColors.ENDCOLOR} Before we start, here are useful features...   {shellColors.GREEN}|{shellColors.ENDCOLOR}')
        print(f'{shellColors.GREEN}|{shellColors.ENDCOLOR}    • Enter the number choice when asked.       {shellColors.GREEN}|{shellColors.ENDCOLOR}')
        print(f'{shellColors.GREEN}|{shellColors.ENDCOLOR}    • Provide as much or as little as you want. {shellColors.GREEN}|{shellColors.ENDCOLOR}')
        print(f'{shellColors.GREEN}|{shellColors.ENDCOLOR}      Dont worry, you can make changes!         {shellColors.GREEN}|{shellColors.ENDCOLOR}')
        print(f'{shellColors.GREEN}|{shellColors.ENDCOLOR}    • Press "enter" to skip Y/N questions.      {shellColors.GREEN}|{shellColors.ENDCOLOR}')
        print(f'{shellColors.GREEN}|{shellColors.ENDCOLOR}    • Type "quit" to any Y/N question to quit.  {shellColors.GREEN}|{shellColors.ENDCOLOR}')
        print(Format.LINE)
        self.main_menu_nav()

    def display_delete_warning(self):
        """Displays a delete warning message"""
        print(f'{shellColors.RED}Deletions cannot be undone!{shellColors.ENDCOLOR}')

    def display_warning(self, msg):
        "Displays warning message of provided message"
        print(f'{shellColors.YELLOW}{msg}: {shellColors.ENDCOLOR}')

    def get_user_input(self, prompt):
        """Get input from user based on provided prompt"""
        answer = input(f'{shellColors.BLUE}{prompt}: {shellColors.ENDCOLOR}')
        return answer

    def main_menu_nav(self):
        """Display navigation"""
        print(Format.NEWLINE)
        print(Format.LINE)
        print(Format.APPNAME)
        print(Format.LINE)
        print(f'{shellColors.BLUE}Where would you like to go?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(["Itinerary", "Packing List", "Budget", "Travel Planner", "Quit"])
        self.check_quit(user_input)

        # check input
        if user_input == "1":
            self.itinerary_nav()
        elif user_input == "2":
            self.packing_nav()
        elif user_input == "3":
            self.budget_nav()
        elif user_input == "4":
            self.planner_nav()
        elif user_input == "5":
            self.quit_process()
            return

    #### ITINERARY SECTION START ####

    def itinerary_nav(self):
        """Display the itinerary nav"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.ITINAME)
        print(Format.LINEBLU)
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')

        user_input = self.get_user_choice(
            ["Create Itinerary", "Update Itinerary", "Delete Itinerary", "View Itinerary", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)
        print('')

        if user_input == "1":
            self.create_new_itinerary()
        elif user_input == "2":
            self.update_itinerary_nav()
        elif user_input == "3":
            self.delete_itinerary_nav()
        elif user_input == "4":
            self.display_itinerary()
            self.itinerary_nav()
        elif user_input == "5":
            self.main_menu_nav()
        elif user_input == "6":
            self.quit_process()
            return

    def create_new_itinerary(self):
        """Creates a new itinerary"""
        self.set_trip_name()
        self.set_start_date()
        self.set_end_date()
        self.set_from_location()
        self.set_to_location()
        self.set_itinerary()

    def set_trip_name(self) -> None:
        """Sets trip name"""
        prompt = 'What would you like to name this trip?'
        trip_name = self.get_user_input(prompt)
        self.check_quit(trip_name)
        self._trip_name = trip_name

    def get_trip_name(self) -> None:
        """Gets trip name"""
        return self._trip_name

    def set_start_date(self):
        """Sets start date"""
        prompt = 'When does your trip start [MM/DD/YY]?'
        start_date = self.get_user_input(prompt)
        self.check_quit(start_date)
        self._start_date = start_date

    def get_start_date(self):
        """Gets start date"""
        return self._start_date

    def set_end_date(self):
        """Sets end date"""
        prompt = 'When does your trip start [MM/DD/YY]?'
        end_date = self.get_user_input(prompt)
        self.check_quit(end_date)
        self._end_date = end_date

    def get_end_date(self):
        """Get end date """
        return self._end_date

    def set_from_location(self):
        """Set from Location"""
        prompt = 'Where you you leaving from?'
        from_location = self.get_user_input(prompt)
        self.check_quit(from_location)
        self._from_location = from_location

    def get_from_location(self):
        """Get from Location"""
        return self._from_location

    def set_to_location(self):
        """Set to Location"""
        prompt = 'Where you you going to?'
        to_location = self.get_user_input(prompt)
        self.check_quit(to_location)
        self._to_location = to_location

    def get_to_location(self):
        """Get to Location"""
        return self._to_location

    def set_itinerary(self) -> None:
        """Set and create an itinerary"""
        prompt = 'Would you like to create an itinerary of activities? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        self.check_quit(user_input)
        # check input
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):

            continue_flag = True
            activity_counter = 0

            while continue_flag is True:
                activity_counter += 1
                user_activity = input(f'{shellColors.BLUE}{activity_counter}) Activity Description: ')
                self._travel_itinerary[activity_counter] = user_activity
                continue_input = input(f'{shellColors.BLUE} Would you like to add another? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}: ')
                self.check_quit(continue_input)

                if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                    continue_flag = True
                else:
                    continue_flag = False

        print('')
        prompt = f'Would you like to view the itinerary? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        self.check_quit(user_input)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_itinerary()
        self.itinerary_nav()

    def update_activities_nav(self):
        """Navigation for updates to activities"""
        print('')
        print(f'What activities would you like to {shellColors.YELLOW}update{shellColors.ENDCOLOR}?')
        user_input = self.get_user_choice(
            ["Update All", "Update Activity", "Itinerary Menu", "View Itinerary", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)

        if user_input == "1":
            self.set_itinerary()
        if user_input == "2":
            self.update_selected_activity()
        if user_input == "3":
            self.itinerary_nav()
        if user_input == "4":
            self.display_itinerary()
            self.update_itinerary_nav()
        if user_input == "5":
            self.main_menu_nav()
        if user_input == "6":
            self.quit_process()
            return

    def update_selected_activity(self):
        """Updates Selected Activity"""
        choices_list = []
        for i in self._travel_itinerary:
            choices_list.append(f'{self._travel_itinerary[i]}')

        main_choices = ["Itinerary Menu", "View Itinerary", "Main Menu"]

        choices_list = choices_list + main_choices
        print('\nWhat activity would you like to update')
        user_input = self.get_user_choice(choices_list)
        self.check_quit(user_input)

        if int(user_input) <= (len(choices_list) - len(main_choices)):
            print(f'Updating Activity {user_input}: {self._travel_itinerary[int(user_input)]}...')
            prompt = 'Updated Activity: '
            new_description = self.get_user_input(prompt)
            self._travel_itinerary[int(user_input)] = new_description
        elif user_input == str(len(choices_list) - 2):
            print('yep')
            self.itinerary_nav()
        elif user_input == str(len(choices_list) - 1):
            print('wrong')
            self.display_itinerary()
            self.update_selected_activity()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def display_itinerary(self):
        """Displays itinerary"""
        print('')
        print(f'{shellColors.BOLD}Trip Name{shellColors.ENDCOLOR}: {shellColors.GREEN}{self._trip_name}{shellColors.ENDCOLOR}')
        print(f'{shellColors.BOLD}Leaving{shellColors.ENDCOLOR} {shellColors.GREEN}{self._start_date}{shellColors.ENDCOLOR} {shellColors.BOLD}to{shellColors.ENDCOLOR} {shellColors.GREEN}{self._end_date}{shellColors.ENDCOLOR}')
        print(f'{shellColors.BOLD}From{shellColors.ENDCOLOR} {shellColors.GREEN}{self._from_location}{shellColors.ENDCOLOR} {shellColors.BOLD}to{shellColors.ENDCOLOR} {shellColors.GREEN}{self._to_location}{shellColors.ENDCOLOR}')

        if self._travel_itinerary:
            print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Activities:{shellColors.ENDCOLOR}')
            for i in self._travel_itinerary:
                print(f'{shellColors.BOLD}{i}{shellColors.ENDCOLOR} : {self._travel_itinerary[i]}')
        else:
            self.display_warning('Your itinerary of activiites is empty!')

    def update_itinerary_nav(self):
        """Update itinerary navigation"""
        print('')
        print(f'{shellColors.BLUE}What would you like to {shellColors.ENDCOLOR}{shellColors.YELLOW}update{shellColors.ENDCOLOR}?')
        user_input = self.get_user_choice(
            ["Update All", "Update Trip Name", "Update Dates", "Update Locations", "Update Activiites", "Itinerary Menu", "View Itinerary", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)

        if user_input == "1":
            self.create_new_itinerary()
        elif user_input == "2":
            self.set_trip_name()
            self.itinerary_nav()
        elif user_input == "3":
            self.set_start_date()
            self.set_end_date()
            self.itinerary_nav()
        elif user_input == "4":
            self.set_from_location()
            self.set_to_location()
            self.itinerary_nav()
        elif user_input == "5":
            self.update_activities_nav()
            self.itinerary_nav()
        elif user_input == "6":
            self.itinerary_nav()
        elif user_input == "7":
            self.display_itinerary()
            self.itinerary_nav()
        elif user_input == "8":
            self.main_menu_nav()
        elif user_input == "9":
            self.quit_process()
            return

    def delete_itinerary_nav(self):
        """Delete itinerary nav"""
        print(f'What would you like to {shellColors.RED}delete?{shellColors.ENDCOLOR}')
        self.display_delete_warning()
        user_input = self.get_user_choice(
            ["Delete All", "Delete Trip Name", "Delete Dates", "Delete Locations", "Delete Activities", "Itinerary Menu", "View Itinerary", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)

        if user_input == "1":
            user_input = input(f'{shellColors.RED}Are you sure you want to delete all fields{shellColors.ENDCOLOR}? Type {shellColors.BOLD}{shellColors.RED}"yes" or "y": {shellColors.ENDCOLOR}')
            if user_input.lower() == "yes" or user_input.lower() == "y":
                self._trip_name = None
                self._start_date = None
                self._end_date = None
                self._from_location = None
                self._to_location = None
                self._travel_itinerary = {}
                self.display_warning("All items deleted.")
            self.itinerary_nav()
        elif user_input == "2":
            user_input = input(f'{shellColors.RED}Are you sure you want to delete the trip name?{shellColors.ENDCOLOR}? Type {shellColors.BOLD}{shellColors.RED}"yes" or "y": {shellColors.ENDCOLOR}')
            if user_input.lower() == "yes" or user_input.lower() == "y":
                self._trip_name = None
                self.display_warning("Trip name deleted.")
            self.itinerary_nav()
        elif user_input == "3":
            user_input = input(f'{shellColors.RED}Are you sure you want to delete the dates{shellColors.ENDCOLOR}? Type {shellColors.BOLD}{shellColors.RED}"yes" or "y": {shellColors.ENDCOLOR}')
            if user_input.lower() == "yes" or user_input.lower() == "y":
                self._start_date = None
                self._end_date = None
                self.display_warning("Dates deleted.")
            self.itinerary_nav()
        elif user_input == "4":
            user_input = input(f'{shellColors.RED}Are you sure you want to delete the locations{shellColors.ENDCOLOR}? Type {shellColors.BOLD}{shellColors.RED}"yes" or "y": {shellColors.ENDCOLOR}')
            if user_input.lower() == "yes" or user_input.lower() == "y":
                self._from_location = None
                self._to_location = None
                self.display_warning("Locations deleted.")
            self.itinerary_nav()
        elif user_input == "5":
            user_input = input(f'{shellColors.RED}Are you sure you want to delete the activities{shellColors.ENDCOLOR}? Type {shellColors.BOLD}{shellColors.RED}"yes" or "y": {shellColors.ENDCOLOR}')
            if user_input.lower() == "yes" or user_input.lower() == "y":
                self._travel_itinerary = {}
                self.display_warning("Itinerary of activities deleted.")
            self.itinerary_nav()
        elif user_input == "6":
            self.itinerary_nav()
        elif user_input == "7":
            self.display_itinerary()
        elif user_input == "8":
            self.main_menu_nav()
        elif user_input == "9":
            self.quit_process()

    #### ITINERARY SECTION END ####

    #### PACKING LIST SECTION START ####

    def packing_nav(self):
        """Display the itinerary nav"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.PCKNAME)
        print(Format.LINEBLU)

        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')

        user_input = self.get_user_choice(
            ["Create Packing List", "Update Packing List", "Delete Packing List", "View Packing List", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)
        print('')

        if user_input == "1":
            self.create_new_packing_list()
        elif user_input == "2":
            self.update_packing_list_nav()
        elif user_input == "3":
            self.delete_packing_list()
        elif user_input == "4":
            self.display_packing_list()
            self.packing_nav()
        elif user_input == "5":
            self.main_menu_nav()
        elif user_input == "6":
            self.quit_process()
            return

    def create_new_packing_list(self):
        """Creates a new packing list"""
        prompt = 'Would you like to create a packing list? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        self.check_quit(user_input)

        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            continue_flag = True
            item_counter = 0

            while continue_flag is True:
                item_counter += 1
                item_name = input(f'{shellColors.BLUE}{item_counter}) Item name: ')
                item_quantity = input(f'{shellColors.BLUE}{item_counter}) Item quantity: ')
                self._packing_list[item_counter] = [item_name, item_quantity]
                continue_input = input(f'{shellColors.BLUE} Would you like to add another? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}: ')
                self.check_quit(continue_input)

                if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                    continue_flag = True
                else:
                    continue_flag = False

        print('')
        prompt = f'Would you like to view the packing list? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        self.check_quit(user_input)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_packing_list()
        self.packing_nav()


    def update_packing_list_nav(self):
        """Update packing list nav"""
        choices_list = []
        for i in self._packing_list:
            choices_list.append(f'{self._packing_list[i]}')

        main_choices = ["Add New Item", "Packing Menu", "View Packing List", "Main Menu"]

        choices_list = choices_list + main_choices
        print('\nWhat item would you like to update')
        user_input = self.get_user_choice(choices_list)
        self.check_quit(user_input)

        if int(user_input) <= (len(choices_list) - len(main_choices)):
            print(f'Updating Activity {user_input}: {self._packing_list[int(user_input)]}...')
            item_name = 'Updated Item Name: '
            item_quantity = 'Updated Item Quantity: '
            new_name = self.get_user_input(item_name)
            new_quantity = self.get_user_input(item_quantity)
            self._packing_list[int(user_input)] = [new_name, new_quantity]
            self.packing_nav()
        elif user_input == str(len(choices_list) - 3):
            if self._packing_list:
                keys = self._packing_list.keys()
                key_list = []
                for key in keys:
                    key_list.append(key)
                item_counter = int(key_list[-1]) + 1
            else:
                item_counter = 0
            continue_flag = True
            while continue_flag is True:
                item_counter += 1
                item_name = input(f'{shellColors.BLUE}{item_counter}) Item name: ')
                item_quantity = input(f'{shellColors.BLUE}{item_counter}) Item quantity: ')
                self._packing_list[item_counter] = [item_name, item_quantity]
                continue_input = input(f'{shellColors.BLUE} Would you like to add another? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}: ')
                self.check_quit(continue_input)
                if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                    continue_flag = True
                else:
                    continue_flag = False
            self.packing_nav()
        elif user_input == str(len(choices_list) - 2):
            self.packing_nav()
        elif user_input == str(len(choices_list) - 1):
            self.display_packing_list()
            self.packing_nav()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def delete_packing_list(self):
        """Delete packing list"""
        self.display_delete_warning()
        user_input = self.get_user_choice(
            ["Delete All", "Packing Menu", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)

        if user_input == "1":
            self.display_delete_warning()
            user_input = input(f'{shellColors.RED}Are you sure you want to delete all packing items{shellColors.ENDCOLOR}? Type {shellColors.BOLD}{shellColors.RED}"yes" or "y": {shellColors.ENDCOLOR}')
            if user_input.lower() == "yes" or user_input.lower() == "y":
                self._packing_list = {}
            self.packing_nav()
        elif user_input == "2":
            self.packing_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    def display_packing_list(self):
        """Display packing list"""
        print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Packing List:{shellColors.ENDCOLOR}')
        if self._packing_list:
            # Print the names of the columns.
            print("{:<10} {:<10} {:<10}".format(f'{shellColors.GREEN}{shellColors.BOLD}Item #{shellColors.ENDCOLOR}', f'    {shellColors.GREEN}{shellColors.BOLD}Item{shellColors.ENDCOLOR}', f'      {shellColors.GREEN}{shellColors.BOLD}Quantity{shellColors.ENDCOLOR}'))
            # print each data item.
            for key, value in self._packing_list.items():
                item, quantity = value
                print("{:<10} {:<10} {:<10}".format(f'{key}', f'{item}', f'{quantity}'))
        else:
            self.display_warning('Your packing list is empty.')

    #### PACKING LIST END ####


    #### BUDGET START ####

    def budget_nav(self):
        """Display the budget nav"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.BDGNAME)
        print(Format.LINEBLU)

        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')

        user_input = self.get_user_choice(
            ["Create Budget", "Update Budget", "Delete Budget", "View Budget", "Convert Budget to FX", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)
        print('')

        if user_input == "1":
            self.create_new_budget()
        elif user_input == "2":
            self.update_budget_nav()
        elif user_input == "3":
            self.delete_budget()
        elif user_input == "4":
            self.display_budget()
            self.budget_nav()
        elif user_input == "5":
            self.convert_budget_to_fx()
        elif user_input == "6":
            self.main_menu_nav()
        elif user_input == "7":
            self.quit_process()
            return

    def create_new_budget(self):
        """Create a new budget"""
        prompt = 'Would you like to create a budget? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        self.check_quit(user_input)

        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            target_budget = self.get_user_input('What is your total budget?')
            self._target_budget = target_budget
            continue_flag = True
            item_counter = 0

            while continue_flag is True:
                item_counter += 1
                spend_name = input(f'{shellColors.BLUE}{item_counter}) Spend name: ')
                spend_amount = input(f'{shellColors.BLUE}{item_counter}) Spend amount: ')
                self._travel_budget[item_counter] = [spend_name, spend_amount]
                continue_input = input(f'{shellColors.BLUE} Would you like to add another? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}: ')
                self.check_quit(continue_input)
                if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                    continue_flag = True
                else:
                    continue_flag = False

        print('')
        prompt = f'Would you like to view the budget? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        self.check_quit(user_input)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_budget()
        self.budget_nav()

    def update_budget_nav(self):
        """Update budget navigation"""
        choices_list = []
        for i in self._travel_budget:
            choices_list.append(f'{self._travel_budget[i]}')

        main_choices = ["Add New Budget Item", "Budget Menu", "View Budget", "Main Menu"]

        choices_list = choices_list + main_choices
        print('\nWhat item would you like to update')
        user_input = self.get_user_choice(choices_list)
        self.check_quit(user_input)

        if int(user_input) <= (len(choices_list) - len(main_choices)):
            print(f'Updating Budget {user_input}: {self._travel_budget[int(user_input)]}...')
            item_name = 'Updated Spend Name: '
            item_spend = 'Updated Spend Amount: '
            new_name = self.get_user_input(item_name)
            new_spend = self.get_user_input(item_spend)
            self._travel_budget[int(user_input)] = [new_name, new_spend]
            self.budget_nav()
        elif user_input == str(len(choices_list) - 3):
            if self._travel_budget:
                keys = self._travel_budget.keys()
                key_list = []
                for key in keys:
                    key_list.append(key)
                item_counter = int(key_list[-1]) + 1
            else:
                item_counter = 0
            continue_flag = True
            while continue_flag is True:
                item_counter += 1
                item_name = input(f'{shellColors.BLUE}{item_counter}) Spend name: ')
                item_quantity = input(f'{shellColors.BLUE}{item_counter}) Spend amount: ')
                self._travel_budget[item_counter] = [item_name, item_quantity]
                continue_input = input(f'{shellColors.BLUE} Would you like to add another? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}: ')
                self.check_quit(continue_input)
                if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                    continue_flag = True
                else:
                    continue_flag = False
            self.budget_nav()
        elif user_input == str(len(choices_list) - 2):
            self.budget_nav()
        elif user_input == str(len(choices_list) - 1):
            self.display_budget()
            self.budget_nav()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def delete_budget(self):
        """Delete budget"""
        self.display_delete_warning()
        user_input = self.get_user_choice(
            ["Delete All", "Budget Menu", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)

        if user_input == "1":
            self.display_delete_warning()
            user_input = input(f'{shellColors.RED}Are you sure you want to delete all budget items{shellColors.ENDCOLOR}? Type {shellColors.BOLD}{shellColors.RED}"yes" or "y": {shellColors.ENDCOLOR}')
            if user_input.lower() == "yes" or user_input.lower() == "y":
                self._target_budget = None
                self._travel_budget = {}
            self.budget_nav()
        elif user_input == "2":
            self.budget_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    def display_budget(self):
        """Display the budget"""
        print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Budget:{shellColors.ENDCOLOR}')
        # show if the currency pair has been specified for the budget
        if self._currency_pair['Base'] is not None:
            user_ccy = self._currency_pair['Base']
            print(f'Target Budget {self._currency_pair["Quote"]}: {self._target_budget_converted}')
        else:
            user_ccy = ''
        # get calculated total
        calc_total = self.calculate_total_spend()
        print(f'Target Budget {user_ccy}: {self._target_budget} vs Calculated Total: {calc_total}')
        # if a target budget has been specified then display it
        if self._target_budget is not None:
            if int(calc_total) <= int(self._target_budget):
                print(f'You are under budget by {shellColors.GREEN}{shellColors.BOLD}{int(self._target_budget) - int(calc_total)}{shellColors.ENDCOLOR}')
            else:
                print(f'You are over budget by {shellColors.RED}{shellColors.BOLD}{int(self._target_budget) - int(calc_total)}{shellColors.ENDCOLOR}')
        print('')
        # if there is a target budget then display all the budget line items
        if self._target_budget:
            # Print the names of the columns.
            print("{:<10} {:<10} {:<10}".format(f'{shellColors.GREEN}{shellColors.BOLD}Category{shellColors.ENDCOLOR}', f'  {shellColors.GREEN}{shellColors.BOLD}Amount{shellColors.ENDCOLOR}', f'  {shellColors.GREEN}{shellColors.BOLD}FX ({self._currency_pair["Quote"]}){shellColors.ENDCOLOR}'))
            # print each data item.
            for key, value in self._travel_budget.items():
                category, spend = value
                if self._target_budget_converted is None:
                    fx_amt = None
                else:
                    fx_amt = self._travel_budget_converted[key][1]
                print("{:<10} {:<10} {:<10}".format(f'{category}', f'{spend}', f'{fx_amt}'))
        # otherwise the budget is empty
        else:
            self.display_warning('Your budget is empty.')

    def calculate_total_spend(self):
        """Calculate total provided user input for budget"""
        total = 0
        if self._travel_budget:
            keys = self._travel_budget.keys()
            for key in keys:
                total += int(self._travel_budget[key][1])
        return total

    def convert_budget_to_fx(self):
        """Convert the budget to FX with Microservice"""
        # get user input
        user_input = self.get_user_choice(
            ["Convert Budget to FX", "Budget Menu", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)

        # convert the budget to FX
        if user_input == "1":
            # if a budget hasn't yet been specified then go back to nav
            if not self._travel_budget:
                self.display_warning('The budget is currently empty! Please create a budget first.')
                self.budget_nav()
            # otherwise, get the from/to currency and then provide to microservice to get conversion
            else:
                from_ccy = input(f'{shellColors.BLUE} From Currency: ')
                to_ccy = input(f'{shellColors.BLUE} To Currency: ')
                self._currency_pair['Base'] = from_ccy
                self._currency_pair['Quote'] = to_ccy

                # open the communication pipe file and write to it the fx pair and amount to convert
                pair = str(from_ccy+to_ccy)
                pair_amt = [pair, self._target_budget]
                with open('./CurrencyMS/fx_request.csv', 'w') as fx_req_file:
                    writer = csv.writer(fx_req_file)
                    writer.writerow(pair_amt)

                # open the communication text file and write RUN so that microservice can fetch and convert
                with open('./CurrencyMS/fx_run.txt', 'w') as req_file:
                    req_file.write('RUN')

                # display message to the user
                self.display_warning('Microservice is fetching rates and performing calculations...')
                time.sleep(10)

                # open the communication pipe file and read from it the converted amount
                with open('./CurrencyMS/fx_converted.csv', 'r') as fx_rec_file:
                    datareader = csv.reader(fx_rec_file)
                    converted_amount = next(datareader)
                    converted_amount = float(converted_amount[0])
                    self._fx_rate = converted_amount / float(self._target_budget)
                    self._target_budget_converted = converted_amount

                # add converted amounts to converted dict
                for key in self._travel_budget:
                    category = self._travel_budget[key][0]
                    amount = float(self._travel_budget[key][1])
                    amt_fx = round(amount * self._fx_rate, 2)
                    amt_fx = str(amt_fx)
                    self._travel_budget_converted[key] = [category, amt_fx]

                # go back to nav
                self.display_warning('Conversions Completed!')
                self.budget_nav()
        # go back to budget menu
        elif user_input == "2":
            self.budget_nav()
        # go back to main menu
        elif user_input == "3":
            self.main_menu_nav()
        # quit process
        elif user_input == "4":
            self.quit_process()


    #### TRAVEL PLANNER ####

    def planner_nav(self):
        """Display the budget nav"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.PLRNAME)
        print(Format.LINEBLU)

        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')

        user_input = self.get_user_choice(
            ["View Planner", "Main Menu", "Quit"]
        )
        self.check_quit(user_input)
        print('')

        if user_input == "1":
            self.display_planner()
        elif user_input == "2":
            self.main_menu_nav()
        elif user_input == "3":
            self.quit_process()
            return

    def display_planner(self):
        """Display the Travel Planner"""
        print(Format.LINE)
        self.display_itinerary()
        print('')
        self.display_packing_list()
        print('')
        self.display_budget()
        print(Format.LINE)
        self.planner_nav()

# start process
travel_planner = TravelPlanner()
travel_planner.start_process()