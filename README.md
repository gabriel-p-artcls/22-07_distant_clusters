
# Analysis of the 25 most distant clusters


<!-- MarkdownTOC levels="1,2,3" autolink="true" style="ordered" -->

1. [Gaia EDR3 data](#gaia-edr3-data)
1. [pyUPMASK](#pyupmask)
1. [Members selection](#members-selection)
1. [Extinction](#extinction)
1. [ASteCA](#asteca)

<!-- /MarkdownTOC -->


## Gaia EDR3 data

The clusters where selected from the WEBDA, OPENCLUST, MWSC, and [Cantat-Gaudin](https://www.aanda.org/articles/aa/abs/2020/08/aa38192-20/aa38192-20.html) databases, as those with a catalogued distance of 9 Kpc or more.

Data from Gaia EDR3 was downloaded with a length of .3 deg for all the clusters.

> DM diameter (arcmin)
> A_OC, A_CG, A_WB: log(ages) for OPENCLUST, Cantat-Gaudin, and WEBDA,
> respectively
> D_OC, D_CG, D_WB: distances for OPENCLUST, Cantat-Gaudin, and WEBDA,
> respectively

```
Cluster      RA  DEC       Dm  A_OC  D_OC  A_CG D_CG  A_WB  D_WB  A_MW  D_MW
-----------------------------------------------------------------------------
Ber73        95.50  -6.35  2   9.18  9800  9.15 6158  9.36  6850  9.15  7881
Ber25        100.25 -16.52 5   9.7   11400 9.39 6780  9.6   11300 9.7   11400
Ber75        102.25 -24.00 4   9.6   9100  9.23 8304  9.48  9800  9.3   6273
Ber26        102.58 5.75   4   9.6   12589 --   --    9.6   4300  8.71  2724
Ber29        103.27 16.93  6   9.025 14871 9.49 12604 9.025 14871 9.1   10797
Tombaugh2    105.77 -20.82 3   9.01  6080  9.21 9316  9.01  13260 9.01  6565
Ber76        106.67 -11.73 5   9.18  12600 9.22 4746  9.18  12600 8.87  2360
FSR1212      106.94 -14.15 --  --    --    9.14 9682  --    --    8.65  1780
Saurer1      110.23 1.81   4   9.7   13200 --   --    9.85  13200 9.6   13719
Czernik30    112.83 -9.97  3   9.4   9120  9.46 6647  9.4   6200  9.2   6812
Arp-Madore2  114.69 -33.84 2   9.335 13341 9.48 11751 9.335 13341 9.335 13338
vdBH4        114.43 -36.07 2   --    --    --   --    8.3   19300 --    --
FSR1419      124.71 -47.79 --  --    --    9.21 11165 --    --    8.375 7746
vdBH37       128.95 -43.62 3   8.84  11220 8.24 4038  8.85  2500  7.5   5202
ESO09205     150.81 -64.75 5   9.3   5168  9.65 12444 9.78  10900 9.3   5168
ESO09218     153.74 -64.61 5   9.024 10607 9.46 9910  9.024 607   9.15  9548
Saurer3      160.35 -55.31 4   9.3   9550  --   --    9.45  8830  9.3   7075
Kronberger39 163.56 -61.74 .8 --     11100 --   --    --    --    6.    4372
Shorlin1¹    166.44 -61.23 .8 --     --    --   --    --    12600 6.5   5594
ESO09308     169.92 -65.22 1   9.74  14000 --   --    9.65  3700  9.8   13797
vdBH144      198.78 -65.92 1.5 8.9   12000 9.17 9649  8.9   12000  9    7241
vdBH176      234.85 -50.05 3   --    --    --   --    --    13400  9.8  18887
Kronberger31 295.05 26.26  1.3 --    11900 --   --    --    --     8.5  12617
Saurer6      297.76 32.24  1.8 9.29  9330  --   --    9.29  9330   9.2  7329
Ber56        319.43 41.83  3   9.6   12100 9.47 9516  9.6   12100  9.4  13180
FSR0338      327.93 55.33  2.7 8.1   14655 --   --    --    --     8.1  14655
Ber102       354.66 56.64  5   9.5   9638  9.59 10519 8.78  2600   9.14 4900
```
¹: *Not enough stars* flag in CG

The article [Dias et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021MNRAS.504..356D/abstract) lists the following clusters that are in the table above:

```
Name           Dist     log(age)
--------------------------------
Tombaugh2      8978        9.355
Ber73          5832        9.347
Czernik30      5938        9.475
vdBH37         3439        8.427
```

The [MWSC](https://heasarc.gsfc.nasa.gov/W3Browse/all/mwsc.html) catalogue lists the following clusters in the analyzed distance range:

```
name                distance    log_age   D_WB
----------------------------------------------
IRAS 02459+6029     12998       7.9        ---
BDSB 51             12002       8.15       ---
Kronberger 85       10380       8.5        ---
NGC 3105            10301       7.4       4884
Berkeley 1          10300       8.6       2420
vdBergh-Hagen 79    10270       8.4        nan
FSR 0378            10000       8.1        ---
MWSC 5076           9842        8.85       ---
vdBergh-Hagen 78    9763        8.6        nan
FSR 1694            9537        8.4        ---
Berkeley 91         9471        8.4       2400
```



## pyUPMASK

Processed all clusters with pyUPMASK+GMM, using only the proper motions as processing data.



## Members selection

The columns show the number of members estimated manually (`man`), and automatically by ASteCA (`auto`). The rest of the columns are the number of members selected by several runs of the `members_select` code:

* 1st: 'man' N_memb + EE + 0.95 (0.98 for eso09308); KRON39 manual (Glue)
* 2nd: 'auto' N_memb + EE + auto
* 3rd: 'auto' N_memb + 2DE + .9
* 4th: 'auto' N_memb + 3DE + .9

In all cases the radii were fixed.

We used the results from the `1st` run (a smaller but more pure sample was favored) for all clusters except BER29 and KRON39. For BER29 I used the `3rd` run because it uses a larger (more reasonable) radius than the `1st`. For KRON39 a manual selection of members (using Glue) was employed.

```
Cluster      man  auto 1st 2nd  3rd 4th      rad
------------------------------------------------
arpm2        200  315  200 315  198 283    0.050
ber26        120  151  79  109  66  81     0.027
ber29        320  359  243 359  218 315    0.050
ber56        900  1179 900 1179 729 1032   0.075
ber76        160  254  160 254  159 224    0.067
eso09308     220  204  65  204  104 149    0.025
saurer1      90   116  90  116  73  103    0.033
tombaugh2    1020 1036 907 1036 608 810    0.058
vdbh4        80   114  70  104  49  71     0.033
vdbh176      410  323  333 323  267 325    0.033
vdbh144      400  199  400 199  199 293    0.025
ber25        220  428  220 428  267 367    0.083
ber73        110  133  105 128  78  95     0.033
ber75        115  124  99  121  65  87     0.033
ber102       160  222  160 222  130 179    0.042
czernik30    120  168  120 168  119 160    0.042
eso09205     400  520  400 520  370 484    0.050
eso09218     950  807  823 807  602 807    0.050
fsr1212      100  171  100 171  98  130    0.050
fsr1419      150  223  150 223  174 223    0.050
kronberger31 150  223  150 223  223 232    0.033
kronberger39 MAN  153  80  153  153 162    0.033
saurer3      160  248  160 248  175 232    0.033
saurer6      180  116  153 266  166 228    0.033
vdbh37       90   149  90  149  98  133    0.033
```



## Extinction

The SFD maps give:

```
Ber73:        median=0.307, min=0.283, max=0.369
Ber25:        median=0.378, min=0.344, max=0.419
Ber75:        median=0.099, min=0.095, max=0.116
Ber26:        median=0.503, min=0.426, max=0.548
Ber29:        median=0.081, min=0.071, max=0.088
Tomb2:        median=0.341, min=0.298, max=0.419
Ber76:        median=0.600, min=0.496, max=0.720
FSR1212:      median=0.689, min=0.615, max=0.732
Saurer1:      median=0.146, min=0.124, max=0.174
Czernik30:    median=0.295, min=0.255, max=0.352
ArpM2:        median=0.627, min=0.533, max=0.834
vdBH4:        median=0.421, min=0.381, max=0.475
FSR1419:      median=0.683, min=0.630, max=0.757
vdBH37:       median=1.905, min=1.549, max=2.900
ESO09205:     median=0.180, min=0.165, max=0.208
ESO09218:     median=0.243, min=0.224, max=0.255
Saurer3:      median=0.822, min=0.654, max=1.028
Kronberger39: median=0.609, min=0.386, max=0.908
Shorlin1:     median=2.711, min=1.533, max=4.636
ESO09308:     median=0.785, min=0.707, max=0.930
vdBH144:      median=0.801, min=0.758, max=0.917
vdBH176:      median=0.537, min=0.490, max=0.630
Kronberger31: median=1.432, min=1.324, max=2.651
Saurer6:      median=1.158, min=1.079, max=1.360
Ber56:        median=0.542, min=0.485, max=0.806
FSR0338:      median=2.096, min=1.891, max=2.275
Ber102:       median=0.574, min=0.478, max=0.715
```



## ASteCA

```
R1   arpm2         min/max   8/max      0/.9    10/16 100/100000  0/1   3.1
R1   ber26         min/max   8/max      0/.6    10/16 100/100000  0/1   3.1
R1   ber73         min/max   8/max      0/.4    10/16 100/100000  0/1   3.1
R1   czernik30     min/max   8/max      0/.4    10/16 100/100000  0/1   3.1
R1   eso09308      min/max   8/max      0/1.    10/16 100/100000  0/1   3.1
R1   kronberger31  min/max   8/max      0/3     10/16 100/100000  0/1   3.1
R1   saurer3       min/max   8/max      0/1.2   10/16 100/100000  0/1   3.1
R1   vdbh144       min/max   8/max      0/1.    10/16 100/100000  0/1   3.1
R1   vdbh4         min/max   8/max      0/.5    10/16 100/100000  0/1   3.1
R1   ber102        min/max   8/max      0/.8    10/16 100/100000  0/1   3.1
R1   ber29         min/max   8/max      0/.15   10/16 100/100000  0/1   3.1
R1   ber75         min/max   8/max      0/.2    10/16 100/100000  0/1   3.1
R1   eso09205      min/max   8/max      0/.3    10/16 100/100000  0/1   3.1
R1   fsr1212       min/max   8/max      0/.8    10/16 100/100000  0/1   3.1
R1   kronberger39  min/max   8/max      0/1     10/16 100/100000  0/1   3.1
R1   saurer6       min/max   8/max      0/1.5   10/16 100/100000  0/1   3.1
R1   vdbh176       min/max   8/max      0/.7    10/16 100/200000  0/1   3.1
R1   ber25         min/max   8/max      0/.5    10/16 100/100000  0/1   3.1
R1   ber56         min/max   8/max      0/1.5   10/16 100/100000  0/1   3.1
R1   ber76         min/max   8/max      0/1.    10/16 100/100000  0/1   3.1
R1   eso09218      min/max   8/max      0/.3    10/16 100/100000  0/1   3.1
R1   fsr1419       min/max   8/max      0/.8    10/16 100/100000  0/1   3.1
R1   saurer1       min/max   8/max      0/.2    10/16 100/100000  0/1   3.1
R1   tombaugh2     min/max   8/max      0/.5    10/16 100/100000  0/1   3.1
R1   vdbh37        min/max   8/max      0/3.    10/16 100/100000  0/1   3.1
```

