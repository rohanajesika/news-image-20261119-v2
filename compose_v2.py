#!/usr/bin/env python3
"""Draw the news-image-20261119 v2 poster: one dense front page summing up
Thursday 19 November 2026 in 50 sourced stories.

All 50 stories were verified first reported on 19 November 2026 (UTC);
see ../news-image-20261119-v2-research.md for the sourcing notes.
Wire times are UTC hours of first report (Reuters Akvan 04:25 UTC is the
minute-precise anchor). The Earth strip is a crop of NASA's Apollo 17
Blue Marble photograph (public domain), stored beside this script as
earth_band.jpg. Output is a deterministic 1024x1024 PNG.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (15, 42, 74)
RED = (185, 28, 28)
GOLD = (242, 201, 76)
GREEN = (20, 83, 45)
SLATE = (71, 85, 105)
ROW_ALT = (238, 231, 216)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)

REGION_COLORS = {
    "ASIA": (180, 83, 9),
    "EUROPE": (29, 78, 216),
    "MIDEAST": (185, 28, 28),
    "AFRICA": (21, 128, 61),
    "AMERICAS": (109, 40, 217),
    "WORLD": (14, 116, 144),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))

# (no, kicker, headline, body, source, region)
LEADS = [
    (1, "SHENZHEN  ·  APEC",
     "Trump, Xi and Putin hold first three-way summit",
     "Peace declaration: nuclear risks, UN reform, oil, courts. "
     "No Ukraine or Iran. Trump called Putin a friend.",
     "BBC · Guardian · PBS", "ASIA"),
    (2, "THE HAGUE  ·  JUSTICE",
     "UN court: Myanmar committed genocide on Rohingya",
     "First state held responsible for genocide. Vote 9-6. "
     "Gambia filed in 2019; refugees in Bangladesh cheered.",
     "BBC · UN News · Guardian", "EUROPE"),
    (3, "ODISHA  ·  CYCLONE AKVAN",
     "Odisha evacuates 47,000+ as third storm in a month nears",
     "Landfall Friday noon; winds 90-100 km/h. Schools shut. "
     "Third storm in a month; Andhra yet to evacuate.",
     "Reuters 04:25 UTC", "ASIA"),
    (4, "LAUNCH DAY  ·  GAMES",
     "GTA VI goes on sale after a 13-year wait",
     "Est. 24.58m copies, ~$2.36bn. PS outage at launch. "
     "Hailed by critics after 13 years and two delays.",
     "Straits Times · Al Jazeera", "AMERICAS"),
]

# (no, utc_hour, headline, source, region, context)
WIRE = [
    (5, 0, "Australia jobless rate hits 4.9%, a five-year high", "Guardian", "ASIA", "Jobless up from 4.7%."),
    (6, 1, "Van Gogh sells for record $190.4m", "BBC", "AMERICAS", "1890 work; beats the $117.2m mark."),
    (7, 1, "S. Korea holds Suneung exam under AI curbs", "Yonhap", "ASIA", "22 caught; AI-cheat suspect in arrest."),
    (8, 3, "Japan core inflation hits year high; Nikkei -4.68%", "CNBC", "ASIA", "Subsidy expiry lifted prices."),
    (9, 5, "England win ODI series in Australia", "BBC Sport", "ASIA", "Duckett century seals series."),
    (10, 6, "Philippines-Chile free-trade deal at APEC", "Inquirer", "ASIA", "Manila's first Latin America deal."),
    (11, 7, "Takaichi meets Xi and Putin at APEC", "Japan Times", "ASIA", "10-sec Xi handshake; first in 7 yrs."),
    (12, 8, "S. Korea-China agree to expand cultural exchange", "Yonhap", "ASIA", "Easing seen on Korean content curbs."),
    (13, 9, "Denmark ratifies US Greenland security deal 109-0", "CNBC", "EUROPE", "Boosts US military presence on island."),
    (14, 9, "Nearly 1 in 4 children live in conflict zones", "Straits Times", "WORLD", "589m children; Africa is half."),
    (15, 10, "BepiColombo reaches Mercury orbit", "Guardian", "WORLD", "Second mission to orbit Mercury."),
    (16, 10, "Violence in Bangladesh over Hasina's return", "Guardian", "ASIA", "Two killed in Narail; ~300 arrests."),
    (17, 10, "Migrant boat capsizes off Senegal; dozens missing", "BBC", "AFRICA", "50-100 aboard; four bodies recovered."),
    (18, 10, "Mongolian president resigns", "AP", "ASIA", "Khurelsukh out; vote in four months."),
    (19, 10, "EU Commission hit by AI-powered cyberattack", "DW", "EUROPE", "Tools offline; 33,000 staff data at risk."),
    (20, 11, "EU-Mexico deal to remove 95% of farm tariffs", "ANSA", "EUROPE", "95% farm tariffs cut; 568 labels kept."),
    (21, 11, "Court sentences Imamoglu, eight others", "BBC Türkçe", "EUROPE", "Nine jailed, banned in CHP case."),
    (22, 12, "EU approves trade deal with Indonesia", "Al Jazeera", "EUROPE", "Duties cut on 90%+ of goods."),
    (23, 12, "Litton Das sets Test record: 8 dismissals", "AFP via France 24", "AFRICA", "Six catches, two stumpings."),
    (24, 13, "Lee Kang-in is Asia's top footballer again", "Yonhap", "ASIA", "Second straight year for Atletico star."),
    (25, 13, "Foord is Asia's women's international player", "ABC Australia", "ASIA", "Arsenal striker honoured."),
    (26, 13, "Beiranvand first keeper to win Asia's top award", "The National", "ASIA", "First goalkeeper to win the award."),
    (27, 14, "Anthropic up 17% after record $81bn IPO", "BBC", "AMERICAS", "Opened near $111.50; largest IPO ever."),
    (28, 14, "Nvidia faces California probe after Huang exit", "BBC", "AMERICAS", "Subpoena on China chip disclosures."),
    (29, 14, "Houthi missile hits Riyadh's tallest tower", "Sky News", "MIDEAST", "PIF Tower hit; no injuries."),
    (30, 15, "Iraq orders Kataib Hezbollah out of Jurf al-Nasr", "Euronews", "MIDEAST", "Must leave by Friday; army deploys."),
    (31, 15, "IAEA: N. Korea expanded enrichment at Yongbyon", "Euronews", "ASIA", "No IAEA access since 2009."),
    (32, 15, "Senegal's ruling party expels President Faye", "Africanews", "AFRICA", "Faye expelled with 31 others."),
    (33, 16, "US consortium wins Kenya critical minerals deal", "BBC", "AFRICA", "Mrima Hill holds $60bn+ in minerals."),
    (34, 16, "Sudan: WFP aid for 30,000 displaced at El Dabba", "AllAfrica", "AFRICA", "Drones cause 80% of civilian toll."),
    (35, 17, "Five EU states to send asylum seekers to Rwanda", "CBS", "EUROPE", "Germany among five; far from done deal."),
    (36, 17, "Record rain from atmospheric river hits California", "Guardian", "AMERICAS", "LA warned of evacuations."),
    (37, 17, "COP31 draft drops fossil fuel language", "CBC", "EUROPE", "African states want more finance."),
    (38, 18, "US tech outages hit Outlook, banks and flights", "BBC", "AMERICAS", "A week of outages; Vance cancels trip."),
    (39, 18, "US and Venezuela sign military cooperation deal", "BBC", "AMERICAS", "Signed with acting president Rodriguez."),
    (40, 18, "US loses measles elimination status", "Al Jazeera", "AMERICAS", "Disease now endemic; jabs falling."),
    (41, 19, "Democrats nominate Jeffries for House speaker", "BBC", "AMERICAS", "First Black speaker; House votes Jan 3."),
    (42, 19, "Iran escalates Hormuz tanker and Gulf strikes", "Japan Times", "MIDEAST", "Tanker hit a mine; Senate 51-48."),
    (43, 19, "Trump: Iran eyeing chemical, biological arms", "Straits Times", "AMERICAS", "No evidence; US vows retaliation."),
    (44, 19, "European allies in Berlin ready for Russia talks", "BBC", "EUROPE", "Macron urges NATO membership talks."),
    (45, 20, "Crimean Bridge hit; Putin vows harsher reply", "BBC", "EUROPE", "Traffic halted; one span damaged."),
    (46, 20, "Israel ends Gaza ground op beyond Yellow Line", "BBC", "MIDEAST", "First ground op since the ceasefire."),
    (47, 20, "Israel delays E1 plan; settler kills woman", "Guardian", "MIDEAST", "UK sanctions cited; woman, 72, shot."),
    (48, 20, "Sánchez admits mistakes in election debate", "France 24", "EUROPE", "Spain votes 29 Nov; Feijóo ahead."),
    (49, 21, "Wall Street falls 2% for a fifth straight day", "UPI", "AMERICAS", "Fed flags AI overheating."),
    (50, 22, "Trump posthumously pardons Pete Rose", "BBC", "AMERICAS", "Rose died in 2024; banned over bets."),
]

MARKETS = ("MARKETS 19 NOV  —  S&P 500 -2.02%  ·  Nikkei -4.68%  ·  "
           "Gold $3,596 -2.42% (14-month low)  ·  Brent $89.72 +0.31%  ·  "
           "Bitcoin below $63,000")
SOURCES_LINE = ("Sources: Reuters · AP · BBC · UN News · Guardian · Al Jazeera · "
                "France 24 · CNBC · NPR · CBS · DW · Euronews · Yonhap · Japan Times · "
                "Straits Times · Hindu · El País · RFI · UPI · SCMP · ABC · Africanews · "
                "AllAfrica · ANSA · CBC")
DATECHECK = ("All 50 stories above were first reported on Thursday 19 November 2026 "
             "(UTC). Each names its source — check the headline against that outlet's "
             "19 Nov 2026 edition. Wire times are UTC hours of first report; checked "
             "20 Nov 2026 vs Reuters, AP, BBC, UN News, The Guardian, One Turn.")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt, max_w):
    """Truncate with ellipsis if the single line is too wide; warn."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    print(f"WARNING truncated: {text!r}", file=sys.stderr)
    while text and draw.textlength(text + "…", font=fnt) > max_w:
        text = text[:-1]
    return text + "…"


def draw_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 74], fill=NAVY)
    f_title = font(SERIF_B, 28)
    f_date = font(SANS_B, 19)
    f_badge = font(SANS_B, 13)
    f_badge2 = font(SANS, 11)
    d.text((16, 9), "THE WORLD IN ONE DAY", font=f_title, fill=WHITE)
    d.text((16, 43), "Thursday, 19 November 2026", font=f_date, fill=GOLD)
    badge = "50 SOURCED STORIES"
    d.text((W - 16 - d.textlength(badge, font=f_badge), 11), badge,
           font=f_badge, fill=WHITE)
    badge2 = "UTC WIRE  ·  DATE CHECK"
    d.text((W - 16 - d.textlength(badge2, font=f_badge2), 34), badge2,
           font=f_badge2, fill=(200, 210, 225))
    d.rectangle([0, 74, W, 78], fill=RED)

    # ---- Earth strip ------------------------------------------------------
    band = Image.open(os.path.join(HERE, "earth_band.jpg")).convert("RGB")
    assert band.size == (1024, 100), f"earth band is {band.size}"
    img.paste(band, (0, 78))
    f_cap = font(SANS_B, 8)
    cap = "EARTH · APOLLO 17, NASA (PUBLIC DOMAIN)"
    cw = d.textlength(cap, font=f_cap)
    d.rectangle([W - 16 - cw - 10, 160, W - 10, 176], fill=NAVY)
    d.text((W - 16 - cw - 5, 163), cap, font=f_cap, fill=WHITE)

    # ---- Lead panels ----------------------------------------------------
    lead_y, lead_h = 184, 136
    col_w, gap = 242, 8
    f_kick = font(SANS_B, 10)
    f_lead = font(SANS_B, 15)
    f_body = font(SANS, 11)
    f_src = font(SANS, 10)
    for i, (num, kicker, head, body, src, region) in enumerate(LEADS):
        x = 16 + i * (col_w + gap)
        rc = REGION_COLORS[region]
        d.rectangle([x, lead_y, x + col_w, lead_y + lead_h], fill=PANEL,
                    outline=(200, 192, 172))
        d.rectangle([x, lead_y, x + col_w, lead_y + 4], fill=rc)
        d.text((x + 8, lead_y + 8), f"{num:02d}  {kicker}", font=f_kick, fill=rc)
        lines = wrap(d, head, f_lead, col_w - 16)
        y = lead_y + 24
        for ln in lines[:3]:
            d.text((x + 8, y), ln, font=f_lead, fill=INK)
            y += 17
        blines = wrap(d, body, f_body, col_w - 16)
        y += 3
        for ln in blines[:3]:
            d.text((x + 8, y), ln, font=f_body, fill=(45, 45, 45))
            y += 13
        d.text((x + 8, lead_y + lead_h - 14), "— " + src, font=f_src, fill=SLATE)

    # ---- Wire header ------------------------------------------------------
    f_wire_h = font(SANS_B, 13)
    f_wire_h2 = font(SANS, 11)
    d.text((16, 326), "THE WIRE — 46 MORE STORIES, IN UTC ORDER",
           font=f_wire_h, fill=NAVY)
    rh = "ASIA 15  ·  EUROPE 11  ·  AMERICAS 12  ·  MIDEAST 5  ·  AFRICA 5  ·  WORLD 2"
    d.text((W - 16 - d.textlength(rh, font=f_wire_h2), 327), rh,
           font=f_wire_h2, fill=SLATE)

    # ---- Wire rows: 3 columns x 16 rows ----------------------------------
    f_head = font(SANS, 12)
    f_meta = font(SANS, 9)
    f_meta_b = font(SANS_B, 9)
    wire_y, row_h = 350, 34
    col_w3 = 325
    col_x = [16, 16 + col_w3 + 8, 16 + 2 * (col_w3 + 8)]
    for idx, (num, hh, head, src, region, ctx) in enumerate(WIRE):
        col = idx // 16
        row = idx % 16
        x = col_x[col]
        y = wire_y + row * row_h
        if row % 2 == 0:
            d.rectangle([x, y, x + col_w3, y + row_h], fill=ROW_ALT)
        rc = REGION_COLORS[region]
        d.rectangle([x + 2, y + 6, x + 9, y + 13], fill=rc)
        head_fit = fit_text(d, head, f_head, col_w3 - 17)
        d.text((x + 13, y + 3), head_fit, font=f_head, fill=INK)
        prefix = f"{num:02d} · {hh:02d}:00 · {src} — "
        pw = d.textlength(prefix, font=f_meta_b)
        ctx_fit = fit_text(d, ctx, f_meta, col_w3 - 13 - pw - 2)
        d.text((x + 13, y + 18), prefix, font=f_meta_b, fill=RED)
        d.text((x + 13 + pw, y + 18), ctx_fit, font=f_meta, fill=SLATE)

    # ---- 24h UTC arc ------------------------------------------------------
    arc_y = 900
    f_arc = font(SANS_B, 10)
    f_arc2 = font(SANS, 10)
    d.text((16, arc_y), "THE DAY IN UTC — ONE DOT PER STORY",
           font=f_arc, fill=NAVY)
    bar_x0, bar_x1, bar_y = 16, 1008, arc_y + 16
    d.rectangle([bar_x0, bar_y, bar_x1, bar_y + 6], fill=(210, 202, 186))
    for h in range(0, 25, 3):
        tx = bar_x0 + (bar_x1 - bar_x0) * h / 24.0
        d.line([tx, bar_y - 3, tx, bar_y + 9], fill=SLATE, width=1)
        lab = f"{h:02d}"
        d.text((tx - d.textlength(lab, font=f_arc2) / 2, bar_y + 11), lab,
               font=f_arc2, fill=SLATE)
    lead_hours = {1: 7, 2: 9, 3: 4, 4: 0}
    dots = []
    for (num, kicker, head, body, src, region) in LEADS:
        dots.append((lead_hours[num], num, region))
    for (num, hh, head, src, region, ctx) in WIRE:
        dots.append((hh, num, region))
    for (hour, num, region) in dots:
        cx = bar_x0 + (bar_x1 - bar_x0) * hour / 24.0
        cy = bar_y + 3 + ((num * 7) % 3 - 1) * 4
        r = 4
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=REGION_COLORS[region], outline=WHITE)

    # ---- Date check -------------------------------------------------------
    dc_y, dc_h = 942, 54
    d.rectangle([0, dc_y, W, dc_y + dc_h], fill=GREEN)
    f_dc_h = font(SANS_B, 14)
    f_dc = font(SANS, 12)
    d.text((16, dc_y + 5), "✓  DATE CHECK", font=f_dc_h, fill=WHITE)
    lines = wrap(d, DATECHECK, f_dc, W - 32)
    y = dc_y + 23
    for ln in lines[:2]:
        d.text((16, y), ln, font=f_dc, fill=(235, 245, 235))
        y += 15

    # ---- Footer -----------------------------------------------------------
    f_mkt = font(SANS_B, 11)
    f_ftr = font(SANS, 8)
    d.text((16, 998), MARKETS, font=f_mkt, fill=NAVY)
    src_fit = fit_text(d, SOURCES_LINE, f_ftr, W - 32)
    d.text((16, 1010), src_fit, font=f_ftr, fill=SLATE)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = draw_poster()
    img.save(out, format="PNG")
    print(out)


if __name__ == "__main__":
    main()
