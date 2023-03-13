from format import *
import csv
import time


class TravelPlanner:
    """Represents the travel planner application"""

    def __init__(self) -> None:
        """Initialize attributes for storing data provided by user"""
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

    def check_valid_budget(self):
        """Checks if the budget is valid (not empty), if valid then request the fx pair"""
        # if a budget hasn't yet been specified then go back to nav, else get from/to currency from user
        if not self._travel_budget:
            self.display_warning('The budget is currently empty! Please create a budget first.')
            self.budget_nav()
        else:
            self.get_currency_pair()

    def convert_budget_to_fx_nav(self):
        """Convert the budget to FX with Microservice navigation menu"""
        # get user input choice, convert the budget to FX or go to other menus based on user choice
        user_input = self.get_user_choice(["Convert Budget to FX", "Budget Menu", "Main Menu", "Quit"])
        if user_input == "1":
            self.check_valid_budget()
        elif user_input == "2":
            self.budget_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    def get_currency_pair(self):
        """Get the currency pair from user input to request fx conversion from microservice"""
        from_ccy = input(f'{shellColors.BLUE} From Currency: ')
        to_ccy = input(f'{shellColors.BLUE} To Currency: ')
        self._currency_pair['Base'] = from_ccy
        self._currency_pair['Quote'] = to_ccy
        # request the fx from microservice based on provided currency pair
        self.request_fx(str(from_ccy + to_ccy))

    def request_fx(self, pair):
        """Provide the currency pair to microservice (comm pipe) to request fx rates for provided pair"""
        pair_amt = [pair, self._target_budget]
        # call the functions to write, request and read from the Microservice communication pipe files
        self.write_to_fx_request_file(pair_amt)
        self.run_fx_request()
        self.read_from_fx_converted_file()
        # update the budget amounts with the fx received
        self.update_budget_with_converted_fx()

    def write_to_fx_request_file(self, pair_amt):
        """Write to the FX request file the fx pair and amount for Microservice to convert"""
        with open('./CurrencyMS/fx_request.csv', 'w') as fx_req_file:
            writer = csv.writer(fx_req_file)
            writer.writerow(pair_amt)

    def run_fx_request(self):
        """Write to the FX run text file 'RUN' so Microservice can check communication pipeline"""
        with open('./CurrencyMS/fx_run.txt', 'w') as req_file:
            req_file.write('RUN')
        # display message to the user that the service is running and wait for it to complete
        self.display_warning('Microservice is fetching rates and performing calculations...')
        time.sleep(10)

    def read_from_fx_converted_file(self):
        """Read the converted fx from the fx converted file that Microservice provided"""
        with open('./CurrencyMS/fx_converted.csv', 'r') as fx_rec_file:
            datareader = csv.reader(fx_rec_file)
            # convert to float to be used in the application and set the fx rate & update the amount with the fx
            converted_amount = next(datareader)
            converted_amount = float(converted_amount[0])
            self._fx_rate = converted_amount / float(self._target_budget)
            self._target_budget_converted = converted_amount

    def update_budget_with_converted_fx(self):
        """Update all budget items with the FX conversion for target that was provided by Microservice"""
        # apply the received fx rate from the microservice to all items in the budget then go back to nav
        for key in self._travel_budget:
            self.apply_fx_rate(key)
        self.display_warning('Conversions Completed!')
        self.budget_nav()

    def apply_fx_rate(self, key):
        """Apply the fx rate and conversion from Microservice to the specified budget item"""
        category = self._travel_budget[key][0]
        amount = float(self._travel_budget[key][1])
        amt_fx = round(amount * self._fx_rate, 2)
        amt_fx = str(amt_fx)
        self._travel_budget_converted[key] = [category, amt_fx]

    ### INTERACTION WITH MICROSERVICE END ###

    ### GENERAL SETUP AND MAIN APPLICATION NAVIGATION ###

    def generate_input_choices_main_nav(self, choices):
        """Generates the list of choices to display in numbered order"""
        # create the options a user can choose based on the provided choices and return the list
        index_list = []
        for index, choice in enumerate(choices):
            index_list.append(str(index + 1))
            print(f'{index + 1}: {choice}')
        return index_list

    def get_user_choice(self, choices):
        """Gets and returns the users choice from a provided list of choices"""
        index_list = self.generate_input_choices_main_nav(choices)
        # keep checking for valid input
        while True:
            # get the user input and first see if they typed quit
            user_input = input(f'{shellColors.BLUE}Please Enter The Number: {shellColors.ENDCOLOR}')
            self.check_quit(user_input)
            # if the user input is invalid notify until a valid input is received
            if user_input not in index_list:
                self.display_incorrect_choice_msg(len(choices))
                continue
            return user_input

    def get_user_input(self, prompt):
        """Gets and returns input from user based on provided prompt"""
        answer = input(f'{shellColors.BLUE}{prompt}: {shellColors.ENDCOLOR}')
        self.check_quit(answer)
        return answer

    def continue_input(self):
        """Asks if the user would like to add another item (i.e. continue by inputting another item)"""
        # variables to store bash colors and input prompt, get use input and return it
        blue, bold, end_color = shellColors.BLUE, shellColors.BOLD, shellColors.ENDCOLOR
        continue_input = input(
            f'{blue} Would you like to add another? Type {bold}"yes" or "y"{end_color}: '
        )
        self.check_quit(continue_input)
        return continue_input

    def update_continue_input_flag(self, continue_input):
        """Update and return input flag depending on if user chose to continue providing input or not"""
        # if the user wants to continue the input then flag is still false
        if str.lower(continue_input) == "yes" or str.lower(continue_input) == "y":
            continue_flag = True
        else:
            continue_flag = False
        return continue_flag

    def display_incorrect_choice_msg(self, len_choices):
        """Display an error/warning message that the input should be within the provided choice range"""
        # assign variables to store bash color info, display message to user choice should be in range
        yellow, bold, end_color = shellColors.YELLOW, shellColors.BOLD, shellColors.ENDCOLOR
        print(f'{yellow}Sorry, your answer should be between {bold}{1} and {len_choices}{end_color}')

    def check_quit(self, input):
        """Checks if the user typed 'quit' to input"""
        if input.lower() == "quit":
            self.quit_process()

    def quit_process(self):
        """Quits the process"""
        print('Quitting the application, thanks for using the Travel App...Bye!')
        exit()

    def display_intro_msg(self):
        """Display an introductory message to the user"""
        green, end_color = shellColors.GREEN, shellColors.ENDCOLOR
        print(f'{green}|{end_color} Before we start, here are useful features...   {green}|{end_color}')
        print(f'{green}|{end_color}    • Enter the number choice when asked.       {green}|{end_color}')
        print(f'{green}|{end_color}    • Provide as much or as little as you want. {green}|{end_color}')
        print(f'{green}|{end_color}      Dont worry, you can make changes!         {green}|{end_color}')
        print(f'{green}|{end_color}    • Press "enter" to skip Y/N questions.      {green}|{end_color}')
        print(f'{green}|{end_color}    • Type "quit" to any Y/N question to quit.  {green}|{end_color}')

    def display_delete_warning(self):
        """Displays delete warning (red) message that deletions cannot be undone"""
        print(f'{shellColors.RED}Deletions cannot be undone!{shellColors.ENDCOLOR}')

    def display_warning(self, msg):
        """Displays warning message (yellow) of provided message"""
        print(f'{shellColors.YELLOW}{msg}{shellColors.ENDCOLOR}')

    def display_application_title(self):
        """Displays the application title to the user"""
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
        """Return a list of all the features of the application that a user can navigate to from main menu"""
        choices = [
            "Itinerary",
            "Packing List",
            "Budget",
            "Important Contacts",
            "Travel Planner",
            "Travel Tips",
            "Quit"
        ]
        return choices

    def main_menu_nav(self):
        """Display navigation for the main menu - navigates to all features of the application"""
        self.display_application_title()
        # get user choice to take the user to where they would like to go
        print(f'{shellColors.BLUE}Where would you like to go?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(self.main_nav_choices())
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
        """Return a list of all the features of the app that a user can navigate to from itinerary menu"""
        choices = ["Create Itinerary", "Update Itinerary", "Delete Itinerary", "View Itinerary", "Main Menu", "Quit"]
        return choices

    def itinerary_nav(self):
        """Display the itinerary navigation menu"""
        self.display_itinerary_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        # get the user choice and go to the section
        user_input = self.get_user_choice(self.itinerary_nav_choices())
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

    def create_new_itinerary(self):
        """Creates a new itinerary"""
        # call all the setter methods to get the user input and set the trip details
        self.set_trip_name()
        self.set_trip_dates()
        self.set_trip_locations()
        self.set_itinerary()

    def set_trip_dates(self):
        """Sets trip dates"""
        self.set_start_date()
        self.set_end_date()

    def set_trip_locations(self):
        """Sets trip locations"""
        self.set_from_location()
        self.set_to_location()

    def set_trip_name(self) -> None:
        """Sets trip name from user input"""
        prompt = 'What would you like to name this trip?'
        trip_name = self.get_user_input(prompt)
        self._trip_name = trip_name

    def set_start_date(self):
        """Sets start date from user input"""
        prompt = 'When does your trip start?'
        start_date = self.get_user_input(prompt)
        self._start_date = start_date

    def set_end_date(self):
        """Sets end date from user input"""
        prompt = 'When does your trip end?'
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
        """Sets the itinerary activities based on user input - user can enter as many items as desired"""
        continue_flag, activity_counter = True, 0
        # while the user still wants to input activities continue to ask and add the details to the itinerary
        while continue_flag is True:
            activity_counter += 1
            user_activity = input(f'{shellColors.BLUE}{activity_counter}) Activity Description: ')
            self._travel_itinerary[activity_counter] = user_activity
            # ask if the user would like to continue, continue to provide another activity otherwise stop loop
            continue_input = self.continue_input()
            continue_flag = self.update_continue_input_flag(continue_input)

    def prompt_view_itinerary(self):
        """Prompts user asking if the user would like to view the itinerary details"""
        prompt = f'\nWould you like to view the itinerary? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_itinerary()
        self.itinerary_nav()

    def set_itinerary(self):
        """Set and create an itinerary of activities based on user input"""
        prompt = 'Would you like to create an itinerary of activities? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        # if the user wants to provide an itinerary of activities, then continue to ask until they are finished
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            self.set_itinerary_activities()
        # ask if user would like to see the itinerary
        self.prompt_view_itinerary()

    def update_activities_nav_choices(self):
        """Return list of all the features of the app that a user can navigate to from itinerary update menu"""
        choices = ["Update All", "Update Activity", "Itinerary Menu", "View Itinerary", "Main Menu", "Quit"]
        return choices

    def update_activities_nav(self):
        """Update activities navigation menu"""
        print(f'\nWhat activities would you like to {shellColors.YELLOW}update{shellColors.ENDCOLOR}?')
        # go to section based on user input
        user_input = self.get_user_choice(self.update_activities_nav_choices())
        if user_input == "1":
            self.set_itinerary()
        if user_input == "2":
            self.update_selected_activity_nav()
        if user_input == "3":
            self.itinerary_nav()
        if user_input == "4":
            self.display_itinerary()
            self.update_itinerary_nav()
        if user_input == "5":
            self.main_menu_nav()
        if user_input == "6":
            self.quit_process()

    def create_itinerary_update_nav_choices(self):
        """Creates the menu of itinerary activity choices for updating an activity"""
        # create a list of all the current activities to display back to user in numbered order for choosing
        choices_list = []
        for i in self._travel_itinerary:
            choices_list.append(f'{self._travel_itinerary[i]}')
        main_choices = ["Itinerary Menu", "View Itinerary", "Main Menu"]
        choices_list = choices_list + main_choices
        return choices_list, main_choices

    def update_selected_activity(self, user_input):
        """Update the selected activity from user input"""
        print(f'Updating Activity {user_input}: {self._travel_itinerary[int(user_input)]}...')
        prompt = 'Updated Activity: '
        new_description = self.get_user_input(prompt)
        self._travel_itinerary[int(user_input)] = new_description

    def update_selected_activity_nav(self):
        """Update selected activities navigation menu"""
        choices_list, main_choices = self.create_itinerary_update_nav_choices()
        print('\nWhat activity would you like to update?')
        user_input = self.get_user_choice(choices_list)
        # update the corresponding user selected item
        if int(user_input) <= (len(choices_list) - len(main_choices)):
            self.update_selected_activity(user_input)
        elif user_input == str(len(choices_list) - 2):
            self.itinerary_nav()
        elif user_input == str(len(choices_list) - 1):
            self.display_itinerary()
            self.itinerary_nav()
        elif user_input == str(len(choices_list)):
            self.main_menu_nav()

    def update_itinerary_nav_choices(self):
        """Return list of all the features of the application that a user can navigate to from itinerary update menu"""
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

    def update_itinerary_dates(self):
        """Update itinerary dates"""
        self.set_start_date()
        self.set_end_date()
        self.itinerary_nav()

    def update_itinerary_locations(self):
        """Update itinerary locations"""
        self.set_from_location()
        self.set_to_location()
        self.itinerary_nav()

    def update_itinerary_nav(self):
        """Update itinerary navigation menu"""
        blue, yellow, end_color = shellColors.BLUE, shellColors.YELLOW, shellColors.ENDCOLOR
        print(f'\n{blue}What would you like to {end_color}{yellow}update{end_color}?')
        # get the user input and go to the section
        user_input = self.get_user_choice(self.update_itinerary_nav_choices())
        if user_input == "1":
            self.create_new_itinerary()
        elif user_input == "2":
            self.set_trip_name()
            self.itinerary_nav()
        elif user_input == "3":
            self.update_itinerary_dates()
        elif user_input == "4":
            self.update_itinerary_locations()
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
        """Return list of all features of the application that a user can navigate to from itinerary delete menu"""
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
        """Delete itinerary navigation menu"""
        print(f'What would you like to {shellColors.RED}delete?{shellColors.ENDCOLOR}')
        # display warning that deletions cannot be undone, make change or go to section based on user input
        user_input = self.get_user_choice(self.itinerary_delete_nav_choices())
        if user_input == "1":
            self.delete_all_itinerary_items()
        elif user_input == "2":
            self.delete_trip_name()
        elif user_input == "3":
            self.delete_dates()
        elif user_input == "4":
            self.delete_locations()
        elif user_input == "5":
            self.delete_activities()
        elif user_input == "6":
            self.itinerary_nav()
        elif user_input == "7":
            self.display_itinerary()
        elif user_input == "8":
            self.main_menu_nav()
        elif user_input == "9":
            self.quit_process()

    def delete_all_itinerary_items(self):
        """Deletes all itinerary details and activities if user chooses yes"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete all fields{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._trip_name = None
            self._start_date = None
            self._end_date = None
            self._from_location = None
            self._to_location = None
            self._travel_itinerary = {}
            self.display_warning("All items deleted.")
        self.itinerary_nav()

    def delete_trip_name(self):
        """Deletes the trip name if user chooses yes"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the trip name?{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._trip_name = None
            self.display_warning("Trip name deleted.")
        self.itinerary_nav()

    def delete_dates(self):
        """Deletes the dates of the trip if user chooses yes"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the dates{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._start_date = None
            self._end_date = None
            self.display_warning("Dates deleted.")
        self.itinerary_nav()

    def delete_locations(self):
        """Deletes the locations of the trip if user chooses yes"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the locations{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._from_location = None
            self._to_location = None
            self.display_warning("Locations deleted.")
        self.itinerary_nav()

    def delete_activities(self):
        """Deletes all the activities of the trip if user chooses yes"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        user_input = input(
            f'{red}Are you sure you want to delete the activities{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._travel_itinerary = {}
            self.display_warning("Itinerary of activities deleted.")
        self.itinerary_nav()

    def display_a_to_b(self, a, msg, b):
        """Display provided message in the format of 'a' to 'b'"""
        green, bold, end_color = shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        print(f'{bold}{msg}{end_color} {green}{a}{end_color} {bold}to{end_color} {green}{b}{end_color}')

    def display_trip_details(self):
        """Displays trip name, dates and location details"""
        # store formatting
        green, bold, end_color = shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        print('')
        print(f'{bold}Trip Name{end_color}: {green}{self._trip_name}{end_color}')
        self.display_a_to_b(self._start_date, 'Leaving', self._end_date)
        self.display_a_to_b(self._from_location, 'From', self._to_location)

    def display_itinerary_activities(self):
        """Displays the list of itinerary activities"""
        # if there is an activity then display it otherwise notify user there are no activities
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
        """Packing navigation menu"""
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

    def prompt_view_packing_list(self):
        """Prompts user asking if the user would like to view the packing list"""
        prompt = f'\nWould you like to view the packing list? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_packing_list()
        self.packing_nav()

    def create_new_packing_list(self):
        """Creates new packing list to add new items if user chooses yes"""
        prompt = 'Would you like to create a packing list? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        # if the user wants to create a packing list then continue to prompt for packing items until user is done
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            self.add_new_packing_item()
        # asks if user wants to view packing list
        self.prompt_view_packing_list()

    def create_packing_update_choices(self):
        """Creates and returns the menu of choices for updating a packing item"""
        choices_list = []
        # go through each packing item and add it to the list so user can specify which item to update
        for i in self._packing_list:
            choices_list.append(f'{self._packing_list[i]}')
        main_choices = ["Add New Item", "Packing Menu", "View Packing List", "Main Menu"]
        choices_list = choices_list + main_choices
        return choices_list, main_choices

    def update_packing_item(self, item):
        """Update specified packing item with new user input details"""
        print(f'Updating Activity {item}: {self._packing_list[int(item)]}...')
        item_name = 'Updated Item Name: '
        item_quantity = 'Updated Item Quantity: '
        new_name = self.get_user_input(item_name)
        new_quantity = self.get_user_input(item_quantity)
        self._packing_list[int(item)] = [new_name, new_quantity]

    def get_packing_item_counter(self):
        """Gets the item number (count) in packing list"""
        # if there are items in the list then get the latest count of items to display numbered order for user
        item_counter = 0
        if self._packing_list:
            keys = self._packing_list.keys()
            key_list = []
            for key in keys:
                key_list.append(key)
            item_counter = int(key_list[-1])
        return item_counter

    def add_new_packing_item(self):
        """Add a new packing item to the packing list while user wants to continue adding items"""
        continue_flag, item_counter = True, self.get_packing_item_counter()
        # continue to prompt user to add items to existing packing list
        while continue_flag is True:
            item_counter += 1
            self.set_packing_item_details(item_counter)
            # ask if user wants to continue inputting an item
            continue_input = self.continue_input()
            continue_flag = self.update_continue_input_flag(continue_input)

    def set_packing_item_details(self, item_counter):
        """Sets the item name and quantity in the packing list from user input"""
        item_name = input(f'{shellColors.BLUE}{item_counter}) Item name: ')
        item_quantity = input(f'{shellColors.BLUE}{item_counter}) Item quantity: ')
        self._packing_list[item_counter] = [item_name, item_quantity]

    def update_packing_list_nav(self):
        """Update packing list navigation menu"""
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
        """Deletes all packing list items if user chooses yes"""
        # store formatting and display warning
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        self.display_delete_warning()
        user_input = input(
            f'{red}Do you want to delete all packing items{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._packing_list = {}
            self.display_warning("Packing List deleted.")
        self.packing_nav()

    def delete_packing_nav(self):
        """Delete packing list navigation menu"""
        # display warning message to user, either delete the packing list or go to section
        self.display_delete_warning()
        user_input = self.get_user_choice(["Delete All", "Packing Menu", "Main Menu", "Quit"])
        if user_input == "1":
            self.delete_all_packing_items()
        elif user_input == "2":
            self.packing_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    def display_packing_table_headers(self):
        """Display table headers for packing list"""
        # store formatting then display the headers
        bold, underline, end_color = shellColors.BOLD, shellColors.UNDERLINE, shellColors.ENDCOLOR
        green, space, column_size = shellColors.GREEN, '    ', "{:<10} {:<10} {:<10}"
        print(column_size.format(
            f'{green}{bold}Item #',
            f'{space}{green}{bold}Item',
            f'{space}{green}{bold}Quantity{end_color}'
        ))

    def display_packing_table_rows(self):
        """Display packing table data rows (items and associated quantities)"""
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
        # if there are items in the packing list then display a table, else it's empty so notify user
        if self._packing_list:
            self.display_packing_table_headers()
            self.display_packing_table_rows()
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
        """Return a list of all the features of the app that a user can navigate to from budget menu"""
        choices = ["Create Budget",
                   "Update Budget",
                   "Delete Budget",
                   "View Budget",
                   "Convert Budget to FX",
                   "Main Menu",
                   "Quit"]
        return choices

    def budget_nav(self):
        """Display the budget navigation menu"""
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
            self.convert_budget_to_fx_nav()
        elif user_input == "6":
            self.main_menu_nav()
        elif user_input == "7":
            self.quit_process()

    def add_new_budget_item(self):
        """Adds a new budget item to the budget by allowing a user to add as many as they choose"""
        continue_flag, item_counter = True, self.get_budget_item_counter()
        # continue to ask user to enter budget item until user stops and add to the budget
        while continue_flag is True:
            item_counter += 1
            self.set_budget_details(item_counter)
            # ask if the user wants to provide another budget item
            continue_input = self.continue_input()
            continue_flag = self.update_continue_input_flag(continue_input)

    def set_budget_details(self, item_counter):
        """Sets the spend name and amount in the budget from user input"""
        spend_name = input(f'{shellColors.BLUE}{item_counter}) Spend name: ')
        spend_amount = input(f'{shellColors.BLUE}{item_counter}) Spend amount: ')
        self._travel_budget[item_counter] = [spend_name, spend_amount]

    def set_target_budget(self):
        """Sets the target budget from user input"""
        target_budget = self.get_user_input('What is your total budget?')
        self._target_budget = target_budget

    def prompt_view_budget(self):
        """Prompts user if they want to view budget and displays the budget if so"""
        prompt = f'Would you like to view the budget? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_budget()
        self.budget_nav()

    def create_new_budget(self):
        """Asks user if they would like to create a new budget"""
        prompt = 'Would you like to create a budget? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        # if user wants to create a new budget then create a new budget by prompting them for details
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            self.set_target_budget()
            self.add_new_budget_item()
        print('')
        # ask if the user wants to view the budget
        self.prompt_view_budget()

    def create_budget_update_nav_choices(self):
        """Creates the menu of budget items and the main choices for updating a budget item"""
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
        # if there are items in the budget then assign numbers for choices to display
        item_counter = 0
        if self._travel_budget:
            keys = self._travel_budget.keys()
            key_list = []
            for key in keys:
                key_list.append(key)
            item_counter = int(key_list[-1]) + 1
        return item_counter

    def update_budget_nav(self):
        """Update budget navigation menu"""
        choices_list, main_choices = self.create_budget_update_nav_choices()
        # ask the user what they would like to update from the choices list
        print('\nWhat item would you like to update')
        user_input = self.get_user_choice(choices_list)
        # if user selected specific item then update it else go to the section
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
        """Delete the budget if a user chooses yes"""
        # store formatting
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        self.display_delete_warning()
        user_input = input(
            f'{red}Do you want to delete all budget items{end_color}? Type {bold}{red}"yes" or "y": {end_color}'
        )
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._target_budget = None
            self._travel_budget = {}
            self.display_warning("Packing List deleted.")
        self.budget_nav()

    def delete_budget_nav(self):
        """Delete budget navigation menu"""
        # display delete warning and then delete or navigate to section depending on user input
        self.display_delete_warning()
        user_input = self.get_user_choice(["Delete All", "Budget Menu", "Main Menu", "Quit"])
        if user_input == "1":
            self.delete_budget()
        elif user_input == "2":
            self.budget_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    def display_budget_target(self):
        """Display the provided target budget and fx from Microservice if applied"""
        print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Budget:{shellColors.ENDCOLOR}')
        # show if the currency pair if it has been specified for the budget
        if self._currency_pair['Base'] != 'None':
            user_ccy = self._currency_pair['Base']
            print(f'Target Budget {self._currency_pair["Quote"]}: {self._target_budget_converted}')
        else:
            user_ccy = ''
        return user_ccy

    def budget_vs_target(self, user_ccy):
        """Get calculated budget total to display the provided items calculated total vs input target"""
        # get the calculated total spend from provided input
        calc_total = self.calculate_total_spend()
        print(f'Target Budget {user_ccy}: {self._target_budget} vs Calculated Total: {calc_total}')
        # if a target budget has been specified then display the calculated total vs the target
        if self._target_budget is not None:
            self.display_over_under_budget(calc_total)
        print('')

    def display_over_under_budget(self, calc_total):
        """Displays the formatted over or under budget calculation"""
        # store formats and get total calculated spend based on user input items
        red, green, bold, end_color = shellColors.RED, shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        # display red if over and green if under budget
        if int(calc_total) <= int(self._target_budget):
            print(f'You are under budget by {green}{bold}{int(self._target_budget) - int(calc_total)}{end_color}')
        else:
            print(f'You are over budget by {red}{bold}{int(self._target_budget) - int(calc_total)}{end_color}')

    def calculate_total_spend(self):
        """Calculate total spend of items provided by user input for budget"""
        # iterate through the budget and increment the total accordingly
        total = 0
        if self._travel_budget:
            keys = self._travel_budget.keys()
            for key in keys:
                total += int(self._travel_budget[key][1])
        return total

    def display_budget_table_headers(self):
        """Display budget table headers"""
        # store formats and display the table headers
        green, bold, end_color = shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        column_headers = '{:<10} {:<10} {:<10}'
        print(column_headers.format(
            f'{green}{bold}Category{end_color}',
            f'  {green}{bold}Amount{end_color}',
            f'  {green}{bold}FX ({self._currency_pair["Quote"]}){end_color}'))

    def display_budget_table_rows(self):
        """Display table data rows of budget items"""
        # iterate through the budget and display the items (show fx if requested via Microservice)
        for key, value in self._travel_budget.items():
            category, spend = value
            if self._target_budget_converted is None:
                fx_amt = None
            else:
                fx_amt = self._travel_budget_converted[key][1]
            print("{:<10} {:<10} {:<10}".format(f'{category}', f'{spend}', f'{fx_amt}'))

    def display_budget(self):
        """Display the budget"""
        # display the target and get calculated total to show if the budget is over or under the target
        user_ccy = self.display_budget_target()
        self.budget_vs_target(user_ccy)
        print('')
        # if there is a target budget then display all the budget line items, otherwise notify user it's empty
        if self._target_budget:
            self.display_budget_table_headers()
            self.display_budget_table_rows()
        else:
            self.display_warning('Your budget is empty.')

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
        choices = ["Add Contacts",
                   "Update Contacts",
                   "Delete Contacts",
                   "View Contacts",
                   "Main Menu",
                   "Quit"]
        return choices

    def contacts_nav(self):
        """Display the contacts nav"""
        # display the section title and go to section based on user input
        self.display_contacts_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(self.contacts_nav_choices())
        print('')
        if user_input == "1":
            self.create_new_contact()
        elif user_input == "2":
            self.update_contact_nav()
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
        continue_flag, contact_counter = True, self.get_contact_item_counter()
        # continue to ask for user input until user stops
        while continue_flag is True:
            contact_counter += 1
            self.set_contact(contact_counter)
            # ask if user wants to add a new contact item
            continue_input = self.continue_input()
            continue_flag = self.update_continue_input_flag(continue_input)

    def set_contact(self, contact_counter):
        """Sets user input into contacts information and orders it"""
        name = input(f'{shellColors.BLUE}{contact_counter}) Contact Name: ')
        phone_number = input(f'{shellColors.BLUE}{contact_counter}) Contact Phone Number: ')
        email = input(f'{shellColors.BLUE}{contact_counter}) Contact Email: ')
        notes = input(f'{shellColors.BLUE}{contact_counter}) Notes: ')
        self._contacts[contact_counter] = [name, phone_number, email, notes]

    def prompt_view_contacts(self):
        """Prompts user if they want to view contacts and displays contacts if so"""
        prompt = f'Would you like to view the contacts? Type {shellColors.BOLD}"yes" or "y"{shellColors.ENDCOLOR}'
        user_input = self.get_user_input(prompt)
        if str.lower(user_input) == "yes" or str.lower(user_input) == "y":
            self.display_contacts()
        self.contacts_nav()

    def create_new_contact(self):
        """Asks user if they would like to create a new contact to add to the contact information"""
        prompt = 'Would you like to add a contact? Type "yes" or "y"'
        user_input = self.get_user_input(prompt)
        # if user wants to add a contact then add a new contact with user provided details
        if str.lower(user_input) == "yes" or str.lower(user_input) == str.lower("y"):
            self.add_new_contact_item()
        print('')
        # ask if user wants to view contacts
        self.prompt_view_contacts()

    def display_contacts_table_headers(self):
        """Display contacts table headers"""
        # store formats and display table headers
        green, bold, end_color = shellColors.GREEN, shellColors.BOLD, shellColors.ENDCOLOR
        column_headers = '{:<10} {:<10} {:<10} {:<10}'
        print(column_headers.format(f'{green}{bold}Name{end_color}',
                                    f'    {green}{bold}Phone{end_color}',
                                    f'      {green}{bold}Email{end_color}',
                                    f'      {green}{bold}Notes{end_color}'))

    def display_contacts_table_rows(self):
        """Display contacts table rows"""
        # display the contact detail/data rows
        for key, value in self._contacts.items():
            name, phone, email, notes = value
            print("{:<10} {:<10} {:<10} {:<10}".format(f'{name}', f'{phone}', f'{email}', f'{notes}'))

    def display_contacts(self):
        """Display contacts list"""
        print(f'\n{shellColors.BOLD}{shellColors.UNDERLINE}Contacts:{shellColors.ENDCOLOR}')
        # display the contacts (full table) if any, otherwise notify user it's empty
        if self._contacts:
            self.display_contacts_table_headers()
            self.display_contacts_table_rows()
        else:
            self.display_warning('Your contact list is empty.')

    def create_contacts_update_nav_choices(self):
        """Creates the menu of choices for updating a contact"""
        choices_list = []
        # go through each item in the contacts list to assign a number for a choice
        for i in self._contacts:
            choices_list.append(f'{self._contacts[i]}')
        main_choices = ["Add New Contact", "Contacts Menu", "View Contacts", "Main Menu"]
        choices_list = choices_list + main_choices
        return choices_list, main_choices

    def update_contact_item(self, item):
        """Update specified contact item details"""
        print(f'Updating Contact {item}: {self._contacts[int(item)]}...')
        new_name = self.update_contact_name()
        new_phone = self.update_contact_phone()
        new_email = self.update_contact_email()
        new_notes = self.update_contact_notes()
        self._contacts[int(item)] = [new_name, new_phone, new_email, new_notes]

    def update_contact_name(self):
        """Gets new name from user input for contact name"""
        new_name = self.get_user_input('Updated Name: ')
        return new_name

    def update_contact_phone(self):
        """Gets new phone from user input for contact phone"""
        new_phone = self.get_user_input('Updated Phone: ')
        return new_phone

    def update_contact_email(self):
        """Gets new email from user input for contact email"""
        new_email = self.get_user_input('Updated Email: ')
        return new_email

    def update_contact_notes(self):
        """Gets new notes from user input for contact notes"""
        new_notes = self.get_user_input('Updated Notes: ')
        return new_notes

    def get_contact_item_counter(self):
        """Gets the item number (count) in budget"""
        # if there are items in the contacts then assign numbers for choices
        item_counter = 0
        if self._contacts:
            keys = self._contacts.keys()
            key_list = []
            for key in keys:
                key_list.append(key)
            item_counter = int(key_list[-1]) + 1
        return item_counter

    def update_contact_nav(self):
        """Update contact navigation menu"""
        print('\nWhat item would you like to update')
        # get the available contacts to update and update the specified contact
        choices_list, main_choices = self.create_contacts_update_nav_choices()
        user_input = self.get_user_choice(choices_list)
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
        """Deletes contacts list if user chooses yes"""
        # store formatting and display delete warning
        red, bold, end_color = shellColors.RED, shellColors.BOLD, shellColors.ENDCOLOR
        self.display_delete_warning()
        user_input = input(
            f'{red}Are you sure you want to delete all contacts{end_color}? Type {bold}{red}"yes" or "y": {end_color}')
        if user_input.lower() == "yes" or user_input.lower() == "y":
            self._contacts = {}
            self.display_warning("Contacts list deleted.")
        self.contacts_nav()

    def delete_contact_nav(self):
        """Delete contact navigation menu"""
        # display delete warning to user, delete if user chooses to or go to other menu
        self.display_delete_warning()
        user_input = self.get_user_choice(["Delete All", "Contacts Menu", "Main Menu", "Quit"])
        if user_input == "1":
            self.delete_contacts()
        elif user_input == "2":
            self.contacts_nav()
        elif user_input == "3":
            self.main_menu_nav()
        elif user_input == "4":
            self.quit_process()

    #### CONTACTS SECTION END ####

    #### TRAVEL TIPS SECTION START ####

    def display_travel_tips_title(self):
        """Displays travel tips section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEPUR)
        print(Format.TIPNAME)
        print(Format.LINEPUR)

    def display_travel_tips_list_items(self):
        """Displays the list of travel tips"""
        tips_list = [
            "1) Carry emergency contact information.",
            "2) Call ahead for reservations.",
            "3) Research local transportation options.",
            "4) Keep your friends and family updated.",
            "5) Make copies of important documents.\n",
        ]
        # display each tip
        for tip in tips_list:
            print(f'{shellColors.BOLD}{shellColors.PURPLE}{tip}{shellColors.ENDCOLOR}')

    def prompt_user_international_travel(self):
        """Ask if user is traveling internationally to provide helpful related information"""
        blue, bold, end_color = shellColors.BLUE, shellColors.BOLD, shellColors.ENDCOLOR
        response = input(f'{blue} Are you travelling abroad? Type {bold}"yes" or "y"{end_color}: ')
        # if the user is going international provide helpful link
        if str.lower(response) == "yes" or str.lower(response) == "y":
            print('')
            self.display_international_travel_tips()

    def display_international_travel_tips(self):
        """Display the resource for international travel resources"""
        purple, bold, end_color = shellColors.PURPLE, shellColors.BOLD, shellColors.ENDCOLOR
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
        # ask if user is traveling internationally then go back to main menu
        self.prompt_user_international_travel()
        self.main_menu_nav()

    #### TRAVEL PLANNER ####

    def display_travel_planner_title(self):
        """Displays travel planner section title to the user"""
        print(Format.NEWLINE)
        print(Format.LINEBLU)
        print(Format.PLRNAME)
        print(Format.LINEBLU)

    def planner_nav(self):
        """Travel Planner navigation menu"""
        # display section title and go to section user chooses (or display planner)
        self.display_travel_planner_title()
        print(f'{shellColors.BLUE}What would you like to do?{shellColors.ENDCOLOR}')
        user_input = self.get_user_choice(["View Planner", "Main Menu", "Quit"])
        print('')
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