# Pyping

[![GitHub Repo](https://img.shields.io/badge/GitHub-Pyping-181717?logo=github)](https://github.com/purrfecto114-lgtm/Pyping/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

一个基于 Python `tkinter` 和 `ping3` 的图形化 Ping 工具，支持实时输出、丢包统计、次数/持续时间双模式、轻量级延迟图表、PNG 图片导出，以及 Windows 高 DPI 显示优化。

A GUI-based Ping tool built with Python `tkinter` and `ping3`. It supports real-time output, packet loss statistics, count/duration modes, lightweight latency charts, PNG image export, and Windows high-DPI display optimization.

---

## 目录 / Table of Contents

- [功能特性 / Features](#功能特性--features)
- [截图 / Screenshots](#截图--screenshots)
- [安装 / Installation](#安装--installation)
- [运行 / Run](#运行--run)
- [使用方法 / Usage](#使用方法--usage)
- [注意事项 / Notes](#注意事项--notes)
- [PyInstaller 打包 / Build EXE with PyInstaller](#pyinstaller-打包--build-exe-with-pyinstaller)
- [常见问题 / FAQ](#常见问题--faq)
- [依赖 / Dependencies](#依赖--dependencies)
- [许可 / License](#许可--license)
- [致谢 / Acknowledgements](#致谢--acknowledgements)
- [贡献 / Contributing](#贡献--contributing)

---

## 功能特性 / Features

### 图形化 Ping 参数设置 / GUI Ping Configuration

- 支持输入目标主机，域名或 IP 均可。
- 支持设置 Ping 包大小。
- 支持设置 Ping 间隔。
- 支持次数模式和持续时间模式。

**English:**

- Supports target host input, either domain name or IP address.
- Supports custom packet size.
- Supports custom ping interval.
- Supports count mode and duration mode.

### 域名预检 / Domain Pre-check

程序开始 Ping 前会先解析目标主机。如果域名无效，会直接弹出错误提示，避免进入无意义的测试流程。

**English:** The program resolves the target host before starting. If the domain is invalid, an error message is shown immediately.

### 实时输出 / Real-time Output

每次 Ping 的结果都会实时显示在输出框中，包括：延迟时间、超时、解析失败、权限不足和其他网络错误。

**English:** Each ping result is displayed in real time, including latency, timeout, DNS resolution failure, permission error, and other network errors.

### 实时统计 / Real-time Statistics

底部状态栏会实时更新：总包数、丢包数、丢包率、平均延迟。

**English:** The status bar updates in real time: total packets, lost packets, packet loss rate, and average latency.

### 双模式支持 / Dual Mode Support

- **次数模式 / Count Mode**：设置固定 Ping 次数。`0` 或留空表示无限 Ping，直到手动停止。
- **持续时间模式 / Duration Mode**：设置持续时间（秒），时间到达后程序自动停止。

**English:**
- **Count Mode**: Set a fixed number of pings. `0` or empty means unlimited pinging until manually stopped.
- **Duration Mode**: Set a duration in seconds. The program stops automatically when the duration is reached.

### 延迟图表 / Latency Chart

Ping 结束后，如果存在有效数据，程序会自动弹出图表窗口。图表包含：蓝色折线（延迟变化）、红色 X（丢包点）、底部统计摘要、目标主机标题和图例说明。

**English:** After pinging finishes, a chart window is automatically shown if data exists. It includes a blue line (latency trend), red X (packet loss points), bottom statistics summary, target host title, and legend.

### PNG 图片导出 / PNG Image Export

图表支持保存为 PNG 图片。当前版本使用 Pillow 的 `ImageGrab` 截取图表 Canvas 区域导出 PNG，不再依赖 Ghostscript。

**English:** The chart can be exported as a PNG image. The current version uses Pillow `ImageGrab` to capture the chart Canvas area and export it as PNG. Ghostscript is no longer required.

### 高 DPI 优化 / High-DPI Optimization

针对 Windows 高分辨率屏幕进行了全面优化，已解决按钮显示不完整、布局溢出、图表图例超界和字体缩放异常等问题。

**English:** Fully optimized for high-resolution Windows displays. Issues like incomplete buttons, layout overflow, legend clipping, and abnormal font scaling have been resolved.

### 多语言支持 / Multi-language Support

当前支持简体中文和 English。

**English:** Currently supports Simplified Chinese and English.

### 图表窗口管理 / Chart Window Management

如果上一次图表窗口仍未关闭，再次生成图表时程序会弹出保存确认，避免误覆盖或丢失数据。

**English:** If a previous chart window is still open, the program asks whether to save it before generating a new chart, preventing accidental data loss.

---

## 截图 / Screenshots

请访问 [Releases 页面](https://github.com/purrfecto114-lgtm/Pyping/releases) 查看截图。

**English:** Please visit the [Releases page](https://github.com/purrfecto114-lgtm/Pyping/releases) for screenshots.

---

## 安装 / Installation

### 环境要求 / Requirements

- Python 3.8 或更高版本
- Windows / Linux / macOS
- Python 依赖: `ping3`, `Pillow`
- `tkinter` 通常随 Python 自带，无需额外安装。

**English:**
- Python 3.8+
- Windows / Linux / macOS
- Python dependencies: `ping3`, `Pillow`
- `tkinter` is usually bundled with Python.

### 克隆仓库 / Clone Repository

```bash
git clone https://github.com/purrfecto114-lgtm/Pyping.git
cd Pyping
```

### 安装依赖 / Install Dependencies

推荐在虚拟环境中安装：

```bash
# 创建虚拟环境（可选）
python -m venv venv
# 激活虚拟环境
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

如果仓库中没有 `requirements.txt`，可手动安装：

```bash
pip install ping3 pillow
```

---

## 运行 / Run

假设主程序文件名为 `PingTool.py`：

```bash
python PingTool.py
```

如果你的文件名不同，请替换为实际文件名。

**English:** Run the main script (default name: `PingTool.py`). Replace with your actual filename if different.

---

## 使用方法 / Usage

1. 启动程序。
2. 输入目标主机（例如 `www.bing.com` 或 `8.8.8.8`）。
3. 设置包大小。
4. 设置 Ping 间隔。
5. 选择模式：次数模式或持续时间模式。
6. 点击“开始 Ping”。
7. 在实时输出框查看结果。
8. 可随时点击“停止”手动结束。
9. Ping 结束后自动查看图表。
10. 点击“保存为图片”导出 PNG 图表。

**English:**
1. Start the program.
2. Enter a target host (e.g., `www.bing.com` or `8.8.8.8`).
3. Set packet size.
4. Set ping interval.
5. Choose mode: count or duration.
6. Click "Start Ping".
7. View real-time output.
8. Click "Stop" to manually stop at any time.
9. View the chart after pinging finishes.
10. Click "Save as Image" to export the chart as PNG.

---

## 注意事项 / Notes

### ICMP 权限 / ICMP Permission

`ping3` 使用 ICMP 协议。在某些系统中，发送 ICMP 包可能需要管理员/root 权限：

- **Windows**：如遇权限错误，请以管理员身份运行。
- **Linux**：可能需要 `sudo python PingTool.py`。

**English:** `ping3` uses ICMP. On some systems, administrator/root privileges may be required. On Windows, run as administrator if a permission error occurs. On Linux, you may need `sudo python PingTool.py`.

### PNG 导出 / PNG Export

PNG 导出依赖 Pillow，无需 Ghostscript。如果缺少 Pillow，请安装：

```bash
pip install pillow
```

**English:** PNG export requires Pillow; Ghostscript is not needed. Install Pillow with `pip install pillow` if missing.

---

## PyInstaller 打包 / Build EXE with PyInstaller

### 安装 PyInstaller / Install PyInstaller

```bash
pip install -U pyinstaller
```

> **注意**：在 Windows 上执行以下命令；Linux/macOS 用户请将续行符 `^` 替换为 `\`。

### 推荐：目录模式 / Recommended: One-directory Mode

开发测试阶段推荐使用 `--onedir`。

```bash
pyinstaller ^
  --clean ^
  --noconfirm ^
  --onedir ^
  --windowed ^
  --name "PingTool" ^
  --hidden-import ping3 ^
  --hidden-import PIL ^
  --hidden-import PIL.ImageGrab ^
  PingTool.py
```

生成路径：`dist/PingTool/PingTool.exe`。请保留整个 `dist/PingTool/` 文件夹，不要只复制 `.exe` 文件。

**English:** The output is in `dist/PingTool/`. Keep the entire folder; do not copy only the `.exe` file.

### 单文件模式 / One-file Mode

如果只需要一个 exe 文件：

```bash
pyinstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name "PingTool" ^
  --hidden-import ping3 ^
  --hidden-import PIL ^
  --hidden-import PIL.ImageGrab ^
  PingTool.py
```

生成路径：`dist/PingTool.exe`。单文件模式启动时需解包，启动速度可能略慢。

**English:** Single executable is generated at `dist/PingTool.exe`. It may start slower due to on‑the‑fly unpacking.

### 调试打包问题 / Debug Build

如果 exe 打开后闪退，请使用控制台模式查看错误信息：

```bash
pyinstaller ^
  --clean ^
  --noconfirm ^
  --onedir ^
  --console ^
  --name "PingTool_Debug" ^
  --hidden-import ping3 ^
  --hidden-import PIL ^
  --hidden-import PIL.ImageGrab ^
  PingTool.py
```

然后运行 `dist/PingTool_Debug/PingTool_Debug.exe`，控制台会显示错误信息。

**English:** Use `--console` mode to see error messages if the GUI crashes immediately.

---

## 常见问题 / FAQ

**Q: 为什么 `dist` 里的 exe 要和文件夹一起复制？**  
A: 如果使用 `--onedir`，必须复制整个 `dist/PingTool/` 文件夹，因为程序依赖其中的库文件。

**Q: 为什么 PNG 导出不需要 Ghostscript？**  
A: 当前版本使用 Pillow 的 `ImageGrab` 直接截取 Canvas 区域保存为 PNG，不再通过 `postscript()` 转换。

**Q: 高 DPI 下按钮曾经显示不完整，现在是如何解决的？**  
A: 按钮宽度改用等比例网格布局，避免字符宽度在高缩放比下溢出窗口。图表图例也做了动态边距计算，确保完整显示。

---

## 依赖 / Dependencies

- `ping3`：发送 ICMP 包并获取延迟
- `Pillow`：用于 PNG 图片导出
- `tkinter`：图形界面，Python 标准库
- `threading`：后台 Ping 线程，Python 标准库
- `queue`：线程间通信，Python 标准库
- `socket`：域名解析，Python 标准库
- `datetime`：时间戳记录，Python 标准库

---

## 许可 / License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 致谢 / Acknowledgements

Part of this project was generated or optimized with the assistance of AI.  
本项目的部分代码由 AI 辅助生成与优化。

---

## 贡献 / Contributing

Issues and Pull Requests are welcome.  
欢迎提交 Issue 或 Pull Request 来改进这个工具。
