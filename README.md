# Tabular Data Viewer

A simple GUI application for viewing tabular data files, built using [NiceGUI](https://nicegui.io/). This app supports CSV, Excel, and SAS files and provides an interactive interface for file upload and preview.

## Features

- Supports CSV, Excel (`.xls`, `.xlsx`, `.xlsm`), and SAS (`.sas7bdat`, `.xpt`) file formats.
- Automatically detects CSV delimiters or allows manual input.
- Handles multiple sheets in Excel files.
- Provides a simple UI for uploading and previewing data.
- Built with Nuitka for standalone distribution.

## Installation

### Running from Source

#### Prerequisites

Ensure you have Python 3.8+ installed, along with the following dependencies:

```sh
pip install nicegui pywebview pandas pyreadstat openpyxl 
```

#### Running the App

```sh
python tabular_viewer.py
```

### Running the Prebuilt Executable

You can download the latest release from the [Releases](https://github.com/Varen-6/tabular_viewer_test_task/releases) section, which contains the prebuilt `.exe` file. Simply run the executable—no installation required.

## Building the Executable

To build the application yourself, use [Nuitka](https://nuitka.net/):

bash:
```sh
python -m nuitka --onefile --mingw64 --clang \
    --windows-console-mode=disable \
    --include-package=pandas \
    --include-package=pyreadstat \
    --include-package=openpyxl \
    --include-package=nicegui \
    --nofollow-import-to=pywebview \
    --include-module=pygments.formatters.html \
    --assume-yes-for-downloads \
    --noinclude-pytest-mode=nofollow \
    --nofollow-import-to=tests  \
    --nofollow-import-to=markdown2.doctest \
    --nofollow-import-to=pydoc \
    --include-package-data=nicegui \
    --output-dir=build tabular_viewer.py
```
windows:
```
python -m nuitka --onefile --mingw64 --clang --windows-console-mode=disable --include-package=pandas --include-package=pyreadstat --include-package=openpyxl --include-package=nicegui --nofollow-import-to=pywebview --include-module=pygments.formatters.html --assume-yes-for-downloads --noinclude-pytest-mode=nofollow --nofollow-import-to=tests --nofollow-import-to=markdown2.doctest --nofollow-import-to=pydoc --include-package-data=nicegui --output-dir=build tabular_viewer.py

```

This will generate a single `.exe` file in the `build/` directory.

## Usage

1. Run the application (`tabular_viewer.exe` or `python tabular_viewer.py`).
2. Upload a tabular data file.
3. The app will display a preview of the file's contents.
4. Close any preview using the "Close" button.
5. Use "Shutdown" button to clear any temporary files app may create during it's work and exit the application.

## Notes

- The `temp/` directory is used for storing uploaded files temporarily and is cleaned upon shutdown.
- If an unsupported file format is uploaded or app can't handle the supported file due to some unsupported features(for example `.xpt` file being a CPORT file instead of XPORT and requires SAS installation to handle), an error notification will be displayed.

## License

This project is for evaluation purposes and does not have an assigned license.

