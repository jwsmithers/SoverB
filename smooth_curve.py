from root_numpy import hist2array
import numpy as np
import math
import matplotlib.pyplot as plt
import ROOT
from rootpy.plotting.style import set_style
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
set_style('ATLAS', mpl=True)


total_error_with_ppt=[61.851959,
73.557281,
77.241753,
73.537308,
52.451118,
77.259621,
62.263344,
66.908913,
66.775131,
69.740173,
49.274830,
54.018188,
77.873222,
92.991486,
165.950577]

total_error_without_ppt=[38.422432,
47.862087,
43.504967,
56.230820,
79.577484,
43.515686,
59.012699,
77.111404,
62.119514,
60.963024,
76.491035,
146.361496,
118.906387,
60.736725,
60.924484]


def return_errors(hist):
  error = []
  for i in range(1,hist.GetNbinsX()+1):
    error.append(hist.GetBinError(i))
  return error

def return_errors_graph(hist):
  error = []
  for i in range(0,15):
    error.append(hist.GetErrorY(i))
  return error

def square(L):
    return np.asarray([i ** 2 for i in L])

def square_root(L):
    return np.asarray([math.sqrt(i) for i in L])


def retreive_events(path,File):

  filename = path+File

#  f_postfit = ROOT.TFile.Open(path+post_fit_filename)
#  ttphoton_hist = f.Get("h_ttphoton_postFit")
#  ttphoton_hist_errors = return_errors(ttphoton_hist)
#  hfake_hist = f.Get("h_hadronfakes_postFit")
#  hfake_hist_errors = return_errors(hfake_hist)
#  efake_hist = f.Get("h_electronfakes_postFit")
#  efake_hist_errors = return_errors(efake_hist)
#  qcd_hist = f.Get("h_QCD_postFit")
#  qcd_hist_errors = return_errors(qcd_hist)
#  wphoton_hist = f.Get("h_Wphoton_postFit")
#  wphoton_hist_errors = return_errors(wphoton_hist)
#  other_hist = f.Get("h_Other_postFit")
#  other_hist_errors=return_errors(other_hist)

#  _total_error = f_postfit.Get("g_totErr_postFit")
#  total_errors = return_errors_graph(_total_error)

  #prefit
  f = ROOT.TFile.Open(filename)
  ttphoton_hist = f.Get("event_ELD_MVA_ejets_ttphoton")
  ttphoton_hist_errors = return_errors(ttphoton_hist)
  hfake_hist = f.Get("event_ELD_MVA_ejets_hadronfakes")
  hfake_hist_errors = return_errors(hfake_hist)
  efake_hist = f.Get("event_ELD_MVA_ejets_electronfakes")
  efake_hist_errors = return_errors(efake_hist)
  qcd_hist = f.Get("event_ELD_MVA_ejets_QCD")
  qcd_hist_errors = return_errors(qcd_hist)
  wphoton_hist = f.Get("event_ELD_MVA_ejets_Wphoton")
  wphoton_hist_errors = return_errors(wphoton_hist)
  other_hist = f.Get("event_ELD_MVA_ejets_Other")
  other_hist_errors=return_errors(other_hist)

  signal_hist = hist2array(ttphoton_hist, include_overflow=False, copy=True, return_edges=False)

  _hfake_hist = hist2array(hfake_hist, include_overflow=False, copy=True, return_edges=False)
  _efake_hist = hist2array(efake_hist, include_overflow=False, copy=True, return_edges=False)
  _qcd_hist = hist2array(qcd_hist, include_overflow=False, copy=True, return_edges=False)
  _wphoton_hist = hist2array(wphoton_hist, include_overflow=False, copy=True, return_edges=False)
  _other_hist = hist2array(other_hist, include_overflow=False, copy=True, return_edges=False)

  bkg_hist = _hfake_hist+_efake_hist+_qcd_hist+_wphoton_hist+_other_hist

  s_over_b = []
  s_over_b_error=[]
  significance = []
  significance_errors = []


  #add_bkg_errors = square(hfake_hist_errors)+square(efake_hist_errors)+square(qcd_hist_errors)+square(wphoton_hist_errors)+square(other_hist_errors)
  #total_bkg_error = square_root(add_bkg_errors)


  #Now we cut at each bin and calculate the total s/b
  for i in range(0,len(signal_hist)):
    s = sum(signal_hist[i:])
    b = sum(bkg_hist[i:])
    s_over_b.append(s/b)
    significance.append(s/math.sqrt(b))

#    #calculate the error:
#    ds = ttphoton_hist_errors[i]
#    db = total_bkg_error[i]
#    s_over_b_error.append(float(math.sqrt( ((b**2*ds**2)+(db**2*s**2))/b**4 )))
#    significance_errors.append((1/2.)*math.sqrt((4*(b**2)*(ds**2) + (db**2)*(s**2))/b**3))

    if "NO_PPT" in path:
      total_error_list = total_error_without_ppt[i]
    else:
      total_error_list = total_error_with_ppt[i]

    # Scale the total error respectively
    s_over_b_error.append((total_error_list*(s/b))/(s+b))
    significance_errors.append((total_error_list*(s/math.sqrt(b)))/(s+b))

  return s_over_b, significance, np.asarray(s_over_b_error), np.asarray(significance_errors)

withppt_path = "/afs/desy.de/user/j/jwsmith/01_07_2018/singlelepton_fullFit_merged_C_On_auto/build/SR1_ejets_mujets_merged/ejets_mujets_merged/Histograms/"
withoutppt_path = "/afs/desy.de/user/j/jwsmith/ttgammaPlottingPipeline/batch_submit/singlelepton_fullFit_merged_C_On_auto_NO_PPT/build/SR1_ejets_mujets_merged/ejets_mujets_merged/Histograms/"
filename = "ejets_mujets_merged_event_ELD_MVA_ejets_histos.root"
post_fit_filename="event_ELD_MVA_ejets_postFit.root"

no_ppt=retreive_events(withoutppt_path,filename)
s_over_b_without_ppt = no_ppt[0]
significance_withoutppt = no_ppt[1]
s_over_b_without_ppt_errors = no_ppt[2]
significance_withoutppt_errors = no_ppt[3]

with_ppt=retreive_events(withppt_path,filename)
s_over_b_with_ppt = with_ppt[0]
significance_with_ppt = with_ppt[1]
s_over_b_with_ppt_errors = with_ppt[2]
significance_with_ppt_errors = with_ppt[3]


my_xticks = map(lambda x: x*0.07, range(0, 15, 1))
error = np.random.normal(0.1, 0.02, size=(1,)) +.1

fig, ax1 = plt.subplots()
ax1.xaxis.set_ticks_position("both")
ax1.minorticks_on()
ax1.plot(my_xticks,s_over_b_with_ppt,"b-",label="with PPT",linewidth=2)
ax1.fill_between(my_xticks, s_over_b_with_ppt-s_over_b_with_ppt_errors, s_over_b_with_ppt+s_over_b_with_ppt_errors,
    alpha=1, edgecolor='#089FFF', facecolor='#089FFF',linewidth=0)

ax1.set_xlabel('Event level descriminator',horizontalalignment='right',x=1.0)
ax1.set_ylabel(r'$s/b$',color="b",horizontalalignment='right',y=1.0)
ax1.tick_params(axis="y",colors="b",direction='in', which="both")
ax1.tick_params(axis="x",direction='in', which="both")
ax1.plot(my_xticks,s_over_b_without_ppt,"b--",label="without PPT",linewidth=2)
ax1.fill_between(my_xticks, s_over_b_without_ppt-s_over_b_without_ppt_errors, s_over_b_without_ppt+s_over_b_without_ppt_errors,
    alpha=1, edgecolor='#08ecff', facecolor='#08ecff',linewidth=0)

ax2 = ax1.twinx()
ax2.xaxis.set_ticks_position("both")
ax2.minorticks_on()
ax2.plot(my_xticks,significance_with_ppt,"r-",label="with PPT",linewidth=2)
ax2.fill_between(my_xticks, significance_with_ppt-significance_with_ppt_errors, significance_with_ppt+significance_with_ppt_errors,
    alpha=1, edgecolor='#FF7272', facecolor='#FF7272',linewidth=0)

ax2.set_ylabel(r"$s/\sqrt{b}$",color="r",horizontalalignment='right',y=1.0)
ax2.tick_params(axis="y",colors="r",direction='in', which="both")
ax2.tick_params(axis="x",direction='in', which="both")
ax2.plot(my_xticks,significance_withoutppt,"r--",label="without PPT",linewidth=2)
ax2.fill_between(my_xticks, significance_withoutppt-significance_withoutppt_errors, significance_withoutppt+significance_withoutppt_errors,
    alpha=1, edgecolor='#FFB3A0', facecolor='#FFB3A0',linewidth=0)


withppt = mlines.Line2D([], [], color='black',linewidth=2, label=r'with PPT')
withoutppt = mlines.Line2D([], [], color='black',linewidth=2, label=r'without PPT', linestyle="--")
uncert = mpatches.Patch(color='grey', label='Systematic uncertainty')



ax1.text(0.18,3.7,r"$\sqrt{s}=$13 TeV, 36.1 fb$^{-1}$",
          fontsize=14, color='black')
plt.legend(handles=[withppt,withoutppt,uncert],loc=(0.2,0.45),frameon=False,fontsize =13)

plt.tight_layout()
plt.gcf().subplots_adjust(left=0.11)
plt.savefig("soverb_smooth_curve.eps",format="eps")
