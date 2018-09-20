from root_numpy import hist2array
from root_numpy import testdata
import math
import matplotlib.pyplot as plt
import ROOT
from rootpy.plotting.style import set_style
import matplotlib.lines as mlines
set_style('ATLAS', mpl=True)

def retreive_events(filename):

  f = ROOT.TFile.Open(filename)
  ttphoton_hist = f.Get("event_ELD_MVA_ejets_ttphoton")
  hfake_hist = f.Get("event_ELD_MVA_ejets_hadronfakes")
  efake_hist = f.Get("event_ELD_MVA_ejets_electronfakes")
  qcd_hist = f.Get("event_ELD_MVA_ejets_QCD")
  wphoton_hist = f.Get("event_ELD_MVA_ejets_Wphoton")
  other_hist = f.Get("event_ELD_MVA_ejets_Other")
  
  signal_hist = hist2array(ttphoton_hist, include_overflow=False, copy=True, return_edges=False)

  _hfake_hist = hist2array(hfake_hist, include_overflow=False, copy=True, return_edges=False)
  _efake_hist = hist2array(efake_hist, include_overflow=False, copy=True, return_edges=False)
  _qcd_hist = hist2array(qcd_hist, include_overflow=False, copy=True, return_edges=False)
  _wphoton_hist = hist2array(wphoton_hist, include_overflow=False, copy=True, return_edges=False)
  _other_hist = hist2array(other_hist, include_overflow=False, copy=True, return_edges=False)

  bkg_hist = _hfake_hist+_efake_hist+_qcd_hist+_wphoton_hist+_other_hist

  #bkg_hist = hist2array(background, include_overflow=False, copy=True, return_edges=False)

  s_over_b = []
  significance = []

  for i in range(0,len(signal_hist)):
    s = signal_hist[i]
    b = bkg_hist[i]
    s_over_b.append(s/b)
    significance.append(s/math.sqrt(b))

  return s_over_b, significance

withppt_path = "/afs/desy.de/user/j/jwsmith/01_07_2018/singlelepton_fullFit_merged_C_On_auto/build/SR1_ejets_mujets_merged/ejets_mujets_merged/Histograms/"
withoutppt_path = "/afs/desy.de/user/j/jwsmith/ttgammaPlottingPipeline/batch_submit/singlelepton_fullFit_merged_C_On_auto_NO_PPT/build/SR1_ejets_mujets_merged/ejets_mujets_merged/Histograms/"
filename = "ejets_mujets_merged_event_ELD_MVA_ejets_histos.root"

no_ppt_file=withoutppt_path+filename
with_ppt_file=withppt_path+filename

no_ppt=retreive_events(no_ppt_file)
s_over_b_without_ppt = no_ppt[0]
significance_withoutppt = no_ppt[1]

with_ppt=retreive_events(with_ppt_file)
s_over_b_with_ppt = with_ppt[0]
significance_with_ppt = with_ppt[1]


fig, ax1 = plt.subplots()
ax1.xaxis.set_ticks_position("both")
ax1.minorticks_on()
ax1.plot(s_over_b_with_ppt,"b-",label="with PPT",linewidth=2)
ax1.set_xlabel('ELD bin number',horizontalalignment='right',x=1.0)
ax1.set_ylabel(r'$s/b$',color="b",horizontalalignment='right',y=1.0)
ax1.tick_params(axis="y",colors="b",direction='in', which="both")
ax1.tick_params(axis="x",direction='in', which="both")
ax1.plot(s_over_b_without_ppt,"b--",label="without PPT",linewidth=2)


ax2 = ax1.twinx()
ax2.xaxis.set_ticks_position("both")
ax2.minorticks_on()
ax2.plot(significance_with_ppt,"r-",label="with PPT",linewidth=2)
ax2.set_ylabel(r"$s/\sqrt{b}$",color="r",horizontalalignment='right',y=1.0)
ax2.tick_params(axis="y",colors="r",direction='in', which="both")
ax2.tick_params(axis="x",direction='in', which="both")
ax2.plot(significance_withoutppt,"r--",label="without PPT",linewidth=2)


withppt = mlines.Line2D([], [], color='black',linewidth=2, label=r'with PPT')
withoutppt = mlines.Line2D([], [], color='black',linewidth=2, label=r'without PPT', linestyle="--")

plt.legend(handles=[withppt,withoutppt],loc="upper left",frameon=False,fontsize =13)

plt.tight_layout()
plt.savefig("soverb.eps",format="eps")
