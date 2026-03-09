# Scan Workflow

1. 读取 branch contract。
2. 读取 scan directive。
3. 扫描 `Octopus_OS` 根层、容器根层和 `Octopus_OS/Mother_Doc/docs`。
4. 输出 `scan_report.json`。
5. 不做 collect，不做 push。
