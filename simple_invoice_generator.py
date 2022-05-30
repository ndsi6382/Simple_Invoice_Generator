#!/usr/bin/env python3
from datetime import datetime
import getopt, os, sys, csv, re
from config import *
from copy import deepcopy
from md2pdf.core import md2pdf

# Absolute path of program directory
PDIR = os.path.dirname(os.path.abspath(__file__))
# Absolute path of current working directory
CWD = os.getcwd()

class Settings:
    mode = "i"
    batchfile = ""
    outputDir = "" # Must be set with the setDirectory method.
    report = Options.Report

    def setDirectory(path):
        if not os.path.isabs(path):
            path = CWD + "/" + path
        if not os.path.exists(path):
            os.makedirs(path)
        Settings.outputDir = path

    def print():
        print("Settings:")
        print(f"  Mode: {Settings.mode}")
        print(f"  Output directory: {Settings.outputDir}")
        if Settings.batchfile:
            print(f"  Batch file: {Settings.batchfile}")
        print(f"  Generate report: {'yes' if Settings.report else 'no'}")

class Invoice:
    def __init__(self, name, line1, line2):
        self.date = datetime.now().strftime('%d/%m/%Y')
        self.name = name
        self.line1 = line1
        self.line2 = line2
        self.activities = []
    
    def __str__(self):
        return f"{self.name}, {self.line1}, {self.line2}, {self.activities}"
    
    def addActivity(self, desc, qty, unitPrc):
        a = {"desc":desc, "qty":qty, "unitPrc":float(unitPrc)}
        try:
            a['qty'] = float(a['qty'])
            a['tot'] = round(a['qty']*a['unitPrc'], 2)
        except ValueError:
            a['tot'] = round(a['unitPrc'], 2)
        self.activities.append(a)
    
    def createInvoice(self, customNumber="", customFilename=""):
        def setInvNbr(self, customNumber=""):
            if customNumber:
                self.nbr = 1
            else:
                i = int(datetime.now().strftime('%Y%m%d')[2:]) * 100
                dirlist = os.listdir(Settings.outputDir)
                while (str(i) in str(dirlist)):
                    i += 1
                self.nbr = i
        
        def setFilename(self, customFilename=""):
            if customFilename:
                if Settings.outputDir:
                    self.mdAbsFilename = f"{Settings.outputDir}/{customFilename[:-4]}.md"
                else:
                    self.mdAbsFilename = f"{customFilename[:-4]}.md"
                try:
                    if os.path.exists(self.mdAbsFilename):
                        raise FileExistsError
                except FileExistsError:
                    print("File already exists!")
                    print("Choose another filename, or delete the original file.")
                    sys.exit(1)
            else:
                if Settings.outputDir:
                    self.mdAbsFilename = f"{Settings.outputDir}/Invoice_{self.nbr}.md"
                else:
                    self.mdAbsFilename = f"Invoice_{self.nbr}.md"
        
        setInvNbr(self, customNumber)
        setFilename(self, customFilename)
        with open(self.mdAbsFilename, 'w') as file:
            # Letterhead
            if Options.Letterhead:
                file.write(f"![Letterhead]({Options.Letterhead})  \n")
            # Title
            file.write( "# Tax Invoice  \n")
            file.write(f"***Invoice Number:*** *{self.nbr}*  \n")
            file.write(f"***Date:*** *{self.date}*  \n")
            file.write("  ---\n")
            # Recipient Details
            file.write(f"### Invoice for:  \n")
            file.write("| | |\n")
            file.write("| :--- | :--- |\n")
            file.write(f"| **Name:** | {self.name} |\n")
            file.write(f"| **Details:** | {self.line1}<br>{self.line2} |\n")
            file.write("| | |\n")
            file.write("  ---\n")
            # Activities Section
            file.write("| Services | Qty | Unit Price | Total Price |\n")
            file.write("| --- | ---: | ---: | ---: |\n")
            for e in self.activities:
                file.write(f"| {e['desc']} | {e['qty']} | " +
                        f"{'-' if e['unitPrc'] < 0 else ''}${abs(e['unitPrc']):.2f} | " + 
                        f"{'-' if e['tot'] < 0 else ''}${abs(e['tot']):.2f} |\n")
            # Total / GST Statement
            file.write(f"**Total: ${sum([e['tot'] for e in self.activities]):.2f}**  \n")
            if Options.GST:
                file.write("<sub><i>*Including GST.</i></sub>\n")
            else:
                file.write("<sub><i>*No GST has been charged.</i></sub>\n")
            file.write("  ---  \n")
            # Sender Details
            file.write(f"### **Payable to:**\n")
            file.write("| | |\n")
            file.write("| :--- | :--- |\n")
            file.write(f"| **Name:** | {Sender.Name} |\n")
            file.write(f"| **BSB:** | {Sender.BSB} |\n")
            file.write(f"| **Account Number:** | {Sender.AccNo} |\n")
            if Sender.BankName:
                file.write(f"| **Bank Name:** | {Sender.BankName} |\n")
            if Sender.ABN:
                file.write(f"| **ABN:** | {Sender.ABN} |\n")
            if Sender.Line1:
                file.write(f"| **Contact:** | {Sender.Line1}<br>{Sender.Line2} |\n")
            file.write("| | |\n")
            file.write("  ---  \n")
            # Footer
            if Options.FooterMsg:
                file.write(f"<sub><i>{Options.FooterMsg}</i></sub>\n")

        # Execution Commands
        md2pdf(f"{self.mdAbsFilename.replace('.md', '.pdf')}",
               md_file_path=f"{self.mdAbsFilename}",
               css_file_path=f"{PDIR}/resources/{Options.CSS}",
               base_url=f"{PDIR}/resources")
        os.remove(self.mdAbsFilename)
        # Log in report
        f = re.search('/[^/]*.pdf', self.mdAbsFilename.replace('.md', '.pdf'))
        Report.addTask(f.group()[1:], self.name)

def main():
    print("Welcome to the Simple Invoice Generator!")
    argList = sys.argv[1:]
    opts = "hsb:d:r"; longOpts = ["help", "singular", "batch=", "directory=", "report"]
    try:
        args, vals = getopt.getopt(argList, opts, longOpts) 
        u = 0
        for a, v in args:
            if a in ("-h", "--help"):
                help()
            elif a in ("-s", "--singular"):
                u += 1
                Settings.mode = "s"
            elif a in ("-b", "--batch"):
                u += 1
                Settings.mode = "b"
                Settings.batchfile = v
            elif a in ("-d", "--directory"):
                Settings.setDirectory(v)
            elif a in ("-r", "--report"):
                Settings.report = True
        if u == 2:
            raise getopt.error("Usage error.")
        if not Settings.outputDir:
            Settings.setDirectory(Options.OutputDir)
    except getopt.error:
        print("Incorrect usage!")
        help()

    Settings.print()
    if Settings.mode == "i":
        inputMode()
    elif Settings.mode == "s":
        singularMode()
    elif Settings.mode == "b":
        batchMode()
    if Settings.report:
        Report.createReport()
    print("Done. Goodbye!")

class Report:
    tasks = []

    def addTask(filename, recipient):
        time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        Report.tasks.append({'time':time, 'filename':filename, 'recipient':recipient})

    def createReport():
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f"{Settings.outputDir}/Report_{date}.txt", 'w') as file:
            file.write( "SIMPLE INVOICE GENERATOR REPORT\n\n")
            file.write(f"Report generated: {date}\n")
            file.write(f"Output directory: {Settings.outputDir}\n\n")
            file.write( "TIME & DATE          FILENAME & RECIPIENT\n")
            file.write( "-------------------------------------------\n")
            for e in Report.tasks:
                file.write(f"{e['time']}  {e['filename']}  {e['recipient']}\n")
            file.write( "-------------------------------------------\n")
            file.write("End of report.\n")

def inputMode():
    name = input("Recipient Name: ")
    line1 = input("Recipient Details, line 1 (Street Address; or Email): ")
    line2 = input("Recipient Details, line 2 (City, State, Postcode; or Phone: ")
    inv = Invoice(name, line1, line2)
    nActivities = int(input("Number of Activities for Invoice: "))
    for i in range(1, nActivities + 1):
        desc = input(f"Activity {i} description: ")
        qty = input(f"Activity {i} qty (or hrs) (enter '-' if not applicable): ")
        unitPrc = float(input(f"Activity {i} unit price (in $): "))
        inv.addActivity(desc, qty, unitPrc)
    print("Creating invoice...")
    inv.createInvoice()

def singularMode():
    print("Creating invoice...")
    inv = Invoice(Recipient.Name, Recipient.Line1, Recipient.Line2)
    for e in (Recipient.Activities):
        inv.addActivity(e["desc"], e["qty"], e["unitPrc"])
    inv.createInvoice()

def batchMode():
    try:
        with open(Settings.batchfile, 'r') as file:
            print("Batch creating invoices...")
            reader = csv.DictReader(file)
            prev = Invoice("_", "_", "_")
            invoiceList = []
            for r in reader:
                if r['name'] and r['contact1']:
                    # New recipient
                    if prev.name != "_":
                        invoiceList.append(deepcopy(prev))
                    prev = Invoice("_", "_", "_")
                    prev.name = r["name"]
                    prev.line1 = r["contact1"]
                    prev.line2 = r["contact2"]
                    prev.addActivity(r["desc"], r["qty"], r["unitPrc"])
                else:
                    # Add to previous recipient
                    prev.addActivity(r["desc"], r["qty"], r["unitPrc"])
            invoiceList.append(prev)
            for e in invoiceList:
                e.createInvoice()
    except FileNotFoundError:
        print("File not found.")
        print("Check path and filename, subdirectories should not begin with '/'.")
        sys.exit(1)

def help():
    """Displays the following help message, then exits"""
    print("Usage: ./simple_invoice_generator.py [-h] [[-s] OR [-b INPUT.csv]] [-d OUTPUT_DIR] [-r]\n")
    print("  no arguments:   create invoice through prompts to user")
    print("  -h, --help:     display this help message and exit")
    print("  -r, --report:   generate a report of the created invoices (more useful for batches)")
    print("  -s, --singular: create singular invoice from parameters specified in config.py")
    print("  -b INPUT.CSV, --batch INPUT.CSV:     batch creates invoices from a specified .csv file")
    print("  -d DIRECTORY, --directory DIRECTORY: override output directory specified in config.py")
    print("\nFurther information available in README.md")
    print("Goodbye!")
    sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)

# TODO:
#   Implement functionality for custom invoice numbers, custom output filenames
#   Streamline command-line arguments for the above