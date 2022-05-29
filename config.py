# Configuration File for Simple Invoice Generator

# Modify the parameters in this file accordingly.
class Recipient:
#   To ignore a field, use "".
    name = "John Smith"
    line1 = "12 Street Road"
    line2 = "Sydney, NSW, 2000"
    activities = [
#       Add/Remove services here, with credits listed with a negative unitPrc
#       If "qty" is not applicable, assign it a hyphen string: "-".
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
#   To ignore a field, use "".
    name = "Nicholas Lastname"
    line1 = "nicholasemail@example.com"
    line2 = "0412 345 678"
    bsb = "123 456"
    accNo = "12 345 678"
    bankName = "National Australia Bank"
    abn = "12 345 678 901"
    

class Options:
#   Paths beginning with '/' or '\' will be treated as absolute paths.
#   Syntax such as '.', '..', or not being prefixed with a slash will be
#   interpreted as a subdirectory of the current working directory.
#   Do not suffix directories with '/'.
#   gst can only True or False.
    gst = False
#   "" for no letterhead, otherwise enter path to letterhead.
#   The letterhead is an image file with a recommended width of 628px.
    letterhead = "sample_letterhead.png"
#   "" for no footer message.
    footerMsg = "*Full amount to be paid within 14 days of receipt."
#   "" for current working directory, otherwise enter path to output directory.
    outputDir = "sample_output"