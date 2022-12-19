#! python
'''rivtapi 

    The *rivtapi* module is part of the *rivt* Python package and is imported
    at the beginning of a rivt calculation. It defines the five API methods:
    R(rs), I(rs), V(rs), T(rs), X(rs); where *rs* represents a *rivtText*
    string.
    
    When running in an IDE (e.g. VSCode), each method can be run interactively
    using the cell decorator # %%. In file run mode (entire file processed) the
    output is written to the screen and disk as a utf8, PDF, or HTML file.
    
    The calculation input files are separated into two folders labeled *calcs*
    and *docs*. Files in the *calcs* folder are text files under version
    control that contain the primary calculation and supporting files. They are
    designed to be shared. The *docs* folders include supporting calculation
    files that are typically binary files (images, pdf etc.) and files that
    include confidential project information or copyrights. The *docs* folder
    is typically not shared.

    Output files are written to three places. The UTF8 calc output format is
    written as a *readme.txt* file to the *calcs* folder and is automatically
    displayed on source control platforms like GitHub. The PDF output is
    written to the *reports* folder, and the HTML output is written to the
    *sites* folder.
    
    The rivt calc input file is a Python file written in *rivtText*, a superset
    markup language reStructuredText (reST) defined at
    https://docutils.sourceforge.io/rst.html. *rivtText* is designed for
    clarity and brevity when reading and writing calculation input and output.
    It may include rivt commands and tags, reStructuredText (reST) and native
    Python code. Commands start a line with || and always read or write files
    into and out of the calculation. Tags terminate a line with the symbol
    _[tag] and always evaluate or format. Block tags start the block with
    ___[tag] (three underscores) and end with a blank line.
    
    *rivtCalc* is an open source software stack for writing, sharing and
    publishing engineering calculations. The stack includes *Python*, Python
    science and engineering libraries, *VSCode*, *LaTeX (TexLive)*, *GitHub* and
    *rivt*.

    In the syntax summary below, user settings are separated by |. User
    selections are separated by semi-colons for a single selection and commas
    for multiply selectable settings. The first line of each method specifies
    formatting and labeling parameters for that rivt string. The method label
    can be a section or paragraph title, or just a label for bookmarking (see
    tags for explanation).

    ========= ==================================================================     
    API name           method, first line settings and commands
    ========= ================================================================== 
    repo      rv.R("""method label | calc title | utf;pdf;html;inter | page #
                       
                  ||text, ||table, ||github ||project
                       
                  """)
    
    insert    rv.I("""method label | /docs/folder_override;default 
                       
                  ||text, ||table, ||image, ||image2, ||append 
                  
                  """)
    
    values    rv.V("""method label | sub;nosub | /docs/folder_override;default 
                        
                  =, ||values, ||lists, ||import

                  ||text, ||table, ||image, ||image2, ||append 
                        
                  """)
    
    tables    rv.T("""method label | /docs/folder_override;default
                        
                  Python simple statements 
                  (any valid expression or statment on a single line)

                  ||text, ||table, ||image, ||image2, ||append  
                        
                  """)
    
    exclude  rv.X("""  any text           
                        
                 any commands 
                        
                 """)

    =============================================================== ============
    rivt command syntax                                               methods
    =============================================================== ============
    || github | repo_name | param1 | param                             R
                github repo parameters
    
    || project | file_name | /docsfolder; default                      R
                .txt; rst; csv; syk; xls | project info folder 
    
    || lists | file_name  |  [:];[x:y]                                    V
                .csv;.syk;.txt;.py | rows to import
     
    || values | file_name |  [:];[x:y]                                    V 
                .csv; .syk; .txt; .py | rows to import
    
    || functions | file_name |  docs; nodocs                              V
                .for; .py; .c; .c++; .jl | insert docstrings

    || image | file_name  | .50                                          I,V,T
                .png; .jpg | fraction of page width
    
    || image2 | file_name  | .40 | file_name  | .40 |                    I,V,T
                side by side images
    
    || attach | file_name | ./docfolder; default / count; nocount        I,V,T
                .pdf; .txt | pdf folder / include page numbers

    || text | file_name | shade; noshade                               R,I,V,T
                .txt; .py; .tex | shade background
    
    || table | file_name |  [:] | 60 r;l;c                             R,I,V,T
                .csv or .rst file | rows | max col width, locate text

    =====================  ===================================================== 
    rivt tag syntax                 description (user input)                
    =====================  ===================================================== 
                
                rivt string settings - first line:

    """Title |                     Denotes new section title, autonumber
    """ Title |                    Single start space - denotes paragraph title
    """  label |                   Double start space - denotes continuation    
                  
                  All other rivt string lines:

    sympy eq _[s]                 format sympy equation                
    latex eq _[x]                 format LaTeX equation                
    title _[p]                    paragraph title (centered)                        
    title _[t]                    table title, autonumber            
    caption _[f]                  figure caption, autonumber         
    text _[r]                     right justify line of text                     
    text _[c]                     center line of text                            
    text _[line]                  horizontal line - width of page        
    text _[page]                  new PDF page
    text _[#]                     footnote, autonumber                    
    footnote _[foot]              footnote description
    _[address label _url]         http://xyz link label
    _[target _lnk]                target can be - title of section, paragraph, 
                                  table or equation

    ___[literal]                  literal block, end with blank line                          
    ___[latex]                    LateX block, end with blank line                            
    ___[math]                     LaTeX math block, end with blank line                       
    ___[r]                        right justify text block, end with blank line                
    ___[c]                        center text block, end with blank line                      
                
                The following tags only apply to Values method:

    descrip _[2,2]                equation description, autonumber, decimals
    a = b + c | unit, alt         define equation, units
    a = n | unit, alt | descrip   assign value, units, description
    
    By convention the first line of a rivt file is *import rivtapi as rv*. The
    first method is always the Repo method R(rs), followed by any of the other
    four methods in any number or order. R(rs) occurs only one time and sets
    options for repository, report and calc output formats.
    
    Formatting conventions follow the Python formatter *yapf*. Method names
    start in column 1 and subsequent lines are indented 4 spaces. This
    layout supports section folding and navigation, bookmarking and improved
    legibility.

example rivt calc file  --------------------------------------------------------

import rivt.rivtapi as rv

rv.R(
    """Repo method summary | Example Calculation | inter | 1 

    The Repo method (short for repository or report) is the first method in a
    calc and specifies repository settings and output formats. It also typically
    includes a calculation summary. 

    The setting line specifies the method, paragraph or section label, the calc
    title, the processing type and the starting page number for the output.
    
    The ||github command specifies settings for updating a public rivt repo. 

    || github  | param1 | param2

    The ||project command imports data from the docs folder containing
    proprietary project data.  Its format depends on the file type.

    || project | file | default
    
    """
) 
rv.I("""Insert method summary | default

    The Insert method formats descriptive information as opposed to
    calculations and values that are stored during the calc processing.
    
    The ||text command inserts and processes text files of various types. Text
    files are always inserted as literal, without formatting.

    || text | file | shade 

    Tags _[t] and _[f] format and autonumber tables and figures.

    table title  [t]_ 
    || table | file.csv; .rst; .syk | 60r;l;c 

    || image | f1.png | 50 
    A figure caption [f]_

    Insert two images side by side: 
    || image2 | f2.png | 35 | f3.png | 45
    The first figure caption [f]_ 
    The second figure caption  [f]_

    The tags [x]_ and [s]_ format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  [x]_ 
    x = 32 + (y/2)  [s]_

    http://wwww.someurl.suffix  (label) [link]_ {formats a URL link}

    The ||attach command attaches PDF documents at the end of the method. 

    || attach | file | default | count
    """
) 
rv.V(
    """Value method summary | nosub | save | /docfolder/override

    The Value method assigns values to variables and evaluates equations. The
    first setting is the section title. The sub;nosub setting specifies whether
    equations are output with substituted numerical values. The save;nosave
    setting specifies whether equations and value assignments are written to a
    values.txt file when the calc file is run. The values write is not triggered in
    interactive mode. The docfolder setting overrides the folder containing image
    
    The = tag in an expression triggers the evaluation of values and equations.
    A block of values terminated with a blank line are formatted into tables.

    a1 = 10.1    | unit, alt | description 
    d1 = 12.1    | unit, alt | description 
    
    Example equation tag - Area of circle  _[2,2]
    a1 = 3.14*(d1/2)^2 | unit, alt 

    An equation tag; labels it with a description, auto numbers it, and
    specifies the printed decimal places in the equation and results. The
    equation tag is optional. Decimal places are retained until changed.

    The ||values command imports values from a csv or text file, where each row
    includes the variable name, value, primary unit, secondary unit, and
    description. 

    || values | file | [:]
    
    The ||lists command inserts lists from a csv, text or Python file where the
    first column is the variable name and the subsequent values make up a
    vector of values assigned to the variable.
        
    || lists | file | [:] 
  
    The ||functions method imports Python, Fortran, C or C++ functions. The
    function signature and doc strings are inserted into the calcs.

    || functions | file | docs;nodocs

    """
)
 rv.T("""Table method summary

    The Table method generates tables, plots and functions from native Python
    code. The method may include any Python simple statement (single line),
    rivt commands or tags. Any library imported at the top of the calc may be
    used, along with pandas, numpy, matplotlib and sympy library methods, which
    are imported by rivt. The four standard libraries import names are:
    
    pandas: pd.method() 
    numpy: np.method() 
    matplotlib: mp.method()
    sympy: sy.method()

    Common single line Python statements for defining functions or reading
    a file include:
    
    def f1(x,y): z = x + y; print(z); return
    
    with open('file.csv', 'r') as f: output = f.readlines()
    """
)
rv.X("""[n]_ skip-string

    Skips evaluation of the string. Used for comments and debugging. 
    """ 
) '''

import os
import sys
import subprocess
import time
import logging
import warnings
import shutil
import fnmatch
import numpy as np
from pathlib import Path
from collections import deque
import rivt._r as rM
import rivt._i as iM
import rivt._v as vM
import rivt._t as tM
import rivt.reports as rptM
import rivt.tags as tagM
import rivt.commands as cmdM

# specify test files and get paths
cfileS = "c0101_calc.py"
cfolderP = Path("./rivt_test/calcs/rv0101_test/")

for _fileS in os.listdir("."):
    if fnmatch.fnmatch(_fileS, "c[0-9][0-9][0-9][0-9]_*.py"):
        cfileS = _fileS  # calc file name
        calcfolderP = Path(os.getcwd())
        break
    else:
        print("calc file not found - check file name")
        sys.exit

# calc file full path
cbaseS = cfileS.split(".py")[0]  # calc file basename
calcbakP = Path(cfolderP / ".".join((cbaseS, "bak")))
rivtprojectP = cfolderP.parent.parent.parent  # project folder path
calcsP = cfolderP.parent.parent  # calcs folder path
cdescripS = cbaseS.split("_")[1]

docsP = Path(rivtprojectP / "docs")  # docs folder path
docnameS = "".join(["d", cbaseS[1:3], "_", cdescripS])
docfolderP = Path(docsP / docnameS _)  # doc folder path
dcfgP = Path(docsP / "d00_docs")  # doc config folder
siteP = Path(rivtprojectP / "site")  # site folder path
reportP = Path(rivtprojectP / "reports")  # report folder path
rivtcalcP = Path("rivt.rivtapi.py").parent  # rivt package path

print("INFO: calc folder is ", calcfolderP)
print("INFO: doc folder is ", docfolderP)

# check that calc and doc directories exist
for root, dir, file in os.walk(_calcsP):
    for i in dir:
        if _cfileS[0:5] == i[0:5]:
            print("INFO: calc directory is ", i)
        else:
            print("INFO: calc directory ", _curcalcP, " not found")
for root, dir, file in os.walk(_docsP):
    for i in dir:
        if "".join(["d", _cfileS[1:3]]) == i[0:3]:
            print("INFO: doc directory is ", i)
        else:
            print("INFO: doc directory ", _curdocP, " not found")

# initialize objects
utfS = """"""  # utf accumulating calc-string
rstS = """"""  # reST accumulating calc-string
exportS = """"""  # values string export
rivtD = {}  # values dictionary
_foldD = {}  # folder dict
_rstB = False  # reST generation flag
for variable in ["_rivtP", "_calcsP", "_curcalcP"]:
    _foldD[variable] = eval(variable)
for variable in ["_curdocP", "_docsP", "_dcfgP", "_siteP"]:
    _foldD[variable] = eval(variable)
_tagD = {
    "fnumS": _cbaseS[0:5],  # file number
    "cnumS": _cbaseS[1:5],  # calc number
    "dnumS": _cbaseS[1:3],  # division number
    "sdnumS": _cbaseS[3:5],  # subdivision number
    "snameS": "",  # section title
    "snumS": "",  # section number
    "swidthI": 80,  # utf section width
    "twidthI": 78,  # utf body width
    "enumI": 0,  # equation number
    "tnumI": 0,  # table number
    "fnumI": 0,  # figure number
    "ftqueL": deque([1]),  # footnote number
    "countI": 0,  # footnote counter
    "decI": 2,
    "decvI": 2,
    "subvB": False,
}
# run backups and logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename="error_log.txt",
    filemode="w",
)
logconsole = logging.StreamHandler()
logconsole.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
logconsole.setFormatter(formatter)
logging.getLogger("").addHandler(logconsole)
warnings.filterwarnings("ignore")
_rshortP = Path(*Path(_dcfgP).parts[-3:])
_lshortP = Path(*Path(_dcfgP).parts[-4:])
logging.info(f"""calc path: {_rshortP}""")
logging.info(f"""log path: {_lshortP}""")
with open(_cfileS, "r") as f2:
    calcbak = f2.read()
with open(_rvbak, "w") as f3:
    f3.write(calcbak)
logging.info(f"""calc backup written to calc folder""")
print(" ")

# set default output parameters
doctypeS = "term"
stylefileS = "rivt"
calctitleS = "Calculation"
startpageS = "1"
_rstB = False

# API methods
def R(rvS: str):
    """Reads, formats and adds processed string to calc string.

    :param str rvS: triple quoted Repo string
    """
    global utfS, rstS, valuesD, _foldD, _tagD, _rstB
    cmdL = ["project", "search", "attach"]
    rvL = rvS.split("\n")

    # set output parameters
    for iS in rvL:
        if iS.strip()[:2] == "||":
            iL = iS[2:].split("|")
            if iL[0].strip == "output":
                doctypeS = iL[1].strip()
                stylefileS = iL[2].strip()
                calctitleS = iL[3].strip()
                startpageS = iL[4].strip()
                clrS = iL[5].strip()

    if doctypeS == "inter":
        utfS += _tagM._tags(utfL[0])  # section
        rC = _rM._R2utf()
        for i in utfL[1:]:
            rC = _rM.R2utf
            utfS += rC.r_utf
        print(utfS)
    elif doctypeS == "utf":  # write utf calc file
        """write utf-calc to associated calc folder and exit"""
        f1 = open(_cfullP, "r")
        utfL = f1.readlines()
        f1.close()
        print("INFO calc file read: " + str(_cfullP))
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += _rM.r_utf(cmdL)
        # print(utfS)
        exec(utFS, globals(), locals())
        utffile = Path(_cpath / _setsectD["fnumS"] / ".".join([_cnameS, "txt"]))
        if filepathS == "default":  # check file write location
            utfpthS = Path(utffile)
        else:
            utfpthS = Path(_cpath / filepathS / ".".join((_cnameS, "txt")))

        with open(utfpthS, "wb") as f1:
            f1.write(utfcalcS.encode("UTF-8"))
        print("INFO: utf calc written to calc folder", flush=True)
        print("INFO: program complete")
        os._exit(1)
    elif doctypeS == "pdf" or doctypeS == "html":
        _rstB = True
        gen_rst(cmdS, doctypeS, stylefileS, calctitleS, startpageS)
        _rstB = True
        rcalc = _init(rvS)
        rcalcS, _setsectD = rcalc.r_rst()
        rstcalcS += rcalcS
        # clean temp files
        fileL = [
            Path(_dcfgP, ".".join([_cnameS, "pdf"])),
            Path(_dcfgP, ".".join([_cnameS, "html"])),
            Path(_dcfgP, ".".join([_cnameS, "rst"])),
            Path(_dcfgP, ".".join([_cnameS, "tex"])),
            Path(_dcfgP, ".".join([_cnameS, ".aux"])),
            Path(_dcfgP, ".".join([_cnameS, ".out"])),
            Path(_dcfgP, ".".join([_cnameS, ".fls"])),
            Path(_dcfgP, ".".join([_cnameS, ".fdb_latexmk"])),
        ]
        os.chdir(_dcfgP)
        tmpS = os.getcwd()
        if tmpS == str(_dcfgP):
            for f in fileL:
                try:
                    os.remove(f)
                except:
                    pass
            time.sleep(1)
            print("INFO: temporary Tex files deleted \n", flush=True)
        print("exit")
        os.exit(1)
    else:
        pass


def I(rvS: str):
    """Reads, formats and adds processed string to calc string.

    :param str rvS: triple quoted Insert string
    """
    global utfS, rstS, _rstB, _foldD, _tagD, _rivtD
    cmdL = ["text", "table", "image"]
    rvL = rvS.split("\n")
    iC = _iM._I2utf()  

    if doctypeS == "term":
        utfS += _tagM.tags(rvL[0])
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += iC.i_utf(cmdL)
        print(utfS)


def V(rvS: str):
    """Value-string

    Args:
        rvS: rivt-string
    """
    global utfS, rstS, _rstB, _folderD, _tagD, _rivtD, exportS
    cmdL = ["=", "list", "values", "import", "text", "table", "image"]
    rvL = rvS.split("\n")
    vC = _vM._V2utf()

    if doctypeS == "term":
        utfS += _tagM.tags(rvL[0])
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += vC.v_utf(cmdL)
        print(utfS)


def T(rvS: str):
    """table-string to utf-string

    Args:
       rvS: rivt-string
    """
    global utfS, rstS, rivtD, _rstB, _folderD, _tagD
    cmdL = ["list", "values", "import", "text", "table", "image"]
    rvL = rvS.split("\n")
    tC = _tM._T2utf()

    if doctypeS == "term":
        utfS += _tagM.tags(rvL[0])
        for i in rvL[1:]:
            utL = _tagM.tags(i, False)
            if utL[1]:
                utfS += utL[0]
                continue
            else:
                utfS += tC.t_utf(cmdL)
        print(utfS)


def X(rvS: str):
    """skip processing of rv-string

    Args:
       rvS: rivt-string
    """
    rvS
    pass
