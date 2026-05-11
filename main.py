from mcp.server.fastmcp import FastMCP
from typing import Optional
import os
import shutil
import pandas as pd
import plotly.express as px
import webbrowser

mcp = FastMCP("Data Visualization MCP")

# Paths to dataset and data visualization folders within mcp-server directory
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "datasets")
DATA_VIS_FOLDER = os.path.join(os.path.dirname(__file__), "data_vis")

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"} # add others later
AVAILABLE_VIS = {"scatter plot"} # available visualizations methods

def ensure_folders():
    """
    If the dataset and data visualization folders do not already exist, create them
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    if not os.path.exists(DATA_VIS_FOLDER):
        os.makedirs(DATA_VIS_FOLDER)

@mcp.tool()
def list_datasets() -> str:
    """
    Returns: list of datasets currently in the datasets folder
    """
    datasets = os.listdir(DATA_FOLDER)
    return "\n".join(datasets) if datasets else "No datasets found."

@mcp.tool()
def list_data_vis() -> str:
    """
    Returns: list of data visualizations currently in the data_vis folder
    """
    data_vis = os.listdir(DATA_VIS_FOLDER)
    return "\n".join(data_vis) if data_vis else "No data visualizations found."

@mcp.tool()
def add_dataset(filename: str, overwrite: Optional[bool] = False, rename: Optional[str] = "") -> str:
    """
    Allows the user to add a dataset to the directory at DATA_FOLDER. If the name
    of the dataset already exists, allows system to rerun the function after
    specifying if the pre-existing file should be overwritten or the current file
    should be renamed to something the user provides.
    Note: Overwrite and rename cannot both be true. If somehow both are true, then
    function will only rename and not overwrite.

    Parameter: filename - absolute path on the local machine to the dataset
    Parameter: overwrite - True to replace existing file
    Parameter: rename - new name to save the file as
    Returns: string indicating that the dataset has been successfully added
    """
    ensure_folders()

    # Checking file extension
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return f"Error: Unsupported filetype {ext}. Allowed filetypes are: {', '.join(ALLOWED_EXTENSIONS)}"

    # Rename file if necessary
    basename = os.path.basename(filename)
    if rename:
        basename = rename if rename.endswith(ext) else rename + ext
        dest_path = os.path.join(DATA_FOLDER, basename)
        shutil.copyfile(filename, dest_path)
        return f"Dataset added: {basename}"

    dest_path = os.path.join(DATA_FOLDER, basename)

    # Checking for duplicate names in dataset folder
    if os.path.exists(dest_path) and not overwrite:
        return f"Duplicate: {basename} already exists. To add this file, prompt to overwrite the previous file or rename the file being uploaded"

    shutil.copyfile(filename, dest_path)
    return f"Dataset added: {basename}"

@mcp.tool()
def return_data_vis(data_vis: str) -> str:
    """
    Opens the specified data visualization in the user's web browser.
    Note: This method is currently being used to bypass the issue of the
    data visualization being too big and ensuring that the interactive elements
    are available. This method works locally but would have issues for remote
    machines.

    Parameter: data_vis - name of the data visualization to  return
    Returns: if the data visualization could be found, opens it in user's browser
    """
    path = os.path.join(DATA_VIS_FOLDER, data_vis)
    if not os.path.exists(path):
        return f"Error: '{data_vis}' not found"
    webbrowser.open(f"file:///{path}")
    return f"Visualization {data_vis} opened in web browser"

def read_file(file: str) -> pd.DataFrame:
    """
    Read file depending on what file type it is. Designed so that other file
    types can easily be added.
    """
    file_path = os.path.join(DATA_FOLDER, file)
    if not os.path.exists(file_path):
        raise ValueError(f"File {file} not found in uploaded datasets")

    ext = os.path.splitext(file)[1].lower()
    readers = {
        ".csv": lambda f: pd.read_csv(f),
        ".xlsx": lambda f: pd.read_excel(f),
        ".xls": lambda f: pd.read_excel(f)
    }
    # double check that file is correct format
    if ext not in readers:
        raise ValueError(f"Unsupported file type {ext}")
    return readers[ext](file_path)

def name_data_vis(file1: str, col1: str, col2: str, plot_type: str, extension: str, col3: Optional[str] = "", col4: Optional[str] = "") -> str:
    """
    Separate naming function to ensure uniform naming of data visualizations.
    Note: format would change to something more generic or with conditional
    statements as more types of visualizations are added
    """
    vis_name = f"{file1}_{col1}_vs_{col2}"
    if col3:
        vis_name += f"_{col3}"
    if col4:
        vis_name += f"_{col4}"
    vis_name += f"_{plot_type}.{extension}"
    return vis_name

@mcp.tool()
def create_scatter_plot(file1: str, col1: str, col2: str, color: Optional[str] = "", hover_name: Optional[str] = "") -> str:
    """
    Creates a scatter plot using plotly with at least two columns from the same file.
    Note: Currently only takes a few parameters for plotly.express scatter for prototype,
    but would realistically be able to take many more parameters. Also, could be modified
    later to optionally take another file to compare data between different datasets.

    Parameter: file1 - name of the file corresponding to col1
    Parameter: col1 - name of the first column to compare (numeric, x-axis)
    Parameter: col2 - name of the second column to compare (numeric, y-axis)
    Parameter: color - name of another column to compare (color of the points)
    Parameter: hover_name - name of another column (displayed when hovering over a point in the scatter plot)
    Returns: message confirming the scatter plot was created and added to data_vis folder
    """

    df = read_file(file1)

    # Check that columns exist in corresponding file
    cols = df.columns
    if col1 not in cols:
        return f"Error: '{col1}' not found in {file1}. Available columns: {', '.join(df.columns)}"
    if col2 not in cols:
        return f"Error: '{col2}' not found in {file1}. Available columns: {', '.join(df.columns)}"
    if color and color not in cols:
        return f"Error: '{color}' not found in {file1}. Available columns: {', '.join(df.columns)}"
    elif hover_name and hover_name not in cols:
        return f"Error: '{hover_name}' not found in {file1}. Available columns: {', '.join(df.columns)}"

    # Check that the x and y axes are from numeric columns
    numeric_cols = df.select_dtypes(include="number").columns
    if col1 not in numeric_cols:
        return f"Error: '{col1}' does not contain numeric values. Available numeric columns: {', '.join(numeric_cols)}"
    if col2 not in numeric_cols:
        return f"Error: '{col2}' does not contain numeric values. Available numeric columns: {', '.join(numeric_cols)}"

    # Create scatter plot
    fig = px.scatter(
        df,
        x=col1,
        y=col2,
        color=color if color else None,
        hover_name=hover_name if hover_name else None)

    plot_name = name_data_vis(file1, col1, col2, "scatter", "html", color, hover_name)

    fig.update_layout(title=f"{col1} vs {col2}")
    plot_path = os.path.join(DATA_VIS_FOLDER, plot_name)
    fig.write_html(plot_path)

    return f"Scatter plot saved! {plot_name}"

@mcp.resource("datasets://{filename}/columns")
def get_columns(filename: str) -> str:
    """
    Returns a list of the specified dataset's columns separated by commas
    """
    df = read_file(filename)
    return ", ".join(df.columns)

@mcp.prompt()
def explore_dataset(filename: str):
    """
    Based on the columns and which ones are numeric, prompts to suggest interesting
    data visualizations
    """
    df = read_file(filename)
    columns = get_columns(filename)
    numeric_cols = ", ".join(df.select_dtypes(include="number").columns)
    return (
        f"The dataset {filename} has columns: {columns}. The numeric columns are {numeric_cols}."
        f"Suggest interesting visualizations based on the available visualizations in {AVAILABLE_VIS} and what those visualizations may reveal about the dataset"
    )

if __name__ == "__main__":
    mcp.run()
