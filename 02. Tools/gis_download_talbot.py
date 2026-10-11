"""Download Talbot-only GeoJSON extracts from ArcGIS REST layers (paginated, EPSG:4326).
Usage: ~/.venvs/esl/bin/python -I 02. Tools/gis_download_talbot.py [slug ...]   (no args = all)
Records each file in Talbot/Manifest.csv.  Skips (and reports) anything > 50 MB.
"""
import sys, json, time, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CORPUS, sha256, upsert_manifest, get

B = "https://mdgeodata.md.gov/imap/rest/services"
M = "https://mdpgis.mdp.state.md.us/arcgis/rest/services"
T = "https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services"
MAXB = 50 * 1024 * 1024
PARCEL_FIELDS = ("JURSCODE,ACCTID,ADDRESS,CITY,ZIPCODE,OWNADD1,OWNADD2,OWNCITY,OWNSTATE,OWNERZIP,LEGAL1,LEGAL2,LEGAL3,"
                 "DR1LIBER,DR1FOLIO,TOWNCODE,DESCTOWN,SUBDIVSN,DESCSUBD,PLAT,PLTLIBER,PLTFOLIO,MAP,GRID,PARCEL,LOT,BLOCK,"
                 "ZONING,ZNCHGDAT,LU,DESCLU,DESCCIUSE,EXCLASS,DESCEXCL,ACRES,LANDAREA,LUOM,YEARBLT,SQFTSTRC,"
                 "NFMLNDVL,NFMIMPVL,NFMTTLVL,CRTARCOD,AGFNDAREA,TRADATE,CONSIDR1,SDATDATE,POLYDATE,PTYPE,SDATWEBADR")
# slug: (layer url, where, outFields, title, use_envelope)
LAYERS = {
 "parcels-sdat-mdp": (f"{B}/PlanningCadastre/MD_ParcelBoundaries/MapServer/0", "JURSCODE='TALB'", PARCEL_FIELDS, "Talbot parcels (MDP/SDAT statewide parcel layer, trimmed fields)", False),
 "parcels-talbot-county-2026feb": (f"{T}/TALBPOLY_2026FEB/FeatureServer/3", "1=1", PARCEL_FIELDS, "Talbot parcels (Talbot County GIS TALBPOLY_2026FEB, trimmed fields)", False),
 "zoning-talbot-county": (f"{T}/Zoning_Effective_With_Annexations/FeatureServer/8", "1=1", "*", "Talbot County zoning districts (county GIS, effective w/ annexations)", False),
 "zoning-generalized-2025-mdp": (f"{M}/PlanningCadastre/Generalized_Zoning_2025/MapServer/0", "JURSCODE='TALB'", "*", "MDP Generalized Zoning 2025 - Talbot (incl. municipalities)", False),
 "overlay-airport": (f"{T}/Airport_Overlay_District/FeatureServer/28", "1=1", "*", "Talbot Airport Overlay District", False),
 "overlay-historic": (f"{T}/Historical_Overlay_District/FeatureServer/21", "1=1", "*", "Talbot Historical Overlay District", False),
 "overlay-gateway": (f"{T}/Gateway_Overlay_District/FeatureServer/22", "1=1", "*", "Talbot Gateway Overlay District", False),
 "critical-area-state-county": (f"{B}/Environment/MD_CriticalAreas/MapServer/1", "Location='Talbot County'", "*", "Chesapeake Bay Critical Area IDA/LDA/RCA - Talbot unincorporated (DNR via iMAP)", False),
 "critical-area-state-towns": (f"{B}/Environment/MD_CriticalAreas/MapServer/0", "County='Talbot'", "*", "Chesapeake Bay Critical Area IDA/LDA/RCA - Talbot towns (DNR via iMAP)", False),
 "critical-area-boundary-line-talbot-county": (f"{T}/Chesapeake_Bay_Critical_Area/FeatureServer/5", "1=1", "*", "Talbot County Critical Area 1000-ft boundary line (county GIS)", False),
 "critical-area-buffer-mgmt-areas": (f"{T}/Buffer_Management_Areas/FeatureServer/27", "1=1", "*", "Talbot Buffer Management Areas (county GIS)", False),
 "pfa-mdp": (f"{B}/PlanningCadastre/MD_PriorityFundingAreas/MapServer/0", "JURSCODE='TALB'", "*", "Priority Funding Areas - Talbot (MDP)", False),
 "septic-tiers-mdp": (f"{M}/PlanningCadastre/Septic_Growth_Tiers/MapServer/0", "JURSCODE='TALB'", "*", "SB236 septic growth tiers - Talbot (MDP)", False),
 "septic-tiers-talbot-county-2016": (f"{T}/Septic_Tier_Land_Use_Plan_Aug2016/FeatureServer/16", "1=1", "*", "Talbot septic tier / land use plan Aug 2016 (county GIS)", False),
 "sewer-service-area-talbot-county": (f"{T}/Sewer_Service_Area_07_11_2023/FeatureServer/15", "1=1", "*", "Talbot sewer service area (W&S plan categories, 2023-07-11)", False),
 "water-service-area-talbot-county": (f"{T}/Water_Service_Area_07_11_2023/FeatureServer/10", "1=1", "*", "Talbot water service area (W&S plan categories, 2023-07-11)", False),
 "easements-malpf": (f"{B}/Environment/MD_ProtectedLands/MapServer/4", "JURSCODE='TALB'", "*", "MALPF ag preservation easements - Talbot (MDP/MDA)", False),
 "easements-met": (f"{B}/Environment/MD_ProtectedLands/MapServer/2", "County='Talbot'", "*", "Maryland Environmental Trust easements - Talbot", False),
 "rural-legacy": (f"{B}/Environment/MD_ProtectedLands/MapServer/1", "County LIKE '%Talbot%'", "*", "Rural Legacy areas touching Talbot (DNR)", False),
 "protected-lands-dnr": (f"{B}/Environment/MD_ProtectedLands/MapServer/0", "County='Talbot'", "*", "DNR owned lands & conservation easements - Talbot", False),
 "protected-lands-local": (f"{B}/Environment/MD_ProtectedLands/MapServer/5", "JURSCODE='TALB'", "*", "Local protected lands - Talbot", False),
 "protected-lands-tdr-pdr": (f"{B}/Environment/MD_ProtectedLands/MapServer/9", "JURSCODE='TALB'", "*", "TDR/PDR protected lands - Talbot", False),
 "protected-lands-talbot-county-2026": (f"{T}/Protected_Lands_2026/FeatureServer/17", "1=1", "*", "Talbot protected lands 2026 (county GIS; easement holder, PPA flag)", False),
 "priority-preservation-areas": (f"{B}/Agriculture/MD_AgriculturalDesignations/MapServer/0", "JURSCODE='TALB'", "*", "Priority Preservation Areas - Talbot (MDP)", False),
 "municipal-boundaries-mdp": (f"{B}/Boundaries/MD_PoliticalBoundaries/MapServer/5", "JURSCODE='TALB'", "*", "Municipal boundaries (detailed) - Talbot (MDP)", False),
 "municipal-boundaries-talbot-county": (f"{T}/Talbot_Municipal_Boundary/FeatureServer/12", "1=1", "*", "Talbot municipal boundaries (county GIS)", False),
 "wetlands-special-state-concern": (f"{B}/Hydrology/MD_Wetlands/MapServer/3", "1=1", "*", "Wetlands of Special State Concern (polygons) in Talbot envelope (MDE/DNR)", True),
 "cbra-areas": (f"{T}/Coastal_Bay_Resource_Act_Areas_2024/FeatureServer/25", "1=1", "*", "Coastal Barrier Resources Act areas (county GIS)", False),
 "limwa-line": (f"{T}/LiMWA_Revised/FeatureServer/3", "1=1", "*", "Limit of Moderate Wave Action line (county GIS)", False),
 "road-centerlines-talbot-county": (f"{T}/Road_Centerlines_0716/FeatureServer/0", "1=1", "full_stnam,roadclass,speedlimit,sha_type,sha_num,incmuni_l,incmuni_r,postcode_l", "Talbot road centerlines (county GIS, trimmed fields)", False),
}

def jget(url, params):
    from urllib.parse import urlencode
    r = get(url + "?" + urlencode(params))
    return r.json()

def envelope():
    d = jget(f"{B}/Boundaries/MD_PoliticalBoundaries/MapServer/1/query",
             {"where": "COUNTY='Talbot'", "returnExtentOnly": "true", "outSR": 4326, "f": "json"})
    e = d["extent"]; return f"{e['xmin']},{e['ymin']},{e['xmax']},{e['ymax']}"

# slug -> readable file name in Talbot/Originals/Maps
FILENAMES = {'parcels-sdat-mdp': 'Parcels (State SDAT)', 'parcels-talbot-county-2026feb': 'Parcels (County, Feb 2026)', 'zoning-talbot-county': 'Zoning (County)', 'zoning-generalized-2025-mdp': 'Zoning Generalized (State, 2025)', 'overlay-airport': 'Overlay - Airport', 'overlay-historic': 'Overlay - Historic', 'overlay-gateway': 'Overlay - Gateway', 'critical-area-state-county': 'Critical Area Classes - County (State)', 'critical-area-state-towns': 'Critical Area Classes - Towns (State)', 'critical-area-boundary-line-talbot-county': 'Critical Area Boundary Line (County)', 'critical-area-buffer-mgmt-areas': 'Critical Area Buffer Management Areas (County)', 'pfa-mdp': 'Priority Funding Areas (State)', 'septic-tiers-mdp': 'Septic Tiers (State)', 'septic-tiers-talbot-county-2016': 'Septic Tiers and Land Use Plan (County, 2016)', 'sewer-service-area-talbot-county': 'Sewer Service Areas (County, 2023)', 'water-service-area-talbot-county': 'Water Service Areas (County, 2023)', 'easements-malpf': 'Ag Easements - MALPF', 'easements-met': 'Easements - Maryland Environmental Trust', 'rural-legacy': 'Rural Legacy Areas', 'protected-lands-dnr': 'Protected Lands - DNR', 'protected-lands-local': 'Protected Lands - Local', 'protected-lands-tdr-pdr': 'Protected Lands - TDR and PDR', 'protected-lands-talbot-county-2026': 'Protected Lands (County, 2026)', 'priority-preservation-areas': 'Priority Preservation Areas', 'municipal-boundaries-mdp': 'Municipal Boundaries (State)', 'municipal-boundaries-talbot-county': 'Municipal Boundaries (County)', 'wetlands-special-state-concern': 'Wetlands of Special State Concern', 'cbra-areas': 'Coastal Barrier Resources Areas', 'limwa-line': 'Limit of Moderate Wave Action', 'road-centerlines-talbot-county': 'Road Centerlines (County)'}


def fetch(slug):
    url, where, fields, title, env = LAYERS[slug]
    base = {"where": where, "outFields": fields, "outSR": 4326, "f": "geojson", "returnGeometry": "true", "orderByFields": "OBJECTID"}
    if slug.startswith("parcels"): base["geometryPrecision"] = 6  # ~0.1 m; keeps parcel files < 50 MB
    if env:
        base.update({"geometry": envelope(), "geometryType": "esriGeometryEnvelope", "inSR": 4326, "spatialRel": "esriSpatialRelIntersects"})
    meta = jget(url, {"f": "json"})
    page = min(int(meta.get("maxRecordCount") or 1000), 2000)
    feats, off = [], 0
    while True:
        d = jget(url + "/query", dict(base, resultOffset=off, resultRecordCount=page))
        if "error" in d: raise RuntimeError(str(d["error"]))
        f = d.get("features", [])
        feats += f; off += len(f)
        if not f or (not d.get("exceededTransferLimit") and len(f) < page): break
        if off * 1500 > MAXB * 3: print("  runaway?", slug, off)
    return url, title, {"type": "FeatureCollection", "features": feats}

def main(slugs):
    out = CORPUS / "Talbot/Originals/Maps"; out.mkdir(parents=True, exist_ok=True)
    for s in slugs:
        try:
            url, title, fc = fetch(s)
            data = json.dumps(fc, separators=(",", ":")).encode()
            if len(data) > MAXB: print(f"SKIP {s}: {len(data)/1e6:.1f} MB > 50 MB"); continue
            p = out / f"{FILENAMES.get(s, s)}.geojson"; tmp = p.with_suffix(".part"); tmp.write_bytes(data); os.replace(tmp, p)
            upsert_manifest("Talbot", [dict(path=str(p.relative_to(CORPUS)), category="map", title=title, source_url=url,
                sha256=sha256(p), bytes=p.stat().st_size, notes=f"{len(fc['features'])} features; EPSG:4326 GeoJSON via paginated ArcGIS REST query; see 01. Maryland/GIS/SOURCES.md")])
            print(f"OK   {s}: {len(fc['features'])} feats, {len(data)/1e6:.2f} MB")
        except Exception as e:
            print(f"FAIL {s}: {str(e)[:200]}")

if __name__ == "__main__":
    main(sys.argv[1:] or list(LAYERS))
