import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.decomposition import PCA
from scipy.cluster import hierarchy

def pca_plot(venomseq):
  pca = PCA(n_components=2)
  X_r = pca.fit(venomseq.connectivity.wcs.T).transform(venomseq.connectivity.wcs.T)
  f, ax = plt.subplots(1, 1)
  ax.scatter(X_r[:,0], X_r[:,1], s=12)
  return ax

def heatmap(matrix, annotations):
  sns.clustermap(data=matrix)

# def heatmap_wrapper(data, vmin=None, vmax=None, cmap=None, center=None, robust=False,
#                     annot=None, fmt=".2g", annot_kws=None,
#                     linewidths=0, linecolor="white",
#                     cbar=True, cbar_kws=None, cbar_ax=None,
#                     square=False, xticklabels="auto", yticklabels="auto",
#                     mask=None, ax=None, **kwargs):

#   # Initialize the plotter object
#   plotter = _HeatMapper(data, vmin, vmax, cmap, center, robust, annot, fmt,
#                         annot_kws, cbar, cbar_kws, xticklabels,
#                         yticklabels, mask)

#   # Add the pcolormesh kwargs here
#   kwargs["linewidths"] = linewidths
#   kwargs["edgecolor"] = linecolor

#   # Draw the plot and return the Axes
#   if ax is None:
#     ax = plt.gca()
#   if square:
#     ax.set_aspect("equal")
#   plotter.plot(ax, cbar_ax, kwargs)
#   return ax

# class _HeatMapper(object):
#   """Draw a heatmap plot of a matrix with nice labels and colormaps."""

#   def __init__(self, data, vmin, vmax, cmap, center, robust, annot, fmt,
#          annot_kws, cbar, cbar_kws,
#          xticklabels=True, yticklabels=True, mask=None):
#     """Initialize the plotting object."""
#     # We always want to have a DataFrame with semantic information
#     # and an ndarray to pass to matplotlib
#     if isinstance(data, pd.DataFrame):
#       plot_data = data.values
#     else:
#       plot_data = np.asarray(data)
#       data = pd.DataFrame(plot_data)

#     # Validate the mask and convet to DataFrame
#     mask = _matrix_mask(data, mask)

#     plot_data = np.ma.masked_where(np.asarray(mask), plot_data)

#     # Get good names for the rows and columns
#     xtickevery = 1
#     if isinstance(xticklabels, int):
#       xtickevery = xticklabels
#       xticklabels = _index_to_ticklabels(data.columns)
#     elif xticklabels is True:
#       xticklabels = _index_to_ticklabels(data.columns)
#     elif xticklabels is False:
#       xticklabels = []

#     ytickevery = 1
#     if isinstance(yticklabels, int):
#       ytickevery = yticklabels
#       yticklabels = _index_to_ticklabels(data.index)
#     elif yticklabels is True:
#       yticklabels = _index_to_ticklabels(data.index)
#     elif yticklabels is False:
#       yticklabels = []

#     # Get the positions and used label for the ticks
#     nx, ny = data.T.shape

#     if not len(xticklabels):
#       self.xticks = []
#       self.xticklabels = []
#     elif isinstance(xticklabels, string_types) and xticklabels == "auto":
#       self.xticks = "auto"
#       #self.xticklabels = _index_to_ticklabels(data.columns)
#       #self.xticklabels = np.array(data.columns) + 1
#       reordered_species_names = []
#       for x in np.array(data.columns):
#         reordered_species_names.append(species_names[x])
#       self.xticklabels = np.array(reordered_species_names)
#     else:
#       self.xticks, self.xticklabels = self._skip_ticks(xticklabels,
#                                xtickevery)

#     if not len(yticklabels):
#       self.yticks = []
#       self.yticklabels = []
#     elif isinstance(yticklabels, string_types) and yticklabels == "auto":
#       self.yticks = "auto"
#       self.yticklabels = _index_to_ticklabels(data.index)
#     else:
#       self.yticks, self.yticklabels = self._skip_ticks(yticklabels,
#                                ytickevery)

#     # Get good names for the axis labels
#     xlabel = _index_to_label(data.columns)
#     ylabel = _index_to_label(data.index)
#     self.xlabel = xlabel if xlabel is not None else ""
#     self.ylabel = ylabel if ylabel is not None else ""

#     # Determine good default values for the colormapping
#     self._determine_cmap_params(plot_data, vmin, vmax,
#                   cmap, center, robust)

#     # Sort out the annotations
#     if annot is None:
#       annot = False
#       annot_data = None
#     elif isinstance(annot, bool):
#       if annot:
#         annot_data = plot_data
#       else:
#         annot_data = None
#     else:
#       try:
#         annot_data = annot.values
#       except AttributeError:
#         annot_data = annot
#       if annot.shape != plot_data.shape:
#         raise ValueError('Data supplied to "annot" must be the same '
#                  'shape as the data to plot.')
#       annot = True

#     # Save other attributes to the object
#     self.data = data
#     self.plot_data = plot_data

#     self.annot = annot
#     self.annot_data = annot_data

#     self.fmt = fmt
#     self.annot_kws = {} if annot_kws is None else annot_kws
#     self.cbar = cbar
#     self.cbar_kws = {} if cbar_kws is None else cbar_kws
#     self.cbar_kws.setdefault('ticks', mpl.ticker.MaxNLocator(6))

#   def _determine_cmap_params(self, plot_data, vmin, vmax,
#                  cmap, center, robust):
#     """Use some heuristics to set good defaults for colorbar and range."""
#     calc_data = plot_data.data[~np.isnan(plot_data.data)]
#     if vmin is None:
#       vmin = np.percentile(calc_data, 2) if robust else calc_data.min()
#     if vmax is None:
#       vmax = np.percentile(calc_data, 98) if robust else calc_data.max()
#     self.vmin, self.vmax = vmin, vmax

#     # Choose default colormaps if not provided
#     if cmap is None:
#       #if center is None:
#       #    self.cmap = cm.inferno
#       #else:
#       #    self.cmap = cm.icefire
#       self.cmap = cm.coolwarm
#     elif isinstance(cmap, string_types):
#       self.cmap = mpl.cm.get_cmap(cmap)
#     elif isinstance(cmap, list):
#       self.cmap = mpl.colors.ListedColormap(cmap)
#     else:
#       self.cmap = cmap

#     # Recenter a divergent colormap
#     if center is not None:
#       vrange = max(vmax - center, center - vmin)
#       normlize = mpl.colors.Normalize(center - vrange, center + vrange)
#       cmin, cmax = normlize([vmin, vmax])
#       cc = np.linspace(cmin, cmax, 256)
#       self.cmap = mpl.colors.ListedColormap(self.cmap(cc))

#   def _annotate_heatmap(self, ax, mesh):
#     """Add textual labels with the value in each cell."""
#     mesh.update_scalarmappable()
#     height, width = self.annot_data.shape
#     xpos, ypos = np.meshgrid(np.arange(width) + .5, np.arange(height) + .5)
#     for x, y, m, color, val in zip(xpos.flat, ypos.flat,
#                      mesh.get_array(), mesh.get_facecolors(),
#                      self.annot_data.flat):
#       if m is not np.ma.masked:
#         lum = relative_luminance(color)
#         text_color = ".15" if lum > .408 else "w"
#         annotation = ("{:" + self.fmt + "}").format(val)
#         text_kwargs = dict(color=text_color, ha="center", va="center")
#         text_kwargs.update(self.annot_kws)
#         ax.text(x, y, annotation, **text_kwargs)

#   def _skip_ticks(self, labels, tickevery):
#     """Return ticks and labels at evenly spaced intervals."""
#     n = len(labels)
#     if tickevery == 0:
#       ticks, labels = [], []
#     elif tickevery == 1:
#       ticks, labels = np.arange(n) + .5, labels
#     else:
#       start, end, step = 0, n, tickevery
#       ticks = np.arange(start, end, step) + .5
#       labels = labels[start:end:step]
#     return ticks, labels

#   def _auto_ticks(self, ax, labels, axis):
#     """Determine ticks and ticklabels that minimize overlap."""
#     transform = ax.figure.dpi_scale_trans.inverted()
#     bbox = ax.get_window_extent().transformed(transform)
#     size = [bbox.width, bbox.height][axis]
#     axis = [ax.xaxis, ax.yaxis][axis]
#     tick, = axis.set_ticks([0])
#     fontsize = tick.label.get_size()
#     max_ticks = int(size // (fontsize / 72))
#     if max_ticks < 1:
#       return [], []
#     tick_every = len(labels) // max_ticks + 1
#     tick_every = 1 if tick_every == 0 else tick_every
#     ticks, labels = self._skip_ticks(labels, tick_every)
#     return ticks, labels

#   def plot(self, ax, cax, kws):
#     """Draw the heatmap on the provided Axes."""
#     # Remove all the Axes spines
#     despine(ax=ax, left=True, bottom=True)

#     # Draw the heatmap
#     mesh = ax.pcolormesh(self.plot_data, vmin=self.vmin, vmax=self.vmax,
#                cmap=self.cmap, **kws)

#     # Set the axis limits
#     ax.set(xlim=(0, self.data.shape[1]), ylim=(0, self.data.shape[0]))

#     # Invert the y axis to show the plot in matrix form
#     ax.invert_yaxis()

#     # Possibly add a colorbar
#     if self.cbar:
#       cb = ax.figure.colorbar(mesh, cax, ax, **self.cbar_kws)
#       cb.outline.set_linewidth(0)
#       # If rasterized is passed to pcolormesh, also rasterize the
#       # colorbar to avoid white lines on the PDF rendering
#       if kws.get('rasterized', False):
#         cb.solids.set_rasterized(True)

#     # Add row and column labels
#     if isinstance(self.xticks, string_types) and self.xticks == "auto":
#       xticks, xticklabels = self._auto_ticks(ax, self.xticklabels, 0)
#     else:
#       xticks, xticklabels = self.xticks, self.xticklabels

#     if isinstance(self.yticks, string_types) and self.yticks == "auto":
#       yticks, yticklabels = self._auto_ticks(ax, self.yticklabels, 1)
#     else:
#       yticks, yticklabels = self.yticks, self.yticklabels

#     ax.set(xticks=xticks, yticks=yticks)
#     xtl = ax.set_xticklabels(xticklabels)
#     ytl = ax.set_yticklabels(yticklabels, rotation="vertical")

#     # Possibly rotate them if they overlap
#     if hasattr(ax.figure.canvas, "get_renderer"):
#       ax.figure.draw(ax.figure.canvas.get_renderer())
#     if axis_ticklabels_overlap(xtl):
#       plt.setp(xtl, rotation="vertical")
#     if axis_ticklabels_overlap(ytl):
#       plt.setp(ytl, rotation="horizontal")

#     # Add the axis labels
#     ax.set(xlabel=self.xlabel, ylabel=self.ylabel)

#     # Annotate the cells with the formatted values
#     if self.annot:
#       self._annotate_heatmap(ax, mesh)



# def _matrix_mask(data, mask):
#   if mask is None:
#     mask = np.zeros(data.shape, np.bool)
#   if isinstance(mask, np.ndarray):
#     if mask.shape != data.shape:
#       raise ValueError("Mask must have the same shape as data.")
#     mask = pd.DataFrame(mask,
#               index=data.index,
#               columns=data.columns,
#               dtype=np.bool)
#   elif isinstance(mask, pd.DataFrame):
#     if not mask.index.equals(data.index) \
#        and mask.columns.equals(data.columns):
#       err = "Mask must have the same index and columns as data."
#       raise ValueError(err)
#   mask = mask | pd.isnull(data)
#   return mask

# def _index_to_label(index):
#   if isinstance(index, pd.MultiIndex):
#     return "-".join(map(to_utf8, index.names))
#   else:
#     return index.name
# def _index_to_ticklabels(index):
#   if isinstance(index, pd.MultiIndex):
#     return ["-".join(map(to_utf8, i)) for i in index.values]
#   else:
#     return index.values
# string_types = str
# def despine(fig=None, ax=None, top=True, right=True, left=False,
#       bottom=False, offset=None, trim=False):
#   if fig is None and ax is None:
#     axes = plt.gcf().axes
#   elif fig is not None:
#     axes = fig.axes
#   elif ax is not None:
#     axes = [ax]
#   for ax_i in axes:
#     for side in ["top", "right", "left", "bottom"]:
#       is_visible = not locals()[side]
#       ax_i.spines[side].set_visible(is_visible)
#       if offset is not None and is_visible:
#         try:
#           val = offset.get(side, 0)
#         except AttributeError:
#           val = offset
#         _set_spine_position(ax_i.spines[side], ('outward', val))
#     if left and not right:
#       maj_on = any(t.tick1On for t in ax_i.yaxis.majorTicks)
#       min_on = any(t.tick1On for t in ax_i.yaxis.minorTicks)
#       ax_i.yaxis.set_ticks_position("right")
#       for t in ax_i.yaxis.majorTicks:
#         t.tick2On = maj_on
#       for t in ax_i.yaxis.minorTicks:
#         t.tick2On = min_on
#     if bottom and not top:
#       maj_on = any(t.tick1On for t in ax_i.xaxis.majorTicks)
#       min_on = any(t.tick1On for t in ax_i.xaxis.minorTicks)
#       ax_i.xaxis.set_ticks_position("top")
#       for t in ax_i.xaxis.majorTicks:
#         t.tick2On = maj_on
#       for t in ax_i.xaxis.minorTicks:
#         t.tick2On = min_on
#     if trim:
#       xticks = ax_i.get_xticks()
#       if xticks.size:
#         firsttick = np.compress(xticks >= min(ax_i.get_xlim()),
#                     xticks)[0]
#         lasttick = np.compress(xticks <= max(ax_i.get_xlim()),
#                      xticks)[-1]
#         ax_i.spines['bottom'].set_bounds(firsttick, lasttick)
#         ax_i.spines['top'].set_bounds(firsttick, lasttick)
#         newticks = xticks.compress(xticks <= lasttick)
#         newticks = newticks.compress(newticks >= firsttick)
#         ax_i.set_xticks(newticks)
#       yticks = ax_i.get_yticks()
#       if yticks.size:
#         firsttick = np.compress(yticks >= min(ax_i.get_ylim()),
#                     yticks)[0]
#         lasttick = np.compress(yticks <= max(ax_i.get_ylim()),
#                      yticks)[-1]
#         ax_i.spines['left'].set_bounds(firsttick, lasttick)
#         ax_i.spines['right'].set_bounds(firsttick, lasttick)
#         newticks = yticks.compress(yticks <= lasttick)
#         newticks = newticks.compress(newticks >= firsttick)
#         ax_i.set_yticks(newticks)
# def axis_ticklabels_overlap(labels):
#   if not labels:
#     return False
#   try:
#     bboxes = [l.get_window_extent() for l in labels]
#     overlaps = [b.count_overlaps(bboxes) for b in bboxes]
#     return max(overlaps) > 1
#   except RuntimeError:
#     return False