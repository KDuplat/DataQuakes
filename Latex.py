import os.path
import re
from sympy import expand
from mainfct import mainfct
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.cm as cm
import numpy as np
import math

#%%
foldername = ["TestLatex"]
execindicies = [[5]] 



#%%Hidden parameters
#Reminder: L1 is the width of the system, L2 is the lenght of the system
L1 = 0
L2 = 0
nu = -1
dim = [2]
ncifras = [1]
nbins = 12
nbfile = 1
casetab = [0]
nbava = -1
bccond = -1
zpar = -1
zmpar = -1
nshape = -1
#%%*******************FUNCTIONS***********************
def preambule(*packages):
    p = ""
    for i in packages:
        p = p+"\\usepackage{"+i+"}\n"
    return p

def insertfigure(name, dim, description):
    fig = "\\begin{figure}[h] \n  \\centering\n       "
    fig += f"\\includegraphics[width={dim}\\textwidth]{{{name}}}\n  \\centering\n"
    fig += f"\\caption{{{description}}}\n"
    fig += "\end{figure}\n"
    return fig

def coorno(n, L1):
    x1=n%L1
    x2=n//L1
    return (x1, x2)

def extract_nb(string):
    # Utilisez une expression régulière pour extraire le nombre de la chaîne
    match = re.search(r'\d+', string)
    return int(match.group()) if match else 0  # Retourne 0 si aucun nombre n'est trouvé

    

#%%*******************PARAMETERS******************

brutpath = "/home/kduplat/Documents/Data/Brut"


start = "\\documentclass[12pt,a4paper,french]{article}\n\\usepackage[utf8]{inputenc}\n"
start = start+preambule('amsmath','lmodern','babel','graphicx')
start = start+"\n\\begin{document}\n\n \n"
end = "\n\\end{document}"


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
            
            rapportfolderpath = f"{rapportpath}/{folder}"
            
            if not os.path.exists(f"{rapportfolderpath}") and not os.path.isdir(f"{rapportfolderpath}"):
                os.mkdir(rapportfolderpath)

            folderpath = f"{projectpath}/{folder}"
            #Write the parameters
            body = "\\section{Parameters used:}\n \n"
            f = open(f"{folderpath}/Para_used.par")
            
            bodypara1 = "\\subsection{Dimensions:}  \\noindent "
            bodypara2 = "\\subsection{Initial conditions:}\n \\noindent "
            bodypara3 = "\\subsection{Threshold conditions:}\n  \\noindent "
            
            #format the text to correspond to latex syntax
            for k, line in enumerate(f) :
                
                match = re.match(r'(\d+)   # L1     :lattice size x1', line)
                if match:
                    L1 = int(match.group(1))
                    bodypara1 += f"L1 : {L1}\\\ \n"
                    continue
                    
                match = re.match(r'(\d+)   # L2     :lattice size x2', line)
                if match:
                    L2 = int(match.group(1))
                    bodypara1 += f"L2 : {L2}\\\ \n"
                    continue
                    
                match = re.match(r'(\d+(\.\d+)?)   # nu    : dissipation', line)
                if match:
                    nu = float(match.group(1))
                    bodypara1 += f"Dissipation : {nu}\\\ \n"  
                    continue
                    
                match = re.match(r'(\d+(\.\d+)?(?:[eE][+-]?\d+)?)\s*#navmax\s*:\s*maximum number of avalanches', line)
                if match:
                    nbava = float(match.group(1))  
                    bodypara1 += f"Maximum number of avalanches : {nbava:.0e}\\\ \n" 
                    continue
                    
                match = re.match(r'(\d+)    #bcmode: boundary condition mode', line)
                if match:
                    bccond = int(match.group(1))          
                    if bccond == 0:
                        bodypara2 += "Open bondary conditions.\\\ \n"
                    elif bccond == 1:
                        bodypara2 += "Periodic bondary conditions on x2 and open bondary condition on x1.\\\ \n"
                    elif bccond == 2: 
                        bodypara2 += "Periodic bondary conditions on x2, open for x1 = L1 and reflectiv for x1 = 0.\\\ \n"
                    else:
                        raise ValueError("Boundary conditions found but no matching mode")
                    continue

                match = re.match(r'(\d+)   #zmode     :mode   initializing  z value', line)
                if match:
                    zpar = int(match.group(1))
                    if zpar == 0:
                        bodypara2 += "Sites initialized at 0.\\\ \n"
                    elif zpar == 1:
                        bodypara2 += "Sites initialized at a random value between 0 and 1.\\\ \n"
                    else:
                        raise ValueError("zpar found but no matching mode")
                    continue
                    
                match = re.match(r'(\d+)   #zmmode     :mode   renewing threshold', line)
                if match:
                    zmpar = int(match.group(1))
                    if zmpar == 0:
                        bodypara3 += "Threshold set to a random value between 0 and 1 and reset when toppled.\\\ \n"
                    elif zmpar == 1:
                        bodypara3 += "Threshold set to a random value between 0.9 and 1.1 and reset when toppled.\\\ \n"
                    elif zmpar == 3:
                        bodypara3 += "Threshold set to a random value following a Gaussian. NEED TO SAVE THE DEVIATION OF THE GAUSSIAN.\\\ \n"
                    elif zmpar == 4:
                        bodypara3 += "Threshold fixed at 1.\\\ \n"
                    else : 
                        raise ValueError("zmpar found but no matching mode")
                    continue
                    
                match = re.match(r'(\d+)    #Nb of avalanches where we want to see their shape', line)
                if match:
                    nshape = int(match.group(1))
                    continue
                    
                    
            if nbava == -1:
                raise ValueError("No maximum number of avalanche found")
            if nu == -1: 
                raise ValueError("No dissipation found")       
            if bccond == -1: 
                raise ValueError("No boundary condition found")
            if zpar == -1:
                raise ValueError("No z parameter found")
            if zmpar == -1:
                raise ValueError("No threshold parameter found")
            if nshape == -1:
                raise ValueError("No nshape found")
            
            body += bodypara1 + bodypara2 + bodypara3
            body += "\\subsection{Toppling:} \n \\noindent "
            body += "Toppling site gives its energy to its four neighbour and is reset to 0."
            f.close()
            
            lenghtTab = L1*L2
            alpha = [(1 - nu) / 4]
            filetab = [f"{folderpath}/Avalanche_outputB.txt"]
            
            
            
#%%*******************STATISTIQUES******************
            body += "\\newpage\n\\section{Statistiques:}\n"
            data = np.zeros(L1*L2)
            
            print("Launch of the main function")
            ndatafit, ndistloglog, disip, nstat, d1 = mainfct(alpha, ncifras, dim, lenghtTab, filetab , casetab, nbfile, nbins)
            print("End of the main function")
            
            n = 0
            c = 0
            for i in range(len(d1)):
                try:
                    n += d1[i][0]
                except ValueError:
                    n += 0
                if(n*100/nbava >90 and c == 0):
                    body += f" \\noindent 90\% of the avalanches are smaller or equal to size = {i}\\\ \n"
                    c += 1
                if(n*100/nbava >95 and c == 1):
                    body += f"95\% of the avalanches are smaller or equal to size = {i}\\\ \n"
                    c += 1
                if(n*100/nbava >99 and c == 2):
                    body += f"99\% of the avalanches are smaller or equal to size = {i}\\\ \n"
                    c += 1
                if(n*100/nbava >99.9 and c == 3):
                    body += f"99.9\% of the avalanches are smaller or equal to size = {i}\\\ \n"
                    c += 1
                    
            ndist=10**ndistloglog
            
            fig=plt.figure(figsize=(30,30))
            plt.plot(ndist[0,:,0],ndist[0,:,1],'ok-',linewidth=1,markersize=6,mec="k", mfc="none") 
            plt.axis([9*10**-1, 10**5, 10**-10, 1])
            plt.xscale("log")
            plt.yscale("log")
            plt.xlabel('s(number of sites, fontsize=20) ', fontsize=40)
            plt.ylabel('P(s) ', fontsize=40)
            plt.tick_params(labelsize=40) 
            plt.show()
            plt.savefig(f"{rapportfolderpath}/distrib.pdf", format = "pdf")  
            body += insertfigure(f"{rapportfolderpath}/distrib.pdf", 0.99, "Probability distribution")
            
            
#%%******************SHAPE OF THE LAST AVALANCHES******************
            body += "\\newpage\n\\section{Shape of the last 1000 ava:}\n"
            plt.figure(figsize=(30,30)) 

            colors = iter(cm.rainbow(np.linspace(0, 1, nshape+1)))
            f=f"{folderpath}/shape_outputB.txt"
            shape = open(f, "r")

            for i, line in enumerate(shape):
                x1, x2 = [], []
                col = line.strip().split()
                for n in range(len(col)):
                    x1_value, x2_value = coorno(int(col[n]), L1)
                    x1.append(x1_value)
                    x2.append(x2_value)
                    
                plt.scatter(x2,x1, s = 10, color = next(colors), alpha = 0.5)
                    
                plt.axis([0, L2, 0, L1])
                plt.gca().set_aspect('equal', adjustable='box')
                
            plt.show()
            plt.savefig(f"{rapportfolderpath}/shape.pdf", format = "pdf")  
            body += insertfigure(f"{rapportfolderpath}/shape.pdf", 0.99, "Shape of the last 1000 avalanches")
            shape.close()
            
#%%****************POSITION OF THE LAST AVA**********************
            plt.figure(figsize=(30,30)) 
            body += "\\newpage\n\\section{Initial position of the last 1000 ava:}\n"
            
            fpos = open(f"{folderpath}/Avalanche_outputB.txt", "r")
            colors = iter(cm.rainbow(np.linspace(0, 1, nshape+1)))
            c = 0
            for line in fpos:
                c += 1
                if c >= (nbava - nshape):
                    col = line.strip().split()
                    
                    x1, x2 = coorno(int(col[2]), L1)
                    plt.scatter(x2,x1, s = 50, color = next(colors), alpha = 0.5)
            
            plt.axis([0, L2, 0, L1])
            plt.tick_params(labelsize=50) 
            plt.gca().set_aspect('equal', adjustable='box')
            plt.show()
            plt.savefig(f"{rapportfolderpath}/position.pdf", format = "pdf")  
            
            fpos.close()
            
            body += insertfigure(f"{rapportfolderpath}/position.pdf", 0.99, "Initial position of the last 1000 avalanches")
            
            
            
            
#%%********************SNAPSHOTS**********************
            body += "\\newpage\n\\section{Figsnap:}\n"
            elements = os.listdir(folderpath)
            files = []
            pattern2 = re.compile(f"^{folderpath}/nav\d+_outputB.txt$")
            
            for element in elements:
                completpath = os.path.join(folderpath, element)
                if os.path.isfile(completpath) and pattern2.match(completpath):
                    files.append(element)
            
            files = sorted(files, key = extract_nb, reverse = True)
            dimplot = len(files)/(len(files)**(1/2))
            
            if len(files) > 9:
                dimplot = 3
                
            plt.subplots_adjust(wspace=0.2, hspace=0.2)
            k = 1
            l = 1
            for  file in files:
                if k == 1:
                    plt.figure(figsize=(50,50)) 
                    
                ax = plt.subplot(round(dimplot+0.5), round(dimplot), k)
                snapshot = np.zeros(L1*L2)   
                f = open(f"{folderpath}/{file}")
                match = re.search(r'\d+', file)
                nava = int(match.group())
                
                j = 0
                for line in f :
                    if not line.startswith('#'):
                        col = line.strip().split("  ")
                        snapshot[j] = col[0]
                        j += 1
                
                sys = np.zeros((L1,L2))
                for n in range (L1*L2):
                    x1, x2 = coorno(n, L1)
                    sys[x1][x2] = snapshot[n]
                            
                plt.imshow(sys, cmap = "binary")
                plt.title(f"{nava:.1e} avalanches", fontsize=40)
                plt.colorbar()
                plt.gca().set_aspect('equal', adjustable = 'box')
                plt.tick_params(labelsize=35) 
                
                
                if k == 9:
                    plt.savefig(f"{rapportfolderpath}/figsnap{l}.pdf", format = "pdf") 
                    body += insertfigure(f"{rapportfolderpath}/figsnap{l}.pdf", 0.99, "Snapshots")
                    body += "\\newpage \n"
                    l += 1
                    k = 1
                    ax.remove()
                else:
                    k += 1
                
                
        
            
            
#%%**********************Evolution Simulation time*************************
            body += "\\section{Time evolution:}\n"
            
            loaddata= np.loadtxt(f"{folderpath}/time_outputB.txt", comments="#")
            
            plt.figure(figsize=(30,30))
            plt.scatter(loaddata[:,0], loaddata[:,2], color = "b")
            plt.xlabel("Number of avalanges", size = 40)
            plt.ylabel("Average time of the last 1000 avalanches", size = 45)
            plt.xscale("log")
            plt.gca().xaxis.get_offset_text().set_fontsize(40)
            plt.xticks(size=35)
            plt.yticks(size=35)
            plt.savefig(f"{rapportfolderpath}/time.pdf", format = "pdf")  
            plt.show()
            body += insertfigure(f"{rapportfolderpath}/time.pdf", 0.9, "Evolution of the simulation time")
            
#%% WRITE THE LATEX FILE
            container = start + body + end
            filename = f"{rapportfolderpath}/Rapport{folder}.tex"
            if os.path.exists(filename):
                os.remove(filename)
            file = open(filename,"x") # "x" pour la création et l'écriture
            file.write(container)
            file.close()
            
            instructions = f"pdflatex -output-directory={rapportfolderpath} "+filename#"
            os.system(instructions)
            readpdf = "START "+filename+".pdf"
            os.system(readpdf)
    



    
    
