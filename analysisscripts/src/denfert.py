# coding: utf-8
#

# Copyright (C) 2014 ESRF
#
# Principal author: Martha Brennich
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Martha Brennich"
__license__ = "GPLv3+"
__copyright__ = "2014 ESRF"
__date__ = "20141007"
__status__ = "development"


import subprocess as sp  
import os
import os.path as op
from datetime import datetime
from shutil import copyfile 

program_name = '/users/brennich/softwaretest/Denfert/Denfert_linux64'
config_name = 'denfertconfig.txt'
inputfile= 'merege_v1_invA_v1.out'
numberofruns = 10

def strEmptyDefault(valueString):
    if not valueString == '':
        return str(valueString) 
    return valueString
    

def generateConfigText(inputfile, prefix="denfert", runNumber=1, mode="A", q_max='', D_max='', 
                       subtract = '', particleDensity = '', solventDensity = '', 
                       layerContrast = '', knotNumber = '', radius = '', annealingT = '',
                       annealingSchedule = '', penalty = '', trialsperbead = ''):
    text = ""
    if not (solventDensity == '' and layerContrast == '' and knotNumber == '' and \
              radius == '' and  annealingT == '' and annealingSchedule == '' and  penalty == '' and
              trialsperbead == ''):
        mode = 'A'
    mode = mode.upper()
    if mode not in ('A', 'S', 'F'): 
        mode = 'A'
    text += mode + "\n"
    text += prefix + str(runNumber) + "\n"
    text += inputfile + "\n"
    text += strEmptyDefault(q_max) + "\n"
    text += strEmptyDefault(D_max) + "\n"
    text += strEmptyDefault(subtract) + "\n"
    text += strEmptyDefault(particleDensity) + "\n"
    text += strEmptyDefault(solventDensity) + "\n"
    text += strEmptyDefault(layerContrast) + "\n"
    text += strEmptyDefault(knotNumber) + "\n"
    text += strEmptyDefault(radius) + "\n"
    text += strEmptyDefault(annealingT) + "\n"
    text += strEmptyDefault(annealingSchedule) + "\n"
    text += strEmptyDefault(penalty) + "\n"
    text += strEmptyDefault(trialsperbead) + "\n"
    return text
    
if __name__ == '__main__':
    
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')).translate(None, ' -:')
    directory = "denfert" + date
    if not os.path.exists(directory):
        os.makedirs(directory)
    copyfile(inputfile, op.join(directory,inputfile))
    os.chdir(directory)
    for runNumber in range(numberofruns):
        config_name = 'denfert_config%d.txt'%runNumber
        with open(config_name,'a') as config:
            config.write(generateConfigText(inputfile, prefix="test", runNumber=runNumber))
        sp.call([program_name,config_name])
    