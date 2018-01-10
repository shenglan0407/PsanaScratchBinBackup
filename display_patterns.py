from psana import *
import matplotlib.pyplot as plt

ds = DataSource('exp=cxilp6715:run=80:smd')
det = Detector('CxiDs1.0:Cspad.0')

for nevent,evt in enumerate(ds.events()):
    if nevent>=2: break
    # includes pedestal subtraction, common-mode correction, bad-pixel
    # suppresion, and uses geometry to position the multiple CSPAD panels
    # into a 2D image
    print 'Fetching event number',nevent
    img = det.image(evt)
    plt.imshow(img,vmin=0,vmax=40)
    #plt.imshow(img,vmin=-2,vmax=2)
    plt.show()
print 'Done.'
