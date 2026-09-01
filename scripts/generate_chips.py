"""
Generate blue-themed tech chip SVGs in yuki4266 style.
Each chip has: rounded pill shape, subtle float animation, fade-in, icon + label.
Color scheme: macaron blue (#0284C7 accent, #38BDF8 highlight, #7DD3FC soft)
"""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chips")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Blue palette
ACCENT = "#0284C7"       # deep sky blue
HIGHLIGHT = "#38BDF8"    # bright sky blue
SOFT = "#7DD3FC"         # soft sky blue
LABEL_COLOR = "#64748B"  # slate gray for category labels
FLOWER_OUTER = "#38BDF8" # flower petals
FLOWER_INNER = "#0284C7" # flower center

# ============ Label (category header) chips ============
LABELS = {
    "label-0": ("MODELS", 85),
    "label-1": ("VISION", 78),
    "label-2": ("TUNING", 80),
    "label-3": ("DEPLOY", 82),
    "label-4": ("LANG / OPS", 100),
}

def make_label_svg(text, width):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 30" width="{width}" height="30" font-family="Segoe UI, Ubuntu, Helvetica, Arial, sans-serif"><title>{text}</title><g transform="translate(14,15)"><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/><circle cx="0" cy="-6.5" r="3.4" fill="{FLOWER_OUTER}"/><circle cx="6.2" cy="-2" r="3.4" fill="{FLOWER_OUTER}"/><circle cx="3.8" cy="5.3" r="3.4" fill="{FLOWER_OUTER}"/><circle cx="-3.8" cy="5.3" r="3.4" fill="{FLOWER_OUTER}"/><circle cx="-6.2" cy="-2" r="3.4" fill="{FLOWER_OUTER}"/></g><circle r="2.8" fill="{FLOWER_INNER}"/></g><text x="30" y="19" font-size="11" letter-spacing="1.5" fill="{LABEL_COLOR}">{text}</text></svg>
'''

# ============ Tech chip template ============
def make_chip_svg(name, icon_path, width, color=ACCENT, dur="3.7s", delay="-0.6s"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 30" width="{width}" height="30" font-family="Segoe UI, Ubuntu, Helvetica, Arial, sans-serif"><title>{name}</title><g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0s" dur="0.5s" fill="freeze"/><g><animateTransform attributeName="transform" type="translate" values="0 1.2;0 -1.2;0 1.2" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1" dur="{dur}" begin="{delay}" repeatCount="indefinite"/><rect x="1" y="4" width="{width-2}" height="22" rx="11" fill="{color}" fill-opacity="0.07" stroke="{color}" stroke-width="1.3"/><g transform="translate(12,8) scale(0.5833)">{icon_path}</g><text x="32" y="19" font-size="12" font-weight="600" fill="{color}">{name}</text></g></g></svg>
'''

# Simple circle icon for chips without complex paths
def make_simple_chip(name, width, color=ACCENT, dur="3.7s", delay="-0.6s"):
    icon = f'<circle cx="12" cy="12" r="8" fill="{color}" opacity="0.3"/><circle cx="12" cy="12" r="5" fill="{color}"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 30" width="{width}" height="30" font-family="Segoe UI, Ubuntu, Helvetica, Arial, sans-serif"><title>{name}</title><g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0s" dur="0.5s" fill="freeze"/><g><animateTransform attributeName="transform" type="translate" values="0 1.2;0 -1.2;0 1.2" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1" dur="{dur}" begin="{delay}" repeatCount="indefinite"/><rect x="1" y="4" width="{width-2}" height="22" rx="11" fill="{color}" fill-opacity="0.07" stroke="{color}" stroke-width="1.3"/><g transform="translate(12,8) scale(0.5833)">{icon}</g><text x="32" y="19" font-size="12" font-weight="600" fill="{color}">{name}</text></g></g></svg>
'''

# ============ Define all chips ============
# Format: (filename, display_name, width, color, dur, delay)
CHIPS = {
    # MODELS row
    "clip": ("CLIP", 74, ACCENT, "3.7s", "-0.6s"),
    "gpt": ("GPT", 68, ACCENT, "3.9s", "-1.2s"),
    "gemini": ("Gemini", 90, ACCENT, "4.1s", "-0.3s"),
    "llama": ("Llama", 82, ACCENT, "3.5s", "-1.8s"),
    "qwen": ("Qwen", 78, ACCENT, "3.8s", "-0.9s"),
    "sam": ("SAM", 70, ACCENT, "4.0s", "-1.5s"),
    "vit": ("ViT / DiT", 94, ACCENT, "3.6s", "-2.1s"),
    # VISION row
    "opencv": ("OpenCV", 92, HIGHLIGHT, "3.9s", "-0.4s"),
    "yolo": ("YOLO", 76, HIGHLIGHT, "4.2s", "-1.0s"),
    "unet": ("U-Net", 78, HIGHLIGHT, "3.7s", "-1.6s"),
    "medseg": ("Med Seg", 90, HIGHLIGHT, "3.5s", "-2.2s"),
    "vqa": ("VQA", 68, HIGHLIGHT, "4.0s", "-0.7s"),
    "depth": ("Depth", 80, HIGHLIGHT, "3.8s", "-1.3s"),
    # TUNING row
    "lora": ("LoRA", 74, ACCENT, "3.6s", "-0.5s"),
    "adapter": ("Adapter", 92, ACCENT, "4.1s", "-1.1s"),
    "prompt": ("Prompt", 86, ACCENT, "3.9s", "-1.7s"),
    "sft": ("SFT", 66, ACCENT, "3.7s", "-2.3s"),
    "dpo": ("DPO", 68, ACCENT, "4.3s", "-0.8s"),
    "rag": ("RAG", 66, ACCENT, "3.5s", "-1.4s"),
    "agent": ("Agents", 82, ACCENT, "3.8s", "-2.0s"),
    # DEPLOY row
    "tensorrt": ("TensorRT", 100, HIGHLIGHT, "4.0s", "-0.3s"),
    "onnx": ("ONNX", 78, HIGHLIGHT, "3.6s", "-0.9s"),
    "faiss": ("FAISS", 74, HIGHLIGHT, "3.9s", "-1.5s"),
    "docker": ("Docker", 84, HIGHLIGHT, "4.2s", "-2.1s"),
    "linux": ("Linux", 78, HIGHLIGHT, "3.7s", "-0.6s"),
    "git": ("Git", 62, HIGHLIGHT, "3.5s", "-1.2s"),
    # LANG / OPS row
    "python": ("Python", 86, ACCENT, "3.8s", "-0.4s"),
    "cpp": ("C++", 66, ACCENT, "4.1s", "-1.0s"),
    "typescript": ("TypeScript", 106, ACCENT, "3.6s", "-1.6s"),
    "pytorch": ("PyTorch", 94, ACCENT, "3.9s", "-2.2s"),
    "latex": ("LaTeX", 78, ACCENT, "4.0s", "-0.7s"),
    "cuda": ("CUDA", 76, ACCENT, "3.7s", "-1.3s"),
}

def main():
    # Generate label SVGs
    for fname, (text, width) in LABELS.items():
        svg = make_label_svg(text, width)
        path = os.path.join(OUTPUT_DIR, f"{fname}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  [label] {path}")

    # Generate chip SVGs
    for fname, (name, width, color, dur, delay) in CHIPS.items():
        svg = make_simple_chip(name, width, color, dur, delay)
        path = os.path.join(OUTPUT_DIR, f"{fname}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  [chip]  {path}")

    print(f"\n[OK] Generated {len(LABELS)} labels + {len(CHIPS)} chips in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
