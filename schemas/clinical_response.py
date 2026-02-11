from typing import List, Optional
from pydantic import BaseModel, Field


class ClinicalResponse(BaseModel):
    condition: str = Field(description="Canonical condition name")
    icd10: List[str] = Field(description="ICD-10 code(s) for the condition")
    rxnorm: List[str] = Field(description="RxNORM code(s) for relevant drugs")
    loinc: Optional[List[str]] = Field(
        default=None,
        description="LOINC code(s) for relevant labs or diagnostics",
    )
    summary: str = Field(description="Evidence narrative summarizing findings")
    sources: List[str] = Field(
        description="Citations as guideline names or PubMed PMIDs"
    )
