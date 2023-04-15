# Accurate Hijri Calculator (AHC)

![image1](ahc_logo.png)

Accurate Hijri Calculator (AHC) is a software for calculating the position and visibility of the crescent moon at the sunset time after the conjunction (ijtima'/new moon phase) that marks the beginning of a new month in the Islamic lunar calendar (Hijri calendar). This tool is intended for helping moslem people in estimating the start of a new Hijri month, making a calendar for coming years, comparing among the criteria of Hijri calendar, as well as educating people about the current issues regarding the Hijri calendar. This software incorporates various current crescent visibility criteria adopted by moslem organizations around the world. AHC was firt developed in 2012 and was published at [link](https://fi.ub.ac.id/kemahasiswaan-alumni/keorganisasian/tim-astronomi-fisika/accurate-hijri-calculator-2-2/). While it was built with GUI support from Delphi, now AHC is transformed into fully python package and work on terminal without GUI display. One can run AHC on [Jupyter notebook](https://jupyter.org/) to get GUI experience as shown in example here.         

## Developer
This software is developed and maintained by [Abdurro'uf](https://aabdurrouf.github.io/), who is currently working as a researcher at the Department of Physics and Astronomy, The Johns Hopkins University and The Space Telescope Science Institute (STScI). 
 
## Installation
To install AHC, first clone AHC package into your desired directory (in your local machine) and then enter `ahc` directory and install. You can do it using the following commands 

```
git clone https://github.com/accuhijri/ahc.git
cd ahc
python -m pip install .
```

To use AHC, you need to put `de421.bsp` file in wherever directory you are working. This file is included in the `ahc` package and can be copied to your working directory. An alternative way would be to download this file from NASA website using the following command

```
wget https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp
```

Last but not least, you need to install [geopandas](https://geopandas.org/en/stable/) if you intend to produce crescent visibility map with AHC. To install it, you can use the following command, assuming you have `conda` installed in your machine.

```
conda install -c conda-forge geopandas
```

## Some features
