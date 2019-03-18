import os, sys, subprocess, shutil

def list_file(f):
    files=[]
    for dirname, dirnames, filenames in os.walk(f):
        for filename in filenames:
           files.append(os.path.join(dirname, filename))
    return files

def list_dir(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

script_dir=os.path.dirname(os.path.realpath(sys.argv[0]))
work_dir=os.getcwd()

print('\nWelcome! Initialized:\n')

filename = input('Enter .xyz file name...\t\t\t')

molecule=[]

with open(filename) as file:
    lines = file.readlines()

H_count=0

for line in lines:
    line=line.split()
    if line[0]=='H':
        H_count+=1
    molecule.append([line[0],line[1],line[2],line[3]])

print('Hydrogens detected...\t\t\t', H_count, sep='')

H_select = input('Enter index of removable atoms...\t')
H_select=H_select.split()

### Hydrogens check
H_suspect=[]
for i in H_select:
    if molecule[int(i)-1][0]!='H':
        H_suspect.append(i)
if len(H_suspect)!=0:
    print('Hydrogens check...\t\t\tFAILED!')
    print('Warning! Atom', ',  '.join(H_suspect), 'is/are not an Hydrogen...   Abort, sorry :(')
    quit()
else:
    print('Hydrogens check...\t\t\tPASS!')
### End Hydrogens check

print('Generating G16 input...', end="", flush=True)

if not os.path.exists(work_dir + '/Radicals'):
    os.makedirs(work_dir + '/Radicals')
else:
    shutil.rmtree(work_dir + '/Radicals')
    os.makedirs(work_dir + '/Radicals')


for i in H_select:
    f=open(str(work_dir + '/Radicals/'+str(i)+'.rad'),"w+")
    for idx_i, pro_i in enumerate(molecule):
        if idx_i!=int(i)-1:
            f.write(str('    '.join(pro_i) + '\n'))
    f.close()


for i in list_file(work_dir + '/Radicals'):
    subprocess.call('cat ' + script_dir + '/head ' + i + ' ' + script_dir + '/tail' + ' > ' + i +'.inp', shell=True)
print('DONE!')
