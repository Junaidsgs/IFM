# Impression Forecast Model (IFM)

**Authors:** Junaid Ahmad ([ja4893@rit.edu](mailto:ja4893@rit.edu)), Fardin Anam Aungon ([fa4111@rit.edu](mailto:fa4111@rit.edu)), and Subash Velmurugan ([sv9252@g.rit.edu](mailto:sv9252@g.rit.edu))

## Problem Statement:

To develop a time-series regression model that predicts the number of downloads for an application on day T, given a feature vector X representing the preceding n days of historical data.

## Motivation:

For App developers having a model that can predict the future downloads is invaluable. It can help them make better decisions to improve their businesses.

Some use cases can be:
- **To optimize UA (User Acquisition) spend** to reach quarterly targets.
- **Outlier detection:** Developers can detect recent update performance on organic growth.
    - Increase downloads due to store listing updates.
    - Reduction in downloads due to increased crashes in a new update.

## Methodology

1. **Data Collection & Integration:** Collect all time-series data into a Google Sheet file.
2. **Preprocessing:** Determine the best way to preprocess the data (Handling missing dates, smoothing ratings, etc.).
   - See [Data Preprocessing Guide](resources/data_preprocessing.md).
3. **Data Splitting:** Split the data into training and test sets. **Note: Time-series data must be split by time, not randomly.**
4. **Baseline Modeling:** Run traditional regression algorithms to create the initial model.
5. **Advanced Modeling:** Research and implement subsequent models (LSTM, BiLSTM, etc.).
6. **State-of-the-Art Implementation:** Run the data through **Facebook’s Prophet** model.
7. **Evaluation:** Evaluate the results using time-series metrics (MAE, MSE, Huber Loss).

## Evaluation Plans:

We will evaluate each of the models we build and compare them with each other. Finally, we will cross-test each model to determine which works best for predicting application impressions.

---

## Github Link
https://github.com/Junaidsgs/IFM.git
