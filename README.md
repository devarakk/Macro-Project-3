# Macro-Project-3
**Part 1**
**Data sources**

Data for part 1 came from the OECD's economic outlook.

**Steps for data cleaning and analysis**

The python script details the instructions for cleaning and analyzing the data. It pivots the data around the different macroeconomic variables. It converts the time variable to datetime format. The data frame was then limited to the macroeconomic variables, and standard deviation and correlation was calculated for these variables, grouped by country. Finally, this data was graphed for each variable for each country.

**Instructions for reproducing results**

Go to the OECD Data Explorer and download the variables specified in the paper for Germany, Australia, and the United States. The frequency must be quarterly and data goes back to 2002. Then run the Python Script to clean and analyze the data, including producing standard deviations, correlations, and graphs.

**Part 3**

Data for part three came from the WRDS website, specifically the compustat resource. 

**Steps for cleaning, analysis, and reproduction**

The python code walks through the analysis of the data. The data needs a standardized date format and then to be broken into the three periods, pre, during, and post GFC. From there it is just a matter of putting the information into a table and graphing. Pulling the data from the website requires an account or a day pass that must be authorized by the company. 



