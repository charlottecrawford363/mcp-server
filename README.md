# MCP Data Visualization Server

## Overview
This is a prototype of a data visualization MCP server. It allows the user to upload 

## Design Choices & Assumptions
### Simplifications
- **File upload through absolute path**: The add_dataset tool currently takes the absolute path of the file on the local machine instead of a direct file upload. It uses the copyfile() method from the shutil to then copy that file into servers's dataset folder which helps avoid issues that come with the file size at the cost of the user's convenience. Some method of chunk-based uploading would likely be best to avoid file size issues.
- **Single visualization type (scatter plot)**: The server currently only has a tool to create a scatterplot and no other data visualizations. The plotly library and the possibility of creating more general helper functions to use between data visualization creating tools leaves room for many more data visualizations to be added later during this project. The current scatter plot creating tool also currently only takes parameters for the columns for the axes, the color grouping, and the hover name, while the plotly scatter function has room for a lot more specific design aspects. 
- **Single shared data_vis folder rather than per-dataset folders**: Rather than creating an individual data_vis folder for each dataset, all of the data visualization for every dataset are contained in the singular data_vis folder. This is mostly done with the idea that, with more types of data visualizations and functionalities for those visualizations added, there will be visualizations that contain data from more than one dataset, which could make the folders a bit more complicated. Rather, the server currently handles which dataset belongs to which visualization with a uniform naming convention that will make searching for visualizations by dataset easier. Note: the current naming convention is more of a placeholder and would be modified as more forms of visualizations are added.
- **File Types**: Currently only excepts files of type ".csv", ".xlsx" or ".xls" to keep analysis of the datasets simple and uniform. 
- **File checking**: Current file checking only checks based on the name of the file (whether it ends in ".csv", ".xlsx" or ".xls") and not the actual content of the file. To be safe, it would be helpful to add something that checks whether the contents of the file are in line with the extension defined in the name of the file.
- **No functionality for cross-dataset plots**: Currently does not have the capabilities of creating plots between two or more datasets. Something to be considered for that would be the lengths of the columns being compared: if one column is longer than the other, then it might be best to add some sort of method that generates data for the shorter column based on the pattern of existing data using machine learning concepts.

### Tradeoffs
- **File upload method (absolute path vs direct upload)**: Having the user provide the absolute path of the file is more simple and reliable on the backend, not having to worry about memory issues that comes with trying to copy over data from a direct file upload, but this method also puts more of a burden on the user to find the absolute path of the file they want to upload. 
- **Visualization retrieval (browser vs in-conversation)**: The return_data_vis function is currently designed to open the specified data visualization in the user's browser through the webbrowser library. This was done to bypass the issues that came with the data visualization file being too large to display in the chat and to ensure that the interactive elements of it were working properly. For a non-prototype version of this server, it would likely be easier on the user's end if the visualizations could be displayed in the chat with the rest of the conversation.
- **Memory efficiency vs version history (multiple versions of same plot)**: Each time a data visualization is slightly modified (i.e. adding a column to do color grouping with in a scatter plot), an entirely new file of that plot is created with a specific name to prevent pre-existing visualizations to be overwritten. This is useful in that it essentially contains the version history of the plot if the user wants to look back at the different versions of the plot, but it is very inefficient in terms of memory. 

## Reflection: Is LLM Integration Worth It?
LLM integration helps in allowing the user to be able to use more natural language in creating data visualizations and not have the burden of handling the coding themselves. It also usually allows the user to refer to columns without having to use the precise column name, the LLM correcting the errors itself. If there are errors, it is also able to provide those in a more easily understandable way for humans, leaving room for the user to modify their prompt to fix those errors. The conversations in an LLM are also an easy way to track the user's history of creating visualizations. The use of prompts can be useful as well, like the explore_dataset function that has the LLM view a dataset's columns and suggest interesting visualizations from that, which would be much more difficult to code. 

However, with the current design of the MCP server tools and some other issues that come with it simply being an LLM, it is not as impactful as it could be. If a dataset's column names are more ambiguous, like some odd arrangement of numbers and letters that are not easily interpretable (ex. a12), it is more difficult for the LLM to correct any incorrect references to columns. With the current file upload and data visualization retrieval methods, utilizing an LLM is not as efficient or seamless as it could be otherwise. Additionally, any time a plot is modified (ex. adding one extra column for the hover_name parameter of the scatter plot tool), it creates an entirely new scatter plot file, which could easily cause issues with the memory. 

As I was creating this MCP server, I began wondering how useful LLM integration was compared to something like creating a user interface that carries out the same functions. Aside from prompting, a properly designed user interface could be more effective and remove the issue of natural language by adding something like drop down menus (Column 1, Column 2, Plot Type, etc.) that would also bypass the ambiguity problem. Ultimately, I think that adding features to make the server have a more seamless workflow within the chat and more prompt features that are useful and couldn't be easily implemented into something like the aforementioned user interface would make LLM integration worth it, depending on what the user values in the data visualization creation process.

## Learning Process
For basic understanding of what an MCP was and how an MCP server worked: https://modelcontextprotocol.io/docs/getting-started/intro 
For another introduction to MCP servers and a basic tutorial on how to create my own custom MCP server: https://www.youtube.com/watch?v=-8k9lGpGQ6g

Using the two links above, I was able to form a basic understanding of what an MCP server and how to start my own. Following the creation method in the YouTube video above, I used `FastMCP` and read up on how that worked (https://gofastmcp.com/getting-started/welcome), mainly focusing on the "Core Components" section which helped me learn more about how to use tools, resources, and prompts. I then began creating methods for the data visualization MCP server, finding libraries, looking up documentation, and looking at example MCP servers as I went. Note: Claude Desktop was used for testing.

### Challenges
Some of the main challenges I faced:
- I had originally built the file upload tool `add_dataset` to allow the user to directly upload a file, taking in the name of the file and the contents of the file as parameters, but when I tested this, I quickly realized it failed on larger datasets. So, I looked up Python libraries to help with this and found `shutil` which has the copyfile() method currently implemented. I found it doesn't really have the same file size issue, but it takes a path to a file as a paramater, forcing the user to provide the absolute path of the file they want to upload to the LLM. While I think that allowing the user to directly upload files would be essential to a seamless workflow, I left it as is for the prototype.
- I also originally wrote the data visualization retrieval tool `return_data_vis` to return the data visualization within the chat, but that also had issues with file size. So, I wrote it to return an html path for the data visualization that the user could then copy and paste into their browser. Finding this tedious, I looked up if there was a way to have it launch directly in the user's browser and found the `webbrowser` library which I implemented into the tool. This also breaks the workflow and would likely be something fixed in a non-prototype version.
- When I added more Python libraries to the server (like `pandas` and `plotly`), I originally ran into some issues getting the MCP server connected to Claude Desktop. Viewing the logs through the Developer Settings, I figured out the issue was in the `claude_desktop_config.json` and read the MCP debugging documentation and checked the server logs to figure out how to modify the json to read the libraries from the server and not just `mcp[cli]` like it was originally designed. The `claude_desktop_config.json` code I ended up using is:
```
"mcpServers": {
    "Data_Visualization_MCP": {
      "command": "C:\\Users\\charl\\.local\\bin\\uv.EXE",
      "args": [
        "run",
        "--frozen",
        "--directory",
        "C:\\Users\\charl\\mcp-server",
        "mcp",
        "run",
        "main.py"
      ]
    }
  }
```
- As I was creating the scatter plot creation tool using the plotly scatter function, I quickly realized there were a lot more parameters than I was expecting. To keep it cleaner for the prototype, I only added a few of those parameters, but for the most freedom in user styling, these parameters would need to be added to the mcp.tool() as well, as well as a more efficient way to check/validate those parameters. 
### Future Additions
- Direct file upload functionality
- Data visualization display in LLM chat
- File deletion (most likely with a parameter that allows a user to specify if, when deleting a dataset, they want all associated data visualizations to be deleted as well)
- Cross-dataset visualizations and optional machine learning algorithms to fix columns of different lengths
- A lot more data visualization options (from plotly and likely other data visualization libraries)
- Better uniform naming convention for data visualizations
- Modifications to be able to add more file types
- Check that contents of the file follow the declared file type
- If sensitive data were to be handled, would be important to add some security measures
