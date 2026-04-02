# Program Contracts Index

这个文件给 `HydroMind` 项目群里的“Case / Data Pack / Run / Review / Release”对象一个统一入口。

它回答 3 个问题：

1. 哪些对象已经稳定进入 `hydromind-contracts`
2. 代码入口和校验入口分别在哪
3. 其他 repo 应该如何消费这些对象

## Current Contract Set

第一批 program contracts 已经进入：

- [program_contracts.py](/Users/rainfields/hydrosis-local/research/hydromind-contracts/hydromind_contracts/program_contracts.py)

包含对象：

- `ArtifactRef`
- `SourceRecord`
- `CaseManifest`
- `SourceBundle`
- `DataPack`
- `WorkflowStepRun`
- `WorkflowRun`
- `ReviewFinding`
- `ReviewBundle`
- `ReleaseManifest`

统一 schema 版本常量：

- `PROGRAM_SCHEMA_VERSION`

稳定导入入口：

- [contract_index.py](/Users/rainfields/hydrosis-local/research/hydromind-contracts/hydromind_contracts/contract_index.py)

## Validation Entry

基础校验入口：

- [program_validation.py](/Users/rainfields/hydrosis-local/research/hydromind-contracts/hydromind_contracts/program_validation.py)

当前提供两类能力：

- 直接校验对象
  - `validate_case_manifest`
  - `validate_source_bundle`
  - `validate_data_pack`
  - `validate_workflow_run`
  - `validate_review_bundle`
  - `validate_release_manifest`
  - `validate_program_contract`

- 从 `dict` 加载并校验
  - `load_and_validate_case_manifest`
  - `load_and_validate_source_bundle`
  - `load_and_validate_data_pack`
  - `load_and_validate_workflow_run`
  - `load_and_validate_review_bundle`
  - `load_and_validate_release_manifest`

- 直接失败的 assert 入口
  - `assert_valid_case_manifest`
  - `assert_valid_source_bundle`
  - `assert_valid_data_pack`
  - `assert_valid_workflow_run`
  - `assert_valid_review_bundle`
  - `assert_valid_release_manifest`

## Consumption Pattern

推荐其他 repo 按这个顺序消费：

1. 从 JSON / YAML 读取 `dict`
2. 调用 `load_and_validate_*`
3. 若 `errors` 非空，先失败并回显
4. 通过后再入库、执行 workflow 或生成 report

最小示例：

```python
from hydromind_contracts import load_and_validate_source_bundle

bundle, errors = load_and_validate_source_bundle(payload)
if errors:
    raise ValueError(errors)
```

## Repo Mapping

### `pipedream-hydrology-integration-lab`

当前已开始消费这些对象：

- `kb_pipeline` 可导入 `SourceBundle / ReviewBundle / ReleaseManifest`

### `Hydrology`

当前可直接消费：

- `CaseManifest / DataPack / WorkflowRun / ReviewBundle / ReleaseManifest`

下一步仍应继续接入：

- workflow spec 输入输出对象
- run / review / release 结果对象

### `research/cases/*`

案例入口应逐步和 `CaseManifest` 对齐。

## Rule

如果某个对象：

- 需要跨 repo 交换
- 需要跨会话持续存在
- 需要被 agent 和 CLI 共同理解

它就应该优先落成这里的 contract，而不是散落在某个 repo 的私有 JSON 里。

---
status: active  
scope: program  
source_of_truth: yes
