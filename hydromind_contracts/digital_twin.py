"""Digital twin protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class DigitalTwinProtocol(Protocol):
    """Contract for digital twin synchronization and prediction.

    A digital twin maintains a virtual replica of a physical water system,
    continuously synchronized with real-world observations. It supports
    forward prediction and discrepancy analysis.
    """

    def sync(self, real_state: dict) -> dict:
        """Synchronize the twin with the latest real-world state.

        Args:
            real_state: Observed state from sensors / SCADA.

        Returns:
            Dictionary containing:
                - ``synced`` (bool): Whether synchronization succeeded.
                - ``drift`` (float): State drift magnitude before sync.
                - ``timestamp`` (str): Sync timestamp.
        """
        ...

    def predict(self, duration: float) -> dict:
        """Run a forward prediction from the current twin state.

        Args:
            duration: Prediction horizon in seconds.

        Returns:
            Dictionary containing:
                - ``states`` (list): Predicted state snapshots.
                - ``horizon`` (float): Actual horizon covered.
                - ``confidence`` (float): Prediction confidence.
        """
        ...

    def get_discrepancy(self) -> dict:
        """Report the discrepancy between twin and real system.

        Returns:
            Dictionary containing:
                - ``variables`` (dict): Per-variable discrepancy values.
                - ``overall`` (float): Aggregate discrepancy metric.
                - ``timestamp`` (str): When the comparison was made.
        """
        ...
