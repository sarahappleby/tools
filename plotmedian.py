
import pylab as plt
import numpy as np
from scipy import stats

def histedges_equalN(x, nbin):
	npt = len(x)
	return np.interp(np.linspace(0, npt, nbin + 1),
					 np.arange(npt),
					 np.sort(x))

def plotmedian(x,y,yflag=[],c='k',ltype='--',lw=3,stat='median',ax='plt',bins=8,label=None):
	if len(yflag) != len(x):
		#print 'Plotmedian: No flag provided, using all values'
		xp = x
		yp = y
	else:
		xp = x[yflag]
		yp = y[yflag]
	if bins < 0:	# bins<0 sets bins such that there are equal numbers per bin
		bin_edges = histedges_equalN(xp,-bins)
		bin_means, bin_edges, binnumber = stats.binned_statistic(xp,yp,bins=bin_edges,statistic=stat)
	else:
		bin_means, bin_edges, binnumber = stats.binned_statistic(xp,yp,bins=bins,statistic=stat)
		bin_cent = 0.5*(bin_edges[1:]+bin_edges[:-1])
		#print bin_cent,bin_means,binnumber
		ax.plot(bin_cent, bin_means, ltype, lw=lw, color=c, label=label)

def runningmedian(x,y,xlolim=-1.e20,ylolim=-1.e20,bins=10,stat='median'):
		xp = x[(x>xlolim)&(y>ylolim)]
		yp = y[(x>xlolim)&(y>ylolim)]
		hist,bin_edges=np.histogram(xp,bins)
		ymed = []
		ymean = []
		ysigma = []
		ndata = []
		for i in range(0,len(bin_edges[:-1])):
				xsub = xp[xp>bin_edges[i]]
				ysub = yp[xp>bin_edges[i]]
				ysub = ysub[xsub<bin_edges[i+1]]
				ymed.append(np.median(10**ysub))
				ymean.append(np.mean(10**ysub))
				ysigma.append(np.std(10**ysub))
				ndata.append(len(ysub))
		bin_cent = 0.5*(bin_edges[1:]+bin_edges[:-1])
		if stat=='median': ymean = np.asarray(ymed)
		else: ymean = np.asarray(ymean)
		ysiglo = np.maximum(ymean-ysigma,ymean*0.1)
		ysiglo = np.log10(ymean)-np.log10(ysiglo)
		ysighi = np.log10(ymean+ysigma)-np.log10(ymean)
		ymean = np.log10(ymean)
		ndata = np.array(ndata)
		#print bin_cent,ymean,ysiglo,ysighi
		#plt.plot(bin_cent,ymed,'ro',ms=12,color='c')
		#plt.plot(bin_cent,ymean,'--',lw=3,color='m')
		#plt.errorbar(bin_cent,ymean,yerr=[ysiglo,ysighi],fmt='ro')
		return bin_cent,ymean,ysiglo,ysighi,ndata

