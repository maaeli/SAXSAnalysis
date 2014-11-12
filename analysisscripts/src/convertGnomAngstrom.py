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

import os.path as op
import os 



filenameIn = '/users/brennich/barbaramaria/GrpE45/20140925_13mg/dammif/gnomv3p2/frame842_856_v3.out'
filenameOut = filenameIn.split('.')[0] + '_invA.out'

def convert(filenameIn, filenameOut):
    with open(filenameIn,'rb') as nmFile:
        with open(filenameOut,'w') as AngFile:
            scatteringdata = False
            gnomdata = False
            lastline = ''
            for line in nmFile:
                outline =''
                if 'Current ALPHA' in line:
                    values = line.split()
                    values[-4] = 10* float(values[-4])
                    outline = '  Current ALPHA         :   {:s}   Rg :  {:.3E}   I(0) :   {:s}'.format(values[-7], values[-4],values[-1])
                elif scatteringdata: 
                    if line.split() == []:
                        outline = line
                        scatteringdata = False
                    else: 
                        values = line.split()
                        q = '{:.4E}'.format(0.1*float(values[0]))
                        outline = line.replace(values[0],q,1)
                        assert len(line) == len(outline)
                elif gnomdata:
                    if any(text in line for text in ('Real','Reciprocal')):
                        values = line.split() 
                        Rg = '{:g}'.format(10*float(values[4]))
                        outline = line.replace(values[4],Rg,1)  
                        if 'Real' in line:  
                            dRg = '{:g}'.format(10*float(values[6]))
                            outline = outline.replace(values[6],dRg,1)
                            gnomdata = False
                    else: 
                        values = line.split()
                        d = '{:.4E}'.format(10*float(values[0]))
                        outline = line.replace(values[0],d,1)
                        assert len(line) == len(outline)        
                elif    'S          J EXP       ERROR' in lastline and line.split() == []:
                    outline = line 
                    scatteringdata = True
                elif   'R          P(R)      ERROR' in lastline and line.split() == []:
                    outline = line 
                    gnomdata = True
                else:
                    outline = line   
                lastline = line
                AngFile.write(outline)   
                     
                     
if __name__ == '__main__':
    convert(filenameIn, filenameOut)                     
