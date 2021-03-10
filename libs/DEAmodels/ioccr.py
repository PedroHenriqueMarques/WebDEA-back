import sys
import warnings

import libs.DEAmodels.io_reduction_functions as io
import libs.DEAmodels.json_manager as jm


def ioccr(x,y):
  '''
    x,y : (DMUs x INPUTS), (DMUS x OUTPUTS) two matrices with the DMUs' inputs and outputs
    sol : a dictionary containing the solution's status, vector with DMUs' efficiencies, and weights (lambdas) 
  '''
  from mip import Model, xsum, minimize, OptimizationStatus, CBC
  if len(x) != len(y):
    warnings.warn("Number of DMUs differs between input and output data.")
  if len(x[0]) < 1:
    warnings.warn("Number of inputs must be at least 1.")
  if len(y[0]) < 1:
    warnings.warn("Number of outputs must be at least 1.")
  D,I,O = range(len(x)),range(len(x[0])),range(len(y[0]))
  eff,_ll = [],[]
  gstatus = 'Failed'
  for dr in D:
    m = Model("ioccr",solver_name=CBC)
    m.verbose = 0
    theta = m.add_var(name='theta')
    ll = [m.add_var(name='l('+str(d)+')') for d in D]
    m.objective = minimize(theta)
    for i in I: 
      m += xsum(ll[d] * x[d][i] for d in D) <= x[dr][i] * theta , 'input'+str(i)
    for o in O:
      m += xsum(ll[d] * y[d][o] for d in D) >= y[dr][o], 'output'+str(o)
    status = m.optimize()
    if status != OptimizationStatus.OPTIMAL:
      warnings.warn("DMU's efficiency " + str(dr) + " failed to be obtained ")
    gstatus = 'Success'
    #m.write('ioccr'+str(dr)+'.lp')
    eff.append(m.objective_value)
    _ll.append([l.x  for l in ll])
  sol = {}
  sol['status'] = gstatus 
  sol['eff'] = eff
  sol['lambda'] = _ll
  return sol


def solveIoccr(data):
  if isinstance(data['table'], list):
    x,y = jm.get_inputs_outputs_list(data)
    sol = ioccr(x,y)
    sol = jm.get_solution_list(data,sol)
  else:
    x,y = jm.get_inputs_outputs_dict(data)
    sol = ioccr(x,y)
    sol = jm.get_solution_dict(data,sol)
  return sol


if __name__ == "__main__":
  data = jm.read_json(sys.argv[1])
  x,y = jm.get_inputs_outputs_list(data)
  print(x,y)
  sol = ioccr(x,y)
  print(sol)

