"""System identification protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class IdentifierProtocol(Protocol):
    """Contract for system identification / parameter estimation.

    Implementations calibrate model parameters from observed data using
    techniques such as least-squares, Bayesian inference, or machine learning.
    """

    def identify(self, data: dict, method: str) -> dict:
        """Identify (calibrate) model parameters.

        Args:
            data: Observed input-output data for calibration.
            method: Identification method name (e.g. ``"least_squares"``,
                ``"bayesian"``, ``"neural"``).

        Returns:
            Dictionary containing:
                - ``parameters`` (dict): Estimated parameter values.
                - ``fitness`` (float): Goodness-of-fit metric.
                - ``metadata`` (dict): Convergence info, uncertainty bounds.
        """
        ...

    def validate(self, model: dict, test_data: dict) -> dict:
        """Validate an identified model against independent test data.

        Args:
            model: Model specification including identified parameters.
            test_data: Independent dataset not used during identification.

        Returns:
            Dictionary containing:
                - ``metrics`` (dict): Validation metrics (NSE, RMSE, etc.).
                - ``predictions`` (list): Model predictions on test data.
                - ``passed`` (bool): Whether validation criteria are met.
        """
        ...
