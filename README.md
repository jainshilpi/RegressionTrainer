In order to use this code do:

```bash
==============================Instructions for 2018 UL release=====================================
cmsrel CMSSW_10_5_0
cd CMSSW_10_5_0/src
cmsenv
git clone git@github.com:cms-egamma/HiggsAnalysis.git
To make it work in CMSSW_10_5_0, please change the line in HiggsAnalysis/GBRLikelihood/Buildfile.xml:
<flags CXXFLAGS="-O3 -ftree-loop-linear -floop-interchange -ffast-math -fopenmp -std=gnu++1y"/>
TO
<flags CXXFLAGS="-O3 -ftree-loop-linear -floop-interchange -ffast-math -fopenmp "/>

scram b -j 4
git clone https://github.com/jainshilpi/RegressionTrainer.git -b PFUL2018
cd RegressionTrainer
make -j 4
```



```bash
==============================Instructions for 2017 UL release=====================================
cmsrel CMSSW_10_5_0
cd CMSSW_10_5_0/src
cmsenv
git clone git@github.com:cms-egamma/HiggsAnalysis.git
To make it work in CMSSW_10_5_0, please change the line in HiggsAnalysis/GBRLikelihood/Buildfile.xml:
<flags CXXFLAGS="-O3 -ftree-loop-linear -floop-interchange -ffast-math -fopenmp -std=gnu++1y"/>
TO
<flags CXXFLAGS="-O3 -ftree-loop-linear -floop-interchange -ffast-math -fopenmp "/>

scram b -j 4
git clone https://github.com/jainshilpi/RegressionTrainer.git -b PF2017UL_trainer
cd RegressionTrainer
make -j 4
```

```bash
==============================Instructions for 10X release=====================================
cmsrel CMSSW_10_0_3
cd CMSSW_10_0_3/src
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
