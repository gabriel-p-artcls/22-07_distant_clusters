Referee Report

The manuscript by Perren et al. presents an interesting reanalysis of the most
distant known open clusters in the Milky Way. The authors use the recent Gaia
EDR3 data for those objects to demonstrate the strengths and the limitations of
their open-source cluster analysis code ASteCA, and to evaluate how
(un-)reliable previous estimates of stellar parameters are, especially for
objects beyond the Gaia parallax sphere. The assumptions of the paper are
spelled out clearly and the analysis is easily reproducible (I have been able
to successfully test the ASteCA code for some examples). I congratulate the
authors: the code is well documented, understandable, and produces
self-explanatory plots.

The methods are generally described in sufficient detail (taking into account
the previous publications of the authors). I do, however, have a number of
questions / suggestions, mostly rearding the interpretation, that I detail
below. In general, the new results are highlighted enough, and the selection of
figures (except probably for Figs. 8 & 9) and tables is plausible. In some
aspects I find the interpretation of the results to be slightly too naïve, and
therefore some conclusions a bit rash. This is my major concern with the paper
in its present state. Sect. 4.2 could possibly be an Appendix (à la "Notes on
individual objects"), but this is up to the taste of the authors. Tables 1, 2,
3 could be made available jointly as a machine-readable table too. The
designation of objects is, as far as I can see, according to IAU standards.




0. Since this is discussed already in the Abstract: I find the large distance
and age spreads found in the literature not very surprising, given the quality
of the pre-Gaia data and the diversity of methods used. And, perhaps most
importantly, CMD fitting techniques allow us to determine distance *modulus*
and *log* age, so looking at differences in linear distance scale will of
course result in huge differences for the most distant objects... In that
sense, the author might opt for being a bit more careful not to overinterpret
these differences. For example, I find the comparison to Cantat-Gaudin+2020
very reassuring, actually - the level of concordance is very much in line with
the uncertainties given by those authors. That paper was based on DR2, while
the present study uses EDR3 - together with the much more accurate & precise
parallax calibration of Lindegren+2021. Perhaps a bit more emphasis should be
given to the fact that only with Gaia it has become much easier to determine
meaningful parameters...

1. The most fundamental methodological question I have with regard to the paper
(and perhaps this is answered somewhere in the previous papers?) is why and how
exactly the authors use pyUPMASK in conjunction with ASteCA. If I am not
mistaken the reason seems to be that the membership algorithm implemented in
ASteCA is not the most reliable? If this is correct, then how is the output of
pyUPMASK used as an input for ASteCA? Do you somehow run ASteCA without running
the membership algorithm part of ASteCA (i.e. do you go straight to the final
part of the ASteCA algorithm or does the pyUPMASK membership list pass the
additional filter of ASteCA)? This could be made a bit more clear in the text,
in my opinion.

2. The second question I have concerns the binary fractions delivered by ASteCA.
Binary fractions higher than 50% have, to the best of my knowledge, not been
reported in Galactic open clusters. Table 2, however, suggests that this is
rather the rule than the exception if we believe the results delivered by
ASteCA. Unless the authors can convince me otherwise, I think these results are
largely unphysical and the authors should regard the binary fraction more as a
nuisance parameter than as a meaningfully derived variable for the moment. The
text is not sufficiently clear on this matter: rather, the binary fractions
seem to be taken at face value without a critical analysis. I should highlight,
however, that I highly value the authors' approach, and that taking into
account binarity in their analysis potentially greatly improves the results for
ages, metallicity, and distance, as convincingly explained on page 7. My
feeling is that the overestimated binary fractions are mostly due to problems
with modelling Gaia photometric errors, especially at the faint end? Can the
authors remind me how they are taken into account? An additional complication
is of course differential extinction, and (probably a secondary effect), the
variation of the extinction law. I have seen that within ASteCA there seems to
be an option under development that allows to account for differential
extinction. If I read the code correctly, then any differential extinction
(either within the cluster or in the foreground) is absorbed in the binary
fraction right now. Maybe the authors can comment on this point explicitly,
thus cautioning the reader from using the values in Table 2 without a second
thought.

3. With respect to the metallicities delivered by ASteCA, I think one can argue
that the data presented by the authors show that the output values are mostly
inconclusive - if not meaningless. The metallicities of the quoted literature
in Table 3 are derived from (typically high-res.) spectroscopy and therefore
established to +-0.05-0.1 dex. I wonder if the ASteCA fits would improve if
instead of leaving metallicity free you would consider the spectroscopic
measurements as an additional input? (in the absence of spectroscopic
measurements you could also use the metallicity gradient +- some reasonable
scatter as a prior). Right now, the uniform prior in z translates to a
non-uniform prior in [M/H] - one that prefers higher metallicities... Leaving
too many free parameters without any priors might lead to solutions in
unphysical parameter regions (this is clearly visible for metallicity & binary
fraction, but might affect also age and extinction to some degree). For
example, Saurer 1 cannot be of super-solar metallicity. There already exist
spectroscopic studies confirming its low metallicity... It is not as if the
cluster "was assigned" a low metallicity - it has been measured with very small
error bars derived from high-resolution spectroscopy - several times! At the
very least, obviously erroneous solutions like this should be critically
discussed without relativising statements like "This can be the reason for the
large metallicity given by ASteCA, although a spectroscopic metallicity study
with more confirmed members would be ideal to provide a more accurate
estimate." Here readers with a spectroscopic background are likely to become
slightly annoyed. It sounds a bit like you are questioning the reliability of
past spectroscopic studies.. The given alternative explanation ("less than a
full magnitude visible below the TO with a total of only 84 members present in
the CMD") is much more than convincing to me. In the same respect, I think
Figs. 8 & 9 are hardly telling anything about Galactic history, but rather
about the poor quality of many of the derived metallicities (which is of course
expected - this is exactly the reason of spectroscopic open-cluster surveys).

Minor comments:

Introduction:
- "The intrinsic value of studying OCs has been profusely de- scribed in several
   opportunities and we are not going to repeat them here. However a brief
   enumeration ..." ---> This is contradictory:) Just delete the 2 sentences?
- It is not clear to me what Hayes+2015 tell us about cluster destruction? There
  are more meaningful theoretical and observational studies... e.g.
  Lamers+2005, Piskunov+2006
- "Young OCs are mainly arranged along the Galactic disk" is quite an
   understatement. Their scale height is <<50 pc...
- " Stars in the lower part of their sequences" --> their main sequences?
- "it is not only the photometric space that is disturbed by distance" -->
   sounds a bit strange

Sect 2
- "hereinafter" --> hereafter
- "The method employed by the authors of the MWSC catalog is a semi-automated
 isochrone fit, while the CG20 catalog was generated employing an artificial
 neural network (trained on parameter values taken from the literature)."
---> The largest difference between the 2 catalogues is that MWSC contains loads
of *candidate* clusters (where most of the spurious ones come from the
candidate catalogue of FSR2007), while CG+2020 only includes clusters
verified undoubtedly by Gaia (see Cantat-Gaudin & Anders 2020 for a long
discussion).
- Is there any particular reason for using the Momany+2006 spiral arm model?
There are some more recent alternatives, e.g. Reid+2019 or  Castro-Ginard+2021 
(based on clusters)


Sect 3
- I find Fig 1 a bit too cluttered. Instead of telling a story, it is confusing
the story. The point of the plot is to show the different distributions of
the distant clusters when different catalogues are used. So why not make a
big plot showing the X-Y distribution obtained from ASteCA and 4 smaller
panels showing the same for the 4 other catalogues? Or, if you want to
maintain Fig. 7 as is, only show the 4 XY subpanels? Things are made all the
more confusing because the symbols are not consistent between Fig. 1 & 5..
and the same symbols reappear with other meanings in Fig. 6..
- " The selected clustering method in pyUPMASK was a Gaussian Mixture Model,
which demonstrated to have the best performance in Pera et al.(2021, see
Sect. 4)." --> This sounds slightly at odds with the findings of Hunt &
Reffert (2020)?
- "Using a physically reasonable number of members not only reduces the
probability of excluding true members (by only selecting those with the
largest membership probabilities), it also ensures that the estimation of
the total mass parameter is properly performed by ASteCA." --> Here I am a
bit lost. Isn't ASteCA cutting all members outside r_a? (up to 20% of the
members) - And then you are recompensating for this loss by allowing for
less probable members within r_a?
- It makes sense to have uniform priors in log age, EBV, and distance modulus,
but wouldn't it also be natural to have uniform priors in log Z (i.e.
[M/H]) and log Mass, instead of z & mass?


Sect 4
- " This is however a lower limit estimate since ASteCA does not take into
account the experienced dynamical mass loss, which can be significant for
old stellar clusters (Martinez-Medina et al. 2017)." --> this is rather
obvious. Or do you mean the mass still contained within the tidal radius
(or even the tails), but outside r_a?
- "Even the CG20 database, the one with the better overall match to our values,
shows differences larger than 2 kpc for clusters located at a distance
of &#8764; 10 kpc from the Sun. It is thus clear that even the database with
the closest fit contains substantial disagreements with the distance values
estimated by ASteCA." --> If you take into account the uncertainties, things
are actually matching well! (see point 0 above)
- "As can be seen in the bottom plot of Fig. 5, there appears to be a
correlation between the difference in age estimates and the binarity
fraction estimated." --> This correlation is not very clear to me. Also:
which one is the dominant factor: age or bf?
- "This result points to the importance of taking binary systems into account
when performing stellar clusters’ parameters estimations." --> I agree that
this is important, but I think the uniform prior for f_b is not a good
idea - it is clearly unphysical. The authors themselves admit that "0.3 is
usually chosen to be a reasonable estimate for open clusters (Sollima et
al. 2010)." So why not make use of this prior knowledge and consider a broad
Gaussian prior? 0.3+-0.2 or something like that? As is, I am much more
inclined to trust the red triangles in Fig. 6 than the nominal ASteCA
values...

4.2
- BH 176 is clearly one of the most interesting among the studied objects. Its
ASteCA values look very reasonable - and especially the distance is quite
precise... So why not mention some of your results for this object in the
abstract? because as you say it "could be the most remote open cluster found
to date"!

4.3
- Compared to the previous sections, I find this to be considerably less
convincing, especially due to the large photometric metallicity
uncertainties (see main point above)

Conclusions:
- The disc orbits of Berkeley 29 and Saurer 1 are extensively discussed in Gaia
  Collaboration et al. (2021)
- The spatial distribution of outer-disc clusters is also nicely reviewed in
  Cantat-Gaudin (2022)
