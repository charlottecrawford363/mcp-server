
Installation:
download uv
uv add "mcp[cli]"
uv add fastmcp???

** add what the claude desktop config should look like

pip install openpyxl xlrd
- xlrd to read older excel files (xsl) and openpyxl to read newer excel files (xslx)


Libraries:
utilizing **shutil** library to handling the copying/uploading of files
    note: shutil.copyfile does it in chunks to avoid having a restricted file size

plotly for data vis?

webbrowser to open data visualizations in web browser because the files are too large to be displayed in the claude chat

note: testing was done with claude desktop

naming convention of data visualizations should prevent duplicates

add functionality to remove datasets and data visualizations

considerations or things to add in future versions:
* if sensitive data is being handled it would be important to add some more security or authentication
* 


in regards to whether ai makes this process faster, i'd honestly argue not really
I think it is very possibly to make a relatively simple interface that would be just as if not
more effective than creating this as an mcp server