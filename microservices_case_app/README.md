# Communication Contract
<strong>Chart Microservices for Case Management Application</strong>

<strong><i><u>General Notes</i></u></strong>: 

`chart_service.txt` file serves as the communication pipe between the Case App and the Microservice.

`reports` folder will serve to save the PDF of the charts.

*Microservice expects a csv file that matches the columns exactly as the example provided to properly chart.

*Save microservice files in same directory as case app (otherwise update directory location for txt file comms pipe)

<strong><i><u>Libraries-Dependencies</i></u></strong>: 

`csv` [standard python library - https://docs.python.org/3/library/csv.html]

`matplotlib` [python library to assist with charts - https://matplotlib.org/]

`numpy` [python library to assist with charts - https://numpy.org/]


## Request Data
To request data (charts) to be created from the provided case database csv file:

 Update and replace the contents of `chart_service.txt` file with the following instructions.
 
`createChart` : the microservice will look for this string EXACTLY and then it will create charts from provided csv

`case_database.csv` : the database csv file to create charts from (file/path location)

Example Call (shows database csv file and chart service txt file saved in same directory):

```    
with open('chart_service.txt', "w") as file:
    lines = ["createChart\n", "case_database.csv\n"]
    file.writelines(lines)
```

## Receive Data

Data charts will be saved as a PDF in the `reports` folder in the same local directory.

The microservice will update the `chart_service.txt` file with the path to the PDF file after it's completed creating the charts.

To receive the path to the PDF file, read from the `chart_service.txt` after the charts have been created and saved.

Example:

```    
    with open('chart_service.txt', "r") as file:
        pdf_file_path = file.readline()
    print(pdf_file_path)
```

## UML Sequence Chart
![UML Sequence Chart Image](./UML.png)