from collections import namedtuple
from glob import glob
import pandas as pd
import numpy as np
import os

from .utils import read_gctx

SYMBOL_MAP_FNAME = os.path.join(os.path.dirname(__file__), "data", "symbol_map.npy")

class VenomSeq(object):
  def __init__(self,
    #           counts_file = None,
               samples_file = None,
               gctx_file = None,
               signatures_dir = None):
    #self.counts_file = counts_file
    self.samples_file = samples_file  # Metadata describing venom samples
    self.gctx_file = gctx_file
    self.signatures_dir = signatures_dir

    self.cmap = self.read_reference_dataset()
    self.signatures = self.read_signatures()

    self.init_connectivity()

    # Handle gene symbols
    self.hsap_symbol_map = np.load(SYMBOL_MAP_FNAME)
    self.cmap_genes = self.process_cmap_genes()

  def __repr__(self):
    """Return a string that summarizes the data loaded into the VenomSeq
    object. This should look something like the output of `summary()` in R.
    """
    return """VenomSeq object of {0} venom signatures.
    """.format(
      len(self.signatures)
    )

  def init_connectivity(self):
    ConnectivityData = namedtuple('ConnectivityData', ['wcs','ncs','tau'])
    self.connectivity = ConnectivityData(wcs=None, ncs=None, tau=None)

  def load(self,
           wcs_file=None,
           ncs_file=None,
           tau_file=None):
    """Load precomputed VenomSeq data from local files.
    """
    if not (wcs_file or ncs_file or tau_file):
      raise Exception('Must supply at least one filename argument to load().')

    if wcs_file is not None:
      self.connectivity.wcs = np.load(wcs_file)
    if ncs_file is not None:
      self.connectivity.ncs = np.load(ncs_file)
    if tau_file is not None:
      self.connectivity.tau = np.load(tau_file)

  def process_cmap_genes(self):
    """Parse an integer-valued list of NCBI gene IDs corresponding
    to the individual rows of the CMap data table.

    GCTX metadata tables don't always conform to a standard, so this
    code may necessarily become messy to account for edge-cases as
    they are encountered.
    """
    cmap_genes = self.cmap.rows.index
    if cmap_genes[0][-3:] == '_at':
      # We need to look in a different column for the gene IDs
      cmap_genes = self.cmap.rows['pr_gene_id'].astype(int).tolist()
    return cmap_genes

  def read_reference_dataset(self):
    CMap = namedtuple('CMap', ['data', 'cols', 'rows'])
    data_df, cm, rm = read_gctx(self.gctx_file)
    return CMap(data=data_df, cols=cm, rows=rm)

  def read_signatures(self):
    sig_files = glob("{0}/*.csv".format(self.signatures_dir))
    sigs_pd = []
    sigs = []

    for f in sig_files:
      v = f.split("/")[-1].split(".")[0]
      sig = pd.read_csv(f, sep=",")
      sig = sig[pd.notnull(sig['symbol'])]
      sigs_pd.append((v, sig))

    for s in sigs_pd:
      i, sig = s
      n_down = sig.loc[sig['log2FoldChange'] < 0].shape[0]
      n_up = sig.loc[sig['log2FoldChange'] > 0].shape[0]
      sigs.append({
        'venom': i,
        'n_up': n_up,
        'n_down': n_down,
        'up': np.array(sig.loc[sig['log2FoldChange'] > 0]),
        'up_list': list(np.array(sig.loc[sig['log2FoldChange'] > 0])[:,1]),
        'down': np.array(sig.loc[sig['log2FoldChange'] < 0]),
        'down_list': list(np.array(sig.loc[sig['log2FoldChange'] < 0])[:,1]),
      })

    return sigs

  def compute_connectivities(self):
    pass

  def normalize_connectivities(self):
    pass

  def compute_taus(self):
    pass

  def compute_pcl_enrichments(self):
    pass