"""
Tip calibration
===============

Initialize the datafile containing the calibration measurements, using nuMat=0.18 as the tip’s Poisson’s ratio::

		from nanoindentation import Indentation, Tip
		i = Indentation("FS_Calibration.xls", nuMat=0.18)
		i.plotAsDepth("K2P")

.. figure:: ../source/img/plotAsDepth_k2p.png
	:width: 400
	:align: center
	:alt: Alternative text

``i.plotAsDepth("K2P")`` plots :math:`stiffness^2/load` as a function of the depth and the orange line should be horizontal.

Perform the calibration. Specify "True" for plotStiffness and plotTip  to check the plotted compliance and shape of the tip::

		i.calibration(plotStiffness=True, plotTip=True)

.. figure:: ../source/img/calibrate_plotStiffness.png
	:width: 400
	:align: center
	:alt: Alternative text

	Stiffness

The datapoints at larger forces (smaller values on the diagram) are used for the fitting.

.. figure:: ../source/img/calibrate_plotTip.png
	:width: 400
	:align: center
	:alt: Alternative text

	Tip Shape

.. figure:: ../source/img/plotIndenterShape_error.png
	:width: 400
	:align: center
	:alt: Alternative text

	Error in tip shape calibration

The blue points represent the experimental data. The blunting of the used tip is easily noticable at the very beginning of the orange line. A relative error of 5-10% is typical.

(To zoom in the blunted part of the tip, use ``plotIndenterShape()`` at e.g. maxDepth 0.25)::

		i.tip.plotIndenterShape(maxDepth=0.25)

Finally, initialize the measurement data, specifying the tip as the just calibrated one::

		j = Indentation("NiAl_250nm_TUIL_max_depth_1000nm_GM3_SM_previousGM1.xls", tip = i.tip)

Continue the analysis with the calibrated tip as described in the "Getting started" secion.
"""