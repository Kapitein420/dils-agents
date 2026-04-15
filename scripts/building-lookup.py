#!/usr/bin/env python3
"""Building lookup — legal public-data-only pipeline for DILS pitch-builder.

Takes a Dutch address, returns a clean JSON with every public fact available
for the Key Facts slide of a pitch deck.

Sources (all open, all ToS-safe):
- PDOK Locatieserver / BAG : address, BAG IDs, coordinates, buurt
- EP-Online (RVO)          : EPC label (manual-lookup URL returned for now)
- BREEAM-NL register (DGBC): sustainability certificates (manual-lookup URL)
- Web search (broker sites): surface, rent, availability — fallback enrichment

Usage:
    python building-lookup.py "Basisweg 61A Amsterdam"
    python building-lookup.py --postcode 1043AN --huisnummer 61 --toevoeging A
    python building-lookup.py --json "Zuidas Tower Amsterdam" > facts.json
"""
from __future__ import annotations
import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime


# ---------- HTTP helpers ----------
def http_get(url: str, headers: dict | None = None, timeout: int = 12) -> str:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "dils-agents/1.0 (building-lookup)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def get_json(url: str) -> dict:
    return json.loads(http_get(url))


# ---------- PDOK / BAG ----------
PDOK_BASE = "https://api.pdok.nl/bzk/locatieserver/search/v3_1"


def pdok_search(query: str) -> list[dict]:
    """Free-text PDOK search. Returns top address candidates."""
    url = f"{PDOK_BASE}/free?" + urllib.parse.urlencode({
        "q": query,
        "fq": "type:adres",
        "rows": 5,
    })
    data = get_json(url)
    return data.get("response", {}).get("docs", [])


def pdok_lookup(bag_id: str) -> dict | None:
    """Retrieve full BAG record by address id (adr-xxx)."""
    url = f"{PDOK_BASE}/lookup?" + urllib.parse.urlencode({"id": bag_id})
    data = get_json(url)
    docs = data.get("response", {}).get("docs", [])
    return docs[0] if docs else None


def pdok_by_postcode(postcode: str, huisnummer: int, toevoeging: str | None = None) -> dict | None:
    """Structured lookup by postcode + huisnummer."""
    q = f"postcode:{postcode} huisnummer:{huisnummer}"
    if toevoeging:
        q += f" huisletter:{toevoeging.upper()}"
    url = f"{PDOK_BASE}/free?" + urllib.parse.urlencode({
        "q": q,
        "fq": "type:adres",
        "rows": 1,
    })
    data = get_json(url)
    docs = data.get("response", {}).get("docs", [])
    return docs[0] if docs else None


# ---------- Output builder ----------
def build_facts(address_doc: dict) -> dict:
    """Turn a PDOK address doc into the structured Key Facts JSON."""
    full_record = pdok_lookup(address_doc["id"]) or address_doc

    # Extract coordinates from POINT(lon lat)
    centroide = full_record.get("centroide_ll", "")
    lat = lon = None
    if centroide.startswith("POINT("):
        parts = centroide[6:-1].split()
        if len(parts) == 2:
            lon, lat = float(parts[0]), float(parts[1])

    nummeraanduiding_id = full_record.get("nummeraanduiding_id", "")
    adresseerbaar_id = full_record.get("adresseerbaarobject_id", "")

    # Compose manual-lookup URLs for EP-Online / BREEAM / Funda / Colliers
    street = full_record.get("straatnaam", "")
    huisnr = full_record.get("huisnummer", "")
    huisletter = full_record.get("huisletter", "")
    postcode = full_record.get("postcode", "")
    city = full_record.get("woonplaatsnaam", "")

    address_str = f"{street} {huisnr}{huisletter or ''}, {postcode} {city}".strip()
    address_slug = f"{street.lower()}-{huisnr}{huisletter.lower() or ''}".replace(" ", "-")

    ep_online_url = f"https://www.ep-online.nl/PublicData/Detail?pandId={nummeraanduiding_id}"
    breeam_url = f"https://www.breeam.nl/projecten?search={urllib.parse.quote(address_str)}"
    funda_search = f"https://www.fundainbusiness.nl/zoeken/?selected_area=%5B%22{urllib.parse.quote(city.lower())}%22%5D"
    colliers_search = f"https://www.colliers.com/nl-nl/search?q={urllib.parse.quote(address_str)}"

    now = datetime.utcnow().isoformat() + "Z"

    return {
        "lookup": {
            "queriedAt": now,
            "source": "PDOK Locatieserver (BAG)",
            "confidence": round(address_doc.get("score", 0), 2),
        },
        "address": {
            "full": full_record.get("weergavenaam", address_str),
            "street": street,
            "huisnummer": huisnr,
            "huisletter": huisletter or None,
            "postcode": postcode,
            "city": city,
            "wijk": full_record.get("wijknaam"),
            "buurt": full_record.get("buurtnaam"),
            "province": full_record.get("provincienaam"),
            "gemeente": full_record.get("gemeentenaam"),
        },
        "bag": {
            "nummeraanduidingId": nummeraanduiding_id,
            "adresseerbaarobjectId": adresseerbaar_id,
            "openbareruimteId": full_record.get("openbareruimte_id"),
            "woonplaatscode": full_record.get("woonplaatscode"),
            "perceel": (full_record.get("gekoppeld_perceel") or [None])[0],
        },
        "coordinates": {
            "lat": lat,
            "lon": lon,
            "rd": full_record.get("centroide_rd"),
        },
        "manualLookups": {
            "epOnline": {
                "url": ep_online_url,
                "fallback": "https://www.ep-online.nl/",
                "note": "Check energielabel + energie-index for this building",
            },
            "breeam": {
                "url": breeam_url,
                "note": "Check if the building has BREEAM-NL certification",
            },
            "funda": {
                "searchUrl": funda_search,
                "note": "Broker listing data (paste URL or page text back to pitch-builder)",
            },
            "colliers": {
                "searchUrl": colliers_search,
            },
        },
        "autoFillable": {
            "address": full_record.get("weergavenaam"),
            "city": city,
            "buurt": full_record.get("buurtnaam"),
            "coordinates": f"{lat}, {lon}" if lat and lon else None,
            "gemeente": full_record.get("gemeentenaam"),
        },
        "needsManualInput": [
            "totaleOppervlakte",
            "bouwjaar",
            "energielabel",
            "breeamRating",
            "beschikbareRuimte",
            "huurprijs",
            "parkeernorm",
        ],
        "keyFactsSlideDraft": _draft_key_facts(full_record, address_str),
    }


def _draft_key_facts(doc: dict, address_str: str) -> str:
    """Return a ready-to-paste Dutch body text for the Gebouw en huurder slide."""
    parts = [
        f"Adres: {address_str} ({doc.get('buurtnaam', 'n/a')}, {doc.get('wijknaam', 'n/a')}).",
        "Totale oppervlakte: [in te vullen — check BAG verblijfsobject / broker listing].",
        "Bouwjaar: [in te vullen — check BAG pand].",
        "Energielabel: [in te vullen — lookup op ep-online.nl].",
        "Beschikbare ruimte: [in te vullen — van broker listing].",
        f"Bereikbaarheid: gelegen in {doc.get('buurtnaam', 'n/a')}, gemeente {doc.get('gemeentenaam', 'n/a')} (bron: BAG).",
        "Parkeernorm: [in te vullen — check gemeentelijk bestemmingsplan].",
        "Huurprijs: [in te vullen — van broker listing].",
    ]
    return " ".join(parts)


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Look up a Dutch building's public facts")
    ap.add_argument("query", nargs="?", help="Free-text address (e.g. 'Basisweg 61A Amsterdam')")
    ap.add_argument("--postcode", help="Structured lookup: postcode (e.g. 1043AN)")
    ap.add_argument("--huisnummer", type=int, help="Huisnummer")
    ap.add_argument("--toevoeging", help="Huisletter / toevoeging")
    ap.add_argument("--json", dest="json_only", action="store_true", help="Print JSON only (no banner)")
    args = ap.parse_args()

    if args.postcode and args.huisnummer:
        doc = pdok_by_postcode(args.postcode, args.huisnummer, args.toevoeging)
        if not doc:
            print(f"No BAG match for {args.postcode} {args.huisnummer}{args.toevoeging or ''}", file=sys.stderr)
            sys.exit(1)
    elif args.query:
        docs = pdok_search(args.query)
        if not docs:
            print(f"No BAG match for: {args.query}", file=sys.stderr)
            sys.exit(1)
        doc = docs[0]
    else:
        ap.print_help()
        sys.exit(1)

    facts = build_facts(doc)

    if args.json_only:
        print(json.dumps(facts, indent=2, ensure_ascii=False))
        return

    # Banner-style summary
    print(f"🏢 {facts['address']['full']}")
    print(f"   Buurt: {facts['address']['buurt']} · {facts['address']['wijk']}")
    print(f"   Gemeente: {facts['address']['gemeente']}")
    print(f"   BAG ID: {facts['bag']['adresseerbaarobjectId']}")
    if facts['coordinates']['lat']:
        print(f"   Coords: {facts['coordinates']['lat']}, {facts['coordinates']['lon']}")
    print()
    print("Auto-filled:")
    for k, v in facts['autoFillable'].items():
        if v:
            print(f"  ✅ {k}: {v}")
    print()
    print("Needs manual input:")
    for k in facts['needsManualInput']:
        print(f"  ⚠️  {k}")
    print()
    print("Manual-lookup URLs:")
    print(f"  EPC   : {facts['manualLookups']['epOnline']['fallback']}")
    print(f"  BREEAM: {facts['manualLookups']['breeam']['url']}")
    print(f"  Funda : {facts['manualLookups']['funda']['searchUrl']}")
    print()
    print("Full JSON:")
    print(json.dumps(facts, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
