# GH Asesores Payroll Processor

## Description

Welcome to GH Asesores Payroll Processor! This application has been developed to calculate employee payments considering weeks worked, overtime, and hours worked. It utilizes the openpyxl library to process Excel files and is presented through Streamlit, offering an interactive and easy-to-use web interface.

## Operation of the Application

### Page 1: Load an Excel File

1. On the '1_📈_Load_Sheet' page, use the 'Browse Files' button to upload your Excel file. Make sure it's in 'xlsx' or 'xls' format and does not exceed 200 MB.

2. After uploading the file, the application will automatically check if it contains the necessary data. A warning will be shown if the file is empty, and a log message will be recorded.

3. If the file has valid data, the application will apply modifications based on rules defined in the 'rules' folder.

4. On the interface, you'll see a progress bar indicating the application's progress through the rules.

5. After applying all the rules, a modified file will be generated.

6. You'll see a 'Download Modified File' button. Click to download the modified file to your device.

## Important Considerations

1.  **Excel File Format:** Ensure that the Excel file contains only one data sheet. The first column should contain the list of collaborators, while the subsequent columns should represent the working days to be analyzed.

2.  **Workweek:** The program will only consider workweeks from Monday to Sunday. If a week is incomplete, it will not be taken into account for calculations.

3.  **Entry and Exit Time Format:** It is crucial that entry and exit records follow the 12-hour time format, followed by 'a.m.' or 'p.m.'. For example: 6:00:00 a.m. If the records do not comply with this format, they will not be included in the calculations.

4. **Holidays:** The program identifies holidays as those with the cell highlighted with color. It is recommended to avoid highlighting other non-holiday days to avoid altering the calculation of hours worked that are affected by special rates.

## Streamlit

Streamlit is an open-source framework that makes it easy to create web applications for data analysis and interactive prototypes. With Streamlit, developers can effortlessly turn Python scripts into web applications.

### Key Features of Streamlit

- **Simplicity:** With just a few Python commands, it's possible to create interactive interfaces without the need for web development expertise.

- **Dynamic Updates:** Interface elements automatically update when data or parameters change.

- **Easy Integration:** Easily integrates with popular libraries such as Pandas, Plotly, and Matplotlib for data visualization.

## Openpyxl

Openpyxl is a Python library that allows reading and writing Excel files in xlsx format. With Openpyxl, it's possible to programmatically manipulate spreadsheets, cells, and data.

### Key Features of Openpyxl

- **Read and Write:** Enables reading and writing of data in Excel files.

- **Spreadsheet Manipulation:** Facilitates the creation, duplication, and deletion of spreadsheets.

- **Cell Formatting:** Allows formatting cells, such as styles, colors, and formulas.

## System Requirements

- **Python 3.x**

- **Libraries:** Streamlit, Openpyxl
