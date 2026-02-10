# Magma MCP Server — API Reference

*Auto-generated from server tool and resource registrations. Run `python -m mmcp.gen_api_docs` to regenerate.*

---

## Tools

### `magma_build_image`

Build a Docker image for a fuzzer/target combination. Returns a task_id for tracking (async operation).

**Parameters:**

- `fuzzer`: Fuzzer name (e.g. 'aflplusplus', 'honggfuzz')
- `target`: Target name (e.g. 'libpng', 'libtiff')
- `target_version`: Version from releases file (default 'PIONEER')
- `canary_mode`: 1=with canaries, 2=no canaries, 3=with fixes (default 1)
- `isan`: Enable fatal canaries (default false)
- `harden`: Enable hardened canaries (default false)
- `source_coverage`: Enable source coverage instrumentation (default false)

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `fuzzer` | `string` | yes | — |
| `target` | `string` | yes | — |
| `target_version` | `string` | no | PIONEER |
| `canary_mode` | `integer` | no | 1 |
| `isan` | `boolean` | no | False |
| `harden` | `boolean` | no | False |
| `source_coverage` | `boolean` | no | False |

---

### `magma_build_images`

Build Docker images for multiple fuzzer/target combinations with concurrency control.

**Parameters:**

- `fuzzers`: List of fuzzer names. Empty or null for all fuzzers.
- `targets`: List of target names. Empty or null for all targets.
- `max_parallel`: Maximum concurrent builds (default 2)
- `target_version`: Version from releases file (default 'PIONEER')
- `canary_mode`: 1=with canaries, 2=no canaries, 3=with fixes (default 1)
- `isan`: Enable fatal canaries (default false)
- `harden`: Enable hardened canaries (default false)
- `source_coverage`: Enable source coverage instrumentation (default false)

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `fuzzers` | `any` | no | None |
| `targets` | `any` | no | None |
| `max_parallel` | `integer` | no | 2 |
| `target_version` | `string` | no | PIONEER |
| `canary_mode` | `integer` | no | 1 |
| `isan` | `boolean` | no | False |
| `harden` | `boolean` | no | False |
| `source_coverage` | `boolean` | no | False |

---

### `magma_configure_cpus`

Reconfigure the CPU pool for campaign affinity. Fails if any CPUs are allocated.

**Parameters:**

- `worker_mode`: CPU dedup mode: 1=all logical CPUs, 2=one per physical core, 3=one per socket. 0 keeps current.
- `max_cpus`: Cap the pool to this many CPUs. 0 for no cap.

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `worker_mode` | `integer` | no | 0 |
| `max_cpus` | `integer` | no | 0 |

---

### `magma_cpu_status`

Show CPU pool status: total, free, allocated per-task, and queued count.

---

### `magma_extract_pocs`

Extract proof-of-concept crash inputs from campaign findings. Async operation.

**Parameters:**

- `fuzzer`: Fuzzer name
- `target`: Target name
- `program`: Program name
- `shared_dir`: Path to campaign shared directory (contains findings/)
- `poc_dir`: Where to save extracted PoCs. Auto-created if empty.

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `fuzzer` | `string` | yes | — |
| `target` | `string` | yes | — |
| `program` | `string` | yes | — |
| `shared_dir` | `string` | yes | — |
| `poc_dir` | `string` | no |  |

---

### `magma_generate_json`

Convert campaign results in a workdir to a JSON summary. Async operation.

**Parameters:**

- `workdir`: Path to the captain workdir
- `output_file`: Path for JSON output. Auto-generated if empty.
- `workers`: Number of parallel workers (default 4)

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `workdir` | `string` | yes | — |
| `output_file` | `string` | no |  |
| `workers` | `integer` | no | 4 |

---

### `magma_get_api_reference`

Retrieve the MCP API reference documentation.

**Parameters:**

- `tool_name`: Optional specific tool name (e.g. 'magma_build_image'). Empty for full reference.

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `tool_name` | `string` | no |  |

---

### `magma_get_bug_patch`

Read the full patch content for a specific bug.

**Parameters:**

- `target`: Target name (e.g. 'libpng')
- `bug_id`: Bug identifier (e.g. 'PNG001')

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `target` | `string` | yes | — |
| `bug_id` | `string` | yes | — |

---

### `magma_get_build_matrix`

Get a summary matrix of all build tasks showing pass/fail status per fuzzer×target.

---

### `magma_get_campaign_results`

Get per-bug reach/trigger timing data for a specific campaign run.

**Parameters:**

- `workdir`: Path to the captain workdir
- `fuzzer`: Fuzzer name
- `target`: Target name
- `program`: Program name
- `run_id`: Run identifier (integer string)

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `workdir` | `string` | yes | — |
| `fuzzer` | `string` | yes | — |
| `target` | `string` | yes | — |
| `program` | `string` | yes | — |
| `run_id` | `string` | yes | — |

---

### `magma_get_knowledge`

Retrieve Magma knowledge base documentation for understanding the benchmark.

**Parameters:**

- `topic`: Optional topic filter. Supported: 'canary', 'targets', 'fuzzers', 'docker', 'campaign', 'monitor', 'patches', 'captain', 'runonce', 'coverage', 'env', 'mcp'. Empty for full document.

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `topic` | `string` | no |  |

---

### `magma_get_patch`

Read a bug patch or setup patch for a target.

**Parameters:**

- `target`: Target name (e.g. 'libpng')
- `patch_name`: Patch filename without .patch extension (e.g. 'PNG001') or with extension

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `target` | `string` | yes | — |
| `patch_name` | `string` | yes | — |

---

### `magma_get_target_info`

Get detailed information about a specific target including programs, args, versions, bugs, and corpus sizes.

**Parameters:**

- `target`: Target name (e.g. 'libpng', 'libtiff')

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `target` | `string` | yes | — |

---

### `magma_get_task_log`

Retrieve the full log for a task from disk.

**Parameters:**

- `task_id`: The task_id returned by an async tool
- `tail`: Only return the last N lines (0 = all)
- `search`: Filter to lines containing this string (e.g. 'error', 'FAILED')

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `task_id` | `string` | yes | — |
| `tail` | `integer` | no | 0 |
| `search` | `string` | no |  |

---

### `magma_get_task_status`

Check the status of campaign tasks by batch ID.

**Parameters:**

- `batch_id`: The batch_id returned by magma_start_campaign.
- `task_ids`: Optional list of specific task IDs to check. If empty/null, returns all tasks in the batch.

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `batch_id` | `integer` | yes | — |
| `task_ids` | `any` | no | None |

---

### `magma_list_active_tasks`

List all active batches with their running/queued tasks.

---

### `magma_list_bugs`

List all bugs across all targets, or filtered to a specific target.

**Parameters:**

- `target`: Optional target name to filter by (e.g. 'libpng'). Empty string for all targets.

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `target` | `string` | no |  |

---

### `magma_list_campaigns`

List completed or in-progress campaigns in a workdir.

**Parameters:**

- `workdir`: Path to the captain workdir (contains ar/ subdirectory)
- `fuzzer`: Optional filter by fuzzer name
- `target`: Optional filter by target name

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `workdir` | `string` | yes | — |
| `fuzzer` | `string` | no |  |
| `target` | `string` | no |  |

---

### `magma_list_fuzzers`

List all available fuzzers with their script files.

---

### `magma_list_images`

List all built Magma Docker images.

---

### `magma_list_targets`

List all available fuzzing targets with their programs, bug IDs, and versions.

---

### `magma_start_campaign`

Start fuzzing campaign(s) in Docker containers. Returns task_id(s) for tracking.

**Parameters:**

- `fuzzer`: Fuzzer name (e.g. 'aflplusplus')
- `target`: Target name (e.g. 'libpng')
- `program`: Program name from the target's configrc (e.g. 'libpng_read_fuzzer')
- `args`: Program launch arguments (e.g. '@@')
- `fuzz_args`: Extra arguments to pass to the fuzzer
- `timeout`: Campaign duration with suffix: s/m/h/d (default '1m')
- `repeat`: Number of independent campaign trials to run (default 1)
- `num_cpus`: CPUs to auto-allocate per campaign (0 = no affinity)
- `poll`: Seconds between monitor polls (default 5)
- `no_archive`: If true, move findings directly to ar/ instead of tarring (default false)

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `fuzzer` | `string` | yes | — |
| `target` | `string` | yes | — |
| `program` | `string` | yes | — |
| `args` | `string` | no |  |
| `fuzz_args` | `string` | no |  |
| `timeout` | `string` | no | 1m |
| `repeat` | `integer` | no | 1 |
| `num_cpus` | `integer` | no | 0 |
| `poll` | `integer` | no | 5 |
| `no_archive` | `boolean` | no | False |

---

### `magma_stop_campaign`

Stop running campaigns by batch ID, optionally filtering by task IDs.

**Parameters:**

- `batch_id`: The batch_id returned by magma_start_campaign.
- `task_ids`: Optional list of specific task IDs to stop. If empty/null, stops all tasks in the batch.

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `batch_id` | `integer` | yes | — |
| `task_ids` | `any` | no | None |

---

### `magma_test_input`

Run a single test case in an ephemeral Docker container to check if any bugs are reached or triggered.

**Parameters:**

- `fuzzer`: Fuzzer name (e.g. 'aflplusplus')
- `target`: Target name (e.g. 'libpng')
- `program`: Program name (e.g. 'libpng_read_fuzzer')
- `input_path`: Absolute path to the test case file on the host

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `fuzzer` | `string` | yes | — |
| `target` | `string` | yes | — |
| `program` | `string` | yes | — |
| `input_path` | `string` | yes | — |

---

### `magma_update_patch`

Write updated patch content for a bug or setup patch.

**Parameters:**

- `target`: Target name (e.g. 'libpng')
- `patch_name`: Patch name without .patch extension (e.g. 'PNG001')
- `content`: New patch file content

**Schema:**

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `target` | `string` | yes | — |
| `patch_name` | `string` | yes | — |
| `content` | `string` | yes | — |

---

## Resources

Resources provide read-only data accessible via URI patterns.

### Static Resources

| URI | Description |
|-----|-------------|
| `magma://api-reference` | Auto-generated MCP API reference — all tools, parameters, schemas, and resources. |
| `magma://config/captainrc` | Current captainrc configuration file content. |
| `magma://docker/images` | Currently built Magma Docker images. |
| `magma://fuzzers` | List of all fuzzer names with available scripts. |
| `magma://knowledge-base` | Complete Magma knowledge base — architecture, concepts, env vars, workflows, conventions. |
| `magma://targets` | List of all target names with summary information. |

### URI Templates

| URI Pattern | Description |
|-------------|-------------|
| `magma://fuzzers/{fuzzer}` | Fuzzer detail: scripts present, capabilities. |
| `magma://fuzzers/{fuzzer}/{script}` | Content of a specific fuzzer script. |
| `magma://targets/{target}` | Full target detail: programs, args, versions, bugs, corpus counts. |
| `magma://targets/{target}/bugs` | List of bug IDs with has_poc flag. |
| `magma://targets/{target}/bugs/{bug_id}` | Raw patch file content for a specific bug. |
| `magma://targets/{target}/configrc` | Raw configrc file content. |
| `magma://targets/{target}/corpus/{program}` | List of seed file names for a program. |
| `magma://targets/{target}/releases` | Raw releases file content. |

