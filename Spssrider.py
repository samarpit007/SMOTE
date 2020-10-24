import numpy as np
import pandas as pd
import pyreadstat

def distance(zero_data,raw_data,number_of_demog):
  from scipy.spatial import distance
  a=np.empty([1,raw_data.shape[1]])
  print("Shape of Raw Data ",raw_data.shape)
  for i in range(0,zero_data.shape[0]):
    x=zero_data[i,0:number_of_demog]
    min_dist=200000000
    index=-2
    for j in range(0,raw_data.shape[0]):
      y=raw_data[j,0:number_of_demog]
      dist = distance.euclidean(x, y)
      if dist<min_dist:
          min_dist=dist
          index=j
    x1=np.copy(zero_data[i,0:number_of_demog])
    x2=np.copy(raw_data[index,number_of_demog:raw_data.shape[1]])
    x3=np.append(x1,x2)
    a=np.append(a,x3.reshape(1,raw_data.shape[1]),axis=0)
    print(i+1," Zero Cells done")
  
    
  a=np.delete(a, 0, 0)
  return a

def zero_cell(vector,vector_vcol):
  temp=vector.shape
  y=temp[0]
  a=np.empty([1,vector.shape[1]])
  zero=0
  for i in range(0,y):
    index= 0
    if vector[i][vector_vcol+1]==0:
      zero=zero+1
      a=np.append(a,vector[i,:].reshape(1,vector.shape[1]),axis=0)
  print('Number of Zero Cells',zero ) 
  print('Zero Cells Done ',int(y/i*100),"%" )
  a=np.delete(a, 0, 0)
  return a

def vector_freq(vector,data,vector_vcol,data_vcol):
  temp=data.shape
  x=temp[0]
  temp=vector.shape
  y=temp[0]
  a=np.zeros([y,1])
  for i in range(0,x):

    for j in range(0,y):
      if vector[j][vector_vcol]==data[i][data_vcol]:
        a[j][0]=a[j][0]+1
        
        break
    if(i%2000==0):
        print("Frequency  Done ", int(i/x*100),"%")
  return a

def key_gen(nparray,col,row):
  x=0
  print("Key Gen Row ",row, "col ", col)
  a=np.empty([row,1],np.longlong)
  for i in range(0,row):
    text=''
    x=i
    for j in range(0,col):
      text=text+str(((int(nparray[int(i),int(j)]))))
    a[i]=text
  print(text)
  print(a[row-4:row-1])
  return a

number_of_demog=5 # the weighting variable should be the first set of varibales

#data=pd.read_csv('SMOTE1.csv')
#vector=pd.read_csv('vector_urban.csv')

data=pd.read_spss('1.sav')
vector=pd.read_csv('vector_urban.csv')


print(vector.head())
print(data.head())
print('Shape of the ICUBE Data:',data.shape )
data_raw=data.values
data_np=np.copy(data_raw[:,0:number_of_demog]) # Drop it in final run 
vector_np=vector.values
data_shape=data_np.shape
data_vcol=data_shape[-1]
vector_shape=vector_np.shape
vector_vcol=vector_shape[-1]

print('Shape of the ICUBE Data:',data_shape )
print('Shape of the Vector:',vector_shape)
print( 'Vector Collumn for Main data is', data_vcol, ' and Vector Collumn for vector  data is ', vector_vcol)

data_np_key=key_gen(data_np,number_of_demog,data_shape[0])
vector_np_key=key_gen(vector_np,number_of_demog,vector_shape[0])

data_np=np.append(data_np,data_np_key,axis=1)
vector_np=np.append(vector_np,vector_np_key,axis=1)
print("Shape of Data Key", data_np_key.shape)
print("Shape of Vector Key", vector_np_key.shape)
print("New data shape", data_np.shape)
print("New vector shape",vector_np.shape)

v_freq=vector_freq(vector_np,data_np,vector_vcol,data_vcol)
print("vector frequency shape",v_freq.shape)
vector_np=np.append(vector_np,v_freq,axis=1)
print("new vector shape",vector_np.shape)

zero_np=zero_cell(vector_np,vector_vcol)

return_data=distance(zero_np,data_raw,number_of_demog)
print("Shape of New Data: ",return_data.shape)
missing_data = pd.DataFrame(data=return_data)
print(missing_data.head())
missing_data.to_csv(r'SMor', index = False)
def missing_data():
    if (missing_data==0):
        st="-"
        print(st)
    else:
        st= missing_data
        print(st)
pyreadstat.write_sav( missing_data,'C:/ICube 2020/Universe/Zero CEll/survey_1_copy.sav' ) 