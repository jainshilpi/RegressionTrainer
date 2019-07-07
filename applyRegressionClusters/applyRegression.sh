#!/bin/bash


#./applyRegression.exe -t /eos/cms/store/group/phys_egamma/PFClusteRegressionTrees/afterDebug_16june/pfClusters_PU_testing.root -o pfClusters_PU_application_OLD.root -c ../python/training_all_weights_NOPU_nbinsFlag_nhits123AsInput_FULLnoPUstats_NOPTETA_AFTERDEBUG16june/Config_May8_pfcluster -p ../training_all_weights_NOPU_nbinsFlag_nhits123AsInput_FULLnoPUstats_NOPTETA_AFTERDEBUG16june/Config_May8_pfcluster


#./applyRegression.exe -t /eos/cms/store/group/phys_egamma/PFClusterCalibration/150_V0_2017/pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/Config_May8_pfcluster -p ../rootfiles_16may/Config_May8_pfcluster

#./applyRegression.exe -t pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/morenhits_8cores/Config_May8_pfcluster -p ../morenhits_8cores/Config_May8_pfcluster

#./applyRegression.exe -t pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/morenhits_8cores_actualnhits/Config_May8_pfcluster -p ../morenhits_8cores_actualnhits/Config_May8_pfcluster

#./applyRegression.exe -t pfClusters_noPU_testing.root -o pfClusters_noPU_application.root -c ../python/Config_May8_pfcluster -p ../rootfiles_16may/Config_May8_pfcluster

#./applyRegression.exe -t pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/Config_May8_pfcluster -p ../rootfiles_20may_trainingPU/Config_May8_pfcluster

#./applyRegression.exe -t pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/configs_PU_nvtx/Config_May8_pfcluster -p ../Config_May8_pfcluster

#./applyRegression.exe -t pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/Config_May8_pfcluster -p ../rootfiles_16may/Config_May8_pfcluster

#./applyRegression.exe -t pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/Config_May8_pfcluster -p ../PU_etaLT2/Config_May8_pfcluster

./applyRegression.exe -t pfClusters_PU_testing.root -o pfClusters_PU_application.root -c ../python/configs_PU/Config_May8_pfcluster -p ../PU_allEta/Config_May8_pfcluster