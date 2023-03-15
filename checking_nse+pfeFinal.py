#checking NSE

import csv
import numpy as np
from swmm_api import read_inp_file, SwmmInput,read_out_file
from swmm_api.input_file.section_labels import TIMESERIES,JUNCTIONS,SUBCATCHMENTS
from swmm_api import swmm5_run
from swmm_api.output_file import VARIABLES, OBJECTS

def calculatense(predictions,targets,predictions2,targets2) :
    a=0
    b=0
    a = 1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2))
    b = 1-(np.sum((predictions2-targets2)**2)/np.sum((targets2-np.mean(targets2))**2))
    c = (a+b)/2
    return(c)



def calculate_pfe(simulated_values,observed_values,simulated_values1,observed_values1):
    """
    Calculates Potential Future Exposure (PFE) given arrays of observed values and simulated values.

    Args:
        observed_values (ndarray): An array of observed exposure values.
        simulated_values (ndarray): An array of simulated exposure values.

    Returns:
        float: The calculated PFE value.
    """
    pfe=((max(observed_values)-max(simulated_values))/(max(observed_values)))
    pfe1=((max(observed_values1)-max(simulated_values1))/(max(observed_values1)))
    #pfe = np.maximum(0, np.max(simulated_values) - np.min(observed_values))
    #pfe1 = np.maximum(0, np.max(simulated_values1) - np.min(observed_values1))
    c=(pfe+pfe1)/2
    return (c)


with open('flow.csv', 'r') as infile:
  # read the file as a dictionary for each row ({header : value})
  reader = csv.DictReader(infile)
  data = {}
  for row in reader:
    for header, value in row.items():
      try:
        data[header].append(value)
      except KeyError:
        data[header] = [value]

obsdat1= data['06L95-06L98'] #Need to Modify this in Excel make sure header name is same 
obsdat2= data['06M5-06M4']
obsdat1 = list(map(float,obsdat1))
obsdat2 = list(map(float,obsdat2))
obsdat1= np.array(obsdat1)
obsdat2= np.array(obsdat2)

inp = SwmmInput.read_file('P_Tud_Sewer_V2.inp') #read input file
out = read_out_file('P_Tud_Sewer_V2.out')

zai=np.array((out.get_part(OBJECTS.LINK, '06L95-06L98', 'flow')).tolist())
yai=np.array((out.get_part(OBJECTS.LINK, '06M5-06M4', 'flow')).tolist())
nse=calculatense(zai,obsdat1,yai,obsdat2)
pfe=calculate_pfe(zai,obsdat1,yai,obsdat2)



print("NSE = ",nse,"PFE = ",pfe)
