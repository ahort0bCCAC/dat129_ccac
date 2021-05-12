# Final Project - Python 2 SP21

## Social Security Administration Names database.

The Social Security Adminsitration has name, gender and occurences* data available for each year of birth after 1879.
This data is available in .txt files as national data (one file per year), state data (one file per state), and teritory data (one file per teritory).
I have chosen to work with national data for this project.  *To safeguard privacy, the SSA restricts the list of names to those with at least 5 occurrences.
https://www.ssa.gov/oact/babynames/limits.html

## Data Prep
To run the file you'll need to download the National data from the Social Security Adminsitration's website linked above.  The data downloads in a zip file.
Within this program you can update folder location of the files.

## Database Prep
This program creates a database to store the data and run the queries using sqlite3. 
After creating the database, the data is loaded from the files into normalized tables, with the exception of gender which is added from the program.
The program reads each file, finds the name in the record and loads it to a names table.  The names table is contrained to unique records only, duplicates are ignored.
The program reads each file again to load the full data details. A guery is used to find the gender id and name id from the newly created tables that match the gender code and name with each record in order to maintain data normalization.  The txt files do not inlcude the data year within the files, therefore the year data is extracted from the file name and loaded into the data table.

While working through creating/testing my code I created functions to drop the tables created in earlier steps so that I could reset the tables for additional run of the program.  These functions are still available if needed.

## Actions
I have created a function for ease of running the database prep actions on demand.


## Data Queries
This program includes various queries for evaluating the data.  Most of these queries can be run for a name lists or for all records. I have defined functions to build the query with and without a where clause.  There are a few queries that do not have the optional where clause because they are for overall data.
I have built a function for easy selection of pre-defined name lists, and name lists that can customized.

## file attachments
I am including a Jupyter notebook and the same file downloaded to a py file. Due to file qty and size I am not including source data which can be downloaded.

## Next Steps
With minor adjustments this program can be altered to read the state and/or territory data also available.
Additional coding is needed for more user interactivity, like user input prompts for actions, pre-defined namelist selection and custom namelist building.
