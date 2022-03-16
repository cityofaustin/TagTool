### City of Austin Innovation Office

# TagTool User Guide🏷️

---

### Preparing a document

First step is to open a file. TagTool accepts both **CSV** and **Excel** files. When opening a CSV file or an Excel document with a single page, the results will be loaded into the main table.

If the Excel file has multiple pages, you will be presented with the **Select Page window**. This will preview the pages in the document. You can go forward and back until you get to the page you'd like to work with, and click on **Open Page**.

<img title="" src="img\selectpage.jpg" alt="IMAGE" width="435">

Once the document is loaded, you will need to select the **Active Column**. This is the column that the application will search through and match keywords to. You simply need to select any cell in that column and press the **Set Active Column** button. The column will then turn green, indicating that it has been selected.

<img title="" src="img\activecolumn.jpg" alt="IMAGE" width="435">

*Select a column and press the Set Active Column button. The selected column will turn green.*

### Tag All

The **Tag All** button will compare the keywords to each item in the **Active Column** and put all of the results in a single column separated by a comma. For example, if you have two categories called <u>Food</u> and <u>Water</u> that match a single column, the resulting new column will say "**Food, Water**". This is useful if you want to put all of the results in a single cell together.

### Tag Individual

The **Tag Individual** button will compare the keywords to each item in the **Active Column** and put all of the results in their own column named after the category. Each category will get its own column and if there is a match in that row, it will put a Y in that cell. For example, if you have two categories called <u>Food</u> and <u>Water</u> that match a single column, the resulting new columns will say "Food" and "Water" with a Y in each. This is useful if you want to break the results into their own cells.

### Keyword Editor

<img title="" src="img\keywordeditor.jpg" alt="IMAGE" width="435">

The **Keyword Editor** is how you create **Keywords** and **Blacklist** words. You can edit the words directly in the Keyword Editor or you can import/export csv files and edit them externally in your software of choice.

Pressing the **New Entry** button will prompt you to type in a category name. This is how you create a new category. Once you select a name, it will appear in the list. You are able to edit the keywords and blacklist words by double clicking the cell and typing them in. Each word is to be separated by a comma. 

Pressing the **Delete Entry** button will delete the category and its words from the database.

The **Save Default and Close** button will write the changes to the **default.json** and be the default file the next time you work with the application.

##### Import and Export CSV files

Importing CSV files requires the following three column names: **Category, Keywords, Blacklist**. If you attempt to import a CSV file that doesn't have all three of these columns, it gives an error message. If there are additional columns, they will be dropped upon import.

Exporting a CSV will export everything in the keyword database to a CSV file of your choosing. You will get a save file dialog. This can come in handy if you wish to edit the categories in Excel or another spreadsheet program that can open and save to CSV. After changes have been made you can simply import them back in.

## Breaking it all down

Now that the main elements have been covered, let's break down what is happening. Once you tag the document with either Tag All or Tag Individually, the application will look at every row inside that column. It will go through all of the blacklist words and remove them from the search query and then it will go through and will compare the remaining text with the keywords. Let's say the keyword has **"Water"** but the blacklist has **"Lake Water"**. Removing ***"Lake Water"*** from the results will prevent it from flagging **"water"** as a keyword. If water isn't preceded with **"Lake"** then the flag will be successful.
