# GeoScPlot

GeoScPlot is a Python "library" created to provide nice, high-quality (high-resolution) templates for common discriminant plots used in Earth Sciences.
Basically, all plots are those I often used while studying Geosciences at Universidad de Los Andes, Bogotá, Colombia.

Templates are built over Matplotlib and [Ternary](https://github.com/marcharper/python-ternary) so you should install them both beforehand.

The package is also capable of plotting a bunch of geochemical discriminant plots from (geochemical) data, for this, I used McDonough & Sun's data on chondrites and MORB. To test it, I used data that was provided to me in the courses of Geochemistry (2015-1) and Petrology (2016-2). In principle, any set of geochemical data can be processed to be used with the library, here a few important steps.

## Processing input datasets
The library relies strongly on Pandas, so install that, too.
+ Import raw dataset as pandas DataFrame.
+ Make sure that the *sample name* is the DataFrame's index and that each *oxide/element* is a column, avoid repetition.
+ I believe anyone would be able to workaround an unexpected issue. For example, the code is designed to plot 6 samples of different colors, I believe there would be trouble with more samples than that but a look at the source code should give the answer (which is: **put more colors in  `loscolores` list**.)

## Using the templates

There are a handful of quite useful templates, divided in two "modules"

### TwoDPlots
To use it, save the **GeoScPlot** folder in your working directory and import it as
 ```
 from GeoScPlot.TwoDPlots import *
 ```
This module contains:
+ `convertToAnhBase()` given a LOI column
+ `buildTas()` Total Alkali vs. feldespar
+ `plotTAS(data)`
+ `plotHarker(data)` Harker plots (plenty)
+ `buildZrTi_NbY()` Igneous rock classification
+ `plotZrTi_NbY(data)`
+ `plotREE(data)` Rare Earth Elements plot
+ `plotSpider(data)` Spider plot
+ `buildShervais()` Shervais discriminant for igneous provenance
+ `plotShervais(data)`
+ `buildThTa()` Igneous provenance classification/ series classification
+ `plotThTa(data)`
+ `buildPierce()` Igneous provenance
+ `plotPierce(data)`

All `build*` functions return a `figure, ax`, so they are to be used as `fig, ax = buildTas()`. This will return the template for the TAS discriminant.

All `plot*` functions have keyword arguments `save` and `nombre` (sorry for the spanglish) so they can be called as
`plotTAS(data, save=True, nombre = "proyectoPetrologia")`. Default save resolution is 300dpi (which I think is more than enough).

![alt text](https://github.com/dforero0896/GeoScPlot/blob/master/readme_pics/exampleTASTemp.png)

A Shervais diagram would look like

![alt text](https://github.com/dforero0896/GeoScPlot/blob/master/readme_pics/exampleShervais.png)


Some examples may be found [here](https://github.com/dforero0896/GeoScPlot/blob/master/tests/geoscplot_test.ipynb).

### TernaryPlots

To use it, save the **GeoScPlot** folder in your working directory and import it as
 ```
 from GeoScPlot.TernaryPlots import *
 ```

These were usually a pain to plot in a nice way, until I found [Ternary library](https://github.com/marcharper/python-ternary). Nevertheless, the templates were still missing, so I made them. This module does *not* include plotting functions, but I'll show how to use the templates since I find them easier to use on their own.

This module contains:
+ `buildProvenancePlot()` Tectonic provenance classification
+ `buildSSTClassification()` Sandstone classification
+ `buildPettijohnSST()` Pettijohn sandstone classification
+ `buildPettijohnWacke()` Pettijohn wacke classification.
+ `buildCong()` conglomerate/gravel classification.
+ `buildQAP()` the upper part of the QAPF diagram
+ `buildAPF()` the other part of the QAPF diagram.

These functions return `figure, tax`. You should read Ternary's docs for accurate information on `tax` (`TernaryAxesSubplot`) objects, but they work quite similarly to `AxesSubplot` from Matplotlib.

#### Use of TernaryPlots

```
from GeoScPlot.TernaryPlots import *
```
Get the template that you need, for example let's say you are to classify an igneous rock using the QAP diagram.
```
fig, tax = buildQAP() #Plots the template
```
Your data (sample composition) must be in a python tuple of the form `rock = (P, Q, A)`, although you can have `rock = (P,Q)` and Ternary will figure out `A` since they all must add 100.
```
tax.scatter([rock], s = 100, marker = 's', c='r') #Plots the dot with size 100 and a red square marker.
```
In general, data should be passed as a list of tuples or lists, one per sample. These samples must be organized as `(Bottom, Right, Left) = (Bottom right, Top, Bottom left)`, the latter in terms of triangle vertices.

Now, let's use other template:
```
f, tax = buildCong()
rock = [50., 20.] #50% Sand, 20% Gravel, then 30% Mud
tax.scatter([rock], s =100, marker ='s', c='r')
plt.gcf()
plt.tight_layout()
plt.show()
```
![alt text](https://github.com/dforero0896/GeoScPlot/blob/master/readme_pics/exampleGravelCongs.png)


For more details on the use of the ternary library, visit their GitHub.

## Bibliography

+ W.F. McDonough and S. -s. Sun, Chemical Geology 120, 223 (1995).
+ J.A. Pearce, T. Alabaster, A.W. Shelton, and M.P. Searle, Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences 300, 299 (1981).
+ J.W. Shervais, Earth and Planetary Science Letters 59, 101 (1982).
+ S. -s. Sun and W.F. McDonough, Geological Society, London, Special Publications 42, 313 (1989).
+ I.F. Blanco-Quintero, A. García-Casco, L.M. Toro, M. Moreno, E.C. Ruiz, C.J. Vinasco, A. Cardona, C. Lázaro, and D. Morata, International Geology Review 56, 1852 (2014).
