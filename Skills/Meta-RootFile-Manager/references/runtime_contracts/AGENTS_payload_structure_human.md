---
doc_id: meta_rootfile_manager.references_runtime_contracts_agents_payload_structure
doc_type: topic_atom
topic: AGENTS_payload_structure
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# AGENTS_payload_structure

Human mirror for `AGENTS_payload_structure.json`.

```json
{
  "version": 1,
  "targets": {
    "AGENTS.md": {
      "type": "object",
      "key_order": [
        "owner",
        "entry_role",
        "runtime_source_policy",
        "default_meta_skill_order",
        "turn_start_actions",
        "runtime_constraints",
        "execution_modes",
        "repo_local_contract_handoff",
        "forbidden_primary_runtime_pattern",
        "turn_end_actions"
      ],
      "properties": {
        "owner": {
          "type": "string"
        },
        "entry_role": {
          "type": "string"
        },
        "runtime_source_policy": {
          "type": "object",
          "key_order": [
            "runtime_rule_source",
            "audit_fields_are_not_primary_runtime_instructions",
            "path_metadata_is_not_action_guidance"
          ],
          "properties": {
            "runtime_rule_source": {
              "type": "string"
            },
            "audit_fields_are_not_primary_runtime_instructions": {
              "type": "boolean"
            },
            "path_metadata_is_not_action_guidance": {
              "type": "boolean"
            }
          }
        },
        "default_meta_skill_order": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "turn_start_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "runtime_constraints": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "execution_modes": {
          "type": "object",
          "key_order": [
            "READ_EXEC",
            "WRITE_EXEC"
          ],
          "properties": {
            "READ_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            },
            "WRITE_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "repo_local_contract_handoff": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "forbidden_primary_runtime_pattern": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "turn_end_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "Otctopus_OS_AgentConsole/AGENTS.md": {
      "type": "object",
      "key_order": [
        "owner",
        "entry_role",
        "runtime_source_policy",
        "default_meta_skill_order",
        "peer_summary_policy",
        "skills_required_techstacks",
        "turn_start_actions",
        "runtime_constraints",
        "execution_modes",
        "forbidden_primary_runtime_pattern",
        "turn_end_actions",
        "repo_name"
      ],
      "properties": {
        "owner": {
          "type": "string"
        },
        "entry_role": {
          "type": "string"
        },
        "runtime_source_policy": {
          "type": "object",
          "key_order": [
            "runtime_rule_source",
            "audit_fields_are_not_primary_runtime_instructions",
            "path_metadata_is_not_action_guidance"
          ],
          "properties": {
            "runtime_rule_source": {
              "type": "string"
            },
            "audit_fields_are_not_primary_runtime_instructions": {
              "type": "boolean"
            },
            "path_metadata_is_not_action_guidance": {
              "type": "boolean"
            }
          }
        },
        "default_meta_skill_order": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "peer_summary_policy": {
          "type": "object",
          "key_order": [
            "available",
            "relation",
            "read_policy",
            "guidance"
          ],
          "properties": {
            "available": {
              "type": "boolean"
            },
            "relation": {
              "type": "string"
            },
            "read_policy": {
              "type": "string"
            },
            "guidance": {
              "type": "string"
            }
          }
        },
        "skills_required_techstacks": {
          "type": "object",
          "key_order": [
            "python_backend",
            "vue3_typescript_frontend"
          ],
          "properties": {
            "python_backend": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "vue3_typescript_frontend": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          }
        },
        "turn_start_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "runtime_constraints": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "execution_modes": {
          "type": "object",
          "key_order": [
            "READ_EXEC",
            "WRITE_EXEC"
          ],
          "properties": {
            "READ_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            },
            "WRITE_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "forbidden_primary_runtime_pattern": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "turn_end_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "repo_name": {
          "type": "string"
        }
      }
    },
    "Octopus_OS/AGENTS.md": {
      "type": "object",
      "key_order": [
        "owner",
        "entry_role",
        "runtime_source_policy",
        "default_meta_skill_order",
        "turn_start_actions",
        "runtime_constraints",
        "execution_modes",
        "repo_local_contract_handoff",
        "forbidden_primary_runtime_pattern",
        "turn_end_actions",
        "repo_name"
      ],
      "properties": {
        "owner": {
          "type": "string"
        },
        "entry_role": {
          "type": "string"
        },
        "runtime_source_policy": {
          "type": "object",
          "key_order": [
            "runtime_rule_source",
            "audit_fields_are_not_primary_runtime_instructions",
            "path_metadata_is_not_action_guidance"
          ],
          "properties": {
            "runtime_rule_source": {
              "type": "string"
            },
            "audit_fields_are_not_primary_runtime_instructions": {
              "type": "boolean"
            },
            "path_metadata_is_not_action_guidance": {
              "type": "boolean"
            }
          }
        },
        "default_meta_skill_order": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "turn_start_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "runtime_constraints": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "execution_modes": {
          "type": "object",
          "key_order": [
            "READ_EXEC",
            "WRITE_EXEC"
          ],
          "properties": {
            "READ_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            },
            "WRITE_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "repo_local_contract_handoff": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "forbidden_primary_runtime_pattern": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "turn_end_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "repo_name": {
          "type": "string"
        }
      }
    },
    "Octopus_OS/Client_Applications/AGENTS.md": {
      "type": "object",
      "key_order": [
        "owner",
        "entry_role",
        "runtime_source_policy",
        "default_meta_skill_order",
        "turn_start_actions",
        "runtime_constraints",
        "execution_modes",
        "repo_local_contract_handoff",
        "forbidden_primary_runtime_pattern",
        "turn_end_actions",
        "repo_name"
      ],
      "properties": {
        "owner": {
          "type": "string"
        },
        "entry_role": {
          "type": "string"
        },
        "runtime_source_policy": {
          "type": "object",
          "key_order": [
            "runtime_rule_source",
            "audit_fields_are_not_primary_runtime_instructions",
            "path_metadata_is_not_action_guidance"
          ],
          "properties": {
            "runtime_rule_source": {
              "type": "string"
            },
            "audit_fields_are_not_primary_runtime_instructions": {
              "type": "boolean"
            },
            "path_metadata_is_not_action_guidance": {
              "type": "boolean"
            }
          }
        },
        "default_meta_skill_order": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "turn_start_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "runtime_constraints": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "execution_modes": {
          "type": "object",
          "key_order": [
            "READ_EXEC",
            "WRITE_EXEC"
          ],
          "properties": {
            "READ_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            },
            "WRITE_EXEC": {
              "type": "object",
              "key_order": [
                "goal",
                "default_actions"
              ],
              "properties": {
                "goal": {
                  "type": "string"
                },
                "default_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "repo_local_contract_handoff": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "forbidden_primary_runtime_pattern": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "turn_end_actions": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "repo_name": {
          "type": "string"
        }
      }
    },
    "Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/AGENTS.md": {
      "type": "object",
      "key_order": [
        "owner",
        "entry_role",
        "governed_container",
        "workflow_contract",
        "turn_end_contract_hooks"
      ],
      "properties": {
        "owner": {
          "type": "string"
        },
        "entry_role": {
          "type": "string"
        },
        "governed_container": {
          "type": "object",
          "key_order": [
            "development_docs_root",
            "codebase_root",
            "module_dir"
          ],
          "properties": {
            "development_docs_root": {
              "type": "string"
            },
            "codebase_root": {
              "type": "string"
            },
            "module_dir": {
              "type": "string"
            }
          }
        },
        "workflow_contract": {
          "type": "object",
          "key_order": [
            "required_skill"
          ],
          "properties": {
            "required_skill": {
              "type": "string"
            }
          }
        },
        "turn_end_contract_hooks": {
          "type": "object",
          "key_order": [
            "frontend_skill_backflow"
          ],
          "properties": {
            "frontend_skill_backflow": {
              "type": "object",
              "key_order": [
                "enabled",
                "target_skill",
                "scope_root",
                "required_frontmatter_keys",
                "qualifying_abstraction_levels",
                "required_turn_end_actions",
                "product_contract_precedence"
              ],
              "properties": {
                "enabled": {
                  "type": "boolean"
                },
                "target_skill": {
                  "type": "string"
                },
                "scope_root": {
                  "type": "string"
                },
                "required_frontmatter_keys": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "qualifying_abstraction_levels": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "required_turn_end_actions": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "product_contract_precedence": {
                  "type": "boolean"
                }
              }
            }
          }
        }
      }
    }
  }
}
```
