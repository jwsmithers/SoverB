#!/bin/bash
echo "Setting up ATLAS environment ..."
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
. ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet || return 1
lsetup "lcgenv -p LCG_92 x86_64-slc6-gcc62-opt root_numpy"
lsetup "lcgenv -p LCG_92 x86_64-slc6-gcc62-opt matplotlib"
lsetup "lcgenv -p LCG_92 x86_64-slc6-gcc62-opt rootpy"
