# tests/test_main.py
from pathlib import Path
import subprocess
import sys
import os

def test_main_smoke(tmp_path: Path):
    inst = "\n".join([
        "CACHE,1",
        "ADDI,R1,R0,5",
        "SW,R1,8(R0)",
        "CACHE,2",
        "HALT,;",
    ])
    data = "8,0\n"
    inst_p = tmp_path / "inst.txt"
    data_p = tmp_path / "data.txt"
    inst_p.write_text(inst, encoding="utf-8")
    data_p.write_text(data, encoding="utf-8")

    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    # Keep existing PYTHONPATH first (pytest-cov’s shim), then append src/
    existing = env.get("PYTHONPATH", "")
    added = str(repo_root / "src")
    env["PYTHONPATH"] = added if not existing else existing + os.pathsep + added

    cmd = [
        sys.executable, "-m", "cpu_sim.main",
        "--instructions", str(inst_p),
        "--data", str(data_p),
        "--no-trace",
    ]
    proc = subprocess.run(cmd, cwd=repo_root, env=env, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert "MEM[8] = 5" in proc.stdout

