.. _tif:

Tif Images: Basic usage
***********************

Usage of the Tif library is straight forward

- open the file with i = Tif('')
- enhance the gray-scales. The default is generally ok. Sometimes, other contrast adaptation might be better.
- add a scale bar. The default calculates the size and font-size and puts it on the bottom left.
- show the image on the screen, for verification.
- save the file, the default is jpg.

This is excuted in the following fashion::

  from micromechanics.tif import Tif
  i = Tif('examples/Zeiss/Zeiss.tif')
  i.enhance()
  i.addScaleBar()
  i.show()
  i.save()

Please see the complete documentation for more options: :ref:`tifLibrary`
