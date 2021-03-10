
import numpy as np


def zScoreNormalize(v):
  '''Z-score normalizing '''
  x = np.copy(v)
  return (x - np.mean(x,axis=0).T)/np.std(x,axis=0).T

def meanNormalize(x):
  return x/np.mean(x,axis=0)

def removeNegatives(v, dmu_type):
  x = np.copy(v)
  max_val = np.max(x)
  i = -1
  prev = 0
  curr = 0
  while True:
    curr = max_val % 10 ** (i + 1)
    if curr == prev:
      break
    else:
      prev = curr
      i += 1
  if dmu_type == 'input':
    return x - (10 ** i)
  else:
    return x + (10 ** i)
  
def fillMissingData(v):
  x = np.copy(v)
  Ve = (np.nanmax(x,axis=0) + 4 * np.nanmean(x,axis=0) + np.nanmin(x,axis=0)) / 6
  #Ve = (Vo + 4*Vm + Vp) / 6
  for i in range(x.shape[0]):
    for j in range(x.shape[1]):
      if x[i,j] == np.NaN:
        x[i,j] = Ve[j]
  return x

def jenkins_corr(x,y):
  if len(x) != len(y) and len(x[0]) != len(y[0]):
    return False
  x_norm = zScoreNormalize(x)
  y_norm = zScoreNormalize(y)

  slice_ind = 1

  Vx = np.cov(x_norm,rowvar=False)
  Vy = np.cov(y_norm,rowvar=False)
  best_x = np.matrix(Vx).trace()
  best_y = np.matrix(Vy).trace()
  set_x = np.arange(Vx.shape[0])
  set_y = np.arange(Vy.shape[0])
  best_set_x = np.arange(Vx.shape[0])
  best_set_y = np.arange(Vy.shape[0])

  while slice_ind < (len(x)//3):
    Vx11 = Vx[:-slice_ind,:-slice_ind]
    Vx12 = Vx[:-slice_ind,:slice_ind]
    Vx21 = Vx[:slice_ind,:-slice_ind]
    Vx22 = Vx[:slice_ind,:slice_ind]
    Vx112 = (Vx11 - np.dot(np.dot(Vx12, np.linalg.inv(Vx22)),Vx21))

    Vy11 = Vy[:-slice_ind,:-slice_ind]
    Vy12 = Vy[:-slice_ind,:slice_ind]
    Vy21 = Vy[:slice_ind,:-slice_ind]
    Vy22 = Vy[:slice_ind,:slice_ind]
    Vy112 = (Vy11 - np.dot(np.dot(Vy12, np.linalg.inv(Vy22)),Vy21))

    traco_x = np.matrix(Vx112).trace()
    traco_y = np.matrix(Vy112).trace()

    slice_ind += 1
    if traco_x < best_x:
      best_x = traco_x
      best_set_x = set_x
    if traco_y < best_y:
      best_y = traco_y
      best_set_y = set_y
    if best_x <= 1e-6 or best_y <= 1e-6:
      break

    troca = int(np.random.choice(Vx.shape[0], 1))
    Vx[:,[0, troca]] = Vx[:,[troca, 0]]
    set_x[:,[0, troca]] = set_x[:,[troca, 0]]
    Vy[:,[0, troca]] = Vy[:,[troca, 0]]
    set_y[:,[0, troca]] = set_y[:,[troca, 0]]
  
  return best_set_x, best_set_y

def PCA(x,y, R = 0.95):
  if len(x) != len(y) and len(x[0]) != len(y[0]):
    return False
  x_norm = zScoreNormalize(x)
  y_norm = zScoreNormalize(y)
  Vx = np.cov(x_norm.T)
  Vy = np.cov(y_norm.T)
  eigen_values_x, eigen_vectors_x = np.linalg.eig(Vx)
  eigen_values_y, eigen_vectors_y = np.linalg.eig(Vy)
  var_exp_x = []
  for i in eigen_values_x:
      var_exp_x.append((i/sum(eigen_values_x))*100)
          
  print(var_exp_x)
  acc_var_exp_x = np.cumsum(var_exp_x)
  print(acc_var_exp_x)
  for i,v in enumerate(acc_var_exp_x):
    if v >= R:
      num_var_x = i

  var_exp_y = []
  for i in eigen_values_y:
      var_exp_y.append((i/sum(eigen_values_y))*100)
          
  print(var_exp_y)
  acc_var_exp_y = np.cumsum(var_exp_y)
  print(acc_var_exp_y)
  for i,v in enumerate(acc_var_exp_y):
      if v >= R:
        num_var_y = i

  projection_matrix_x = (eigen_vectors_x.T[:][:num_var_x]).T
  print(projection_matrix_x)
  projection_matrix_y = (eigen_vectors_y.T[:][:num_var_y]).T
  print(projection_matrix_y)