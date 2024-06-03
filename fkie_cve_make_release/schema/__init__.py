# generated by datamodel-codegen:
#   filename:  nvd.json
#   timestamp: 2024-06-03T09:21:24+00:00

from __future__ import annotations

import datetime as dt

from enum import Enum
from typing import List, Optional

from msgspec import Meta, Struct, field
import msgspec
from typing_extensions import Annotated

from . import cvss_v2, cvss_v3

from .enums import (
    AccessComplexityType,
    AccessVectorType,
    AttackComplexityType,
    AttackVectorType,
    AuthenticationType,
    CiaRequirementType,
    CiaType,
    CiaTypeModel,
    CollateralDamagePotentialType,
    ConfidenceType,
    ExploitabilityType,
    ExploitCodeMaturityType,
    ModifiedAttackComplexityType,
    ModifiedAttackVectorType,
    ModifiedCiaType,
    ModifiedPrivilegesRequiredType,
    ModifiedScopeType,
    ModifiedUserInteractionType,
    Operator,
    PrivilegesRequiredType,
    RemediationLevelType,
    ReportConfidenceType,
    ScopeType,
    SeverityType,
    TargetDistributionType,
    Type,
    UserInteractionType,
)

from .types import (
    CveId,
    ScoreType,
)

class LangString(Struct, kw_only=True, omit_defaults=True):
    lang: str
    value: Annotated[str, Meta(max_length=4096)]


class Reference(Struct, kw_only=True, omit_defaults=True):
    url: Annotated[str, Meta(max_length=500)]
    source: Optional[str] = None
    tags: Optional[List[str]] = None


class VendorComment(Struct, kw_only=True, omit_defaults=True):
    organization: str
    comment: str
    last_modified: str = field(name='lastModified')


class Weakness(Struct, kw_only=True, omit_defaults=True):
    source: str
    type: str
    description: List[LangString]


class CpeMatch(Struct, kw_only=True, omit_defaults=True):
    vulnerable: bool
    criteria: str
    version_start_excluding: Optional[str] = field(
        name='versionStartExcluding', default=None
    )
    version_start_including: Optional[str] = field(
        name='versionStartIncluding', default=None
    )
    version_end_excluding: Optional[str] = field(
        name='versionEndExcluding', default=None
    )
    version_end_including: Optional[str] = field(
        name='versionEndIncluding', default=None
    )
    match_criteria_id: str = field(name='matchCriteriaId')


DefSubscore = Annotated[float, Meta(description='CVSS subscore.', ge=0.0, le=10.0)]


class Node(Struct, kw_only=True, omit_defaults=True):
    operator: Operator
    negate: Optional[bool] = None
    cpe_match: List[CpeMatch] = field(name='cpeMatch')


class CvssV2(Struct, kw_only=True, omit_defaults=True):
    source: str
    type: Type
    cvss_data: cvss_v2.Field0 = field(name='cvssData')
    base_severity: Optional[str] = field(name='baseSeverity', default=None)
    exploitability_score: Optional[DefSubscore] = field(
        name='exploitabilityScore', default=None
    )
    impact_score: Optional[DefSubscore] = field(name='impactScore', default=None)
    ac_insuf_info: Optional[bool] = field(name='acInsufInfo', default=None)
    obtain_all_privilege: Optional[bool] = field(
        name='obtainAllPrivilege', default=None
    )
    obtain_user_privilege: Optional[bool] = field(
        name='obtainUserPrivilege', default=None
    )
    obtain_other_privilege: Optional[bool] = field(
        name='obtainOtherPrivilege', default=None
    )
    user_interaction_required: Optional[bool] = field(
        name='userInteractionRequired', default=None
    )


class CvssV30(Struct, kw_only=True, omit_defaults=True):
    source: str
    type: Type
    cvss_data: cvss_v3.Field0 = field(name='cvssData')
    exploitability_score: Optional[DefSubscore] = field(
        name='exploitabilityScore', default=None
    )
    impact_score: Optional[DefSubscore] = field(name='impactScore', default=None)


class CvssV31(Struct, kw_only=True, omit_defaults=True):
    source: str
    type: Type
    cvss_data: cvss_v3.Field1 = field(name='cvssData')
    exploitability_score: Optional[DefSubscore] = field(
        name='exploitabilityScore', default=None
    )
    impact_score: Optional[DefSubscore] = field(name='impactScore', default=None)


class Config(Struct, kw_only=True, omit_defaults=True):
    operator: Optional[Operator] = None
    nodes: List[Node]
    negate: Optional[bool] = None


class Metrics(Struct, kw_only=True, omit_defaults=True):
    cvss_metric_v31: Optional[
        Annotated[List[CvssV31], Meta(description='CVSS V3.1 score.')]
    ] = field(name='cvssMetricV31', default=None)
    cvss_metric_v30: Optional[
        Annotated[List[CvssV30], Meta(description='CVSS V3.0 score.')]
    ] = field(name='cvssMetricV30', default=None)
    cvss_metric_v2: Optional[
        Annotated[List[CvssV2], Meta(description='CVSS V2.0 score.')]
    ] = field(name='cvssMetricV2', default=None)


class CveItem(Struct, kw_only=True, omit_defaults=True):
    id: CveId
    source_identifier: Optional[str] = field(name='sourceIdentifier', default=None)
    published: Annotated[dt.datetime, msgspec.Meta(tz=False)]
    last_modified: Annotated[dt.datetime, msgspec.Meta(tz=False)] = field(name='lastModified')
    vuln_status: Optional[str] = field(name='vulnStatus', default=None)
    evaluator_comment: Optional[str] = field(name='evaluatorComment', default=None)
    evaluator_solution: Optional[str] = field(name='evaluatorSolution', default=None)
    evaluator_impact: Optional[str] = field(name='evaluatorImpact', default=None)
    cisa_exploit_add: Optional[dt.date] = field(name='cisaExploitAdd', default=None)
    cisa_action_due: Optional[dt.date] = field(name='cisaActionDue', default=None)
    cisa_required_action: Optional[str] = field(name='cisaRequiredAction', default=None)
    cisa_vulnerability_name: Optional[str] = field(
        name='cisaVulnerabilityName', default=None
    )
    descriptions: List[LangString]
    vendor_comments: Optional[List[VendorComment]] = field(
        name='vendorComments', default=None
    )
    metrics: Optional[
        Annotated[
            Metrics,
            Meta(description='Metric scores for a vulnerability as found on NVD.'),
        ]
    ] = None
    weaknesses: Optional[List[Weakness]] = None
    configurations: Optional[List[Config]] = None
    references: List[Reference]


class DefCveItem(Struct, kw_only=True, omit_defaults=True):
    cve: CveItem


class JsonSchemaForNvdVulnerabilityDataApiVersion210(Struct, kw_only=True, omit_defaults=True):
    results_per_page: int = field(name='resultsPerPage')
    start_index: int = field(name='startIndex')
    total_results: int = field(name='totalResults')
    format: str
    version: str
    timestamp: Annotated[dt.datetime, msgspec.Meta(tz=False)]
    vulnerabilities: Annotated[
        List[DefCveItem], Meta(description='NVD feed array of CVE')
    ]
