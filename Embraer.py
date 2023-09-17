import numpy as np
import matplotlib.pyplot as plt


def CriaL(x0,y0,xf,yf,xobj,yobj,nx,ny,passoX,passoY):
	Lcoor = []
	for i in range(0,ny):
		y = y0+i*passoY
		for j in range (0,nx):
			x = x0+j*passoX
			Lcoor.append([np.sqrt((x-xobj)**2+(y-yobj)**2),x,y])
		
	return Lcoor
		
def GeraInterferencia(Ondamot1,Ondamot2,Ondacanc1,Ondacanc2):
	Ondagraf = []
	for i in range(0,len(Ondamot1)):
		Ondagraf.append([Ondamot1[i][0]+Ondamot2[i][0]+Ondacanc1[i][0]+Ondacanc2[i][0],Ondamot1[i][1],Ondamot1[i][2]])
	return Ondagraf
				
def CriaOnda(L,A,k,w,t,fase):
	Onda1 = []
	for j in range(0,len(L)):
		M = L[j]
		if M[0] != 0:
			M[0] = A*np.cos(k*M[0]-w*t+fase)/M[0]
		M.append(t)
		Onda1.append(M)
	return Onda1
			
def GeraGrafico(Onda,nome):
	A_values = [point[0] for point in Onda]
	x_values = [point[1] for point in Onda]
	y_values = [point[2] for point in Onda]
	
	fig = plt.figure(figsize=(32, 24))
	
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	scatter = ax.scatter(x_values, y_values, A_values, c=A_values, cmap='plasma')  # Change 'coolwarm' to your desired colormap
	
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('A')
	nome = str(int(nome))
	titulo = "Amplitudes, t(0.1ms) = "+nome
	s = "Apresentar"+nome+".png"
	plt.title(titulo)
	fig.colorbar(scatter, shrink=0.5, aspect=5)
	plt.savefig(s)
	
def CalculaEficiencia(Onda):
	A2 = 0
	out = 0
	for i in Onda:
		if i[0] <3:
			A2+=i[0]**2
		else:
			out+=1
	return A2/(len(Onda)-out)

def ProgramaGeraOnda(passoX,passoY,x0,xf,y0,yf,t,dt,fi0,w,k,nx,ny,nt,xcanc1,xcanc2,ycanc1,ycanc2,Acanc,fi1,Ondamot1,Ondamot2,nome):
	Lcanc1 = CriaL(x0,y0,xf,yf,xcanc1,ycanc1,nx,ny,passoX,passoY)
	Ondacanc1 = CriaOnda(Lcanc1,Acanc,k,w,t,fi1)
	Lcanc2 = CriaL(x0,y0,xf,yf,xcanc2,ycanc2,nx,ny,passoX,passoY)
	Ondacanc2 = CriaOnda(Lcanc2,Acanc,k,w,t,fi1)
	Onda = GeraInterferencia(Ondamot1,Ondamot2,Ondacanc1,Ondacanc2)
	GeraGrafico(Onda,(nome/dt)//1)
	print("Numero base Cancelador: ",CalculaEficiencia(Onda))
	
	
	
def ProgramaCalculaFase(passo,x0,xf,y0,yf,t0,tf,dt,fi0,w,k,nx,ny,nt,xcanc1,xcanc2,ycanc1,ycanc2,Acanc,fi1,Ondamot1,Ondamot2):
	Lcanc1 = CriaL(x0,y0,xf,yf,xcanc1,ycanc1,nx,ny,passo)
	Efic = 10
	while fi1<3.14:
		Ondacanc1 = CriaOnda(Lcanc1,Acanc,k,w,t0,dt,nt,fi1)
		Onda = GeraInterferencia(Ondamot1,Ondamot2,Ondacanc1,Ondamot2)
		ef = CalculaEficiencia(Onda)
		if ef < Efic:
			Efic = ef
			FI = fi1
		fi1 +=0.01
	return(FI)


def ProgramaCalculaAmplitude(passo,x0,xf,y0,yf,t0,tf,dt,fi0,w,k,nx,ny,nt,xcanc1,xcanc2,ycanc1,ycanc2,Acanc,fi1,Ondamot1,Ondamot2):	
	Efic = 10
	Lcanc1 = CriaL(x0,y0,xf,yf,xcanc1,ycanc1,nx,ny,passo)
	Efic = 10
	while Acanc<0.5:
		Ondacanc1 = CriaOnda(Lcanc1,Acanc,k,w,t0,dt,nt,fi1)
		Onda = GeraInterferencia(Ondamot1,Ondamot2,Ondacanc1,Ondamot2)
		ef = CalculaEficiencia(Onda)
		if ef < Efic:
			Efic = ef
			Amp = Acanc
		Acanc +=0.01
		
	return(Amp)

def GeraFotos(passoX,passoY,x0,xf,y0,yf,t0,tf,dt,fi0,w,k,nx,ny,nt,xcanc1,xcanc2,ycanc1,ycanc2,Acanc,fi1,xmot1,xmot2,ymot1,ymot2,A,fi):
	for i in range(0,nt):
		t = t0+i*dt
		Lmot1 = CriaL(x0,y0,xf,yf,xmot1,ymot1,nx,ny,passoX,passoY)
		Ondamot1 = CriaOnda(Lmot1,A,k,w,t,fi)
		Lmot2 = CriaL(x0,y0,xf,yf,xmot2,ymot2,nx,ny,passoX,passoY)
		Ondamot2 = CriaOnda(Lmot2,A,k,w,t,fi)
		ProgramaGeraOnda(passoX,passoY,x0,xf,y0,yf,t,dt,fi0,w,k,nx,ny,nt,xcanc1,xcanc2,ycanc1,ycanc2,Acanc,fi1,Ondamot1,Ondamot2,t)
def main():
	passoX = 0.0075 #Passo cartesiano de simulação(x e y)
	passoY = 0.1
	x0 = 6.5 #x inicial de simulação
	xf = 12 #x final de simulação
	y0 = -1 # y inicial de simução
	yf = 1 # y final de simulação
	
	t0 = 0 #tempo inicial simulação
	tf = .01 #tempo final de simulação
	dt = 0.0001 #passo temporal
	ntempo = (tf-t0)/dt
	fi0 = 0 #Fase inicial Motor
	k = 90 #Número de onda, 2pi/lambda
	w = 340*k #Frequência angular, 2pi*f
	nx = int(((xf-x0)/passoX)//1)+1
	ny = int(((yf-y0)/passoY)//1)+1
	nt = int(((tf-t0)/dt)//1)	+1
	
	xmot1 = 0 # coordenada x do motor 1
	xmot2 = 0 # coordenada x do motor 2
	ymot1 = 1 # coordenada y do motor 1
	ymot2 = -1 # coordenada y do motor 2
	A = 1 #Amplitude do motor
	fi = 0.0 #Fase do motor. A princípio, sempre 0)
	
	xcanc1 = 5.6 #coordenada x do cancelador 1
	xcanc2 = 0 #coordenada x do cancelador 2
	ycanc1 = .5 #coordenada y do cancelador 1
	ycanc2 = -.5 #coordenada y do cancelador 2
	Acanc = 0.2 #amplitude do cancelador
	fi1 = -.65 #diferença de fase cancelador1
	modo = 2
	
	if modo ==1:
	
		Lmot1 = CriaL(x0,y0,xf,yf,xmot1,ymot1,nx,ny,passoX,passoY)
		Ondamot1 = CriaOnda(Lmot1,A,k,w,t0,fi)
		Lmot2 = CriaL(x0,y0,xf,yf,xmot2,ymot2,nx,ny,passoX,passoY)
		Ondamot2 = CriaOnda(Lmot2,A,k,w,t0,fi)
		ProgramaGeraOnda(passoX,passoY,x0,xf,y0,yf,t0,dt,fi0,w,k,nx,ny,nt,xcanc1,xcanc2,ycanc1,ycanc2,Acanc,fi1,Ondamot1,Ondamot2,t0)
	if modo ==2:
		GeraFotos(passoX,passoY,x0,xf,y0,yf,t0,tf,dt,fi0,w,k,nx,ny,nt,xcanc1,xcanc2,ycanc1,ycanc2,Acanc,fi1,xmot1,xmot2,ymot1,ymot2,A,fi)
	
main()
