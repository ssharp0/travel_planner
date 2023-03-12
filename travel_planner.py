from format import *
import csv
import time


class TravelPlanner:

    def __init__(self) -> None:
        """Initialize for storing data provided by user."""
        self._trip_name = None
        self._start_date = None
        self._end_date = None
        self._from_location = None
        self._to_location = None
        self._travel_itinerary = {}
        self._packing_list = {}
        self._travel_budget = {}
        self._target_budget = None
        self._currency_pair = {'Base': 'None', 'Quote': 'None'}
        self._travel_budget_converted = {}
        self._fx_rate = None
        self._target_budget_converted = None
        self._contacts = {}

    ### INTERACTION WITH MICROSERVICE START ###

    def convert_budget_to_fx(self):
        """Convert the budget to FX with Microservice"""
        # get user input and check if they typed quit
        user_input = self.get_user_choice(["Convert Budget to FX", "Budget Menu", "Main Menu", "Quit"])
        self.check_quit(user_input)
        # convert the budget to FX
        if user_input == "1":
            # if a budget hasn't yet been specified then go back to nav
            if not self._travel_budget:
                self.display_warning('The budget is currently empty! Please create a budget first.')
                self.budget_nav()
            # otherwise, get the from/to currency and then provide to microservice to get conversion
            else:
                self.get_currency_pair()
        # go back to budget menu
        elif user_input == "2":
            self.budget_nav()
        # go back to main menu
        elif user_input == "3":
            self.main_menu_nav()
        # quit process
        elif user_input == "4":
            self.quit_process()

    def get_currency_pair(self):
        """Gets the currency pair from user input to request fx from microservice"""
        from_ccy = input(f'{shellColors.BLUE} From Currency: ')
        to_ccy = input(f'{shellColors.BLUE} To Currency: ')
        self._currency_pair['Base'] = from_ccy
        self._currency_pair['Quote'] = to_ccy
        # request the fx from microservice based on currency pair
        self.request_fx_ms(from_ccy, to_ccy)

    def request_fx_ms(self, from_ccy, to_ccy):
        """Provide from and to currency to microservice to get the fx rates for provided pair"""
        pair = str(from_ccy + to_ccy)
        pair_amt = [pair, self._target_budget]
        # call the functions to write, request and read from the Microservice
        self.write_to_fx_request_file(pair_amt)
        self.run_fx_request()
        self.read_from_fx_converted_file()
        # update the budget amounts with the fx received then go back to the nav
        self.update_budget_with_converted_fx()
        self.budget_nav()

    def write_to_fx_request_file(self, pair_amt):
        """Write to the FX request file the fx pair and amount for Microservice to convert"""
        with open('./CurrencyMS/fx_request.csv', 'w') as fx_req_file:
            writer = csv.writer(fx_req_file)
            writer.writerow(pair_amt)

    def run_fx_request(self):
        """Write to the FX run text file 'RUN' so Microservice can check communication pipeline"""
        with open('./CurrencyMS/fx_run.txt', 'w') as req_file:
            req_file.write('RUN')
        # display message to the user that MS is running
        self.display_warning('Microservice is fetching rates and performing calculations...')
        time.sleep(10)

    def read_from_fx_converted_file(self):
        """Read the converted fx from the fx converted file that the Mircoservice updated"""
        with open('./CurrencyMS/fx_converted.csv', 'r') as fx_rec_file:
            datareader = csv.reader(fx_rec_file)
            # convert to float to be used in the application and set the fx rate & update the amount with the fx
            converted_amount = next(datareader)
            converted_amount = float(converted_amount[0])
            self._fx_rate = converted_amount / float(self._target_budget)
            self._target_budget_converted = converted_amount

    def update_budget_with_converted_fx(self):
        """Update each item in the budget with the FX that was provided by the Mircoservice"""
        # apply the recieved fx from the microservice to all items in the budget
        for key in self._travel_budget:
            category = self._travel_budget[key][0]
            amount = float(self._travel_budget[key][1])
            amt_fx = round(amount * self._fx_rate, 2)
            amt_fx = str(amt_fx)
            self._travel_budget_converted[key] = [category, amt_fx]
        # notify user the fx process has been completed
        self.display_warning('Conversions Completed!')

    ### INTERACTION WITH MICROSERVICE END ###

    ### GENERAL SETUP AND MAIN APPLICATION NAVIGATION ###

    def get_user_choice(self, choices):
        """Gets the users choice from a provided list of choices"""
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
                self.display_incorrect_choice_msg(len(choices))
                continue
            else:
                return user_input

    def get_user_input(self, prompt):
        """Gets input from user based on provided prompt"""
        answer = input(f'{shellColors.BLUE}{prompt}: {shellColors.ENDCOLOR}')
        self.check_quit(answer)
        return answer

    def continue_input(self):
        """Asks if the user would like to add another item (i.e. continue by inputting another item)"""
        # variables to store bash colors and input prompt
        blue = shellColors.BLUE
        bold = shellColors.BOLD
        end_color = shellColors.ENDCOLOR
        continue_input = input(
            f'{blue} Would you like to add another? Type {bold}"yes" or "y"{end_color}: '
        )
        self.check_quit(continue_input)
        # return the user input
        return continue_input

    def display_incorrect_choice_msg(self, len_choices):
        """Display an error/warning message that the input should be within the provided range"""
        # assign variables to store bash color info
        yellow = shellColors.YELLOW
        bold = shellColors.BOLD
        end_color = shellColors.ENDCOLOR
        # display message to the user that the choice selection should be within range
        print(f'{yellow}Sorry, your answer should be between {bold}{1} and {len_choices}{end_color}')

    def check_quit(self, input):
        """Checks if the user typed quit to input"""
        if input.lower() == "quit":
            self.quit_process()

    def quit_process(self):
        """Quits the process"""
        print('Quitting process, thanks for using the Travel App...Bye!')
        exit()

    def display_intro_msg(self):
        """Display an introductory message to the user"""
        green = shellColors.GREEN
        end_color = shellColors.ENDCOLOR
        print(f'{green}|{end_color} Before we start, here are useful features...   {green}|{end_color}')
        print(f'{green}|{end_color}    • Enter the number choice when asked.       {green}|{end_color}')
        print(f'{green}|{end_color}    • Provide as much or as little as you want. {green}|{end_color}')
        print(f'{green}|{end_color}      Dont worry, you can make changes!         {green}|{end_color}')
        print(f'{green}|{end_color}    • Press "enter" to skip Y/N questions.      {green}|{end_color}')
        print(f'{green}|{end_color}    • Type "quit" to any Y/N question to quit.  {green}|{end_color}')

    def display_delete_warning(self):
        """Displays a delete warning (red) message"""
        print(f'{shellColors.RED}Deletions cannot be undone!{shellColors.ENDCOLOR}')

    def display_warning(self, msg):
        "Displays warning message (yellow) of provided message"
        print(f'{shellColors.YELLOW}{msg}{shellColors.ENDCOLOR}')

    def display_application_title(self):
        """Displays the application title and message to the user"""
        print(Format.NEWLINE)
        print(Format.LINE)
        print(Format.APPNAME)
        print(Format.LINE)

    def start_process(self):
        """Starts the Travel Planner Application by displaying a message to the user of useful features"""
        print('Starting Application...\n')
        print(Format.APPNAME)
        print(Format.LINE)
        self.display_intro_msg()
        print(Format.LINE)
        self.main_menu_nav()

    def main_nav_choices(self):
        """Store a list of all the features of the application that a user can navigate to from main menu"""
        choices = [
            "Itinerary",
            "Packing List",
            "Budget",
            "Important Contacts",
            "Travel Planner",
            "Travel Tips",
            "Quit"
        ]
        # return all the current navigation options
        return choices

    def main_menu_nav(self):
        """Display navigation for the main menu - navigates to all features of the application"""
        self.display_application_title()
        # get user choice to take the user to where they would like to go and check
        print(f'{shellColors.BLUE}Where would you like to go?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(self.main_nav_choices())

        # check the input and take them to where they would like to go
        if user_input == "1":
            self.itinerary_nav()
        elif user_input == "2":
            self.packing_nav()
        elif user_input == "3":
            self.budget_nav()
        elif user_input == "4":
            self.contacts_nav()
        elif user_input == "5":
            self.planner_nav()
        elif user_input == "6":
            self.display_travel_tips()
        elif user_input == "7":
            self.quit_process()

    ### SETUP AND MAIN APPLICATION NAVIGATION END ###

    #### ITINERARY SECTION START ####

    def display_itinerary_title(self):
        """Displays the itinerary section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.ITINAME)
        print(Format.LINEBLU)

    def itinerary_nav_choices(self):
        """Return a list of all the features of the application that a user can navigate to from itinerary menu"""
        choices = ["Create Itinerary", "Update Itinerary", "Delete Itinerary", "View Itinerary", "Main Menu", "Quit"]
        return choices

    def itinerary_nav(self):
        """Display the itinerary navigation"""
        self.display_itinerary_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        # get the user choice
        user_input = self.get_user_choice(self.itinerary_nav_choices())
        print('')
        # go the section based on user choice
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

    def create_new_itinerary(self):
        """Creates a new itinerary"""
        # call all the setter methods to get the user input and set the trip details
        self.set_trip_name()
        self.set_start_date()
        self.set_end_date()
        self.set_from_location()
        self.set_to_location()
        self.set_itinerary()

    def set_trip_name(self) -> None:
        """Sets trip name from user input"""
        prompt = 'What would you like to name this trip?'
        trip_name = self.get_user_input(prompt)
        self._trip_name = trip_name

    def set_start_date(self):
        """Sets start date from user input"""
        prompt = 'When does your trip start [MM/DD/YY]?'
        start_date = self.get_user_input(prompt)
        self._start_date = start_date

    def set_end_date(self):
        """Sets end date from user input"""
        prompt = 'When does your trip start [MM/DD/YY]?'
        end_date = self.get_user_input(prompt)
        self._end_date = end_date

    def set_from_location(self):
        """Set from Location from user input"""
        prompt = 'Where you you leaving from?'
        from_location = self.get_user_input(prompt)
        self._from_location = from_location

    def set_to_location(self):
        """Set to Location from user input"""
        prompt = 'Where you you going to?'
        to_location = self.get_user_input(prompt)
        self._to_location = to_location

    def set_itinerary_activities(self):
        """Sets the itinerary activites based on user input - user can enter as many items as desired"""
        # flags to help determine when the user wants to stop inputting activities
        continue_flag = True
        activity_counter = 0
        # while the user still wants to input activities continue to ask and add the details to the itinerary
        while continue_flag is True:
            activity_counter += 1
            user_activity = input(f'{shellColors.BLUE}{activity_counter}) Activity Description: ')
            self._travel_itinerary[activity_counter] = user_activity
            # ask if the user would like to continue
            continue_input = self.continue_input()
            # if they want to provide another activity then continue, otherwise stop loop
            if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                continue_flag = True
            else:
                continue_flag = False

    def set_itinerary(self):
        """Set and create an itinerary of activities based on user input"""
        prompt = 'Would you like to create an itinerary of activities? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        # if the user wants to provide an itinerary of activities, then continue to ask until they are finished
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            self.set_itinerary_activities()
        prompt = f'\nWould you like to view the itinerary? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        # if the user wants to see the itinerary then display it otherwise go back to nav menu
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_itinerary()
        self.itinerary_nav()

    def update_activities_nav_choices(self):
        """Return list of all the features of the application that a user can navigate to from itinerary update menu"""
        choices = ["Update All", "Update Activity", "Itinerary Menu", "View Itinerary", "Main Menu", "Quit"]
        return choices

    def update_activities_nav(self):
        """Navigation for updates to activities"""
        print(f'\nWhat activities would you like to {shellColors.YELLOW}update{shellColors.ENDCOLOR}?')
        user_input = self.get_user_choice(self.update_activities_nav_choices())
        # go to section based on user input
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

    def create_itinerary_update_choices(self):
        """Creates the menu of activities and the main choices for updating an activity"""
        # create a list of all the current activities to display back to user in numbered order
        choices_list = []
        for i in self._travel_itinerary:
            choices_list.append(f'{self._travel_itinerary[i]}')
        # combine the current activities and the main choices
        main_choices = ["Itinerary Menu", "View Itinerary", "Main Menu"]
        choices_list = choices_list + main_choices
        return choices_list, main_choices

    def update_selected_activity(self):
        """Update Selected Activity"""
        choices_list, main_choices = self.create_itinerary_update_choices()
        print('\nWhat activity would you like to update?')
        user_input = self.get_user_choice(choices_list)
        # update the corresponding user selected item
        if int(user_input) <= (len(choices_list) - len(main_choices)):
            print(f'Updating Activity {user_input}: {self._travel_itinerary[int(user_input)]}...')
            prompt = 'Updated Activity: '
            new_description = self.get_user_input(prompt)
            self._travel_itinerary[int(user_input)] = new_description
        elif user_input == str(len(choices_list) - 2):
            self.itinerary_nav()
        elif user_input == str(len(choices_list) - 1):
            self.display_itinerary()
            self.update_selected_activity()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def itinerary_update_main_nav_choices(self):
        """Return list of all the features of the application that a user can navigate to from itinerary update menu"""
        # return all the choices for the main itinerary update nav
        choices = ["Update All",
                   "Update Trip Name",
                   "Update Dates",
                   "Update Locations",
                   "Update Activities",
                   "Itinerary Menu",
                   "View Itinerary",
                   "Main Menu",
                   "Quit"]
        return choices

    def update_itinerary_nav(self):
        """Update itinerary navigation"""
        # display message to user to ask what they would like to update
        blue, yellow, end_color = shellColors.BLUE, shellColors.YELLOW, shellColors.ENDCOLOR
        print(f'\n{blue}What would you like to {end_color}{yellow}update{end_color}?')
        # get the user input and go to the section
        user_input = self.get_user_choice(self.itinerary_update_main_nav_choices())
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

    def itinerary_delete_nav_choices(self):
        """Return list of all features of the application that a user can navigate to from itinerary update menu"""
        # return all the choices for the main itinerary update nav
        choices = ["Delete All",
                   "Delete Trip Name",
                   "Delete Dates",
                   "Delete Locations",
                   "Delete Activities",
                   "Itinerary Menu",
                   "View Itinerary",
                   "Main Menu",
                   "Quit"]
        return choices

    def delete_itinerary_nav(self):
        """Delete itinerary nav"""
        print(f'What would you like to {shellColors.RED}delete?{shellColors.ENDCOLOR}')
        # display warning that deletions are irreversable and get user choice
        self.display_delete_warning()
        user_input = self.get_user_choice(self.itinerary_delete_nav_choices())
        # get the user input and go to the section
        if user_input == "1":
            self.delete_all_itinerary_items()
            self.itinerary_nav()
        elif user_input == "2":
            self.delete_trip_name()
            self.itinerary_nav()
        elif user_input == "3":
            self.delete_dates()
            self.itinerary_nav()
        elif user_input == "4":
            self.delete_locations()
            self.itinerary_nav()
        elif user_input == "5":
            self.delete_activities()
            self.itinerary_nav()
        elif user_input == "6":
            self.itinerary_nav()
        elif user_input == "7":
            self.display_itinerary()
        elif user_input == "8":
            self.main_menu_nav()
        elif user_input == "9":
            self.quit_process()

    def delete_all_itinerary_items(self):
        """Deletes all itinerary items"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete all fields{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        # if user wants to delete all then delete all currently stored itinerary information
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._trip_name = None
            self._start_date = None
            self._end_date = None
            self._from_location = None
            self._to_location = None
            self._travel_itinerary = {}
            self.display_warning("All items deleted.")

    def delete_trip_name(self):
        """Deletes the trip name"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the trip name?{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        # if user wants to delete the trip name then delete
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._trip_name = None
            self.display_warning("Trip name deleted.")

    def delete_dates(self):
        """Deletes the dates of the trip"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the dates{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        # if user wants to delete the trip dates then delete
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._start_date = None
            self._end_date = None
            self.display_warning("Dates deleted.")

    def delete_locations(self):
        """Deletes the locations of the trip"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the locations{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        # if user wants to delete the trip locations then delete
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._from_location = None
            self._to_location = None
            self.display_warning("Locations deleted.")

    def delete_activities(self):
        """Deletes all the activities of the trip"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the activities{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        # if user wants to delete the activities then delete
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._travel_itinerary = {}
            self.display_warning("Itinerary of activities deleted.")

    def display_a_to_b(self, a, a_msg, b):
        """Display message in the format of a to b"""
        # variables for formatting
        bold = shellColors.BOLD
        end_color = shellColors.ENDCOLOR
        green = shellColors.GREEN
        print(f'{bold}{a_msg}{end_color} {green}{a}{end_color} {bold}to{end_color} {green}{b}{end_color}')

    def display_trip_details(self):
        """Displays trip name, dates and locations"""
        # variables for formatting
        bold = shellColors.BOLD
        end_color = shellColors.ENDCOLOR
        green = shellColors.GREEN
        print('')
        print(f'{bold}Trip Name{end_color}: {green}{self._trip_name}{end_color}')
        self.display_a_to_b(self._start_date, 'Leaving', self._end_date)
        self.display_a_to_b(self._from_location, 'From', self._to_location)

    def display_itinerary_activities(self):
        """Displays the list of itinerary activities"""
        # if there is an activity then display it otherwise notify user
        if self._travel_itinerary:
            print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Activities:{shellColors.ENDCOLOR}')
            for i in self._travel_itinerary:
                print(f'{shellColors.BOLD}{i}{shellColors.ENDCOLOR} : {self._travel_itinerary[i]}')
        else:
            self.display_warning('Your itinerary of activities is empty!')

    def display_itinerary(self):
        """Displays itinerary details and activities"""
        self.display_trip_details()
        self.display_itinerary_activities()

    #### ITINERARY SECTION END ####

    #### PACKING LIST SECTION START ####

    def display_packing_title(self):
        """Displays the packing section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.PCKNAME)
        print(Format.LINEBLU)

    def packing_nav_choices(self):
        """Return a list of all the features of the application that a user can navigate to from packing menu"""
        choices = ["Create Packing List",
                   "Update Packing List",
                   "Delete Packing List",
                   "View Packing List",
                   "Main Menu",
                   "Quit"]
        return choices

    def packing_nav(self):
        """Display the packing nav"""
        self.display_packing_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        # get the user choice and then go to the section
        user_input = self.get_user_choice(self.packing_nav_choices())
        print('')
        if user_input == "1":
            self.create_new_packing_list()
        elif user_input == "2":
            self.update_packing_list_nav()
        elif user_input == "3":
            self.delete_packing_nav()
        elif user_input == "4":
            self.display_packing_list()
            self.packing_nav()
        elif user_input == "5":
            self.main_menu_nav()
        elif user_input == "6":
            self.quit_process()

    def set_packing_items(self):
        """Sets the packing list by prompting user until they choose to stop"""
        # variables to flag when user wishes to stop
        continue_flag = True
        item_counter = 0
        # continue asking if user wants to enter another packing item until they are done
        while continue_flag is True:
            item_counter += 1
            item_name = input(f'{shellColors.BLUE}{item_counter}) Item name: ')
            item_quantity = input(f'{shellColors.BLUE}{item_counter}) Item quantity: ')
            self._packing_list[item_counter] = [item_name, item_quantity]
            # check if user would like to input another packing item
            continue_input = self.continue_input()
            if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                continue_flag = True
            else:
                continue_flag = False

    def prompt_view_packing_list(self):
        """Prompts user asking if the user would like to view the packing list"""
        # ask if the user would like to view the packing list, then go back to the packing nav
        prompt = f'\nWould you like to view the packing list? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_packing_list()
        self.packing_nav()

    def create_new_packing_list(self):
        """Creates a new packing list"""
        prompt = 'Would you like to create a packing list? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        # if the user wants to create a packing list then continue to prompt for packing items until user is done
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            self.set_packing_items()
        # asks if user wants to view packing list
        self.prompt_view_packing_list()

    def create_packing_update_choices(self):
        """Creates the menu of activities and the main choices for updating a packing item"""
        choices_list = []
        # go through each packing item and add it to the list so user can specify which item to update
        for i in self._packing_list:
            choices_list.append(f'{self._packing_list[i]}')
        main_choices = ["Add New Item", "Packing Menu", "View Packing List", "Main Menu"]
        choices_list = choices_list + main_choices
        # return the choices available to update
        return choices_list, main_choices

    def update_packing_item(self, item):
        """Update specified packing item"""
        print(f'Updating Activity {item}: {self._packing_list[int(item)]}...')
        item_name = 'Updated Item Name: '
        item_quantity = 'Updated Item Quantity: '
        new_name = self.get_user_input(item_name)
        new_quantity = self.get_user_input(item_quantity)
        self._packing_list[int(item)] = [new_name, new_quantity]

    def get_packing_item_counter(self):
        """Gets the item number (count) in packing list"""
        # if there are items in the list then get the latest count
        if self._packing_list:
            keys = self._packing_list.keys()
            key_list = []
            for key in keys:
                key_list.append(key)
            item_counter = int(key_list[-1]) + 1
        # there are no items so the count is zero
        else:
            item_counter = 0
        return item_counter

    def add_new_packing_item(self):
        """Add a new packing item to existing list"""
        # get the item count
        item_counter = self.get_packing_item_counter()
        continue_flag = True
        # continue to prompt user to add items to existing packing list
        while continue_flag is True:
            item_counter += 1
            item_name = input(f'{shellColors.BLUE}{item_counter}) Item name: ')
            item_quantity = input(f'{shellColors.BLUE}{item_counter}) Item quantity: ')
            self._packing_list[item_counter] = [item_name, item_quantity]
            # ask if user wants to continue inputting an item
            continue_input = self.continue_input()
            if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                continue_flag = True
            else:
                continue_flag = False

    def update_packing_list_nav(self):
        """Update packing list nav"""
        choices_list, main_choices = self.create_packing_update_choices()
        print('\nWhat item would you like to update')
        user_input = self.get_user_choice(choices_list)
        # if the user choose to update a specific item then update it
        if int(user_input) <= (len(choices_list) - len(main_choices)):
            self.update_packing_item(user_input)
            self.packing_nav()
        elif user_input == str(len(choices_list) - 3):
            self.add_new_packing_item()
            self.packing_nav()
        elif user_input == str(len(choices_list) - 2):
            self.packing_nav()
        elif user_input == str(len(choices_list) - 1):
            self.display_packing_list()
            self.packing_nav()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def delete_all_packing_items(self):
        """Deletes all packing list items"""
        # store formatting and display warning
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        self.display_delete_warning()
        user_input = input(
            f'{red}Do you want to delete all packing items{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        # if user wants to delete then delete the stored information
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._packing_list = {}

    def delete_packing_nav(self):
        """Delete packing list"""
        # display warning message to user and ask if they want to delete all items
        self.display_delete_warning()
        user_input = self.get_user_choice(["Delete All", "Packing Menu", "Main Menu", "Quit"])
        # either delete the packing list or go to the section
        if user_input == "1":
            self.packing_nav()
        elif user_input == "2":
            self.packing_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    def display_packing_table_headers(self):
        """Display table headers for packing list"""
        # display column headers
        bold, underline, end_color = shellColors.BOLD, shellColors.UNDERLINE, shellColors.ENDCOLOR
        green, space = shellColors.GREEN, '    '
        column_size = "{:<10} {:<10} {:<10}"
        # display headers
        print(column_size.format(
            f'{green}{bold}Item #',
            f'{space}{green}{bold}Item',
            f'{space}{green}{bold}Quantity{end_color}'
        ))

    def display_packing_table_rows(self):
        """Display packing table rows"""
        # display each packing item
        column_size = "{:<10} {:<10} {:<10}"
        for key, value in self._packing_list.items():
            item, quantity = value
            print(column_size.format(f'{key}', f'{item}', f'{quantity}'))

    def display_packing_list(self):
        """Display packing list"""
        # store formatting
        bold, underline, end_color = shellColors.BOLD, shellColors.UNDERLINE, shellColors.ENDCOLOR
        print(f'\n{bold}{underline}Packing List:{end_color}')
        # if there are items in the packing list then display a table
        if self._packing_list:
            self.display_packing_table_headers()
            self.display_packing_table_rows()
        # else the packing list is empty so display message to user
        else:
            self.display_warning('Your packing list is empty.')

    #### PACKING LIST END ####

    #### BUDGET SECTION START ####

    def display_budget_title(self):
        """Displays the budget section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.BDGNAME)
        print(Format.LINEBLU)

    def budget_nav_choices(self):
        """Return a list of all the features of the application that a user can navigate to from budget menu"""
        # return list of choices available in budget nav
        choices = ["Create Budget",
                   "Update Budget",
                   "Delete Budget",
                   "View Budget",
                   "Convert Budget to FX",
                   "Main Menu",
                   "Quit"]
        return choices

    def budget_nav(self):
        """Display the budget nav"""
        self.display_budget_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(self.budget_nav_choices())
        print('')
        # go to the section based on user choice
        if user_input == "1":
            self.create_new_budget()
        elif user_input == "2":
            self.update_budget_nav()
        elif user_input == "3":
            self.delete_budget_nav()
        elif user_input == "4":
            self.display_budget()
            self.budget_nav()
        elif user_input == "5":
            self.convert_budget_to_fx()
        elif user_input == "6":
            self.main_menu_nav()
        elif user_input == "7":
            self.quit_process()

    def add_new_budget_item(self):
        """Adds a new budget item to the budget"""
        # continue asking user for budget item until user is done adding
        item_counter = self.get_budget_item_counter()
        continue_flag = True
        # continue to ask user to enter budget item until user stops
        while continue_flag is True:
            item_counter += 1
            spend_name = input(f'{shellColors.BLUE}{item_counter}) Spend name: ')
            spend_amount = input(f'{shellColors.BLUE}{item_counter}) Spend amount: ')
            self._travel_budget[item_counter] = [spend_name, spend_amount]
            # ask if the user wants to provide another budget item
            continue_input = self.continue_input()
            if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                continue_flag = True
            else:
                continue_flag = False

    def prompt_view_budget(self):
        """Prompts user if they want to view budget and displays the budget if so"""
        prompt = f'Would you like to view the budget? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_budget()
        self.budget_nav()

    def create_new_budget(self):
        """Create a new budget"""
        prompt = 'Would you like to create a budget? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        # if user wants to create a new budget then create a new budget by prompting them for details
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            # prompt user for target budget
            target_budget = self.get_user_input('What is your total budget?')
            self._target_budget = target_budget
            self.add_new_budget_item()
        print('')
        # ask if the user wants to view the budget
        self.prompt_view_budget()

    def create_budget_update_choices(self):
        """Creates the menu of activities and the main choices for updating a budget item"""
        choices_list = []
        # go through each item in the budget to get assign a number for a choice
        for i in self._travel_budget:
            choices_list.append(f'{self._travel_budget[i]}')
        main_choices = ["Add New Budget Item", "Budget Menu", "View Budget", "Main Menu"]
        choices_list = choices_list + main_choices
        return choices_list, main_choices

    def update_budget_item(self, item):
        """Update specified budget item"""
        print(f'Updating Budget {item}: {self._travel_budget[int(item)]}...')
        item_name = 'Updated Spend Name: '
        item_spend = 'Updated Spend Amount: '
        new_name = self.get_user_input(item_name)
        new_spend = self.get_user_input(item_spend)
        self._travel_budget[int(item)] = [new_name, new_spend]

    def get_budget_item_counter(self):
        """Gets the item number (count) in budget"""
        # if there are items in the budget then assign numbers for choices
        if self._travel_budget:
            keys = self._travel_budget.keys()
            key_list = []
            for key in keys:
                key_list.append(key)
            item_counter = int(key_list[-1]) + 1
        # else the budget is empty
        else:
            item_counter = 0
        return item_counter

    def update_budget_nav(self):
        """Update budget navigation"""
        # get the list of choices of budget items available to update
        choices_list, main_choices = self.create_budget_update_choices()
        # ask the user what they would like to update
        print('\nWhat item would you like to update')
        user_input = self.get_user_choice(choices_list)
        # if user selected specific item then udpate it else go to the section
        if int(user_input) <= (len(choices_list) - len(main_choices)):
            self.update_budget_item(user_input)
            self.budget_nav()
        elif user_input == str(len(choices_list) - 3):
            self.add_new_budget_item()
            self.budget_nav()
        elif user_input == str(len(choices_list) - 2):
            self.budget_nav()
        elif user_input == str(len(choices_list) - 1):
            self.display_budget()
            self.budget_nav()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def delete_budget(self):
        """Deletes the budget"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        self.display_delete_warning()
        # ask if user wants to delete and if so then delete
        user_input = input(
            f'{red}Do you want to delete all budget items{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        # if user input yes then delete the budget
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._target_budget = None
            self._travel_budget = {}

    def delete_budget_nav(self):
        """Delete budget"""
        # display delete warning and asks if user wants to delete
        self.display_delete_warning()
        user_input = self.get_user_choice(["Delete All", "Budget Menu", "Main Menu", "Quit"])
        # if user chooses to delete then delete the budget
        if user_input == "1":
            self.budget_nav()
        elif user_input == "2":
            self.budget_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    def display_budget_target(self):
        """Display the provided target budget and fx if applied"""
        print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Budget:{shellColors.ENDCOLOR}')
        # show if the currency pair if it has been specified for the budget
        if self._currency_pair['Base'] != 'None':
            user_ccy = self._currency_pair['Base']
            print(f'Target Budget {self._currency_pair["Quote"]}: {self._target_budget_converted}')
        else:
            user_ccy = ''
        return user_ccy

    def display_budget_over_under(self, user_ccy):
        """Calculate and display the over under of the calculated input budget of items vs input target"""
        # store formats and get total calculated spend based on user input items
        red, green, bold, end_color = shellColors.RED, shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        calc_total = self.calculate_total_spend()
        print(f'Target Budget {user_ccy}: {self._target_budget} vs Calculated Total: {calc_total}')
        # if a target budget has been specified then display it
        if self._target_budget is not None:
            if int(calc_total) <= int(self._target_budget):
                print(f'You are under budget by {green}{bold}{int(self._target_budget) - int(calc_total)}{end_color}')
            else:
                print(f'You are over budget by {red}{bold}{int(self._target_budget) - int(calc_total)}{end_color}')
        print('')

    def display_budget_table_headers(self):
        """Display budget table headers"""
        # store formats
        green, bold, end_color = shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        column_headers = '{:<10} {:<10} {:<10}'
        # Print the names of the columns.
        print(column_headers.format(
            f'{green}{bold}Category{end_color}',
            f'  {green}{bold}Amount{end_color}',
            f'  {green}{bold}FX ({self._currency_pair["Quote"]}){end_color}'))

    def display_budget_table_rows(self):
        """Display the table data rows of budget items"""
        # iterate through the budget and display the items
        for key, value in self._travel_budget.items():
            category, spend = value
            if self._target_budget_converted is None:
                fx_amt = None
            else:
                fx_amt = self._travel_budget_converted[key][1]
            print("{:<10} {:<10} {:<10}".format(f'{category}', f'{spend}', f'{fx_amt}'))

    def display_budget(self):
        """Display the budget"""
        # display the target
        user_ccy = self.display_budget_target()
        # get calculated total and show if the budget is over or under the target
        self.display_budget_over_under(user_ccy)
        print('')
        # if there is a target budget then display all the budget line items
        if self._target_budget:
            self.display_budget_table_headers()
            self.display_budget_table_rows()
        # otherwise the budget is empty
        else:
            self.display_warning('Your budget is empty.')

    def calculate_total_spend(self):
        """Calculate total provided user input for budget"""
        total = 0
        # iterate through the budget and increment the total accordingly
        if self._travel_budget:
            keys = self._travel_budget.keys()
            for key in keys:
                total += int(self._travel_budget[key][1])
        return total

    #### BUDGET SECTION END ####

    #### IMPORTANT CONTACTS SECTION START ####

    def display_contacts_title(self):
        """Displays contacts section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.CONNAME)
        print(Format.LINEBLU)

    def contacts_nav_choices(self):
        """Return a list of all the features of the application that a user can navigate to from contacts menu"""
        # return list of choices available in contacts nav
        choices = ["Add Contacts",
                   "Update Contacts",
                   "Delete Contacts",
                   "View Contacts",
                   "Main Menu",
                   "Quit"]
        return choices

    def contacts_nav(self):
        """Display the contacts nav"""
        # display the section title
        self.display_contacts_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(self.contacts_nav_choices())
        print('')
        # go the section
        if user_input == "1":
            self.create_new_contact()
        elif user_input == "2":
            self.update_contact()
        elif user_input == "3":
            self.delete_contact_nav()
        elif user_input == "4":
            self.display_contacts()
            self.contacts_nav()
        elif user_input == "5":
            self.main_menu_nav()
        elif user_input == "6":
            self.quit_process()

    def add_new_contact_item(self):
        """Adds a new contact item to the list with details input by user"""
        continue_flag = True
        contact_counter = self.get_contact_item_counter()
        # continue to ask for user input until user stops
        while continue_flag is True:
            contact_counter += 1
            name = input(f'{shellColors.BLUE}{contact_counter}) Contact Name: ')
            phone_number = input(f'{shellColors.BLUE}{contact_counter}) Contact Phone Number: ')
            email = input(f'{shellColors.BLUE}{contact_counter}) Contact Email: ')
            notes = input(f'{shellColors.BLUE}{contact_counter}) Notes: ')
            self._contacts[contact_counter] = [name, phone_number, email, notes]
            # ask if user wants to add a new contact item
            continue_input = self.continue_input()
            if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
                continue_flag = True
            else:
                continue_flag = False

    def prompt_view_contacts(self):
        """Prompts user if they want to view contacts and displays contacts if so"""
        # ask user if they would like to view the contacts
        prompt = f'Would you like to view the contacts? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_contacts()
        self.contacts_nav()

    def create_new_contact(self):
        """Creates a new contact list"""
        # prompt user
        prompt = 'Would you like to add a contact? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        self.check_quit(user_input)
        # if user wants to add a contact then add a new contact with user provided detials
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            self.add_new_contact_item()
        print('')
        # ask if user wants to view contacts
        self.prompt_view_contacts()

    def display_contacts_table_headers(self):
        """Display contacts table headers"""
        # store formats
        green, bold, end_color = shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        column_headers = '{:<10} {:<10} {:<10} {:<10}'
        # display the column headers
        print(column_headers.format(f'{green}{bold}Name{end_color}',
                                    f'    {green}{bold}Phone{end_color}',
                                    f'      {green}{bold}Email{end_color}',
                                    f'      {green}{bold}Notes{end_color}'))

    def display_contacts_table_rows(self):
        """Display contacts table rows"""
        # display the contact detail rows
        for key, value in self._contacts.items():
            name, phone, email, notes = value
            print("{:<10} {:<10} {:<10} {:<10}".format(f'{name}', f'{phone}', f'{email}', f'{notes}'))

    def display_contacts(self):
        """Display contacts list"""
        print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Contacts:{shellColors.ENDCOLOR}')
        # display the contacts if any otherwise notify user
        if self._contacts:
            # Print the names of the columns.
            self.display_contacts_table_headers()
            # print each data item.
            self.display_contacts_table_rows()
        else:
            self.display_warning('Your contact list is empty.')

    def create_contacts_update_choices(self):
        """Creates the menu of activities and the main choices for updating a budget item"""
        choices_list = []
        # go through each item in the contacts list to assign a number for a choice
        for i in self._contacts:
            choices_list.append(f'{self._contacts[i]}')
        main_choices = ["Add New Contact", "Contacts Menu", "View Contacts", "Main Menu"]
        choices_list = choices_list + main_choices
        return choices_list, main_choices

    def update_contact_item(self, item):
        """Update specified contact item"""
        print(f'Updating Contact {item}: {self._contacts[int(item)]}...')
        name = 'Updated Name: '
        phone = 'Updated Phone: '
        email = 'Updated Email: '
        notes = 'Updated Notes: '
        new_name = self.get_user_input(name)
        new_phone = self.get_user_input(phone)
        new_email = self.get_user_input(email)
        new_notes = self.get_user_input(notes)
        self._contacts[int(item)] = [new_name, new_phone, new_email, new_notes]

    def get_contact_item_counter(self):
        """Gets the item number (count) in budget"""
        # if there are items in the contacts then assign numbers for choices
        if self._contacts:
            keys = self._contacts.keys()
            key_list = []
            for key in keys:
                key_list.append(key)
            item_counter = int(key_list[-1]) + 1
        # else the contacts list is empty
        else:
            item_counter = 0
        return item_counter

    def update_contact(self):
        """Update packing list nav"""
        print('\nWhat item would you like to update')
        # get the available contacts to udpate
        choices_list, main_choices = self.create_contacts_update_choices()
        user_input = self.get_user_choice(choices_list)
        # update the specified contact
        if int(user_input) <= (len(choices_list) - len(main_choices)):
            self.update_contact_item(user_input)
            self.contacts_nav()
        elif user_input == str(len(choices_list) - 3):
            self.add_new_contact_item()
            self.contacts_nav()
        elif user_input == str(len(choices_list) - 2):
            self.contacts_nav()
        elif user_input == str(len(choices_list) - 1):
            self.display_contacts()
            self.contacts_nav()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def delete_contacts(self):
        """Deletes contacts list"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        # display warning and delete if user wants to proceed
        self.display_delete_warning()
        user_input = input(
            f'{red}Are you sure you want to delete all contacts{end_color}? Type {bold}{red}"yes" or "y": {end_color}')
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._contacts = {}

    def delete_contact_nav(self):
        """Delete contact list"""
        # display delete warning to user
        self.display_delete_warning()
        user_input = self.get_user_choice(["Delete All", "Contacts Menu", "Main Menu", "Quit"])
        # if user wants to delete then delete contact list
        if user_input == "1":
            self.delete_contacts()
            self.contacts_nav()
        elif user_input == "2":
            self.contacts_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    #### CONTACTS SECTION END ####

    #### TRAVEL TIPS SECTION START ####

    def display_travel_tips_title(self):
        """Displays contacts section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEPUR)
        print(Format.TIPNAME)
        print(Format.LINEPUR)

    def display_travel_tips_list_items(self):
        """Displays the list of travel tip items"""
        # store a list of tips
        tips_list = [
            "1) Carry emergency contact information.",
            "2) Call ahead for reservations.",
            "3) Research local transportation options.",
            "4) Keep your friends and family updated.",
            "5) Make copies of important documents.",
        ]
        print('')
        # display each tip
        for tip in tips_list:
            print(f'{shellColors.BOLD}{shellColors.PURPLE}{tip}{shellColors.ENDCOLOR}')

    def prompt_user_international_travel(self):
        """Ask if user is traveling internationally to provide helpful related information"""
        # ask the user
        purple, blue, bold, end_color = shellColors.PURPLE, shellColors.BLUE, shellColors.BOLD, shellColors.ENDCOLOR
        response = input(f'{blue} Are you travelling abroad? Type {bold}"yes" or "y"{end_color}: ')
        # if the user is going international provide helpful link
        if str.lower(response) == "yes" or str.lower(response) == "y":
            print('')
            resource = 'https://www.state.gov/travelers/'
            print(f'{bold}{purple}Recommended Resource: {end_color}')
            print(f'{purple}{resource}{end_color}')
            print(f'{purple}Check that your passport is valid!{end_color}')

    def display_travel_tips(self):
        """Display travel tips section"""
        # display the section title and the tips list
        self.display_travel_tips_title()
        self.display_travel_tips_list_items()
        print('')
        # ask if user is traveling internationally
        self.prompt_user_international_travel()
        # go back to the main menu
        self.main_menu_nav()

    #### TRAVEL PLANNER ####

    def display_travel_planner_title(self):
        """Displays travel planner section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.PLRNAME)
        print(Format.LINEBLU)

    def planner_nav(self):
        """Display the travel planner"""
        # display section title and ask user if they would like to view the planner
        self.display_travel_planner_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(["View Planner", "Main Menu", "Quit"])
        print('')
        # display the planner if the user wants to view it otherwise go to main menu or quit depending on choice
        if user_input == "1":
            self.display_planner()
        elif user_input == "2":
            self.main_menu_nav()
        elif user_input == "3":
            self.quit_process()

    def display_planner(self):
        """Display the Travel Planner"""
        print(Format.LINE)
        self.display_itinerary()
        print('')
        self.display_packing_list()
        print('')
        self.display_budget()
        print('')
        self.display_contacts()
        print(Format.LINE)
        self.planner_nav()

# start process
travel_planner = TravelPlanner()
travel_planner.start_process()