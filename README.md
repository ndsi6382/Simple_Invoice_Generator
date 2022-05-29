# Simple Invoice Generator

This is a simple (linux) command line program to generate invoices (with the 
Australian options of GST / ABN included). There is also capability to batch 
create invoices from a CSV file. An example of an invoice produced by this 
program can be found in the `./samples` subdirectory.

Invoice parameters are set either inside the program through prompts, or 
through the `config.py` file. The invoice is written in Markdown format, 
before being converted to PDF.

## Setup and Usage
There is only one dependency: `md2pdf`, which can be installed with: 
`pip install md2pdf`.  
After navigating to the directory of the program, run 
`sudo chmod +x ./simple_invoice_generator.py` to allow the file's execution.  
Usage is as follows: 
`./simple_invoice_generator.py [-h] [[-s] OR [-b INPUT.csv]] [-o OUTPUT_DIR]`.  
Sender details must always be set in `config.py`.  
If no arguments are given, the user is prompted to enter recipient details, 
before generating an invoice. 
- `-s` creates a singular invoice from fields specified in the `config.py` file.
- `-b INPUT.CSV` batch creates invoices from a specified CSV file.
- `-o OUTPUT_DIR` overrides the output directory specified in `config.py`.
- `-h` displays the help message.  

## Configuration
`config.py` contains parameters for changing recipient, activity, and sender 
details, as well as formatting options such as letterheads (an image file for 
which the recommended width is 628px), footers, and the setting of a default 
output directory. To **not** include a field, set its value to an empty string 
`""`. All activity fields must be filled - where a 'qty' is not applicable, a 
hyphen string `"-"` should be used instead. The default styling makes use of a 
small CSS file, which can be modified if desired.  

Please note the following when using paths: paths beginning with `/` or `\` 
will be treated as absolute paths. Syntax such as `.`, `..`, or not being 
prefixed with a slash will be interpreted as a subdirectory of the current 
working directory. Do not suffix directories with `/`, and although there 
are no *expected* problems to occur, avoid using spaces in paths to be safe.

## CSV File Handling and Expectations
An example CSV will be included in the `samples` directory soon.  
CSV files are expected to contain at least 5 headers named as follows: 
- `name` : Recipient name
- `contact1` : Recipient details (line 1) (`contact2` for a second contact 
line is optional)
- `desc` : Activity description
- `qty` : Activity quantity
- `unitPrc` : Unit price

Recipient fields may be empty in order to accomodate invoices where there is 
more than one activity. Entries in the CSV file that contain an empty `name` 
and `contact1` field but filled `desc`, `qty`, and `unitPrc` fields will be 
attributed to the recipient details above.

## Further Updates
- Implement functionality for custom invoice numbers, custom output filenames
- Streamline commandline arguments for the above
- Ability to generate reports/logs.
- Avoid system commands.
