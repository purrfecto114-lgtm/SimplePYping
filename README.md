可以。下面是按你当前代码状态重写后的 `README.md`，直接全量覆盖即可。已修正原 README 里的旧内容：PostScript/Ghostscript、旧仓库名、旧运行文件名、安装格式混乱等问题。原文件内容参考自你上传的 README：

````markdown
# Pyping

[![GitHub Repo](https://img.shields.io/badge/GitHub-Pyping-181717?logo=github)](https://github.com/purrfecto114-lgtm/Pyping/)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

一个基于 Python `tkinter` 和 `ping3` 的图形化 Ping 工具，支持实时输出、丢包统计、次数/持续时间双模式、轻量级延迟图表、PNG 图片导出，以及 Windows 高 DPI 显示优化。

A GUI-based Ping tool built with Python `tkinter` and `ping3`. It supports real-time output, packet loss statistics, count/duration modes, lightweight latency charts, PNG image export, and Windows high-DPI display optimization.

---

## 功能特性 / Features

### 图形化 Ping 参数设置 / GUI Ping Configuration

- 支持输入目标主机，域名或 IP 均可。
- 支持设置 Ping 包大小。
- 支持设置 Ping 间隔。
- 支持次数模式和持续时间模式。

English:

- Supports target host input, either domain name or IP address.
- Supports custom packet size.
- Supports custom ping interval.
- Supports count mode and duration mode.

---

### 域名预检 / Domain Pre-check

程序开始 Ping 前会先解析目标主机。

如果域名无效，会直接弹出错误提示，避免进入无意义的测试流程。

The program resolves the target host before starting.

If the domain is invalid, an error message is shown immediately.

---

### 实时输出 / Real-time Output

每次 Ping 的结果都会实时显示在输出框中，包括：

- 延迟时间
- 超时
- 解析失败
- 权限不足
- 其他网络错误

Each ping result is displayed in real time, including:

- Latency
- Timeout
- DNS resolution failure
- Permission error
- Other network errors

---

### 实时统计 / Real-time Statistics

底部状态栏会实时更新：

- 总包数
- 丢包数
- 丢包率
- 平均延迟

The status bar updates in real time:

- Total packets
- Lost packets
- Packet loss rate
- Average latency

---

### 双模式支持 / Dual Mode Support

#### 次数模式 / Count Mode

设置固定 Ping 次数。

`0` 或留空表示无限 Ping，直到手动停止。

Set a fixed number of pings.

`0` or empty means unlimited pinging until manually stopped.

#### 持续时间模式 / Duration Mode

设置持续时间，单位为秒。

时间到达后程序会自动停止。

Set a duration in seconds.

The program stops automatically when the duration is reached.

---

### 延迟图表 / Latency Chart

Ping 结束后，如果存在有效数据，程序会自动弹出图表窗口。

图表内容包括：

- 蓝色折线：延迟变化
- 红色 X：丢包点
- 底部统计摘要
- 目标主机标题
- 图例说明

After pinging finishes, a chart window is automatically shown if data exists.

The chart includes:

- Blue line: latency trend
- Red X: packet loss points
- Bottom statistics summary
- Target host title
- Legend

---

### PNG 图片导出 / PNG Image Export

图表支持保存为 PNG 图片。

当前版本使用 Pillow 的 `ImageGrab` 截取图表 Canvas 区域导出 PNG，不再依赖 Ghostscript。

The chart can be exported as a PNG image.

The current version uses Pillow `ImageGrab` to capture the chart Canvas area and export it as PNG. Ghostscript is no longer required.

Pillow 官方文档说明，`ImageGrab` 可用于将屏幕或指定区域复制为 PIL 图像。  
According to Pillow documentation, `ImageGrab` can copy the screen or a specified bounding box into a PIL image.  
Reference: https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html

---

### 高 DPI 优化 / High-DPI Optimization

针对 Windows 高分辨率屏幕进行了优化。

已处理的问题包括：

- 225% DPI 下按钮显示不完整
- 中文模式下第三个按钮被挤出窗口
- 图表图例超出窗口边界
- 字体和窗口尺寸随 DPI 缩放异常

Optimized for high-resolution Windows displays.

Fixed issues include:

- Buttons not fully visible at 225% DPI
- The third button being pushed out of the window in Chinese mode
- Chart legend overflowing outside the window
- Abnormal font and window scaling under high DPI

---

### 多语言支持 / Multi-language Support

当前支持：

- 简体中文
- English

Currently supported:

- Simplified Chinese
- English

---

### 图表窗口管理 / Chart Window Management

如果上一次图表窗口仍未关闭，再次生成图表时，程序会弹出保存确认窗口，避免误覆盖或丢失数据。

If a previous chart window is still open, the program asks whether to save it before generating a new chart, preventing accidental data loss.

---

## 截图 / Screenshot

请查看 Release 页面。

Please visit the Release page.

---

## 安装 / Installation

### 环境要求 / Requirements

- Python 3.8 或更高版本
- Windows / Linux / macOS
- Python dependencies:
  - `ping3`
  - `Pillow`

`tkinter` 通常随 Python 自带，无需额外安装。

`tkinter` is usually bundled with Python and does not need separate installation.

---

### 克隆仓库 / Clone Repository

```bash
git clone https://github.com/purrfecto114-lgtm/Pyping.git
cd Pyping
````

---

### 安装依赖 / Install Dependencies

如果仓库中包含 `requirements.txt`：

```bash
python -m pip install -r requirements.txt
```

或者手动安装：

```bash
python -m pip install ping3 pillow
```

---

## 运行 / Run

假设主程序文件名为 `PingTool.py`：

```bash
python PingTool.py
```

如果你的文件名不同，请替换为实际文件名。

If your script has a different filename, replace `PingTool.py` with the actual filename.

---

## 使用方法 / Usage

1. 启动程序。
2. 输入目标主机，例如：

   * `www.bing.com`
   * `8.8.8.8`
3. 设置包大小。
4. 设置 Ping 间隔。
5. 选择模式：

   * 次数模式
   * 持续时间模式
6. 点击“开始 Ping”。
7. 在实时输出框查看结果。
8. 点击“停止”可手动结束。
9. Ping 结束后自动查看图表。
10. 点击“保存为图片”导出 PNG 图表。

English:

1. Start the program.
2. Enter a target host, for example:

   * `www.bing.com`
   * `8.8.8.8`
3. Set packet size.
4. Set ping interval.
5. Choose mode:

   * Count mode
   * Duration mode
6. Click "Start Ping".
7. View real-time output.
8. Click "Stop" to manually stop.
9. View the chart after pinging finishes.
10. Click "Save as Image" to export the chart as PNG.

---

## 注意事项 / Notes

### ICMP 权限 / ICMP Permission

`ping3` 使用 ICMP。

在某些系统中，发送 ICMP 包可能需要管理员/root 权限。

`ping3` uses ICMP.

On some systems, sending ICMP packets may require administrator/root permission.

Windows 下如果出现权限不足提示，可以尝试以管理员身份运行。

On Windows, if a permission error appears, try running the program as administrator.

Linux 下可能需要：

```bash
sudo python PingTool.py
```

---

### PNG 导出 / PNG Export

PNG 导出依赖 Pillow。

如果缺少 Pillow，请安装：

```bash
python -m pip install pillow
```

PNG export depends on Pillow.

If Pillow is missing, install it with:

```bash
python -m pip install pillow
```

Ghostscript is not required.

---

## PyInstaller 打包 / Build EXE with PyInstaller

### 安装 PyInstaller / Install PyInstaller

```bash
python -m pip install -U pyinstaller
```

PyInstaller 可将 Python 程序打包为独立应用。官方文档说明，PyInstaller 支持 Windows、macOS 和 Linux，但不是交叉编译器；打包 Windows 程序应在 Windows 上执行。
PyInstaller can package Python programs into standalone applications. The official documentation states that PyInstaller supports Windows, macOS, and Linux, but it is not a cross-compiler; Windows applications should be built on Windows.
Reference: [https://pyinstaller.org/en/stable/usage.html](https://pyinstaller.org/en/stable/usage.html)

---

### 推荐：目录模式 / Recommended: One-directory Mode

开发和测试阶段推荐使用 `--onedir`。

打包命令：

```bash
python -m PyInstaller ^
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

生成路径：

```text
dist/PingTool/PingTool.exe
```

注意：`--onedir` 模式下，必须保留整个 `dist/PingTool/` 文件夹。

不要只复制 `PingTool.exe`，否则程序可能缺少依赖文件而无法运行。

In `--onedir` mode, keep the entire `dist/PingTool/` folder.

Do not copy only `PingTool.exe`, otherwise the program may fail due to missing dependencies.

---

### 单文件模式 / One-file Mode

如果需要只分发一个 exe 文件，可以使用 `--onefile`：

```bash
python -m PyInstaller ^
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

生成路径：

```text
dist/PingTool.exe
```

官方文档说明，`--onefile` 会在运行时解包，启动速度可能比 `--onedir` 慢。
The official documentation notes that one-file executables unpack on each run, so startup may be slower than one-directory builds.
Reference: [https://pyinstaller.org/en/stable/usage.html](https://pyinstaller.org/en/stable/usage.html)

---

### 调试打包问题 / Debug Build

如果 exe 打开后闪退，建议先使用控制台模式打包：

```bash
python -m PyInstaller ^
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

然后运行：

```text
dist/PingTool_Debug/PingTool_Debug.exe
```

控制台会显示错误信息，方便定位问题。

The console window will show error messages, which helps with debugging.

---

## 常见问题 / FAQ

### Q: `dist` 里的 exe 是否要和文件夹一起复制？

如果使用 `--onedir`，答案是：要。

你应该复制整个：

```text
dist/PingTool/
```

而不是只复制：

```text
PingTool.exe
```

If using `--onedir`, yes.

Copy the entire:

```text
dist/PingTool/
```

not just:

```text
PingTool.exe
```

---

### Q: 为什么 PNG 导出不需要 Ghostscript？

因为当前版本不再使用 `Canvas.postscript()` 转图片。

程序直接使用 Pillow `ImageGrab` 截取 Canvas 区域并保存为 PNG。

Because the current version no longer converts `Canvas.postscript()` output into an image.

It directly uses Pillow `ImageGrab` to capture the Canvas area and save it as PNG.

---

### Q: 为什么高 DPI 下按钮曾经显示不完整？

`ttk.Button(width=...)` 的 `width` 是字符宽度，不是像素宽度。

旧版本在高 DPI 下继续放大按钮宽度，导致中文模式下按钮横向溢出。

当前版本已改为三列等分布局，避免按钮被挤出窗口。

`ttk.Button(width=...)` uses character width, not pixel width.

The older version scaled button width under high DPI, which caused buttons to overflow in Chinese mode.

The current version uses a three-column equal-width layout to prevent overflow.

---

### Q: 为什么图例曾经超出窗口？

旧版本将图例放在窗口右边缘附近，并让文字继续向右绘制。

当前版本会根据图例文字宽度动态计算右边距，并将图例放入安全区域内。

The older version placed the legend near the right edge and drew text further to the right.

The current version dynamically calculates the right margin based on legend text width and keeps the legend inside a safe area.

---

## 依赖 / Dependencies

* `ping3`：发送 ICMP 包并获取延迟
* `Pillow`：用于 PNG 图片导出
* `tkinter`：图形界面，Python 标准库
* `threading`：后台 Ping 线程，Python 标准库
* `queue`：线程间通信，Python 标准库
* `socket`：域名解析，Python 标准库
* `datetime`：时间戳记录，Python 标准库

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## Acknowledgement / 致谢

Part of this project was generated or optimized with the assistance of AI.

本项目的部分代码由 AI 辅助生成与优化。

---

## Contributing / 贡献

Issues and Pull Requests are welcome.

欢迎提交 Issue 或 Pull Request 来改进这个工具。

```
::contentReference[oaicite:1]{index=1}
```
