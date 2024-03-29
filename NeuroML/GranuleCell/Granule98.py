## Aditya Gilra, NCBS, Bangalore, 2012

"""
Inside the .../moose-examples/GranuleCell/ directory supplied with MOOSE, run
python testNeuroML_Gran98.py
(other channels and morph xml files are already present in this same directory).
The soma name below is hard coded for gran98, else any other file can be used by modifying this script.
"""
import os
os.environ['NUMPTHREADS'] = '1'
import sys
#sys.path.append('../../../python')
import moose
from moose.utils import setupTable, resetSim

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
    somaIKCa = setupTable('somaIKCa',moose.element(soma_path+'/Gran_KCa_98'),'Gk')
    #KDrX = setupTable('ChanX',moose.element(soma_path+'/Gran_KDr_98'),'X')
    soma = moose.Compartment(soma_path)
    print("Reinit MOOSE ... ")
    resetSim(['/elec','/cells'],simdt,plotdt,simmethod='ee') # from moose.utils
    print("Running ... ")
    moose.start(runtime)
    print("Finished simulation of %s seconds"%runtime)

    if not nogui:
        import pylab
        import numpy as np
        tvec = np.arange(0.0,runtime,plotdt)
        pylab.plot(tvec,somaVm.vector[1:])
        pylab.title('Soma Vm')
        pylab.xlabel('time (s)')
        pylab.ylabel('Voltage (V)')
        pylab.figure()
        pylab.plot(tvec,somaCa.vector[1:])
        pylab.title('Soma Ca')
        pylab.xlabel('time (s)')
        pylab.ylabel('Ca conc (mol/m^3)')
        pylab.figure()
        pylab.plot(tvec,somaIKCa.vector[1:])
        pylab.title('KCa current (A)')
        pylab.xlabel('time (s)')
        pylab.ylabel('')
        print("Showing plots ...")
        pylab.show()

filename = "GranuleCell.net.xml"

if __name__ == "__main__":
    nogui = False
    if '-nogui' in sys.argv:
        nogui = True
        sys.argv.remove('-nogui')

    if len(sys.argv)<2:
        filename = "GranuleCell.net.xml"
    else:
        filename = sys.argv[1]

    loadGran98NeuroML_L123(filename, nogui)
