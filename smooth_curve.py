from root_numpy import hist2array
import numpy as np
import math
import matplotlib.pyplot as plt
import ROOT
from rootpy.plotting.style import set_style
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
set_style('ATLAS', mpl=True)

#from matplotlib import rc
#rc('text', usetex=True)
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

signal_error_with_ppt = [27.190201, 
31.898310,
52.579323,
36.546188,
32.053516,
43.168060,
47.035297,
54.571823,
55.644463,
50.347736,
33.956764,
43.365265,
57.821518,
77.889450,
156.318161]

background_error_with_ppt = [59.428699, 
68.674637,
74.488487,
65.303169,
46.686226,
66.499092,
49.610222,
40.999603,
42.809963,
51.230968,
39.774769,
37.171600,
50.436943,
43.418961,
46.070732]


signal_error_without_ppt=[19.091253, 
26.131187,
21.160421,
24.735683,
48.555183,
31.894642,
35.454357,
58.091515,
45.814583,
52.198219,
51.320858,
96.067398,
69.173141,
51.244789,
59.280148]


background_error_without_ppt=[37.967445, 
45.762615,
41.780563,
54.296570,
77.235046,
35.616005,
52.660904,
58.515697,
45.664909,
37.177460,
60.152164,
111.847214,
97.058266,
28.016979,
14.711366]

def return_errors(hist):
  error = []
  for i in range(1,hist.GetNbinsX()+1):
    error.append(hist.GetBinError(i))
  return error

def square(L):
    #return np.asarray([i ** 2 for i in L])
    return [i ** 2 for i in L]

def square_root(L):
    return np.asarray([math.sqrt(i) for i in L])


def retreive_events(path,File):

  filename = path+File

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


  #Now we cut at each bin and calculate the total s/b
  for i in range(0,len(signal_hist)):
    s = sum(signal_hist[i:])
    b = sum(bkg_hist[i:])
    s_over_b.append(s/b)
    significance.append(s/math.sqrt(b))

    #if "NO_PPT" in path:
    #  s_err = signal_error_without_ppt[i]
    #  b_err = background_error_without_ppt[i]
    #else:
    #  s_err = signal_error_with_ppt[i]
    #  b_err = background_error_with_ppt[i]

    if "NO_PPT" in path:
      s_err = math.sqrt(sum(square(signal_error_without_ppt[i:])))
      b_err = math.sqrt(sum(square(background_error_without_ppt[i:])))
    else:
      s_err = math.sqrt(sum(square(signal_error_with_ppt[i:])))
      b_err = math.sqrt(sum(square(background_error_with_ppt[i:])))

    s_over_b_error.append(math.sqrt(((s**2*b_err**2)+(s_err**2*b**2))/b**4))
    num = s**2*b_err**2+4*s_err**2*b**2
    denom = b**3
    significance_errors.append(0.5*math.sqrt(num/denom))

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
uncert = mpatches.Patch(color='grey', label=r'Stat. $\oplus$ Syst.')


ax1.text(0.18,3.8,r"ATLAS",style='italic',weight='bold',
          fontsize=18, color='black')
ax1.text(0.38,3.8,r"Internal",
          fontsize=18, color='black')
ax1.text(0.18,3.4,r"$\sqrt{s}=$13 TeV, 36.1 fb$^{-1}$",
          fontsize=14, color='black')
plt.legend(handles=[withppt,withoutppt,uncert],loc=(0.2,0.45),frameon=False,fontsize =13)

plt.tight_layout()
plt.gcf().subplots_adjust(left=0.11)
plt.savefig("soverb_smooth_curve.eps",format="eps")
