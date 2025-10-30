"""
Práctica 3: Sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Aron Cervantes Armenta
Número de control: 22212250
Correo institucional: L22212250@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
n = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,n)
u = np.zeros(n); u[round(1/dt):round(2/dt)] = 1

def funcion(a,Cs,Cp,R): 
    num = [Cs*R, 1 -a]
    den = [R*(Cp+Cs), 1]
    sys = ctrl.tf(num,den)
    return sys

#Función de transferencia: Control
a,Cs,Cp,R = 0.25, 10E-6, 100E-6, 100
sysControl = funcion(a,Cs,Cp,R)
print(f'Función de transferencia del control:{sysControl}')

#Función de transferencia: Caso
a,Cs,Cp,R = 0.25, 10E-6, 100E-6, 10E3
sysCaso = funcion(a,Cs,Cp,R)
print(f'Función de transferencia del caso:{sysCaso}')

_,Fs1 = ctrl.forced_response(sysControl,t,u,x0)
_,Fs2 = ctrl.forced_response(sysCaso,t,u,x0)

fg1 = plt.figure() # Sin tratamiento
plt.plot(t,u,'-',linewidth=1,color=[0.4980,0.2980,0.6471],label='Ve(t)')
plt.plot(t,Fs1,'-',linewidth=1,color=[0.0196,0.4980,0.4275],label='Fs(t): Control')
plt.plot(t,Fs2,'-',linewidth=1,color=[0.8745,0.2235,0.4118],label='Fs(t): Caso')
plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.2); plt.yticks(np.arange(-0.1,1.2, 0.2))
plt.xlabel('t(s)')
plt.ylabel('Fi(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('Sistema musculoesqueletico python.png', dpi=600,bbox_inches='tight')
fg1.savefig('Sistema musculoesqueletico python.pdf')

def tratamiento(kP,kI,sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    PI = ctrl.tf(numPI, denPI)
    X = ctrl.series(PI,sys)
    sysPI = ctrl.feedback(X,1,sign=-1)
    return sysPI

CasoPI = tratamiento(0.020982,43250.2057,sysCaso)

_,Fs3 = ctrl.forced_response(CasoPI, t, Fs1 ,x0)

fg2 = plt.figure() # Con tratamiento
plt.plot(t, u,'-', linewidth=1,color=[0.4980,0.2980,0.6471],label='F(t)')
plt.plot(t,Fs1,'-',linewidth=1,color=[0.0196,0.4980,0.4275],label='Fs(t): Control')
plt.plot(t,Fs2,'-',linewidth=1,color=[0.8745,0.2235,0.4118],label='Fs(t): Caso')
plt.plot(t,Fs3,':',linewidth=1,color=[0.2000,0.7804,0.8471],label='Fs(t): Tratamiento')
plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.2); plt.yticks(np.arange(-0.1,1.2, 0.2))
plt.xlabel('Fs(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('Sistema musculoesquelético PI python.png', dpi=600,bbox_inches='tight')
fg2.savefig('Sistema musculoesquelético PI python.pdf')