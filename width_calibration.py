import csv
import numpy as np
from swmm_api import read_inp_file, SwmmInput,read_out_file
from swmm_api.input_file.section_labels import TIMESERIES,JUNCTIONS,SUBCATCHMENTS
from swmm_api import swmm5_run
from swmm_api.output_file import VARIABLES, OBJECTS


####Things to do before starting the code
#1 See the Options in SWMM and check start time end time etc can be change code too
#by  using inp.OPTIONS['START_TIME']=  check more details on format by print (inp.OPTIONS)

#2 


def calculatense(predictions,targets,predictions2,targets2) :
    a=0
    b=0
    a = 1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2))
    b = 1-(np.sum((predictions2-targets2)**2)/np.sum((targets2-np.mean(targets2))**2))
    c = (a+b)/2
    return(c)   


#############################################################
#THIS PART IS TO READ THE OBSERVED DATA FROM THE CSV FILE
#MAKE SURE THE TIME OF START OF OBSERVED DATA IS THE SAME AS TIME OF START OF SIMULATION
########################################################

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

##########################  CAN USE THESE LINES TO CHECK IF DATES MATCH OF SIMULATED DATA AND OBSERVED DATA


#wearechecking= read_out_file('P_Tud_Sewer_V2.out')
#zai=(wearechecking.get_part(OBJECTS.LINK, '06L95-06L98', 'flow'))
#print(zai)


##################################  CAN USE THESE LINES TO CHECK IF DATES MATCH OF SIMULATED DATA AND OBSERVED DATA



inp = SwmmInput.read_file('P_Tud_Sewer_V2.inp') #read input file

#print(inp.SUBCATCHMENTS[101])

rangeofvalues={'101':[33,100,190,570,1,4], '102' : [20,65,56,167,1,2], '103' : [18,57,70,209,3,8], '104' : [17,54,77,230,2,5], '105' : [7,22,71,212,3,10], '106' : [11,36,102,306,2,7], '107' : [14,46,39,116,2,5], '108' : [4,12,72,216,1,4], '109' : [13,42,102,306,2,5], '110' : [9,28,88,263,2,6], '111' : [7,23,43,129,1,3], '112' : [9,30,117,351,2,6], '113' : [32,100,67,201,2,6], '114' : [8,26,30,89,0,1], '115' : [45,100,157,470,0,1], '116' : [32,100,75,225,4,11], '117' : [45,100,9,27,3,9], '118' : [38,100,12,35,0,1], '119' : [14,46,6,18,1,2] }   ##########################need to enter 'catchment number':[a,a1,b,b1,c,c1] 




subcatchmentnumber=1                         ####################################################### Enter Subcatchment Number
bestNSE=0.9724168122101151 ################################################## Best NSE change if it shows something good   ENTER MANUALLY 



j=subcatchmentnumber

for j in (rangeofvalues): 

 print((int(j)/119)*100)


 bestwid=(inp.SUBCATCHMENTS[str(j)].width)
 bestimp=(inp.SUBCATCHMENTS[str(j)].imperviousness)   
 bestslp=inp.SUBCATCHMENTS[str(j)].slope




 z=rangeofvalues[str(j)]
 #maximp=z[1]+1
 #minimp=z[0]
 maxwid=z[3]+1
 minwid=z[2]
 #maxslp=z[5]+1
 #minslp=z[4]
 steps=(maxwid-minwid)/6


 for width in np.arange (minwid,maxwid,steps) :   ## in range (start,stop+1,step)
   print((width/maxwid)*100,"%")  
   inp.SUBCATCHMENTS[str(j)].width=width
   inp.write_file('P_Tud_Sewer_V2.inp')
   swmm5_run('P_Tud_Sewer_V2.inp', progress_size=100)
   out = read_out_file('P_Tud_Sewer_V2.out')
   zai=np.array((out.get_part(OBJECTS.LINK, '06L95-06L98', 'flow')).tolist())
   yai=np.array((out.get_part(OBJECTS.LINK, '06M5-06M4', 'flow')).tolist())
   nse=calculatense(zai,obsdat1,yai,obsdat2)
   if nse>bestNSE :
      bestwid=width
      bestNSE=nse
      print('change made NSE',bestNSE,'best width',bestwid)


############### Reset to best values and change best values if not better NSE compare once more outside loop 
      
 inp.SUBCATCHMENTS[str(j)].width=bestwid
 inp.write_file('P_Tud_Sewer_V2.inp')
 
 print('THE BEST VALUE OF NSE SO FAR',bestNSE)
 print('THE BEST VALUE OF WIDTH for Subcatchment  ',j,'is',bestwid)
 #print ( inp.SUBCATCHMENTS )
 #print ( inp.SUBCATCHMENTS[str(j)])

