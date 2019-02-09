from collections import namedtuple
from glob import glob
import pandas as pd
import numpy as np
import os
import json

from .utils import read_gctx
from .visualizations import *

SYMBOL_MAP_FNAME = os.path.join(os.path.dirname(__file__), "data", "symbol_map.npy")
DEFAULT_PCL_FNAME = os.path.join(os.path.dirname(__file__), "data", "pcls.json")

class VenomSeq(object):
  def __init__(self,
               samples_file = None,
               gctx_file = None,
               signatures_dir = None,
               pcls_file = DEFAULT_PCL_FNAME,
               verbose = True):
    #self.counts_file = counts_file
    self.verbose = verbose
    self.samples_file = samples_file  # Metadata describing venom samples
    self.gctx_file = gctx_file
    self.pcls_file = pcls_file
    self.signatures_dir = signatures_dir

    if self.verbose:
      print("Loading reference dataset; this may take a while...")
    self.cmap = self.read_reference_dataset()
    if self.verbose:
      print("...done.")
    self.signatures = self.read_signatures()

    self.init_connectivity()

    if self.verbose:
      print("Loading gene symbol data.")
    # Handle gene symbols
    self.hsap_symbol_map = np.load(SYMBOL_MAP_FNAME)
    self.cmap_genes = self.process_cmap_genes()

    if self.verbose:
      print("Parsing perturbagen class (PCL) data.")
    with open(self.pcls_file, 'r') as fp:
      self.pcls = json.load(fp)

    if self.verbose:
      print("Data structures initialized - VenomSeq is now ready for use!")

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
      self.connectivity = self.connectivity._replace(wcs=np.load(wcs_file))
    if ncs_file is not None:
      self.connectivity = self.connectivity._replace(ncs=np.load(ncs_file))
    if tau_file is not None:
      self.connectivity = self.connectivity._replace(tau=np.load(tau_file))

  def subset_connectivity_data(self, type='tau', cell_line=None, pert_type='trt_cp'):
    """Retrieve a subset of a data matrix matching certain conditions.

    Parameters
    ----------
    type : str
      The connectivity data matrix to use. It can be 'wcs', 'ncs', or 'tau';
      other options will be added in future releases.
    cell_line : str, optional
      Cell line name to filter for. If omitted, all cell lines will be returned.
    pert_type : str, optional
      Perturbagen type to filter for. If omitted, all perturbagen types will be
      returned.

    Returns
    -------
    subset : numpy.ndarray
      Returns a 2-dimensional Numpy array containing the requested data.
    """
    if type == 'wcs':
      subset = self.connectivity.wcs
    elif type == 'ncs':
      subset = self.connectivity.ncs
    elif type == 'tau':
      subset = self.connectivity.tau

    cell_idxs = np.arange(subset.shape[0])
    pert_idxs = np.arange(subset.shape[0])

    if cell_line:
      cell_idxs = self._cell_type_idxs(cell_line)
    if pert_type:
      pert_idxs = self._pert_type_idxs(pert_type)

    filter_idxs = np.intersect1d(cell_idxs, pert_idxs)

    return subset[filter_idxs,:]

  def pcl_signatures_with_annotations(self, type='tau'):
    if type == 'wcs':
      subset = self.connectivity.wcs
    elif type == 'ncs':
      subset = self.connectivity.ncs
    elif type == 'tau':
      subset = self.connectivity.tau



  def _cell_type_idxs(self, cell_type):
    mask = np.array(self.cmap.cols.cell_id == cell_type)
    return np.nonzero(mask)[0]

  def _pert_type_idxs(self, pert_type):
    mask = np.array(self.cmap.cols.pert_type == pert_type)
    return np.nonzero(mask)[0]

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
    data_df, cm, rm = read_gctx(self.gctx_file, ignore_data_df=True)
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