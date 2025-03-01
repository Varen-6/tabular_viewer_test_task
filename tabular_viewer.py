from nicegui import ui, events, app
import pandas as pd
import pyreadstat
import csv
import os, shutil


def detect_csv_delimiter(filepath: str):
    """
    Detect the delimiter used in a CSV file.
    
    Args:
        filepath (str): Path to the CSV file to analyze
        
    Returns:
        str: Detected delimiter character if successful, comma (',') if no header detected,
             None if delimiter detection fails
        
    The function reads a sample of the file and uses csv.Sniffer to detect the delimiter.
    If the file has no header or detection fails, returns None.
    """
    try:
        with open(filepath, 'r', newline='') as file:
            sample = file.read(2048)
            sniffer = csv.Sniffer()
            return sniffer.sniff(sample).delimiter if sniffer.has_header(sample) else ','
    except Exception: # Delimiter detection fails
        return None  


def read_file(filepath: str, sheet_name=None) -> pd.DataFrame:
    """
    Read a tabular data file and return its contents as a pandas DataFrame.
    
    Args:
        filepath (str): Path to the file to read
        sheet_name (str, optional): Name of sheet to read for Excel files. Defaults to None.
        
    Returns:
        pd.DataFrame: DataFrame containing the file contents if successful, None if user input needed
        
    Raises:
        ValueError: If the file format is not supported
        
    Supported file formats:
    - CSV/TXT (auto-detects delimiter or prompts for manual entry)
    - Excel (.xls, .xlsx, .xlsm, .xltx, .xltm)
    - SAS7BDAT
    - XPT (SAS transport files)
    """
    ext = filepath.split('.')[-1].lower()
    match ext:
        case 'csv' | 'txt':
            delimiter = detect_csv_delimiter(filepath)
            if not delimiter:
                container = ui.row()
                with container:
                    delimiter_input = ui.input('Enter delimiter:')
                    ui.button('Submit', on_click=lambda: handle_manual_delimiter(filepath, delimiter_input.value, container))
                    ui.button('Close', on_click=lambda: container.clear())
                return None
            return pd.read_csv(filepath, delimiter=delimiter)
        case 'xls' | 'xlsx' | 'xlsm' | 'xltx' | 'xltm':
            xl = pd.ExcelFile(filepath)
            if len(xl.sheet_names) > 1 and not sheet_name:
                container = ui.row()
                with container:
                    sheet_select = ui.select(xl.sheet_names, label='Select sheet')
                    ui.button('Load', on_click=lambda: handle_excel_sheet(filepath, sheet_select.value, container))
                    ui.button('Close', on_click=lambda: container.clear())
                return None
            return pd.read_excel(filepath, sheet_name=sheet_name)
        case 'sas7bdat':
            df, _ = pyreadstat.read_sas7bdat(filepath)
            return df
        case 'xpt':
            df, _ = pyreadstat.read_xport(filepath)
            return df
        case _:
            raise ValueError('Unsupported file format')


def handle_excel_sheet(filepath: str, sheet_name: str, container):
    """
    Process an Excel file with the specified sheet name and display the resulting table.
    
    Args:
        filepath (str): Path to the Excel file to read
        sheet_name (str): Name of the sheet to load from the Excel file
        container (ui.row): UI container element holding the sheet selection components
        
    The function attempts to read the specified sheet from the Excel file and displays
    the data in a table if successful.
    """
    df = read_file(filepath, sheet_name)
    if df is not None:
        display_table(filepath, df)

def handle_manual_delimiter(filepath: str, delimiter: str, container):
    """
    Process a CSV file using a manually specified delimiter and display the resulting table.
    
    Args:
        filepath (str): Path to the CSV file to read
        delimiter (str): Manually specified delimiter character to use
        container (ui.row): UI container element holding the delimiter input components
        
    The function attempts to read the CSV with the given delimiter, clears the input UI,
    and displays the data in a table if successful. Shows an error notification if the
    operation fails.
    """
    try:
        df = pd.read_csv(filepath, delimiter=delimiter)
        container.clear()  # Remove input and button after successful processing
        display_table(filepath, df)
    except Exception as e:
        ui.notify(f'Error: {e}', type='negative')


def handle_upload(file: events.UploadEventArguments):
    """
    Handle file upload events by reading and displaying the uploaded file.
    
    Args:
        file: The uploaded file object containing the file name and data
        
    The function:
    - Creates a temp directory if it doesn't exist
    - Saves the uploaded file to the temp directory
    - Attempts to read the file using read_file()
    - Displays the data in a table if successful
    - Shows an error notification if any operation fails
    """
    try:
        content = file.content.read() 
        if not os.path.exists('temp'):
            os.makedirs('temp')
            
        filename = f"temp/{file.name}"
        with open(filename, 'wb') as f:
            f.write(content)
            
        df = read_file(filename)
        if df is not None:
            display_table(filename, df)
        
    except Exception as e:
        ui.notify(f'Error: {e}', type='negative')


def display_table(filename: str, df: pd.DataFrame):
    """
    Display a preview of a DataFrame in a card with a table.
    
    Args:
        filename (str): Name of the file being displayed
        df (pd.DataFrame): DataFrame containing the data to display
        
    Creates a card containing:
    - A label with the filename
    - A table showing the first 10 rows of data
    - A close button to remove the card
    
    The card reference is stored in table_cards for later cleanup.
    """
    card = ui.card()
    with card:
        ui.label(f'Preview of {filename}').classes('text-lg font-bold')
        ui.table(columns=[{'name': col, 'label': col, 'field': col} for col in df.columns], rows=df.head(10).to_dict('records'))
        ui.button('Close', on_click=lambda c=card: remove_card(c))


def remove_card(card: ui.card):
    """
    Remove a card element from the UI and clean up references.
    
    Args:
        card (ui.card): The card UI element to remove
        
    The function:
    - Clears the card contents
    - Deletes the card element from the UI
    """
    card.clear()
    card.delete()


def shutdown():
    """
    Shutdown the application.

    The function:
    - Clears the temp folder
    - Stops the application
    """
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    app.shutdown()


@ui.page('/')
def index():
    ui.label('Tabular Data Viewer').classes('text-2xl font-bold')
    ui.button('shutdown', on_click=shutdown)
    ui.upload(on_upload=handle_upload, multiple=False, auto_upload=True)


ui.run(native=True)