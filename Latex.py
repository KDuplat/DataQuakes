import os.path
import re
from sympy import expand
from mainfct import mainfct
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.cm as cm
import numpy as np

#%%
foldername = ["TestLatex"]
execindicies = [[1]] 
L1 = 128
L2 = 128













#%%
def preambule(*packages):
    p = ""
    for i in packages:
        p = p+"\\usepackage{"+i+"}\n"
    return p

def insertfigure(name, dim, description):
    fig = "\\begin{figure}[h] \n  \\centering\n       "
    fig += f"\\includegraphics[width={dim}\\textwidth]{{{name}}}\n"
    fig += f"\\caption{{{description}}}\n"
    fig += "\end{figure}\n"
    return fig

def coorno(n, L1):
    x1=n%L1
    x2=n//L1
    return (x1, x2)

#%%

brutpath = "/home/kduplat/Documents/Data/Brut"


start = "\\documentclass[12pt,a4paper,french]{article}\n\\usepackage[utf8]{inputenc}\n"
start = start+preambule('amsmath','lmodern','babel','graphicx')
start = start+"\n\\begin{document}\n\n \n"
end = "\n\\end{document}"

##TROUVER UN MOYEN DE CHANGER L'ORDRE DES FIGURES DANS SNAP FIGURE

for i, project in enumerate(foldername):
    
    index = project[:2]
    projectpath = f"{brutpath}/{project}"
    rapportpath = f"/home/kduplat/Documents/Data/Rapport/{project}"
    if not os.path.exists(f"{rapportpath}") and not os.path.isdir(f"{rapportpath}"):
        os.mkdir(rapportpath)
    
    for j, exec  in enumerate(execindicies[i]):
        #We are looking for the number of folder with the name we want
        pattern = re.compile(f"^{projectpath}/{re.escape(index)}{exec}+n\d+$")
        elements = os.listdir(projectpath)
        folders = []
        for element in elements:
            completpath = os.path.join(projectpath, element)
            if os.path.isdir(completpath) and pattern.match(completpath):
                folders.append(element)
        
        for folder in folders:
            
            folderpath = f"{projectpath}/{folder}"
            #Write the parameters
            body = "\\section{Parameters used:}\n \n"
            f = open(f"{folderpath}/Para_used.par")
            
            for line in f :
                line = line.replace("#" ,"\#")
                line = line.replace("_" ,"\_")
                body += line +"\n"
            f.close()
            
            #Try to make the snapshot graph
            body += "\\newpage\n\\section{Figsnap:}\n"
            elements = os.listdir(folderpath)
            files = []
            pattern2 = re.compile(f"^{folderpath}/nav\d+_outputB.txt$")
            
            for element in elements:
                completpath = os.path.join(folderpath, element)
                if os.path.isfile(completpath) and pattern2.match(completpath):
                    files.append(element)
            
            plt.figure(figsize=(10,10)) 
            for i, file in enumerate(files):
                plt.subplot(int((len(files)/(len(files)**(1/2)))+0.5), int(len(files)/(len(files)**(1/2))), i+1)
                snapshot=np.zeros(L1*L2)   
                f = open(f"{folderpath}/{file}")
                
                j = 0
                for line in f :
                    if not line.startswith('#'):
                        col = line.strip().split("  ")
                        snapshot[j]=col[0]
                        j += 1
                
                sys=np.zeros((L1,L2))

                for n in range (L1*L2):
                    x1, x2=coorno(n, L1)
                    sys[x1][x2]=snapshot[n]
                            
                plt.imshow(sys, cmap="binary")
                plt.title(f"{file}")
                plt.colorbar()
                plt.gca().set_aspect('equal', adjustable='box')
                
            plt.savefig(f"{rapportpath}/figsnap.pdf", format = "pdf")  
            plt.show()  
                
            body += insertfigure(f"{rapportpath}/figsnap.pdf", 0.9, "Snapshots")
            
            """ print(body) """
            container = start + body + end
            filename = f"{rapportpath}/Rapport{folder}.tex"
            if os.path.exists(filename):
                os.remove(filename)
            file = open(filename,"x") # "x" pour la création et l'écriture
            file.write(container)
            file.close()
            
            instructions = f"pdflatex -output-directory={rapportpath} "+filename#"
            os.system(instructions)
            readpdf = "START "+filename+".pdf"
            os.system(readpdf)
    



    
    
