from osgeo import gdal
import subprocess
import glob
import os
import tarfile
import rasterio

## 1. Unzip file ###
def Unzip():
    zipfiles = glob.glob('*.tar.gz')
    for zfile in zipfiles:
        tar = tarfile.open(zfile, 'r:gz')
        tar.extractall(path=zfile[:-7])
        tar.close()
        print('Extracted all file for ' + zfile)
        os.remove(zfile)

## 2. Stack bands ###
def StackBands():
    folders = glob.glob('L*SC*')
    for folder in folders:
        tiffs = glob.glob(folder + '/*band[{0}]*'.format(band))

        with rasterio.open(tiffs[0]) as src:
            profile = src.profile.copy()
        profile.update(count=len(tiffs))
        stackedname = folder[4:20] + '_stack.tif'
        with rasterio.open(stackedname, 'w', **profile) as dst:
            for i, tif in enumerate(tiffs):
                with rasterio.open(tif) as tif_file:
                    dst.write_band(i+1, tif_file.read(1))

### 3. Mosaic inputs ###
def MosaicImages():
    stacked = glob.glob('*stack.tif')
    pipe = subprocess.Popen('bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    mosaicname = 'mosaic.tif'
    imgs = ' '.join(stacked)
    imgs = imgs.replace('\\', '/')
    #commands = 'gdal_merge.py -o {0} -of GTiff -n -9999 {1}'.format(mosaicname, imgs)
    commands = 'gdalwarp -of GTiff -srcnodata -9999 -dstnodata -9999 {0} {1}'.format(imgs, mosaicname)
    output, err = pipe.communicate(bytes(commands, 'utf8'))
    print(output)


########################################

##path = '139'
##year = '2015'
path = input('path: ')
year = input('year: ')
steps = input('Unzip(1), Stack Bands(2), Mosaic Images(3)(e.g. 123 for all steps): ')
os.chdir('D:/CSISS/data/' + path + '/' + year)

bands = ''
if year == '2015':
    band = '2-7'
else:
    band = '1-7'

if steps == '123':
    Unzip()
    StackBands()
    MosaicImages()
elif steps == '23':
    StackBands()
    MosaicImages()
elif steps == '3':
    MosaicImages()
else:
    print('Input error. Try 123 or 23 or 3')


