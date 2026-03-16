#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SHARED_SCRIPTS = SKILL_ROOT.parents[0] / "_shared" / "octopus_os_workflow_runtime" / "scripts"

os.environ["OCTOPUS_WORKFLOW_ACTIVE_SKILL_ROOT"] = str(SKILL_ROOT)
os.environ["OCTOPUS_WORKFLOW_ACTIVE_SKILL_NAME"] = "Workflow-ConstructionPlan-OctopusOS"
os.environ["OCTOPUS_WORKFLOW_ACTIVE_STAGE"] = "construction_plan"
sys.path.insert(0, str(SHARED_SCRIPTS))

from cli_entry import main


if __name__ == "__main__":
    raise SystemExit(main())
