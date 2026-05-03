import time
import threading
import queue
import socket
import sys
import os
import traceback
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

APP_NAME = "Ping Tool"
APP_VERSION = "v0.2"
APP_HOMEPAGE = "https://github.com/purrfecto114-lgtm/Pyping"

DEFAULT_WINDOW_WIDTH = 900
DEFAULT_WINDOW_HEIGHT = 750
DEFAULT_WINDOW_WIDTH_EN = 950
DEFAULT_WINDOW_HEIGHT_EN = 780
MIN_WINDOW_WIDTH = 720
MIN_WINDOW_HEIGHT = 600

BASE_FONT_SIZE = 10
TITLE_FONT_SIZE = 11
SMALL_FONT_SIZE = 9
BUTTON_WIDTH = 12
BUTTON_WIDTH_EN = 15

CHART_WIDTH = 1100
CHART_HEIGHT = 650
SAVE_DIALOG_WIDTH = 400
SAVE_DIALOG_HEIGHT = 200

MIN_INTERVAL_SECONDS = 0.1
QUEUE_POLL_MS = 100
SAVE_DIALOG_TIMEOUT = 15
MAX_POINTS_IN_MEMORY = 5000

IS_FROZEN = getattr(sys, "frozen", False)
MISSING_DEPS = []


def detect_dependencies():
    deps = {"ping3": False, "pillow": False}
    global ping
    ping = None

    try:
        from ping3 import ping as ping3_ping
        ping = ping3_ping
        deps["ping3"] = True
    except Exception:
        deps["ping3"] = False

    try:
        from PIL import ImageGrab
        deps["pillow"] = True
    except Exception:
        deps["pillow"] = False

    return deps


DEPENDENCY_STATUS = detect_dependencies()
if not DEPENDENCY_STATUS["ping3"]:
    MISSING_DEPS.append("ping3")
if not DEPENDENCY_STATUS["pillow"]:
    MISSING_DEPS.append("Pillow (仅影响 PNG 导出，不影响 Ping 主功能)")


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def replace_extension(path: str, new_ext: str) -> str:
    root, _ext = os.path.splitext(path)
    return root + new_ext


def setup_high_dpi():
    if sys.platform != "win32":
        return
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)
    except (AttributeError, OSError):
        try:
            windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass


def configure_tkinter_dpi(root):
    try:
        current_scaling = root.tk.call("tk", "scaling")
        if not current_scaling or float(current_scaling) <= 0:
            root.tk.call("tk", "scaling", 1.0)
    except Exception:
        pass


def get_dpi_scale(root):
    try:
        return max(1.0, root.winfo_fpixels("1i") / 96.0)
    except Exception:
        try:
            return max(1.0, root.winfo_pixels("1i") / 96.0)
        except Exception:
            return 1.0


LANGUAGES = {
    "zh_CN": {
        "app_title": "Ping 工具",
        "param_frame": "参数设置",
        "target_host": "目标主机:",
        "host_placeholder": "例如: www.bing.com 或 8.8.8.8",
        "packet_size": "包大小 (字节):",
        "interval": "间隔 (秒):",
        "mode_frame": "模式选择",
        "count_mode": "次数模式",
        "duration_mode": "持续时间模式",
        "ping_count": "Ping 次数 (0 或空 = 无限):",
        "duration": "持续时间 (秒):",
        "start_btn": "开始 Ping",
        "stop_btn": "停止",
        "output_frame": "实时输出",
        "statistics": "统计信息",
        "total_packets": "总包",
        "lost_packets": "丢包",
        "loss_rate": "丢包率",
        "avg_latency": "平均延迟",
        "min_latency": "最小延迟",
        "max_latency": "最大延迟",
        "save_chart": "保存为图片",
        "chart_title": "Ping 结果",
        "chart_latency": "延迟 (ms)",
        "chart_packet_loss": "丢包",
        "dialog_title": "图表未保存",
        "dialog_message": "当前有未保存的图表窗口，是否保存？",
        "dialog_save": "保存",
        "dialog_discard": "不保存",
        "dialog_cancel": "取消",
        "dialog_timeout": "超时自动放弃保存:",
        "dialog_save_success": "保存成功",
        "dialog_save_path": "图表已保存至:",
        "error_host": "错误",
        "error_host_msg": "请输入目标主机",
        "error_size": "包大小不能为空",
        "error_size_int": "包大小必须为整数",
        "error_size_positive": "包大小必须为正整数",
        "error_interval": "间隔必须为数字",
        "error_interval_positive": "间隔必须为正数",
        "error_interval_too_small": "间隔太小，建议不小于 0.1 秒",
        "error_count": "次数必须为整数",
        "error_count_negative": "次数不能为负数",
        "error_duration": "请输入持续时间",
        "error_duration_positive": "持续时间必须为正数",
        "error_duration_number": "持续时间必须为数字",
        "error_resolve": "域名解析失败",
        "chart_resolve": "目标解析为",
        "output_timeout": "超时",
        "output_resolve_fail": "解析失败",
        "output_permission": "权限不足（Windows 下可能需要管理员权限）",
        "output_missing_ping3": "未检测到 ping3，无法执行 Ping",
        "output_error": "错误",
        "output_cancel": "操作已取消，未生成新图表",
        "output_no_data": "无数据",
        "menu_language": "语言",
        "menu_about": "关于",
        "about_title": "关于 Ping 工具",
        "about_message": f"Ping 工具 {APP_VERSION}\n支持多语言、高 DPI 优化、系统字体\n\n项目地址: {APP_HOMEPAGE}",
        "dependency_warn_title": "依赖提醒",
        "dependency_warn_ping3": "未检测到 ping3，主功能不可用。\nLinux 打包前请先安装依赖；如为 exe，请重新打包并包含 ping3。",
        "dependency_warn_pillow": "未检测到 Pillow，PNG 导出不可用。",
        "dependency_warn_both": "检测到以下依赖缺失:\n{deps}\n\n主功能或部分保存功能可能受到影响。",
        "save_png_missing_pillow": "未检测到 Pillow，无法导出 PNG。",
        "save_png_failed": "PNG 导出失败:",
        "save_png_success": "PNG 已保存:",
        "open_last_chart": "打开上一次图表",
        "no_chart_data": "没有可用的图表数据",
    },
    "en_US": {
        "app_title": "Ping Tool",
        "param_frame": "Parameters",
        "target_host": "Target Host:",
        "host_placeholder": "e.g., www.bing.com or 8.8.8.8",
        "packet_size": "Packet Size (bytes):",
        "interval": "Interval (seconds):",
        "mode_frame": "Mode",
        "count_mode": "Count Mode",
        "duration_mode": "Duration Mode",
        "ping_count": "Ping Count (0 or empty = infinite):",
        "duration": "Duration (seconds):",
        "start_btn": "Start Ping",
        "stop_btn": "Stop",
        "output_frame": "Real-time Output",
        "statistics": "Statistics",
        "total_packets": "Total",
        "lost_packets": "Lost",
        "loss_rate": "Loss Rate",
        "avg_latency": "Avg Latency",
        "min_latency": "Min Latency",
        "max_latency": "Max Latency",
        "save_chart": "Save as Image",
        "chart_title": "Ping Results",
        "chart_latency": "Latency (ms)",
        "chart_packet_loss": "Packet Loss",
        "dialog_title": "Chart Not Saved",
        "dialog_message": "There is an unsaved chart window. Save it?",
        "dialog_save": "Save",
        "dialog_discard": "Discard",
        "dialog_cancel": "Cancel",
        "dialog_timeout": "Auto-discard in:",
        "dialog_save_success": "Save Successful",
        "dialog_save_path": "Chart saved to:",
        "error_host": "Error",
        "error_host_msg": "Please enter target host",
        "error_size": "Packet size cannot be empty",
        "error_size_int": "Packet size must be an integer",
        "error_size_positive": "Packet size must be a positive integer",
        "error_interval": "Interval must be a number",
        "error_interval_positive": "Interval must be positive",
        "error_interval_too_small": "Interval is too small; it should be at least 0.1 seconds",
        "error_count": "Count must be an integer",
        "error_count_negative": "Count cannot be negative",
        "error_duration": "Please enter duration",
        "error_duration_positive": "Duration must be positive",
        "error_duration_number": "Duration must be a number",
        "error_resolve": "DNS resolution failed",
        "chart_resolve": "Target resolved to",
        "output_timeout": "Timeout",
        "output_resolve_fail": "Resolution Failed",
        "output_permission": "Permission denied (may require admin on Windows)",
        "output_missing_ping3": "ping3 is missing; ping cannot start",
        "output_error": "Error",
        "output_cancel": "Operation cancelled, no new chart created",
        "output_no_data": "No Data",
        "menu_language": "Language",
        "menu_about": "About",
        "about_title": "About Ping Tool",
        "about_message": f"Ping Tool {APP_VERSION}\nMulti-language support, High DPI optimized\nSystem fonts\n\nProject: {APP_HOMEPAGE}",
        "dependency_warn_title": "Dependency Warning",
        "dependency_warn_ping3": "ping3 was not found, so the core ping feature is unavailable.\nInstall dependencies before packaging on Linux, or rebuild the executable with ping3 bundled.",
        "dependency_warn_pillow": "Pillow was not found. PNG export is unavailable.",
        "dependency_warn_both": "Missing dependencies detected:\n{deps}\n\nCore functionality or save behavior may be affected.",
        "save_png_missing_pillow": "Pillow is not available, so PNG export is unavailable.",
        "save_png_failed": "PNG export failed:",
        "save_png_success": "PNG saved:",
        "open_last_chart": "Open Last Chart",
        "no_chart_data": "No chart data available",
    },
}

LANGUAGE_NAMES = {
    "zh_CN": "简体中文",
    "en_US": "English",
}


def get_font_config():
    import platform
    system = platform.system()
    if system == "Windows":
        return {
            "cjk": ("Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "SimSun", "PingFang SC"),
            "latin": ("Segoe UI", "Arial", "Tahoma", "Verdana"),
            "fallback": "Segoe UI",
        }
    elif system == "Darwin":
        return {
            "cjk": ("PingFang SC", "Hiragino Sans GB", "STHeiti", "Microsoft YaHei"),
            "latin": ("SF Pro Text", "Helvetica", "Arial"),
            "fallback": "Helvetica",
        }
    else:
        return {
            "cjk": ("Noto Sans CJK SC", "Noto Sans SC", "WenQuanYi Micro Hei", "Noto Sans", "Ubuntu"),
            "latin": ("Noto Sans", "Liberation Sans", "DejaVu Sans", "Arial"),
            "fallback": "DejaVu Sans",
        }


def check_font_available(font_name):
    try:
        root = tk.Tk()
        root.withdraw()
        available = font_name in root.tk.call("font", "families")
        root.destroy()
        return available
    except Exception:
        return False


def get_ui_font():
    cfg = get_font_config()
    for font in cfg["cjk"]:
        if font and check_font_available(font):
            return font
    return cfg["fallback"]


class SimpleChart(tk.Toplevel):
    def __init__(self, parent, timestamps, latencies, errors, host, translations, dpi_scale=1.0):
        super().__init__(parent)
        self.translations = translations
        self.dpi_scale = dpi_scale
        self.title(f"{translations['chart_title']} - {host}")
        self.geometry(f"{int(CHART_WIDTH * dpi_scale)}x{int(CHART_HEIGHT * dpi_scale)}")
        self.minsize(int(CHART_WIDTH * 0.75), int(CHART_HEIGHT * 0.75))

        self.timestamps = timestamps
        self.latencies = latencies
        self.errors = errors
        self.host = host
        self.ui_font = get_ui_font()

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=int(10 * dpi_scale), pady=int(10 * dpi_scale))

        self.bind("<Configure>", lambda _e: self.draw_chart())

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=int(10 * dpi_scale), pady=int(5 * dpi_scale))

        chart_btn_width = 16 if translations.get("save_chart", "").startswith("Save") else 12
        ttk.Button(
            btn_frame,
            text=translations["save_chart"],
            command=self.save_chart,
            width=chart_btn_width,
        ).pack(side="right")

    def _scale(self, value):
        return int(value * self.dpi_scale)

    def _measure_text(self, text, size, weight="normal"):
        font = (self.ui_font, size, weight) if weight != "normal" else (self.ui_font, size)
        item = self.canvas.create_text(0, 0, text=text, anchor="nw", font=font)
        bbox = self.canvas.bbox(item)
        self.canvas.delete(item)
        if not bbox:
            return 0, 0
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def _fit_font(self, desired, minimum, width_budget, text, weight="normal"):
        size = desired
        while size > minimum:
            text_width, _ = self._measure_text(text, size, weight)
            if text_width <= width_budget:
                return size
            size -= 1
        return minimum

    def draw_chart(self):
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 260 or h < 200:
            return

        if self.dpi_scale <= 1.2:
            legend_size = 11
        elif self.dpi_scale <= 1.8:
            legend_size = 10
        else:
            legend_size = 9

        latency_text = self.translations["chart_latency"]
        loss_text = self.translations["chart_packet_loss"]

        latency_width, latency_height = self._measure_text(latency_text, legend_size)
        loss_width, loss_height = self._measure_text(loss_text, legend_size)

        legend_text_width = max(latency_width, loss_width)
        legend_line_height = max(latency_height, loss_height, self._scale(14))
        legend_icon_width = self._scale(14)
        legend_gap = self._scale(8)
        legend_inner_pad = self._scale(10)

        legend_box_width = legend_inner_pad * 2 + legend_icon_width + legend_gap + legend_text_width
        legend_box_height = legend_inner_pad * 2 + legend_line_height * 2 + self._scale(8)

        min_right_margin = self._scale(135)
        right_margin = max(min_right_margin, legend_box_width + self._scale(24))

        margin = {
            "top": self._scale(60),
            "right": right_margin,
            "bottom": self._scale(90),
            "left": self._scale(90),
        }

        x0 = margin["left"]
        y0 = h - margin["bottom"]
        x1 = w - margin["right"]
        y1 = margin["top"] + self._scale(35)

        chart_w = max(80, x1 - x0)
        chart_h = max(80, y0 - y1)

        valid = [
            (i, ts, lat)
            for i, (ts, lat) in enumerate(zip(self.timestamps, self.latencies))
            if lat is not None
        ]
        loss_idx = [i for i, err in enumerate(self.errors) if err == "timeout"]

        if not valid and not loss_idx:
            self.canvas.create_text(
                w // 2,
                h // 2,
                text=self.translations["output_no_data"],
                font=(self.ui_font, 14),
            )
            return

        all_lats = [lat for _, _, lat in valid] if valid else [0.0]
        current_max_lat = max(max(all_lats) * 1.2, 1.0)
        max_idx = max(1, len(self.latencies) - 1)

        title_text = f"{self.translations['chart_title']} - {self.host}"
        title_size = self._fit_font(
            desired=16,
            minimum=11,
            width_budget=int(w * 0.75),
            text=title_text,
            weight="bold",
        )
        self.canvas.create_text(
            w // 2,
            self._scale(25),
            text=title_text,
            font=(self.ui_font, title_size, "bold"),
        )

        self.canvas.create_line(x0, y1, x0, y0, width=2)
        self.canvas.create_line(x0, y0, x1, y0, width=2)

        tick_size = 10
        for i in range(6):
            y_val = current_max_lat * i / 5
            y_pos = y0 - (chart_h * i / 5)
            self.canvas.create_text(
                x0 - self._scale(10),
                y_pos + self._scale(2),
                text=f"{y_val:.1f}",
                anchor="e",
                font=(self.ui_font, tick_size),
            )
            if i > 0:
                self.canvas.create_line(
                    x0,
                    y_pos,
                    x1,
                    y_pos,
                    fill="#E0E0E0",
                    dash=(4, 4),
                )

        self.canvas.create_text(
            self._scale(25),
            y1 + chart_h / 2,
            text=self.translations["chart_latency"],
            angle=90,
            font=(self.ui_font, 11),
        )

        if valid:
            points = []
            for idx, _ts, lat in valid:
                x = x0 + (idx / max_idx) * chart_w
                y = y0 - (lat / current_max_lat) * chart_h
                points.extend([x, y])

                dot_size = max(3, int(3 * self.dpi_scale))
                color = "#2196F3" if lat < 100 else "#FF9800" if lat < 300 else "#F44336"
                self.canvas.create_oval(
                    x - dot_size,
                    y - dot_size,
                    x + dot_size,
                    y + dot_size,
                    fill=color,
                    outline=color,
                )

            if len(points) >= 4:
                self.canvas.create_line(points, fill="#2196F3", width=2)

        for idx in loss_idx:
            x = x0 + (idx / max_idx) * chart_w
            y = y0 - chart_h * 0.05
            self.canvas.create_text(
                x,
                y,
                text="X",
                fill="red",
                font=(self.ui_font, 12, "bold"),
            )

        tick_positions = sorted({0, max_idx // 2, max_idx})
        for idx in tick_positions:
            if idx < len(self.timestamps):
                x = x0 + (idx / max_idx) * chart_w
                self.canvas.create_text(
                    x,
                    y0 + self._scale(20),
                    text=self.timestamps[idx].strftime("%H:%M:%S"),
                    font=(self.ui_font, tick_size),
                )

        # 图例安全布局：
        # 放在绘图区右侧 margin 内，而不是 w - 15 往右画。
        legend_box_left = x1 + self._scale(16)
        legend_box_right = min(w - self._scale(8), legend_box_left + legend_box_width)
        legend_box_left = max(x1 + self._scale(8), legend_box_right - legend_box_width)

        legend_box_top = y1
        legend_box_bottom = min(h - self._scale(80), legend_box_top + legend_box_height)

        if legend_box_bottom > legend_box_top + self._scale(35):
            self.canvas.create_rectangle(
                legend_box_left,
                legend_box_top,
                legend_box_right,
                legend_box_bottom,
                outline="#DDDDDD",
                fill="#FFFFFF",
            )

            icon_x = legend_box_left + legend_inner_pad
            text_x = icon_x + legend_icon_width + legend_gap

            line1_y = legend_box_top + legend_inner_pad + legend_line_height / 2
            line2_y = line1_y + legend_line_height + self._scale(8)

            dot_r = max(4, self._scale(4))
            self.canvas.create_oval(
                icon_x,
                line1_y - dot_r,
                icon_x + dot_r * 2,
                line1_y + dot_r,
                fill="#2196F3",
                outline="#2196F3",
            )
            self.canvas.create_text(
                text_x,
                line1_y,
                text=latency_text,
                anchor="w",
                font=(self.ui_font, legend_size),
                fill="#222222",
            )

            self.canvas.create_text(
                icon_x + dot_r,
                line2_y,
                text="X",
                fill="red",
                font=(self.ui_font, legend_size, "bold"),
            )
            self.canvas.create_text(
                text_x,
                line2_y,
                text=loss_text,
                anchor="w",
                fill="red",
                font=(self.ui_font, legend_size),
            )

        total = len(self.latencies)
        loss = len([e for e in self.errors if e == "timeout"])
        avg_lat = sum(lat for _, _, lat in valid) / len(valid) if valid else 0
        min_lat = min(all_lats) if valid else 0
        max_lat_val = max(all_lats) if valid else 0

        stats_text = (
            f"{self.translations['total_packets']}: {total} | "
            f"{self.translations['lost_packets']}: {loss} ({(loss / total * 100) if total else 0:.1f}%) | "
            f"{self.translations['avg_latency']}: {avg_lat:.1f}ms | "
            f"{self.translations['min_latency']}: {min_lat:.1f}ms | "
            f"{self.translations['max_latency']}: {max_lat_val:.1f}ms"
        )
        stats_size = self._fit_font(
            desired=11,
            minimum=8,
            width_budget=int(w * 0.95),
            text=stats_text,
            weight="bold",
        )
        self.canvas.create_text(
            w // 2,
            h - self._scale(18),
            text=stats_text,
            font=(self.ui_font, stats_size, "bold"),
            fill="#333333",
        )

    def _save_canvas_as_png(self, path):
        if not DEPENDENCY_STATUS["pillow"]:
            raise RuntimeError(self.translations["save_png_missing_pillow"])

        from PIL import ImageGrab

        self.update_idletasks()
        self.canvas.update_idletasks()

        try:
            self.lift()
            self.focus_force()
            self.update()
        except Exception:
            pass

        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w <= 1 or h <= 1:
            raise RuntimeError("Canvas size is invalid")

        bbox = (x, y, x + w, y + h)

        try:
            image = ImageGrab.grab(bbox=bbox, all_screens=True)
        except TypeError:
            image = ImageGrab.grab(bbox=bbox)

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        image.save(path, "PNG")

    def save_chart(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("All Files", "*.*")],
            initialfile=f"ping_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        )
        if not path:
            return

        if not path.lower().endswith(".png"):
            path = replace_extension(path, ".png")

        try:
            self._save_canvas_as_png(path)
            messagebox.showinfo(
                self.translations["dialog_save_success"],
                f"{self.translations['save_png_success']}\n{path}",
            )
        except Exception as exc:
            messagebox.showerror(
                self.translations["error_host"],
                f"{self.translations['save_png_failed']}\n{exc}",
            )


class SaveDialog:
    def __init__(self, parent, translations, timeout=SAVE_DIALOG_TIMEOUT):
        self.parent = parent
        self.translations = translations
        self.timeout = timeout
        self.result = None
        self.dialog = None
        self.timer_id = None
        self.ui_font = get_ui_font()

    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.translations["dialog_title"])
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        dpi_scale = get_dpi_scale(self.dialog)
        width = int(SAVE_DIALOG_WIDTH * dpi_scale)
        height = int(SAVE_DIALOG_HEIGHT * dpi_scale)
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.minsize(int(width * 0.9), int(height * 0.9))

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - width) // 2
        y = (self.dialog.winfo_screenheight() - height) // 2
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

        label_size = max(10, int(BASE_FONT_SIZE * dpi_scale))
        ttk.Label(
            self.dialog,
            text=self.translations["dialog_message"],
            font=(self.ui_font, label_size),
            wraplength=int(width * 0.85),
        ).pack(pady=int(18 * dpi_scale), padx=int(12 * dpi_scale))

        self.countdown_var = tk.StringVar(value=f"{self.translations['dialog_timeout']} {self.timeout}")
        ttk.Label(
            self.dialog,
            textvariable=self.countdown_var,
            foreground="red",
            font=(self.ui_font, max(9, int(SMALL_FONT_SIZE * dpi_scale))),
        ).pack(pady=int(4 * dpi_scale))

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=int(18 * dpi_scale))
        btn_width = max(8, int(BUTTON_WIDTH * 0.9))

        ttk.Button(
            btn_frame,
            text=self.translations["dialog_save"],
            command=self.on_save,
            width=btn_width,
        ).pack(side="left", padx=8)
        ttk.Button(
            btn_frame,
            text=self.translations["dialog_discard"],
            command=self.on_discard,
            width=btn_width,
        ).pack(side="left", padx=8)
        ttk.Button(
            btn_frame,
            text=self.translations["dialog_cancel"],
            command=self.on_cancel,
            width=btn_width,
        ).pack(side="left", padx=8)

        self.remaining = self.timeout
        self._countdown()
        self.dialog.wait_window()
        return self.result

    def _safe_cancel_timer(self):
        if self.timer_id and self.dialog:
            try:
                self.dialog.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

    def _countdown(self):
        if self.remaining > 0 and self.result is None and self.dialog and self.dialog.winfo_exists():
            self.countdown_var.set(f"{self.translations['dialog_timeout']} {self.remaining}")
            self.remaining -= 1
            self.timer_id = self.dialog.after(1000, self._countdown)
        elif self.remaining <= 0 and self.result is None and self.dialog and self.dialog.winfo_exists():
            self.result = "timeout"
            self.dialog.destroy()

    def on_save(self):
        self.result = "save"
        self._safe_cancel_timer()
        self.dialog.destroy()

    def on_discard(self):
        self.result = "discard"
        self._safe_cancel_timer()
        self.dialog.destroy()

    def on_cancel(self):
        self.result = "cancel"
        self._safe_cancel_timer()
        self.dialog.destroy()


def ping_host(host, timeout=2, size=56):
    if ping is None:
        return None, "missing_ping3"
    try:
        rtt = ping(host, timeout=timeout, unit="ms", size=size)
        if rtt is None:
            return None, "timeout"
        return rtt, ""
    except PermissionError:
        return None, "permission"
    except socket.gaierror:
        return None, "resolve_fail"
    except OSError as exc:
        text = str(exc).lower()
        if "permission" in text or "operation not permitted" in text:
            return None, "permission"
        return None, f"error: {exc}"
    except Exception as exc:
        return None, f"error: {exc}"


def sleep_with_check(seconds, stop_event):
    end_time = time.time() + max(0, seconds)
    while time.time() < end_time:
        if stop_event and stop_event.is_set():
            return False
        time.sleep(min(0.1, max(0.0, end_time - time.time())))
    return True


def collect_data(host, count, interval, size, duration=None, callback=None, stop_event=None):
    start_time = time.time()
    i = 0

    while not (stop_event and stop_event.is_set()):
        if duration is not None and (time.time() - start_time) >= duration:
            break
        if count is not None and count > 0 and i >= count:
            break

        now = datetime.now()
        rtt, err = ping_host(host, size=size)

        if callback:
            try:
                callback((now, rtt, err))
            except Exception:
                traceback.print_exc()
                break

        i += 1

        if not sleep_with_check(interval, stop_event):
            break

    if callback:
        try:
            callback(None)
        except Exception:
            traceback.print_exc()


class PingApp:
    def __init__(self, root, lang="zh_CN"):
        self.root = root
        self.lang = lang
        self.translations = LANGUAGES.get(lang, LANGUAGES["zh_CN"])
        self.ui_font = get_ui_font()

        self.dpi_scale = get_dpi_scale(root)
        self.current_window_width = DEFAULT_WINDOW_WIDTH
        self.current_window_height = DEFAULT_WINDOW_HEIGHT
        self.font_size = BASE_FONT_SIZE
        self.small_font_size = SMALL_FONT_SIZE
        self.title_font_size = TITLE_FONT_SIZE

        self.root.title(self.translations["app_title"])
        self.root.resizable(True, True)

        self.host = tk.StringVar(value="www.bing.com")
        self.size = tk.StringVar(value="56")
        self.interval = tk.StringVar(value="1.0")
        self.mode = tk.StringVar(value="count")
        self.count = tk.StringVar(value="30")
        self.duration = tk.StringVar(value="")
        self.menu_lang_var = tk.StringVar(value=self.lang)

        self.ping_thread = None
        self.stop_event = threading.Event()
        self.data_queue = queue.Queue()
        self.after_id = None

        self.timestamps = []
        self.latencies = []
        self.errors = []
        self.last_chart_data = None
        self.total_pings = 0
        self.loss_count = 0
        self.stats_var = tk.StringVar(value=self._get_stats_text())

        self.chart_window = None
        self.last_dpi_scale = self.dpi_scale

        self.setup_style()
        self.apply_scaling()
        self.create_widgets()
        self.create_menu()

        self.root.bind("<Configure>", self.on_window_configure)
        self.root.after(300, self.show_dependency_warnings)

    def _get_running_state(self):
        state = {
            "log_content": self.output.get(1.0, tk.END) if hasattr(self, "output") else "",
            "timestamps": list(self.timestamps),
            "latencies": list(self.latencies),
            "errors": list(self.errors),
            "total_pings": self.total_pings,
            "loss_count": self.loss_count,
            "last_chart_data": self.last_chart_data,
        }

        if self.ping_thread and self.ping_thread.is_alive():
            state["ping_active"] = True
            state["data_queue"] = self.data_queue
            state["stop_event"] = self.stop_event
            if self.after_id:
                try:
                    self.root.after_cancel(self.after_id)
                except Exception:
                    pass
                self.after_id = None
        else:
            state["ping_active"] = False

        return state

    def _restore_running_state(self, state):
        if state.get("ping_active"):
            self.data_queue = state["data_queue"]
            self.stop_event = state["stop_event"]
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")

            class _PingThreadRef:
                def __init__(self, stop_event):
                    self._stop_event = stop_event

                def is_alive(self):
                    return not self._stop_event.is_set()

            self.ping_thread = _PingThreadRef(self.stop_event)
            self.after_id = self.root.after(QUEUE_POLL_MS, self.poll_queue)
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

        if hasattr(self, "output") and state["log_content"]:
            self.output.insert(tk.END, state["log_content"])
            self.output.see(tk.END)

        self.timestamps = state["timestamps"]
        self.latencies = state["latencies"]
        self.errors = state["errors"]
        self.total_pings = state["total_pings"]
        self.loss_count = state["loss_count"]
        self.last_chart_data = state["last_chart_data"]

        if self.total_pings > 0:
            self.update_stats_display()

        self._update_open_last_btn_state()

    def setup_style(self):
        style = ttk.Style()
        try:
            if sys.platform == "win32":
                style.theme_use("vista")
        except Exception:
            pass

        base = max(10, int(BASE_FONT_SIZE * self.dpi_scale))
        small = max(9, int(SMALL_FONT_SIZE * self.dpi_scale))

        style.configure(".", font=(self.ui_font, base))
        style.configure("TLabelframe.Label", font=(self.ui_font, base))
        style.configure("TButton", font=(self.ui_font, base))
        style.configure("TRadiobutton", font=(self.ui_font, base))
        style.configure("TLabel", font=(self.ui_font, base))
        style.configure("Small.TLabel", font=(self.ui_font, small))

    def apply_scaling(self):
        self.dpi_scale = get_dpi_scale(self.root)
        window_scale = min(self.dpi_scale, 1.6)

        if self.lang == "en_US":
            base_width = DEFAULT_WINDOW_WIDTH_EN
            base_height = DEFAULT_WINDOW_HEIGHT_EN
        else:
            base_width = DEFAULT_WINDOW_WIDTH
            base_height = DEFAULT_WINDOW_HEIGHT

        self.current_window_width = int(base_width * window_scale)
        self.current_window_height = int(base_height * window_scale)

        font_scale = 1.0 + (self.dpi_scale - 1.0) * 0.45
        self.font_size = max(10, int(BASE_FONT_SIZE * font_scale))
        self.small_font_size = max(9, int(SMALL_FONT_SIZE * font_scale))
        self.title_font_size = max(11, int(TITLE_FONT_SIZE * font_scale))

        self.root.geometry(f"{self.current_window_width}x{self.current_window_height}")
        self.root.minsize(
            int(MIN_WINDOW_WIDTH * min(window_scale, 1.4)),
            int(MIN_WINDOW_HEIGHT * min(window_scale, 1.4)),
        )

        self.setup_style()

    def _get_stats_text(self):
        return (
            f"{self.translations['total_packets']}: 0 | "
            f"{self.translations['lost_packets']}: 0 | "
            f"{self.translations['loss_rate']}: 0.00%"
        )

    def _s(self, key):
        return self.translations.get(key, key)

    def show_dependency_warnings(self):
        if not MISSING_DEPS:
            return

        if "ping3" in MISSING_DEPS and len(MISSING_DEPS) == 1:
            msg = self._s("dependency_warn_ping3")
        elif len(MISSING_DEPS) == 1 and "Pillow" in MISSING_DEPS[0]:
            msg = self._s("dependency_warn_pillow")
        else:
            msg = self._s("dependency_warn_both").format(deps="\n".join(MISSING_DEPS))

        messagebox.showwarning(self._s("dependency_warn_title"), msg)

    def change_language(self, lang):
        saved_state = self._get_running_state()

        self.lang = lang
        self.translations = LANGUAGES.get(lang, LANGUAGES["zh_CN"])
        self.menu_lang_var.set(lang)
        self.root.title(self.translations["app_title"])

        self.apply_scaling()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.create_menu()
        self._restore_running_state(saved_state)

    def on_window_configure(self, event):
        if event.widget == self.root:
            new_dpi_scale = get_dpi_scale(self.root)
            if abs(new_dpi_scale - self.last_dpi_scale) > 0.05:
                self.last_dpi_scale = new_dpi_scale
                saved_state = self._get_running_state()

                self.apply_scaling()

                for widget in self.root.winfo_children():
                    widget.destroy()

                self.create_widgets()
                self.create_menu()
                self._restore_running_state(saved_state)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self._s("menu_language"), menu=lang_menu)

        for code, name in LANGUAGE_NAMES.items():
            lang_menu.add_radiobutton(
                label=name,
                value=code,
                variable=self.menu_lang_var,
                command=lambda c=code: self.change_language(c),
            )

        menubar.add_command(label=self._s("menu_about"), command=self.show_about)

    def show_about(self):
        messagebox.showinfo(self._s("about_title"), self._s("about_message"))

    def create_widgets(self):
        outer_pad_x = int(12 * min(self.dpi_scale, 1.4))
        outer_pad_y = int(8 * min(self.dpi_scale, 1.4))

        frame_in = ttk.LabelFrame(self.root, text=self._s("param_frame"), padding=12)
        frame_in.pack(fill="x", padx=outer_pad_x, pady=outer_pad_y)

        ttk.Label(frame_in, text=self._s("target_host")).grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.host_entry = ttk.Entry(frame_in, textvariable=self.host)
        self.host_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=6)

        ttk.Label(frame_in, text=self._s("packet_size")).grid(row=1, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(frame_in, textvariable=self.size).grid(row=1, column=1, sticky="w", padx=8, pady=6)

        ttk.Label(frame_in, text=self._s("interval")).grid(row=2, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(frame_in, textvariable=self.interval).grid(row=2, column=1, sticky="w", padx=8, pady=6)

        mode_frame = ttk.Frame(frame_in)
        mode_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=8)

        ttk.Radiobutton(
            mode_frame,
            text=self._s("count_mode"),
            variable=self.mode,
            value="count",
            command=self.on_mode_change,
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            mode_frame,
            text=self._s("duration_mode"),
            variable=self.mode,
            value="duration",
            command=self.on_mode_change,
        ).pack(side="left", padx=10)

        self.count_label = ttk.Label(frame_in, text=self._s("ping_count"))
        self.count_label.grid(row=4, column=0, sticky="w", padx=8, pady=6)

        self.count_entry = ttk.Entry(frame_in, textvariable=self.count)
        self.count_entry.grid(row=4, column=1, sticky="w", padx=8, pady=6)

        self.duration_label = ttk.Label(frame_in, text=self._s("duration"))
        self.duration_entry = ttk.Entry(frame_in, textvariable=self.duration)

        self.on_mode_change()
        frame_in.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=outer_pad_x, pady=outer_pad_y)

        for col in range(3):
            btn_frame.columnconfigure(col, weight=1, uniform="action_buttons")

        btn_width = 16 if self.lang == "zh_CN" else 18
        btn_pad_x = max(4, int(6 * min(self.dpi_scale, 1.2)))
        btn_pad_y = max(3, int(5 * min(self.dpi_scale, 1.2)))

        self.start_btn = ttk.Button(
            btn_frame,
            text=self._s("start_btn"),
            command=self.start_ping,
            width=btn_width,
        )
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=btn_pad_x, pady=btn_pad_y)

        self.stop_btn = ttk.Button(
            btn_frame,
            text=self._s("stop_btn"),
            command=self.stop_ping,
            state="disabled",
            width=btn_width,
        )
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=btn_pad_x, pady=btn_pad_y)

        self.open_last_btn = ttk.Button(
            btn_frame,
            text=self._s("open_last_chart"),
            command=self.open_last_chart,
            width=btn_width,
        )
        self.open_last_btn.grid(row=0, column=2, sticky="ew", padx=btn_pad_x, pady=btn_pad_y)
        self._update_open_last_btn_state()

        out_frame = ttk.LabelFrame(self.root, text=self._s("output_frame"), padding=8)
        out_frame.pack(fill="both", expand=True, padx=outer_pad_x, pady=outer_pad_y)

        output_height = max(12, int(15 * min(self.dpi_scale, 1.3)))
        self.output = scrolledtext.ScrolledText(
            out_frame,
            wrap="word",
            height=output_height,
            font=(self.ui_font, self.small_font_size),
        )
        self.output.pack(fill="both", expand=True)

        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=outer_pad_x, pady=(0, outer_pad_y))

        ttk.Label(
            status_frame,
            textvariable=self.stats_var,
            foreground="blue",
            style="Small.TLabel",
        ).pack(side="left")

    def on_mode_change(self):
        if self.mode.get() == "count":
            self.count_label.grid()
            self.count_entry.grid()
            self.duration_label.grid_remove()
            self.duration_entry.grid_remove()
        else:
            self.count_label.grid_remove()
            self.count_entry.grid_remove()
            self.duration_label.grid(row=4, column=0, sticky="w", padx=5, pady=4)
            self.duration_entry.grid(row=4, column=1, sticky="w", padx=5, pady=4)

    def _update_open_last_btn_state(self):
        if hasattr(self, "open_last_btn") and self.open_last_btn.winfo_exists():
            if self.last_chart_data and self.last_chart_data.get("timestamps"):
                self.open_last_btn.config(state="normal")
            else:
                self.open_last_btn.config(state="disabled")

    def open_last_chart(self):
        if not self.last_chart_data or not self.last_chart_data.get("timestamps"):
            messagebox.showinfo(self._s("app_title"), self._s("no_chart_data"))
            return

        if self.chart_window and self.chart_window.winfo_exists():
            self.chart_window.destroy()

        self.chart_window = SimpleChart(
            self.root,
            self.last_chart_data["timestamps"],
            self.last_chart_data["latencies"],
            self.last_chart_data["errors"],
            self.last_chart_data["host"],
            self.translations,
            self.dpi_scale,
        )

    def validate_inputs(self):
        host = self.host.get().strip()
        if not host:
            messagebox.showerror(self._s("error_host"), self._s("error_host_msg"))
            return None

        size_str = self.size.get().strip()
        if not size_str:
            messagebox.showerror(self._s("error_host"), self._s("error_size"))
            return None

        try:
            size = int(size_str)
            if size <= 0:
                messagebox.showerror(self._s("error_host"), self._s("error_size_positive"))
                return None
        except ValueError:
            messagebox.showerror(self._s("error_host"), self._s("error_size_int"))
            return None

        try:
            interval = float(self.interval.get().strip())
            if interval <= 0:
                messagebox.showerror(self._s("error_host"), self._s("error_interval_positive"))
                return None
            if interval < MIN_INTERVAL_SECONDS:
                messagebox.showerror(self._s("error_host"), self._s("error_interval_too_small"))
                return None
        except Exception:
            messagebox.showerror(self._s("error_host"), self._s("error_interval"))
            return None

        count = None
        duration = None

        if self.mode.get() == "count":
            count_str = self.count.get().strip()
            if count_str == "":
                count = None
            else:
                try:
                    count = int(count_str)
                    if count < 0:
                        messagebox.showerror(self._s("error_host"), self._s("error_count_negative"))
                        return None
                    if count == 0:
                        count = None
                except ValueError:
                    messagebox.showerror(self._s("error_host"), self._s("error_count"))
                    return None
        else:
            dur_str = self.duration.get().strip()
            if dur_str == "":
                messagebox.showerror(self._s("error_host"), self._s("error_duration"))
                return None
            try:
                duration = float(dur_str)
                if duration <= 0:
                    messagebox.showerror(self._s("error_host"), self._s("error_duration_positive"))
                    return None
            except ValueError:
                messagebox.showerror(self._s("error_host"), self._s("error_duration_number"))
                return None

        return host, size, interval, count, duration

    def start_ping(self):
        params = self.validate_inputs()
        if not params:
            return

        if ping is None:
            self.show_dependency_warnings()
            return

        host, size, interval, count, duration = params

        try:
            ip = socket.gethostbyname(host)
            resolve_msg = f"{self._s('chart_resolve')} {host} -> {ip}\n"
        except Exception as exc:
            messagebox.showerror(self._s("error_host"), f"{self._s('error_resolve')}: {exc}")
            return

        self.timestamps.clear()
        self.latencies.clear()
        self.errors.clear()
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, resolve_msg)
        self.output.see(tk.END)

        self.data_queue = queue.Queue()
        self.total_pings = 0
        self.loss_count = 0
        self.stats_var.set(self._get_stats_text())

        self.stop_event = threading.Event()
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        self.ping_thread = threading.Thread(
            target=collect_data,
            args=(ip, count, interval, size),
            kwargs={
                "duration": duration,
                "callback": self.data_queue.put,
                "stop_event": self.stop_event,
            },
            daemon=True,
        )
        self.ping_thread.start()

        self.after_id = self.root.after(QUEUE_POLL_MS, self.poll_queue)

    def trim_data_if_needed(self):
        if len(self.timestamps) > MAX_POINTS_IN_MEMORY:
            overflow = len(self.timestamps) - MAX_POINTS_IN_MEMORY
            if overflow > 0:
                self.timestamps = self.timestamps[overflow:]
                self.latencies = self.latencies[overflow:]
                self.errors = self.errors[overflow:]

    def update_stats_display(self):
        timeout_count = len([e for e in self.errors if e == "timeout"])
        loss_rate = (timeout_count / self.total_pings) * 100 if self.total_pings else 0
        valid_lats = [l for l in self.latencies if l is not None]
        avg_lat = sum(valid_lats) / len(valid_lats) if valid_lats else 0

        self.stats_var.set(
            f"{self._s('total_packets')}: {self.total_pings} | "
            f"{self._s('lost_packets')}: {timeout_count} | "
            f"{self._s('loss_rate')}: {loss_rate:.2f}% | "
            f"{self._s('avg_latency')}: {avg_lat:.1f}ms"
        )

    def poll_queue(self):
        try:
            while True:
                item = self.data_queue.get_nowait()

                if item is None:
                    self.ping_finished()
                    return

                ts, rtt, err = item

                self.timestamps.append(ts)
                self.latencies.append(rtt)
                self.errors.append(err)
                self.total_pings += 1

                if err == "timeout":
                    self.loss_count += 1

                self.trim_data_if_needed()
                self.update_stats_display()

                if rtt is not None:
                    status = f"{rtt:.2f} ms"
                elif err == "timeout":
                    status = self._s("output_timeout")
                elif err == "resolve_fail":
                    status = self._s("output_resolve_fail")
                elif err == "permission":
                    status = self._s("output_permission")
                elif err == "missing_ping3":
                    status = self._s("output_missing_ping3")
                else:
                    status = f"{self._s('output_error')}: {err}"

                self.output.insert(tk.END, f"{ts.strftime('%H:%M:%S')} - {status}\n")
                self.output.see(tk.END)

        except queue.Empty:
            pass

        if self.ping_thread and self.ping_thread.is_alive():
            self.after_id = self.root.after(QUEUE_POLL_MS, self.poll_queue)
        else:
            self.ping_finished()

    def ping_finished(self):
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        if not self.timestamps:
            return

        if self.chart_window and self.chart_window.winfo_exists():
            dlg = SaveDialog(self.root, self.translations, timeout=SAVE_DIALOG_TIMEOUT)
            res = dlg.show()

            if res == "save":
                self.chart_window.save_chart()
                self.chart_window.destroy()
            elif res in ("discard", "timeout"):
                self.chart_window.destroy()
            elif res == "cancel":
                self.output.insert(tk.END, f"{self._s('output_cancel')}\n")
                self.output.see(tk.END)
                return

        self.chart_window = SimpleChart(
            self.root,
            self.timestamps[:],
            self.latencies[:],
            self.errors[:],
            self.host.get(),
            self.translations,
            self.dpi_scale,
        )

        self.last_chart_data = {
            "timestamps": self.timestamps[:],
            "latencies": self.latencies[:],
            "errors": self.errors[:],
            "host": self.host.get(),
        }

        self._update_open_last_btn_state()

    def stop_ping(self):
        if self.stop_event:
            self.stop_event.set()


if __name__ == "__main__":
    setup_high_dpi()

    root = tk.Tk()
    configure_tkinter_dpi(root)

    default_lang = "zh_CN"

    try:
        import locale

        try:
            system_lang = locale.getlocale()[0] or locale.getdefaultlocale()[0]
        except (AttributeError, TypeError):
            system_lang = locale.getdefaultlocale()[0]

        if system_lang:
            if system_lang in LANGUAGES:
                default_lang = system_lang
            elif system_lang.split("_")[0] == "en":
                default_lang = "en_US"
            else:
                default_lang = "zh_CN"
    except Exception:
        pass

    app = PingApp(root, lang=default_lang)
    root.mainloop()