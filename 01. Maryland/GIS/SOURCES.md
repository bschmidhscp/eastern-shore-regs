# Maryland / Talbot GIS source catalog
Verified 2026-10-11 by live `?f=json` and point queries. Machine-readable: `sources.json`. Point CLI: `02. Tools/gis_point_lookup.py`. Talbot extracts: `Talbot/Originals/Maps/`.

## How to query a parcel (lat/lon or address)
1. **Address -> point**: Geocoder (#4) `findAddressCandidates?SingleLine=...&outSR=4326`, or Talbot Address_Points (#33). Gives lon/lat.
2. **Parcel**: State parcel polygon (#1) point-intersect -> ACCTID, ACRES, land use, deed liber/folio. Optional owner history/sales/assessment: Socrata (#3) by JURSCODE+ACCTID; SDAT page link = `County=<first 2 of acct>&District=<next 2>&AccountNumber=<last 6>`.
3. **Zoning**: Talbot County zoning (#6) (authoritative; `Zoning2018`), plus overlays. Else MDP Generalized Zoning (#7). Ignore parcel ZONING field.
4. **Critical Area class**: Critical Area counties (#8) then towns (#9) -> Type IDA/LDA/RCA (no hit = outside the 1000-ft area).
5. **Septic tier**: MDP Septic Growth Tiers (#12) (Talbot local #13). **PFA**: #11. **W&S category**: Talbot sewer/water (#14/#15; no polygon = no planned service).
6. **Flood**: FEMA NFHL layer 28 (#21), fallback #22. **Wetlands**: DNR (#17, ignore Type=Upland), NWI (#18/#19), special state concern (#20). **Soils**: SDA SQL (#23) incl. hydric + septic limitation. Easements: #24-28; SLR: #30.
One command does all: `~/.venvs/esl/bin/python -I "02. Tools/gis_point_lookup.py" --lat 38.70 --lon -76.05 [--sdat] | --address "..."`.

## Access notes
- Primary MD iMAP host geodata.md.gov returned 503 'Site Maintenance' on 2026-10-11; use mdgeodata.md.gov/imap/rest/services (identical paths, working).
- Talbot County's own server gis.talbotdes.org (and map.talbotdes.org) timed out; the county's data is also published on ArcGIS Online org services6.arcgis.com/ScyqVZ3lUUihZ0ky (public, works) - source: web map e41dab3d32b2425fa25479c1d7a8a902 (Talbot County Land Use Basemap).
- MDE has no public W&S plan service; only Talbot's own S-/W- category polygons were found. Other counties: check county GIS / MDP 'Sewer Service Areas' later.
- Owner names are suppressed in the MDP/SDAT parcel layers; SDAT Socrata gives the prior-owner (grantor) and deed references.

## Parcels

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 1 | MD Parcel Boundaries (SDAT+MDP) | MDP / SDAT via MD iMAP | `https://mdgeodata.md.gov/imap/rest/services/PlanningCadastre/MD_ParcelBoundaries/MapServer` / **0** | Polygon | ACCTID (county2+district2+acct6), JURSCODE, ADDRESS, ACRES, LANDAREA, LU/DESCLU, ZONING, CRTARCOD, AGFNDAREA, OWNADD1/OWNCITY (mailing addr), LEGAL1-3, DR1LIBER/FOLIO, MAP/GRID/PARCEL/LOT, SUBDIVSN/PLAT, TRADATE/CONSIDR1, NFMTTLVL, SDATWEBADR | SDATDATE=2026MAY (Talbot); no layer editing date; maxRecordCount 1000 | statewide |
| 2 | MD Property Data (parcel points) | MDP / SDAT | `https://mdgeodata.md.gov/imap/rest/services/PlanningCadastre/MD_PropertyData/MapServer` / **0** | Point | same attributes as parcel polygons + DIGXCORD/DIGYCORD | maxRecordCount 2000 | statewide |
| 3 | SDAT Real Property (Socrata, tabular) | MD SDAT/MDP via opendata.maryland.gov | `https://opendata.maryland.gov/resource/ed4q-f8tm.json` / **ed4q-f8tm** | Table (lat/lon cols) | jurisdiction_code_mdp_field_jurscode, account_id_mdp_field_acctid, real_property_search_link, legal_description_line_1..3, deed_reference_1_liber/folio, sales_segment_1..3 (grantor name, transfer date, consideration, mkt land/improvement value), current_assessment_year_total_assessment, premise address, land_use_code, zoning_code | rowsUpdatedAt 2026-10 (epoch 1791307520) | statewide |
| 4 | Geocoder (address -> point; also by ACCTID) | MD iMAP | `https://mdgeodata.md.gov/imap/rest/services/GeocodeServices/MD_MultiroleLocator/GeocodeServer` | Locator | SingleLine | - | statewide |
| 5 | Talbot County parcels (TALBPOLY_2026FEB) | Talbot County Office of GIS | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/TALBPOLY_2026FEB/FeatureServer` / **3** | Polygon | same schema as state parcels | lastEdit 2026-08-07; SDATDATE=2026FEB; max 2000 | Talbot |

**#1 example:** `https://mdgeodata.md.gov/imap/rest/services/PlanningCadastre/MD_ParcelBoundaries/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=ACCTID,ADDRESS,ACRES,ZONING,DESCLU`  
Notes: NO owner-name field (hidden). SDAT ZONING is blank for ~88% of Talbot parcels and stale (A2 vs county AC) - do not rely on it. CRTARCOD also usually null; use Critical Area polygons. ACRES can be 0/null for lots; use LANDAREA/POLYACRES. Fields ending in 'ZONING' etc. same in Parcel Points layer (PropertyData/0).  
Talbot extract: Talbot/Originals/Maps/parcels-sdat-mdp.geojson (45.7 MB, 22,368 feats, trimmed fields, 6-dp coords)

**#2 example:** `https://mdgeodata.md.gov/imap/rest/services/PlanningCadastre/MD_PropertyData/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=ACCTID,ADDRESS&distance=100&units=esriSRUnit_Meter`  
Notes: Use for address/acct search by attribute (where=ACCTID='...'). Layers 1-2 = tax maps/grids.  

**#3 example:** `https://opendata.maryland.gov/resource/ed4q-f8tm.json?$where=jurisdiction_code_mdp_field_jurscode='TALB' AND account_id_mdp_field_acctid='2103125696'&$limit=1`  
Notes: 'Hidden owner names': current owner suppressed; prior owner = sales_segment_1 grantor. Gives deed liber/folio for land-records lookup and link to SDAT detail page. SoQL column names are the long ones shown. No API key needed (throttled w/o app token).  

**#4 example:** `https://mdgeodata.md.gov/imap/rest/services/GeocodeServices/MD_MultiroleLocator/GeocodeServer/findAddressCandidates?SingleLine=5369+Manadier+Rd,+Trappe,+MD+21673&outSR=4326&maxLocations=2&f=json`  
Notes: Returns address-range and parcel-account candidates (score 100 both). Also GeocodeServices/MD_ParcelAccountNumberLocator.  

**#5 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/TALBPOLY_2026FEB/FeatureServer/3/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=ACCTID,ADDRESS,ACRES`  
Notes: Same schema, older SDAT vintage than state layer (Feb vs May 2026); county may carry newer polygons. Same zoning-field caveat.  
Talbot extract: Talbot/Originals/Maps/parcels-talbot-county-2026feb.geojson (45.3 MB)

## Zoning

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 6 | Talbot County zoning districts | Talbot County Office of GIS (byelton_Talbot) | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Zoning_Effective_With_Annexations/FeatureServer` / **8** | Polygon | Zoning2018 (RC, RR, WRC, AC, VM, VC, LC, GC, LI, TR, TC, VH, VR, CP, MUNI), LOCATION, Map_No, Acres | lastEdit 2026-09-15; 414 feats | Talbot |
| 7 | MDP Generalized Zoning 2025 | MDP | `https://mdpgis.mdp.state.md.us/arcgis/rest/services/PlanningCadastre/Generalized_Zoning_2025/MapServer` / **0** | Polygon | GENZONE, JURSCODE, MUNICIPALITY_NAME, UPDATEYR, ACRES, ABBREVIATION | UPDATEYR 20250228; max 2000 | statewide |

**#6 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Zoning_Effective_With_Annexations/FeatureServer/8/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Zoning2018,LOCATION,Map_No`  
Notes: AUTHORITATIVE for unincorporated Talbot. Field is named Zoning2018 (code list predates later text amendments - verify against current code). Municipal land = MUNI/town zoning (Easton, St Michaels, Oxford, Trappe, Queenstown...) -> use town zoning or MDP generalized. Overlays: Airport (layer 28), Historical (21), Gateway (22).  
Talbot extract: zoning-talbot-county.geojson (8.8 MB); overlay-airport/-historic/-gateway.geojson

**#7 example:** `https://mdpgis.mdp.state.md.us/arcgis/rest/services/PlanningCadastre/Generalized_Zoning_2025/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=GENZONE,JURSCODE,UPDATEYR`  
Notes: Statewide, includes municipalities (use for the other 8 counties as a first pass); categories only (e.g. RURAL LOW DENSITY RESIDENTIAL), not local district codes. Older: Generalized_Zoning MapServer.  
Talbot extract: zoning-generalized-2025-mdp.geojson (10.5 MB)

## Critical Area

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 8 | Critical Areas - Counties (IDA/LDA/RCA) | DNR / MDP / CBCAC via MD iMAP | `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_CriticalAreas/MapServer` / **1** | Polygon | Type (IDA, LDA, RCA, WET, FED), CritArea, Location (county) | max 8000; no edit date exposed | statewide |
| 9 | Critical Area Towns | DNR via MD iMAP | `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_CriticalAreas/MapServer` / **0** | Polygon | Type, CritArea, Town, County | max 8000 | statewide |
| 10 | Talbot 1000-ft Critical Area line + Buffer Management Areas | Talbot County Office of GIS | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Chesapeake_Bay_Critical_Area/FeatureServer` / **5** | Polyline | TYPE (line only; no class) | lastEdit 2026-07-17 | Talbot |

**#8 example:** `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_CriticalAreas/MapServer/1/query?geometry=-76.33,38.717&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Type,CritArea,Location`  
Notes: Classification is by polygon; 'WET'=tidal wetlands, 'FED'=federal. Example uses a Tilghman point (point 38.70,-76.05 is outside the Critical Area). Talbot has 327 polygons (7.5 MB). DNR interpretation - verify with county Critical Area map/Planning staff. Town polygons are layer 0 (Easton, St Michaels, Oxford...).  
Talbot extract: critical-area-state-county.geojson, critical-area-state-towns.geojson

**#9 example:** `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_CriticalAreas/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Type,CritArea,Town,County`  
Notes: Talbot: Easton, St. Michaels, Oxford, Queen Anne (50 polys).  

**#10 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Chesapeake_Bay_Critical_Area/FeatureServer/5/query?where=1%3D1&outFields=TYPE&resultRecordCount=2&f=json`  
Notes: Line only - cannot classify. Buffer_Management_Areas (layer 27; COMMUNITY, TaxMap, Setback) is county polygons.  
Talbot extract: critical-area-boundary-line-talbot-county, critical-area-buffer-mgmt-areas

## PFA

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 11 | Priority Funding Areas | MDP | `https://mdgeodata.md.gov/imap/rest/services/PlanningCadastre/MD_PriorityFundingAreas/MapServer` / **0** | Polygon | JURSCODE, CPFA, MUN_CODE, RUVI_CODE, RUVI_NAME, ACRES, CERT_DATE, STATE_ELIGIBLE_STATUS | CERT_DATE per feature; max 4000 | statewide |

**#11 example:** `https://mdgeodata.md.gov/imap/rest/services/PlanningCadastre/MD_PriorityFundingAreas/MapServer/0/query?geometry=-76.33,38.717&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=JURSCODE,RUVI_NAME,CPFA,CERT_DATE,STATE_ELIGIBLE_STATUS`  
Notes: Point must be inside a polygon (empty result = not in PFA). Example is Tilghman (rural village). Also a FeatureServer twin.  
Talbot extract: pfa-mdp.geojson (2.4 MB)

## Septic tiers

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 12 | SB 236 Septic Growth Tiers (state) | MDP | `https://mdpgis.mdp.state.md.us/arcgis/rest/services/PlanningCadastre/Septic_Growth_Tiers/MapServer` / **0** | Polygon | County, TIER (Tier 1, 1A, 2, 2A-C, 3A-C, 4), TIER_CODE, JURSCODE, MUNI, Adopt_Date, SRC_DATE, NOTE | Talbot adopted 2016-06; src 2018-10-30; max 2000 | statewide |
| 13 | Talbot septic tier / land use plan (Aug 2016) | Talbot County Office of GIS | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Septic_Tier_Land_Use_Plan_Aug2016/FeatureServer` / **16** | Polygon | SepticTier (Tier I-IV, II-A.., III-A..), Plan_Use, PlanMD, ZONE_06, TOWN | lastEdit 2026-07-17 | Talbot |

**#12 example:** `https://mdpgis.mdp.state.md.us/arcgis/rest/services/PlanningCadastre/Septic_Growth_Tiers/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=County,TIER,TIER_CODE,Adopt_Date`  
Notes: Statewide uniform schema. Large vertex count (Talbot 18 MB). Tier IV = no major subdivision on septic (>=5 lots) under 2012 Sustainable Growth Act.  
Talbot extract: septic-tiers-mdp.geojson (18.0 MB)

**#13 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Septic_Tier_Land_Use_Plan_Aug2016/FeatureServer/16/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=SepticTier,Plan_Use,ZONE_06`  
Notes: Local source of the state layer; includes a 'Tier T' value (meaning unverified).  
Talbot extract: septic-tiers-talbot-county-2016.geojson (16.5 MB)

## Water & sewer

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 14 | Talbot Sewer Service Area (S-1/S-2/S-3) | Talbot County Office of GIS | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Sewer_Service_Area_07_11_2023/FeatureServer` / **15** | Polygon | TYPE (S-1, S-2, S-3), Res_No, Date, ID | lastEdit 2026-07-17; plan date 2023-07-11 | Talbot |
| 15 | Talbot Water Service Area (W-1/W-2/W-3) | Talbot County Office of GIS | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Water_Service_Area_07_11_2023/FeatureServer` / **10** | Polygon | TYPE (W-1..W-3), Res_No, Date | lastEdit 2026-07-17 | Talbot |
| 16 | Water Resource Areas (MDP Water Resource Elements) | MDP | `https://mdpgis.mdp.state.md.us/arcgis/rest/services/PlanningCadastre/Water_Resource_Areas/MapServer` / **0** | Polygon | CO, Status, WWR, WellHead, TierII, PresCons_T | Src_Date 2020/03/04 | statewide |

**#14 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Sewer_Service_Area_07_11_2023/FeatureServer/15/query?geometry=-76.33,38.717&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=TYPE,Res_No,Date`  
Notes: County W&S plan categories as GIS. No polygon = no planned public service (S-6/W-6 implied). No statewide W&S layer found: MDE ArcGIS (mdewin64.mde.state.md.us) folders MDE_WSP/MDE_Wastewater/WSIPS_PROD list no public services.  
Talbot extract: sewer-service-area-talbot-county.geojson

**#15 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Water_Service_Area_07_11_2023/FeatureServer/10/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=TYPE,Res_No,Date`  
Notes: As above.  
Talbot extract: water-service-area-talbot-county.geojson

**#16 example:** `https://mdpgis.mdp.state.md.us/arcgis/rest/services/PlanningCadastre/Water_Resource_Areas/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=CO,Status,WellHead,TierII`  
Notes: County-level coarse; wellhead protection / Tier II stream flags. Not a service-area layer.  

## Wetlands

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 17 | DNR Wetlands (polygon) | MD DNR via iMAP | `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Wetlands/MapServer` / **1** | Polygon | Type (incl. Upland), Class | max 65000 | statewide |
| 18 | National Wetlands Inventory (state-hosted copy) | USFWS via MD iMAP | `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Wetlands/MapServer` / **2** | Polygon | Wetland, Code (Cowardin), Legend, Decoder | max 65000 | statewide |
| 19 | NWI (USFWS direct) | USFWS | `https://www.fws.gov/wetlandsmapservice/rest/services/Wetlands/MapServer` / **0** | Polygon | ATTRIBUTE (Cowardin code), WETLAND_TYPE, ACRES | maxRecordCount 500; currency per FWS Wetlands Data Layer | statewide |
| 20 | Wetlands of Special State Concern (polygon / linear) | MDE/DNR via iMAP | `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Wetlands/MapServer` / **3** | Polygon (4 = polyline) | Type | max 65000 | statewide |

**#17 example:** `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Wetlands/MapServer/1/query?geometry=-76.33,38.717&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Type,Class`  
Notes: Includes 'Upland' polygons - treat Type='Upland' as no wetland. Layer 0 = linear DNR wetlands. Talbot county also hosts Talbot_DNR_Wetlands (FeatureServer/13).  

**#18 example:** `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Wetlands/MapServer/2/query?geometry=-76.2250,38.7550&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Wetland,Code,Legend`  
Notes: Example point is open Chesapeake water. Do not bulk-download.  

**#19 example:** `https://www.fws.gov/wetlandsmapservice/rest/services/Wetlands/MapServer/0/query?geometry=-76.2250,38.7550&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=ATTRIBUTE,WETLAND_TYPE,ACRES`  
Notes: Responds; verified empty at test points and non-error. Most current federal source.  

**#20 example:** `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Wetlands/MapServer/3/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Type`  
Notes: Rare; Talbot envelope returned 17 polys (may include neighbors).  
Talbot extract: wetlands-special-state-concern.geojson

## Flood

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 21 | FEMA NFHL - Flood Hazard Zones | FEMA | `https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer` / **28** | Polygon | FLD_ZONE (AE, VE, X, A, AO), ZONE_SUBTY, SFHA_TF, STATIC_BFE, V_DATUM, DFIRM_ID (Talbot 24041C) | FEMA-maintained; max 2000 | statewide |
| 22 | MD Effective FEMA Floodplain (state copy) | MDE/FEMA via iMAP | `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Floodplain/MapServer` / **1** | Polygon | FLD_ZONE, ZONE_SUBTY, SFHA_TF, STATIC_BFE, EFFECTIVE_DATE (e.g. 8/2013) | max 36000 | statewide |

**#21 example:** `https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query?geometry=-76.33,38.717&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=FLD_ZONE,ZONE_SUBTY,SFHA_TF,STATIC_BFE`  
Notes: Verified live. Layer 28 = flood hazard zones (other layers not verified). Coastal A (CoastalAE) appears via ZONE_SUBTY / LiMWA line; VE zone is FLD_ZONE='VE'. No result in Talbot = zone unmapped/outside SFHA polygon (X polygons exist in most mapped areas).  

**#22 example:** `https://mdgeodata.md.gov/imap/rest/services/Hydrology/MD_Floodplain/MapServer/1/query?geometry=-76.33,38.717&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=FLD_ZONE,ZONE_SUBTY,STATIC_BFE,EFFECTIVE_DATE`  
Notes: Backup to NFHL. Also Hydrology/MD_LiMWA (LiMWA line). Talbot hosts FEMA_Flood_Zones_2016/FeatureServer/24 and LiMWA_Revised/3 (downloaded limwa-line).  

## Soils

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 23 | NRCS SSURGO - Soil Data Access (SQL) | USDA NRCS | `https://sdmdataaccess.sc.egov.usda.gov/Tabular/post.rest` | Tabular (POST) | mapunit.muname/mukey, component.compname/comppct_r/drainagecl/hydricrating/hydgrp, cointerp.interphrc (rule 'ENG - Septic Tank Absorption Fields') | SSURGO annual refresh | statewide |

**#23 example:** `POST JSON {"query":"SELECT ... FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('point(-76.05 38.70)')","format":"JSON+COLUMNNAME"}  (see gis_point_lookup.py soils())`  
Notes: Verified. Septic rating classes: Not limited / Somewhat limited / Very limited (nearly all Talbot soils are 'Very limited' by NRCS rule - county perc tests govern). hydricrating Yes/No per component; weight by comppct_r. Spatial alt: Talbot Soils_2020/FeatureServer/14 (MUSYM, MUKEY) at Talbot GIS.  

## Easements

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 24 | MALPF easements | MDP / MDA via iMAP | `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_ProtectedLands/MapServer` / **4** | Polygon | Loc_Nm, EsmtHldr, Date_Prot, GIS_Acres, Source_PAID, JURSCODE, Category | max 36000 | statewide |
| 25 | MET easements | MET/DNR | `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_ProtectedLands/MapServer` / **2** | Polygon | Easement, COHOLD, METAcres, County | max 36000 | statewide |
| 26 | Rural Legacy; DNR lands; Local protected; TDR/PDR; Forest Cons.; CELCP; Private conservation | DNR / MDP | `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_ProtectedLands/MapServer` / **1 RL, 0 DNR, 5 local, 9 TDR/PDR, 3 FCA, 6 CELCP, 7 private** | Polygon | RLArea/County; DNRType/DNRName; Loc_Nm/EsmtHldr/JURSCODE | max 36000 | statewide |
| 27 | Priority Preservation Areas | MDP | `https://mdgeodata.md.gov/imap/rest/services/Agriculture/MD_AgriculturalDesignations/MapServer` / **0** | Polygon | JURSCODE, AREA_NAME, Certified, GIS_Acres | max 10000 | statewide |
| 28 | Talbot Protected Lands 2026 | Talbot County Office of GIS | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Protected_Lands_2026/FeatureServer` / **17** | Polygon | EasementHolder, GISAcres, PPA (YES/NO), ApprovalNumber | lastEdit 2026-09-16; 347 feats | Talbot |

**#24 example:** `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_ProtectedLands/MapServer/4/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Loc_Nm,EsmtHldr,Date_Prot,GIS_Acres,JURSCODE`  
Notes: Test point is inside MALPF 'Blades' easement (279 ac).  
Talbot extract: easements-malpf.geojson (91 polys)

**#25 example:** `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_ProtectedLands/MapServer/2/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=Easement,COHOLD,METAcres,County`  
Talbot extract: easements-met.geojson (109)

**#26 example:** `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_ProtectedLands/MapServer/1/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=RLArea,County,Acres`  
Notes: Query each layer id separately.  
Talbot extract: rural-legacy, protected-lands-dnr/-local/-tdr-pdr .geojson

**#27 example:** `https://mdgeodata.md.gov/imap/rest/services/Agriculture/MD_AgriculturalDesignations/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=JURSCODE,AREA_NAME,Certified`  
Talbot extract: priority-preservation-areas.geojson

**#28 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Protected_Lands_2026/FeatureServer/17/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=EasementHolder,GISAcres,PPA`  
Notes: Most current/complete for Talbot (all holders incl. Eastern Shore Land Conservancy).  
Talbot extract: protected-lands-talbot-county-2026.geojson

## Forest / Green

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 29 | Maryland Green Infrastructure (hubs/corridors/gaps) | DNR via iMAP | `https://mdgeodata.md.gov/imap/rest/services/Biota/MD_GreenInfrastructure/MapServer` / **0** | Polygon | HC_Type (Hub/Corridor/Gap), Area_acres | max 30000 | statewide |

**#29 example:** `https://mdgeodata.md.gov/imap/rest/services/Biota/MD_GreenInfrastructure/MapServer/0/query?geometry=-76.05,38.70&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=HC_Type,Area_acres`  
Notes: Relevant to Forest Conservation Act/ mitigation. Also Biota/MD_Forests (0 Forests of Recognized Importance, 1 Forested Buffers). Not downloaded (large).  

## Sea level rise

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 30 | CoastSmart CRAB flood depth + SLAMM 2050 | DNR via iMAP | `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_CoastSmartCRAB/MapServer` / **0** | Raster (identify) | Classify.Pixel Value (ft depth), Class value | - | statewide |

**#30 example:** `https://mdgeodata.md.gov/imap/rest/services/Environment/MD_CoastSmartCRAB/MapServer/identify?geometry=-76.33,38.717&geometryType=esriGeometryPoint&sr=4326&tolerance=3&mapExtent=-76.4,38.65,-76.25,38.78&imageDisplay=600,400,96&layers=all&f=json`  
Notes: Use identify (rasters). SLAMM2050: Environment/MD_CoastalFloodSLAMM2050/MapServer layer 1 (class value codes). Verified both return pixel values. Also FFRMS ImageServers.  

## Boundaries/Roads

| # | Layer | Publisher | Service URL / layer id | Geom | Key fields | Dates | Scope |
|---|---|---|---|---|---|---|---|
| 31 | Municipal boundaries (detailed) | MDP via iMAP | `https://mdgeodata.md.gov/imap/rest/services/Boundaries/MD_PoliticalBoundaries/MapServer` / **5** | Polygon | MUN_NAME, JURSCODE, MUN_CODE, ANNEXATION_DATE, RESOLUTION_NUMBER, ACRES | max 3000 | statewide |
| 32 | Road centerlines | MDOT SHA via iMAP; Talbot County | `https://mdgeodata.md.gov/imap/rest/services/Transportation/MD_RoadCenterlines/MapServer` / **3** | Polyline | COUNTY, ROADNAMESHA, ROUTEID (state); county layer: full_stnam, roadclass, speedlimit, sha_type | max 65000 | statewide |
| 33 | Talbot address points; building footprints; sewer/water infrastructure | Talbot County Office of GIS | `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Address_Points/FeatureServer` / **1** | Point | fulladdress, add_number, street, post_comm, latitude, longitude | lastEdit 2026-10-01 | Talbot |

**#31 example:** `https://mdgeodata.md.gov/imap/rest/services/Boundaries/MD_PoliticalBoundaries/MapServer/5/query?geometry=-76.0680,38.7740&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false&f=json&outFields=MUN_NAME,JURSCODE,ANNEXATION_DATE`  
Notes: County boundaries = layer 1 (COUNTY, COUNTYNUM). Talbot hosts Talbot_Municipal_Boundary/12 (5 towns).  
Talbot extract: municipal-boundaries-mdp.geojson, municipal-boundaries-talbot-county.geojson

**#32 example:** `https://mdgeodata.md.gov/imap/rest/services/Transportation/MD_RoadCenterlines/MapServer/3/query?where=COUNTY%3D%27Talbot%27&outFields=ROADNAMESHA&resultRecordCount=2&f=json`  
Notes: Talbot county layer: Road_Centerlines_0716/FeatureServer/0 (4,079 segs, downloaded). Also Transportation/MD_AnnualAverageDailyTraffic.  
Talbot extract: road-centerlines-talbot-county.geojson (2.9 MB)

**#33 example:** `https://services6.arcgis.com/ScyqVZ3lUUihZ0ky/arcgis/rest/services/Address_Points/FeatureServer/1/query?where=fulladdress+LIKE+%275369+MANADIER%25%27&outFields=fulladdress&f=json`  
Notes: Building_Footprint (26), Out_Building_Footprint (18), Driveways (4) in same org. Public sewer/water INFRASTRUCTURE (pipes/plants) NOT found public.  

## Talbot extracts downloaded (`Talbot/Originals/Maps/`, EPSG:4326, recorded in `Talbot/Manifest.csv`)

| File | MB |
|---|---|
| cbra-areas.geojson | 0.05 |
| critical-area-boundary-line-talbot-county.geojson | 1.31 |
| critical-area-buffer-mgmt-areas.geojson | 0.67 |
| critical-area-state-county.geojson | 7.48 |
| critical-area-state-towns.geojson | 0.28 |
| easements-malpf.geojson | 1.04 |
| easements-met.geojson | 0.39 |
| limwa-line.geojson | 0.14 |
| municipal-boundaries-mdp.geojson | 1.08 |
| municipal-boundaries-talbot-county.geojson | 0.21 |
| overlay-airport.geojson | 0.00 |
| overlay-gateway.geojson | 0.02 |
| overlay-historic.geojson | 0.09 |
| parcels-sdat-mdp.geojson | 45.71 |
| parcels-talbot-county-2026feb.geojson | 45.28 |
| pfa-mdp.geojson | 2.39 |
| priority-preservation-areas.geojson | 0.44 |
| protected-lands-dnr.geojson | 0.01 |
| protected-lands-local.geojson | 0.14 |
| protected-lands-talbot-county-2026.geojson | 2.14 |
| protected-lands-tdr-pdr.geojson | 0.04 |
| road-centerlines-talbot-county.geojson | 2.89 |
| rural-legacy.geojson | 0.08 |
| septic-tiers-mdp.geojson | 18.00 |
| septic-tiers-talbot-county-2016.geojson | 16.49 |
| sewer-service-area-talbot-county.geojson | 2.22 |
| water-service-area-talbot-county.geojson | 0.60 |
| wetlands-special-state-concern.geojson | 0.10 |
| zoning-generalized-2025-mdp.geojson | 10.55 |
| zoning-talbot-county.geojson | 8.81 |

Not downloaded by design (on-demand point queries only): FEMA NFHL, NWI, SSURGO, wetlands DNR, Green Infrastructure, forests, CRAB/SLAMM. Parcels were exported with trimmed fields and 6-decimal coordinates to stay under 50 MB.
Regenerate downloads: `02. Tools/gis_download_talbot.py [slug...]`; regenerate this catalog: `02. Tools/gis_build_catalog.py` (test outputs below are appended by gis_point_lookup tests).

## Test outputs of gis_point_lookup.py (2026-10-11)

### Rural Talbot: --lat 38.70 --lon -76.05 --sdat (5369 Manadier Rd, 254.9 ac, MALPF easement)
```json
{
 "summary": {
  "parcel_acct": "2103125696",
  "acres": 254.92,
  "county_zoning": "AC",
  "generalized_zoning": "RURAL LOW DENSITY RESIDENTIAL",
  "critical_area": null,
  "septic_tier": "Tier 4",
  "pfa": false,
  "sewer_cat": null,
  "water_cat": null,
  "flood_zone": "X",
  "wetland": false,
  "ag_easement": true,
  "soil": "Woodstown loam, 0 to 2 percent slopes, Mid-Atlantic Coastal Plain",
  "septic_rating_dominant": "Very limited"
 },
 "point": {
  "lat": 38.7,
  "lon": -76.05
 },
 "parcel": [
  {
   "JURSCODE": "TALB",
   "ACCTID": "2103125696",
   "ADDRESS": "5369 MANADIER RD",
   "CITY": "TRAPPE",
   "ZIPCODE": "21673",
   "OWNADD1": "2812 OCEAN GTWY",
   "OWNCITY": "TRAPPE",
   "OWNSTATE": "MD",
   "LEGAL1": "IMPS254.922 AC",
   "LEGAL2": "E/S HAMBLETON TO",
   "DR1LIBER": "02789",
   "DR1FOLIO": "0028",
   "MAP": "0049",
   "GRID": "0013",
   "PARCEL": "0016",
   "ZONING": "A2",
   "DESCLU": "Agricultural",
   "ACRES": 254.92,
   "LANDAREA": 254.92,
   "YEARBLT": "1900",
   "TRADATE": "20201230",
   "NFMTTLVL": 484800,
   "SDATDATE": "2026MAY",
   "SDATWEBADR": "https://sdat.dat.maryland.gov/RealProperty/Pages/viewdetails.aspx?County=21&SearchType=ACCT&District=03&AccountNumber=125696"
  }
 ],
 "talbot_zoning": [
  {
   "Zoning2018": "AC"
  }
 ],
 "generalized_zoning_2025": [
  {
   "GENZONE": "RURAL LOW DENSITY RESIDENTIAL",
   "JURSCODE": "TALB",
   "UPDATEYR": "20250228"
  }
 ],
 "septic_tier_mdp": [
  {
   "County": "Talbot County",
   "TIER": "Tier 4",
   "TIER_CODE": 4,
   "Adopt_Date": 1465257600000,
   "SRC_DATE": "20181030"
  }
 ],
 "fema_nfhl": [
  {
   "DFIRM_ID": "24041C",
   "FLD_ZONE": "X",
   "ZONE_SUBTY": "AREA OF MINIMAL FLOOD HAZARD",
   "SFHA_TF": "F"
  }
 ],
 "wetland_dnr": [
  {
   "Type": "Upland",
   "Class": "U"
  }
 ],
 "malpf_easement": [
  {
   "Loc_Nm": "BLADES",
   "EsmtHldr": "Maryland Agricultural Land Preservation Foundation",
   "Date_Prot": 1203724800000,
   "GIS_Acres": 285.8680454,
   "Source_PAID": "20-95-02",
   "JURSCODE": "TALB"
  }
 ],
 "priority_preservation_area": [
  {
   "JURSCODE": "TALB",
   "Certified": "YES"
  }
 ],
 "soils_ssurgo": [
  {
   "mukey": "1712532",
   "muname": "Woodstown loam, 0 to 2 percent slopes, Mid-Atlantic Coastal Plain",
   "compname": "Woodstown",
   "comppct_r": "80",
   "drainagecl": "Moderately well drained",
   "hydricrating": "No",
   "hydgrp": "C",
   "septic_rating": "Very limited"
  },
  {
   "mukey": "1712532",
   "muname": "Woodstown loam, 0 to 2 percent slopes, Mid-Atlantic Coastal Plain",
   "compname": "Hammonton",
   "comppct_r": "6",
   "drainagecl": "Moderately well drained",
   "hydricrating": "No",
   "hydgrp": "B",
   "septic_rating": "Very limited"
  },
  {
   "mukey": "1712532",
   "muname": "Woodstown loam, 0 to 2 percent slopes, Mid-Atlantic Coastal Plain",
   "compname": "Fallsington",
   "comppct_r": "6",
   "drainagecl": "Poorly drained",
   "hydricrating": "Yes",
   "hydgrp": "B/D",
   "septic_rating": "Very limited"
  },
  {
   "mukey": "1712532",
   "muname": "Woodstown loam, 0 to 2 percent slopes, Mid-Atlantic Coastal Plain",
   "compname": "Hambrook",
   "comppct_r": "4",
   "drainagecl": "Well drained",
   "hydricrating": "No",
   "hydgrp": "B",
   "septic_rating": "Very limited"
  },
  {
   "mukey": "1712532",
   "muname": "Woodstown loam, 0 to 2 percent slopes, Mid-Atlantic Coastal Plain",
   "compname": "Mattapex",
   "comppct_r": "4",
   "drainagecl": "Moderately well drained",
   "hydricrating": "No",
   "hydgrp": "C",
   "septic_rating": "Very limited"
  }
 ],
 "sdat_record": {
  "real_property_search_link": {
   "url": "https://sdat.dat.maryland.gov/RealProperty/Pages/viewdetails.aspx?County=21&SearchType=ACCT&District=03&AccountNumber=125696"
  },
  "record_key_owner_occupancy_code": "D",
  "legal_description_line_1": "IMPS (Improvements). 254.922 AC",
  "legal_description_line_2": "E/S HAMBLETON TO",
  "legal_description_line_3": "MANADIER RD",
  "deed_reference_1_liber": "02789",
  "deed_reference_1_folio": "0028",
  "sales_segment_1_grantor_name": "BLADES  JEAN WISE L/E",
  "sales_segment_1_grantor_deed_reference_1_liber": "00872",
  "sales_segment_1_grantor_deed_reference_1_folio": "0775",
  "sales_segment_1_transfer_date_yyyy_mm_dd": "2020.12.30",
  "sales_segment_1_consideration": "0",
  "sales_segment_2_grantor_name": "BLADES, JEAN WISE L/E",
  "sales_segment_2_grantor_deed_reference_1_liber": "00872",
  "sales_segment_2_grantor_deed_reference_1_folio": "0775",
  "sales_segment_2_transfer_date_yyyy_mm_dd": "1999.11.09",
  "sales_segment_2_consideration": "0",
  "sales_segment_3_grantor_name": "WISE, GRANVILLE L & ETHEL S T/C",
  "sales_segment_3_grantor_deed_reference_1_liber": "00000",
  "sales_segment_3_grantor_deed_reference_1_folio": "0000",
  "sales_segment_3_transfer_date_yyyy_mm_dd": "1997.11.26",
  "sales_segment_3_consideration": "0",
  "current_assessment_year_total_assessment": "484800"
 }
}
```

### Critical Area shoreline, Tilghman: --lat 38.7170 --lon -76.3300 --sdat
```json
{
 "summary": {
  "parcel_acct": "2105183472",
  "acres": 0.328,
  "county_zoning": "VM",
  "generalized_zoning": "VERY LOW DENSITY RESIDENTIAL",
  "critical_area": "LDA",
  "septic_tier": "Tier 3B",
  "pfa": true,
  "sewer_cat": "S-1",
  "water_cat": null,
  "flood_zone": "AE",
  "wetland": false,
  "ag_easement": false,
  "soil": "Udorthents, loamy, 0 to 5 percent slopes",
  "septic_rating_dominant": "Very limited"
 },
 "parcel": [
  {
   "JURSCODE": "TALB",
   "ACCTID": "2105183472",
   "CITY": "TILGHMAN",
   "ZIPCODE": "21671",
   "OWNADD1": "PO BOX 198",
   "OWNCITY": "TILGHMAN",
   "OWNSTATE": "MD",
   "LEGAL1": "LOT 41.25X346.5",
   "LEGAL2": "N/S JACKSON PT RD",
   "DR1LIBER": "01130",
   "DR1FOLIO": "0560",
   "MAP": "0044A",
   "PARCEL": "0008",
   "DESCLU": "Commercial",
   "DESCCIUSE": "BOAT Marina",
   "ACRES": 0.328,
   "LANDAREA": 14293.0,
   "TRADATE": "20030306",
   "CONSIDR1": 149500,
   "NFMTTLVL": 167500,
   "SDATDATE": "2026MAY",
   "SDATWEBADR": "https://sdat.dat.maryland.gov/RealProperty/Pages/viewdetails.aspx?County=21&SearchType=ACCT&District=05&AccountNumber=183472"
  }
 ],
 "critical_area_county": [
  {
   "Type": "LDA",
   "CritArea": "Limited Development Area",
   "Location": "Talbot County"
  }
 ],
 "pfa": [
  {
   "JURSCODE": "TALB",
   "CPFA": "IN",
   "RUVI_NAME": "TILGHMAN",
   "ACRES": 572.6590353,
   "CERT_DATE": 883630800000,
   "STATE_ELIGIBLE_STATUS": "YES"
  }
 ],
 "septic_tier_mdp": [
  {
   "County": "Talbot County",
   "TIER": "Tier 3B",
   "TIER_CODE": 3,
   "Adopt_Date": 1465257600000,
   "SRC_DATE": "20181030"
  }
 ],
 "talbot_septic_tier_2016": [
  {
   "SepticTier": "Tier III-B",
   "Plan_Use": "Community Conservation",
   "PlanMD": "ECA",
   "ZONE_06": "VC"
  }
 ],
 "talbot_sewer_service_area": [
  {
   "TYPE": "S-1",
   "Res_No": "Resolution 100",
   "Date": "June 25, 2002"
  }
 ],
 "talbot_zoning": [
  {
   "Zoning2018": "VM",
   "LOCATION": "County",
   "Map_No": "55"
  }
 ],
 "fema_nfhl": [
  {
   "DFIRM_ID": "24041C",
   "FLD_ZONE": "AE",
   "SFHA_TF": "T",
   "STATIC_BFE": 4.0,
   "V_DATUM": "NAVD88"
  }
 ],
 "soils_ssurgo": [
  {
   "mukey": "1712528",
   "muname": "Udorthents, loamy, 0 to 5 percent slopes",
   "compname": "Udorthents",
   "comppct_r": "90",
   "drainagecl": "Well drained",
   "hydricrating": "No",
   "hydgrp": "C",
   "septic_rating": "Very limited"
  },
  {
   "mukey": "1712528",
   "muname": "Udorthents, loamy, 0 to 5 percent slopes",
   "compname": "Urban land",
   "comppct_r": "10",
   "drainagecl": null,
   "hydricrating": "No",
   "hydgrp": "D",
   "septic_rating": "Not rated"
  }
 ],
 "sdat_record": {
  "real_property_search_link": {
   "url": "https://sdat.dat.maryland.gov/RealProperty/Pages/viewdetails.aspx?County=21&SearchType=ACCT&District=05&AccountNumber=183472"
  },
  "record_key_owner_occupancy_code": "N",
  "legal_description_line_1": "LOT 41.25X346.5",
  "legal_description_line_2": "N/S JACKSON PT RD",
  "legal_description_line_3": "TILGHMAN",
  "deed_reference_1_liber": "01130",
  "deed_reference_1_folio": "0560",
  "sales_segment_1_grantor_name": "MITCHELL, JOHN R SR",
  "sales_segment_1_grantor_deed_reference_1_liber": "00594",
  "sales_segment_1_grantor_deed_reference_1_folio": "0631",
  "sales_segment_1_transfer_date_yyyy_mm_dd": "2003.03.06",
  "sales_segment_1_consideration": "149500",
  "sales_segment_2_grantor_name": "MITCHELL, HERBERT L AND JANIE B",
  "sales_segment_2_grantor_deed_reference_1_liber": "00000",
  "sales_segment_2_grantor_deed_reference_1_folio": "0000",
  "sales_segment_2_transfer_date_yyyy_mm_dd": "1984.12.26",
  "sales_segment_2_consideration": "0",
  "sales_segment_3_grantor_deed_reference_1_liber": "00000",
  "sales_segment_3_grantor_deed_reference_1_folio": "0000",
  "sales_segment_3_transfer_date_yyyy_mm_dd": "0000.00.00",
  "sales_segment_3_consideration": "0",
  "current_assessment_year_total_assessment": "159933"
 }
}
```
