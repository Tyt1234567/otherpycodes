import re
import numpy

with open(r'D:\遥感实习数据\20240623\wordview3_spec.txt','r') as spec_txt:
    text = spec_txt.read()
    text.replace('\n','')
    text = text.split(' ')

data = []
for i in text:
    if len(i)>2:
        data.append(float(i))

#下面存入响应函数
wavelength = []
coastalblue = []
blue = []
green = []
yellow = []
red = []
reddege = []
nir1 = []
nir2 = []

for i in range(0,len(data),9):
    wavelength.append(i)
    coastalblue.append(data[i+1])
    blue.append(data[i+2])
    green.append(data[i+3])
    yellow.append(data[i+4])
    red.append(data[i+5])
    reddege.append(data[i+6])
    nir1.append(data[i+7])
    nir2.append(data[i+8])

def read_spectral(file):
    a = []
    with open(file,'r') as ref_data_txt:
        ref_data = ref_data_txt.read()
        ref_data.replace("\n","")
        ref_data = re.split(r'[ \n]+', ref_data)

    for i in ref_data:
        if len(i)>2:
            a.append(float(i))
    b = []
    for i in range(0,len(a)-1,2):
        b.append(a[i+1])
    return b

cement1 = read_spectral(r'D:\遥感实习数据\20240623\623spectra\15A6068_00002.sed')
cement2 = read_spectral(r'D:\遥感实习数据\20240623\623spectra\15A6068_00007.sed')

grass1 = read_spectral(r'D:\遥感实习数据\20240623\623spectra\15A6068_00003.sed')
grass2 = read_spectral(r'D:\遥感实习数据\20240623\623spectra\15A6068_00018.sed')


def cal_average_reflectance(band,object):
    xiangying_sum = sum(band)
    result = 0
    for i in range(min(len(object),len(band))):
        result+=band[i]*object[i]
    result = result/xiangying_sum
    return result

objects = [grass1,grass2,cement1,cement2]
bands = [coastalblue,blue,green,yellow,red,reddege,nir1,nir2]


reflectance = []
for object in objects:
    for band in bands:
        result = cal_average_reflectance(band,object)
        reflectance.append(result)

grass1_ref = reflectance[0:8]
print(grass1_ref)
grass2_ref = reflectance[8:16]
cement1_ref = reflectance[16:24]
cement2_ref = reflectance[24:32]

grass1_dn = [191,301,382,218,191,349,584,429]
grass2_dn = [182,269,318,174,152,275,519,380]
cement1_dn = [257,472,642,413,403,392,470,323]
cement2_dn = [203,318,375,217,197,208,258,171]

bands_k = []
bands_b = []

grass1_ks, grass2_ks, grass1_bs, grass2_bs, cememt1_ks, cement2_ks, cement1_bs, cement2_bs = [],[],[],[],[],[],[],[]
for i in range(8):
    y=[grass1_ref[i],grass2_ref[i],cement1_ref[i],cement2_ref[i]]
    x=[grass1_dn[i],grass2_dn[i],cement1_dn[i],cement2_dn[i]]

    band_k,band_b = numpy.polyfit(x,y,1)
    bands_k.append(band_k)
    bands_b.append(band_b)

print(bands_k)
print(bands_b)