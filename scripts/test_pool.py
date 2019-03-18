from multiprocessing import Pool
import numpy as np
import pandas as pd

import pdb

class ForkedPdb(pdb.Pdb):
  def interaction(self, *args, **kwargs):
    _stdin = sys._stdin
    try:
      sys.stdin = open()

X = np.random.rand(1000, 500)
total_shape = X.shape
block_ncols = 500
block_shape = (X.shape[0], block_ncols)

total_shape = np.array(total_shape)
#print(total_shape)
block_shape = np.array(block_shape)
#print(block_shape)


out_shape_tups = []
remainder = 0

if (total_shape % block_shape).sum() != 0:
  remainder = (total_shape % block_shape)[-1]
  n_cols_trim = total_shape[1] - remainder
else:
  n_cols_trim = total_shape[1]

n_blocks = int(n_cols_trim / block_ncols)
for i in range(n_blocks):
  out_shape_tups.append( (i*block_ncols, ((i+1)*block_ncols)-1) )

if remainder > 0:
  out_shape_tups.append( (total_shape[-1]-remainder, total_shape[-1]-1) )

#print(out_shape_tups)
#print()


# find sum of columns
sum_old = np.sum(X, axis=0)
sum_new = np.zeros_like(sum_old)

def colsum(start, stop):
  blk = X[:,start:stop]
  return {
    'start': start,
    'stop': stop,
    'data': np.sum(blk, axis=0)
  }

if __name__ == '__main__':
  # Do parallel computing of sums using Pool
  

  pool = Pool(processes=5)
  #print(pool.map(colsum, out_shape_tups))
  #pool.imap_unordered(colsum, out_shape_tups)
  handlers = []
  for block in out_shape_tups:
    #this_block = X[:,block[0]:block[1]]
    handlers.append(pool.apply_async(colsum, args=block))
  results = [handlers[i].get(timeout=None) for i in range(len(handlers))]
  for r in results:
    #ipdb.set_trace()
    sum_new[r['start']:r['stop']] = r['data']
  pool.close()


  print("NON-PARALLEL: {0}".format(sum_old))
  print("PARALLEL:     {0}".format(sum_new))

