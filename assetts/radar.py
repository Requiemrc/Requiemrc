import json
import math

def generate_radar(json_path, output_svg, is_dark=True):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = list(data.keys())
    values = list(data.values())
    n = len(categories)

    cx, cy, r = 250, 200, 130
    bg_color = "#0d1117" if is_dark else "#ffffff"
    stroke_color = "#30363d" if is_dark else "#e1e4e8"
    text_color = "#c9d1d9" if is_dark else "#24292e"
    accent_color = "#58a6ff"

    svg = [f'<svg width="500" height="400" viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="100%" height="100%" fill="{bg_color}" rx="10"/>')

    # Círculos / Niveles de fondo
    for level in [0.25, 0.5, 0.75, 1.0]:
        pts = []
        for i in range(n):
            angle = (2 * math.pi / n) * i - math.pi / 2
            x = cx + r * level * math.cos(angle)
            y = cy + r * level * math.sin(angle)
            pts.append(f"{x:.1f},{y:.1f}")
        svg.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{stroke_color}" stroke-dasharray="3,3"/>')

    # Polígono de datos y etiquetas
    poly_pts = []
    for i, (cat, val) in enumerate(zip(categories, values)):
        angle = (2 * math.pi / n) * i - math.pi / 2
        val_ratio = min(max(val, 0), 100) / 100.0
        x = cx + r * val_ratio * math.cos(angle)
        y = cy + r * val_ratio * math.sin(angle)
        poly_pts.append(f"{x:.1f},{y:.1f}")

        # Texto de la categoría
        tx = cx + (r + 30) * math.cos(angle)
        ty = cy + (r + 30) * math.sin(angle)
        svg.append(f'<text x="{tx:.1f}" y="{ty:.1f}" fill="{text_color}" font-family="sans-serif" font-size="12" text-anchor="middle" dominant-baseline="middle">{cat}</text>')

    svg.append(f'<polygon points="{" ".join(poly_pts)}" fill="{accent_color}" fill-opacity="0.3" stroke="{accent_color}" stroke-width="2"/>')
    svg.append('</svg>')

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

if __name__ == "__main__":
    generate_radar("assets/skills.json", "assets/radar-dark.svg", is_dark=True)
    generate_radar("assets/skills.json", "assets/radar-light.svg", is_dark=False)