# MCP Data Visualization Server

## Overview
Brief description of what the server does and how it works.

## Design Choices & Assumptions
### Simplifications
- Absolute path uploading instead of direct file upload
- Single visualization type (scatter plot)
- Single shared data_vis folder rather than per-dataset folders
- Parameters calibrated qualitatively rather than from data

### Tradeoffs
- File upload method (absolute path vs chunking vs direct upload)
- Visualization retrieval (browser vs in-conversation)
- Cross-dataset comparisons and mismatched column lengths
- Memory efficiency vs version history (multiple versions of same plot)

### Known Issues & Limitations
- No in-place visualization editing (creates new file each time)
- No numeric column validation before plotting
- Cross-dataset plots limited to same-length columns
- File retrieval opens in browser rather than inline

## Reflection: Is LLM Integration Worth It?
### Where it helps
- Natural language column selection
- No need to write plotting code manually
- Self-correcting on column name errors

### Where it struggles
- Ambiguous column names require clarification
- No memory between sessions
- Iterating on the same plot creates file bloat

### How design decisions played in
...

## Learning Process
### What I built
### Challenges I ran into
### What I would do differently
### What I would add next





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