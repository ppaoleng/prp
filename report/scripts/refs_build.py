"""Build refs_master.json: verified references (from agent search results) + retained original references.
DOI policy: only 'seen_in_source' or 'derived_mdpi_pattern' DOIs are printed; recalled DOIs are kept only in the register."""
import json, glob, os, re
RAW = "/tmp/claude-0/-home-user-prp/efc35c36-8d0a-5da3-8409-dee1d83cf835/scratchpad/refs_raw"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "refs_master.json")
pool = {}
for f in sorted(glob.glob(os.path.join(RAW, "B[1-6].json"))):
    for x in json.load(open(f)): pool[x["id"]] = x

KEYS = {  # key -> pool id
 "zhang2022": "B1-01", "barbhuiya2024": "B1-02", "senadheera2023": "B1-03", "murali2024": "B1-04", "danish2021": "B1-05", "maljaee2021": "B1-06",
 "akinyemi2020": "B1-07", "liu2022": "B1-08", "chen2022": "B1-09", "wang2020": "B1-10", "wang2021acs": "B1-11", "gupta2018a": "B1-12",
 "gupta2018b": "B1-13", "gupta2019": "B1-14", "suarez2020": "B1-15", "ling2023": "B1-16", "woolf2010": "B1-17",
 "legan2025": "B2-03", "hylton2024": "B2-04", "sirico2021": "B2-05", "akhtar2018": "B2-06", "gupta2018c": "B2-08", "gupta2022": "B2-09",
 "sikora2022": "B2-10", "abbas2025": "B2-11", "sacdalan2023": "B2-12", "chin2025": "B2-13", "gimbun2025": "B2-14",
 "verian2018": "B3-01", "poon2006": "B3-02", "soutsos2011": "B3-03", "tam2018": "B3-04", "silva2014": "B3-05", "nedeljkovic2021": "B3-06",
 "peiris2025": "B3-07", "namarak2018": "B3-08", "wangx2019": "B3-09", "rodriguez2017": "B3-10", "sambucci2021": "B3-11", "ganjian2015": "B3-12",
 "contreras2022": "B3-13", "djamaluddin2020": "B3-14",
 "astme303": "B4-01", "en1338": "B4-02", "en13036": "B4-03", "bs7976": "B4-04", "uksrg2016": "B4-06", "gierasimiuk2021": "B4-09", "yuan2025": "B4-10",
 "persson2001": "B4-13", "persson2005": "B4-14", "chang2001": "B4-16",
 "pizon2026": "B5-01", "soares2025": "B5-02", "andrew2019": "B5-03", "habert2020": "B5-04", "scrivener2018": "B5-05", "damineli2010": "B5-06",
 "knoeri2013": "B5-07", "wangd2026": "B5-08", "ambaye2026": "B5-09", "agrela2024": "B5-10", "wernet2016": "B5-12", "huijbregts2017": "B5-13",
 "khongprom2017": "B5-14", "ltleds2022": "B5-15", "ndc2025": "B5-16", "iso14040": "B5-17", "iso14044": "B5-18",
 "chenx2013": "B6-01", "kumar2003": "B6-02", "lian2011": "B6-03", "scrivener2004": "B6-04", "xiao2013": "B6-05", "lothenbach2011": "B6-06", "xiao2012": "B6-07",
}
# manual author/title overrides for records whose agent fields are not in citation form
OVR = {
 "gierasimiuk2021": dict(authors="Gierasimiuk, P., Wasilewska, M. and Gardziejczyk, W."),
 "yuan2025": dict(authors="Yuan, J., Feng, Z. and Cui, P."),
 "persson2001": dict(authors="Persson, B.N.J.", container="The Journal of Chemical Physics", volume="115", issue="8", pages="3840-3861", note="journal/volume/pages added from author knowledge; DOI seen in source; re-check"),
 "persson2005": dict(authors="Persson, B.N.J., Albohr, O., Tartaglino, U., Volokitin, A.I. and Tosatti, E."),
 "chang2001": dict(authors="Chang, W.-R., Grönqvist, R., Leclercq, S. et al."),
 "pizon2026": dict(authors="Pizoń, J., Poranek, N. and Horňáková, M.", note="author list as printed on the PDF supplied by the user"),
 "habert2020": dict(authors="Habert, G., Miller, S.A., John, V.M. et al."),
 "astme303": dict(authors="ASTM International", title="ASTM E303-22. Standard test method for measuring surface frictional properties using the British Pendulum Tester", container="West Conshohocken: ASTM International", year=2022),
 "en1338": dict(authors="European Committee for Standardization (CEN)", title="EN 1338:2003. Concrete paving blocks - Requirements and test methods", container="Brussels: CEN (adopted as BS EN 1338:2003)", year=2003),
 "en13036": dict(authors="European Committee for Standardization (CEN)", title="EN 13036-4:2011. Road and airfield surface characteristics - Test methods - Part 4: Method for measurement of slip/skid resistance of a surface: the pendulum test", container="Brussels: CEN", year=2011),
 "bs7976": dict(authors="British Standards Institution (BSI)", title="BS 7976-2:2002+A1:2013. Pendulum testers - Method of operation (withdrawn 2022)", container="London: BSI", year=2013),
 "uksrg2016": dict(authors="UK Slip Resistance Group (UKSRG)", title="The assessment of floor slip resistance: the UK Slip Resistance Group guidelines, Issue 5.0", container="UKSRG", year=2016, note="bands quoted from secondary sources; verify against the Guidelines"),
 "ltleds2022": dict(authors="Royal Thai Government", title="Thailand's long-term low greenhouse gas emission development strategy (revised version)", container="Submission to the UNFCCC, 8 November 2022", year=2022),
 "ndc2025": dict(authors="Kingdom of Thailand", title="Thailand's second updated nationally determined contribution (NDC 3.0)", container="Submission to the UNFCCC, 4 November 2025", year=2025),
 "iso14040": dict(authors="International Organization for Standardization", title="ISO 14040:2006. Environmental management - Life cycle assessment - Principles and framework", container="Geneva: ISO", year=2006),
 "iso14044": dict(authors="International Organization for Standardization", title="ISO 14044:2006. Environmental management - Life cycle assessment - Requirements and guidelines", container="Geneva: ISO", year=2006),
 "murali2024": dict(authors="Murali, G. and Wong, L.S."),
 "sirico2021": dict(authors="Sirico, A. et al."),
 "xiao2013": dict(authors="Xiao, J. et al."),
 "lian2011": dict(authors="Lian, C., Zhuge, Y. and Beecham, S.", container="Construction and Building Materials"),
 "maljaee2021": dict(authors="Maljaee, H., Madadi, R., Paiva, H. et al."),
 "ling2023": dict(authors="Ling, Y., Wu, X., Tan, K. et al."),
 "legan2025": dict(authors="Legan, M., Štukovnik, P., Zupan, K. and Žgajnar Gotvajn, A."),
}
VERIF = {  # verification level shown in the register
 "V1": "existence confirmed in search results; DOI seen/derived", "V2": "existence confirmed in search results; DOI not seen", "V3": "weak/indirect evidence only",
 "O": "retained from the original draft; not re-verified here", "S": "standard / institutional document; DOI not applicable",
}

def fmt_authors(a, complete):
    if isinstance(a, list):
        a = [str(x) for x in a]
        if len(a) > 3 or not complete: return ", ".join(a[:3]) + (" et al." if len(a) > 3 or not complete else "")
        return " and ".join([", ".join(a[:-1]), a[-1]]) if len(a) > 1 else a[0]
    return a

refs = {}
for key, pid in KEYS.items():
    x = pool[pid]; o = OVR.get(key, {})
    d = dict(key=key, src=pid, authors=o.get("authors") or fmt_authors(x.get("authors"), x.get("authors_complete", True)),
             year=o.get("year", x.get("year")), title=o.get("title", x.get("title")), container=o.get("container", x.get("container")),
             volume=o.get("volume", x.get("volume")), issue=o.get("issue", x.get("issue")), pages=o.get("pages", x.get("pages_or_article_no")),
             doi=x.get("doi"), doi_status=x.get("doi_status"), doi_recalled=x.get("doi_recalled_unverified"), verified=x.get("verified"),
             key_finding=x.get("key_finding"), key_quant=x.get("key_quant"), quote=x.get("quote"), evidence=x.get("evidence_urls"), tags=x.get("tags"), note=o.get("note") or x.get("notes"), lang="en")
    if d["pages"] and "article ID in URL" in str(d["pages"]): d["pages"] = "CET23106069"
    if key in ("persson2001",): d["doi"] = "10.1063/1.1388626"; d["doi_status"] = "seen_in_source"
    if key in ("astme303","en1338","en13036","bs7976","uksrg2016","ltleds2022","ndc2025","iso14040","iso14044"): d["level"] = "S"
    else: d["level"] = "V1" if d["doi"] else "V2"
    if key in ("tam2018", "silva2014", "soutsos2011", "gupta2018a", "gupta2018b", "gupta2019", "gupta2018c", "gupta2022", "murali2024"): d["level"] = "V3" if not d["doi"] else d["level"]
    refs[key] = d

# ---- retained original references (as printed in the draft; formatting normalised only) ----
ORIG = [
 dict(key="nxpo2021", authors="Office of National Higher Education Science Research and Innovation Policy Council (NXPO)", year=2021, title="Thailand announces targets for carbon neutrality by 2050 and net-zero GHG emissions by 2065 (in Thai)", container="NXPO web article, 1 November 2021. Available from: https://www.nxpo.or.th/th/9651/", lang="th", orig="[1]"),
 dict(key="tripathi2019", authors="Tripathi, N., Hills, C.D., Singh, R.S. and Atkinson, C.J.", year=2019, title="Biomass waste utilisation in low-carbon products: harnessing a major potential resource", container="npj Climate and Atmospheric Science", orig="[2]"),
 dict(key="windeatt2014", authors="Windeatt, J.H., Ross, A.B., Williams, P.T. et al.", year=2014, title="Characteristics of biochars from crop residues: potential for carbon sequestration and soil amendment", container="Journal of Environmental Management", volume="146", pages="189-197", orig="[4]"),
 dict(key="wangf2021", authors="Wang, F., Harindintwali, J.D., Yuan, Z. et al.", year=2021, title="Technologies and perspectives for achieving carbon neutrality", container="The Innovation", orig="[5]"),
 dict(key="he2022", authors="He, M., Xu, Z., Hou, D. et al.", year=2022, title="Waste-derived biochar for water pollution control and sustainable development", container="Nature Reviews Earth & Environment", volume="3", pages="444-460", orig="[9]"),
 dict(key="sajjadi2019", authors="Sajjadi, B., Chen, W.-Y. and Egiebor, N.O.", year=2019, title="A comprehensive review on physical activation of biochar for energy and environmental applications", container="Reviews in Chemical Engineering", volume="35", pages="735-776", orig="[12]"),
 dict(key="lehmann2015", authors="Lehmann, J. and Joseph, S.", year=2015, title="Biochar for environmental management: an introduction. In: Biochar for environmental management", container="London: Routledge", pages="1-13", orig="[18]"),
 dict(key="czajczynska2017", authors="Czajczyńska, D., Anguilano, L., Ghazal, H. et al.", year=2017, title="Potential of pyrolysis processes in the waste management sector", container="Thermal Science and Engineering Progress", volume="3", pages="171-197", orig="[21]", note="author list completed from author knowledge; re-check"),
 dict(key="cherdkun2019", authors="Cherdkun, N.", year=2019, title="Preparation of activated carbon from biochar and subbituminous coal (thesis)", container="Department of Chemical Technology, Chulalongkorn University", orig="[23]"),
 dict(key="biederman2013", authors="Biederman, L.A. and Harpole, W.S.", year=2013, title="Biochar and its effects on plant productivity and nutrient cycling: a meta-analysis", container="GCB Bioenergy", volume="5", issue="2", pages="202-214", orig="[24]"),
 dict(key="ahmad2014", authors="Ahmad, M., Rajapaksha, A.U., Lim, J.E. et al.", year=2014, title="Biochar as a sorbent for contaminant management in soil and water: a review", container="Chemosphere", volume="99", pages="19-33", orig="[26]"),
 dict(key="sangmanee2025", authors="Sangmanee, K.", year=2025, title="Effects of durian shell biochar and green manure on soil properties, growth and yield of green oak lettuce in acid sulfate soil", container="Naresuan Agriculture Journal", volume="22", issue="1", orig="[27]"),
 dict(key="buddee2024", authors="Buddee, S., Rotduang, P. and Rattanaburi, P.", year=2024, title="The adsorption of malachite green dye using biochar from bagasse", container="Wichcha Journal", volume="43", issue="2", pages="50-65", orig="[28]"),
 dict(key="shao2026", authors="Shao, Z. and Sakai, Y.", year=2026, title="Low-carbon construction material from waste concrete powder through compaction and carbonation: effect of powder size", container="Construction and Building Materials", volume="514", pages="145555", orig="[54]"),
 dict(key="wangx2026", authors="Wang, X. et al.", year=2026, title="From waste to carbon benefits - a dynamic spatiotemporal model for assessing carbon reduction potential in urban concrete recycling systems", container="Resources, Conservation & Recycling", orig="[55]"),
 dict(key="sept2018", authors="Small Element Pavement Technology (SEPT)", year=2018, title="The international body for the development of concrete block pavement technology", container="Available from: http://www.sept.org/", orig="[59]"),
 dict(key="saetang2024", authors="Saetang, C., Wannasri, N. and Thurawat, P.", year=2024, title="Design and development of lignite fly ash concrete paving block (in Thai)", container="Journal of Fine Arts Research and Applied Arts", volume="11", issue="1", pages="144-158", lang="th", orig="[60]"),
 dict(key="paoleng2025ncce", authors="Paoleng, P., Meepon, I. and Mahannopkul, K.", year=2025, title="Mechanical and physical properties of concrete paving blocks using vinasse fly ash and rice husk ash as cement replacement (in Thai). In: Proceedings of the 30th National Convention on Civil Engineering (NCCE30), Nakhon Pathom", container="NCCE30", lang="th", orig="[61]"),
 dict(key="pluemruetai2011", authors="Pluemruetai, S. and Uengkul, Y.", year=2011, title="Development of concrete block using water hyacinth (in Thai). In: Silpakorn Graduate Studies Conference 2, Nakhon Pathom", container="Silpakorn University", pages="149-166", lang="th", orig="[62]"),
 dict(key="chantaramanee2024", authors="Chantaramanee, S. et al.", year=2024, title="Physical properties, compressive strength and microstructure of interlocking concrete paving block containing bamboo ash", container="The Journal of Industrial Technology", volume="20", issue="1", pages="46-61", orig="[63]"),
 dict(key="khamput2024", authors="Khamput, P. et al.", year=2024, title="Development of interlocking concrete paving block from plastic bottle waste incorporated with stone dust (in Thai)", container="KMUTNB Academic Journal", volume="34", issue="3", lang="th", orig="[64]", note="first author transliterated from the original Thai entry; re-check"),
 dict(key="kaewkamthong2025", authors="Kaewkamthong, P.", year=2025, title="Utilization of plastic waste and demolished concrete as ingredients in sidewalk paving blocks (in Thai)", container="Industrial Technology Journal, Surindra Rajabhat University", volume="10", issue="1", pages="12-20", lang="th", orig="[65]", note="author transliterated from the original Thai entry; re-check"),
 dict(key="klathae2020", authors="Klathae, T. et al.", year=2020, title="Utilization of parawood ash in concrete paving blocks (in Thai)", container="Rajamangala University of Technology Srivijaya Research Journal", volume="12", issue="1", pages="36-48", lang="th", orig="[66]"),
 dict(key="nuansawan2008", authors="Nuansawan, N.", year=2008, title="Utilization of label-type waste in making interlocking concrete paving blocks using limestone powder-cement as binder (in Thai)", container="Master thesis, Chulalongkorn University, Bangkok", lang="th", orig="[67]", note="author transliterated from the original Thai entry; re-check"),
 dict(key="suwiro2018", authors="Suwiro, K. et al.", year=2018, title="Utilization of volcanic rock waste in paving block products (in Thai)", container="Journal of Community Development and Life Quality", volume="3", issue="3", pages="361-368", lang="th", orig="[68]", note="author transliterated from the original Thai entry; re-check"),
 dict(key="tis827", authors="Thai Industrial Standards Institute (TISI)", year=2022, title="TIS 827-2565. Interlocking concrete paving blocks (in Thai)", container="Bangkok: TISI", lang="th", orig="[69]", level="S", note="year derived from the B.E. 2565 designation; draft listed 1988"),
 dict(key="tis2035", authors="Thai Industrial Standards Institute (TISI)", year=2022, title="TIS 2035-2565. Interlocking concrete paving blocks for heavy duty (in Thai)", container="Bangkok: TISI", lang="th", orig="[70]", level="S", note="year derived from the B.E. 2565 designation; draft listed 2000"),
 dict(key="jiepa2017", authors="Japan Interlocking Pavement Engineering Association (JIEPA)", year=2017, title="Japan interlocking block pavement design and construction manual", container="Tokyo: JIEPA", orig="[71]", level="S"),
 dict(key="astmc936", authors="ASTM International", year=2021, title="ASTM C936/C936M-21b. Standard specification for solid concrete interlocking paving units", container="West Conshohocken: ASTM International", orig="[73]", level="S", note="draft listed 2016; revision suffix 21b implies 2021"),
 dict(key="is15658", authors="Bureau of Indian Standards", year=2006, title="IS 15658:2006. Precast concrete blocks for paving - Specification", container="New Delhi: BIS", orig="[74]", level="S"),
 dict(key="paoleng2025", authors="Paoleng, P., Kongsomsaksakul, S., Meepon, I. and Maneekaew, S.", year=2025, title="Application of biochar as partial cement replacement with polypropylene plastic waste for sustainable concrete paving blocks", container="Cuestiones de Fisioterapia", volume="54", issue="5", pages="4978-4991", doi="10.48047/vmsxaq82", doi_status="from_author_cv", orig="CV", level="O", note="DOI printed in the researcher's own publication list in the draft"),
 dict(key="en1992", authors="European Committee for Standardization (CEN)", year=2004, title="EN 1992-1-1:2004. Eurocode 2: Design of concrete structures - Part 1-1: General rules and rules for buildings", container="Brussels: CEN", level="S", note="well-known standard (Cl. 3.1.2); not re-verified in this session"),
 dict(key="un2015", authors="United Nations General Assembly", year=2015, title="Transforming our world: the 2030 Agenda for Sustainable Development, Resolution A/RES/70/1", container="New York: United Nations", level="S", note="well-known document; not re-verified in this session"),
]
for o in ORIG:
    o.setdefault("level", "O"); o.setdefault("doi", None); o.setdefault("doi_status", "not_seen" if not o.get("doi") else o.get("doi_status")); refs[o["key"]] = o

dropped = {  # original reference -> reason
 "[3]": "Yang et al. 2019 (phase-change energy materials): unrelated to the biochar CO2 claim it supported",
 "[6]/[10]": "duplicates of Akinyemi (2020) / Maljaee (2021) already in the verified pool",
 "[7]/[8]": "duplicate entries of Zhang et al. (2022)", "[11]": "Chen et al. 2022 retained once (verified record)", "[13]": "WBCSD 2018 report: could not be verified",
 "[14]": "Palomo & Blanco-Varela: title/journal not verifiable", "[15]/[16]": "IEA / GCCA reports: year/edition not verifiable", "[17]": "Scrivener & John (2010): author/title could not be verified",
 "[19]/[20]": "Maschio 1992 (too old) / Biswal 2013 (paper-cup waste): not relevant", "[22]": "magazine web page; replaced by Zhang et al. (2022) for the process scheme",
 "[25]": "Woolf et al. 2010 retained as verified record", "[29]-[45]": "malformed author strings; replaced by verified C&D-waste / RCA literature (Verian, Tam, Silva, Contreras Llanes, Peiris, ...)",
 "[46]": "Verian et al. retained as verified record", "[47]": "Krishnan & Bishnoi (dolomite hydration): not relevant to RCA claim", "[48]": "Shah et al. (crumb-rubber cement composite): not relevant",
 "[49]": "McGovern et al. (asphalt oxidative ageing): not relevant", "[50]": "Joseph et al. (MSWI bottom-ash concrete): did not support the claim (RCA QC flow / SDG)", "[51]/[52]/[53]": "Ling, Barbhuiya, Peiris retained as verified records",
 "[56]": "Zhang et al. 2021 (boron nitride / silicone rubber for lithium batteries): unrelated to SDG claim", "[57]": "He et al. 2021 (organic Rankine cycle): unrelated to the safety-in-use claim",
 "[58]": "Namarak retained as verified record", "[72]": "EN 1338:2003 retained as verified record",
}
json.dump(dict(refs=refs, dropped=dropped, verif=VERIF), open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(refs), "references in master;", sum(1 for r in refs.values() if r.get("doi")), "with printable DOI")
