import os.path
import re
#%%
foldername = ["TestLatex"]
execindicies = [[1]] 














#%%
def preambule(*packages):
    p = ""
    for i in packages:
        p = p+"\\usepackage{"+i+"}\n"
    return p

Brutpath = "/home/kduplat/Documents/Data/Brut"
Rapportpath = "/home/kduplat/Documents/Data/Rapport"


start = "\\documentclass[12pt,a4paper,french]{article}\n\\usepackage[utf8]{inputenc}\n"
start = start+preambule('amsmath','lmodern','babel')
start = start+"\\begin{document}\n\\begin{align*}\n"
end = "\\end{align*}\n\\end{document}"

body = ""

for i, project in enumerate(foldername):
    
    index = project[:2]
    projectpath = f"{Brutpath}/{project}"
    rapportpath = f"/home/kduplat/Documents/Data/Rapport/{project}"
    if not os.path.exists(f"{rapportpath}") and not os.path.isdir(f"{rapportpath}"):
        os.mkdir(rapportpath)
    
    for j, exec  in enumerate(execindicies[i]):
        
        pattern = re.compile(f"^{projectpath}/{re.escape(index)}{exec}+n\d+$")
        print(pattern)
        elements = os.listdir(projectpath)
        print(elements)
        folders = []
        for element in elements:
            completpath = os.path.join(projectpath, element)
            if os.path.isdir(completpath) and pattern.match(completpath):
                folders.append(element)
                
        print(folders)
        
        for folder in folders:
                
            #Write the parameters
            body += "Parameter used:\n"
            f = open(f"{projectpath}/{folder}/Para_used.par")
            for line in f :
                body += line +"\n"
                
            
            container = start+body+end
            filename = f"{rapportpath}/Rapport{folder}.tex"
            if os.path.exists(filename):
                os.remove(filename)
            file = open(filename,"x") # "x" pour la création et l'écriture
            file.write(container)
            file.close()
            
            instructions = "pdflatex "+filename#"
            os.system(instructions)
            readpdf = "START "+filename+".pdf"
            os.system(readpdf)
    



    
    
