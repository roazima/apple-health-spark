import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("data/export.xml")
root = tree.getroot()

records = []
for elem in root.findall("Record"):
    record_type = elem.attrib.get("type")
    if record_type in [
        "HKQuantityTypeIdentifierStepCount",
        "HKQuantityTypeIdentifierActiveEnergyBurned",
        "HKCategoryTypeIdentifierSleepAnalysis"
    ]:
        raw_value = elem.attrib.get("value")
        if "Sleep" in record_type:
            value = 1  # Treat each record as 1 sleep segment
        else:
            try:
                value = float(raw_value)
            except (TypeError, ValueError):
                continue


        try:
            value = float(value)
        except ValueError:
            continue

        records.append({
            "type": record_type,
            "value": value,
            "startDate": elem.attrib["startDate"],
            "endDate": elem.attrib["endDate"]
        })

df = pd.DataFrame(records)
df.to_csv("data/export.csv", index=False)
