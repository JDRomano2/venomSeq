import venomseq

v = venomseq.VenomSeq(samples_file = "test",
                      gctx_file = "venomseq/data/testdata_n1000x978.gctx",
                      signatures_dir = "venomseq/data/signatures_test"
)

print(v)

connectivity = venomseq.Connectivity(v)