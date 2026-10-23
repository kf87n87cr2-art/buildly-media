import os, sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, s)
BOLD = lambda s: F("InterDisplay-Bold.otf", s)
SEMI = lambda s: F("InterDisplay-SemiBold.otf", s)
MED = lambda s: F("Inter-Medium.otf", s)
REG = lambda s: F("Inter-Regular.otf", s)

BG = (11, 12, 16); FG = (244, 245, 247); MUTED = (150, 155, 168)
ACCENT = (79, 124, 255); CARD = (22, 24, 31); LINE = (40, 43, 54)
W, H = 1080, 1350
M = 96  # side margin

def mark(d, x, y, size, top=FG):
    s = size / 100
    d.rounded_rectangle((x + 14*s, y + 8*s, x + 40*s, y + 92*s), 7*s, fill=ACCENT)
    d.rounded_rectangle((x + 48*s, y + 44*s, x + 86*s, y + 92*s), 9*s, fill=ACCENT)
    d.rounded_rectangle((x + 48*s, y + 8*s, x + 64*s, y + 24*s), 5*s, fill=top)

def brand(d, x=M, y=88):
    mark(d, x, y, 52)
    d.text((x + 64, y + 2), "buildly", font=BOLD(46), fill=FG)

def footer(d, page=None, total=None, swipe=False):
    d.text((M, H - 120), "@buildly.lb", font=MED(32), fill=MUTED)
    if page:
        txt = f"{page}/{total}"
        if swipe: txt = "Swipe  →"
        w = d.textlength(txt, font=MED(32))
        d.text((W - M - w, H - 120), txt, font=MED(32), fill=MUTED)

def wrap(d, text, font, maxw):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=font) <= maxw: cur = t
            else: lines.append(cur); cur = w_
        lines.append(cur)
    return lines

def block(d, x, y, text, font, color, maxw=W - 2*M, lh=1.12):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=color)
        y += int(font.size * lh)
    return y

def new():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def cover(title, accent_word, sub, page, total, name):
    img, d = new(); brand(d)
    y = 420
    for ln in wrap(d, title, BOLD(104), W - 2*M):
        x = M
        for i, word in enumerate(ln.split()):
            col = ACCENT if word.strip(".,?") in accent_word else FG
            d.text((x, y), word, font=BOLD(104), fill=col)
            x += d.textlength(word + " ", font=BOLD(104))
        y += 118
    if sub: block(d, M, y + 40, sub, REG(42), MUTED)
    footer(d, page, total, swipe=True)
    img.save(f"{OUT}/{name}")

def point(num, title, sub, page, total, name):
    img, d = new(); brand(d)
    d.text((M, 380), num, font=BOLD(150), fill=ACCENT)
    y = block(d, M, 590, title, BOLD(84), FG)
    block(d, M, y + 40, sub, REG(42), MUTED)
    footer(d, page, total)
    img.save(f"{OUT}/{name}")

def cta(page, total, name, headline="Ready for yours?"):
    img, d = new(); brand(d)
    y = block(d, M, 470, headline, BOLD(104), FG)
    font = SEMI(52); label = "DM us to get started"
    tw = d.textlength(label, font=font)
    d.rounded_rectangle((M, y + 60, M + tw + 112, y + 60 + 124), 62, fill=ACCENT)
    d.text((M + 56, y + 60 + 32), label, font=font, fill=(255, 255, 255))
    d.text((M, y + 250), "Websites built for your business.", font=REG(42), fill=MUTED)
    footer(d, page, total)
    img.save(f"{OUT}/{name}")

# Profile picture
img = Image.new("RGB", (1080, 1080), BG); d = ImageDraw.Draw(img)
mark(d, 280, 280, 520); img.save(f"{OUT}/00-profile-picture.png")

# Post 2: intro
img, d = new()
mark(d, M, 300, 220)
y = block(d, M, 600, "Hello, we're Buildly.", BOLD(104), FG)
block(d, M, y + 40, "We build fast, modern websites for businesses in Lebanon and beyond.", REG(46), MUTED, maxw=820)
footer(d)
img.save(f"{OUT}/02-intro.png")

# Post 3: 5 signs carousel
signs = [
    ("01", "Customers ask if you have a website", "If they're asking, they're already looking for you online."),
    ("02", "You only exist on Instagram", "If your account has a problem, your business disappears with it."),
    ("03", "You answer the same questions every day", "Prices, hours, location. A website answers them for you, 24/7."),
    ("04", "Competitors look more professional", "First impressions happen online now, before anyone visits you."),
    ("05", "People can't find you on Google", "No website usually means no search results."),
]
T = 7
cover("5 signs your business needs a website", ["website"], None, 1, T, "03-signs-1.png")
for i, (n, t, s) in enumerate(signs):
    point(n, t, s, i + 2, T, f"03-signs-{i+2}.png")
cta(T, T, "03-signs-7.png")

# Post 4: how it works carousel
steps = [
    ("01", "Tell us about your business", "A quick chat on DM. What you do, who your customers are, what you need."),
    ("02", "We design and build it", "You see a live preview and request changes until it feels right."),
    ("03", "Your site goes live", "On your own domain, fast and perfect on every phone."),
]
T = 5
cover("How we build your website", ["website"], "Three simple steps.", 1, T, "04-how-1.png")
for i, (n, t, s) in enumerate(steps):
    point(n, t, s, i + 2, T, f"04-how-{i+2}.png")
cta(T, T, "04-how-5.png", "Let's build yours.")

# Post 5: services
img, d = new(); brand(d)
d.text((M, 260), "What we build", font=BOLD(96), fill=FG)
services = [
    ("Landing pages", "One focused page that turns visitors into customers."),
    ("Business websites", "A complete site for your brand, menu, services or portfolio."),
    ("Monthly care", "Updates, fixes and edits, so your site stays fresh."),
]
y = 410
for t, s in services:
    d.rounded_rectangle((M, y, W - M, y + 200), 28, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle((M + 44, y + 48, M + 64, y + 68), 5, fill=ACCENT)
    d.text((M + 90, y + 34), t, font=SEMI(52), fill=FG)
    block(d, M + 90, y + 106, s, REG(36), MUTED, maxw=W - 2*M - 140)
    y += 224
d.text((M, y + 20), "DM us for pricing →", font=SEMI(46), fill=ACCENT)
footer(d)
img.save(f"{OUT}/05-services.png")

# Post 6: instagram vs website carousel
T = 4
cover("Instagram page vs. website", ["website"], "Which one does your business need?", 1, T, "06-vs-1.png")
img, d = new(); brand(d)
cols = [("Instagram page", ["Great for reach", "The algorithm decides who sees you", "Not on Google", "You don't own it"]),
        ("Website", ["Builds trust", "Always open, always yours", "Shows up on Google", "All your info in one place"])]
cw = (W - 2*M - 32) // 2
for i, (title, pts) in enumerate(cols):
    x = M + i * (cw + 32)
    hl = i == 1
    d.rounded_rectangle((x, 300, x + cw, 1130), 28, fill=CARD, outline=ACCENT if hl else LINE, width=3 if hl else 2)
    d.text((x + 40, 350), title, font=SEMI(46), fill=ACCENT if hl else FG)
    yy = 470
    for p in pts:
        d.ellipse((x + 40, yy + 16, x + 54, yy + 30), fill=ACCENT if hl else MUTED)
        yy = block(d, x + 76, yy, p, REG(36), FG, maxw=cw - 110) + 44
footer(d, 2, T)
img.save(f"{OUT}/06-vs-2.png")
img, d = new(); brand(d)
y = block(d, M, 470, "The answer? You need both.", BOLD(104), FG)
block(d, M, y + 40, "Instagram gets you attention. Your website turns that attention into trust and customers.", REG(46), MUTED)
footer(d, 3, T)
img.save(f"{OUT}/06-vs-3.png")
cta(T, T, "06-vs-4.png")
print("done")
