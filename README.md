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
