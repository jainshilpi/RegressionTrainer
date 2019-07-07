import os
import pickle
from math import sqrt, exp,log
from array import array

import ROOT
ROOT.gROOT.SetBatch(True)


cWidth = 887
cHeight = int( (800./1000.) * cWidth )

c = ROOT.TCanvas( 'c', 'c', cWidth, cHeight )


xAxisLabelDict = {
    'genPt' : 'p_{t, gen} [GeV]',
    }




def MakePlots_standard( self ):

    ########################################
    # Plotting
    ########################################

    self.p( 'Making plots the standard way', 1 )


    # ======================================
    # Per bin fits

    # Find a clever number of divisions for the canvas
    int_sqrt_bins = int(sqrt(self.n_bins))
    dec_sqrt_bins = sqrt(self.n_bins) - int_sqrt_bins

    if dec_sqrt_bins < 0.0000001:
        n_columns = int_sqrt_bins
        n_rows    = int_sqrt_bins
    elif dec_sqrt_bins < 0.5:
        n_columns = int_sqrt_bins + 1
        n_rows    = int_sqrt_bins
    else:
        n_columns = int_sqrt_bins + 1
        n_rows    = int_sqrt_bins + 1

    c.Divide( n_columns, n_rows )


    # Should really be True except in exceptional plots
    drawFit = True
    if hasattr( self, 'disableDrawFits' ) and self.disableDrawFits: drawFit = False


    for histvar in self.histvars:

        histvarname = histvar.GetName()

        for i_bin in xrange(self.n_bins):

            c.cd(i_bin+1)
            ROOT.gPad.SetLeftMargin(0.20)
            ROOT.gPad.SetBottomMargin(0.14)
            ROOT.gPad.SetRightMargin(0.01)
            ROOT.gPad.SetTopMargin(0.1)

            H = self.Fit[histvarname]['fitdata'][i_bin]

            if not drawFit:
                H = H.Rebin(10)

            H.Draw()

            histvartitle = 'E_{{{0}}}/E_{{true}}'.format( histvar.GetTitle() )
            # Default is to assume it's an energy ratio, if not change the plotting label a bit
            if hasattr( self, 'notAnEnergyRatio' ) and self.notAnEnergyRatio:
                histvartitle = histvar.GetTitle()

            H.SetTitle( '{0} ( {2} <= {1} < {3} )'.format(
                histvartitle,
                self.slicevarname,
                self.bounds[i_bin], self.bounds[i_bin+1]
                ))
            H.SetTitleSize(0.06);

            H.GetXaxis().SetTitle( histvartitle )
            #H.GetXaxis().SetRangeUser( 0.7, 1.2 );
            #H.GetXaxis().SetRangeUser( 0.7, 1.4 );
            H.GetXaxis().SetRangeUser( 0.6, 1.6 );

            H.GetXaxis().SetLabelSize(0.05);
            H.GetXaxis().SetTitleSize(0.06);
            H.GetYaxis().SetLabelSize(0.05);
            H.GetYaxis().SetTitleSize(0.06);


            if drawFit:
                H_CB = self.Fit[histvarname]['CBhist'][i_bin]
                H_CB.Scale( H.Integral() / H_CB.Integral() * H_CB.GetNbinsX() / H.GetNbinsX() )
                H_CB.SetLineColor(2)
                H_CB.Draw('HISTSAMEL')


                # ======================================
                # Labels

                lx = 0.24
                ly = 0.88
                nl = 0.07
                nc = 0.1

                l = ROOT.TLatex()
                l.SetTextAlign(13)
                l.SetNDC()
                l.SetTextSize(0.05)

                l.DrawLatex( lx, ly, 'CB parameters' )
                ly -= nl+0.02

                parvalues = self.Fit[histvarname]['CBvals'][i_bin]
                partitles = [ '#alpha_{1}', 'n_{1}', '#mu', '#sigma', '#alpha_{2}', 'n_{2}' ]

                for parvalue, partitle in zip( parvalues, partitles ):
                    l.DrawLatex( lx,     ly, partitle )
                    l.DrawLatex( lx+nc, ly, '{0:.4f}'.format(parvalue) )
                    ly -= nl
                ly -= 0.015
                l.DrawLatex( lx,    ly, '#sigma_{eff}' )
                l.DrawLatex( lx+nc, ly, '{0:.4f}'.format( self.Fit[histvarname]['effsigma'][i_bin] ) )


        self.Save( c, 'PerBinFit' + histvarname.capitalize() )


    # ======================================
    # Plot of variable over slices

    c.Clear()

    c.SetLeftMargin(   self.sliceplot_LeftMargin )
    c.SetRightMargin(  self.sliceplot_RightMargin )
    c.SetBottomMargin( self.sliceplot_BottomMargin )
    c.SetTopMargin(    self.sliceplot_TopMargin )

    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()


    base = ROOT.TH1F()
    base.Draw()

    print "histvar name is ", histvarname
    print "self.name ",self.name
    if self.name == 'EBFULL_GENPT_0020_0100':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.1
    
    if self.name == 'EEFULL_GENPT_0020_0100':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.1
    
    if self.name == 'EBFULL_GENETA_0020_0100':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.1
    
    if self.name == 'EEFULL_GENETA_0020_0100':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.1

#######2nd pt bin
    if self.name == 'EBFULL_GENPT_0005_0020':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
#        self.sliceplotsigma_y_max = 0.2
        self.sliceplotsigma_y_max = 0.2
    
    if self.name == 'EEFULL_GENPT_0005_0020':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.2
    
    if self.name == 'EBFULL_GENETA_0005_0020':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.2
    
    if self.name == 'EEFULL_GENETA_0005_0020':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.2


#######3rd pt bin
    if self.name == 'EBFULL_GENPT_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3
    
    if self.name == 'EEFULL_GENPT_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3
    
    if self.name == 'EBFULL_GENETA_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3
    
    if self.name == 'EEFULL_GENETA_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3
        

    
    base.GetXaxis().SetLimits( self.bounds[0], self.bounds[-1] )
    base.SetMinimum(self.sliceplot_y_min)
    base.SetMaximum(self.sliceplot_y_max)




    if self.slicevarname in xAxisLabelDict:
        base.GetXaxis().SetTitle( xAxisLabelDict[self.slicevarname] )
    elif hasattr( self, 'slicevartitle' ):
        base.GetXaxis().SetTitle( self.slicevartitle )
    else:
        # This here so it's still possible to plot old fits
        base.GetXaxis().SetTitle( self.slicevarname )


    base.GetXaxis().SetNdivisions(505)
    base.GetYaxis().SetTitleOffset(1.1)
    base.GetXaxis().SetLabelSize(0.05)
    base.GetXaxis().SetTitleSize(0.06)
    base.GetYaxis().SetLabelSize(0.05)
    base.GetYaxis().SetTitleSize(0.06)


    # First the means

    base.GetYaxis().SetTitle( '#mu' )

    leg_mu = ROOT.TLegend(
        self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin,
        1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    leg_mu.SetNColumns(3)
    leg_mu.SetFillStyle(0)

    Hmus = []
    Hmus_filled = []
    for i_histvar, histvar in enumerate(self.histvars):

        Hmu = ROOT.TH1F( 'mu_'+histvar.GetName(), '', self.n_bins, array('d',self.bounds) )

        for i_bin in xrange(self.n_bins):
            bin_width  = self.bounds[i_bin+1] - self.bounds[i_bin]
            bin_center = self.bounds[i_bin] + 0.5*bin_width
            Hmu.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['CBvals'][i_bin][2] )
            Hmu.SetBinError(   i_bin+1, self.Fit[histvar.GetName()]['CBerrs'][i_bin][2] )

        # This is the line with line error bars
        Hmu.SetMarkerSize(0)
        Hmu.SetLineColor( self.colorlist[i_histvar] )
        Hmu.SetLineWidth(2)

        # This draws filled squares around the error bars (should be drawn before the line object)
        Hmu_filled = Hmu.Clone()
        Hmu_filled.SetName( Hmu_filled.GetName() + '_clone' )
        Hmu_filled.SetFillColorAlpha( self.colorlist[i_histvar], 0.3 )
        Hmu_filled.SetMarkerSize(0)

        Hmu_filled.Draw('SAMEE2')
        Hmu.Draw('HISTSAMEE')

        # Append for persistence
        Hmus.append( Hmu )
        Hmus_filled.append( Hmu_filled )

        leg_mu.AddEntry( 'mu_' + histvar.GetName(), '#mu_{CB, ' + histvar.GetTitle() + '}  ', 'lf' )

    leg_mu.Draw('SAME')
    self.Save( c, 'MuOverBins' )


    # Then the sigmas

    c.Clear()
    base.SetMinimum( self.sliceplotsigma_y_min )
    base.SetMaximum( self.sliceplotsigma_y_max )
    base.Draw()

#    base.GetYaxis().SetTitle( '#sigma_{eff}' )
    base.GetYaxis().SetTitle( '#sigma_{eff}/#mu' )

    leg_sigma = ROOT.TLegend(
        self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin,
        1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    leg_sigma.SetNColumns(3)
    leg_sigma.SetFillStyle(0)

    Hsigmas = []
    Hsigmas_filled = []
    for i_histvar, histvar in enumerate(self.histvars):

        Hsigma = ROOT.TH1F( 'sigma_'+histvar.GetName(), '', self.n_bins, array('d',self.bounds) )

        for i_bin in xrange(self.n_bins):
            bin_width  = self.bounds[i_bin+1] - self.bounds[i_bin]
            bin_center = self.bounds[i_bin] + 0.5*bin_width
            Hsigma.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['effsigma'][i_bin]/self.Fit[histvar.GetName()]['CBvals'][i_bin][2] )
            #print ""
            #print "hist name : effsigma : mean  : ", histvar.GetName(), " ",self.Fit[histvar.GetName()]['effsigma'][i_bin]," ",self.Fit[histvar.GetName()]['CBvals'][i_bin][2]
            #Hsigma.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['effsigma'][i_bin] )
            #Hsigma.SetBinError(   i_bin+1, self.Fit[histvar.GetName()]['CBerrs'][i_bin][3] )
            Hsigma.SetBinError(   i_bin+1, 0 )

        # This is the line with line error bars
        Hsigma.SetMarkerSize(0)
        Hsigma.SetLineColor( self.colorlist[i_histvar] )
        Hsigma.SetLineWidth(2)

        # This draws filled squares around the error bars (should be drawn before the line object)
        Hsigma_filled = Hsigma.Clone()
        Hsigma_filled.SetName( Hsigma_filled.GetName() + '_clone' )
        Hsigma_filled.SetFillColorAlpha( self.colorlist[i_histvar], 0.3 )
        Hsigma_filled.SetMarkerSize(0)

        #Hsigma_filled.Draw('SAMEE2')
        #Hsigma.Draw('HISTSAMEE')
        Hsigma.Draw('HISTSAME')

        # Append for persistence
        Hsigmas.append( Hsigma )
        Hsigmas_filled.append( Hsigma_filled )

        leg_sigma.AddEntry( 'sigma_' + histvar.GetName(), '#sigma_{CB, ' + histvar.GetTitle() + '}', 'lf' )


    # leg_sigma.SetBorderSize(0)
    # square = ROOT.TBox( self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin - 0.25,
    #     1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    # # square.SetFillStyle(1)
    # # square.SetLineColor(1)
    # # square.SetLineStyle(1)
    # # square.SetLineWidth(1)
    # square.Draw('SAME')

    leg_sigma.Draw('SAME')
    self.Save( c, 'EffSigmaOverBins' )


###############################################GAUS####################################
def MakePlots_standard_Gaus( self ):

    ########################################
    # Plotting
    ########################################

    self.p( 'Making plots the standard way for GAUS FIT', 1 )


    # ======================================
    # Per bin fits

    # Find a clever number of divisions for the canvas
    int_sqrt_bins = int(sqrt(self.n_bins))
    dec_sqrt_bins = sqrt(self.n_bins) - int_sqrt_bins

    if dec_sqrt_bins < 0.0000001:
        n_columns = int_sqrt_bins
        n_rows    = int_sqrt_bins
    elif dec_sqrt_bins < 0.5:
        n_columns = int_sqrt_bins + 1
        n_rows    = int_sqrt_bins
    else:
        n_columns = int_sqrt_bins + 1
        n_rows    = int_sqrt_bins + 1

    c.Divide( n_columns, n_rows )


    # Should really be True except in exceptional plots
    drawFit = True
    if hasattr( self, 'disableDrawFits' ) and self.disableDrawFits: drawFit = False


    for histvar in self.histvars:

        histvarname = histvar.GetName()

        for i_bin in xrange(self.n_bins):

            c.cd(i_bin+1)
            ROOT.gPad.SetLeftMargin(0.20)
            ROOT.gPad.SetBottomMargin(0.14)
            ROOT.gPad.SetRightMargin(0.01)
            ROOT.gPad.SetTopMargin(0.1)

            H = self.Fit[histvarname]['fitdata'][i_bin]

            if not drawFit:
                H = H.Rebin(10)

            H.Draw()

            histvartitle = 'E_{{{0}}}/E_{{true}}'.format( histvar.GetTitle() )
            # Default is to assume it's an energy ratio, if not change the plotting label a bit
            if hasattr( self, 'notAnEnergyRatio' ) and self.notAnEnergyRatio:
                histvartitle = histvar.GetTitle()

            H.SetTitle( '{0} ( {2} <= {1} < {3} )'.format(
                histvartitle,
                self.slicevarname,
                self.bounds[i_bin], self.bounds[i_bin+1]
                ))
            H.SetTitleSize(0.06);

            H.GetXaxis().SetTitle( histvartitle )
            #H.GetXaxis().SetRangeUser( 0.7, 1.2 );
            #H.GetXaxis().SetRangeUser( 0.7, 1.4 );
            H.GetXaxis().SetRangeUser( 0.6, 1.6 );

            H.GetXaxis().SetLabelSize(0.05);
            H.GetXaxis().SetTitleSize(0.06);
            H.GetYaxis().SetLabelSize(0.05);
            H.GetYaxis().SetTitleSize(0.06);


            if drawFit:
#                H_CB = self.Fit[histvarname]['Gaushist'][i_bin]
#                H_CB.Scale( H.Integral() / H_CB.Integral() * H_CB.GetNbinsX() / H.GetNbinsX() )
#                H_CB.SetLineColor(2)
#                H_CB.Draw('HISTSAMEL')

                H_CB = self.Fit[histvarname]['Gausfit'][i_bin]
                #H_CB.Scale( H.Integral() / H_CB.Integral() * H_CB.GetNbinsX() / H.GetNbinsX() )
                H_CB.SetLineColor(2)
                H_CB.Draw('SAME')

                # ======================================
                # Labels

                lx = 0.24
                ly = 0.88
                nl = 0.07
                nc = 0.1

                l = ROOT.TLatex()
                l.SetTextAlign(13)
                l.SetNDC()
                l.SetTextSize(0.05)

                l.DrawLatex( lx, ly, 'Gaus parameters' )
                ly -= nl+0.02

                parvalues = self.Fit[histvarname]['Gausvals'][i_bin]
                partitles = [ '#mu', '#sigma' ]

                for parvalue, partitle in zip( parvalues, partitles ):
                    l.DrawLatex( lx,     ly, partitle )
                    l.DrawLatex( lx+nc, ly, '{0:.4f}'.format(parvalue) )
                    ly -= nl
                ly -= 0.015
                l.DrawLatex( lx,    ly, '#sigma_{eff}' )
                l.DrawLatex( lx+nc, ly, '{0:.4f}'.format( self.Fit[histvarname]['effsigma'][i_bin] ) )


        self.Save( c, 'PerBinFit' + histvarname.capitalize() )


    # ======================================
    # Plot of variable over slices

    c.Clear()

    c.SetLeftMargin(   self.sliceplot_LeftMargin )
    c.SetRightMargin(  self.sliceplot_RightMargin )
    c.SetBottomMargin( self.sliceplot_BottomMargin )
    c.SetTopMargin(    self.sliceplot_TopMargin )

    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()


    base = ROOT.TH1F()
    base.Draw()


    print "histvar name is ", histvarname
    #######3rd pt bin
    if self.name == 'EBFULL_GENPT_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3
    
    if self.name == 'EEFULL_GENPT_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3
    
    if self.name == 'EBFULL_GENETA_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3
    
    if self.name == 'EEFULL_GENETA_0001_0005':
        self.sliceplot_y_min = 0.9
        self.sliceplot_y_max = 1.1
        self.sliceplotsigma_y_max = 0.3

    
    base.GetXaxis().SetLimits( self.bounds[0], self.bounds[-1] )
    base.SetMinimum(self.sliceplot_y_min)
    base.SetMaximum(self.sliceplot_y_max)




    if self.slicevarname in xAxisLabelDict:
        base.GetXaxis().SetTitle( xAxisLabelDict[self.slicevarname] )
    elif hasattr( self, 'slicevartitle' ):
        base.GetXaxis().SetTitle( self.slicevartitle )
    else:
        # This here so it's still possible to plot old fits
        base.GetXaxis().SetTitle( self.slicevarname )


    base.GetXaxis().SetNdivisions(505)
    base.GetYaxis().SetTitleOffset(1.1)
    base.GetXaxis().SetLabelSize(0.05)
    base.GetXaxis().SetTitleSize(0.06)
    base.GetYaxis().SetLabelSize(0.05)
    base.GetYaxis().SetTitleSize(0.06)


    # First the means

    base.GetYaxis().SetTitle( '#mu' )

    leg_mu = ROOT.TLegend(
        self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin,
        1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    leg_mu.SetNColumns(3)
    leg_mu.SetFillStyle(0)

    Hmus = []
    Hmus_filled = []
    for i_histvar, histvar in enumerate(self.histvars):

        Hmu = ROOT.TH1F( 'mu_'+histvar.GetName(), '', self.n_bins, array('d',self.bounds) )

        for i_bin in xrange(self.n_bins):
            bin_width  = self.bounds[i_bin+1] - self.bounds[i_bin]
            bin_center = self.bounds[i_bin] + 0.5*bin_width
            Hmu.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['Gausvals'][i_bin][0] )
            Hmu.SetBinError(   i_bin+1, self.Fit[histvar.GetName()]['Gauserrs'][i_bin][0] )

        # This is the line with line error bars
        Hmu.SetMarkerSize(0)
        Hmu.SetLineColor( self.colorlist[i_histvar] )
        Hmu.SetLineWidth(2)

        # This draws filled squares around the error bars (should be drawn before the line object)
        Hmu_filled = Hmu.Clone()
        Hmu_filled.SetName( Hmu_filled.GetName() + '_clone' )
        Hmu_filled.SetFillColorAlpha( self.colorlist[i_histvar], 0.3 )
        Hmu_filled.SetMarkerSize(0)

        Hmu_filled.Draw('SAMEE2')
        Hmu.Draw('HISTSAMEE')

        # Append for persistence
        Hmus.append( Hmu )
        Hmus_filled.append( Hmu_filled )

        leg_mu.AddEntry( 'mu_' + histvar.GetName(), '#mu_{Gaus, ' + histvar.GetTitle() + '}  ', 'lf' )

    leg_mu.Draw('SAME')
    self.Save( c, 'MuOverBins' )


    # Then the sigmas

    c.Clear()
    base.SetMinimum( self.sliceplotsigma_y_min )
    base.SetMaximum( self.sliceplotsigma_y_max )
    base.Draw()

#    base.GetYaxis().SetTitle( '#sigma_{eff}' )
    base.GetYaxis().SetTitle( '#sigma_{eff}/#mu' )

    leg_sigma = ROOT.TLegend(
        self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin,
        1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    leg_sigma.SetNColumns(3)
    leg_sigma.SetFillStyle(0)

    Hsigmas = []
    Hsigmas_filled = []
    for i_histvar, histvar in enumerate(self.histvars):

        Hsigma = ROOT.TH1F( 'sigma_'+histvar.GetName(), '', self.n_bins, array('d',self.bounds) )

        for i_bin in xrange(self.n_bins):
            bin_width  = self.bounds[i_bin+1] - self.bounds[i_bin]
            bin_center = self.bounds[i_bin] + 0.5*bin_width
            Hsigma.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['effsigma'][i_bin]/self.Fit[histvar.GetName()]['Gausvals'][i_bin][0] )
            #Hsigma.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['effsigma'][i_bin] )
            #Hsigma.SetBinError(   i_bin+1, self.Fit[histvar.GetName()]['Gauserrs'][i_bin][1] )
            Hsigma.SetBinError(   i_bin+1, 0 )

        # This is the line with line error bars
        Hsigma.SetMarkerSize(0)
        Hsigma.SetLineColor( self.colorlist[i_histvar] )
        Hsigma.SetLineWidth(2)

        # This draws filled squares around the error bars (should be drawn before the line object)
        Hsigma_filled = Hsigma.Clone()
        Hsigma_filled.SetName( Hsigma_filled.GetName() + '_clone' )
        #Hsigma_filled.SetFillColorAlpha( self.colorlist[i_histvar], 0.3 ) ###SJ
        Hsigma_filled.SetMarkerSize(0)

        #Hsigma_filled.Draw('SAMEE2') ##SJ
        Hsigma.Draw('HISTSAMEE')

        # Append for persistence
        Hsigmas.append( Hsigma )
        Hsigmas_filled.append( Hsigma_filled )

        leg_sigma.AddEntry( 'sigma_' + histvar.GetName(), '#sigma_{Gaus, ' + histvar.GetTitle() + '}', 'lf' )


    # leg_sigma.SetBorderSize(0)
    # square = ROOT.TBox( self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin - 0.25,
    #     1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    # # square.SetFillStyle(1)
    # # square.SetLineColor(1)
    # # square.SetLineStyle(1)
    # # square.SetLineWidth(1)
    # square.Draw('SAME')

    leg_sigma.Draw('SAME')
    self.Save( c, 'EffSigmaOverBins' )





#############################################Max#########
def MakePlots_standard_Max( self ):

    ########################################
    # Plotting
    ########################################

    self.p( 'Making plots the standard way for MAX FIT', 1 )


    # ======================================
    # Per bin fits

    # Find a clever number of divisions for the canvas
    int_sqrt_bins = int(sqrt(self.n_bins))
    dec_sqrt_bins = sqrt(self.n_bins) - int_sqrt_bins

    if dec_sqrt_bins < 0.0000001:
        n_columns = int_sqrt_bins
        n_rows    = int_sqrt_bins
    elif dec_sqrt_bins < 0.5:
        n_columns = int_sqrt_bins + 1
        n_rows    = int_sqrt_bins
    else:
        n_columns = int_sqrt_bins + 1
        n_rows    = int_sqrt_bins + 1

    c.Divide( n_columns, n_rows )


    # Should really be True except in exceptional plots
    drawFit = True
    if hasattr( self, 'disableDrawFits' ) and self.disableDrawFits: drawFit = False


    for histvar in self.histvars:

        histvarname = histvar.GetName()

        for i_bin in xrange(self.n_bins):

            c.cd(i_bin+1)
            ROOT.gPad.SetLeftMargin(0.20)
            ROOT.gPad.SetBottomMargin(0.14)
            ROOT.gPad.SetRightMargin(0.01)
            ROOT.gPad.SetTopMargin(0.1)

            #H = self.Fit[histvarname]['fitdata'][i_bin]
            H = self.Fit[histvarname]['Maxhist'][i_bin]

            if not drawFit:
                H = H.Rebin(10)

            H.Draw()

            histvartitle = 'E_{{{0}}}/E_{{true}}'.format( histvar.GetTitle() )
            # Default is to assume it's an energy ratio, if not change the plotting label a bit
            if hasattr( self, 'notAnEnergyRatio' ) and self.notAnEnergyRatio:
                histvartitle = histvar.GetTitle()

            H.SetTitle( '{0} ( {2} <= {1} < {3} )'.format(
                histvartitle,
                self.slicevarname,
                self.bounds[i_bin], self.bounds[i_bin+1]
                ))
            H.SetTitleSize(0.06);

            H.GetXaxis().SetTitle( histvartitle )
            #H.GetXaxis().SetRangeUser( 0.7, 1.2 );
            #H.GetXaxis().SetRangeUser( 0.7, 1.4 );
            H.GetXaxis().SetRangeUser( 0.6, 1.6 );

            H.GetXaxis().SetLabelSize(0.05);
            H.GetXaxis().SetTitleSize(0.06);
            H.GetYaxis().SetLabelSize(0.05);
            H.GetYaxis().SetTitleSize(0.06);


            if drawFit:

                lx = 0.24
                ly = 0.88
                nl = 0.07
                nc = 0.1

                l = ROOT.TLatex()
                l.SetTextAlign(13)
                l.SetNDC()
                l.SetTextSize(0.05)

                l.DrawLatex( lx, ly, 'Max parameters' )
                ly -= nl+0.02

                parvalues = self.Fit[histvarname]['Maxvals'][i_bin]
                partitles = [ '#mu', '#sigma' ]

                for parvalue, partitle in zip( parvalues, partitles ):
                    l.DrawLatex( lx,     ly, partitle )
                    l.DrawLatex( lx+nc, ly, '{0:.4f}'.format(parvalue) )
                    ly -= nl
                ly -= 0.015
                l.DrawLatex( lx,    ly, '#sigma_{eff}' )
                l.DrawLatex( lx+nc, ly, '{0:.4f}'.format( self.Fit[histvarname]['effsigma'][i_bin] ) )


        self.Save( c, 'PerBinFit' + histvarname.capitalize() )


    # ======================================
    # Plot of variable over slices

    c.Clear()

    c.SetLeftMargin(   self.sliceplot_LeftMargin )
    c.SetRightMargin(  self.sliceplot_RightMargin )
    c.SetBottomMargin( self.sliceplot_BottomMargin )
    c.SetTopMargin(    self.sliceplot_TopMargin )

    ROOT.gPad.SetGridx()
    ROOT.gPad.SetGridy()


    base = ROOT.TH1F()
    base.Draw()

    base.GetXaxis().SetLimits( self.bounds[0], self.bounds[-1] )
    base.SetMinimum(self.sliceplot_y_min)
    base.SetMaximum(self.sliceplot_y_max)




    if self.slicevarname in xAxisLabelDict:
        base.GetXaxis().SetTitle( xAxisLabelDict[self.slicevarname] )
    elif hasattr( self, 'slicevartitle' ):
        base.GetXaxis().SetTitle( self.slicevartitle )
    else:
        # This here so it's still possible to plot old fits
        base.GetXaxis().SetTitle( self.slicevarname )


    base.GetXaxis().SetNdivisions(505)
    base.GetYaxis().SetTitleOffset(1.1)
    base.GetXaxis().SetLabelSize(0.05)
    base.GetXaxis().SetTitleSize(0.06)
    base.GetYaxis().SetLabelSize(0.05)
    base.GetYaxis().SetTitleSize(0.06)


    # First the means

    base.GetYaxis().SetTitle( '#mu' )

    leg_mu = ROOT.TLegend(
        self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin,
        1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    leg_mu.SetNColumns(3)
    leg_mu.SetFillStyle(0)

    Hmus = []
    Hmus_filled = []
    for i_histvar, histvar in enumerate(self.histvars):

        Hmu = ROOT.TH1F( 'mu_'+histvar.GetName(), '', self.n_bins, array('d',self.bounds) )

        for i_bin in xrange(self.n_bins):
            bin_width  = self.bounds[i_bin+1] - self.bounds[i_bin]
            bin_center = self.bounds[i_bin] + 0.5*bin_width
            Hmu.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['Maxvals'][i_bin][0] )
            Hmu.SetBinError(   i_bin+1, self.Fit[histvar.GetName()]['Maxerrs'][i_bin][0] )

        # This is the line with line error bars
        Hmu.SetMarkerSize(0)
        Hmu.SetLineColor( self.colorlist[i_histvar] )
        Hmu.SetLineWidth(2)

        # This draws filled squares around the error bars (should be drawn before the line object)
        Hmu_filled = Hmu.Clone()
        Hmu_filled.SetName( Hmu_filled.GetName() + '_clone' )
        Hmu_filled.SetFillColorAlpha( self.colorlist[i_histvar], 0.3 )
        Hmu_filled.SetMarkerSize(0)

        Hmu_filled.Draw('SAMEE2')
        Hmu.Draw('HISTSAMEE')

        # Append for persistence
        Hmus.append( Hmu )
        Hmus_filled.append( Hmu_filled )

        leg_mu.AddEntry( 'mu_' + histvar.GetName(), '#mu_{Max, ' + histvar.GetTitle() + '}  ', 'lf' )

    leg_mu.Draw('SAME')
    self.Save( c, 'MuOverBins' )


    # Then the sigmas

    c.Clear()
    base.SetMinimum( self.sliceplotsigma_y_min )
    base.SetMaximum( self.sliceplotsigma_y_max )
    base.Draw()

    base.GetYaxis().SetTitle( '#sigma_{eff}' )

    leg_sigma = ROOT.TLegend(
        self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin,
        1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    leg_sigma.SetNColumns(3)
    leg_sigma.SetFillStyle(0)

    Hsigmas = []
    Hsigmas_filled = []
    for i_histvar, histvar in enumerate(self.histvars):

        Hsigma = ROOT.TH1F( 'sigma_'+histvar.GetName(), '', self.n_bins, array('d',self.bounds) )

        for i_bin in xrange(self.n_bins):
            bin_width  = self.bounds[i_bin+1] - self.bounds[i_bin]
            bin_center = self.bounds[i_bin] + 0.5*bin_width
            Hsigma.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['effsigma'][i_bin]/self.Fit[histvar.GetName()]['Maxvals'][i_bin][0] )
            #Hsigma.SetBinContent( i_bin+1, self.Fit[histvar.GetName()]['effsigma'][i_bin])
            #Hsigma.SetBinError(   i_bin+1, self.Fit[histvar.GetName()]['Maxerrs'][i_bin][1] )
            Hsigma.SetBinError(   i_bin+1, 0 )

        # This is the line with line error bars
        Hsigma.SetMarkerSize(0)
        Hsigma.SetLineColor( self.colorlist[i_histvar] )
        Hsigma.SetLineWidth(2)

        # This draws filled squares around the error bars (should be drawn before the line object)
        Hsigma_filled = Hsigma.Clone()
        Hsigma_filled.SetName( Hsigma_filled.GetName() + '_clone' )
        #Hsigma_filled.SetFillColorAlpha( self.colorlist[i_histvar], 0.3 ) ###SJ
        Hsigma_filled.SetMarkerSize(0)

        #Hsigma_filled.Draw('SAMEE2') ##SJ
        Hsigma.Draw('HISTSAMEE')

        # Append for persistence
        Hsigmas.append( Hsigma )
        Hsigmas_filled.append( Hsigma_filled )

        leg_sigma.AddEntry( 'sigma_' + histvar.GetName(), '#sigma_{Max, ' + histvar.GetTitle() + '}', 'lf' )


    # leg_sigma.SetBorderSize(0)
    # square = ROOT.TBox( self.sliceplot_LeftMargin,      1.0-self.sliceplot_TopMargin - 0.25,
    #     1.0-self.sliceplot_RightMargin, 1.0-self.sliceplot_TopMargin+self.sliceplot_legheight  )
    # # square.SetFillStyle(1)
    # # square.SetLineColor(1)
    # # square.SetLineStyle(1)
    # # square.SetLineWidth(1)
    # square.Draw('SAME')

    leg_sigma.Draw('SAME')
    self.Save( c, 'EffSigmaOverBins' )
    

