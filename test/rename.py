import os
from os import listdir
from os.path import isfile, join
mypath='C:/Users/Lam/Videos/TEECHIP/ASANTAINTHECHRISMAS'
# listdir=os.listdir(path)
onlyfolder = [f for f in listdir(mypath) if not isfile(join(mypath, f))]
print(onlyfolder)

for folder in onlyfolder[:]:
    new_path=mypath+"/"+folder
    onlyfile_png=[f for f in listdir(new_path) if  isfile(join(new_path, f))  and 'cool' in f]
    old_name=new_path+'/'+ onlyfile_png[0]
    new_name=folder.title().replace('-', ' ')
    new_name=new_path+'/'+ new_name+'.png'

    print(new_name)
    os.rename(old_name, new_name)
