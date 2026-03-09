import json
from typing import Dict, Optional

from langchain.tools import tool

# Lookup structure: term → {icd10, rxnorm, loinc}
# ICD-10: condition codes, RxNORM: drug concept IDs, LOINC: lab/diagnostic codes
# To extend: add a new key matching a lowercase clinical term or common synonym.
_ONTOLOGY: Dict[str, dict] = {
    "diabetes": {
        "icd10": ["E11", "E11.9"],
        "rxnorm": ["860975", "4815"],   # metformin, insulin
        "loinc": ["4548-4", "17856-6"], # HbA1c, fasting glucose
    },
    "type 2 diabetes": {
        "icd10": ["E11", "E11.9"],
        "rxnorm": ["860975", "4815"],
        "loinc": ["4548-4", "17856-6"],
    },
    "hypertension": {
        "icd10": ["I10"],
        "rxnorm": ["29046", "214354"],  # lisinopril, amlodipine
        "loinc": ["55284-4"],           # blood pressure panel
    },
    "asthma": {
        "icd10": ["J45", "J45.9"],
        "rxnorm": ["745679", "2108226"], # albuterol, budesonide
        "loinc": ["33243-0"],            # spirometry FEV1
    },
    "heart failure": {
        "icd10": ["I50", "I50.9"],
        "rxnorm": ["29046", "203644"],   # lisinopril, carvedilol
        "loinc": ["33762-9"],            # NT-proBNP
    },
    "copd": {
        "icd10": ["J44", "J44.9"],
        "rxnorm": ["2108226", "1547660"], # budesonide, tiotropium
        "loinc": ["33243-0"],
    },
    "atrial fibrillation": {
        "icd10": ["I48", "I48.91"],
        "rxnorm": ["1037045", "114979"],  # apixaban, metoprolol
        "loinc": ["11524-6"],             # ECG
    },
    "chronic kidney disease": {
        "icd10": ["N18", "N18.9"],
        "rxnorm": ["29046"],              # lisinopril (renoprotective)
        "loinc": ["2160-0", "33914-3"],   # creatinine, eGFR
    },
    "hypothyroidism": {
        "icd10": ["E03.9"],
        "rxnorm": ["10582"],              # levothyroxine
        "loinc": ["3016-3"],             # TSH
    },
    "depression": {
        "icd10": ["F32", "F32.9"],
        "rxnorm": ["41493", "72625"],     # sertraline, fluoxetine
        "loinc": None,
    },
}


def _normalize(term: str) -> Optional[str]:
    key = term.strip().lower()
    if key in _ONTOLOGY:
        return key
    for k in _ONTOLOGY:
        if k in key or key in k:
            return k
    return None


@tool
def map_ontology(term: str) -> str:
    """Map a clinical term to ICD-10, RxNORM, and LOINC codes.

    Returns a JSON object with icd10, rxnorm, and loinc fields, or an
    error message if the term is not found in the ontology.
    """
    key = _normalize(term)
    if key is None:
        return json.dumps({"error": f"Term not found in ontology: {term}"})
    return json.dumps(_ONTOLOGY[key])
