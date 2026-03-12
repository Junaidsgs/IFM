import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset


def create_sequences(data_x, data_y, window=7):
    """Build sliding-window sequences for time-series modeling."""
    X, y = [], []
    for i in range(len(data_x) - window):
        X.append(data_x[i : i + window])
        y.append(data_y[i + window])
    return torch.tensor(np.array(X), dtype=torch.float32), torch.tensor(
        np.array(y), dtype=torch.float32
    )


def preprocess_time_series(
    df,
    features,
    target_col,
    window_size=30,
    train_ratio=0.8,
    batch_size=32,
):
    """Run temporal split, scaling, sequence creation, and DataLoader setup."""
    train_size = int(len(df) * train_ratio)
    train_df = df.iloc[:train_size]
    test_df = df.iloc[train_size:]

    scaler_x = StandardScaler()
    scaler_y = StandardScaler()

    train_x_scaled = scaler_x.fit_transform(train_df[features])
    train_y_scaled = scaler_y.fit_transform(train_df[[target_col]])

    test_x_scaled = scaler_x.transform(test_df[features])
    test_y_scaled = scaler_y.transform(test_df[[target_col]])

    X_train, y_train = create_sequences(train_x_scaled, train_y_scaled, window_size)
    X_test, y_test = create_sequences(test_x_scaled, test_y_scaled, window_size)

    train_loader = DataLoader(
        TensorDataset(X_train, y_train), batch_size=batch_size, shuffle=False
    )

    return {
        "train_size": train_size,
        "train_df": train_df,
        "test_df": test_df,
        "scaler_x": scaler_x,
        "scaler_y": scaler_y,
        "train_x_scaled": train_x_scaled,
        "train_y_scaled": train_y_scaled,
        "test_x_scaled": test_x_scaled,
        "test_y_scaled": test_y_scaled,
        "X_train": X_train,
        "y_train": y_train,
        "X_test": X_test,
        "y_test": y_test,
        "train_loader": train_loader,
    }
