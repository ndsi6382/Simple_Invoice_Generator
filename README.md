# Simple Invoice Generator

This is a simple (linux) command line program to generate invoices (with the 
Australian options of GST / ABN included). There is also capability to batch 
create invoices from a CSV file. An example of an invoice produced by this 
program can be found in the `samples` subdirectory.

Invoice parameters are set either inside the program through prompts, or 
through the `config.py` file. The invoice is written in Markdown format, 
before being converted to PDF.

## Setup and Usage
There is only one dependency: `md2pdf`, which can be installed with: 
`pip install md2pdf`.  
After navigating to the directory of the program, run 
`sudo chmod +x ./simple_invoice_generator.py` to allow the file's execution.  
Usage is as follows: 
`./simple_invoice_generator.py [-h] [[-s] OR [-b INPUT.csv]] [-d DIRECTORY] [-r]`.  
Sender details must always be set in `config.py`.  
If no arguments are given, the user is prompted to enter recipient details, 
before generating an invoice. 
- `-h` displays the help message.
- `-r` generates a report of the created invoices (more useful for batches).
- `-s` creates a singular invoice from fields specified in the `config.py` file.
- `-b INPUT.CSV` batch creates invoices from a specified CSV file.
- `-d DIRECTORY` overrides the output directory specified in `config.py`.  

## Configuration
`config.py` contains parameters for changing recipient, activity, and sender 
details, as well as formatting options such as letterheads (an image file for 
which the recommended width is 628px), footers, and the setting of a default 
output directory. To **not** include a field, set its value to an empty string 
`""`. All activity fields must be filled - where a 'qty' is not applicable, a 
hyphen string `"-"` should be used instead. The default styling makes use of a 
small CSS file, which can be modified if desired. CSS and letterhead files 
must be placed in the `resources` subdirectory for them to be used.  

Please note the following when using paths: paths beginning with `/` or `\` 
will be treated as absolute paths. Syntax such as `.`, `..`, or not being 
prefixed with a slash will be interpreted as a subdirectory of the current 
working directory. Do not suffix directories with `/`, and although there 
are no *expected* problems to occur, avoid using spaces in paths to be safe.

## CSV File Handling and Expectations
An example CSV has been included in the `samples` subdirectory. The batch 
output from that CSV can be found in the `samples/sample_batch_output` 
subdirectory. The subdirectory also includes a report generated from the sample 
CSV. CSV files are expected to contain at least 5 headers named as follows: 
- `name` : Recipient name
- `contact1` : Recipient details (line 1)
- [`contact2` : *Recipient details (line 2) is optional, but will be read into 
               the invoice if the field exists*]
- `desc` : Activity description
- `qty` : Activity quantity (or hrs)
- `unitPrc` : Unit price (in $)

The first row of the CSV file will be interpreted to be the headers. 
Recipient fields may be empty in order to accomodate invoices where there is 
more than one activity. Entries in the CSV file that contain an empty `name` 
and `contact1` field but filled `desc`, `qty`, and `unitPrc` fields will be 
attributed to the recipient details above.

## Further Updates
- Implement functionality for custom invoice numbers, custom output filenames
- Streamline commandline arguments for the above
