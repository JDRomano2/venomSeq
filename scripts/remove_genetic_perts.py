import numpy as np
import pandas as pd

from cmapPy.pandasGEXpress.parse import parse
from cmapPy.pandasGEXpress.write_gctx import write
from cmapPy.pandasGEXpress.GCToo import GCToo

print("Load data")
dset_full = parse("C:/users/jdr2160/venomseq_data/annotated_GSE92742_Broad_LINCS_Level5_COMPZ_n473647x12328.gctx")
cm_file = "C:/data/out_cm.h5"
rm_file = "C:/data/out_rm.h5"

cm_full = pd.read_hdf(cm_file)
rm_full = pd.read_hdf(rm_file)

print("Set mask")
mask = cm_full.pert_type.isin(['trt_cp','ctl_untrt'])

print("Subset data")
df_sub = dset_full.data_df.iloc[:,np.array(mask)]
cm_sub = cm_full.iloc[np.array(mask),:]
df_sub.columns = [c[2:-1] for c in df_sub.columns]
df_sub.index = [r[2:-1] for r in df_sub.index]

print("Write to disk")
out_gctx = GCToo(data_df=df_sub,
                 row_metadata_df=rm_full,
                 col_metadata_df=cm_sub)

write(out_gctx, "C:/data/GSE92742_cps_level5.gctx")