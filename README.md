# On the Use of Quantile Regression Forests for Sub-seasonal Rainfall Forecasting over India

Research code accompanying the manuscript **“On the Use of Quantile Regression Forests for Sub-seasonal Rainfall Forecasting over India.”** The study evaluates Quantile Regression Forest (QRF) calibration of GEFSv12 sub-seasonal Indian summer monsoon rainfall forecasts and compares it with Extended Logistic Regression (ELR).

## Authors

Bohar Singh, Abhik Biswas, Andrew W. Robertson, Muhammad Azhar Ehsan, Aaron Kaplan, Avijit Dey, and Susmitha Joseph.

## Repository contents

- `QRF/` — QRF probability generation, tercile export, plotting utilities, and tuned parameters.
- `QRF/Hyperparameter_training/` — grid-point experiments and hyperparameter-tuning notebooks.
- `ELR/` — baseline ELR calibration notebook.
- `Verification/` — RPS/RPSS, GROC, ignorance-score, reliability, and forecast-figure notebooks.
- `shapes/` — geographic boundary files used for maps.
- `environment-qrf.yml` — captured QRF/scikit-garden environment (Python 3.7; macOS Intel build).
- `environment-xcast.yml` — captured analysis and verification environment (Python 3.12; macOS Apple Silicon build).

## Data

The large forecast, reforecast, and observation datasets are not redistributed in this repository. The analysis uses:

- GEFSv12 forecasts and 1989–2019 reforecasts accessed through the IRI Data Library and SubC database.
- Indian Meteorological Department (IMD) and merged TRMM–IMD precipitation observations.
- Independent test seasons from June–September 2022–2024.

Users must obtain access to the source datasets under their respective terms and update the local paths in the notebooks. Some notebooks retain machine-specific absolute paths from the original analysis; search for `/Users/` before running them on another system.

## Environment setup

The project preserves two historical Conda environments because QRF model fitting and the later verification workflow were developed with different Python stacks.

For QRF model fitting:

```bash
conda env create -f environment-qrf.yml
conda activate skgarden
```

For verification and plotting:

```bash
conda env create -f environment-xcast.yml
conda activate xcast_env
```

The QRF environment depends on the legacy `scikit-garden` package. ELR notebooks also import the research module `elr_c`, which is not distributed here; those notebooks require that module to be supplied separately. The environment files capture the original macOS builds and may need platform-specific adjustments on Linux or Windows.

## Suggested workflow

1. Obtain and preprocess the GEFSv12 and observational data.
2. Run the notebooks in `QRF/Hyperparameter_training/` to reproduce parameter selection.
3. Generate calibrated tercile probabilities with `QRF/Terciles Export.ipynb`.
4. Generate the ELR baseline with `ELR/ELR.ipynb` when `elr_c` is available.
5. Run the notebooks in `Verification/` to reproduce the skill analyses and publication figures.

The notebooks are research workflows rather than a packaged command-line application. They should be reviewed and their paths/configuration adapted before execution.

## Citation

Please cite the archived software release using the metadata in [`CITATION.cff`](CITATION.cff). A version-specific DOI will be provided through Zenodo with the first GitHub release.

## License

See [`LICENSE`](LICENSE) for reuse terms.
