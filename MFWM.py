#!/usr/bin/env python3
import os
import sys

def DeltaBeta(m,p,n,N,aff_final=False):
	ind = [n+p-m,m,p,n]
	ind.sort()

	if ind.count(n+p-m) > 1:
		ind.remove(n+p-m)

	if ind.count(m) > 1:
		ind.remove(n+p-m)

	if ind.count(p) > 1:
		ind.remove(p)

	if ind.count(n) > 1:
		ind.remove(n)

	indstr = str(ind)
	indstr = indstr.replace('[','')
	indstr = indstr.replace(']','')
	indstr = indstr.replace(',','')
	indstr = indstr.replace(' ','')
	
	a = (n-m)*(p-m)
	b = (n-m)*(p-m)*(n+p-N-1)
	c = (n-m)*(p-m)*(3*(n+p-N-1)**2+(n-m)**2+(p-m)**2)
	
	txt = "\Delta \\beta_{"+indstr+"}"

	if a<0:
		txt = '-'+txt
		a = -a
		b = -b
		c = -c

	if aff_final == True:
		txt += "="+str(a)+"\Delta \omega^2 \\beta_2"

		if b != 0:
			txt += "+\\frac{"+str(b)+"}{2}\Delta \omega^3 \\beta_3"

		txt += "+\\frac{"+str(c)+"}{24}\Delta \omega^4 \\beta_4" 
		#supretion of txt = '-'+txt
		txt = txt.replace("-\Delta \\beta","\Delta \\beta")
		txt = txt.replace("1\Delta \omega^2","\Delta \omega^2")
		txt = txt.replace("+\\frac{-","-\\frac{")

	return txt

def DeltaBetatotal(N):
	text = ""
	for n in range(1,N+1):
		for p in range(1,N+1):
			M = list(range(1,N+1))
			if M.count(n) != 0:
				M.remove(n)
			
			if M.count(p)!= 0:
				M.remove(p)
			
			for m in M:
				npm=n+p-m
				if m<=npm and npm<=N:
					tmpDeltaBeta = DeltaBeta(m,p,n,N,True)
					if text.count(tmpDeltaBeta) == 0:
						text += "\n\\begin{equation}"
						text += "\n"+tmpDeltaBeta
						text += "\n\\end{equation}"
					#endif
				#endif
			#endfor
		#endfor

	return text

def lost(n):
	text = "-\\frac{\\alpha}{2}A_"+str(n)
	return text

def XPM_SPM(n,N):
	text = "+i\gamma & \\left(|A_"+str(n)+"|^2"
	counter = 0 #counter ton count the number of terms on a line
	
	Q = list(range(1,N+1))
	Q.remove(n)
	
	for q in Q:
		if counter == 5:
			#add the line jump
			text+="\\right.\\\\\\nonumber\n&\\left."
			counter = 0
		
		text += "+2|A_"+str(q)+"|^2"
		counter += 1
	text += "\\right)A_"+str(n)
	return text

def FWM(n,N):
	text = "+i\gamma & \\left("
	counter = 0 # counter to know how many terms are on a line
	
	for p in range(1,N+1):
		M = list(range(1,N+1))
		if M.count(n) != 0:
			M.remove(n)
		
		if M.count(p)!= 0:
			M.remove(p)
		
		for m in M:
			npm=n+p-m
			if m<=npm and npm<=N:
				if counter == 3:
					#add the line jump
					text += "\\right.\\\\\\nonumber\n&\\left."
					counter = 0
				#endif
				if npm == m:
					text += "+A^2_"+str(npm)+"A^*_"+str(p)+"e^{i"+DeltaBeta(m,p,n,N)+"z}"
					counter += 1
				else:
					text += "+2A_"+str(npm)+"A_"+str(m)+"A^*_"+str(p)+"e^{i"+DeltaBeta(m,p,n,N)+"z}"
					counter +=1
				#endif
			#endif
		#endfor
	text += "\\right)"
	text = text.replace("i-","-i")
	text = text.replace("(+","(")
	return text

def DA(n,N):
	return "\n\n\\begin{align}\n\\frac{dA_"+str(n)+"}{dz}="+lost(n)+XPM_SPM(n,N)+"\\\\\\nonumber\n"+FWM(n,N)+"\n\\end{align}"

def begeningoflateXfile(N):
	text = "\documentclass[12pt,a4paper]{article}"
	text += "\n\\usepackage[utf8]{inputenc}"
	text += "\n\\usepackage{amsmath}"
	text += "\n\\usepackage{amsfonts}"
	text += "\n\\usepackage{amssymb}"
	text += "\n\\usepackage{graphicx}"
	text += "\n\\title{MFWM equations automatically generated for "+str(N)+" waves}"
	text += "\n\\author{Python code}"
	text += "\n\\begin{document}"
	text += "\n\maketitle"
	return text

def endoflateXfile():
	return "\n\n\n\end{document}"




if __name__ == "__main__":
	N = int(input("How many waves do you whant to be compute? N = "))
	
	Latex_text = begeningoflateXfile(N)
	Latex_text += "\\section{Coupled equations}"
	
	for n in range(1,N+1):
		Latex_text += DA(n,N)
	
	Latex_text += "\\clearpage"
	Latex_text += "\\section{Phase mismatch $\Delta \\beta$}"
	Latex_text += DeltaBetatotal(N)
	Latex_text += endoflateXfile()
	
	
	#Write all the text in the LateX file
	print("Write all in the text file")
	file_name = str(N)+"waves_MFWM"
	file = open(file_name+'.tex', 'w')
	file.write(Latex_text)
	file.close()
	print("it's finish")
	
	print("Doing pdflatex")
	os.system("pdflatex "+file_name+".tex")
	print("pdflatex done")
	print("removing all the garbages")
	platformname = sys.platform

	if platformname == "linux":
		os.system("rm "+file_name+".aux")
		os.system("rm "+file_name+".log")

	if platformname == "win32":
		os.system("del "+file_name+".aux")
		os.system("del "+file_name+".log")
	
	print("done")
	input("Press Enter to finish")
