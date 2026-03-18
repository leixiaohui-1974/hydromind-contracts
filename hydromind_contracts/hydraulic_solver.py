"""Hydraulic solver protocol contracts for HydroMind.

定义统一水力学求解器接口协议，所有渠道/管网求解器均应实现此协议。
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class HydraulicSolverProtocol(Protocol):
    """统一水力学求解器接口协议。

    所有求解器（Tank ODE, Kinematic Wave, Diffusion Wave,
    Lax-Wendroff, MacCormack, Godunov-HLL, TVD-MUSCL,
    Preissmann, SWMM, PINN等）均实现此协议。

    Attributes:
        name: 求解器名称，如 "LaxWendroff", "GodunovHLL"。
        order: 精度阶数，如 "1st", "2nd"。
        scheme: 数值格式描述，如 "explicit finite-difference"。
    """

    name: str
    order: str
    scheme: str

    def initialize(self, h0: float, Q0: float | None = None) -> None:
        """初始化求解器状态（均匀流初始条件）。

        Args:
            h0: 初始水深 (m)。
            Q0: 初始流量 (m³/s)，为 None 时由 Manning 公式推算。
        """
        ...

    def advance(
        self, dt: float, Q_upstream: float, h_downstream: float | None = None
    ) -> None:
        """推进一个时间步。

        Args:
            dt: 时间步长 (s)。
            Q_upstream: 上游入流量 (m³/s)。
            h_downstream: 下游水深边界 (m)，为 None 时使用自由出流。
        """
        ...

    def get_h_profile(self) -> Any:
        """返回当前水深空间分布。

        Returns:
            形状为 (n_nodes,) 的数组，单位 m。
        """
        ...

    def get_state(self) -> dict[str, Any]:
        """返回完整状态。

        Returns:
            至少包含 ``t`` (当前时刻), ``h`` (水深数组),
            ``x`` (空间坐标数组) 的字典。
        """
        ...


@runtime_checkable
class ChannelConfigProtocol(Protocol):
    """渠道配置协议，支持 YAML 序列化。

    Attributes:
        length: 渠道长度 (m)。
        width: 断面宽度 (m)。
        slope: 底坡 (-)。
        manning_n: Manning 糙率系数。
        n_nodes: 空间离散节点数。
    """

    length: float
    width: float
    slope: float
    manning_n: float
    n_nodes: int
