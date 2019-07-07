#include "CondFormats/EgammaObjects/interface/GBRForest.h"
#include "CondFormats/EgammaObjects/interface/GBRForestD.h"
#include "TFile.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include "ParReader.h"

// Needed for randomly assigned weight
#include "TRandom.h"
#include "TF1.h"
#include "TMath.h"

#include <boost/program_options.hpp>
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/filesystem.hpp>

#include <iterator>
#include <typeinfo>
#include <cstring>
#include <iostream>
#include <cstdlib>
#include <array>

using namespace std;
using namespace boost;
using namespace boost::program_options;
using namespace boost::filesystem;

#define debug false
//#define debug true

bool replace(std::string& str, const std::string& from, const std::string& to) {
  size_t start_pos = str.find(from);
  if(start_pos == std::string::npos)
    return false;
  str.replace(start_pos, from.length(), to);
  return true;
}

int main(int argc, char** argv) {

  string configPrefix;
  string trainingPrefix;
  string testingFileName;
  string outputFileName;
  string supressVariable;
  

  options_description desc("Allowed options");
  desc.add_options()
    ("help,h", "print usage message")
    ("config,c", value<string>(&configPrefix), "Configuration prefix")
    ("prefix,p", value<string>(&trainingPrefix), "Training prefix")
    ("testing,t", value<string>(&testingFileName), "Testing tree")
    ("output,o", value<string>(&outputFileName), "Output friend tree")
    ;

  variables_map vm;
  store(parse_command_line(argc, argv, desc), vm);
  notify(vm);
  
  if (vm.count("help")) {
    cout << desc << "\n";
    return 1;
  }

  if (!vm.count("config")) {
    configPrefix = trainingPrefix;
    replace(configPrefix, "../", "../python/");
  }

  double responseMin = -0.336 ;
  double responseMax = 0.916 ;
  double resolutionMin = 0.001 ;
  double resolutionMax = 0.4 ;

  cout << "Response parameters "  << responseMin << " " << responseMax << endl;

  double responseScale = 0.5*( responseMax - responseMin );
  double responseOffset = responseMin + 0.5*( responseMax - responseMin );

  double resolutionScale = 0.5*( resolutionMax - resolutionMin );
  double resolutionOffset = resolutionMin + 0.5*( resolutionMax - resolutionMin );

  GBRForestD* forest_EB_full_pt1_scale;
  GBRForestD* forest_EB_full_pt1_resolution;
  GBRForestD* forest_EB_full_pt2_scale;
  GBRForestD* forest_EB_full_pt2_resolution;
  GBRForestD* forest_EB_full_pt3_scale;
  GBRForestD* forest_EB_full_pt3_resolution;

  GBRForestD* forest_EE_full_pt1_scale;
  GBRForestD* forest_EE_full_pt1_resolution;
  GBRForestD* forest_EE_full_pt2_scale;
  GBRForestD* forest_EE_full_pt2_resolution;
  GBRForestD* forest_EE_full_pt3_scale;
  GBRForestD* forest_EE_full_pt3_resolution;

  GBRForestD* forest_EB_zs1_scale;
  GBRForestD* forest_EB_zs1_resolution;

  GBRForestD* forest_EB_zs2_scale;
  GBRForestD* forest_EB_zs2_resolution;

  GBRForestD* forest_EB_zs3_scale;
  GBRForestD* forest_EB_zs3_resolution;

  GBRForestD* forest_EE_zs1_scale;
  GBRForestD* forest_EE_zs1_resolution;

  GBRForestD* forest_EE_zs2_scale;
  GBRForestD* forest_EE_zs2_resolution;

  GBRForestD* forest_EE_zs3_scale;
  GBRForestD* forest_EE_zs3_resolution;

  std::vector<TFile*> file_;

  file_.push_back(TFile::Open(TString::Format("%s_EB_full_pt1_results.root", trainingPrefix.c_str())));
  forest_EB_full_pt1_scale = (GBRForestD*) file_.back()->Get("EBCorrection");
  forest_EB_full_pt1_resolution = (GBRForestD*) file_.back()->Get("EBUncertainty");
  file_.push_back(TFile::Open(TString::Format("%s_EB_full_pt2_results.root", trainingPrefix.c_str())));
  forest_EB_full_pt2_scale = (GBRForestD*) file_.back()->Get("EBCorrection");
  forest_EB_full_pt2_resolution = (GBRForestD*) file_.back()->Get("EBUncertainty");
  file_.push_back(TFile::Open(TString::Format("%s_EB_full_pt3_results.root", trainingPrefix.c_str())));
  forest_EB_full_pt3_scale = (GBRForestD*) file_.back()->Get("EBCorrection");
  forest_EB_full_pt3_resolution = (GBRForestD*) file_.back()->Get("EBUncertainty");

  file_.push_back(TFile::Open(TString::Format("%s_EE_full_pt1_results.root", trainingPrefix.c_str())));
  forest_EE_full_pt1_scale = (GBRForestD*) file_.back()->Get("EECorrection");
  forest_EE_full_pt1_resolution = (GBRForestD*) file_.back()->Get("EEUncertainty");
  file_.push_back(TFile::Open(TString::Format("%s_EE_full_pt2_results.root", trainingPrefix.c_str())));
  forest_EE_full_pt2_scale = (GBRForestD*) file_.back()->Get("EECorrection");
  forest_EE_full_pt2_resolution = (GBRForestD*) file_.back()->Get("EEUncertainty");
  file_.push_back(TFile::Open(TString::Format("%s_EE_full_pt3_results.root", trainingPrefix.c_str())));
  forest_EE_full_pt3_scale = (GBRForestD*) file_.back()->Get("EECorrection");
  forest_EE_full_pt3_resolution = (GBRForestD*) file_.back()->Get("EEUncertainty");

  file_.push_back(TFile::Open(TString::Format("%s_EB_zs1_results.root", trainingPrefix.c_str())));
  forest_EB_zs1_scale = (GBRForestD*) file_.back()->Get("EBCorrection");
  forest_EB_zs1_resolution = (GBRForestD*) file_.back()->Get("EBUncertainty");

  /*file_.push_back(TFile::Open(TString::Format("%s_EB_zs2_results.root", trainingPrefix.c_str())));
  forest_EB_zs2_scale = (GBRForestD*) file_.back()->Get("EBCorrection");
  forest_EB_zs2_resolution = (GBRForestD*) file_.back()->Get("EBUncertainty");

  file_.push_back(TFile::Open(TString::Format("%s_EB_zs3_results.root", trainingPrefix.c_str())));
  forest_EB_zs3_scale = (GBRForestD*) file_.back()->Get("EBCorrection");
  forest_EB_zs3_resolution = (GBRForestD*) file_.back()->Get("EBUncertainty");
  */
  file_.push_back(TFile::Open(TString::Format("%s_EE_zs1_results.root", trainingPrefix.c_str())));
  forest_EE_zs1_scale = (GBRForestD*) file_.back()->Get("EECorrection");
  forest_EE_zs1_resolution = (GBRForestD*) file_.back()->Get("EEUncertainty");
  /*
  file_.push_back(TFile::Open(TString::Format("%s_EE_zs2_results.root", trainingPrefix.c_str())));
  forest_EE_zs2_scale = (GBRForestD*) file_.back()->Get("EECorrection");
  forest_EE_zs2_resolution = (GBRForestD*) file_.back()->Get("EEUncertainty");

  file_.push_back(TFile::Open(TString::Format("%s_EE_zs3_results.root", trainingPrefix.c_str())));
  forest_EE_zs3_scale = (GBRForestD*) file_.back()->Get("EECorrection");
  forest_EE_zs3_resolution = (GBRForestD*) file_.back()->Get("EEUncertainty");
  */
  ParReader reader_EB_full_pt1; reader_EB_full_pt1.read(TString::Format("%s_EB_full_pt1.config", configPrefix.c_str()).Data());
  ParReader reader_EB_full_pt2; reader_EB_full_pt2.read(TString::Format("%s_EB_full_pt2.config", configPrefix.c_str()).Data());
  ParReader reader_EB_full_pt3; reader_EB_full_pt3.read(TString::Format("%s_EB_full_pt3.config", configPrefix.c_str()).Data());

  ParReader reader_EE_full_pt1; reader_EE_full_pt1.read(TString::Format("%s_EE_full_pt1.config", configPrefix.c_str()).Data());
  ParReader reader_EE_full_pt2; reader_EE_full_pt2.read(TString::Format("%s_EE_full_pt2.config", configPrefix.c_str()).Data());
  ParReader reader_EE_full_pt3; reader_EE_full_pt3.read(TString::Format("%s_EE_full_pt3.config", configPrefix.c_str()).Data());

  ParReader reader_EB_zs1; reader_EB_zs1.read(TString::Format("%s_EB_zs1.config", configPrefix.c_str()).Data());
  /*ParReader reader_EB_zs2; reader_EB_zs2.read(TString::Format("%s_EB_zs2.config", configPrefix.c_str()).Data());
  ParReader reader_EB_zs3; reader_EB_zs3.read(TString::Format("%s_EB_zs3.config", configPrefix.c_str()).Data());
  */
  ParReader reader_EE_zs1; reader_EE_zs1.read(TString::Format("%s_EE_zs1.config", configPrefix.c_str()).Data());
  /*ParReader reader_EE_zs2; reader_EE_zs2.read(TString::Format("%s_EE_zs2.config", configPrefix.c_str()).Data());
  ParReader reader_EE_zs3; reader_EE_zs3.read(TString::Format("%s_EE_zs3.config", configPrefix.c_str()).Data());
  */
  TFile* testingFile = TFile::Open(testingFileName.c_str());
  TTree* testingTree = (TTree*) testingFile->Get("een_analyzer/PfTree");

  //std::cout<<"Opened the testing file"<<std::endl;

  TTreeFormula clusrawE("clusrawE", "clusrawE", testingTree);
  TTreeFormula cluscorrE("cluscorrE", "cluscorrE", testingTree);
  TTreeFormula genEnergy("genEnergy", "genEnergy", testingTree);
  TTreeFormula clusEta("clusEta", "clusEta", testingTree);
  TTreeFormula clusPhi("clusPhi", "clusPhi", testingTree);

  TTreeFormula clusIetaIx("clusIetaIx", "clusIetaIx", testingTree);
  TTreeFormula clusIphiIy("clusIphiIy", "clusIphiIy", testingTree);

  TTreeFormula clusPS1("clusPS1", "clusPS1", testingTree);
  TTreeFormula clusPS2("clusPS2", "clusPS2", testingTree);
  TTreeFormula clusFlag("clusFlag", "clusFlag", testingTree);
  TTreeFormula clusLayer("clusLayer", "clusLayer", testingTree);
  TTreeFormula clusSize("clusSize", "clusSize", testingTree);
  TTreeFormula ietamod20("ietamod20", "ietamod20", testingTree);
  TTreeFormula iphimod20("iphimod20", "iphimod20", testingTree);

  //TTreeFormula weight("weight", "weight", testingTree);
  TTreeFormula nvtx("nvtx", "nvtx", testingTree);
  TTreeFormula nhits("nhits", "nhits", testingTree);
  //TTreeFormula nhits("nhits_mod", "nhits_mod", testingTree);

  char_separator<char> sep(":");

  //std::cout<<"Defined all the ttree formula"<<std::endl;

  std::vector<TTreeFormula*> inputforms_EB_full_pt1;
  { tokenizer<char_separator<char>> tokens(reader_EB_full_pt1.m_regParams[0].variablesEB, sep); for (const auto& it : tokens) inputforms_EB_full_pt1.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }
  std::vector<TTreeFormula*> inputforms_EB_full_pt2;
  { tokenizer<char_separator<char>> tokens(reader_EB_full_pt2.m_regParams[0].variablesEB, sep); for (const auto& it : tokens) inputforms_EB_full_pt2.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }
  std::vector<TTreeFormula*> inputforms_EB_full_pt3;
  { tokenizer<char_separator<char>> tokens(reader_EB_full_pt3.m_regParams[0].variablesEB, sep); for (const auto& it : tokens) inputforms_EB_full_pt3.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }

  std::vector<TTreeFormula*> inputforms_EE_full_pt1;
  { tokenizer<char_separator<char>> tokens(reader_EE_full_pt1.m_regParams[0].variablesEE, sep); for (const auto& it : tokens) {
      inputforms_EE_full_pt1.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); 
      std::cout<<"name in EE full_pt1 : "<<it.c_str()<<std::endl;
    }
  }

  std::vector<TTreeFormula*> inputforms_EE_full_pt2;
  { tokenizer<char_separator<char>> tokens(reader_EE_full_pt2.m_regParams[0].variablesEE, sep); for (const auto& it : tokens) {
      inputforms_EE_full_pt2.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); 
      std::cout<<"name in EE full_pt2 : "<<it.c_str()<<std::endl;
    }
  }
  
  
  std::vector<TTreeFormula*> inputforms_EE_full_pt3;
  { tokenizer<char_separator<char>> tokens(reader_EE_full_pt3.m_regParams[0].variablesEE, sep); for (const auto& it : tokens){
      inputforms_EE_full_pt3.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); 
      std::cout<<"name in EE full_pt3 : "<<it.c_str()<<std::endl;
    }
  }

  std::vector<TTreeFormula*> inputforms_EB_zs1;
  { tokenizer<char_separator<char>> tokens(reader_EB_zs1.m_regParams[0].variablesEB, sep); for (const auto& it : tokens) inputforms_EB_zs1.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }
  /*
  std::vector<TTreeFormula*> inputforms_EB_zs2;
  { tokenizer<char_separator<char>> tokens(reader_EB_zs2.m_regParams[0].variablesEB, sep); for (const auto& it : tokens) inputforms_EB_zs2.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }

  std::vector<TTreeFormula*> inputforms_EB_zs3;
  { tokenizer<char_separator<char>> tokens(reader_EB_zs3.m_regParams[0].variablesEB, sep); for (const auto& it : tokens) inputforms_EB_zs3.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }
  */

  std::vector<TTreeFormula*> inputforms_EE_zs1;
  { tokenizer<char_separator<char>> tokens(reader_EE_zs1.m_regParams[0].variablesEE, sep); for (const auto& it : tokens) inputforms_EE_zs1.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }
  /*
  std::vector<TTreeFormula*> inputforms_EE_zs2;
  { tokenizer<char_separator<char>> tokens(reader_EE_zs2.m_regParams[0].variablesEE, sep); for (const auto& it : tokens) inputforms_EE_zs2.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }

  std::vector<TTreeFormula*> inputforms_EE_zs3;
  { tokenizer<char_separator<char>> tokens(reader_EE_zs3.m_regParams[0].variablesEE, sep); for (const auto& it : tokens) inputforms_EE_zs3.push_back(new TTreeFormula(it.c_str(),it.c_str(),testingTree)); }
  */

  std::vector<float> vals;
  Float_t response = 0.;
  Float_t resolution = 0.;
  
  //initialize new friend tree
  TFile* outputFile = TFile::Open(outputFileName.c_str(), "RECREATE");
  outputFile->mkdir("een_analyzer");
  outputFile->cd("een_analyzer");

  TTree *friendtree = new TTree("correction", "correction");

  ///not writing here - will user merge.py since one needs to call EvalInstance for every variable to be written in the tree. If not called, then it is 0.
  /*TTree *friendtree = new TTree("PfTree", "PfTree");
  friendtree = testingTree->CloneTree(0);
  */

  friendtree->Branch("response", &response, "response/F");
  friendtree->Branch("resolution", &resolution, "resolution/F");
  
  for (Long64_t iev=0; iev<testingTree->GetEntries(); ++iev) {

    response = 0.;
    resolution = 0.;
    if (iev%100000==0) printf("%i\n",int(iev));
    testingTree->LoadTree(iev);

    bool EB_ = (clusLayer.EvalInstance() == -1);
    bool EE_ = (clusLayer.EvalInstance() == -2);
    /*bool pt1_ = clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) <= 4.5;
    bool pt2_ = clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) <= 18. && clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) > 4.5;
    bool pt3_ = clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) > 18.;
    bool zs_ = clusFlag.EvalInstance() == 1;
    */
    bool pt1_ = clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) <= 2.5;
    bool pt2_ = clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) <= 6. && clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) > 2.5;
    bool pt3_ = clusrawE.EvalInstance()/TMath::CosH(clusEta.EvalInstance()) > 6.0;
    //bool zs1_ = clusSize.EvalInstance() == 1;
    /*bool zs2_ = clusSize.EvalInstance() == 2;
    bool zs3_ = clusSize.EvalInstance() >=3 &&  clusSize.EvalInstance()<=6;
    */
    bool zs1_ = clusFlag.EvalInstance() == 1;
    bool zs_ = zs1_;
    //bool zs_ = zs1_ || zs2_ || zs3_;
    

    vals.clear();

    if (EB_ && zs1_) { for (auto&& input : inputforms_EB_zs1) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EB_zs1_scale->GetResponse(vals.data()); resolution = forest_EB_zs1_resolution->GetResponse(vals.data()); }
    /*
    else if (EB_ && zs2_) { for (auto&& input : inputforms_EB_zs2) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EB_zs2_scale->GetResponse(vals.data()); resolution = forest_EB_zs2_resolution->GetResponse(vals.data()); }

    else if (EB_ && zs3_) { for (auto&& input : inputforms_EB_zs3) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EB_zs3_scale->GetResponse(vals.data()); resolution = forest_EB_zs3_resolution->GetResponse(vals.data()); }
    */

    else if (EE_ && zs1_) { for (auto&& input : inputforms_EE_zs1) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << "EE: zs1 : "<< input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EE_zs1_scale->GetResponse(vals.data()); resolution = forest_EE_zs1_resolution->GetResponse(vals.data()); }

    /*else if (EE_ && zs2_) { for (auto&& input : inputforms_EE_zs2) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EE_zs2_scale->GetResponse(vals.data()); resolution = forest_EE_zs2_resolution->GetResponse(vals.data()); }

    else if (EE_ && zs3_) { for (auto&& input : inputforms_EE_zs3) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EE_zs3_scale->GetResponse(vals.data()); resolution = forest_EE_zs3_resolution->GetResponse(vals.data()); }
    */
    
    else if (EB_ && !zs_ && pt1_) { for (auto&& input : inputforms_EB_full_pt1) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EB_full_pt1_scale->GetResponse(vals.data()); resolution = forest_EB_full_pt1_resolution->GetResponse(vals.data()); }
    else if (EB_ && !zs_ && pt2_) { for (auto&& input : inputforms_EB_full_pt2) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EB_full_pt2_scale->GetResponse(vals.data()); resolution = forest_EB_full_pt2_resolution->GetResponse(vals.data()); }
    else if (EB_ && !zs_ && pt3_) { for (auto&& input : inputforms_EB_full_pt3) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " " << input->EvalInstance() << endl; } 
      response = forest_EB_full_pt3_scale->GetResponse(vals.data()); resolution = forest_EB_full_pt3_resolution->GetResponse(vals.data()); }

    else if (EE_ && !zs_ && pt1_) { for (auto&& input : inputforms_EE_full_pt1) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " EE: pt1 : " << input->EvalInstance() << endl; } 
      response = forest_EE_full_pt1_scale->GetResponse(vals.data()); resolution = forest_EE_full_pt1_resolution->GetResponse(vals.data()); }
    else if (EE_ && !zs_ && pt2_) { for (auto&& input : inputforms_EE_full_pt2) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << " EE:pt2 : " << input->EvalInstance() << endl; } 
      response = forest_EE_full_pt2_scale->GetResponse(vals.data()); resolution = forest_EE_full_pt2_resolution->GetResponse(vals.data()); }
    else if (EE_ && !zs_ && pt3_) { for (auto&& input : inputforms_EE_full_pt3) { input->GetNdata(); vals.push_back(input->EvalInstance()); if(debug) cout << input->GetExpFormula().Data() << "EE:pt3:  " << input->EvalInstance() << endl; } 
      response = forest_EE_full_pt3_scale->GetResponse(vals.data()); resolution = forest_EE_full_pt3_resolution->GetResponse(vals.data()); }

    /*
    if(EE_) 
      {
	cout<<"clusrawE : ieta : iphi : ietamod20 : iphimod20 : (eps1+eps2)/raw : nhits"<<clusrawE.EvalInstance()<<" "<<clusIetaIx.EvalInstance()<<" "<<clusIphiIy.EvalInstance()<<" "<<ietamod20.EvalInstance()<<" "<<iphimod20.EvalInstance()<<" "<<(clusPS1.EvalInstance()+clusPS2.EvalInstance())/clusrawE.EvalInstance()<<" "<<nhits.EvalInstance()<<" "<<clusFlag.EvalInstance()<<endl;
	cout<<"bare response : sin : "<<response<<endl;
	
      }
    */

    if (TMath::Abs(response) > TMath::Pi()/2 ) response = 0.0;
    else response = responseOffset + responseScale*sin(response);
  
    if (TMath::Abs(resolution) > TMath::Pi()/2 ) resolution = 1.0;
    else resolution = resolutionOffset + resolutionScale*sin(resolution);

    
    


    response = TMath::Exp(response);
    resolution = TMath::Abs(response)*resolution;

    //cout<<"ieta20 eta ipho20 phi "<<ietamod20.EvalInstance()<<" "<<clusEta.EvalInstance()<<" "<<iphimod20.EvalInstance()<<" "<<clusPhi.EvalInstance()<<endl;

    //if (EB_ && zs1_) cout<<" 91X response : "<<response << endl;
    //if (EB_ && !zs_ && pt1_) cout<<" 91X response : "<<response << endl;
    //if (EB_ && !zs_ && pt2_) cout<<" 91X response : "<<response << endl;
    //if (EB_ && !zs_ && pt3_) cout<<" 91X response : "<<response << endl;

    //if (EE_ && zs1_) cout<<" 91X response : "<<response << endl;
    //if (EE_ && !zs_ && pt1_) cout<<" 91X response : "<<response << endl;
    //if (EE_ && !zs_ && pt2_) cout<<" 91X response : "<<response << endl;
    //if (EE_ && !zs_ && pt3_) cout<<" 91X response : "<<response << endl;
    //cout<<" 91X response : "<<response << endl;

    if (debug) cout << "91X response " << response << endl;
    if (EB_) {
      if (debug) cout << "GEN (91X) response " << genEnergy.EvalInstance()/clusrawE.EvalInstance() << endl;
    } else {
      if (debug) cout << "GEN (91X) response " << genEnergy.EvalInstance()/(clusrawE.EvalInstance()+clusPS1.EvalInstance()+clusPS2.EvalInstance()) << endl;
    }
    if (debug) cout << "74X response " << cluscorrE.EvalInstance()/clusrawE.EvalInstance() << endl;
    if (debug) cout << "GEN (74X) response " << genEnergy.EvalInstance()/clusrawE.EvalInstance() << endl;

    friendtree->Fill();
  }
    
  // Writes output
  outputFile->cd("een_analyzer");
  friendtree->Write();
  outputFile->Close();
    
    
}
  

