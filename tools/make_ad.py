import subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 15.0
OUT = sys.argv[1]
HANDLE = sys.argv[2] if len(sys.argv) > 2 else "@yourhandle"

FD = "/usr/share/fonts/opentype/inter/"
def F(name, size): return ImageFont.truetype(FD + name, size)
BOLD = lambda s: F("InterDisplay-Bold.otf", s)
SEMI = lambda s: F("InterDisplay-SemiBold.otf", s)
MED = lambda s: F("Inter-Medium.otf", s)
REG = lambda s: F("Inter-Regular.otf", s)

BG = (11, 12, 16)
FG = (244, 245, 247)
MUTED = (140, 145, 158)
ACCENT = (79, 124, 255)
CARD = (22, 24, 31)
LINE = (38, 41, 52)
SKEL = (44, 48, 60)

def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(int(lerp(x, y, t)) for x, y in zip(c1, c2))
def clamp(t): return max(0.0, min(1.0, t))
def ease(t):
    t = clamp(t); return 1 - (1 - t) ** 3

def env(t, start, end, fin=0.5, fout=0.4):
    """visibility 0..1 and rise offset for an element shown in [start,end]"""
    a_in = ease((t - start) / fin)
    a_out = 1 - ease((t - (end - fout)) / fout) if end else 1
    return clamp(min(a_in, a_out)), (1 - a_in) * 40

def text_c(d, y, s, font, color, a, under=BG, dy=0):
    if a <= 0: return
    w = d.textlength(s, font=font)
    d.text(((W - w) / 2, y + dy), s, font=font, fill=mix(under, color, a))

def frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Scene 1: hook (0 - 3.4s)
    a, dy = env(t, 0.2, 3.4)
    text_c(d, 760, "Your business", BOLD(104), FG, a, dy=dy)
    a2, dy2 = env(t, 0.6, 3.4)
    text_c(d, 890, "deserves a", BOLD(104), FG, a2, dy=dy2)
    a3, dy3 = env(t, 1.0, 3.4)
    text_c(d, 1020, "great website.", BOLD(104), ACCENT, a3, dy=dy3)

    # Scene 2: browser being built (3.6 - 7.4s)
    s, e = 3.6, 7.4
    ca, cdy = env(t, s, e, fin=0.6)
    if ca > 0:
        x0, y0, x1, y1 = 140, 520 + cdy, 940, 1400 + cdy
        d.rounded_rectangle((x0, y0, x1, y1), 28, fill=mix(BG, CARD, ca), outline=mix(BG, LINE, ca), width=2)
        d.line((x0, y0 + 70, x1, y0 + 70), fill=mix(BG, LINE, ca), width=2)
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
            cx = x0 + 44 + i * 34
            d.ellipse((cx - 9, y0 + 26, cx + 9, y0 + 44), fill=mix(CARD, c, ca * 0.9))
        d.rounded_rectangle((x0 + 170, y0 + 20, x1 - 60, y0 + 50), 15, fill=mix(CARD, SKEL, ca * 0.7))
        # blocks appearing one by one
        blocks = [
            ((x0 + 50, y0 + 115, x0 + 200, y0 + 145), SKEL, 0.5),
            ((x1 - 330, y0 + 120, x1 - 50, y0 + 140), SKEL, 0.6),
            ((x0 + 50, y0 + 220, x1 - 160, y0 + 290), FG, 0.9),
            ((x0 + 50, y0 + 310, x1 - 300, y0 + 380), FG, 1.05),
            ((x0 + 50, y0 + 420, x1 - 120, y0 + 445), SKEL, 1.25),
            ((x0 + 50, y0 + 465, x1 - 250, y0 + 490), SKEL, 1.35),
            ((x0 + 50, y0 + 545, x0 + 300, y0 + 615), ACCENT, 1.6),
            ((x0 + 50, y0 + 680, x0 + 260, y0 + 830), SKEL, 1.85),
            ((x0 + 295, y0 + 680, x0 + 505, y0 + 830), SKEL, 1.95),
            ((x0 + 540, y0 + 680, x1 - 50, y0 + 830), SKEL, 2.05),
        ]
        for box, col, delay in blocks:
            ba = min(ca, ease((t - s - delay) / 0.35))
            if ba > 0:
                r = 14 if col != ACCENT else 35
                bx0, by0, bx1, by1 = box
                bx1 = bx0 + (bx1 - bx0) * ease((t - s - delay) / 0.45)
                d.rounded_rectangle((bx0, by0, max(bx0 + 1, bx1), by1), min(r, (by1 - by0) // 2), fill=mix(CARD, col, ba * (0.9 if col == FG else 1)))
        la, ldy = env(t, s + 0.3, e)
        text_c(d, 1490, "Designed. Built. Launched.", SEMI(62), FG, la, dy=ldy)

    # Scene 3: benefits (7.6 - 11.2s)
    s, e = 7.6, 11.2
    ha, hdy = env(t, s, e)
    text_c(d, 640, "What you get", MED(44), MUTED, ha, dy=hdy)
    items = ["Delivered in days", "Perfect on every phone", "Fair, simple pricing"]
    for i, it in enumerate(items):
        ia, idy = env(t, s + 0.35 + i * 0.35, e)
        if ia <= 0: continue
        y = 790 + i * 170 + idy
        font = SEMI(72)
        tw = d.textlength(it, font=font)
        total = 70 + 36 + tw
        x = (W - total) / 2
        d.ellipse((x, y + 8, x + 70, y + 78), fill=mix(BG, ACCENT, ia))
        p = ease((t - (s + 0.5 + i * 0.35)) / 0.35)
        pts = [(x + 20, y + 44), (x + 31, y + 56), (x + 51, y + 31)]
        if p > 0:
            seg = [pts[0], pts[1]] if p < 0.4 else pts
            if p < 0.4:
                seg = [pts[0], (lerp(pts[0][0], pts[1][0], p / 0.4), lerp(pts[0][1], pts[1][1], p / 0.4))]
            else:
                q = (p - 0.4) / 0.6
                seg = [pts[0], pts[1], (lerp(pts[1][0], pts[2][0], q), lerp(pts[1][1], pts[2][1], q))]
            d.line(seg, fill=mix(ACCENT, FG, ia), width=8, joint="curve")
        d.text((x + 106, y), it, font=font, fill=mix(BG, FG, ia))

    # Scene 4: CTA (11.4 - 15s)
    s = 11.4
    ba, bdy = env(t, s, None)
    if ba > 0:
        bf = BOLD(64)
        bw = d.textlength("buildly", font=bf) + 82
        bx = (W - bw) / 2
        ms, my = 0.68, 486 + bdy
        A = mix(BG, ACCENT, ba)
        d.rounded_rectangle((bx + 14*ms, my + 8*ms, bx + 40*ms, my + 92*ms), 5, fill=A)
        d.rounded_rectangle((bx + 48*ms, my + 44*ms, bx + 86*ms, my + 92*ms), 6, fill=A)
        d.rounded_rectangle((bx + 48*ms, my + 8*ms, bx + 64*ms, my + 24*ms), 3, fill=mix(BG, FG, ba))
        d.text((bx + 82, 486 + bdy), "buildly", font=bf, fill=mix(BG, FG, ba))
    a, dy = env(t, s, None)
    text_c(d, 690, "Websites built", BOLD(110), FG, a, dy=dy)
    a2, dy2 = env(t, s + 0.3, None)
    text_c(d, 820, "for your business.", BOLD(110), FG, a2, dy=dy2)
    ua = ease((t - s - 0.8) / 0.6)
    if ua > 0:
        lw = 220 * ua
        d.rounded_rectangle(((W - lw) / 2, 1000, (W + lw) / 2, 1008), 4, fill=ACCENT)
    a3, dy3 = env(t, s + 1.0, None)
    if a3 > 0:
        font = SEMI(56)
        label = "DM to get started"
        tw = d.textlength(label, font=font)
        bw, bh = tw + 120, 130
        bx, by = (W - bw) / 2, 1090 + dy3
        d.rounded_rectangle((bx, by, bx + bw, by + bh), bh // 2, fill=mix(BG, ACCENT, a3))
        d.text(((W - tw) / 2, by + 32), label, font=font, fill=mix(BG, (255, 255, 255), a3))
    a4, dy4 = env(t, s + 1.3, None)
    text_c(d, 1290, HANDLE, MED(52), MUTED, a4, dy=dy4)
    return img

proc = subprocess.Popen([
    "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
    "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
for i in range(int(DUR * FPS)):
    proc.stdin.write(frame(i / FPS).tobytes())
proc.stdin.close()
proc.wait()

if len(sys.argv) > 3:
    for ts in [1.8, 5.8, 9.8, 14.0]:
        frame(ts).save(f"{sys.argv[3]}/still_{ts}.png")
