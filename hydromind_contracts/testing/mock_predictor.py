"""Mock predictor implementing PredictorProtocol for testing."""

from __future__ import annotations


class MockPredictor:
    """A trivial predictor that satisfies :class:`PredictorProtocol`.

    Returns constant or linearly extrapolated forecasts for testing.
    """

    def __init__(self) -> None:
        self._last_data: dict = {}

    def predict(self, data: dict, horizon: float) -> dict:
        """Generate a mock prediction returning constant values."""
        self._last_data = dict(data)
        n_steps = max(1, int(horizon))
        last_value = data.get("last_value", 0.0)
        return {
            "forecast": [last_value] * n_steps,
            "confidence": [0.9] * n_steps,
            "metadata": {"model": "mock", "horizon": horizon},
        }
