#!/usr/bin/env python3
"""Compose the 24 Nov 2026 front page: 'The World in One Picture'.

Fresh implementation. Reads three editorial panels from ./panels/, draws the
masthead, headlines, stories and markets strip with PIL, writes entry.png
(1024x1024, <=1 MiB). No network, no randomness: identical inputs give
identical bytes, so two runs produce the same sha256.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (250, 246, 238)
INK = (17, 17, 17)
GREY = (84, 84, 84)
RED = (155, 28, 28)
STRIP_BG = (16, 16, 16)
STRIP_FG = (232, 232, 232)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(draw, text, path, start, minimum, max_w):
    """Largest font size in [minimum, start] whose text fits max_w."""
    size = start
    while size > minimum and text_w(draw, text, font(path, size)) > max_w:
        size -= 2
    return size


def crop_to(im, tw, th, focus=0.5):
    """Center-crop (with vertical focus bias 0..1) to the target aspect."""
    iw, ih = im.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(round(iw * scale)), int(round(ih * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - tw) // 2
    y0 = int(round((nh - th) * focus))
    return im.crop((x0, y0, x0 + tw, y0 + th))


def draw_rule(draw, y, x0, x1, width, fill=INK):
    draw.rectangle([x0, y, x1, y + width - 1], fill=fill)


def build():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    y = 22
    # --- masthead ---
    f_mast = font(SERIF_B, 56)
    d.text((W // 2, y), "THE WORLD IN ONE PICTURE", font=f_mast,
           fill=INK, anchor="mt")
    y += 62
    draw_rule(d, y, MARGIN, W - MARGIN, 2)
    y += 8
    # --- dateline row ---
    f_date = font(SANS_B, 20)
    f_tag = font(SANS, 17)
    d.text((MARGIN, y), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=INK)
    tag = "ONE DAY  ·  ONE PICTURE  ·  THE WORLD"
    d.text((W - MARGIN, y), tag, font=f_tag, fill=GREY, anchor="ra")
    y += 27
    draw_rule(d, y, MARGIN, W - MARGIN, 4)
    y += 12

    # --- hero headline ---
    hl1 = "HUANG IS BACK"
    s1 = fit_size(d, hl1, SANS_B, 96, 72, CW)
    d.text((MARGIN, y), hl1, font=font(SANS_B, s1), fill=INK)
    y += s1 + 4
    hl2 = "NVIDIA +31.5% AS TRUMP SEALS COMEBACK"
    s2 = fit_size(d, hl2, SANS_B, 46, 34, CW)
    d.text((MARGIN, y), hl2, font=font(SANS_B, s2), fill=INK)
    y += s2 + 8
    # --- deck ---
    deck = ("The board unanimously reinstates its chief days after his "
            "resignation; the Nasdaq jumps 6.51% and the S&P 500 climbs "
            "4.73% in a record rally.")
    f_deck = font(SERIF, 23)
    for line in wrap(d, deck, f_deck, CW):
        d.text((MARGIN, y), line, font=f_deck, fill=(34, 34, 34))
        y += 29
    y += 8

    # --- hero photo ---
    hero = Image.open(os.path.join(HERE, "panels",
        "media-generation-hero-nvidia-0-b1718278-282b-4853-926e-a29dfa18bddb.webp")).convert("RGB")
    page.paste(crop_to(hero, CW, 202, focus=0.62), (MARGIN, y))
    y += 202 + 5
    f_cap = font(SERIF_I, 16)
    d.text((MARGIN, y), "Huang returned to Nvidia's Santa Clara headquarters "
           "on Monday to cheers from staff.", font=f_cap, fill=GREY)
    y += 24
    y += 6

    # --- two story columns ---
    col_w = (CW - 20) // 2  # 466
    stories = [
        ("RIYADH",
         "DRONE HITS RIYADH'S TALLEST TOWER",
         "media-generation-panel-riyadh-0-968d6591-510c-473f-b26c-48951cb7c948.webp",
         "A Houthi drone struck Riyadh's 385-metre Public Investment Fund "
         "Tower on Tuesday, wounding 11 people \u2014 the second hit on the "
         "tower in less than a week."),
        ("GAZA CITY",
         "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
         "media-generation-panel-gaza-0-cb4f2042-9524-459d-858a-59b0a26dc5ba.webp",
         "Naim Abu Nahal, 50, head of Hamas's Internal Security Service, "
         "was killed in an Israeli strike in western Gaza City. At least "
         "seven died in Tuesday's strikes, medics said."),
    ]
    f_kick = font(SANS_B, 18)
    f_story_h = font(SANS_B, 29)
    f_body = font(SERIF, 18)
    col_top = y
    col_bottom = col_top
    for i, (kicker, headline, panel, body) in enumerate(stories):
        x = MARGIN + i * (col_w + 20)
        cy = col_top
        d.text((x, cy), kicker, font=f_kick, fill=RED)
        cy += 23
        for line in wrap(d, headline, f_story_h, col_w):
            d.text((x, cy), line, font=f_story_h, fill=INK)
            cy += 33
        cy += 4
        im = Image.open(os.path.join(HERE, "panels", panel)).convert("RGB")
        page.paste(crop_to(im, col_w, 122, focus=0.5), (x, cy))
        cy += 122 + 6
        for line in wrap(d, body, f_body, col_w):
            d.text((x, cy), line, font=f_body, fill=(34, 34, 34))
            cy += 21
        col_bottom = max(col_bottom, cy)
    y = col_bottom + 10

    # --- dark markets strip ---
    strip_top = y
    strip_h = H - 24 - strip_top
    assert strip_h >= 110, f"strip too short: {strip_h}px"
    d.rectangle([0, strip_top, W, H - 24], fill=STRIP_BG)
    sy = strip_top + 13
    f_mkt = font(SANS_B, 23)
    d.text((MARGIN, sy), "MARKETS", font=f_mkt, fill=(255, 196, 66))
    mkt = "Nasdaq +6.51%   ·   S&P 500 +4.73%   ·   Dow +3.01%   ·   Nvidia +31.5%"
    d.text((MARGIN + 132, sy), mkt, font=f_mkt, fill=(255, 255, 255))
    sy += 34
    briefs = ("BEIJING \u2014 Shanghai chief Chen Jining probed, 4th Politburo "
              "member since 2025  ·  NEPAL \u2014 5.6 quake, no casualties  ·  "
              "14 NATIONS back ICJ Rohingya ruling  ·  SEOUL scrambles F-15Ks "
              "as Russian jets near Ulleung  ·  RIAL hits record 2.82M per "
              "dollar  ·  COLOMBIA \u2014 car bomb wounds 23 in Villavicencio")
    f_brief = font(SANS, 17)
    for line in wrap(d, briefs, f_brief, CW):
        d.text((MARGIN, sy), line, font=f_brief, fill=STRIP_FG)
        sy += 21

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG")
    print(f"wrote {out}  strip_top={strip_top} strip_h={strip_h}")


if __name__ == "__main__":
    build()
