import venomseq

# v = venomseq.VenomSeq(
#   samples_file = "test",
#   gctx_file = "./testdata_n1000x978.gctx",
#   signatures_dir = "./signatures_test"
# )
v = venomseq.VenomSeq(
  samples_file = "test",
  gctx_file= "/Users/jdr2160/data/cmap/annotated_GSE92742_Broad_LINCS_Level5_COMPZ_n473647x12328.gctx",
  signatures_dir = "./signatures_test/"
)

print(v)

v.load(
  wcs_file = "/Users/jdr2160/data/venomseq/FINAL/wcs.npy",
  tau_file = "/Users/jdr2160/data/venomseq/FINAL/tau.npy"
)

#conn = venomseq.Connectivity(v)
#conn.run()