"""Point lookup across the verified Maryland / Talbot GIS endpoints.
  ~/.venvs/esl/bin/python -I 02. Tools/gis_point_lookup.py --lat 38.70 --lon -76.05 [--county talbot] [--sdat]
  ~/.venvs/esl/bin/python -I 02. Tools/gis_point_lookup.py --address "5369 Manadier Rd, Trappe, MD 21673"
Prints one compact JSON object. Endpoints documented in 01. Maryland/GIS/SOURCES.md / sources.json.
Notes: parcel ZONING from SDAT is mostly null/stale -> use county zoning (Talbot) / generalized zoning.
"""
import argparse, json, sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
from curl_cffi import requests as rq

B = "https://mdgeodata.md.gov/imap/rest/services"
M = "https://mdpgis.mdp.state.md.us/arcgis/rest/services"
T = "https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services"
FEMA = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer"
FWS = "https://www.fws.gov/wetlandsmapservice/rest/services/Wetlands/MapServer/0"
SDA = "https://sdmdataaccess.sc.egov.usda.gov/Tabular/post.rest"
GEOCODE = f"{B}/GeocodeServices/MD_MultiroleLocator/GeocodeServer/findAddressCandidates"
SOCRATA = "https://opendata.maryland.gov/resource/ed4q-f8tm.json"

# key: (layer url, outFields, county-only)  county-only = only valid for the named county
STATE = {
 "parcel": (f"{B}/PlanningCadastre/MD_ParcelBoundaries/MapServer/0", "JURSCODE,ACCTID,ADDRESS,CITY,ZIPCODE,OWNADD1,OWNCITY,OWNSTATE,LEGAL1,LEGAL2,DR1LIBER,DR1FOLIO,MAP,GRID,PARCEL,LOT,SUBDIVSN,ZONING,DESCLU,DESCCIUSE,ACRES,LANDAREA,YEARBLT,CRTARCOD,AGFNDAREA,DESCTOWN,TRADATE,CONSIDR1,NFMTTLVL,SDATDATE,SDATWEBADR"),
 "critical_area_county": (f"{B}/Environment/MD_CriticalAreas/MapServer/1", "Type,CritArea,Location"),
 "critical_area_town": (f"{B}/Environment/MD_CriticalAreas/MapServer/0", "Type,CritArea,Town,County"),
 "pfa": (f"{B}/PlanningCadastre/MD_PriorityFundingAreas/MapServer/0", "JURSCODE,CPFA,MUN_CODE,RUVI_NAME,ACRES,CERT_DATE,STATE_ELIGIBLE_STATUS"),
 "septic_tier_mdp": (f"{M}/PlanningCadastre/Septic_Growth_Tiers/MapServer/0", "County,TIER,TIER_CODE,MUNI,Adopt_Date,SRC_DATE"),
 "generalized_zoning_2025": (f"{M}/PlanningCadastre/Generalized_Zoning_2025/MapServer/0", "GENZONE,JURSCODE,MUNICIPALITY_NAME,UPDATEYR"),
 "municipality": (f"{B}/Boundaries/MD_PoliticalBoundaries/MapServer/5", "MUN_NAME,JURSCODE,ANNEXATION_DATE"),
 "wetland_dnr": (f"{B}/Hydrology/MD_Wetlands/MapServer/1", "Type,Class"),
 "wetland_nwi_md": (f"{B}/Hydrology/MD_Wetlands/MapServer/2", "Legend,Wetland,Code"),
 "wetland_special_state_concern": (f"{B}/Hydrology/MD_Wetlands/MapServer/3", "Type"),
 "wetland_nwi_fws": (FWS, "ATTRIBUTE,WETLAND_TYPE,ACRES"),
 "fema_nfhl": (f"{FEMA}/28", "DFIRM_ID,FLD_ZONE,ZONE_SUBTY,SFHA_TF,STATIC_BFE,V_DATUM"),
 "fema_md_floodplain": (f"{B}/Hydrology/MD_Floodplain/MapServer/1", "FLD_ZONE,ZONE_SUBTY,SFHA_TF,STATIC_BFE,EFFECTIVE_DATE"),
 "malpf_easement": (f"{B}/Environment/MD_ProtectedLands/MapServer/4", "Loc_Nm,EsmtHldr,Date_Prot,GIS_Acres,Source_PAID,JURSCODE"),
 "met_easement": (f"{B}/Environment/MD_ProtectedLands/MapServer/2", "Easement,COHOLD,METAcres,County"),
 "rural_legacy": (f"{B}/Environment/MD_ProtectedLands/MapServer/1", "RLArea,County,Acres"),
 "dnr_lands": (f"{B}/Environment/MD_ProtectedLands/MapServer/0", "LABEL,DNRType,DNRName,County"),
 "local_protected_lands": (f"{B}/Environment/MD_ProtectedLands/MapServer/5", "Loc_Nm,EsmtHldr,Category,Acres,JURSCODE"),
 "priority_preservation_area": (f"{B}/Agriculture/MD_AgriculturalDesignations/MapServer/0", "JURSCODE,AREA_NAME,Certified"),
 "green_infrastructure": (f"{B}/Biota/MD_GreenInfrastructure/MapServer/0", "HC_Type,Area_acres"),
}
TALBOT = {
 "talbot_zoning": (f"{T}/Zoning_Effective_With_Annexations/FeatureServer/8", "Zoning2018,LOCATION,Map_No"),
 "talbot_septic_tier_2016": (f"{T}/Septic_Tier_Land_Use_Plan_Aug2016/FeatureServer/16", "SepticTier,Plan_Use,PlanMD,ZONE_06,TOWN"),
 "talbot_sewer_service_area": (f"{T}/Sewer_Service_Area_07_11_2023/FeatureServer/15", "TYPE,Res_No,Date"),
 "talbot_water_service_area": (f"{T}/Water_Service_Area_07_11_2023/FeatureServer/10", "TYPE,Res_No,Date"),
 "talbot_protected_lands": (f"{T}/Protected_Lands_2026/FeatureServer/17", "EasementHolder,GISAcres,PPA"),
 "talbot_buffer_mgmt_area": (f"{T}/Buffer_Management_Areas/FeatureServer/27", "COMMUNITY,TaxMap,Setback"),
 "talbot_historic_overlay": (f"{T}/Historical_Overlay_District/FeatureServer/21", "Dist_Name"),
 "talbot_gateway_overlay": (f"{T}/Gateway_Overlay_District/FeatureServer/22", "towndesc,BUFFERDIS"),
 "talbot_airport_overlay": (f"{T}/Airport_Overlay_District/FeatureServer/28", "ZONING__ID"),
 "talbot_cbra": (f"{T}/Coastal_Bay_Resource_Act_Areas_2024/FeatureServer/25", "Unit,Name,Unit_Type"),
}

def http(method, url, **kw):
    for _ in range(2):
        try:
            r = rq.request(method, url, impersonate="chrome", timeout=25, **kw)
            if r.status_code == 200: return r
        except Exception as e:
            err = e
    return None

def query(url, fields, lon, lat, dist_m=0):
    p = {"f": "json", "geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "inSR": 4326,
         "spatialRel": "esriSpatialRelIntersects", "outFields": fields, "returnGeometry": "false"}
    if dist_m: p.update(distance=dist_m, units="esriSRUnit_Meter")
    r = http("GET", url + "/query?" + urlencode(p))
    if r is None: return {"error": "no response / timeout"}
    d = r.json()
    if "error" in d: return {"error": d["error"].get("message")}
    rows = []
    for f in d.get("features", []):
        a = {k: (v.strip() if isinstance(v, str) else v) for k, v in f["attributes"].items() if v not in (None, "", " ", -9999)}
        rows.append(a)
    return rows

def soils(lon, lat):
    q = f"""SELECT mu.mukey, mu.muname, c.compname, c.comppct_r, c.drainagecl, c.hydricrating, c.hydgrp, ci.interphrc AS septic_rating
FROM mapunit mu JOIN component c ON c.mukey=mu.mukey
LEFT JOIN cointerp ci ON ci.cokey=c.cokey AND ci.mrulename='ENG - Septic Tank Absorption Fields' AND ci.ruledepth=0
WHERE mu.mukey IN (SELECT * FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('point({lon} {lat})')) ORDER BY c.comppct_r DESC"""
    r = http("POST", SDA, json={"query": q, "format": "JSON+COLUMNNAME"})
    if r is None: return {"error": "SDA no response"}
    t = r.json().get("Table", [])
    if len(t) < 2: return []
    h = t[0]; return [dict(zip(h, row)) for row in t[1:]]

def sdat(acct, jurs):
    r = http("GET", SOCRATA + "?" + urlencode({"$where": f"jurisdiction_code_mdp_field_jurscode='{jurs}' AND account_id_mdp_field_acctid='{acct}'", "$limit": 1}))
    if r is None or not r.json(): return {"error": "no SDAT row"}
    d = r.json()[0]
    keep = ("owner_occupancy", "grantor_name", "transfer_date", "_consideration_", "deed_reference_1", "legal_description", "real_property_search_link", "current_assessment_year_total_assessment")
    return {k.split("_mdp_field")[0].split("_sdat_field")[0]: v for k, v in d.items() if any(x in k for x in keep) and v}

def geocode(addr):
    r = http("GET", GEOCODE + "?" + urlencode({"SingleLine": addr, "outSR": 4326, "maxLocations": 3, "f": "json"}))
    c = (r.json().get("candidates") if r else None) or []
    return c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float); ap.add_argument("--lon", type=float)
    ap.add_argument("--address"); ap.add_argument("--county", default=None, help="talbot enables county-hosted layers (auto-detected from parcel JURSCODE if omitted)")
    ap.add_argument("--sdat", action="store_true", help="also pull SDAT owner/sales row from opendata.maryland.gov")
    a = ap.parse_args()
    out = {}
    if a.address:
        c = geocode(a.address); out["geocode"] = [{"address": x["address"], "score": x["score"], "x": x["location"]["x"], "y": x["location"]["y"]} for x in c]
        if not c: print(json.dumps(out)); sys.exit(1)
        a.lon, a.lat = c[0]["location"]["x"], c[0]["location"]["y"]
    if a.lat is None or a.lon is None: ap.error("need --lat/--lon or --address")
    out["point"] = {"lat": a.lat, "lon": a.lon}
    jobs = {k: (lambda u=u, f=f: query(u, f, a.lon, a.lat)) for k, (u, f) in STATE.items()}
    county = (a.county or "").lower()
    if county in ("", "talbot"):   # try county layers; harmless if point is outside Talbot (returns [])
        jobs.update({k: (lambda u=u, f=f: query(u, f, a.lon, a.lat)) for k, (u, f) in TALBOT.items()})
    jobs["soils_ssurgo"] = lambda: soils(a.lon, a.lat)
    with ThreadPoolExecutor(10) as ex:
        res = {k: ex.submit(v) for k, v in jobs.items()}
        for k, f in res.items(): out[k] = f.result()
    p = out.get("parcel")
    if a.sdat and isinstance(p, list) and p:
        out["sdat_record"] = sdat(p[0].get("ACCTID"), p[0].get("JURSCODE"))
    # summary
    s = {}
    def first(k, f):
        v = out.get(k); return v[0].get(f) if isinstance(v, list) and v else None
    s["parcel_acct"] = first("parcel", "ACCTID"); s["acres"] = first("parcel", "ACRES")
    s["county_zoning"] = first("talbot_zoning", "Zoning2018"); s["generalized_zoning"] = first("generalized_zoning_2025", "GENZONE")
    s["critical_area"] = first("critical_area_county", "Type") or first("critical_area_town", "Type")
    s["septic_tier"] = first("septic_tier_mdp", "TIER"); s["pfa"] = bool(out.get("pfa"))
    s["sewer_cat"] = first("talbot_sewer_service_area", "TYPE"); s["water_cat"] = first("talbot_water_service_area", "TYPE")
    s["flood_zone"] = first("fema_nfhl", "FLD_ZONE") or first("fema_md_floodplain", "FLD_ZONE")
    s["wetland"] = bool(out.get("wetland_dnr") and any(r.get("Type") != "Upland" for r in out["wetland_dnr"])) or bool(out.get("wetland_nwi_md") or out.get("wetland_nwi_fws"))
    s["ag_easement"] = bool(out.get("malpf_easement") or out.get("met_easement") or out.get("talbot_protected_lands"))
    sl = out.get("soils_ssurgo"); s["soil"] = sl[0].get("muname") if isinstance(sl, list) and sl else None
    s["septic_rating_dominant"] = sl[0].get("septic_rating") if isinstance(sl, list) and sl else None
    out = {"summary": s, **out}
    print(json.dumps(out, indent=1, default=str))

if __name__ == "__main__":
    main()
