# Simple Invoice Generator

This is a simple (linux) command line program to generate invoices (with the 
Australian options of GST / ABN included). There is also capability to batch 
create invoices from a CSV file. An example of an invoice produced by this 
program can be found in the `./sample_output` subdirectory.

Invoice parameters are set either inside the program through prompts, or 
through the `config.py` file. The invoice is written in Markdown format, 
before being converted to PDF.

## Setup and Usage
There is only one dependency: `md2pdf`, which can be installed with: 
`pip install md2pdf`.  
Usage is as follows: 
`./simple_invoice_generator.py [-h] [[-s] OR [-b INPUT.csv]] [-o OUTPUT_DIR]` 
Sender details must always be set in `config.py`.  
If no arguments are given, the user is prompted to enter recipient details, 
before generating an invoice.  
`-s` creates a singular invoice from fields specified in the `config.py` file.  
`-b INPUT.CSV` batch creates invoices from a specified .csv file.  
`-o OUTPUT_DIR` overrides the output directory specified in `config.py`.  
`-h` displays the help message.  

## Configuration
`config.py` contains parameters for changing recipient, activity, and sender 
details, as well as formatting options such as letterheads (for which the 
recommended width is 628px), footers, and the setting of a default output
directory. To **not** include a field, set its value to an empty string `""`. 
All activity fields must be filled - where "qty" is not applicable, a hyphen
string `"-"` should be used instead. The default styling makes use of a small 
css file, which can be modified if desired.  

Please note the following when using paths: paths beginning with '/' or '\' 
will be treated as absolute paths. Syntax such as '.', '..', or not being 
prefixed with a slash will be interpreted as a subdirectory of the current 
working directory.Do not suffix directories with '/'.

## CSV Handling
An example .csv will be included here soon.  
.csv files are expected to contain 6 headers named as follows: Recipient name: 
`name`, Recipient details (line 1): `contact1`, Recipient details (line 2 - 
optional): `contact2`, Activity description: `desc`, Activity quantity: `qty`, 
Unit price: `unitPrc`. Recipient fields may be empty in order to accomodate 
invoices where there is more than one activity. Entries in the .csv file that 
contain an empty `name` and `contact1` field but filled `desc`, `qty`, and 
`unitPrc` fields will be attributed to the recipient details above.
