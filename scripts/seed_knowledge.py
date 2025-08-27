"""
Writes curated tomato disease markdown files to ./knowledge.
Run once before ingest:
    python scripts/seed_knowledge.py
"""
from pathlib import Path
import textwrap

DISEASES = [
    {
        "slug": "early-blight",
        "name": "Early Blight (Alternaria solani)",
        "overview": "A common fungal disease causing target-like concentric brown lesions. Often starts on older leaves.",
        "symptoms": [
            "Brown spots with concentric rings ('bullseye' pattern) on lower/older leaves",
            "Yellowing around lesions; defoliation under severe pressure",
            "Dark, sunken lesions on stems; fruit shoulder rot under calyx",
        ],
        "favorable_conditions": [
            "Warm temperatures (24–29°C)",
            "Frequent leaf wetness / overhead irrigation",
            "High humidity and stressed plants (nutrient deficiency)",
        ],
        "management": [
            "Remove infected lower leaves; avoid overhead irrigation",
            "Mulch to reduce soil splash; stake/prune to improve airflow",
            "Rotate crops (2–3 years); sanitize debris after season",
            "Protectant fungicides (chlorothalonil, mancozeb); rotate FRAC groups",
        ],
        "notes": "Often confused with Septoria; early blight lesions are larger with clear concentric rings.",
    },
    {
        "slug": "late-blight",
        "name": "Late Blight (Phytophthora infestans)",
        "overview": "A devastating oomycete disease (same pathogen as Irish potato famine). Spreads rapidly in cool, wet conditions.",
        "symptoms": [
            "Irregular, water-soaked lesions that turn brown/black on leaves and stems",
            "White fuzzy growth at lesion edges on leaf undersides in humid conditions",
            "Rapid plant collapse; brown, firm lesions on fruit",
        ],
        "favorable_conditions": [
            "Cool (10–20°C), wet, overcast weather",
            "Prolonged leaf wetness; dense canopies",
        ],
        "management": [
            "Scout frequently; remove and destroy infected plants immediately",
            "Avoid overhead irrigation; maximize airflow and spacing",
            "Use resistant cultivars when available",
            "Apply fungicides with anti-oomycete activity (e.g., cyazofamid, mandipropamid); rotate modes of action",
        ],
        "notes": "Emergency disease—respond quickly to first symptoms.",
    },
    {
        "slug": "septoria-leaf-spot",
        "name": "Septoria Leaf Spot (Septoria lycopersici)",
        "overview": "Very common foliar disease causing many small round spots with dark borders and tan/gray centers.",
        "symptoms": [
            "Numerous small (1–3 mm) circular lesions with dark margins and light centers",
            "Tiny black fruiting bodies (pycnidia) visible in lesion centers",
            "Starts on lower leaves; may cause heavy defoliation",
        ],
        "favorable_conditions": [
            "Moderate temps (20–25°C)",
            "High humidity, frequent rains or overhead irrigation",
        ],
        "management": [
            "Remove infected leaves; sanitize plant debris",
            "Mulch and avoid leaf wetness",
            "Protectant fungicides (chlorothalonil, copper) on a schedule; rotate FRAC groups",
        ],
        "notes": "Distinguish from early blight: septoria spots are smaller, more numerous, lack prominent concentric rings.",
    },
    {
        "slug": "bacterial-spot",
        "name": "Bacterial Spot (Xanthomonas spp.)",
        "overview": "Bacterial disease affecting leaves and fruit; spreads fast in warm, wet conditions.",
        "symptoms": [
            "Small dark, greasy-looking leaf spots; may have yellow halos",
            "Ragged leaf edges due to lesion coalescence",
            "Raised, scabby fruit spots (cosmetic damage)",
        ],
        "favorable_conditions": [
            "Warm (25–30°C) and wet weather",
            "Overhead irrigation and wind-driven rain",
        ],
        "management": [
            "Use certified clean seed/transplants; sanitize tools",
            "Copper-based bactericides + mancozeb (check local guidelines)",
            "Avoid working plants when wet; improve airflow",
        ],
        "notes": "Bacterium—not controlled by fungicides; limit spread and protect healthy tissue.",
    },
    {
        "slug": "tomato-mosaic-virus",
        "name": "Tomato Mosaic Virus (ToMV)",
        "overview": "Seed-borne virus causing mosaic/mottling and leaf distortion. Very stable and easily spread mechanically.",
        "symptoms": [
            "Mosaic/mottled light and dark green patterns on leaves",
            "Leaf narrowing, puckering; overall stunting",
            "Uneven fruit ripening; reduced yield",
        ],
        "favorable_conditions": [
            "Any season; spread by handling, tools, and seed",
        ],
        "management": [
            "Strict sanitation: wash hands/tools; avoid tobacco use around plants",
            "Remove infected plants; control weeds (alternate hosts)",
            "Resistant varieties; hot-water seed treatment",
        ],
        "notes": "Viruses have no curative chemicals—focus on prevention and sanitation.",
    },
    {
        "slug": "physiological-leaf-curl",
        "name": "Physiological Leaf Curl (Abiotic)",
        "overview": "Non-pathogenic curling due to heat, drought, pruning, or nutrient stress.",
        "symptoms": [
            "Upward or inward rolling of leaves without distinct lesions",
            "Plants otherwise appear healthy; symptoms fluctuate with stress",
        ],
        "favorable_conditions": [
            "High heat, drought, heavy pruning, excessive nitrogen",
        ],
        "management": [
            "Optimize irrigation; provide consistent soil moisture",
            "Avoid excessive pruning; balance fertility",
            "Mulch and provide shade during heat waves",
        ],
        "notes": "Differentiate from viral leaf curl by absence of mosaic, distortion, or vector presence.",
    },
]

def to_markdown(d):
    lines = [
        f"# {d['name']}",
        "",
        f"**Overview:** {d['overview']}",
        "",
        "## Key Symptoms",
        *[f"- {s}" for s in d["symptoms"]],
        "",
        "## Favorable Conditions",
        *[f"- {c}" for c in d["favorable_conditions"]],
        "",
        "## Management & Control",
        *[f"- {m}" for m in d["management"]],
        "",
        f"**Notes:** {d['notes']}",
    ]
    return "\\n".join(lines)

def main():
    out_dir = Path("knowledge")
    out_dir.mkdir(parents=True, exist_ok=True)
    for d in DISEASES:
        path = out_dir / f"{d['slug']}.md"
        path.write_text(to_markdown(d), encoding="utf-8")
    print(f"Wrote {len(DISEASES)} markdown files to {out_dir.resolve()}")

if __name__ == "__main__":
    main()
