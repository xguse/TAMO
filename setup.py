# window 100 columns wide, please

from distutils.core import setup, Extension
import os, sys, string

if( sys.hexversion < 0x020200f0 ):
	print "\nPython 2.2 or greater is required for TAMO\n";
	sys.exit(1)
elif( sys.hexversion < 0x020300f0 ):
	print "\nPython 2.3 or greater is recommended for TAMO\n"
	print "With v2.2 there may be reduced funcationality.  Your mileage may vary.\n\n";
	yn = raw_input("Install anyway? (Y/n)")
	if( string.lower(yn) == 'n' ):
		sys.exit(1)

print sys.argv
ok = 0
for a in sys.argv:
	if( string.find(a, 'install') > -1 ): ok = 1

if( not ok ):
	print "Usage:\n"
	print "	python setup.py install		- to install TAMO\n\n"
	sys.exit(0)

setup(name='TAMO',
      version=open('VERSION').read().strip(),
      packages=['TAMO', 'TAMO.seq', 'TAMO.util', 'TAMO.DataSources', 
                'TAMO.MD', 'TAMO.Clustering', 'TAMO.MDconvert'],
      ext_modules=[Extension('TAMO.MD._MDsupport', ['TAMO/MD/MDsupport_source/MDsupport.cxx', 
                                                   'TAMO/MD/MDsupport_source/MDsupport_wrap.cxx']), 
                   Extension('TAMO.util._swilk',   ['TAMO/util/swilk_source/swilk.cxx', 
                                                   'TAMO/util/swilk_source/swilk_wrap.cxx'])],
     )

# so it loads the module from the lib, not .
sys.path[0] = '/dev/null'

import TAMO
tamopath = getattr(TAMO, '__path__')[0]

print "\nTAMO is installed in %s\n\n" % tamopath
datapath = ''
#while( not os.path.isdir(datapath) or not os.access(datapath, os.W_OK) ):
while not os.path.isdir(datapath) :
	datapath = raw_input("Enter path for TAMO data: ")
	datapath = os.path.realpath(datapath)
	if( not os.access(datapath, os.F_OK) ):
		createyn = 'z'
		while( createyn and string.lower(createyn) != 'y' and 
                       string.lower(createyn) != 'n' ):
			createyn = raw_input("Directory does not exist, create? (Y/n)")
		if( string.lower(createyn) == 'y' or not createyn ):
			os.mkdir(datapath)
		else:
			datapath = ''

print "Using datapath: %s\n" % datapath

f = open(tamopath + "/localpaths.py", "w")
f.write("TAMOroot = '%s/'\n" % tamopath)
f.write("TAMOdata = '%s/'\n" % datapath)
f.close()

for x in ['/MD/AlignAce.py', '/MD/MDscan.py', '/MD/Meme.py', '/MD/TAMO_EM.py', '/seq/FakeFasta.py',
          '/seq/GenerateFastas.py', '/seq/Background.py', '/util/WMWtest.py', '/util/Arith.py', 
          '/util/PermuteTools.py', '/util/Poisson.py', '/DataSources/GO.py', 
          '/DataSources/PDB.py', '/DataSources/SGD.py', '/DataSources/Holstege.py', 
          '/DataSources/Yeast6kArray.py', '/DataSources/Novartis.py',
          '/MotifMetrics.py', '/MDconvert/ace2tamo.py', '/MDconvert/kellis2tamo.py',
          '/MDconvert/tamo2table.py', '/MDconvert/tamo2tamo.py', '/MDconvert/meme2tamo.py',
          '/MDconvert/memeset2tamo.py', '/Sitemap.py', '/GetDataFiles.py', 
          '/Clustering/Kmedoids.py', '/Clustering/MotifCompare.py', '/Clustering/UPGMA.py', '/MD/THEME.py']:
	os.chmod(tamopath + x, 0755)

print "\nData file download:\n\nNOTE: HumanSeq download is very large.\n";
for ds in "HumanSeq Whitehead Novartis GO SGD Holstege".split():
	yn = raw_input("Download '%s' data set (Y/n)? " % ds)
	if( string.lower(yn) != 'n' ):
		os.system("%s %s/GetDataFiles.py --%s" % (sys.executable, tamopath, ds))

print "\nExternal code download:\n";
for dstup in [("Clarke", 'ROC AUC')]:
	yn = raw_input("Download '%s' (%s) code (Y/n)? " % (dstup[0],dstup[1]))
	if( string.lower(yn) != 'n' ):
		os.system("%s %s/GetDataFiles.py --%s" % (sys.executable, tamopath, dstup[0]))

print """

To download skipped datasets or code later, run:
%s/GetDataFiles.py --DataSetName (or --SourceCodeName)

Running the program without arguments will provide a list of possible names.

NOTE: setup.py does NOT install the WebLogo package from weblogo.berkeley.edu.
If you would like to install it, use the --weblogo option for GetDataFiles.py,
and follow the manual installation instructions.

""" % (tamopath)

raw_input("[Hit Enter]")

print "\nTesting..."
print "\tChecking the Enrichment of GCN4 binding motif "
print "\tin YPD Binding data from Harbison et al."
p = os.popen("%s %s/MotifMetrics.py GCN4_YPD.fsa TGASTCA" % (sys.executable, tamopath), "r")
plines = p.readlines()
p.close()
testok = 0
print
print ''.join(plines)
print 
for rl in plines:
	if( rl[0] == 'E' ):
		if( rl[:64] == "E:      233 / 6725,  40 /   59 found.       p: 1.01e-45  TGASTCA" ):
			print "Success!  The Enrichment of the motif is log10(1.01e-45).\n"
			testok = 1
		else:
			print "FAILED\n"
			sys.exit(1)

if( not testok ):
	print "FAILED\n"
	sys.exit(1)

raw_input("[Hit Enter]")

print """

You probably want to set a "TAMO" environmental variable pointing to
the installation path to the TAMO modules.  This will be useful when
invoking TAMO command line utilities.  For example, after you've set
up TAMO, you'll be able to simply invoke "$TAMO/Sitemap.py" in order
to build a motif map from a fasta-formatted file with occurences of
your favorite motif or "$TAMO/AlignAce.py" to run the multi-pass
AlignACE wrapper program.

If your shell is a csh/tcsh derivative, the variable is set executing the line:

   setenv TAMO "%s"

and by also putting a line with this command into your .cshrc or .tcshrc.

For sh/bash shells, type
   
   TAMO="%s"
   export TAMO

You'll also need to put these lines into your .bashrc file.
""" % (tamopath, tamopath)


