# Configuration File for Simple Invoice Generator

# Modify the parameters in this file accordingly.

class Recipient:
#   Line2 may be ignored by leaving as "".
    Name = "John Smith"
    Line1 = "12 Street Road"
    Line2 = "Sydney, NSW, 2000"
    Activities = [
#       Add/Remove services here, with credits listed with a negative unitPrc.
#       If a "qty" is not applicable, assign it a hyphen string: "-".
#       {
#           "desc":"desc",
#           "qty":"0",
#           "unitPrc":"0"
#       }
        {
            "desc":"Term 2 Clarinet Lessons",
            "qty":10,
            "unitPrc":45
        },
        {
            "desc":"Lesson Credit from Previous Term",
            "qty":2,
            "unitPrc":-45
        },
        {
            "desc":"AMEB Exam Recording Session",
            "qty":'-',
            "unitPrc":60
        }
    ]


class Sender:
#   'Line[1,2]', 'BankName', 'ABN' may be ignored by leaving as "" (some of 
#   these details may already be in the letterhead, therefore do not need 
#   inclusion here).
    Name = "Nicholas Lastname"
    BSB = "123 456"
    AccNo = "12 345 678"
    BankName = "National Australia Bank"
    ABN = "12 345 678 901"
    Line1 = ""
    Line2 = ""
    

class Options:
#   Paths beginning with '/' or '\' will be treated as absolute paths.
#   Syntax such as '.', '..', or not being prefixed with a slash will be
#   interpreted as a subdirectory of the current working directory.
#   Do not suffix directories with '/'.

#   'Report' may only be True or False.
    Report = False

#   'GST' may only be True or False.
    GST = True

#   Leave as "" for no Footer Message.
    FooterMsg = "*Full amount to be paid within 14 days of receipt."

#   Leave as "" for Current Working Directory, otherwise enter path to the 
#   output directory.
    OutputDir = ""

#   "" for no letterhead, otherwise enter the filename of the letterhead
#   image. The letterhead is an image file with a recommended width of 628px.
#   It must be placed in the 'resources' subdirectory of this program.
    Letterhead = "sample_letterhead.png"

#   Name of the CSS file to use (leave as "default.css" for no custom styling).
#   It must be placed in the 'resources' subdirectory of this program.
    CSS = "default.css"
