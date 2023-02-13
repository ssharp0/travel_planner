import csv, time
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


def create_charts(inputCSVFile):
    """
    Opens provided CSV file containing data and parses to collect information for outcomes by month.
    :param inputCSVFile:
    :return: none
    """

    # arrays and dictionaries to store desired information from csv data file
    data_dict_hospital = {}
    data_dict_doctor = {}
    data_dict_month = {}
    hospitals = []
    doctors = []
    implant_months = []
    outcomes = []

    print(f'Opening {inputCSVFile} file...')
    time.sleep(5)

    # open the csv and go through every row and parse the data
    with open(inputCSVFile, 'r') as csv_data:
        # skip headers
        next(csv_data)
        # get rows
        rows = csv.reader(csv_data, delimiter=',')

        # iterate through each row in the csv
        for row in rows:
            # grab current element values
            doctor = row[1]
            hospital = row[2]
            implant_month = row[9]
            outcome = row[18]

            # element is not in the hospital data dictionary, then create it with appropriate keys, set val to 0
            if not data_dict_hospital.get(hospital):
                data_dict_hospital[hospital] = {}
            if not data_dict_hospital.get(hospital).get(implant_month):
                data_dict_hospital[hospital][implant_month] = {}
            if not data_dict_hospital.get(hospital).get(implant_month).get(outcome):
                data_dict_hospital[hospital][implant_month][outcome] = 0

            # increment the value based on outcome by month for the hospital
            val = data_dict_hospital[hospital][implant_month][outcome]
            val += 1
            data_dict_hospital[hospital][implant_month][outcome] = val

            # element is not in the doctor data dictionary, then create it with appropriate keys, set val to 0
            if not data_dict_doctor.get(doctor):
                data_dict_doctor[doctor] = {}
            if not data_dict_doctor.get(doctor).get(implant_month):
                data_dict_doctor[doctor][implant_month] = {}
            if not data_dict_doctor.get(doctor).get(implant_month).get(outcome):
                data_dict_doctor[doctor][implant_month][outcome] = 0

            # increment the value based on outcome by month for the doctor
            val = data_dict_doctor[doctor][implant_month][outcome]
            val += 1
            data_dict_doctor[doctor][implant_month][outcome] = val

            # element is not in the month dictionary, then create it with appropriate keys, set val to 0
            if not data_dict_month.get(implant_month):
                data_dict_month[implant_month] = {}
            if not data_dict_month.get(implant_month).get(outcome):
                data_dict_month[implant_month][outcome] = 0

            # increment the value based on outcome by month for the month
            val = data_dict_month[implant_month][outcome]
            val += 1
            data_dict_month[implant_month][outcome] = val

            # add the values to the lists to be used for charts
            if doctor not in doctors:
                doctors.append(doctor)
            if hospital not in hospitals:
                hospitals.append(hospital)
            if implant_month not in implant_months:
                implant_months.append(implant_month)
            if outcome not in outcomes:
                outcomes.append(outcome)

    print('Creating PDF Charts: Outcomes by Month for Doctors and Hospitals...')
    time.sleep(5)
    # create charts for outcomes by month for doctors and hospitals
    create_bar_chart_outcomes_by_month(
        hospitals,
        doctors,
        implant_months,
        data_dict_hospital,
        data_dict_doctor,
        data_dict_month,
        outcomes
    )

    print('Displaying Chart: Total Outcomes by Month...')
    time.sleep(5)
    # display the bar chart for total outcomes by month
    display_total_outcomes_by_month(implant_months, data_dict_month, outcomes)

    # close all charts
    plt.close('all')


def create_bar_chart_outcomes_by_month(hospitals, doctors, implant_months, data_dict_hospital, data_dict_doctor, data_dict_month, outcomes):
    """
    Creates charts to show outcomes by month based on provided csv data file.
    :param hospitals: list of hospitals from data
    :param doctors:   list of doctors from data
    :param implant_months:  list of months from data
    :param data_dict_hospital: dictionary of hospital data
    :param data_dict_doctor: dictionary of doctor data
    :param data_dict_month:  dictionary of month data
    :param outcomes: list of outcomes
    :return: none, saves charts to PDF
    """
    # store data for x and y axis
    x_axis_dates = []
    y_axis_good_outcomes = []
    y_axis_bad_outcomes = []
    pdf_file = PdfPages('./reports/outcomes_by_month.pdf')

    # create outcomes by month chart
    for month in implant_months:
        x_axis_dates.append(month)
        if not data_dict_month.get(month):
            y_axis_good_outcomes = 0
            y_axis_bad_outcomes = 0
        else:
            for outcome in outcomes:
                if outcome == 'Good':
                    if not data_dict_month.get(month).get(outcome):
                        y_axis_good_outcomes.append(0)
                    else:
                        val = data_dict_month[month][outcome]
                        y_axis_good_outcomes.append(val)
                if outcome == 'Bad':
                    if not data_dict_month.get(month).get(outcome):
                        y_axis_bad_outcomes.append(0)
                    else:
                        val = data_dict_month[month][outcome]
                        y_axis_bad_outcomes.append(val)

    # create and save chart to pdf
    x = np.arange(len(x_axis_dates))
    fig, ax = plt.subplots()
    ax.bar(x - 0.25 / 2, y_axis_good_outcomes, 0.25, label='Good Outcomes', color='g')
    ax.bar(x + 0.25 / 2, y_axis_bad_outcomes, 0.25, label='Bad Outcomes', color='r')
    ax.set_ylabel('# Outcomes')
    ax.set_xlabel('Months')
    ax.set_xticks(x, x_axis_dates)
    ax.legend()
    plt.title(f'Total Outcomes by Month')
    fig.savefig(pdf_file, format='pdf')
    plt.close(fig)

    # reset axis data
    x_axis_dates = []
    y_axis_good_outcomes = []
    y_axis_bad_outcomes = []

    # create charts to show outcomes by month for hospitals
    for hospital in hospitals:
        for month in implant_months:
            x_axis_dates.append(month)
            if not data_dict_hospital.get(hospital).get(month):
                y_axis_good_outcomes.append(0)
                y_axis_bad_outcomes.append(0)
            else:
                for outcome in outcomes:
                    if outcome == 'Good':
                        if not data_dict_hospital.get(hospital).get(month).get(outcome):
                            y_axis_good_outcomes.append(0)
                        else:
                            val = data_dict_hospital[hospital][month][outcome]
                            y_axis_good_outcomes.append(val)
                    if outcome == 'Bad':
                        if not data_dict_hospital.get(hospital).get(month).get(outcome):
                            y_axis_bad_outcomes.append(0)
                        else:
                            val = data_dict_hospital[hospital][month][outcome]
                            y_axis_bad_outcomes.append(val)

        # create and save plot to PDF
        x = np.arange(len(x_axis_dates))
        fig, ax = plt.subplots()
        ax.bar(x - 0.25 / 2, y_axis_good_outcomes, 0.25, label='Good Outcomes', color='g')
        ax.bar(x + 0.25 / 2, y_axis_bad_outcomes, 0.25, label='Bad Outcomes', color='r')
        ax.set_ylabel('# Outcomes')
        ax.set_xlabel('Months')
        ax.set_xticks(x, x_axis_dates)
        ax.legend()
        plt.title(f'Hospital | {str(hospital)}: Outcomes by Month')
        fig.savefig(pdf_file, format='pdf')
        plt.close(fig)

        # reset the axis data for next hosptisal
        x_axis_dates = []
        y_axis_good_outcomes = []
        y_axis_bad_outcomes = []

    # reset variables to store access data
    x_axis_dates = []
    y_axis_good_outcomes = []
    y_axis_bad_outcomes = []

    # craete chart to show doctors outcomes by month
    for doctor in doctors:
        for month in implant_months:
            x_axis_dates.append(month)
            if not data_dict_doctor.get(doctor).get(month):
                y_axis_good_outcomes.append(0)
                y_axis_bad_outcomes.append(0)
            else:
                for outcome in outcomes:
                    if outcome == 'Good':
                        if not data_dict_doctor.get(doctor).get(month).get(outcome):
                            y_axis_good_outcomes.append(0)
                        else:
                            val = data_dict_doctor[doctor][month][outcome]
                            y_axis_good_outcomes.append(val)
                    if outcome == 'Bad':
                        if not data_dict_doctor.get(doctor).get(month).get(outcome):
                            y_axis_bad_outcomes.append(0)
                        else:
                            val = data_dict_doctor[doctor][month][outcome]
                            y_axis_bad_outcomes.append(val)

        # create and save chart by doctor to pdf
        x = np.arange(len(x_axis_dates))
        fig, ax = plt.subplots()
        ax.bar(x - 0.25/2, y_axis_good_outcomes, 0.25, label='Good Outcomes', color='g')
        ax.bar(x + 0.25/2, y_axis_bad_outcomes, 0.25, label='Bad Outcomes', color='r')
        ax.set_ylabel('# Outcomes')
        ax.set_xlabel('Months')
        ax.set_xticks(x, x_axis_dates)
        ax.legend()
        plt.title(f'Doctor | {str(doctor)}: Outcomes by Month')
        fig.savefig(pdf_file, format='pdf')
        plt.close(fig)

        # reset axis for next doctor
        x_axis_dates = []
        y_axis_good_outcomes = []
        y_axis_bad_outcomes = []

    # close the file
    pdf_file.close()
    print('Charts saved as PDF...')


def display_total_outcomes_by_month(implant_months, data_dict_month, outcomes):
    """
    Displays the total outcomes by month.
    :param implant_months: list of months
    :param data_dict_month: dictionary of months data
    :param outcomes:  list of outcomes
    :return:
    """
    # store data for x and y axis
    x_axis_dates = []
    y_axis_good_outcomes = []
    y_axis_bad_outcomes = []

    # get outcomes by month
    for month in implant_months:
        x_axis_dates.append(month)
        if not data_dict_month.get(month):
            y_axis_good_outcomes = 0
            y_axis_bad_outcomes = 0
        else:
            for outcome in outcomes:
                if outcome == 'Good':
                    if not data_dict_month.get(month).get(outcome):
                        y_axis_good_outcomes.append(0)
                    else:
                        val = data_dict_month[month][outcome]
                        y_axis_good_outcomes.append(val)
                if outcome == 'Bad':
                    if not data_dict_month.get(month).get(outcome):
                        y_axis_bad_outcomes.append(0)
                    else:
                        val = data_dict_month[month][outcome]
                        y_axis_bad_outcomes.append(val)

    # create the cart
    x = np.arange(len(x_axis_dates))
    fig, ax = plt.subplots()
    ax.bar(x - 0.25 / 2, y_axis_good_outcomes, 0.25, label='Good Outcomes', color='g')
    ax.bar(x + 0.25 / 2, y_axis_bad_outcomes, 0.25, label='Bad Outcomes', color='r')
    ax.set_ylabel('# Outcomes')
    ax.set_xlabel('Months')
    ax.set_xticks(x, x_axis_dates)
    ax.legend()
    plt.title(f'Total Outcomes by Month')
    # display the chart
    plt.show(block=False)
    plt.pause(15)
    plt.close(fig)


print('Chart Mircroservice is running...')

while True:

    """
    Microservice that looks for 'createChart' string in the chart_service.txt
    Once the string has been communicated, then the microservice will look for the provided case_database.csv 
    file to create the data charts: outcomes by month
    """

    time.sleep(5)

    # open the communication pipe file and look for instructions
    with open('chart_service.txt', "r") as file:
        # get the instruction and the csv file
        instruction = file.readline().strip()
        database_csv = file.readline().strip()

        # if valid instruction is recieved
        if instruction == 'createChart':
            print(f'Valid REQUEST received, preparing to create charts from {database_csv}')
            # create the charts outcomes by month
            create_charts(database_csv)

            # update the communication pipe with the path to the saved PDFcharts
            with open('chart_service.txt', "w") as file:
                print('Writing back to chart_service.txt with file path of PDFs: ./reports/outcomes_by_month.pdf')
                file.write('./reports/outcomes_by_month.pdf')
