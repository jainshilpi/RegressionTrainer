import ROOT, math, numpy
import sys

def separate(initial,target,filename,inputTree, outfilename):

	print "opening file pfClusters_%s.root" %(filename)

	#outputFile = ROOT.TFile.Open('pfClusters_%s_%s.root' %(filename,outfilename), 'RECREATE')
#	outputFile = ROOT.TFile.Open('eos/cms/store/group/phys_egamma/PFClusteRegressionTrees/pfClusters_%s_%s.root' %(filename,outfilename), 'RECREATE')
#	outputFile = ROOT.TFile.Open('eos/cms/store/group/phys_egamma/PFClusteRegressionTrees/afterDebug_16june/pfClusters_%s_%s.root' %(filename,outfilename), 'RECREATE')
#	outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/MC18_V2/FlatTrees/pfClusters_%s_%s.root' %(filename,outfilename), 'RECREATE')
#	outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/pfClusters_%s_%s.root' %(filename,outfilename), 'RECREATE')
	outputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/FlatTrees/v1/pfClusters_%s_%s.root' %(filename,outfilename), 'RECREATE')
	outputFile.mkdir('een_analyzer')
	outputFile.cd('een_analyzer')
	


	nentries = int(inputTree.GetEntries())
	print "Total entries in original tree ",nentries
	print "For training tree, copying ",target-initial, " entries"
	
#outputTree = inputTree.CopyTree('','',target,0)
#outputTree.Write('PfTree')
#outputFile.Close()


	outputTree = inputTree.CloneTree(0)
#	print "Now writing the branch weight in the output file"
	weight = numpy.zeros(1, dtype=float)
	nhits_mod = numpy.zeros(1, dtype=int)
	

	outputTree.Branch('weight',weight,'weight/D')
	outputTree.Branch('nhits_mod',nhits_mod,'nhits_mod/I')

#	print "Entries in output tree ", outputTree.GetEntries()

###0 till target-1
	for ev in range(initial,target):
		if (inputTree.GetEntry(ev) <= 0):
			raise Exception('TTree::GetEntry() failed')
        
		weight[0] = (1.0/(target-initial))
		nhits_mod[0] = inputTree.clusSize
		if(inputTree.clusSize >= 3):
			nhits_mod[0] = 3

		#print("nhits %d : nhits_mod %d" %(inputTree.clusSize,nhits_mod[0]))	
	#	print "weight is ",weight[0]
		outputTree.Fill()

	print "Looped over the output treee"

	outputFile.cd('een_analyzer')
	outputTree.Write('PfTree')

###################################################################3
####training tree
#inputFile = ROOT.TFile.Open('root://eoscms.cern.ch//eos/cms/store/group/phys_egamma/PFClusteRegressionTrees/pfClusters_%s.root' % sys.argv[1])
#inputFile = ROOT.TFile.Open('root://eoscms.cern.ch//eos/cms/store/group/phys_egamma/PFClusteRegressionTrees/afterDebug_16june/pfClusters_%s.root' % sys.argv[1])

#print "input file is /eos/cms/store/group/phys_egamma/PFClusterCalibration/MC18_V2/FlatTrees/pfClusters_%s.root", sys.argv[1]
#inputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/MC18_V2/FlatTrees/pfClusters_%s.root' % sys.argv[1])


#print "input file is /eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/FlatTrees/pfClusters_%s.root", sys.argv[1]
#inputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/FlatTrees/pfClusters_%s.root' % sys.argv[1])


print "input file is /eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/FlatTrees/v1/pfClusters_%s.root", sys.argv[1]
inputFile = ROOT.TFile.Open('/eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/FlatTrees/v1/pfClusters_%s.root' % sys.argv[1])

inputTree = inputFile.Get('een_analyzer/PfTree')
nentries = int(inputTree.GetEntries())

####training tree
initial = 0
target = int(3.*nentries/4.)
filename = sys.argv[1]
outfilename = "training"
separate(initial,target,filename,inputTree,outfilename)

####training tree
initial = int(3.*nentries/4.)
target  = nentries 
filename = sys.argv[1]
outfilename = "testing"
separate(initial,target,filename,inputTree,outfilename)



