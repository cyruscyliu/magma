"""Docker CLI utility wrappers for listing images, containers, etc."""

import json
import subprocess


def _run_docker(args: list[str], timeout: int = 30) -> str:
    """Run a docker command and return stdout."""
    result = subprocess.run(
        ["docker", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"docker {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def list_magma_images() -> list[dict]:
    """List Docker images matching 'magma/*'.

    Returns list of dicts with: repository, tag, image_id, created, size.
    """
    output = _run_docker([
        "images",
        "--filter=reference=magma/*/*",
        "--format={{json .}}",
    ])
    images = []
    for line in output.strip().splitlines():
        if not line:
            continue
        data = json.loads(line)
        images.append({
            "repository": data.get("Repository", ""),
            "tag": data.get("Tag", ""),
            "image_id": data.get("ID", ""),
            "created": data.get("CreatedSince", ""),
            "size": data.get("Size", ""),
        })
    return images


def list_magma_containers() -> list[dict]:
    """List running Docker containers from magma images.

    Returns list of dicts with: container_id, image, status, created, names.
    """
    output = _run_docker([
        "ps",
        "--filter=ancestor=magma",
        "--format={{json .}}",
    ])

    # Also try filtering by name/image pattern since ancestor filter is exact
    try:
        output2 = _run_docker([
            "ps",
            "--format={{json .}}",
        ])
    except RuntimeError:
        output2 = ""

    containers = []
    seen_ids = set()

    for source in [output, output2]:
        for line in source.strip().splitlines():
            if not line:
                continue
            data = json.loads(line)
            image = data.get("Image", "")
            cid = data.get("ID", "")
            if cid in seen_ids:
                continue
            if not image.startswith("magma/"):
                continue
            seen_ids.add(cid)
            containers.append({
                "container_id": cid,
                "image": image,
                "status": data.get("Status", ""),
                "created": data.get("CreatedAt", ""),
                "names": data.get("Names", ""),
            })

    return containers


def image_exists(image_name: str) -> bool:
    """Check if a Docker image exists locally."""
    try:
        _run_docker(["image", "inspect", image_name])
        return True
    except RuntimeError:
        return False


def stop_container(container_id: str, timeout: int = 10) -> bool:
    """Stop a Docker container."""
    try:
        _run_docker(["stop", "-t", str(timeout), container_id], timeout=timeout + 5)
        return True
    except RuntimeError:
        return False


def remove_container(container_id: str, force: bool = False) -> bool:
    """Remove a Docker container."""
    args = ["rm"]
    if force:
        args.append("-f")
    args.append(container_id)
    try:
        _run_docker(args)
        return True
    except RuntimeError:
        return False
