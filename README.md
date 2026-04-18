# hydromind-contracts

HydroMind 契约与 schema 仓。

当前已覆盖：

- 基础 case / workflow / review / release contracts
- 调度与运行 contracts
- 平台运行态 contracts
- V5-W1 MBD 协议层 contracts：
  - `LifecyclePhase`
  - `ManagementLevel`
  - `RoleProfile`
  - `AgentNodeProfile`
  - `SessionMode`
  - `ModelDelivery`
  - `WorkflowReportSection`
- V5-W2-α 平台并发协同 contracts：
  - `AgentNetwork`
  - `TierMessage`

CLI:

- `hydromind-contracts list-contract-types`
- `hydromind-contracts validate <ContractType> <path>`
- `hydromind-contracts validate-contract <ContractType> <path>`
