# generate a excel report with the data collected from PubChem
import xlsxwriter
import pymongo


def create_worksheets(workbook: xlsxwriter.workbook, sheet_name: str) -> xlsxwriter.worksheet:
    # Create a worksheet
    worksheet = workbook.add_worksheet(sheet_name)
    return worksheet


def set_columns(worksheet: xlsxwriter.worksheet, style: xlsxwriter.styles) -> None:
    index = 0
    columns = ["Compound", "Physical Properties", "Hazards", "First Aids"]
    alphabets = ["A1", "B1", "C1", "D1"]
    # write the column names, corresponding to the MSDS requirements
    for index in range(len(columns)):
        worksheet.write(alphabets[index], columns[index], style)


def getProperty(chemical: dict, prop: str) -> str:
    # get combined properties instead of big broad description
    if chemical[prop] != "":
        result = chemical[prop]
    # if no detailed info available, use big description
    else:
        result = chemical[prop.replace("_combine", "")]
    print("get property")
    print(result)
    print("\n")
    return result


def add_to_report(worksheet: xlsxwriter.worksheet, row_number: int, chemical: dict) -> None:
    name = chemical["Name"]
    property = getProperty(chemical, "description_combine")
    hazards = getProperty(chemical, "GHS_hazard")
    first_aid = getProperty(chemical, "first_aid_combine")
    print("\n")
    print(name)
    print(property)
    print(hazards)
    print(first_aid)
    print("\n")
    worksheet.write("A" + str(row_number), name)
    worksheet.write("B" + str(row_number), property)
    worksheet.write("C" + str(row_number), hazards)
    worksheet.write("D" + str(row_number), first_aid)


def get_chemicals(database: pymongo.MongoClient, identifiers: list = "str") -> list:
    result = []
    myDb = database["my_MSDS"]
    Chemicals = myDb["Chemicals"]
    if str(identifiers) == "all":  # default situation, which will get all information from the current database
        results = list(Chemicals.find({}))  # all records from a collection
    else:
        for identifier in identifiers:
            result.append(Chemicals.find({}, {"identifier": identifier}))
    return result


def generate(report_name: str, address_store: str, chemicals_to_add: list) -> None:
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(address_store)
    # Add a bold format to use to highlight cells.
    cell_format = workbook.add_format({'bold': True})
    cell_format.set_align('left')
    cell_format.set_align('vcenter')
    cell_format.set_text_wrap()
    report = create_worksheets(workbook, report_name)
    set_columns(report, cell_format)  # create columns for the report, could be changed in the function
    index = 0
    for index in range(len(chemicals_to_add)):
        add_to_report(report, index + 2, chemicals_to_add[index])
    workbook.close()


if __name__ == "__main__":
    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
    chemicals = get_chemicals(myClient)
    address = "../OutputReports/MSDS_report.xlsx"
    name = "CHMD16-Lab1-SoilAnalysis"
    generate(name, address, chemicals)

# # Write some numbers, with row/column notation.
# worksheet.write(2, 0, 123)
# worksheet.write(3, 0, 123.456)
#
# # Insert an image.
# worksheet.insert_image('B5', 'logo.png')

# PhysicalProp = ["ordor", "BP", "MP", "solubility", "density", "description"]
# Hazards = ["NFPA_pig", "health_hazards", "fire_hazards", "instability_hazards"]
# First_aids = ["inhalation_first_aid", "skin_first_aid", "eye_first_aid", "ingestion_first_aid", "first_aid"]

# chemical_1 = {'identifier': 'HCL', 'Name': 'Hydrochloric acid', 'MW': '36.46 g/mol',
#               'ordor': 'Pungent, irritating odor', 'BP': '123 °F at 760 mm Hg (USCG, 1999)',
#               'MP': '-174.6 °F (Melting point is -13.7° F for a 39.17% weight/weight solution.) (EPA, 1998)',
#               'solubility': '82.3 g/100 g at 32° F (NTP, 1992)',
#               'density': '1.05 at 59 °F for 10.17% weight/weight solution (EPA, 1998)',
#               'description': 'Hydrochloric acid, solution is a colorless watery liquid with a sharp, irritating odor. Consists of hydrogen chloride, a gas, dissolved in water. Sinks and mixes with water. Produces irritating vapor. (USCG, 1999)',
#               'description_combine': 'ordor: Pungent, irritating odor;\nBoiling Point: 123 °F at 760 mm Hg (USCG, 1999);\nMelting Point: -174.6 °F (Melting point is -13.7° F for a 39.17% weight/weight solution.) (EPA, 1998);\nsolubility: 82.3 g/100 g at 32° F (NTP, 1992);\nDensity: 1.05 at 59 °F for 10.17% weight/weight solution (EPA, 1998);\n',
#               'NFPA_pig': 'https://pubchem.ncbi.nlm.nih.gov/image/nfpa.cgi?code=301',
#               'health_hazards': 'NFPA Health Rating 3 - Materials that, under emergency conditions, can cause serious or permanent injury.',
#               'fire_hazards': 'NFPA Fire Rating 0 - Materials that will not burn under typical fire conditions, including intrinsically noncombustible materials such as concrete, stone, and sand.',
#               'instability_hazards': 'NFPA Instability Rating 1 - Materials that in themselves are normally stable but that can become unstable at elevated temperatures and pressures.',
#               'hazards': 'IDENTIFICATION AND USE: Hydrogen chloride is a colorless gas with pungent, irritating odor. it is used as tuberculocide, disinfectant (bactericide/germicide/purifier, limited, general or broad-spectrum, hospital or medical), sanitizer, virucide, fungicide/fungistat, and microbicide/microbiostat (slime-forming bacteria). It is also used in the manufacture of pharmaceutical hydrochlorides, vinyl chloride from acetylene, alkyl chlorides from olefins, and arsenious chlorides from arsenious oxide. In the chlorination of rubber. In organic reactions involving isomerization, polymerization, and alkylation. For making chlorine where economical. Hydrochloric acid has been identified as being used in hydraulic fracturing as a pH adjuster. HUMAN EXPOSURE AND TOXICITY: Hydrogen chloride will rapidly dissociate and its effects are thought to be a result of pH change (local deposition of H+) rather than effects of hydrogen chloride/hydrochloric acid. Hydrogen chloride is corrosive to the skin and severe effects can be expected from exposure to the eyes. No skin sensitization has been reported. The irritation of hydrogen chloride to mucous is so severe that workers evacuate from the work place shortly after detecting its odor. In humans, no association between hydrogen chloride exposure and tumor incidence was observed. In one of eight asthmatic volunteers exposed to an aerosol of unbuffered hydrochloric acid at pH 2 for 3 min during tidal breathing, airway resistance was increased by 50%. Short term exposures have been reported to induce transitory obstruction in the respiratory tract, which diminishes with repeated exposure, suggesting adaption. Acclimatized workers can work undisturbed with a hydrogen chloride level of 15 mg/cu m (10 ppm). Exposure to hydrochloric acid can produce burns on the skin and mucous membranes, the severity of which is related to the concentration of the solution. Subsequently, ulceration may occur, followed by keloid and retractile scarring. Contact with the eyes may produce reduced vision or blindness. Frequent contact with aqueous solutions of hydrochloric acid may lead to dermatitis. Dental decay, with changes in tooth structure, yellowing, softening and breaking of teeth, and related digestive diseases are frequent after exposures to hydrochloric acid. ANIMAL STUDIES: For repeated dose toxicity, local irritation effects were observed in the groups of 10 ppm and above in a 90-day inhalation study. For genetic toxicity, a negative result has been shown in the Ames test. A positive result, which is considered to be an artifact due to the low pH, has been obtained in a chromosome aberration test using Hamster ovary cells. For carcinogenicity, no pre-neoplastic or neoplastic nasal lesions were observed in a 128-week inhalation study with male rats at 10 ppm hydrogen chloride gas. No evidence of treatment related carcinogenicity was observed either in other animal studies performed by inhalation, oral or dermal administration. Hydrogen chloride is not expected to have developmental toxicity. In addition, no effects on the gonads were observed in a good 90- day inhalation study up to 50 ppm. ECOTOXICITY STUDIES: The hazard of hydrochloric acid for the environment is caused by the proton (pH effect). For this reason the effect of hydrochloric acid on the organisms depends on the buffer capacity of the aquatic ecosystem. Also the variation in acute toxicity for aquatic organisms can be explained for a significant extent by the variation in buffer capacity of the test medium. For example, LC50 values of acute fish toxicity tests varied from 4.92 to 282 mg/L',
#               'hazards_combine': 'NFPA Health Rating 3 - Materials that, under emergency conditions, can cause serious or permanent injury.\nNFPA Fire Rating 0 - Materials that will not burn under typical fire conditions, including intrinsically noncombustible materials such as concrete, stone, and sand.\nNFPA Instability Rating 1 - Materials that in themselves are normally stable but that can become unstable at elevated temperatures and pressures.\n',
#               'GHS_pigment': ['Corrosive', 'Acute Toxic'],
#               'GHS_hazard': 'H314: Causes severe skin burns and eye damage [Danger Skin corrosion/irritation]\nH331: Toxic if inhaled [Danger Acute toxicity, inhalation]',
#               'GHS_precaution': 'P260, P261, P264, P271, P280, P301+P330+P331, P303+P361+P353, P304+P340, P305+P351+P338, P310, P311, P321, P363, P403+P233, P405, and P501\n(The corresponding statement to each P-code can be found at the GHS Classification page.)',
#               'inhalation_first_aid': 'Fresh air, rest. Half-upright position. Artificial respiration may be needed. Refer immediately for medical attention.',
#               'skin_first_aid': 'Wear protective gloves when administering first aid. First rinse with plenty of water for at least 15 minutes, then remove contaminated clothes and rinse again. Refer immediately for medical attention.',
#               'eye_first_aid': 'Rinse with plenty of water for several minutes (remove contact lenses if easily possible). Refer immediately for medical attention.',
#               'ingestion_first_aid': None,
#               'first_aid': 'INHALATION: remove person to fresh air; keep him warm and quiet and get medical attention immediately; start artificial respiration if breathing stops. INGESTION: have person drink water or milk; do NOT induce vomiting. EYES: immediately flush with plenty of water for at least 15 min. and get medical attention; continue flushing for another 15 min. if physician does not arrive promptly. SKIN: immediately flush skin while removing contaminated clothing; get medical attention promptly; use soap and wash area for at least 15 min. (USCG, 1999)',
#               'first_aid_combine': 'inhalation: Fresh air, rest. Half-upright position. Artificial respiration may be needed. Refer immediately for medical attention.\nskin: Wear protective gloves when administering first aid. First rinse with plenty of water for at least 15 minutes, then remove contaminated clothes and rinse again. Refer immediately for medical attention.\neye: Rinse with plenty of water for several minutes (remove contact lenses if easily possible). Refer immediately for medical attention.\n'}
# chemical_2 = {'identifier': 'CaCO3', 'Name': 'Calcium carbonate', 'MW': '100.09 g/mol', 'ordor': 'Odorless',
#               'BP': 'Decomposes (NIOSH, 2016)', 'MP': '1517 to 2442 °F (Decomposes) (NIOSH, 2016)',
#               'solubility': '0.001 % (NIOSH, 2016)', 'density': '2.7 to 2.95 (NIOSH, 2016)',
#               'description': 'Calcium carbonate appears as white, odorless powder or colorless crystals. Practically insoluble in water. Occurs extensive in rocks world-wide. Ground calcium carbonate (CAS: 1317-65-3) results directly from the mining of limestone. The extraction process keeps the carbonate very close to its original state of purity and delivers a finely ground product either in dry or slurry form. Precipitated calcium carbonate (CAS: 471-34-1) is produced industrially by the decomposition of limestone to calcium oxide followed by subsequent recarbonization or as a by-product of the Solvay process (which is used to make sodium carbonate). Precipitated calcium carbonate is purer than ground calcium carbonate and has different (and tailorable) handling properties.',
#               'description_combine': 'ordor: Odorless;\nBoiling Point: Decomposes (NIOSH, 2016);\nMelting Point: 1517 to 2442 °F (Decomposes) (NIOSH, 2016);\nsolubility: 0.001 % (NIOSH, 2016);\nDensity: 2.7 to 2.95 (NIOSH, 2016);\n',
#               'NFPA_pig': None, 'health_hazards': None, 'fire_hazards': None, 'instability_hazards': None,
#               'hazards': None, 'hazards_combine': '', 'GHS_pigment': None,
#               'GHS_hazard': 'Not Classified\nReported as not meeting GHS hazard criteria by 3306 of 3614 companies (only ~ 8.5% companies provided GHS information). For more detailed information, please visit ECHA C&L website',
#               'GHS_precaution': None, 'inhalation_first_aid': 'Fresh air.',
#               'skin_first_aid': 'Rinse skin with plenty of water or shower.',
#               'eye_first_aid': 'Rinse with plenty of water (remove contact lenses if easily possible).',
#               'ingestion_first_aid': 'Rinse mouth.',
#               'first_aid': 'Eye: If this chemical contacts the eyes, immediately wash the eyes with large amounts of water, occasionally lifting the lower and upper lids. Get medical attention immediately. Contact lenses should not be worn when working with this chemical. Skin: If this chemical contacts the skin, wash the contaminated skin with soap and water. Breathing: If a person breathes large amounts of this chemical, move the exposed person to fresh air at once. Other measures are usually unnecessary. (NIOSH, 2016)',
#               'first_aid_combine': 'inhalation: Fresh air.\nskin: Rinse skin with plenty of water or shower.\neye: Rinse with plenty of water (remove contact lenses if easily possible).\ningestion: Rinse mouth.\n'}
# chemical_3 = {'identifier': 'NaCl', 'Name': 'Sodium chloride', 'MW': '58.44 g/mol', 'ordor': None,
#               'BP': '2575 °F at 760 mm Hg (NTP, 1992)', 'MP': '1474 °F (NTP, 1992)',
#               'solubility': 'greater than or equal to 100 mg/mL at 68° F (NTP, 1992)',
#               'density': '2.165 at 77 °F (NTP, 1992)',
#               'description': 'Sodium chloride appears as a white crystalline solid. Commercial grade usually contains some chlorides of calcium and magnesium which absorb moisture and cause caking. (NTP, 1992)',
#               'description_combine': 'Boiling Point: 2575 °F at 760 mm Hg (NTP, 1992);\nMelting Point: 1474 °F (NTP, 1992);\nsolubility: greater than or equal to 100 mg/mL at 68° F (NTP, 1992);\nDensity: 2.165 at 77 °F (NTP, 1992);\n',
#               'NFPA_pig': None, 'health_hazards': None, 'fire_hazards': None, 'instability_hazards': None,
#               'hazards': 'The rare inadvertent intravascular administration or rapid intravascular absorption of hypertonic sodium chloride can cause a shift of tissue fluids into the vascular bed, resulting in hypervolemia, electrolyte disturbances, circulatory failure, pulmonary embolism, or augmented hypertension. ( toxnet)',
#               'hazards_combine': '', 'GHS_pigment': ['Irritant'],
#               'GHS_hazard': 'Aggregated GHS information provided by 2341 companies from 13 notifications to the ECHA C&L Inventory.\nReported as not meeting GHS hazard criteria by 1699 of 2341 companies. For more detailed information, please visit ECHA C&L website\nOf the 9 notification(s) provided by 642 of 2341 companies with hazard statement code(s):\nH319 (100%): Causes serious eye irritation [Warning Serious eye damage/eye irritation]\nInformation may vary between notifications depending on impurities, additives, and other factors. The percentage value in parenthesis indicates the notified classification ratio from companies that provide hazard codes. Only hazard codes with percentage values above 10% are shown.',
#               'GHS_precaution': 'P264, P280, P305+P351+P338, and P337+P313\n(The corresponding statement to each P-code can be found at the GHS Classification page.)',
#               'inhalation_first_aid': None, 'skin_first_aid': None, 'eye_first_aid': None,
#               'ingestion_first_aid': None,
#               'first_aid': "EYES: First check the victim for contact lenses and remove if present. Flush victim's eyes with water or normal saline solution for 20 to 30 minutes while simultaneously calling a hospital or poison control center. Do not put any ointments, oils, or medication in the victim's eyes without specific instructions from a physician. IMMEDIATELY transport the victim after flushing eyes to a hospital even if no symptoms (such as redness or irritation) develop. SKIN: IMMEDIATELY flood affected skin with water while removing and isolating all contaminated clothing. Gently wash all affected skin areas thoroughly with soap and water. If symptoms such as redness or irritation develop, IMMEDIATELY call a physician and be prepared to transport the victim to a hospital for treatment. INHALATION: IMMEDIATELY leave the contaminated area; take deep breaths of fresh air. If symptoms (such as wheezing, coughing, shortness of breath, or burning in the mouth, throat, or chest) develop, call a physician and be prepared to transport the victim to a hospital. Provide proper respiratory protection to rescuers entering an unknown atmosphere. Whenever possible, Self-Contained Breathing Apparatus (SCBA) should be used; if not available, use a level of protection greater than or equal to that advised under Protective Clothing. INGESTION: DO NOT INDUCE VOMITING. If the victim is conscious and not convulsing, give 1 or 2 glasses of water to dilute the chemical and IMMEDIATELY call a hospital or poison control center. Be prepared to transport the victim to a hospital if advised by a physician. If the victim is convulsing or unconscious, do not give anything by mouth, ensure that the victim's airway is open and lay the victim on his/her side with the head lower than the body. DO NOT INDUCE VOMITING. IMMEDIATELY transport the victim to a hospital. (NTP, 1992)",
#               'first_aid_combine': ''}
# chemicals = [chemical_1, chemical_2, chemical_3]
