---
doc_id: meta_agent_browser.references_windows_headed_bridge
doc_type: topic_atom
topic: Windows Headed Bridge
anchors:
- target: ../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Windows Headed Bridge

## Scope
- 这是 `有头模式` 的 Windows 桥接独立入口文档。
- 默认浏览器：Windows Edge
- 默认桥接服务：`win_chrome_devtools`
- 规范桥接路径：WSL dynamic gateway -> Windows Edge debug endpoint `http://<WSL_GATEWAY_IP>:9333`
- 策略：先 fast-start，再 recovery/reset

## Canonical Runtime Contract
Use dynamic WSL gateway. Do not hardcode `127.0.0.1:9333` inside WSL MCP config.

### 1. Wrapper Script
Create or update `~/.codex/bin/win-chrome-devtools-mcp.sh`:

```bash
#!/usr/bin/env sh
set -eu
GW=$(ip route | awk '/default/ {print $3; exit}')
exec /mnt/c/Windows/System32/cmd.exe /c "C:\Users\HP\.mcp-win\node_modules\.bin\chrome-devtools-mcp.cmd" --browserUrl "http://$GW:9333" "$@"
```

Then run:

```bash
chmod +x ~/.codex/bin/win-chrome-devtools-mcp.sh
```

### 2. WSL MCP Config
Append or update this block in `~/.codex/config.toml`:

```toml
[mcp_servers.win_chrome_devtools]
type = "stdio"
command = "/home/jasontan656/.codex/bin/win-chrome-devtools-mcp.sh"
startup_timeout_ms = 180000
```

## Path A: Fast Start
Use this path first for every headed run.

### A1. Launch Edge Debug Endpoint
```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command '$edge="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"; if (!(Test-Path $edge)) {$edge="C:\Program Files\Microsoft\Edge\Application\msedge.exe"}; Start-Process -FilePath $edge -ArgumentList "--remote-debugging-port=9333","--user-data-dir=C:\Users\HP\AppData\Local\EdgeMCPProfile","--new-window","about:blank"; Start-Sleep -Seconds 2; (Invoke-RestMethod -Uri "http://127.0.0.1:9333/json/version" | ConvertTo-Json -Compress)'
```

### A2. Verify from WSL
```bash
codex mcp get win_chrome_devtools
GW=$(ip route | awk '/default/ {print $3; exit}')
curl "http://$GW:9333/json/version"
```

Expected:
- `win_chrome_devtools` is enabled
- JSON includes `Browser: Edg/...`
- WSL curl works

## Path B: Recovery
Use only when Path A fails.

Create `C:\Users\HP\.mcp-win\recover-win-edge-mcp.ps1`:

```powershell
$ErrorActionPreference = "Stop"
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) {
  $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}
$profile = "C:\Users\HP\AppData\Local\EdgeMCPProfile"

Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "msedge.exe" -and $_.CommandLine -like "*--remote-debugging-port=9333*" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Start-Process -FilePath $edge -ArgumentList "--remote-debugging-port=9333","--user-data-dir=$profile","--new-window","about:blank"
Start-Sleep -Seconds 2

netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9333 | Out-Null
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9333 connectaddress=127.0.0.1 connectport=9333 | Out-Null

if (-not (Get-NetFirewallRule -DisplayName "WSL Edge DevTools 9333" -ErrorAction SilentlyContinue)) {
  New-NetFirewallRule -DisplayName "WSL Edge DevTools 9333" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 9333 | Out-Null
}

$ok = $false
for ($i = 0; $i -lt 5; $i++) {
  try {
    $v = Invoke-RestMethod -Uri "http://127.0.0.1:9333/json/version" -TimeoutSec 2
    if ($v.Browser -like "Edg/*") { $ok = $true; break }
  } catch {}
  Start-Sleep -Seconds 1
}
if (-not $ok) { throw "Edge debug endpoint not ready on 127.0.0.1:9333 after recovery." }

Write-Host "[OK] Recovery complete"
Write-Host ("[OK] Browser=" + $v.Browser)
```

Run:

```bash
cmd.exe /c "powershell -ExecutionPolicy Bypass -File C:\Users\HP\.mcp-win\recover-win-edge-mcp.ps1"
```

## Path C: Reset Then Recover
Use only when Path B still fails or bridge rules are polluted.

Create `C:\Users\HP\.mcp-win\reset-win-edge-mcp.ps1`:

```powershell
$ErrorActionPreference = "SilentlyContinue"

Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "msedge.exe" -and $_.CommandLine -like "*--remote-debugging-port=9333*" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9333 | Out-Null
Remove-NetFirewallRule -DisplayName "WSL Edge DevTools 9333" | Out-Null

Write-Host "[OK] Reset cleanup complete"
```

Run:

```bash
cmd.exe /c "powershell -ExecutionPolicy Bypass -File C:\Users\HP\.mcp-win\reset-win-edge-mcp.ps1"
cmd.exe /c "powershell -ExecutionPolicy Bypass -File C:\Users\HP\.mcp-win\recover-win-edge-mcp.ps1"
```

## WSL Side Quick Fix
Create or update `~/.codex/scripts/fix-win-mcp-edge.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p ~/.codex/bin ~/.codex/scripts
cat > ~/.codex/bin/win-chrome-devtools-mcp.sh <<'EOF'
#!/usr/bin/env sh
set -eu
GW=$(ip route | awk '/default/ {print $3; exit}')
exec /mnt/c/Windows/System32/cmd.exe /c "C:\Users\HP\.mcp-win\node_modules\.bin\chrome-devtools-mcp.cmd" --browserUrl "http://$GW:9333" "$@"
EOF
chmod +x ~/.codex/bin/win-chrome-devtools-mcp.sh
echo "[OK] wrapper updated: ~/.codex/bin/win-chrome-devtools-mcp.sh"
echo "Now ensure ~/.codex/config.toml points win_chrome_devtools.command to this wrapper."
```

Run:

```bash
bash ~/.codex/scripts/fix-win-mcp-edge.sh
```

## End-to-End Validation
```bash
GW=$(ip route | awk '/default/ {print $3; exit}')
curl "http://$GW:9333/json/version"
```

Required proof:
1. `list_pages` shows initial page
2. navigate to a site such as `https://www.wikipedia.org`
3. fill one field and submit
4. click one link and confirm URL changed
5. `evaluate_script` `navigator.userAgent` contains `Edg/`
6. close browser and verify `9333` is no longer reachable

## Runtime Rules
- Use this doc only for `有头模式`.
- If `win_chrome_devtools` is unavailable in `codex mcp list`, return `WINDOWS_MCP_BRIDGE_UNAVAILABLE`.
- No silent downgrade: if you must leave headed mode, explain why and switch explicitly.
- Do not assume “window opened” means “bridge healthy”; always verify process and port ownership.
