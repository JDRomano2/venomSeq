import venomseq
import os

import matplotlib.pyplot as plt

# v = venomseq.VenomSeq(
#   samples_file = "test",
#   gctx_file = "./testdata_n1000x978.gctx",
#   signatures_dir = "./signatures_test"
# )

if os.name == 'nt':
  print("Running Windows example.")
  v = venomseq.VenomSeq(
    samples_file="test",
    gctx_file = "C:\\Users\\jdr2160\\venomseq_data\\annotated_GSE92742_Broad_LINCS_Level5_COMPZ_n473647x12328.gctx"
  )
  v.load(
    wcs_file = "C:\\Users\\jdr2160\\venomseq_data\\wcs.npy",
    tau_file = "C:\\Users\\jdr2160\\venomseq_data\\tau.npy"
  )
else:
  print("Running UNIX example.")
  v = venomseq.VenomSeq(
    samples_file = "test",
    gctx_file= "/Users/jdr2160/data/cmap/annotated_GSE92742_Broad_LINCS_Level5_COMPZ_n473647x12328.gctx",
    signatures_dir = "./signatures_test/"
  )
  v.load(
    wcs_file = "/Users/jdr2160/data/venomseq/FINAL/wcs.npy",
    tau_file = "/Users/jdr2160/data/venomseq/FINAL/tau.npy"
  )

#conn = venomseq.Connectivity(v)
#conn.run()