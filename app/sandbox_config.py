# Copyright 2026 Google LLC
# Agent Engine Sandbox Code Executor setup

import json
from pathlib import Path
from google.adk.code_executors.agent_engine_sandbox_code_executor import AgentEngineSandboxCodeExecutor


def get_sandbox_code_executor() -> AgentEngineSandboxCodeExecutor:
    """Instantiate AgentEngineSandboxCodeExecutor using deployment_metadata.json.

    Prefers sandbox_resource_name if set; otherwise uses remote_agent_runtime_id (Agent Engine).
    """
    metadata_path = Path(__file__).parent.parent / "deployment_metadata.json"
    sandbox_id = None
    agent_engine_id = None
    
    if metadata_path.exists():
        try:
            with open(metadata_path, "r") as f:
                data = json.load(f)
            sandbox_id = data.get("sandbox_resource_name")
            agent_engine_id = data.get("remote_agent_runtime_id")
        except Exception as e:
            print(f"Warning: Could not read deployment_metadata.json: {e}")
            
    if sandbox_id:
        return AgentEngineSandboxCodeExecutor(sandbox_resource_name=sandbox_id)
    elif agent_engine_id:
        return AgentEngineSandboxCodeExecutor(agent_engine_resource_name=agent_engine_id)
    else:
        return AgentEngineSandboxCodeExecutor()
