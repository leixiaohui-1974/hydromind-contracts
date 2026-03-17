"""Prediction protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class PredictorProtocol(Protocol):
    """Contract for prediction / forecasting engines.

    Implementations produce forecasts of water levels, flows, demand,
    rainfall, or other hydrological variables over a specified horizon.
    """

    def predict(self, data: dict, horizon: float) -> dict:
        """Generate a prediction.

        Args:
            data: Historical or real-time observations used as input.
            horizon: Forecast horizon in seconds (or time-step count,
                depending on implementation convention).

        Returns:
            Dictionary containing:
                - ``forecast`` (list): Predicted values over the horizon.
                - ``confidence`` (list | float): Confidence or uncertainty.
                - ``metadata`` (dict): Any extra information (model version,
                  feature importance, etc.).
        """
        ...
