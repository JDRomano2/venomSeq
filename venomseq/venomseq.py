class VenomSeq(object):
  def __init__(self, counts_file = None, samples_file = None):
    self.counts_file = counts_file
    self.samples_file = samples_file  # Metadata describing samples

  def summarize(self):
    pass

  def read_counts_data(self):
    pass

  def read_reference_dataset(self):
    pass

  def compute_connectivities(self):
    pass
  
  def normalize_connectivities(self):
    pass

  def compute_taus(self):
    pass

  def compute_pcl_enrichments(self):
    pass