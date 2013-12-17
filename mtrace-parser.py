import sys
import os.path
import string

def parse(ifile, ofile):
    try:
        fromfile=open(ifile,'r')
        tofile=open(ofile, 'w')
    except IOError as e:
        sys.stderr.write('%s: %s\n' % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    memblks={}
    usedmem=0
    usedmax=0
    allocmax=0
    lines=fromfile.readlines()
    for line in lines:
        # print line
        items=line.split()
        if items[0]=='@':
            if items[2]=='+':
                memblks[items[3]]=items[4]
                val=string.atoi(items[4],16)
                if val>allocmax:
                    allocmax=val
                usedmem=usedmem+val
                oline='+%6d=%8d %s' % (val, usedmem, line)
                if usedmem > usedmax:
                    usedmax=usedmem
            elif items[2]=='-':
                val=string.atoi(memblks[items[3]], 16)
                usedmem=usedmem-val
                del memblks[items[3]]
                oline='-%6d=%8d %s' % (val, usedmem, line)
            else:
                sys.stderr.write('error format in line %d\n%s' % (list.index(line), line))
                sys.exit(2)
            print oline    
            tofile.write(oline)
    oline='<%6d<%8d' % (allocmax, usedmax)
    print oline
    fromfile.close()
    tofile.close()                                 
                                 
def main(argv):
    print 'argv=',argv
    if len(argv)==2:
        ifile=argv[0]
        ofile=argv[1]
    elif len(argv)==1:
        ifile=argv[0]
        ofile=argv[0]+'.out'
    elif len(argv)==0:
        ifile=raw_input('full path to the mtrace file: ')
        ofile=ifile+'.out'
    print 'input from file: '+ifile
    print 'output to file: '+ofile

    parse(ifile, ofile)

#entry point
if __name__=="__main__":
    main(sys.argv[1:])
	
