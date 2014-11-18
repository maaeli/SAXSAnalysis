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
import argparse
import glob




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
    parser = argparse.ArgumentParser(description='Convert GNOM .out file from nm to Angstrom')
    parser.add_argument('inputFilename', metavar='inputFilename',nargs='?',
                        help = 'Name of the file to convert. If not specified, all .out files not containing invA will be converted')
    parser.add_argument('-o', metavar='outputFilename', dest = 'outputFilename',default='',
                        help = 'Name of the converted output file.')
    args = parser.parse_args()
    print args
    inputFilename = args.inputFilename
    outputFilename = args.outputFilename
    
    if inputFilename:
        if op.exists(inputFilename):
            print 'File {} exists.'.format(inputFilename)
            if outputFilename == '':
                outputFilename = ''.join(inputFilename.split('.')[:-1])+'_invA.out'
                print outputFilename
            if op.exists(outputFilename):
                print 'File {} exists. No files processed'.format(outputFilename)
            else:
                try: 
                    convert(inputFilename, outputFilename)  
                except IOError:
                    print 'IOError doing the conversion from {} to {}'.format(inputFilename,outputFilename)
                else: 
                    'Converted. Data written to {}'.format(outputFilename)  
        else:
            print 'File {} not found.'.format(args.inputFilename)
    else: 
        files = [fn for fn in glob.glob('*.out') if not 'invA' in fn]
        print 'No file specified. Found {}.'.format(files)
        for inputF in files:            
            outputFilename = ''.join(inputF.split('.')[:-1])+'_invA.out'
            if op.exists(outputFilename):
                print 'File {} exists. {} not processed'.format(outputFilename, inputF)
            else:
                try: 
                    convert(inputF, outputFilename)  
                except IOError:
                    print 'IOError doing the conversion from {} to {}'.format(inputF,outputFilename)
                else: 
                    'Converted {}. Data written to {}'.format(inputF,outputFilename)                         
