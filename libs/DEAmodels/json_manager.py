import json
import os
import warnings

def read_json(file_name):
  '''
  file_name : file name containing the inputs and outputs of the dmus
  data : returns a dictionary with the data table 
  '''
  if os.path.isfile(file_name) == False:
    warnings.warn(file_name + " doesn't exist!")
  
  with open(file_name) as f:
    data = json.load(f)
    tb = json.loads(json.loads(data['table']))
    data['table'] = tb
    return data 


def get_inputs_outputs_list(data):
  '''
    data : a dictionary with a data table with inputs and outputs of the dmus row-wise organized
    x,y : (DMUs x INPUTS), (DMUS x OUTPUTS) two matrices with the DMUs' inputs and outputs
  '''
  tb = data['table']
  Input, Output = [],[]

  for key, val in tb[0].items():
    if val == 'Input':
        Input.append(key)
    if val == 'Output':
        Output.append(key)
  
  x,y = [],[]
  
  for r in tb[1:]: 
    X,Y = [],[]
    for key,val in r.items():
      if key in Input:
          X.append(float(val))
      if key in Output:
          Y.append(float(val))
    x.append(X),y.append(Y)
  
  return x,y  


def get_inputs_outputs_dict(data):
  '''
  data : a dictionary with a data table with inputs and outputs of the dmus row-wise organized
  x,y : (DMUs x INPUTS), (DMUS x OUTPUTS) two matrices with the DMUs' inputs and outputs
  '''
  tb = data['table']
  Input, Output = [],[]
  x,y = [],[]

  for k in tb.keys():
    if tb[k]["0"] == 'Input':
      Input.append(k)
    if tb[k]["0"] == 'Output':
      Output.append(k)
  
  for k in tb.keys(): 
    X,Y = [],[]
    for i in range(1,len(tb[k])):
      try:
        value = float(tb[k][str(i)])
      except ValueError:
        continue
      except TypeError:
        continue
      if k in Input:
        X.append(value)
      if k in Output:
        Y.append(value)
    
    x.append(X),y.append(Y)
  
  x = [i for i in x if i]
  y = [i for i in y if i]
  x = list(map(list, zip(*x)))
  y = list(map(list, zip(*y)))

  return x,y


def get_solution_list(data, sol):
  '''
  data : a dictionary with a data table with inputs and outputs of the dmus row-wise organized
  sol : solution found by the model
  x,y : (DMUs x INPUTS), (DMUS x OUTPUTS) two matrices with the DMUs' inputs and outputs
  '''
  tb = data['table']

  DMU_list = []
  for item in tb:
    for k,v in item.items():
      if k == 'DMU':
        DMU_list.append(v)
      else:
        break
    
  DMU_list.pop(0)  
  sol_out = sol.copy()
  
  for k,v in sol_out.items():
    if isinstance(v, list):
      for i,x in enumerate(v):
        if k == 'lambda':
          temp = {}
          temp['DMU'] = DMU_list[i]
          for j in range(len(x)):
            temp[DMU_list[j]] = round(x[j],2)
          
          sol_out[k][i] = temp
        else:
          sol_out[k][i] = {k: DMU_list[i], "value" : round(x,2)}
  
  return sol_out


def get_solution_dict(data, sol):
  '''
  data : a dictionary with a data table with inputs and outputs of the dmus row-wise organized
  sol : solution found by the model
  x,y : (DMUs x INPUTS), (DMUS x OUTPUTS) two matrices with the DMUs' inputs and outputs
  '''
  tb = data['table']

  DMU_list = [tb['DMU'][str(i)] for i in range(1,len(tb['DMU']))]
  sol_out = sol.copy()

  for k,v in sol_out.items():
    if isinstance(v, list):
      for i,x in enumerate(v):
        if k == 'lambda':
          temp = {}
          for j in range(len(x)):
            temp[DMU_list[j]] = round(x[j],2)
          temp[k] = DMU_list[i]
          sol_out[k][i] = temp
        else:
          sol_out[k][i] = {k: DMU_list[i], "value" : round(x,2)}
          
  return sol_out

