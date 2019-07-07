#!/usr/bin/env python
"""
Thomas:
"""

########################################
# Imports
########################################

import os
import argparse
import pickle

# Change directory to location of this source file
execDir = os.path.dirname( os.path.abspath(__file__) )
os.chdir( execDir )

import sys
sys.path.append('src')

from SlicePlot import SlicePlot

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = kError;")
ROOT.RooMsgService.instance().setSilentMode(True)

ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Eval )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Generation )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Minimization )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Plotting )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Fitting )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Integration )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.LinkStateMgmt )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Caching )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Optimization )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.ObjectHandling )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.InputArguments )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Tracing )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Contents )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.DataHandling )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.NumIntegration )
ROOT.RooMsgService.instance().getStream(1).removeTopic( ROOT.RooFit.Eval )

ROOT.gSystem.Load("libHiggsAnalysisGBRLikelihood")
ROOT.gROOT.LoadMacro( os.getcwd() + "/src/LoadDataset.C" )

# Paths to regression results
result_path = os.getcwd()


########################################
# Main
########################################

def Fit():

    ########################################
    # Command line options
    ########################################

    parser = argparse.ArgumentParser()
    parser.add_argument( '--region', type=str, default='TODO', choices=[ 'EB', 'EE', 'TODO' ] )
    #parser.add_argument( '--flag', type=str, default='TODO', choices=[ 'ZS', 'FULL', 'TODO' ] )
    parser.add_argument( '--flag', type=str, default='TODO', choices=[ 'ZS', 'FULL', 'ALL', 'TODO' ] )
    parser.add_argument( '--ntup', type=str, help='Pass path to an Ntuple')
    parser.add_argument( '--fitfun', type=str, default='CB', choices=['CB', 'Gaus', 'Max'])
    parser.add_argument( '--ptbins', metavar='N', type=float, nargs='+',
                         help='supply a list of global pt bins (there is a default list in the code)' )
    args = parser.parse_args()


    ########################################
    # Settings
    ########################################
    doALL = False
    # Region needs to be determined carefully because the right workspace needs to be loaded
    if args.region == 'EB':
        region = 'EB'
        dobarrel = True
    elif args.region == 'EE':
        region = 'EE'
        dobarrel = False

    if args.flag == 'ZS':
        flag = 'ZS'
        doZS = True
    elif args.flag == 'FULL':
        flag = 'FULL'
        doZS = False
    elif args.flag == 'ALL':
        flag = 'ALL'
        doZS = False
        doALL = True


    fit = 'CB'
    if args.fitfun == 'Gaus':
        fit = 'Gaus'
    elif args.fitfun == 'Max':
        fit = 'Max'
    else:
        fit = 'CB'

    plotdir = 'plotsPY_pfClusters_{0}_{1}'.format( region, flag )

    tree_name = 'PfTree'

    pline()
    print 'Summary of input data for Fit.py:'
    print '    region:    ' + region
    print '    flag:      ' + flag
    print '    plotdir:   ' + plotdir
    print '    ntuple:    ' + args.ntup
    print '    ntup tree: ' + tree_name


    ########################################
    # FITTING PROCEDURE
    ########################################

    # ======================================
    # Get the workspace and set the variables

    pline()

    clusrawE  = ROOT.RooRealVar("clusrawE", "clusrawE", 0.)
    cluscorrE = ROOT.RooRealVar("cluscorrE", "cluscorrE", 0.)
    clusPt    = ROOT.RooRealVar("clusPt", "clusPt", 0.)
    clusEta   = ROOT.RooRealVar("clusEta", "clusEta", 0.)
    clusPhi   = ROOT.RooRealVar("clusPhi", "clusPhi", 0.)
    clusSize  = ROOT.RooRealVar("clusSize", "clusSize", 0.)
    clusPS1   = ROOT.RooRealVar("clusPS1", "clusPS1", 0.)
    clusPS2   = ROOT.RooRealVar("clusPS2", "clusPS2", 0.)
    clusFlag  = ROOT.RooRealVar("clusFlag", "clusFlag", 0.)
    nvtx      = ROOT.RooRealVar("nvtx", "nvtx", 0.)
    genEnergy = ROOT.RooRealVar("genEnergy", "genEnergy", 0.)
    genPt     = ROOT.RooRealVar("genPt", "genPt", 0.)
    genEta    = ROOT.RooRealVar("genEta", "genEta", 0.)
    genPhi    = ROOT.RooRealVar("genPhi", "genPhi", 0.)
    e91X      = ROOT.RooRealVar("e91X", "e91X", 0.)
#    ietamod20      = ROOT.RooRealVar("ietamod20", "ietamod20", 0.)
#    iphimod20      = ROOT.RooRealVar("iphimod20", "iphimod20", 0.)
    clusIetaIx      = ROOT.RooRealVar("clusIetaIx", "clusIetaIx", 0.)
    clusIphiIy      = ROOT.RooRealVar("clusIphiIy", "clusIphiIy", 0.)

    
    # ======================================
    # Set ranges where reasonably possible

#    clusrawE.setRange(0., 350.)
#    cluscorrE.setRange(0., 350.)
#    genEnergy.setRange(0., 350.)
#
#    clusPt.setRange(0., 150.)
#    genPt.setRange(0., 150.)
#
#    clusPhi.setRange(-ROOT.TMath.Pi(), ROOT.TMath.Pi())
#    genPhi.setRange(-ROOT.TMath.Pi(), ROOT.TMath.Pi())
#
#    clusSize.setRange(0., 30.)
#    nvtx.setRange(0., 80.)
#
#    if dobarrel:
#        clusEta.setRange(-1.6, 1.6)
#        genEta.setRange(-1.6, 1.6)
#    else:
#        clusEta.setRange(-3.,3.)
#        genEta.setRange(-3,3)
#
#    if doZS:
#        clusPt.setRange(0., 6.)
#        genPt.setRange(0., 6.)        
#
    # ======================================
    # Define which vars to use

    Vars = [
        clusrawE,
        cluscorrE,
        clusPt,
        clusEta,
        clusPhi,
        clusSize,
        clusPS1,
        clusPS2,
        clusFlag,
        nvtx,
        genEnergy,
        genPt,
        genEta,
        genPhi,
        e91X,
#        ietamod20,
        clusIetaIx,
        clusIphiIy,
        
        ]

    VarsArgList = ROOT.RooArgList()
    for Var in Vars: VarsArgList.add(Var)


    # ======================================
    # Create the dataset

    print 'Getting dataset (using the macro)'
    #eventcut = ''
    eventcut = 'clusrawE > 0.25'

    #eventcut = 'clusrawE > 0.25 && clusEta<2.5 && clusEta>-2.5'
    #eventcut = 'clusrawE > 0.25 && clusEta<2. && clusEta>-2.'
    hdata = ROOT.LoadDataset( eventcut, dobarrel, doZS, doALL, args.ntup, 'een_analyzer', tree_name, VarsArgList )
    print '  Using {0} entries'.format( hdata.numEntries() )


    ########################################
    # Add columns to dataset for E_raw,cor,cor74 over E_true
    ########################################

    # NOTE: BRACKETS AROUND THE FORMULA ARE EXTREMELY IMPORTANT
    #       There is no error message, but the results are interpreted totally different without the brackets!
    #       Or it is the RooArgLists that can't be passed in the defition of the RooFormula directly

    nBinningHistVars = 2000

    rawArgList = ROOT.RooArgList( clusrawE, genEnergy )    
    rawformula = ROOT.RooFormulaVar( 'rawformula', 'raw', '(@0/@1)', rawArgList )
    
    ####added on 26th march
    if args.region == 'EE':
        rawArgList = ROOT.RooArgList( clusrawE, genEnergy, clusPS1, clusPS1 ) 
        rawformula = ROOT.RooFormulaVar( 'rawformula', 'raw', '((@0+@2+@3)/@1)', rawArgList )


    rawvar = hdata.addColumn(rawformula)
    rawvar.setRange( 0., 2. )
    rawvar.setBins(nBinningHistVars)

    ecor74ArgList = ROOT.RooArgList( cluscorrE, genEnergy )
    ecor74formula = ROOT.RooFormulaVar( 'ecor74formula', 'corr. (91X)', '(@0/@1)', ecor74ArgList )
    ecor74var = hdata.addColumn(ecor74formula)
    ecor74var.setRange( 0., 2. )
    ecor74var.setBins(nBinningHistVars)

    ecor91ArgList = ROOT.RooArgList( e91X, genEnergy )
    ecor91formula = ROOT.RooFormulaVar( 'ecor91formula', 'corr. (10X)', '(@0/@1)', ecor91ArgList )
    #ecor91formula = ROOT.RooFormulaVar( 'ecor91formula', 'corr. (94X)', '(@0/@1)', ecor91ArgList )
    ecor91var = hdata.addColumn(ecor91formula)
    ecor91var.setRange( 0., 2. )
    ecor91var.setBins(nBinningHistVars)

    
    ########################################
    # Make the fits
    ########################################

    pline()
    print 'Start fitting\n'

    if not args.ptbins:
        # Default pt bins
#        globalPt_bounds = [
#            0.25,
#            4.5,
#            18.,
#            100.
#            ]

        globalPt_bounds = [
            
            #1.2,
            2.0,
            5.0,
            20.,
            100.,
            300
            ]
#        # ZS pt bins        
        if doZS:
            globalPt_bounds = [
                0.25,  
                #0.,  
                6.0,
                #10.,
                25
                ]
                

    else:
        globalPt_bounds = args.ptbins

        
    print globalPt_bounds
#    allPt_bounds = [0.25]
#    allPt_bounds += [ 0.25  + 0.425*i for i in xrange(1,10) ]
#    allPt_bounds += [ 4.5   + 1.35*i  for i in xrange(10) ]
#    allPt_bounds += [ 18.0  + 8.2*i   for i in xrange(10) ]
#    allPt_bounds += [100.0]
#
########HERE
#    allPt_bounds = [1.2]
#    allPt_bounds = [1.2,2,4,5]
#    allPt_bounds += [ 0.25  + 0.475*i for i in xrange(3,5) ]
#    allPt_bounds += [ 2.15  + 1.425*2 ]
    #allPt_bounds = [1.2] 
    allPt_bounds = [2.0, 4, 5] 
#    allPt_bounds += [ 0.25  + 0.475*i for i in xrange(3,5) ]
#    allPt_bounds += [ 2.15  + 1.425*2 ]
    allPt_bounds += [ 5.0   + 1.5*i  for i in xrange(1,10) ]
    allPt_bounds += [ 20.0  + 8.2*i   for i in xrange(10) ]
#    allPt_bounds += [100.0]
    allPt_bounds += [100.0,150,200,250,300]

#    
    if not dobarrel and not doZS:

#        allPt_bounds = [1.2, 2, 5]
#        allPt_bounds = [1.2]
        allPt_bounds = [2.0, 4, 5]
#        allPt_bounds += [ 0.25  + 1.15*i for i in xrange(2,3) ]
#        allPt_bounds += [ 2.55  + 2.45 ]
        allPt_bounds += [ 5.0   + 1.5*i  for i in xrange(1,10) ]
        allPt_bounds += [ 20.0  + 8.2*i   for i in xrange(10) ]
#        allPt_bounds += [100.0]
        allPt_bounds += [100.0,150,200,250,300]

        
#    allPt_bounds = [0.25,6.0,20.0,100.]

    if doZS:
        #allPt_bounds = [ 0.25  + 0.575*i for i in xrange(11) ]
        #allPt_bounds = [ 0.25  + 1.15*i for i in xrange(6) ] ###SJ
        #allPt_bounds = [ 0. ]
        #allPt_bounds += [ 0.25  + 0.475*i for i in range(10) ] ###SJ
        #allPt_bounds += [ 0.25  + 0.275*i for i in range(10) ] ###SJ
        allPt_bounds = [ 0.25  + 1.15*i for i in range(2) ] ###SJ
        #allPt_bounds += [6] ###SJ
        allPt_bounds += [6, 25.] ###SJ
        
    print allPt_bounds
    print globalPt_bounds

    for i_globalPtBin in xrange(len(globalPt_bounds)-1):

        min_globalPt = globalPt_bounds[i_globalPtBin]
        max_globalPt = globalPt_bounds[i_globalPtBin+1]

        if not fit=='Max':
            if i_globalPtBin==0:
                fit='Gaus'
            else:
                fit ='CB'
                
        if fit == 'Max':
            fit = 'Max'
            #fit ='Gaus'
            
#        if doZS:
#            fit = 'CB'

        if doZS:
            fit = 'Gaus'



        print '    Reducing total dataset to genPt between {0} and {1}'.format( min_globalPt, max_globalPt )
        hdata_globalPtBin = hdata.reduce( 'genPt>{0}&&genPt<{1}'.format( min_globalPt, max_globalPt ) )
        print "pT selection : ",min_globalPt," ",max_globalPt
        print '        Number of entries in this genPt selection: ' + str(hdata_globalPtBin.numEntries())

        histogramVariables = [
            rawvar,
            #ecor74var,
            ecor91var,
            ]
        
        # ======================================
        # genPt plot

        # Get the finer genPt bounds inside this global bin
        localPt_bounds = allPt_bounds[ allPt_bounds.index(min_globalPt) : allPt_bounds.index(max_globalPt) + 1 ]

        # genPt_name = 'GENPT{0}-{1}'.format( int(min_globalPt), int(max_globalPt) )
        #genPt_name = 'GENPT-{0:04d}-{1:04d}'.format( int(min_globalPt), int(max_globalPt) )

        genPt_name = '{0:s}{1:s}_GENPT_{2:04d}_{3:04d}'.format( region, flag, int(min_globalPt), int(max_globalPt) )
        genPt_sliceplot = SlicePlot(
            name     = genPt_name,
            longname = region + flag + '_' + genPt_name,
            plotdir  = plotdir
            )
        genPt_sliceplot.SetDataset( hdata_globalPtBin )
        genPt_sliceplot.SetHistVars( histogramVariables )
        genPt_sliceplot.SetSliceVar(
            genPt,
            localPt_bounds,
            'p_{t, gen}'
            )

        print "fit is ", fit 
        if fit=='Gaus':
            genPt_sliceplot.FitSlicesGaus()

        elif fit=='Max':
            genPt_sliceplot.FitSlicesMax()
    
        else:
            genPt_sliceplot.FitSlices()

        # ======================================
        # genEta plot

        if dobarrel:
            #genEta_bounds = [ 0.0 + 0.075*i for i in xrange(21) ]
#            genEta_bounds = [ 0.0 + 0.1*i for i in xrange(16) ]
            genEta_bounds = [ 0.0 + 0.14*i for i in xrange(11) ]
        else:
            #genEta_bounds = [ 1.4 + 0.055*i for i in xrange(21) ]
            #genEta_bounds = [ 1.4,1.51]
            #genEta_bounds += [ 1.565 + 0.055*i for i in xrange(20) ]

            genEta_bounds = [ 1.4,1.565]
            #genEta_bounds += [ 1.62 + 0.055*i for i in xrange(22) ]
#            genEta_bounds += [ 1.62 + 0.1*i for i in xrange(10) ]
#            genEta_bounds += [ 1.62 + 0.15*i for i in xrange(7) ]

            #genEta_bounds += [ 1.6 + 0.2*i for i in xrange(5) ]
            #genEta_bounds += [3.0]
            genEta_bounds += [ 1.6 + 0.2*i for i in xrange(4) ]
            genEta_bounds += [2.5, 3.0]

#        if dobarrel:
#            genEta_bounds = [ 0.0 + 0.075*2*i for i in xrange(11) ]
#        else:
#            genEta_bounds = [ 1.4 + 0.055*2*i for i in xrange(11) ]
#
        #genEta_name = 'GENETA-{0:04d}-{1:04d}'.format( int(min_globalPt), int(max_globalPt) )
        genEta_name = '{0:s}{1:s}_GENETA_{2:04d}_{3:04d}'.format( region, flag, int(min_globalPt), int(max_globalPt) )
        genEta_sliceplot = SlicePlot(
            name     = genEta_name,
            longname = region + flag + '_' + genEta_name,
            plotdir  = plotdir
            )
        genEta_sliceplot.SetDataset( hdata_globalPtBin )
        genEta_sliceplot.SetHistVars(histogramVariables)
        genEta_sliceplot.SetSliceVar(
            genEta,
            genEta_bounds,
            '#eta_{gen}'
            )
        if fit=='Gaus':
            genEta_sliceplot.FitSlicesGaus()
        elif fit=='Max':
            genEta_sliceplot.FitSlicesMax()

        else:
            genEta_sliceplot.FitSlices()

        # ======================================
        # nvtx plot

        #nvtx_bounds = [ 0.0 + 5*i for i in xrange(13) ]
        nvtx_bounds = [ 1.0 + 5*i for i in xrange(13) ]

        #nvtx_name = 'NVTX-{0:04d}-{1:04d}'.format( int(min_globalPt), int(max_globalPt) )
        nvtx_name = '{0:s}{1:s}_NVTX_{2:04d}_{3:04d}'.format(  region, flag, int(min_globalPt), int(max_globalPt) )
        nvtx_sliceplot = SlicePlot(
            name     = nvtx_name,
            longname = region + flag + '_' + nvtx_name,
            plotdir  = plotdir
            )
        nvtx_sliceplot.SetDataset( hdata_globalPtBin )
        nvtx_sliceplot.SetHistVars(histogramVariables)
        nvtx_sliceplot.SetSliceVar(
            nvtx,
            nvtx_bounds,
            'n_{vtx}'
            )
        if fit=='Gaus':
            nvtx_sliceplot.FitSlicesGaus()
        elif fit=='Max':
            nvtx_sliceplot.FitSlicesMax()

        else:
            nvtx_sliceplot.FitSlices()

        # ======================================
        # clusSize plot

        if doZS:
            #clusSize_bounds = [ 0.0 + i for i in xrange(6) ]
            #clusSize_bounds = [ 1.0 + i for i in xrange(6) ]
            clusSize_bounds = [ 1.0 + i for i in xrange(3) ]
            clusSize_bounds += [6]
        else:
            #clusSize_bounds = [ 0.0 + 5*i for i in xrange(6) ]
            #clusSize_bounds = [ 1.0 + i for i in xrange(5) ]
            #clusSize_bounds += [5 + i*5 for i in xrange(1,5) ]
            clusSize_bounds  = [ 1,2,3,7]
            clusSize_bounds += [7+i*5 for i in xrange(1,5) ]
        
        #clusSize_name = 'CLUSSIZE-{0:04d}-{1:04d}'.format( int(min_globalPt), int(max_globalPt) )
        clusSize_name = '{0:s}{1:s}_CLUSSIZE_{2:04d}_{3:04d}'.format( region, flag,int(min_globalPt), int(max_globalPt) )
        clusSize_sliceplot = SlicePlot(
            name     = clusSize_name,
            longname = region + flag + '_' + clusSize_name,
            plotdir  = plotdir
            )
        clusSize_sliceplot.SetDataset( hdata_globalPtBin )
        clusSize_sliceplot.SetHistVars(histogramVariables)
        clusSize_sliceplot.SetSliceVar(
            clusSize,
            clusSize_bounds,
            'size'
            )
        if fit=='Gaus':
            clusSize_sliceplot.FitSlicesGaus()
        elif fit=='Max':
            clusSize_sliceplot.FitSlicesMax()

        else:
            clusSize_sliceplot.FitSlices()


        # ======================================
        # ieta plot

        if dobarrel:
            clusIetaIx_bounds = [ -85 + i for i in xrange(170) ]
            print "Bounds of iEta "
            print clusIetaIx_bounds
            clusIetaIx_name = '{0:s}{1:s}_iETA_{2:04d}_{3:04d}'.format( region, flag, int(min_globalPt), int(max_globalPt) )
            clusIetaIx_sliceplot = SlicePlot(
                name     = clusIetaIx_name,
                longname = region + flag + '_' + clusIetaIx_name,
                plotdir  = plotdir
                )
            clusIetaIx_sliceplot.SetDataset( hdata_globalPtBin )
            clusIetaIx_sliceplot.SetHistVars(histogramVariables)
            clusIetaIx_sliceplot.SetSliceVar(
                clusIetaIx,
                clusIetaIx_bounds,
                'i#eta'
                )
            clusIetaIx_sliceplot.FitSlices()

        # ======================================


        # ======================================
        # ieta plot

        if dobarrel:
            #clusIphiIy_bounds = [ 2*i for i in xrange(80) ]
            clusIphiIy_bounds = [ i for i in xrange(180) ]
            print "Bounds of iPhi "
            print clusIphiIy_bounds
            clusIphiIy_name = '{0:s}{1:s}_iPHI_{2:04d}_{3:04d}'.format( region, flag, int(min_globalPt), int(max_globalPt) )
            clusIphiIy_sliceplot = SlicePlot(
                name     = clusIphiIy_name,
                longname = region + flag + '_' + clusIphiIy_name,
                plotdir  = plotdir
                )
            clusIphiIy_sliceplot.SetDataset( hdata_globalPtBin )
            clusIphiIy_sliceplot.SetHistVars(histogramVariables)
            clusIphiIy_sliceplot.SetSliceVar(
                clusIphiIy,
                clusIphiIy_bounds,
                'i#phi'
                )
            clusIphiIy_sliceplot.FitSlices()

        # ======================================
        

########################################
# Functions
########################################

def pline(s='='):
    print '\n' + s*70


########################################
# End of Main
########################################
if __name__ == "__main__":
    Fit()
