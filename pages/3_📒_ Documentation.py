import streamlit as st

st.set_page_config(page_title="GH Asesores", page_icon="📒", layout="wide")

if (
    "authentication_status" not in st.session_state
    or st.session_state.authentication_status is None
    or st.session_state.authentication_status is False
):
    st.warning("You must login to access this page.")
    st.markdown(
        f'<meta http-equiv="refresh" content="0;url={st.secrets.urls.login}">',
        unsafe_allow_html=True,
    )
    st.stop()


def main():
    st.title("Welcome to GH Asesores payroll Processor!")

    # Description
    st.header("Description")
    st.write(
        "This application has been developed to calculate employee payments considering weeks worked, overtime and overtime. It uses the openpyxl library to process Excel files and is presented through Streamlit, offering an interactive and easy to use web interface."
    )

    # Operation of the Application
    st.header("Operation of the Application")

    # Page 1: Load an Excel File
    st.header("Page 1: Load an Excel File")
    st.write(
        "1. On the '1_📈_Load_Sheet' page, use the 'Browse Files' button to upload your Excel"
        + " file. Make sure it's in 'xlsx' or 'xls' format and does not exceed 200 MB."
    )
    st.write(
        "2. After uploading the file, the application will automatically check if it contains the necessary data. A warning will be shown if the file is empty, and a log message will be recorded."
    )
    st.write(
        "3. If the file has valid data, the application will apply modifications based on  rules defined in the 'rules' folder."
    )
    st.write(
        "4. On the interface, you'll see a progress bar indicating the application's"
        + " progress through the rules."
    )
    st.write("5. After applying all the rules, a modified file will be generated.")
    st.write(
        "6. You'll see a 'Download Modified File' button. Click to download the modified"
        + " file to your device."
    )

    st.header("Page 2: PDF Download")
    st.write(
        "On this page, you will find a list of employees along with download buttons associated with each of them. These buttons allow you to obtain the pay stub for each employee in PDF format. To download the pay stub of a specific employee, simply click on the 'Download' button next to their name. Once you click the button, the PDF file will start downloading to your device. Then, you will have the option to choose the folder where you want to save the file. Simply select the desired location and save the file. Repeat this process for each employee whose pay stub you wish to download."
    )

    # Considerations
    st.header("Important Considerations")
    st.write(
        "1. **Excel File Format:** Ensure that the Excel file contains only one data sheet. The first column should contain the list of collaborators, while the subsequent columns should represent the working days to be analyzed."
    )
    st.write(
        "2. **Workweek:** The program will only consider workweeks from Monday to Sunday. If a week is incomplete, it will not be taken into account for calculations. Additionally, if a week, even if complete, is divided between two tables, the program will not consider it as a complete week and will not include it in the calculations."
    )
    st.write(
        "3. **Entry and Exit Time Format:** It is crucial that entry and exit records follow the 12-hour time format, followed by 'a.m.' or 'p.m.'. For example: 6:00:00 a.m. If the records do not comply with this format, they will not be included in the calculations."
    )
    st.write(
        "4. **Holidays:** The program identifies holidays as those with the cell highlighted with color. It is recommended to avoid highlighting other non-holiday days to avoid altering the calculation of hours worked that are affected by special rates."
    )
    st.write(
        "5. **PDF:** To generate the PDFs per employee, it's necessary to upload the base file to the load sheet and select the period, so that they can be generated and the necessary data can be obtained to create the pay stub."
    )

    # Streamlit
    st.header("Streamlit")
    st.write(
        "Streamlit is an open-source framework that makes it easy to create web applications"
        + " for data analysis and interactive prototypes. With Streamlit, developers can"
        + " effortlessly turn Python scripts into web applications."
    )
    st.subheader("Key Features of Streamlit")
    st.write(
        "1. **Simplicity:** With just a few Python commands, it's possible to create"
        + " interactive interfaces without the need for web development expertise."
    )
    st.write(
        "2. **Dynamic Updates:** Interface elements automatically update when data or"
        + " parameters change."
    )
    st.write(
        "3. **Easy Integration:** Easily integrates with popular libraries such as Pandas,"
        + " Plotly, and Matplotlib for data visualization."
    )

    # Openpyxl
    st.header("Openpyxl")
    st.write(
        "Openpyxl is a Python library that allows reading and writing Excel files in xlsx"
        + " format. With Openpyxl, it's possible to programmatically manipulate spreadsheets,"
        + " cells, and data."
    )
    st.subheader("Key Features of Openpyxl")
    st.write("1. **Read and Write:** Enables reading and writing of data in Excel files.")
    st.write(
        "2. **Spreadsheet Manipulation:** Facilitates the creation, duplication, and deletion of spreadsheets."
    )
    st.write(
        "3. **Cell Formatting:** Allows formatting cells, such as styles, colors, and formulas."
    )

    # System Requirements
    st.header("System Requirements")
    st.write("1. Python 3.x")
    st.write("2. Libraries: Streamlit, Openpyxl ")


if __name__ == "__main__":
    main()
