# hydromind-contracts

Interface contracts for the HydroMind water network intelligence platform.

## Install

```bash
pip install hydromind-contracts
```

For development:

```bash
pip install -e ".[test]"
pytest
```

For reproducible CI and local test environments:

```bash
pip install -r requirements-test.txt
pip install -e .
pytest
```

To refresh the lockfile after changing test dependencies:

```bash
python -m pip install pip-tools
pip-compile requirements-test.in --output-file requirements-test.txt
```

## Usage

```python
from hydromind_contracts import SimulatorProtocol, ControllerProtocol

# Check that your class implements the protocol
class MySimulator:
    def simulate(self, params, duration, dt): ...
    def get_state(self): ...
    def set_boundary(self, conditions): ...

assert isinstance(MySimulator(), SimulatorProtocol)
```

## License

MIT
