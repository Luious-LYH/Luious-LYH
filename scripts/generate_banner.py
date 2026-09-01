import json
import urllib.request
from datetime import datetime, timezone, timedelta
import os

# ==================== 1. 配置参数 ====================
USER_NAME = "Yuhao Liu (Luious-LYH)"                   # 显示在 Banner 上的名字
STATUS_TITLE = "M.Eng. @ SZU · Multimodal & Medical AI"  # 个人简介/头衔
CITY_NAME = "Shenzhen, China"                          # 城市名称
LATITUDE = 22.5431                                     # 深圳纬度
LONGITUDE = 114.0579                                   # 深圳经度
TIMEZONE_OFFSET = 8                                    # 时区设置 (北京时间 UTC+8)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "dynamic-banner.svg")

# ==================== 2. 获取时间与天气函数 ====================
def get_beijing_time():
    """获取指定的北京时间"""
    tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
    return datetime.now(tz)

def get_weather(lat, lon):
    """从 Open-Meteo 获取免费实时天气"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GitHub-Profile-Banner/1.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            temp = data['current_weather']['temperature']
            wcode = data['current_weather']['weathercode']
            return f"{temp}°C", wcode
    except Exception as e:
        print(f"Weather fetch fallback due to: {e}")
        return "26°C", 0

# ==================== 3. 昼夜色彩主题配置 ====================
def get_theme_palette(hour):
    """根据当前小时数返回不同的色彩配置方案（马卡龙清新温馨风）"""
    # 晨曦 / 白昼 (06:00 - 17:00)
    if 6 <= hour < 17:
        return {
            "period_name": "Daylight Ocean",
            "sky_top": "#BAE6FD", "sky_bottom": "#E0F2FE",
            "sun_moon_color": "#FBBF24", "sun_moon_radius": 24, "sun_y": 70,
            "sea_deep": "#0284C7", "sea_mid": "#38BDF8", "sea_light": "#BAE6FD",
            "window_light_opacity": "0.15",
            "lamp_glow": "rgba(253, 230, 138, 0.4)",
            "dot_color": "#10B981",
            "is_night": False
        }
    # 黄昏 / 日落 (17:00 - 19:00)
    elif 17 <= hour < 19:
        return {
            "period_name": "Golden Sunset",
            "sky_top": "#FDBA74", "sky_bottom": "#FDE68A",
            "sun_moon_color": "#F97316", "sun_moon_radius": 28, "sun_y": 100,
            "sea_deep": "#0369A1", "sea_mid": "#0284C7", "sea_light": "#FDBA74",
            "window_light_opacity": "0.25",
            "lamp_glow": "rgba(251, 191, 36, 0.6)",
            "dot_color": "#F59E0B",
            "is_night": False
        }
    # 夜晚 / 极夜蓝 (19:00 - 06:00)
    else:
        return {
            "period_name": "Night Serenity",
            "sky_top": "#0F172A", "sky_bottom": "#1E293B",
            "sun_moon_color": "#FEF08A", "sun_moon_radius": 20, "sun_y": 60,
            "sea_deep": "#0A2540", "sea_mid": "#0369A1", "sea_light": "#38BDF8",
            "window_light_opacity": "0.05",
            "lamp_glow": "rgba(254, 240, 138, 0.8)",
            "dot_color": "#818CF8",
            "is_night": True
        }

# ==================== 4. 渲染矢量 SVG ====================
def generate_svg():
    now = get_beijing_time()
    temp_str, _ = get_weather(LATITUDE, LONGITUDE)
    theme = get_theme_palette(now.hour)
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%b %d, %Y")

    # 根据昼夜切换天空装饰物 (云朵或星星)
    if theme["is_night"]:
        sky_decorations = """
      <!-- 星空微闪 -->
      <circle class="star-1" cx="80" cy="40" r="1.5" fill="#FEF08A" opacity="0.8"/>
      <circle class="star-2" cx="140" cy="65" r="2" fill="#FFFFFF" opacity="0.9"/>
      <circle class="star-1" cx="210" cy="30" r="1.5" fill="#FEF08A" opacity="0.7"/>
      <circle class="star-3" cx="330" cy="50" r="1.8" fill="#FFFFFF" opacity="0.85"/>
      <circle class="star-2" cx="50" cy="85" r="1.2" fill="#FFFFFF" opacity="0.6"/>
      <circle class="star-3" cx="180" cy="95" r="1.6" fill="#FEF08A" opacity="0.75"/>
        """
    else:
        sky_decorations = """
      <!-- 动态微云 -->
      <g class="cloud-1" opacity="0.75">
        <path d="M40 70 Q55 60 70 70 Q85 60 100 70 Q110 80 100 90 L40 90 Z" fill="#FFFFFF"/>
      </g>
      <g class="cloud-2" opacity="0.6">
        <path d="M220 50 Q235 42 250 50 Q265 42 280 50 Q290 60 280 70 L220 70 Z" fill="#FFFFFF"/>
      </g>
        """

    # 构建 SVG 字符串
    svg_content = f"""<svg width="840" height="340" viewBox="0 0 840 340" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 天空渐变 -->
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{theme['sky_top']}"/>
      <stop offset="100%" stop-color="{theme['sky_bottom']}"/>
    </linearGradient>

    <!-- 室内暖白渐变 (马卡龙暖白) -->
    <linearGradient id="wallGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="100%" stop-color="#FEF9EE"/>
    </linearGradient>

    <!-- 台灯光晕径向渐变 -->
    <radialGradient id="lampGlow" cx="720" cy="180" r="140" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{theme['lamp_glow']}"/>
      <stop offset="100%" stop-color="rgba(254, 249, 238, 0)"/>
    </radialGradient>

    <!-- 柔和阴影滤镜 -->
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.06"/>
    </filter>
  </defs>

  <style>
    .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; }}
    
    /* 动态波浪 */
    @keyframes waveMove {{
      0% {{ transform: translateX(0); }}
      50% {{ transform: translateX(-25px); }}
      100% {{ transform: translateX(0); }}
    }}
    .wave-1 {{ animation: waveMove 8s ease-in-out infinite; }}
    .wave-2 {{ animation: waveMove 12s ease-in-out infinite reverse; }}

    /* 浮云飘动 */
    @keyframes cloudDrift {{
      0% {{ transform: translateX(0); }}
      50% {{ transform: translateX(18px); }}
      100% {{ transform: translateX(0); }}
    }}
    .cloud-1 {{ animation: cloudDrift 16s ease-in-out infinite; }}
    .cloud-2 {{ animation: cloudDrift 22s ease-in-out infinite reverse; }}

    /* 星星闪烁 */
    @keyframes twinkle {{
      0%, 100% {{ opacity: 0.3; transform: scale(0.8); }}
      50% {{ opacity: 1; transform: scale(1.2); }}
    }}
    .star-1 {{ animation: twinkle 3s ease-in-out infinite; }}
    .star-2 {{ animation: twinkle 4.5s ease-in-out infinite 1s; }}
    .star-3 {{ animation: twinkle 3.5s ease-in-out infinite 2s; }}

    /* 咖啡热气升腾 */
    @keyframes steamFloat {{
      0% {{ transform: translateY(0) scaleX(1); opacity: 0; }}
      50% {{ opacity: 0.6; }}
      100% {{ transform: translateY(-16px) scaleX(1.4); opacity: 0; }}
    }}
    .steam-line {{ animation: steamFloat 3s ease-out infinite; }}

    /* 光标闪烁 */
    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
    .cursor {{ animation: blink 1.1s infinite; }}
  </style>

  <!-- 1. 背景主底色 (暖白墙面) -->
  <rect width="840" height="340" rx="16" fill="url(#wallGrad)"/>

  <!-- 2. 左侧落地观海窗 (蓝白海景系统) -->
  <g transform="translate(24, 20)" filter="url(#softShadow)">
    <!-- 窗框与窗外背景剪裁 -->
    <mask id="windowMask">
      <rect width="380" height="230" rx="14" fill="#FFFFFF"/>
    </mask>

    <g mask="url(#windowMask)">
      <!-- 天空 -->
      <rect width="380" height="230" fill="url(#skyGrad)"/>

      <!-- 太阳 / 月亮 -->
      <circle cx="290" cy="{theme['sun_y']}" r="{theme['sun_moon_radius']}" fill="{theme['sun_moon_color']}" opacity="0.92"/>

      {sky_decorations}

      <!-- 远景海平面 -->
      <rect y="125" width="380" height="105" fill="{theme['sea_deep']}"/>

      <!-- 动态海浪层 1 -->
      <path class="wave-2" d="M-40 145 C20 140, 80 150, 140 145 C200 140, 260 150, 320 145 C380 140, 440 150, 500 145 L500 230 L-40 230 Z" fill="{theme['sea_mid']}" opacity="0.85"/>

      <!-- 动态海浪层 2 (前浪带白浪花) -->
      <path class="wave-1" d="M-40 168 C30 162, 90 174, 150 168 C210 162, 270 174, 330 168 C390 162, 450 174, 510 168 L510 230 L-40 230 Z" fill="{theme['sea_light']}"/>
      <path class="wave-1" d="M-40 168 C30 162, 90 174, 150 168 C210 162, 270 174, 330 168 C390 162, 450 174, 510 168" stroke="#FFFFFF" stroke-width="2.5" fill="none" opacity="0.8"/>
    </g>

    <!-- 极简白色实木窗框 -->
    <rect width="380" height="230" rx="14" fill="none" stroke="#FFFFFF" stroke-width="6"/>
    <!-- 垂直窗格线 -->
    <line x1="190" y1="0" x2="190" y2="230" stroke="#FFFFFF" stroke-width="3" opacity="0.8"/>
  </g>

  <!-- 3. 台灯暖光区 (右侧工位氛围) -->
  <circle cx="720" cy="180" r="140" fill="url(#lampGlow)"/>

  <!-- 4. 暖黄马卡龙工位桌面与设备 -->
  <!-- 桌面主体 (奶油黄) -->
  <path d="M0 240 L840 240 L840 340 L0 340 Z" fill="#FEF3C7"/>
  <!-- 桌面边缘厚度实木条 (温暖杏黄) -->
  <rect y="240" width="840" height="6" fill="#FDE68A"/>

  <!-- 右侧笔记本电脑 -->
  <g transform="translate(480, 156)" filter="url(#softShadow)">
    <!-- 屏幕外壳 (温润暖灰) -->
    <rect width="170" height="108" rx="6" fill="#475569"/>
    <!-- 屏幕显示区 (代码编辑器界面) -->
    <rect x="5" y="5" width="160" height="98" rx="3" fill="#1E293B"/>
    
    <!-- 屏幕内代码行与提示 -->
    <text x="14" y="24" fill="#38BDF8" font-size="9" font-weight="bold" class="font-sans">from</text>
    <text x="42" y="24" fill="#FDE68A" font-size="9" class="font-sans">torch.nn</text>
    <text x="88" y="24" fill="#38BDF8" font-size="9" font-weight="bold" class="font-sans">import</text>
    <text x="124" y="24" fill="#FFFFFF" font-size="9" class="font-sans">Module</text>
    
    <text x="14" y="42" fill="#94A3B8" font-size="8" class="font-sans"># Focus: VLM &amp; Medical Seg</text>
    <text x="14" y="56" fill="#4ADE80" font-size="8" class="font-sans">&gt; RDFBNet (TMM): Ready</text>
    <text x="14" y="70" fill="#F472B6" font-size="8" class="font-sans">&gt; PromptAdapter: Active</text>
    
    <!-- 命令行闪烁光标 -->
    <rect x="14" y="80" width="6" height="8" fill="#38BDF8" class="cursor"/>

    <!-- 笔记本转轴与键盘底座 -->
    <path d="M-15 108 L185 108 L175 116 L-5 116 Z" fill="#CBD5E1"/>
  </g>

  <!-- 奶油黄马克杯 + 动态热气 -->
  <g transform="translate(430, 216)">
    <!-- 杯身 -->
    <rect width="24" height="28" rx="4" fill="#FDE68A"/>
    <path d="M24 222 C29 222, 29 232, 24 232" stroke="#FDE68A" stroke-width="3" fill="none"/>
    <!-- 咖啡液面 -->
    <ellipse cx="12" cy="2" rx="10" ry="2" fill="#78350F"/>
    <!-- 升腾热气 -->
    <path class="steam-line" d="M8 -4 C6 -10, 14 -12, 10 -18" stroke="#D97706" stroke-width="1.5" stroke-linecap="round" fill="none"/>
    <path class="steam-line" style="animation-delay: 1.5s;" d="M16 -3 C14 -8, 20 -11, 17 -17" stroke="#D97706" stroke-width="1.5" stroke-linecap="round" fill="none"/>
  </g>

  <!-- 极简暖黄台灯 -->
  <g transform="translate(710, 130)">
    <!-- 灯罩 -->
    <path d="M-20 40 L20 40 L12 15 L-12 15 Z" fill="#FDE68A"/>
    <!-- 灯柱支架 -->
    <path d="M0 40 L0 115" stroke="#D97706" stroke-width="3" stroke-linecap="round"/>
    <!-- 底座 -->
    <rect x="-15" y="115" width="30" height="5" rx="2" fill="#D97706"/>
  </g>

  <!-- 窗台微型多肉盆栽 -->
  <g transform="translate(370, 222)">
    <path d="M4 14 L20 14 L17 26 L7 26 Z" fill="#FDBA74"/>
    <circle cx="12" cy="10" r="5" fill="#86EFAC"/>
    <circle cx="8" cy="12" r="4" fill="#4ADE80"/>
    <circle cx="16" cy="12" r="4" fill="#4ADE80"/>
  </g>

  <!-- 5. 信息标签与实时状态 (Top-Right HUD) -->
  <g transform="translate(430, 30)">
    <!-- 个人名与方向 -->
    <text x="0" y="22" fill="#1E293B" font-size="19" font-weight="700" class="font-sans">{USER_NAME}</text>
    <text x="0" y="44" fill="#64748B" font-size="12" font-weight="500" class="font-sans">{STATUS_TITLE}</text>

    <!-- 实时动态 Capsule (城市 · 天气 · 时间 · 模式) -->
    <g transform="translate(0, 60)" filter="url(#softShadow)">
      <rect width="370" height="32" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.2"/>
      <!-- 小圆点指示灯 -->
      <circle cx="16" cy="16" r="4" fill="{theme['dot_color']}"/>
      <!-- 状态文字 -->
      <text x="28" y="20" fill="#475569" font-size="11" font-weight="500" class="font-sans">
        {CITY_NAME} · {temp_str} · {time_str} ({theme['period_name']})
      </text>
      <!-- 日期 -->
      <text x="354" y="20" text-anchor="end" fill="#94A3B8" font-size="10" class="font-sans">{date_str}</text>
    </g>
  </g>
</svg>"""

    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # 将内容写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Dynamic banner successfully generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_svg()
