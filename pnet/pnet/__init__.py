# Yuncong Ma, 1/19/2024
# pnet
# This script provides the highest level organization of pnet
# It provides workflows of pnet, and examples
# It includes five modules of pnet, underlying functions

#########################################
# Packages
import os
import sys

# path of pnet
current_file_path = os.path.abspath(__file__)
dir_python = os.path.dirname(current_file_path)
dir_pNet = os.path.dirname(dir_python)
dir_brain_template = os.path.join(dir_pNet, 'Brain_Template')
dir_example = os.path.join(dir_pNet, 'Example')

sys.path.append(dir_python)

# Example

# Brain templates

# Module
# This script builds the five modules of pnet
# Functions for modules of pnet
from Module.Data_Input import *
from Module.FN_Computation_torch import *
from Module.FN_Computation import *
from Module.Visualization import *
from Module.Quality_Control import *
from Module.FN_Computation_torch import *
from Report.Web_Report import *
from Workflow.Workflow_Func import *


