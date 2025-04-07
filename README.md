# [pnet](https://github.com/MLDataAnalytics/pNet)

---

![logo](https://github.com/DouHuanHuan/pnet/blob/master/pNet/docs/png/pnet.png)

pNet is a Python package of an [algorithm](<https://pubmed.ncbi.nlm.nih.gov/28483721>) for computing personalized,
sparse, non-negative large-scale functional networks from functional magnetic resonance imaging (fMRI) data,
facilitating effective characterization of individual variation
in [functional topography](<https://pubmed.ncbi.nlm.nih.gov/32078800>). The personalized functional networks are
***comparable across subjects*** while maintaining ***subject specific variation***, reflected by their
***improved functional coherence*** compared with their group-level counterparts. The computation of personalized
functional networks is accompanied by [quality control](https://pubmed.ncbi.nlm.nih.gov/36706636), with visualization
and quantification of their spatial correspondence and functional coherence in reference to their group-level
counterparts.

The [algorithm](<https://pubmed.ncbi.nlm.nih.gov/28483721>) has been successfully applied to studies
of [individual variation in functional topography of association networks in youth](<https://pubmed.ncbi.nlm.nih.gov/32078800>), [functional network topography of psychopathology in youth](<https://pubmed.ncbi.nlm.nih.gov/35927072>), [sex differences in the functional topography of association networks in youth](<https://pubmed.ncbi.nlm.nih.gov/35939696>) (
replicated
in [Reproducible Sex Differences in Personalized Functional Network Topography in Youth](<https://www.biorxiv.org/content/10.1101/2024.09.26.615061v1>)), [dissociable multi-scale patterns of development in personalized brain networks](<https://pubmed.ncbi.nlm.nih.gov/35551181>), [multiscale functional connectivity patterns of the aging brain](<https://pubmed.ncbi.nlm.nih.gov/36731813>), [personalized functional brain network topography in youth cognition](<https://pubmed.ncbi.nlm.nih.gov/38110396>),
and [Polygenic Risk Underlies Youth Psychopathology and Personalized Functional Brain Network Topography](<https://www.medrxiv.org/content/10.1101/2024.09.20.24314007v2>).

![pnet_image](https://github.com/user-attachments/assets/25809dc1-7757-48d0-8d69-c6a23164941b)

## Getting started

Follow the Installation Instructions to install pNet, and then check out
the [APIs](https://pnet.readthedocs.io/en/latest/api.html)
and [Examples]( https://github.com/MLDataAnalytics/pNet/tree/main/src/pnet/examples) to learn how to get up and running!
For visualization issues that might be caused by VTK, please
check [TrobubleShooting](https://github.com/MLDataAnalytics/pNet?tab=readme-ov-file#troubleshooting).

### Prepare

create and active conda environment

```shell
conda create pnet
conda active pnet
```

install requirements

```shell
pip install -r requirements.txt
```

## Run on standalone mode

```shell
```

## Run on  server mode

First run the backend server in the pserver directory

```shell
python manage.py runserver
```

Then run the front server in the pfront directory

```shell
npm install && npm run
```

```
pip install --extra-index-url https://wheels.vtk.org vtk-osmesa
```

# License

Copyright (c) 2025

This project is licensed under the MIT License - see the [LICENSE](https://mit-license.org/) file for details.

# Contact us

If you want to report a bug or just provide us with a suggestion,
please contact us by the following email


