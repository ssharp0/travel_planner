import time

def request_chart():
    """
    Method to request a chart with data based on data from case app in the case_database
    Just to show how requests can be made the informaiton that is received back
    """
    # open the file and write to it the provided instruction (file is properly closed)
    with open('chart_service.txt', "w") as file:
        file.write('case_database.csv')

    # timer to show that the service file is updated with
    time.sleep(45)
    with open('chart_service.txt', "r") as file:
        pdf_file_path = file.readline()

    # display the file path for the created charts
    print(pdf_file_path)


request_chart()