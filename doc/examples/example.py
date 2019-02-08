import venomseq

v = venomseq.VenomSeq(
  samples_file = "test",
  gctx_file = "./testdata_n1000x978.gctx",
  signatures_dir = "./signatures_test"
)

print(v)

conn = venomseq.Connectivity(v)
conn.run()