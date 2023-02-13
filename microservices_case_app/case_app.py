import time


def request_chart():
    """
    Method to request a chart with data based on data from case app in the case_database
    This is to show how requests can be made the data that is received back
    """

    # Make the request
    time.sleep(5)
    with open('chart_service.txt', "w") as f:
        print(f'Sending REQUEST to Chart Microservice')
        lines = ["createChart\n", "case_database.csv\n"]
        f.writelines(lines)

    # check response back from microservice
    time.sleep(40)
    with open('chart_service.txt', "r") as file:
        print(f'Opening communication pipe to check for info RECEIVED')
        pdf_file_path = file.readline()

    # display the file path for the created charts
    print(pdf_file_path)


# request data from microservice
request_chart()