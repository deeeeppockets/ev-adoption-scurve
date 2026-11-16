# EV Adoption S-Curves

**Bonus point project for Adv Math for B&T - VUB**

**Website:** TBU when live

## Question

Can a logistic S-curve forecast electric-car adoption, or does it only describe it after the fact?

The logistic model comes from the ODE:

$$\frac{dP}{dt} = rP\left(1 - \frac{P}{K}\right) \quad\Rightarrow\quad P(t) = \frac{K}{1 + e^{-r(t - t_0)}}$$

The symbols are:

- $P$ - is the EV share of new car sales (%).
- $K$ - is the saturation ceiling.
- $r$ - is the growth rate.
- $t_0$ - is the inflection year. At $t_0$, $P = K/2$ and adoption grows fastest ($P'' = 0$).

## Data

| File | Source | Coverage |
|------|--------|----------|
| `data/raw/electric-car-sales-share.csv` | [Our World in Data: Share of new cars sold that are electric](https://ourworldindata.org/grapher/electric-car-sales-share), based on the IEA Global EV Outlook | 64 countries and regions, 2010–2025 |

"Electric" means battery-electric plus plug-in hybrid cars. The committed CSV is a frozen copy, retrieved on 2026-11-03.

To re-download the data, run `python src/fetch_data.py`.

## Analyses

1. **Hindsight fit (the control).** Fit the logistic model and an exponential model to each country's full 2010–2025 series and compare them using RMSE and AIC. Then refit the logistic model on expanding data windows (ending 2015, 2016, … 2025) and track how the estimated ceiling $K$ converges. This checks that the model and the fitting code work when the whole curve is visible.
2. **Forecast test.** Fit the logistic model on data up to a cutoff year only, forecast the share a few years ahead, and compare with what actually happened. Benchmark against a naive forecast that extends the trend of the last three years in a straight line. Group every forecast by the market's adoption stage when it was made (years before or after its inflection year $t_0$), to test whether forecasting ability depends on stage.

## Main findings

*To be added after the analyses are complete.*

## Limitations

The logistic model is a simplification. Its weaknesses are part of what this project seeks to measure.

- **Fixed ceiling.** $K$ is assumed constant. In reality the saturation level moves with policy, prices, charging infrastructure and model availability.
- **Symmetric curve.** The logistic curve rises and flattens symmetrically around $t_0$. Real adoption can accelerate fast and plateau slowly, or the reverse.
- **No external drivers.** Subsidies, tax changes and emissions rules do not appear in the model. When policy shifts, for example Europe's 2020 jump under the EU CO₂ targets or Germany's incentive cuts in 2022–2023, the model mistakes the effect for a change in the curve itself.
- **Identifiability before the inflection.** The early part of an S-curve looks almost exponential, so many combinations of $(K, r, t_0)$ fit it about equally well. The ceiling $K$ cannot be pinned down until the data passes $P = K/2$.
- **Small sample.** Each country has at most 16 annual points to estimate 3 parameters, and most early points are close to zero and carry little information.
- **Measurement.** The data pools battery-electric and plug-in hybrid cars, whose relative shares change over time. It measures the share of new sales, not the share of cars on the road, and the IEA revises figures between releases.
- **Aggregation.** National and world figures combine markets that are at very different stages of adoption.

## Repository structure

```
data/raw/      source data (frozen copy)
src/           Python scripts
figures/       exported figures (PDF)
docs/          website source (GitHub Pages)
```

## Reproduce

```bash
pip install -r requirements.txt
python src/fetch_data.py   # optional: refresh the data
```
