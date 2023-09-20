#! python

"""Run script from folder. Reads all toc files in the *reprt* folder  
   and writes the toc PDF to the same folder.
   use: python -m once -s reporttoc.py
   """

import sys
import csv
import os
import glob
import shutil
from PyPDF2 import PdfFileMerger, PdfFileReader


preamble = r"""\\documentclass[12pt,notitle]{report}
% generated by Docutils <http://docutils.sourceforge.net/>
\\usepackage{fixltx2e} % LaTeX patches, \\textsubscript
\\usepackage{cmap} % fix search and cut-and-paste in Acrobat
\\usepackage{ifthen}
\\usepackage[T1]{fontenc}
\\usepackage[md8]{ }
\\usepackage{amsmath}
\\usepackage{float} % float configuration
\\floatplacement{figure}{H} % place figures here definitely
\\usepackage{graphicx}
\\setcounter{secnumSdepth}{0}

%%% User specified packages and stylesheets
\\usepackage{tabto}
\\usepackage[no-math]{fontspec}
\\usepackage{fancyhdr}
\\usepackage{titlesec}
\\usepackage[no-math]{fontspec}
\\usepackage{libertine}
\\usepackage[libertine]{newtxmath}
\\usepackage{tocloft}

%% math font
\\setmonofont{DejaVu Sans Mono}[Scale=0.8]
\\DeclareMathSizes{12}{13}{11}{11}

%% margins and page size
\\usepackage{geometry}
\\geometry{letterpaper}
\\geometry{hmargin={1.0in,0.75in},vmargin={1.3in,1.0in}}
\\setlength{\parindent}{0in}

%% pagestyle fancy
\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[L]{\\textbf{\\large\\chaptername}}
\\renewcommand\headrulewidth{1pt}
\\renewcommand\footrulewidth{1pt}
"""


preamble = preamble.replace("\\\\", "\\")
enddoc = """\\end{document}"""


def rewrite():
    """modify toc files"""
    cwd1 = os.getcwd()
    os.chdir("..")
    proj_root = os.getcwd()
    path2 = os.path.join(proj_root, "reprt")
    os.chdir(path2)
    list1 = glob.glob("*.toc")
    list1.sort()
    list2 = []
    for ending in list1:
        a = ending.replace(".toc", ".txt")
        list2.append(a)
    list3 = zip(list1, list2)
    # print(list1)
    tocpart = ""
    for inp1 in list3:
        with open(inp1[0], "r") as file2:
            lines = file2.readlines()
        with open(inp1[1], "w") as file3:
            for s0 in lines:
                s1, s2, s3, s4, S5 = "", "", "", "", ""
                for j in range(1, 50):
                    tst1 = "{chapter." + str(j) + "}"
                    s1 = s0.replace(tst1, " ")
                    tst2 = "\\numberline {" + str(j) + "}"
                    s2 = s1.replace(tst2, " ")
                    if tst2 in s1:
                        s3 = s2.replace("\\contentsline {chapter}", " ")
                        s4 = s3.replace("\hfill", " \\tabto{14cm}")
                        for k in range(1, 50):
                            tst4 = "}{" + str(k) + "}"
                            if tst4 in s4:
                                s5 = s4.replace(
                                    tst4, "}\\hfill{" + str(k) + "}")
                file3.write(s5 + "\\newline")
    writepdf(list2, path2)


def writepdf(list2, path2):
    """write toc pdf file"""
    with open("reportmerge.txt", "r") as file0:
        calclist = file0.readlines()

    bodydoc = (
        """%%% Body
    \\renewcommand\\chaptername{"""
        + calclist[0].strip()
        + """}
    \\begin{document}
    \\vspace{-0.5cm}
    \\today
    \\begin{flushright} \\textbf{Calc Number \\hspace{3mm} Page} \\end{flushright} 
    """
    )

    inx1 = -1
    tocpart = ""
    for item1 in calclist:
        if item1.split("|")[0].strip() == "c":
            inx1 += 1
            s2 = (
                """
            \\underline{\\textbf{"""
                + item1.split("|")[2].strip()
                + """}}
            \\newline
            \\input{"""
                + str(list2[inx1])
                + """}
            \\vspace{6mm}
            """
            )
        elif item1.split("|")[0].strip() == "a":
            s2 = (
                """
            \\textbf{Appendix:  }"""
                + (item1.split("|"))[2].strip()
                + """
            \\vspace{6mm}
            """
            )
        else:
            s2 = " "
        tocpart += s2
    tocstring = preamble + bodydoc + tocpart + enddoc
    with open("reporttoc.tex", "w") as file1:
        file1.write(tocstring)
    try:
        pdf1 = "latexmk -xelatex -quiet -f " + \
            os.path.join(path2, "reporttoc.tex")
        print("< pdf table of contents written to reprt folder >")
        os.system(pdf1)
    except:
        print("< pdf table of contents not written to reprt folder >")


def rmerge():
    """merge pdf files"""
    os.chdir("..")
    proj_root = os.getcwd()
    pathcalc = os.path.join(proj_root, "dbcalc")
    pathreprt = os.path.join(proj_root, "reprt")
    os.chdir(pathreprt)
    with open("reportmerge.txt", "r") as file0:
        calc1 = file0.readlines()
    calc2 = ["cover.pdf", "reporttoc.pdf"]
    for itm1 in calc1:
        if itm1.split("|")[0].strip() == "c":
            calc2.append(itm1.split("|")[1].strip())
    # print('clist', calc2)
    os.chdir(pathcalc)
    print("3", os.getcwd())
    list1 = glob.glob("*.pdf")
    print("list1", list1)
    for itm1 in list1:
        print("item", itm1)
        shutil.copy(itm1, pathreprt)
    os.chdir(pathreprt)
    merger = PdfFileMerger()
    for filename in calc2:
        merger.append(PdfFileReader(open(filename, "rb")))
    merger.write("calcreport.pdf")


def clean():
    """clean temp files"""
    try:
        os.remove("reporttoc.toc")
    except:
        pass
    cleanlist = ("*.aux", "*.out", "*.fls", "*.fdb_latexmk", "*.aux")
    for i1 in cleanlist:
        for f1 in glob.glob(i1):
            try:
                os.remove(f1)
            except OSError:
                pass


if __name__ == "__main__":
    clean()
    rewrite()
    clean()
    rmerge()