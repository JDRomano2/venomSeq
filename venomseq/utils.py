import numpy as np

from cmapPy.pandasGEXpress.parse import parse

def read_gctx(fname, col_meta=True, row_meta=True):
  tmp = parse(fname)
  data_df = tmp.data_df

  fix_mangled_byte_literals(data_df)
  
  if (col_meta):
    cm = tmp.col_metadata_df
    fix_mangled_byte_literals(cm)
  if (row_meta):
    rm = tmp.row_metadata_df
    fix_mangled_byte_literals(rm)
  
  return (data_df, cm, rm)

def fix_mangled_byte_literals(data_df):
  columns = data_df.columns
  idx = data_df.index

  if columns[0][:2] == "b'":
    data_df.columns = [c[2:-1] for c in columns]
  if idx[0][:2] == "b'":
    data_df.index = [i[2:-1] for i in idx]

  # check if byte literals exist in the cells (e.g., if the dataframe contains metadata)
  if data_df.shape != data_df.select_dtypes(np.number).shape:
    # At least one column is nonnumeric, and needs to be checked
    for col in data_df.columns:
      colvalues = np.array(data_df.loc[:,col])
      if not np.issubdtype(colvalues.dtype, np.number):
        if colvalues[0][:2] == "b'":
          data_df.loc[:,col] = [cv[2:-1] for cv in colvalues]