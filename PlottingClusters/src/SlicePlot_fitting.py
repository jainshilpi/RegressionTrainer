import os
import pickle
from math import sqrt, exp,log
from array import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro( os.path.abspath('src/effSigma.C') )

# Returns a unique histogram name (useful if object is not accessed by name anyway)
ROOTCNT = 0
def RootName():
    global ROOTCNT
    ret = 'Object' + str(ROOTCNT)
    ROOTCNT += 1
    return ret


def FitSlices( self ):

    ########################################
    # Fill the Fit dict
    ########################################

    self.p( 'SlicePlot for {0} (bins from {1} to {2})'.format(
            self.slicevarname, self.bounds[0], self.bounds[-1] ), 1 )

    self.Fit = {}
    for histvar in self.histvars:
        self.Fit[histvar.GetName()] = {
            'CBvals'     : [],
            'CBerrs'     : [],
            'effsigma'   : [],
            'fitdata'    : [],
            'CBhist'     : [],
            }


    for i in xrange( self.n_bins ):

        x_min = self.bounds[i]
        x_max = self.bounds[i+1]

        #sel_str = '{0}>{1}&&{0}<{2}'.format( self.slicevarname, x_min, x_max )
        sel_str = '{0}>={1}&&{0}<{2}'.format( self.slicevarname, x_min, x_max ) ###SJ
        self.p( 'Creating reduced dataset; sel_str = ' + sel_str )
        hdata_reduced = self.hdata.reduce(sel_str)
        print "entries in this data set is ",hdata_reduced.numEntries()
        for histvar in self.histvars:
            self.FitOneSlice( hdata_reduced, histvar )
            #self.FitOneSliceGaus( hdata_reduced, histvar )


    # Delete the big data set
    del self.hdata

    self.p( 'Dumping instance to {0}.pickle'.format(self.longname), 1 )
    if not os.path.isdir( self.pickledir ): os.makedirs( self.pickledir )
    with open( os.path.join( self.pickledir, self.longname + '.pickle' ), 'wb' ) as pickle_fp:
        pickle.dump( self, pickle_fp )



def FitOneSlice( self, hdata_reduced, histvar, unbinnedFit=False ):

    # Reduce dataset to one column, only for fitting
    hdata_fit = hdata_reduced.reduce( ROOT.RooArgSet(histvar) )

    # Fit parameters
    #mean = ROOT.RooRealVar( RootName(), RootName(), 1.,   0.9,    1.1 );
    #mean = ROOT.RooRealVar( RootName(), RootName(), 1.,   0.8,    1.1 ); ###SJ
    #mean = ROOT.RooRealVar( RootName(), RootName(), 1.,   0.5,    1.5 ); ###SJ
    mean = ROOT.RooRealVar( RootName(), RootName(), 1.,   0.7,    1.5 ); ###SJ
    #sig  = ROOT.RooRealVar( RootName(), RootName(), 0.01, 0.0002, 0.8 );
    #sig  = ROOT.RooRealVar( RootName(), RootName(), 0.01, 0.0002, 1.4);

#    sig  = ROOT.RooRealVar( RootName(), RootName(), 0.1, 0.0002, 1.4);
    sig  = ROOT.RooRealVar( RootName(), RootName(), 0.1, 0.0002, 4);

    #a1   = ROOT.RooRealVar( RootName(), RootName(), 3,    0.05,   10 );
    #a2   = ROOT.RooRealVar( RootName(), RootName(), 3,    0.05,   10 );

    
    #a1   = ROOT.RooRealVar( RootName(), RootName(), 3,    0.05,   150 );
    #a2   = ROOT.RooRealVar( RootName(), RootName(), 3,    0.05,   150 );


    a1   = ROOT.RooRealVar( RootName(), RootName(), 2,    0.05,   150 );
    a2   = ROOT.RooRealVar( RootName(), RootName(), 1,    0.05,   150 );

    #a1   = ROOT.RooRealVar( RootName(), RootName(), 2 );
    #a1.setConstant(True)
    #a2   = ROOT.RooRealVar( RootName(), RootName(), 1 );
    #a2.setConstant(True)

    n1   = ROOT.RooRealVar( RootName(), RootName(), 3,    1.01,   500 );
    n2   = ROOT.RooRealVar( RootName(), RootName(), 3,    1.01,   500 );

    # Fit function
    pdfCB = ROOT.RooDoubleCBFast(
        RootName(), RootName(),
        histvar,
        mean, sig, a1, n1, a2, n2
        )

    self.p( 'Fitting crystal ball to dataset (histvar: {0}, fitrange: {1} to {2})'.format(
            histvar.GetName(), self.fit_x_min, self.fit_x_max ), 3 )

    self.p( 'Number of entries in fit dataset: ' + str(hdata_fit.numEntries()), 4 )


    

    if unbinnedFit:
        pdfCB.fitTo(
            hdata_fit,
            ROOT.RooFit.Range(self.fit_x_min, self.fit_x_max),
            ROOT.RooFit.PrintEvalErrors(-1), ROOT.RooFit.PrintLevel(-1)
            )
    else:
        #nBinning = 1000
        #nBinning = 500
        #nBinning = 50
        #nBinning = 60
        nBinning = 50

        hdatahist_fit = ROOT.RooDataHist(
            RootName(), RootName(),
            ROOT.RooArgSet( histvar ),
            hdata_fit
            )


        ####23rd May, 2019
        #hdatahist_hist_fit = hdatahist_fit.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(nBinning) )

        #peak = hdatahist_hist_fit.GetXaxis().GetBinCenter(hdatahist_hist_fit.GetMaximumBin())
        #histrms  = hdatahist_hist_fit.GetRMS()


        #self.fit_x_min = peak - 0.1*histrms
        #self.fit_x_max = peak + 0.1*histrms

        #self.fit_x_min = 0.9
        #self.fit_x_max = 1.1


        print "This is binned fit!!!"
        pdfCB.fitTo(hdatahist_fit,
                    ROOT.RooFit.Range(self.fit_x_min, self.fit_x_max),
                    #ROOT.RooFit.Range(0.9,1.1),
                    ROOT.RooFit.PrintEvalErrors(-1), ROOT.RooFit.PrintLevel(-1)
                    #ROOT.RooFit.PrintEvalErrors(-1), ROOT.RooFit.PrintLevel(2)
                    )
        mean.setVal(1.0)
        #sig.setVal(0.2*sig.getVal())
        pdfCB.fitTo(hdatahist_fit,
                    ROOT.RooFit.Range(self.fit_x_min, self.fit_x_max),
                    #ROOT.RooFit.Range(0.9,1.1),
                    ROOT.RooFit.PrintEvalErrors(-1), ROOT.RooFit.PrintLevel(-1)
                    )
            

    # Make a histogram out of the CB function so that effSigma can be calculated
    histCB = pdfCB.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(2000) )
    #effsigma = ROOT.effSigma( histCB )
    hdatahist_hist_fit = hdatahist_fit.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(nBinning) )
    #effsigma = ROOT.effSigma( hdatahist_hist_fit )

    hdatahist_histsigma = hdatahist_fit.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(1000) )
    effsigma = ROOT.effSigma( hdatahist_histsigma )

    #histCB1 = pdfCB.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(nBinning) )
    # Make a histogram of the reduced dataset for easy plotting later
    #fitdata = super(hdata_fit.__class__, hdata_fit).createHistogram( RootName(), histvar, ROOT.RooFit.Binning(400) )
    fitdata = super(hdata_fit.__class__, hdata_fit).createHistogram( RootName(), histvar, ROOT.RooFit.Binning(nBinning) )
    self.p( 'Number of entries in fit histogram: ' + str(fitdata.GetEntries()), 4 )
    self.p( 'Mean of fit histogram: ' + str(fitdata.GetMean()), 5 )

    if fitdata.GetMean() > 1.5 or fitdata.GetMean() < 0.5:
        self.p( 'WARNING: strange mean (fit is designed for 0.5 < mean < 1.5)', 5 )

    # Append results
    self.Fit[histvar.GetName()]['CBvals'].append(
        [ par.getVal() for par in [ a1, n1, mean, sig, a2, n2 ] ] )
    self.Fit[histvar.GetName()]['CBerrs'].append(
        [ par.getError() for par in [ a1, n1, mean, sig, a2, n2 ] ] )
    self.Fit[histvar.GetName()]['CBhist'].append( histCB )
    self.Fit[histvar.GetName()]['effsigma'].append( effsigma )
    self.Fit[histvar.GetName()]['fitdata'].append( fitdata )

    self.p( 'Fit parameters:', 4 )
    self.p( 'mu:       ' + str(mean.getVal()) , 5 )
    self.p( 'sigma:    ' + str(sig.getVal())  , 5 )
    self.p( 'alpha1:   ' + str(a1.getVal())   , 5 )
    self.p( 'alpha2:   ' + str(a2.getVal())   , 5 )
    self.p( 'n1:       ' + str(n1.getVal())   , 5 )
    self.p( 'n2:       ' + str(n2.getVal())   , 5 )
    self.p( 'effsigma: ' + str(effsigma)      , 5 )

    self.p( 'Distribution specifics:', 4 )
    self.p( 'mean:     ' + str(hdata_fit.mean(histvar)) , 5 )
    self.p( 'sigma:    ' + str(hdata_fit.sigma(histvar)), 5 )
    self.p( 'entries:  ' + str(hdata_fit.numEntries())  , 5 )




###################################TRY TO FIT WITH GAUS


def FitSlicesGaus( self ):

    ########################################
    # Fill the Fit dict
    ########################################

    self.p( 'SlicePlot for {0} (bins from {1} to {2})'.format(
            self.slicevarname, self.bounds[0], self.bounds[-1] ), 1 )

    self.Fit = {}
    for histvar in self.histvars:
        self.Fit[histvar.GetName()] = {
            'Gausvals'     : [],
            'Gauserrs'     : [],
            'effsigma'   : [],
            'fitdata'    : [],
            'Gaushist'     : [],
            'Gausfit'     : [],
            }


    for i in xrange( self.n_bins ):

        x_min = self.bounds[i]
        x_max = self.bounds[i+1]

        #sel_str = '{0}>{1}&&{0}<{2}'.format( self.slicevarname, x_min, x_max )
        sel_str = '{0}>={1}&&{0}<{2}'.format( self.slicevarname, x_min, x_max ) ###SJ
        self.p( 'Creating reduced dataset; sel_str = ' + sel_str )
        hdata_reduced = self.hdata.reduce(sel_str)
        print "entries in this data set is ",hdata_reduced.numEntries()
        for histvar in self.histvars:
            #self.FitOneSlice( hdata_reduced, histvar )
            self.FitOneSliceGaus( hdata_reduced, histvar )


    # Delete the big data set
    del self.hdata

    self.p( 'Dumping instance to {0}.pickle'.format(self.longname), 1 )
    if not os.path.isdir( self.pickledir ): os.makedirs( self.pickledir )
    with open( os.path.join( self.pickledir, self.longname + '.pickle' ), 'wb' ) as pickle_fp:
        pickle.dump( self, pickle_fp )


def FitOneSliceGaus( self, hdata_reduced, histvar, unbinnedFit=False ):

    # Reduce dataset to one column, only for fitting
    hdata_fit = hdata_reduced.reduce( ROOT.RooArgSet(histvar) )
    ##get roodatahist
    hdata_fit_datahist = hdata_fit.binnedClone( RootName() )
    ###get TH1F from ths
    hdata_fit_hist = hdata_fit_datahist.createHistogram(RootName(), histvar)


    hdatahist_fit = ROOT.RooDataHist(
        RootName(), RootName(),
        ROOT.RooArgSet( histvar ),
        hdata_fit
        )


    
    nBinning = 50
    #nBinning = 100

    hdatahist_hist_fit = hdatahist_fit.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(nBinning) )

    peak = hdatahist_hist_fit.GetXaxis().GetBinCenter(hdatahist_hist_fit.GetMaximumBin())
    histrms  = hdatahist_hist_fit.GetRMS()
    
    #self.fit_x_min = peak - 0.5*histrms
    #self.fit_x_max = peak + 0.5*histrms

    mean  = hdata_fit_hist.GetMean()

#    self.fit_x_min = peak - 0.8*histrms
#    self.fit_x_max = peak + 0.8*histrms


#    self.fit_x_min = peak - 0.4*histrms
#    self.fit_x_max = peak + 0.4*histrms


#    self.fit_x_min = peak - 0.6*histrms

#    self.fit_x_min = peak - 0.4*histrms
#    self.fit_x_max = peak + 0.5*histrms

    self.fit_x_min = peak - 0.6*histrms
    self.fit_x_max = peak + 0.6*histrms


    #self.fit_x_min = peak - 0.4*histrms
    #self.fit_x_min = peak - 0.4*histrms
    #self.fit_x_max = peak + 0.4*histrms

#    self.fit_x_min = mean - 0.8*histrms
#    self.fit_x_max = mean + 0.7*histrms

    print " peak is", peak, "rms is ", histrms, " Min and max of  range of fit ", self.fit_x_min, " to ",self.fit_x_max

    histmean = hdata_fit_hist.GetMean()  

    self.tfGaus = 0
    self.tfGaus = ROOT.TF1( RootName(),'gaus',self.fit_x_min,self.fit_x_max)
    self.tfGaus.SetLineColor(2)
#    self.tfGaus.SetParameter(1,peak)
#    self.tfGaus.SetParameter(2,histrms)
    

    self.p( 'Fitting GAUS to dataset (histvar: {0}, fitrange: {1} to {2})'.format(
            histvar.GetName(), self.fit_x_min, self.fit_x_max ), 3 )

    self.p( 'Number of entries in fit dataset: ' + str(hdata_fit.numEntries()), 4 )
    


    



    hdatahist_hist_fit.Fit(self.tfGaus,"R")
    mean = self.tfGaus.GetParameter(1)
    sig = self.tfGaus.GetParameter(2)
    #self.tfGaus.SetParameter(1,mean)
    #self.tfGaus.SetParameter(2,sig)
    hdatahist_hist_fit.Fit(self.tfGaus,"R")
    #hdatahist_hist_fit.Fit(self.tfGaus,"R")
    
    hdatahist_hist_fit1 = hdatahist_fit.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(nBinning) )

    histbinning = nBinning
    hist_fitgaus = self.tfGaus.CreateHistogram()
    hist_fitgaus.SetLineColor(4)
    hist_fitgaus.SetLineWidth(3)
    
    #########Now plot the var on canvas#####
#    c = setCanvas()
#    hdatahist_hist_fit.Draw()
#    tfGaus.Draw("same")
#    c.Modified()
#    c.Update()
#    pngname='{0}.png'.format(self.longname)
#    c.Print( "%s" %(pngname) )
#
    


    mean = self.tfGaus.GetParameter(1)
    sig = self.tfGaus.GetParameter(2)

    meanerr = self.tfGaus.GetParError(1)
    sigerr = self.tfGaus.GetParError(2)

    #effsigma = ROOT.effSigma( hdatahist_hist_fit )

    hdatahist_histsigma = hdatahist_fit.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(1000) )
    effsigma = ROOT.effSigma( hdatahist_histsigma )

    # Make a histogram of the reduced dataset for easy plotting later

    fitdata = super(hdata_fit.__class__, hdata_fit).createHistogram( RootName(), histvar, ROOT.RooFit.Binning(histbinning) )
    self.p( 'Number of entries in fit histogram: ' + str(fitdata.GetEntries()), 4 )
    self.p( 'Mean of fit histogram: ' + str(fitdata.GetMean()), 5 )

    if fitdata.GetMean() > 1.5 or fitdata.GetMean() < 0.5:
        self.p( 'WARNING: strange mean (fit is designed for 0.5 < mean < 1.5)', 5 )

    # Append results
    self.Fit[histvar.GetName()]['Gausvals'].append(
        #[ par.getVal() for par in [ a1, n1, mean, sig, a2, n2 ] ] )
        [ par for par in [ mean, sig ] ] )
    self.Fit[histvar.GetName()]['Gauserrs'].append(
        #[ par.getError() for par in [ a1, n1, mean, sig, a2, n2 ] ] )
        #[ par for par in [ meanerr, sigerr ] ] )
        [ par for par in [ meanerr, 0.0 ] ] )
    #self.Fit[histvar.GetName()]['Gaushist'].append( hdatahist_hist_fit1 )
    self.Fit[histvar.GetName()]['Gaushist'].append( hdatahist_hist_fit )
    self.Fit[histvar.GetName()]['Gausfit'].append( self.tfGaus )
    #self.Fit[histvar.GetName()]['Gausfit'].append( hist_fitgaus )
    self.Fit[histvar.GetName()]['effsigma'].append( effsigma )
    self.Fit[histvar.GetName()]['fitdata'].append( fitdata )
    #self.Fit[histvar.GetName()]['fitdata'].append( hdatahist_hist_fit )

    self.p( 'Fit parameters:', 2 )
    self.p( 'mu:       ' + str(mean) , 5 )
    self.p( 'sigma:    ' + str(sig)  , 5 )
    #self.p( 'alpha1:   ' + str(a1.getVal())   , 5 )
    #self.p( 'alpha2:   ' + str(a2.getVal())   , 5 )
    #self.p( 'n1:       ' + str(n1.getVal())   , 5 )
    #self.p( 'n2:       ' + str(n2.getVal())   , 5 )
    self.p( 'effsigma: ' + str(effsigma)      , 5 )

    self.p( 'Distribution specifics:', 3 )
    self.p( 'mean:     ' + str(hdata_fit.mean(histvar)) , 5 )
    self.p( 'sigma:    ' + str(hdata_fit.sigma(histvar)), 5 )
    self.p( 'entries:  ' + str(hdata_fit.numEntries())  , 5 )



######################################MAXIMA of the distribution###############################
def FitSlicesMax( self ):

    ########################################
    # Fill the Fit dict
    ########################################

    self.p( 'SlicePlot for {0} (bins from {1} to {2})'.format(
            self.slicevarname, self.bounds[0], self.bounds[-1] ), 1 )

    self.Fit = {}
    for histvar in self.histvars:
        self.Fit[histvar.GetName()] = {
            'Maxvals'     : [],
            'Maxerrs'     : [],
            'effsigma'   : [],
            'Maxhist'     : [],
            }


    for i in xrange( self.n_bins ):

        x_min = self.bounds[i]
        x_max = self.bounds[i+1]

        #sel_str = '{0}>{1}&&{0}<{2}'.format( self.slicevarname, x_min, x_max )
        sel_str = '{0}>={1}&&{0}<{2}'.format( self.slicevarname, x_min, x_max ) ###SJ
        self.p( 'Creating reduced dataset; sel_str = ' + sel_str )
        hdata_reduced = self.hdata.reduce(sel_str)
        print "entries in this data set is ",hdata_reduced.numEntries()
        for histvar in self.histvars:
            #self.FitOneSlice( hdata_reduced, histvar )
            self.FitOneSliceMax( hdata_reduced, histvar )


    # Delete the big data set
    del self.hdata

    self.p( 'Dumping instance to {0}.pickle'.format(self.longname), 1 )
    if not os.path.isdir( self.pickledir ): os.makedirs( self.pickledir )
    with open( os.path.join( self.pickledir, self.longname + '.pickle' ), 'wb' ) as pickle_fp:
        pickle.dump( self, pickle_fp )


def FitOneSliceMax( self, hdata_reduced, histvar, unbinnedFit=False ):

    # Reduce dataset to one column, only for fitting
    hdata_fit = hdata_reduced.reduce( ROOT.RooArgSet(histvar) )
    ##get roodatahist
    hdata_fit_datahist = hdata_fit.binnedClone( RootName() )
    ###get TH1F from ths
    hdata_fit_hist = hdata_fit_datahist.createHistogram(RootName(), histvar)
    
    peak = hdata_fit_hist.GetXaxis().GetBinCenter(hdata_fit_hist.GetMaximumBin())
    histrms  = hdata_fit_hist.GetRMS()
    
    
    print " peak is", peak, "rms is ", histrms

    histmean = hdata_fit_hist.GetMean()  

    

    self.p( 'Fitting GAUS to dataset (histvar: {0}, fitrange: {1} to {2})'.format(
            histvar.GetName(), self.fit_x_min, self.fit_x_max ), 3 )

    self.p( 'Number of entries in fit dataset: ' + str(hdata_fit.numEntries()), 4 )
    


    nBinning = 50

    hdatahist_fit = ROOT.RooDataHist(
        RootName(), RootName(),
        ROOT.RooArgSet( histvar ),
        hdata_fit
        )


    hdatahist_hist_fit1 = hdatahist_fit.createHistogram( RootName(), histvar, ROOT.RooFit.Binning(nBinning) )

    
    
    effsigma = ROOT.effSigma( hdatahist_hist_fit1 )

    # Append results
    self.Fit[histvar.GetName()]['Maxvals'].append(
        [ par for par in [ peak, effsigma ] ] )
    self.Fit[histvar.GetName()]['Maxerrs'].append(
        #[ par.getError() for par in [ a1, n1, mean, sig, a2, n2 ] ] )
        [ par for par in [ 0, 0 ] ] )
    self.Fit[histvar.GetName()]['Maxhist'].append( hdatahist_hist_fit1 )
    self.Fit[histvar.GetName()]['effsigma'].append( effsigma )

    self.p( 'Fit parameters:', 2 )
    self.p( 'mu:       ' + str(peak) , 5 )
    self.p( 'sigma:    ' + str(effsigma)  , 5 )
    #self.p( 'alpha1:   ' + str(a1.getVal())   , 5 )
    #self.p( 'alpha2:   ' + str(a2.getVal())   , 5 )
    #self.p( 'n1:       ' + str(n1.getVal())   , 5 )
    #self.p( 'n2:       ' + str(n2.getVal())   , 5 )
    self.p( 'effsigma: ' + str(effsigma)      , 5 )

    self.p( 'Distribution specifics:', 3 )
    self.p( 'mean:     ' + str(hdata_fit.mean(histvar)) , 5 )
    self.p( 'sigma:    ' + str(hdata_fit.sigma(histvar)), 5 )
    self.p( 'entries:  ' + str(hdata_fit.numEntries())  , 5 )


######For drawing purpose
def setCanvas():
    
    W = 800
    H = 600
    H_ref = 600
    W_ref = 800
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref
    
#    setTDRStyle()
    c = ROOT.TCanvas('c','c',50,50,W,H)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )

    return c
