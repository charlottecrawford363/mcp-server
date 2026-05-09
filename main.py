from mcp.server.fastmcp import FastMCP
from typing import Optional
import os
import shutil

mcp = FastMCP(
    "Myserver",
    instructions=""
)

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "datasets")
DATA_VIS_FOLDER = os.path.join(os.path.dirname(__file__), "data_vis")

ALLOWED_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls"} # add others later

def ensure_folders():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    if not os.path.exists(DATA_VIS_FOLDER):
        os.makedirs(DATA_VIS_FOLDER)


@mcp.tool()
def add_dataset(filename: str, overwrite: Optional[bool] = False, rename: Optional[str] = "") -> str:
    """
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

    # Checking for duplicate names in dataset folder
    if os.path.exists(dest_path) and not overwrite:
        return f"Duplicate: {basename} already exists. To add this file, prompt to overwrite the previous file or rename the file being uploaded"

    shutil.copyfile(filename, dest_path)
    return f"Dataset added: {basename}"




if __name__ == "__main__":
    mcp.run()
