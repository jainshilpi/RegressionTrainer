import ROOT
import sys

#inputFile = ROOT.TFile.Open('pfClustersTree_FULL_%s_PT3.root' % sys.argv[1])
#inputFile = ROOT.TFile.Open('eos/cms/store/group/phys_egamma/PFClusteRegressionTrees/afterDebug_16june/pfClustersTree_FULL_%s_PT3.root' % sys.argv[1])

#inputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/pfClustersTree_FULL_%s_PT3.root' % sys.argv[1])
#inputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/FlatTrees/v1/pfClustersTree_FULL_%s_PT3.root' % sys.argv[1])
inputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/PU_allEta/pfClustersTree_FULL_%s_PT3.root' % sys.argv[1])
#inputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/pfClustersTree_FULL_%s_PT3.root' % sys.argv[1])
inputTree = inputFile.Get('een_analyzer/PfTree')

#outputFile = ROOT.TFile.Open('pfClustersTree_FULL_%s_PT3_skim.root' % sys.argv[1], 'RECREATE')
#outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/pfClustersTree_FULL_%s_PT3_skim.root' % sys.argv[1], 'RECREATE')
#outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/FlatTrees/v1/pfClustersTree_FULL_%s_PT3_skim.root' % sys.argv[1], 'RECREATE')
#outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/pfClustersTree_FULL_%s_PT3_skim.root' % sys.argv[1], 'RECREATE')
outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/PU_allEta/pfClustersTree_FULL_%s_PT3_skim.root' % sys.argv[1], 'RECREATE')
#outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/pfClustersTree_FULL_%s_PT3_skim.root' % sys.argv[1], 'RECREATE')
outputFile.mkdir('een_analyzer')
outputFile.cd('een_analyzer')

target = 1500000.
#target = 2200000.
nentries = float(inputTree.GetEntries())

outputTree = inputTree.CopyTree('rndm < %f' % (target/nentries))
outputTree.Write('PfTree')
outputFile.Close()

inputFile.Close()
