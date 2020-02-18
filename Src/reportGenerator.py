# generate a excel report with the data collected from PubChem
import xlsxwriter


def create_worksheets(workbook, sheet_name):
    # Create a worksheet
    worksheet = workbook.add_worksheet(sheet_name)
    return worksheet


def set_columns(worksheet, style):
    index = 0
    columns = ["Compound", "Physical Properties", "Hazards", "First Aids"]
    alphabets = ["A", "B", "C", "D"]
    # write the column names, corresponding to the MSDS requirements
    for index in range(len(columns)):
        worksheet.write(alphabets[index], columns[index], style)


def getProperty(chemical, prop):
    # get combined properties instead of big broad description
    if chemical[prop] != "":
        result = chemical[prop]
    # if no detailed info available, use big description
    else:
        result = chemical[prop.replace("_combine", "")]
    return result


def add_to_report(worksheet, row_number, chemical):
    name = chemical["Name"]
    property = getProperty(chemical, "description_combine")
    hazards = getProperty(chemical, "hazards_combine")
    first_aid = getProperty(chemical, "first_aid_combine")
    worksheet.write("A" + row_number, name)
    worksheet.write("B" + row_number, property)
    worksheet.write("C" + row_number, hazards)
    worksheet.write("D" + row_number, first_aid)


def generate(report_name, address_store, chemicals_to_add):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(address_store)
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    report = create_worksheets(workbook, report_name)
    set_columns(report, bold)  # create columns for the report, could be changed in the function
    index = 0
    for index in range(len(chemicals_to_add)):
        add_to_report(report, index + 1, chemicals_to_add[index])
    workbook.close()


if __name__ == "__main__":
    address = '../OutputReports/MSDS_report.xlsx'
    name = "CHMD16-Lab1-SoilAnalysis"
    chemical_1 = {'identifier': 'NaCl', 'Name': 'Sodium chlorid', 'MW': '58.44 g/mo', 'ordor': None, 'BP': '2575 °F at 760 mm Hg (NTP, 1992)', 'MP': '1474 °F (NTP, 1992)', 'solubility': 'greater than or equal to 100 mg/mL at 68° F (NTP, 1992)', 'density': '2.165 at 77 °F (NTP, 1992)', 'description': 'Sodium chloride appears as a white crystalline solid. Commercial grade usually contains some chlorides of calcium and magnesium which absorb moisture and cause caking. (NTP, 1992)', 'description_combine': 'Boiling Point: 2575 °F at 760 mm Hg (NTP, 1992);Melting Point: 1474 °F (NTP, 1992);solubility: greater than or equal to 100 mg/mL at 68° F (NTP, 1992);Density: 2.165 at 77 °F (NTP, 1992);', 'NFPA_pig': None, 'health_hazards': None, 'fire_hazards': None, 'instability_hazards': None, 'hazards': 'The rare inadvertent intravascular administration or rapid intravascular absorption of hypertonic sodium chloride can cause a shift of tissue fluids into the vascular bed, resulting in hypervolemia, electrolyte disturbances, circulatory failure, pulmonary embolism, or augmented hypertension. ( toxnet', 'hazards_combine': '', 'inhalation_first_aid': None, 'skin_first_aid': None, 'eye_first_aid': None, 'ingestion_first_aid': None, 'first_aid': "EYES: First check the victim for contact lenses and remove if present. Flush victim's eyes with water or normal saline solution for 20 to 30 minutes while simultaneously calling a hospital or poison control center. Do not put any ointments, oils, or medication in the victim's eyes without specific instructions from a physician. IMMEDIATELY transport the victim after flushing eyes to a hospital even if no symptoms (such as redness or irritation) develop. SKIN: IMMEDIATELY flood affected skin with water while removing and isolating all contaminated clothing. Gently wash all affected skin areas thoroughly with soap and water. If symptoms such as redness or irritation develop, IMMEDIATELY call a physician and be prepared to transport the victim to a hospital for treatment. INHALATION: IMMEDIATELY leave the contaminated area; take deep breaths of fresh air. If symptoms (such as wheezing, coughing, shortness of breath, or burning in the mouth, throat, or chest) develop, call a physician and be prepared to transport the victim to a hospital. Provide proper respiratory protection to rescuers entering an unknown atmosphere. Whenever possible, Self-Contained Breathing Apparatus (SCBA) should be used; if not available, use a level of protection greater than or equal to that advised under Protective Clothing. INGESTION: DO NOT INDUCE VOMITING. If the victim is conscious and not convulsing, give 1 or 2 glasses of water to dilute the chemical and IMMEDIATELY call a hospital or poison control center. Be prepared to transport the victim to a hospital if advised by a physician. If the victim is convulsing or unconscious, do not give anything by mouth, ensure that the victim's airway is open and lay the victim on his/her side with the head lower than the body. DO NOT INDUCE VOMITING. IMMEDIATELY transport the victim to a hospital. (NTP, 1992)", 'first_aid_combine': ''}
    chemical_2 = {'identifier': 'CaCO3', 'Name': 'Calcium carbonate', 'MW': '100.09 g/mol', 'ordor': 'Odorless', 'BP': 'Decomposes (NIOSH, 2016)', 'MP': '1517 to 2442 °F (Decomposes) (NIOSH, 2016)', 'solubility': '0.001 % (NIOSH, 2016)', 'density': '2.7 to 2.95 (NIOSH, 2016)', 'description': 'Calcium carbonate appears as white, odorless powder or colorless crystals. Practically insoluble in water. Occurs extensive in rocks world-wide. Ground calcium carbonate (CAS: 1317-65-3) results directly from the mining of limestone. The extraction process keeps the carbonate very close to its original state of purity and delivers a finely ground product either in dry or slurry form. Precipitated calcium carbonate (CAS: 471-34-1) is produced industrially by the decomposition of limestone to calcium oxide followed by subsequent recarbonization or as a by-product of the Solvay process (which is used to make sodium carbonate). Precipitated calcium carbonate is purer than ground calcium carbonate and has different (and tailorable) handling properties.', 'description_combine': 'ordor: Odorless;Boiling Point: Decomposes (NIOSH, 2016);Melting Point: 1517 to 2442 °F (Decomposes) (NIOSH, 2016);solubility: 0.001 % (NIOSH, 2016);Density: 2.7 to 2.95 (NIOSH, 2016);', 'NFPA_pig': None, 'health_hazards': None, 'fire_hazards': None, 'instability_hazards': None, 'hazards': None, 'hazards_combine': '', 'inhalation_first_aid': 'Fresh air.', 'skin_first_aid': 'Rinse skin with plenty of water or shower.', 'eye_first_aid': 'Rinse with plenty of water (remove contact lenses if easily possible).', 'ingestion_first_aid': 'Rinse mouth.', 'first_aid': 'Eye: If this chemical contacts the eyes, immediately wash the eyes with large amounts of water, occasionally lifting the lower and upper lids. Get medical attention immediately. Contact lenses should not be worn when working with this chemical. Skin: If this chemical contacts the skin, wash the contaminated skin with soap and water. Breathing: If a person breathes large amounts of this chemical, move the exposed person to fresh air at once. Other measures are usually unnecessary. (NIOSH, 2016)', 'first_aid_combine': 'inhalation: Fresh air.\nskin: Rinse skin with plenty of water or shower.\neye: Rinse with plenty of water (remove contact lenses if easily possible).\ningestion: Rinse mouth.\n'}
    chemicals = [chemical_1, chemical_2]
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



