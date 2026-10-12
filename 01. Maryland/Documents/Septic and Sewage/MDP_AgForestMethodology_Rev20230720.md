---
county: "01. Maryland"
category: "other"
title: "MDP Agriculture and Forest Areas Methodology (Tier IV)"
source_url: "https://planning.maryland.gov/Documents/OurWork/RRP/septicsbill/MDP_AgForestMethodology_Rev20230720.pdf"
effective: "2023-07-20"
retrieved: "2026-10-11"
original: "01. Maryland/Originals/Septic and Sewage/MDP_AgForestMethodology_Rev20230720.pdf"
pages: "3"
needs_ocr: "no"
---

# MDP Agriculture and Forest Areas Methodology (Tier IV)

<!-- page 1 -->
**Dominated by Agricultural and Forest Land** 

# **Maryland Department of Planning GIS Methodology** 

The Sustainable Growth and Agricultural Preservation Act of 2012 requires jurisdictions to map “areas dominated by agricultural and forest lands” consistent with Growth Tier 4. Jurisdictions must consider these areas when adopting Growth Tier maps. 

To support implementation guidance, MDP provides a GIS shape file, along with the following document, to detail the statewide coverage of “Dominated by Agricultural or Forest Land.”  This data layer consists of areas in the state that are 100 or more acres of contiguous agricultural and forest land.  MDP encourages jurisdictions to use this spatial data layer; in conjunction with attributed parcel polygons available from MDP’s GIS download site and the MDiMap 6-inch Imagery; to determine areas “Dominated by Agricultural or Forest Land.”  While not the only possible approach for delineating these areas, MDP’s “Dominated by Ag and Forest Land” information provides specific guidance on this provision. 

Section 2.2.2 Growth Tier Criteria, of the Implementation Guidance for the Sustainable Growth and Agricultural Preservation Act of 2012 contains the following information to define “Dominated by Agricultural or Forest Land:” 

# **_<u>What is “Dominated by Agricultural or Forest Land”?</u>_** 

_In discerning lands dominated by Ag and Forest, it should be noted that the lands for consideration should only be those lands which are not designated within Tiers 1 or 2.  From the remaining land (not appropriately designated as Tiers 1 or 2), there are a number of reasonable approaches to delineating areas that should be included in Tier IV because they are dominated by agricultural and forest lands or other natural areas. MDP recommends the use of its 2010 Land Use/Land Cover layer and other spatial criteria to identify areas to consider for inclusion in Tier IV, followed by explicit evaluation of the resource values on the land so identified, as further explained below._ 

# **_Size and Location Criteria_** 

_For this approach, MDP recommends that areas initially be mapped to include:_ 

- _Agricultural and Forest lands that adjoin or are contiguous to other Tier IV areas.  Other Tier IV areas include zoning districts planned and zoned for preservation/conservation, PPAs, and Rural Legacy Areas._ 

- _Isolated areas 100 acres or larger of contiguous combined agricultural, forest, and other natural land covers._ 

- _Isolated areas of contiguous combined agricultural, forest, and other natural land covers that are smaller than 100 acres in size that have stand-alone resource value identified by the State, local government or the private sector (often individual landowners). Such areas will generally be surrounded by non-agricultural, non-forest land uses such as residential subdivisions or other Tier I, II, or III lands._

<!-- page 2 -->
# **<u>MDP GIS Methodology</u>** 

MDP recommends the following GIS-based approach to construct an initial database of areas dominated by agricultural or forest land as an initial base in identifying these areas; based upon the above size and location criteria.  Further refinement with locally available data can be incorporated. 

1. Download the appropriate MDP 2010 Land Use/Land Cover dataset from the following link: 

   - <u>https://planning.maryland.gov/Pages/OurProducts/DownloadFiles.aspx</u> 

2. Query the following LU_CODES from the GIS file which constitute agricultural, forest and wetlands: 

|LU_CODE|Classification Description|
|---|---|
|21|Cropland - Field crops and forage crops.|
|22|Pasture - Land used forpasture,bothpermanent and rotated; grass.|
|23|Orchards/vineyards/horticulture - Areas of intensively managed commercial bush and tree crops,<br>including areas used for fruit production, vineyards, sod and seed farms, nurseries, and green<br>houses.|
|24|Feeding operations - Cattle feed lots, holding lots for animals, hog feeding lots, poultry houses,<br>and commercial fishingareas(includingoyster beds).|
|241|Feedingoperations - Cattle feed lots,holdinglots for animals,hogfeedinglots, poultryhouses.|
|242|Agricultural building breeding and training facilities, storage facilities, and built-up areas<br>associated with a farmstead,small farmponds,and commercial fishingareas.|
|25|Row andgarden crops - Intensivelymanaged truck and vegetable farms and associated areas.|
|41|Deciduous forest - Forested areas in which the trees characteristically lose their leaves at the end<br>of the growing season.  Included are such species as oak, hickory, aspen, sycamore, birch, yellow<br>poplar,elm,maple,and cypress.|
|42|Evergreen forest - Forested areas in which the trees are characterized by persistent foliage<br>throughout the year.  Included are such species as white pine, pond pine, hemlock, southern<br>white cedar,and redpine.|
|43|Mixed forest - Forested areas in which neither deciduous nor evergreen species dominate, but in<br>which there is a combination of both types.|
|44|Brush - Areas which do not produce timber or other wood products but may have cut-over timber<br>stands, abandoned agriculture fields, or pasture.  These areas are characterized by vegetation<br>types such as sumac,vines,rose,brambles,and tree seedlings.|
|60|Forested or non-forested wetlands, including tidal flats, tidal and non-tidal marshes, and upland<br>swamps and wet areas.|





<!-- Start of picture text -->
Dissolve<br>Aggregates features based on specified<br>attnbutes.<br>INPUT<br>output<br><!-- End of picture text -->

3. Use the Dissolve tool in the “Generalization” toolset to aggregate areas dominated individually by agricultural, forest and wetlands to contiguous groups of all three land types. 4. Calculate Acreage of the resulting polygons and remove all that are less than 100 Acres. 

For interim updates between Land Use Land Cover releases, complete steps 5-9 on the next page, which help account for additional development since 2010.

<!-- page 3 -->
# **<u><mark>Addi�onal Steps for Interim Updates between MDP Statewide Land Use Data Releases</mark></u>** 

_<mark>The following additonal steps help remove from “areas dominated by agriculture and forest” new</mark> i_ _<mark>development since the inital coverage was created in 2012. For interim updates, new development</mark> i_ _<mark>includes parcels less than fve acres that contain a resident</mark> i_ _<mark>al or commercial building. Development on</mark> i_ _<mark>parcels greater than f</mark> i_ _<mark>ve acres will be addressed through MDP’s next statewide Land Use Map Update, which will determine the extent of development on larger parcels.</mark>_ 

<mark>Before comple�ng these steps, download latest available statewide “Parcel Points and Polygons” and “Statewide CAMA” data from: https://planning.maryland.gov/Pages/OurProducts/DownloadFiles.aspx. The vintages used to generate the currently published interim update are the December 2022 Statewide Geodatabase and the January 2021 CAMA Building File.</mark> 

<mark>5) Calculate the parcel acreage, which will be the parcel polygon’s GIS acres or the tax assessed acres if within 25 percent of the GIS acres. Using the GIS acres where larger discrepancies exist between the tax assessed acreage and the GIS acres helps account for areas where the tax assessed acreage does not ref</mark> l <mark>ect the parcel boundary:</mark> 

- <mark>Open the statewide parcel polygon f</mark> i <mark>le (“parcel_polygons”). Run the Calculate Field tool on the POLYACRES f</mark> i <mark>eld using the expression [!SHAPE.AREA@ACRES!] to generate the parcel polygon acres in NAD83 meters.</mark> 

- <mark>Add a SDATPOLYACDIFF feld, which will be used to determine the percent dif</mark> i <mark>erence between</mark> f <mark>the GIS acres (POLYACRES) and tax assessed acreage. Populate the feld using the following</mark> i <mark>expression: "abs(!ACRES!-!POLYACRES!)/!POLYACRES!".</mark> 

- <mark>Add a REVACRES f</mark> i <mark>eld, which will be used to calculate the acreage of each parcel for analysis purposes. Ini�ally, populate this f</mark> i <mark>eld with the contents of the POLYACRES feld.</mark> i 

- <mark>Adjust the REVACRES f</mark> i <mark>eld to include the ACRES (tax assessed acreage) where ACRES > 0 AND SDATPOLYACPDIFF <= .25.</mark> 

<mark>6) Iden�fy parcel accounts containing residen�al or commercial buildings. Open the January 2021 Statewide CAMA f</mark> i <mark>le. Extract residen�al and commercial buildings, excluding boat slips, parking, etc using the following query: (NOT BL_BLDTYPE IN ('0012','C137', 'C314', 'C304')) AND (NOT BL_BLDSTYL IN ('C137', 'C314', 'C304'))</mark> 

<mark>7) Iden�fy parcel polygons less than f</mark> i <mark>ve acres that contain a residen�al or commercial building.  Use the Add Join tool to join the extracted CAMA records from Step 6 to the statewide parcel polygon f</mark> i <mark>le from Step 5 by the ACCTID feld. Export matching records (i.e. parcels containing buildings), and extract from</mark> i <mark>the result records with a residen�al or commercial building where REVACRES < 5.</mark> 

<mark>8) Use the Erase tool to remove parcels less than f</mark> i <mark>ve acres that contain a residen�al or commercial building from either the Step 4 output or the Step 9 output from a previous interim update. Since the currently published interim update is the frst one since 2012, it uses the Step 4 output. Future updates</mark> i <mark>will use the Step 9 output.</mark> 

<mark>9) Repeat Steps 3 and 4 on the Step 8 output to remove any remaining areas less than 100 acres.</mark> 

<mark>For more informa�on please contact Deborah Sward at deborah.sward@maryland.gov.</mark>
