---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.validation
doc_type: action_validation_doc
topic: Mother doc validation
---

# mother_doc 阶段校验

- 当前轮 mother_doc 必须成为唯一需求源。
- `00_index.md` 必须从 folder 结构刷新。
- 当前轮结构变化完成后必须同步 client mirror。
- `mother-doc-lint` 必须通过后才能进入 `construction_plan`。
