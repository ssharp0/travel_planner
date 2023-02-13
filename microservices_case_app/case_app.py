import time

def request_chart():
    """
    Method to request a chart with data based on data from case app in the case_database
    This is to show how requests can be made the data that is received back
    """

    with open('chart_service.txt', "w") as f:
        lines = ["createChart\n", "case_database.csv\n"]
        f.writelines(lines)

    # timer to show that the service file is updated with
    time.sleep(45)
    with open('chart_service.txt', "r") as file:
        pdf_file_path = file.readline()

    # display the file path for the created charts
    print(pdf_file_path)


request_chart()