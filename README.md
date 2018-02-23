In order to use this code do:

```bash
cmsrel CMSSW_9_4_0_patch1
cd CMSSW_9_4_0_patch1/src
cmsenv
git clone git@github.com:cms-egamma/HiggsAnalysis.git
scram b -j 4
git clone https://github.com/jainshilpi/RegressionTrainer.git -b trainer_2018
cd RegressionTrainer
make -j 4
```
==================================Instructions for 2017=================================<br/>
In order to use this code do:

```bash
cmsrel CMSSW_9_1_0_pre3
cd CMSSW_9_1_0_pre3/src
cmsenv
git clone git@github.com:cms-egamma/HiggsAnalysis.git
scram b -j 4
git clone git@github.com:cms-egamma/RegressionTrainer.git
cd RegressionTrainer
make -j 4
```
