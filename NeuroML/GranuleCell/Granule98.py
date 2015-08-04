## Aditya Gilra, NCBS, Bangalore, 2012



import os
os.environ['NUMPTHREADS'] = '1'
import sys
sys.path.append('../../../python')
import moose
from moose.utils import *

from moose.neuroml.NeuroML import NeuroML


simdt = 1e-6 # s
plotdt = 10e-6 # s
runtime = 0.7 # s

def loadGran98NeuroML_L123(filename, nogui=False):
    neuromlR = NeuroML()
    populationDict, projectionDict = \
        neuromlR.readNeuroMLFromFile(filename)
    soma_path = populationDict['Gran'][1][0].path+'/Soma_0'
    somaVm = setupTable('somaVm',moose.Compartment(soma_path),'Vm')
    somaCa = setupTable('somaCa',moose.CaConc(soma_path+'/Gran_CaPool_98'),'Ca')
    somaIKCa = setupTable('somaIKCa',moose.HHChannel(soma_path+'/Gran_KCa_98'),'Gk')

    soma = moose.Compartment(soma_path)
    print("Reinit MOOSE ... ")
    resetSim(['/elec','/cells'],simdt,plotdt,simmethod='ee') # from moose.utils
    print("Running ... ")
    moose.start(runtime)

    if not nogui:
	from pylab import *
        tvec = arange(0.0,runtime,plotdt)
	plot(tvec,somaVm.vector[1:])
	title('Soma Vm')
	xlabel('time (s)')
	ylabel('Voltage (V)')
	figure()
	plot(tvec,somaCa.vector[1:])
	title('Soma Ca')
	xlabel('time (s)')
	ylabel('Ca conc (mol/m^3)')
	figure()
	plot(tvec,somaIKCa.vector[1:])
	title('KCa current (A)')
	xlabel('time (s)')
	ylabel('')
	print "Showing plots ..."
	show()

filename = "GranuleCell.net.xml"
if __name__ == "__main__":

    nogui = '-nogui' in sys.argv

    loadGran98NeuroML_L123("GranuleCell.net.xml", nogui)



