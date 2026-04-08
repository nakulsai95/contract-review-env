# Copyright (c) 2024. All rights reserved.
# Contract clause scenarios with ground truth for grading.
# Sourced from patterns in SEC EDGAR filings and open-source contract templates.

from typing import Any, Dict, List

# Clause types
CLAUSE_TYPES = [
    "indemnification",
    "limitation_of_liability",
    "termination",
    "confidentiality",
    "ip_assignment",
    "non_compete",
    "payment_terms",
    "governing_law",
    "force_majeure",
    "warranty",
    "data_protection",
    "dispute_resolution",
    "assignment_and_change_of_control",
    "representations_and_warranties",
    "audit_rights",
    "insurance_requirements",
    "most_favored_nation",
]

RISK_LEVELS = ["low", "medium", "high"]

TEAMS = [
    "desktop_support",
    "network_ops",
    "security",
    "sysadmin",
    "app_support",
]

# fmt: off
SCENARIOS: List[Dict[str, Any]] = [
    # ── EASY (0-9): clear clause types, obvious risk ──────────────────────
    {
        "id": "clause_001",
        "difficulty": "easy",
        "clause_text": (
            "The Vendor shall indemnify, defend, and hold harmless the Client and its "
            "officers, directors, employees, and agents from and against any and all claims, "
            "damages, losses, costs, and expenses (including reasonable attorneys' fees) "
            "arising out of or relating to any breach of this Agreement by the Vendor."
        ),
        "clause_type": "indemnification",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard mutual indemnification clause with reasonable scope. No unusual risk.",
        "suggested_edit": None,
    },
    {
        "id": "clause_002",
        "difficulty": "easy",
        "clause_text": (
            "IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, "
            "SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, REGARDLESS OF THE CAUSE OF "
            "ACTION OR THE THEORY OF LIABILITY, EVEN IF SUCH PARTY HAS BEEN ADVISED OF "
            "THE POSSIBILITY OF SUCH DAMAGES."
        ),
        "clause_type": "limitation_of_liability",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard bilateral limitation of liability excluding consequential damages.",
        "suggested_edit": None,
    },
    {
        "id": "clause_003",
        "difficulty": "easy",
        "clause_text": (
            "Either party may terminate this Agreement upon thirty (30) days' prior "
            "written notice to the other party. Upon termination, all outstanding invoices "
            "shall become immediately due and payable."
        ),
        "clause_type": "termination",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard termination for convenience with reasonable notice period.",
        "suggested_edit": None,
    },
    {
        "id": "clause_004",
        "difficulty": "easy",
        "clause_text": (
            "Each party agrees to keep confidential all non-public information received "
            "from the other party during the term of this Agreement. This obligation shall "
            "survive for a period of three (3) years following termination."
        ),
        "clause_type": "confidentiality",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard confidentiality clause with reasonable 3-year survival period.",
        "suggested_edit": None,
    },
    {
        "id": "clause_005",
        "difficulty": "easy",
        "clause_text": (
            "This Agreement shall be governed by and construed in accordance with the "
            "laws of the State of Delaware, without regard to its conflict of laws principles."
        ),
        "clause_type": "governing_law",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard Delaware governing law clause. Common and well-understood.",
        "suggested_edit": None,
    },
    {
        "id": "clause_006",
        "difficulty": "easy",
        "clause_text": (
            "Client shall pay all undisputed invoices within thirty (30) days of receipt. "
            "Late payments shall accrue interest at a rate of 1.5% per month or the maximum "
            "rate permitted by law, whichever is less."
        ),
        "clause_type": "payment_terms",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard net-30 payment terms with reasonable late fee.",
        "suggested_edit": None,
    },
    {
        "id": "clause_007",
        "difficulty": "easy",
        "clause_text": (
            "The Vendor warrants that all services provided under this Agreement shall "
            "be performed in a professional and workmanlike manner consistent with "
            "generally accepted industry standards."
        ),
        "clause_type": "warranty",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard professional services warranty. No unusual risk.",
        "suggested_edit": None,
    },
    {
        "id": "clause_008",
        "difficulty": "easy",
        "clause_text": (
            "Neither party shall be liable for any failure or delay in performing its "
            "obligations under this Agreement if such failure or delay results from "
            "circumstances beyond the reasonable control of that party, including but not "
            "limited to acts of God, natural disasters, war, terrorism, riots, embargoes, "
            "acts of civil or military authorities, fire, floods, accidents, strikes, or "
            "shortages of transportation, facilities, fuel, energy, labor, or materials."
        ),
        "clause_type": "force_majeure",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard force majeure clause with comprehensive list of qualifying events.",
        "suggested_edit": None,
    },
    {
        "id": "clause_009",
        "difficulty": "easy",
        "clause_text": (
            "All intellectual property rights in any work product created by the Vendor "
            "specifically for the Client under this Agreement shall be assigned to and "
            "owned by the Client upon full payment."
        ),
        "clause_type": "ip_assignment",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard IP assignment clause with payment condition. Clear and balanced.",
        "suggested_edit": None,
    },
    {
        "id": "clause_010",
        "difficulty": "easy",
        "clause_text": (
            "Any dispute arising out of or relating to this Agreement shall be resolved "
            "through binding arbitration in accordance with the rules of the American "
            "Arbitration Association, with the arbitration to be held in New York, New York."
        ),
        "clause_type": "dispute_resolution",
        "risk_level": "low",
        "issues": [],
        "explanation": "Standard arbitration clause with recognized body and specified venue.",
        "suggested_edit": None,
    },

    # ── MEDIUM (10-19): identifiable issues, moderate risk ────────────────
    {
        "id": "clause_011",
        "difficulty": "medium",
        "clause_text": (
            "The Contractor shall indemnify and hold harmless the Company from any and all "
            "claims, damages, losses, and expenses, including attorneys' fees, arising from "
            "any act or omission of the Contractor, its employees, or subcontractors, "
            "WHETHER OR NOT CAUSED IN WHOLE OR IN PART BY THE NEGLIGENCE OF THE COMPANY."
        ),
        "clause_type": "indemnification",
        "risk_level": "high",
        "issues": [
            "unilateral_indemnification",
            "includes_company_negligence",
            "unlimited_scope",
        ],
        "explanation": (
            "This is a one-sided indemnification that requires the Contractor to cover "
            "losses even when the Company is negligent. This shifts disproportionate risk "
            "to the Contractor."
        ),
        "suggested_edit": (
            "The Contractor shall indemnify and hold harmless the Company from any and all "
            "claims, damages, losses, and expenses, including reasonable attorneys' fees, "
            "arising from any act or omission of the Contractor, its employees, or "
            "subcontractors, except to the extent caused by the negligence or willful "
            "misconduct of the Company."
        ),
    },
    {
        "id": "clause_012",
        "difficulty": "medium",
        "clause_text": (
            "THE TOTAL LIABILITY OF THE VENDOR UNDER THIS AGREEMENT SHALL NOT EXCEED "
            "ONE HUNDRED DOLLARS ($100.00). IN NO EVENT SHALL THE VENDOR BE LIABLE FOR "
            "ANY DAMAGES WHATSOEVER, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, "
            "SPECIAL, OR CONSEQUENTIAL DAMAGES."
        ),
        "clause_type": "limitation_of_liability",
        "risk_level": "high",
        "issues": [
            "unreasonably_low_cap",
            "excludes_direct_damages",
            "unilateral_protection",
        ],
        "explanation": (
            "The $100 liability cap is unreasonably low for any commercial agreement. "
            "Additionally, excluding even direct damages effectively eliminates all "
            "meaningful remedies for the Client."
        ),
        "suggested_edit": (
            "THE TOTAL LIABILITY OF THE VENDOR UNDER THIS AGREEMENT SHALL NOT EXCEED "
            "THE TOTAL FEES PAID BY CLIENT IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM. "
            "IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR INDIRECT, SPECIAL, OR "
            "CONSEQUENTIAL DAMAGES."
        ),
    },
    {
        "id": "clause_013",
        "difficulty": "medium",
        "clause_text": (
            "The Company may terminate this Agreement immediately and without notice for "
            "any reason or no reason at all. Upon termination by the Company, the Contractor "
            "shall not be entitled to any compensation for work in progress or completed "
            "but not yet invoiced."
        ),
        "clause_type": "termination",
        "risk_level": "high",
        "issues": [
            "no_notice_period",
            "forfeiture_of_earned_compensation",
            "unilateral_termination",
        ],
        "explanation": (
            "This clause allows the Company to terminate without notice and forfeit "
            "compensation for work already performed. This is highly unfavorable to the "
            "Contractor and may be unenforceable in some jurisdictions."
        ),
        "suggested_edit": (
            "Either party may terminate this Agreement with thirty (30) days' written "
            "notice. Upon termination, the Contractor shall be compensated for all work "
            "completed and accepted through the termination date."
        ),
    },
    {
        "id": "clause_014",
        "difficulty": "medium",
        "clause_text": (
            "The Receiving Party's confidentiality obligations under this Agreement shall "
            "survive in perpetuity. The Receiving Party shall not disclose Confidential "
            "Information to any third party for any reason, including as required by law, "
            "without the prior written consent of the Disclosing Party."
        ),
        "clause_type": "confidentiality",
        "risk_level": "high",
        "issues": [
            "perpetual_obligation",
            "blocks_legal_compliance",
            "no_exceptions",
        ],
        "explanation": (
            "A perpetual confidentiality obligation is unusual and burdensome. More "
            "critically, prohibiting disclosure even when required by law conflicts with "
            "legal obligations and is likely unenforceable."
        ),
        "suggested_edit": (
            "The Receiving Party's confidentiality obligations shall survive for five (5) "
            "years following termination. The Receiving Party may disclose Confidential "
            "Information if required by law, regulation, or court order, provided it gives "
            "prompt notice to the Disclosing Party to allow them to seek a protective order."
        ),
    },
    {
        "id": "clause_015",
        "difficulty": "medium",
        "clause_text": (
            "All intellectual property, including but not limited to patents, copyrights, "
            "trade secrets, and know-how, developed by the Contractor at any time during "
            "the term of this Agreement, whether or not related to the services performed "
            "hereunder, shall be the sole and exclusive property of the Company."
        ),
        "clause_type": "ip_assignment",
        "risk_level": "high",
        "issues": [
            "overbroad_scope",
            "captures_unrelated_ip",
            "no_pre_existing_ip_carveout",
        ],
        "explanation": (
            "This clause captures ALL IP created during the agreement period, even if "
            "unrelated to the contracted work. It also fails to carve out pre-existing "
            "IP. This is overly broad and potentially unenforceable."
        ),
        "suggested_edit": (
            "All intellectual property developed by the Contractor specifically in "
            "performance of the services under this Agreement shall be the property of "
            "the Company upon full payment. Pre-existing IP of the Contractor shall remain "
            "the Contractor's property, with a license granted to Company as needed to use "
            "the deliverables."
        ),
    },
    {
        "id": "clause_016",
        "difficulty": "medium",
        "clause_text": (
            "During the term of this Agreement and for a period of three (3) years "
            "thereafter, the Employee shall not, directly or indirectly, engage in any "
            "business that competes with the Company anywhere in the world."
        ),
        "clause_type": "non_compete",
        "risk_level": "high",
        "issues": [
            "excessive_duration",
            "unlimited_geographic_scope",
            "overly_broad_activity_restriction",
        ],
        "explanation": (
            "A 3-year non-compete with worldwide geographic scope is likely "
            "unenforceable in most jurisdictions. Courts typically require reasonable "
            "time limits (6-24 months) and geographic restrictions."
        ),
        "suggested_edit": (
            "During the term of this Agreement and for a period of twelve (12) months "
            "thereafter, the Employee shall not, directly or indirectly, engage in any "
            "business that directly competes with the Company's primary line of business "
            "within the metropolitan areas where the Company maintains offices."
        ),
    },
    {
        "id": "clause_017",
        "difficulty": "medium",
        "clause_text": (
            "Client shall pay all invoices within five (5) business days of receipt. "
            "Late payments shall incur a penalty of 10% of the outstanding amount per week. "
            "The Vendor reserves the right to suspend all services immediately upon any "
            "late payment."
        ),
        "clause_type": "payment_terms",
        "risk_level": "high",
        "issues": [
            "unreasonably_short_payment_window",
            "excessive_late_penalty",
            "immediate_service_suspension",
        ],
        "explanation": (
            "5 business days is an extremely short payment window. A 10% weekly penalty "
            "amounts to 520% annualized interest, which may violate usury laws. Immediate "
            "suspension without cure period is aggressive."
        ),
        "suggested_edit": (
            "Client shall pay all undisputed invoices within thirty (30) days of receipt. "
            "Late payments shall incur interest at 1.5% per month. The Vendor may suspend "
            "services if payment is more than fifteen (15) days overdue after written notice."
        ),
    },
    {
        "id": "clause_018",
        "difficulty": "medium",
        "clause_text": (
            "THE VENDOR MAKES NO WARRANTIES OF ANY KIND, WHETHER EXPRESS, IMPLIED, "
            "STATUTORY, OR OTHERWISE, INCLUDING ANY WARRANTIES OF MERCHANTABILITY, "
            "FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. ALL SERVICES AND "
            "DELIVERABLES ARE PROVIDED 'AS IS' AND 'AS AVAILABLE'."
        ),
        "clause_type": "warranty",
        "risk_level": "high",
        "issues": [
            "complete_warranty_disclaimer",
            "no_fitness_warranty",
            "as_is_for_custom_services",
        ],
        "explanation": (
            "A complete warranty disclaimer is unusual for custom professional services. "
            "The client has no recourse if deliverables are defective. 'As is' language "
            "is more appropriate for off-the-shelf software, not bespoke work."
        ),
        "suggested_edit": (
            "The Vendor warrants that all services shall be performed in a professional "
            "and workmanlike manner. Deliverables shall materially conform to the agreed "
            "specifications for a period of ninety (90) days after acceptance. THE VENDOR "
            "DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED."
        ),
    },
    {
        "id": "clause_019",
        "difficulty": "medium",
        "clause_text": (
            "Each party shall comply with all applicable data protection laws, including "
            "GDPR where applicable. However, the Vendor shall have no liability for any "
            "data breach, loss, or unauthorized access to Client data, regardless of cause."
        ),
        "clause_type": "data_protection",
        "risk_level": "high",
        "issues": [
            "contradictory_terms",
            "blanket_liability_exclusion_for_data",
            "gdpr_non_compliance",
        ],
        "explanation": (
            "The clause references GDPR compliance but then disclaims all liability for "
            "data breaches — these are contradictory. Under GDPR, data processors cannot "
            "contractually exclude liability for data protection failures."
        ),
        "suggested_edit": (
            "Each party shall comply with all applicable data protection laws, including "
            "GDPR where applicable. The Vendor shall implement appropriate technical and "
            "organizational measures to protect Client data and shall be liable for data "
            "breaches caused by its failure to maintain such measures."
        ),
    },
    {
        "id": "clause_020",
        "difficulty": "medium",
        "clause_text": (
            "Neither party shall be liable for delays caused by events beyond reasonable "
            "control. The Vendor may invoke force majeure for any event it deems to be "
            "beyond its control, including but not limited to staffing shortages, budget "
            "constraints, or changes in business priorities."
        ),
        "clause_type": "force_majeure",
        "risk_level": "high",
        "issues": [
            "overbroad_force_majeure",
            "includes_foreseeable_business_risks",
            "subjective_determination",
        ],
        "explanation": (
            "Staffing shortages, budget constraints, and changes in business priorities "
            "are normal business risks, not force majeure events. Allowing one party to "
            "subjectively determine force majeure effectively gives them an unlimited "
            "excuse for non-performance."
        ),
        "suggested_edit": (
            "Neither party shall be liable for delays caused by events genuinely beyond "
            "reasonable control, such as natural disasters, war, government action, or "
            "pandemic. The affected party must provide prompt notice and demonstrate the "
            "event was unforeseeable and unavoidable."
        ),
    },

    # ── HARD (20-29): subtle issues, require legal reasoning ──────────────
    {
        "id": "clause_021",
        "difficulty": "hard",
        "clause_text": (
            "The Contractor agrees to indemnify the Company against all third-party claims "
            "arising from the Contractor's services. The Company agrees to indemnify the "
            "Contractor against claims arising from the Company's use of deliverables in "
            "a manner not authorized under this Agreement. Notwithstanding the foregoing, "
            "the Contractor's total indemnification obligation shall not exceed the fees "
            "paid, while the Company's indemnification obligation shall be unlimited."
        ),
        "clause_type": "indemnification",
        "risk_level": "medium",
        "issues": [
            "asymmetric_caps",
            "hidden_imbalance_in_mutual_clause",
        ],
        "explanation": (
            "While this appears to be a balanced mutual indemnification, the caps are "
            "asymmetric: Contractor is capped at fees paid, but Company's obligation is "
            "unlimited. This hidden imbalance favors the Contractor and may not reflect "
            "the actual risk allocation the Company intends."
        ),
        "suggested_edit": (
            "Both parties' indemnification obligations shall be subject to the same "
            "liability cap equal to the total fees paid or payable under this Agreement "
            "in the twelve (12) months preceding the claim, except for indemnification "
            "related to IP infringement or willful misconduct, which shall be uncapped."
        ),
    },
    {
        "id": "clause_022",
        "difficulty": "hard",
        "clause_text": (
            "The total aggregate liability of the Vendor shall not exceed the greater of "
            "(a) the fees paid in the twelve months preceding the claim, or (b) $500,000. "
            "This limitation shall not apply to (i) breaches of confidentiality, "
            "(ii) indemnification obligations, (iii) willful misconduct, or (iv) violations "
            "of applicable law. The Vendor's liability for data breaches shall be limited "
            "to direct damages only."
        ),
        "clause_type": "limitation_of_liability",
        "risk_level": "medium",
        "issues": [
            "carveouts_may_swallow_cap",
            "data_breach_sub_limit_conflicts_with_carveouts",
        ],
        "explanation": (
            "The broad carveouts (confidentiality, indemnification, misconduct, legal "
            "violations) effectively undermine the cap for most serious claims. "
            "Additionally, the data breach sub-limit to direct damages may conflict with "
            "the confidentiality carveout, creating ambiguity about which provision "
            "controls in a data breach scenario."
        ),
        "suggested_edit": (
            "Clarify that the data breach limitation is a specific sub-limit within the "
            "broader framework: 'For data breaches that do not involve willful misconduct, "
            "liability shall be limited to direct damages up to 2x the annual fees. For "
            "data breaches involving willful misconduct, the general carveout applies.'"
        ),
    },
    {
        "id": "clause_023",
        "difficulty": "hard",
        "clause_text": (
            "This Agreement shall automatically renew for successive one-year terms unless "
            "either party provides written notice of non-renewal at least ninety (90) days "
            "before the end of the then-current term. The Company may increase fees by up "
            "to 15% upon each renewal. Early termination by Client during any renewal term "
            "shall require payment of all remaining fees for that term."
        ),
        "clause_type": "termination",
        "risk_level": "medium",
        "issues": [
            "auto_renewal_with_price_escalation",
            "early_termination_penalty",
            "long_notice_period_creates_lock_in",
        ],
        "explanation": (
            "The combination of auto-renewal, 15% annual price increases, and a full-term "
            "early termination penalty creates significant lock-in. If the Client misses "
            "the 90-day notice window, they face either a 15% price increase or paying "
            "the full remaining year's fees to exit."
        ),
        "suggested_edit": (
            "This Agreement shall automatically renew for successive one-year terms unless "
            "either party provides written notice of non-renewal at least sixty (60) days "
            "before the end of the then-current term. Fee increases upon renewal shall not "
            "exceed 5% or CPI, whichever is greater. Client may terminate early with sixty "
            "(60) days' notice, paying a pro-rated termination fee equal to three months' "
            "fees."
        ),
    },
    {
        "id": "clause_024",
        "difficulty": "hard",
        "clause_text": (
            "Confidential Information shall mean all information disclosed by either party, "
            "whether orally, in writing, or electronically, that is designated as "
            "confidential or that a reasonable person would understand to be confidential. "
            "Exclusions: (a) information that becomes publicly available through no fault "
            "of the receiving party; (b) information independently developed by the "
            "receiving party. The receiving party may disclose Confidential Information "
            "if required by law, provided it gives the disclosing party five (5) business "
            "days' notice before disclosure."
        ),
        "clause_type": "confidentiality",
        "risk_level": "medium",
        "issues": [
            "missing_prior_knowledge_exclusion",
            "notice_period_may_conflict_with_legal_deadlines",
            "no_carveout_for_professional_advisors",
        ],
        "explanation": (
            "The exclusions are missing the standard 'already known to receiving party' "
            "exception. The 5-day notice requirement before legally compelled disclosure "
            "may be impossible to meet with certain subpoenas or regulatory demands. "
            "There's no carveout allowing disclosure to attorneys, accountants, or auditors."
        ),
        "suggested_edit": (
            "Add exclusion: '(c) information already known to the receiving party at the "
            "time of disclosure without obligation of confidentiality.' Modify legal "
            "disclosure: 'provided it gives prompt notice where legally permitted.' Add: "
            "'The receiving party may disclose to its professional advisors who are bound "
            "by confidentiality obligations no less restrictive than these.'"
        ),
    },
    {
        "id": "clause_025",
        "difficulty": "hard",
        "clause_text": (
            "All work product, inventions, discoveries, and improvements conceived or "
            "developed by the Contractor in the course of performing services shall be "
            "works made for hire and the exclusive property of the Company. To the extent "
            "any work product does not qualify as work made for hire, the Contractor "
            "hereby irrevocably assigns all rights therein to the Company. The Contractor "
            "grants the Company a perpetual, royalty-free license to any pre-existing IP "
            "incorporated into deliverables."
        ),
        "clause_type": "ip_assignment",
        "risk_level": "medium",
        "issues": [
            "work_for_hire_misapplication_to_contractor",
            "perpetual_license_to_preexisting_ip_too_broad",
            "no_license_back_to_contractor",
        ],
        "explanation": (
            "Work-for-hire doctrine typically applies to employees, not independent "
            "contractors (only 9 specific categories qualify under copyright law). The "
            "assignment backup is good practice, but the perpetual royalty-free license "
            "to pre-existing IP is overly broad — it could give the Company rights to "
            "the Contractor's core tools and frameworks. No license-back is provided "
            "for the Contractor to continue using their own pre-existing IP."
        ),
        "suggested_edit": (
            "Remove work-for-hire language and rely on assignment: 'The Contractor hereby "
            "assigns all rights in work product to the Company upon payment.' Narrow the "
            "pre-existing IP license: 'limited to use within the deliverables as delivered.' "
            "Add license-back: 'The Contractor retains the right to use its pre-existing "
            "IP in other engagements.'"
        ),
    },
    {
        "id": "clause_026",
        "difficulty": "hard",
        "clause_text": (
            "For a period of eighteen (18) months following termination, Employee shall "
            "not solicit or accept business from any entity that was a client, prospective "
            "client, or referral source of the Company during the Employee's tenure, nor "
            "shall Employee recruit any current or former employee of the Company who was "
            "employed at any time during the twenty-four (24) months prior to Employee's "
            "departure."
        ),
        "clause_type": "non_compete",
        "risk_level": "medium",
        "issues": [
            "prospective_client_scope_too_broad",
            "former_employee_restriction_unusual",
            "no_geographic_limitation",
            "combined_non_solicit_and_non_recruit",
        ],
        "explanation": (
            "Including 'prospective clients' is overly broad — it could encompass any "
            "entity the Company ever pitched. The restriction on recruiting 'former' "
            "employees extends the Company's control over people who no longer work there. "
            "The clause combines customer non-solicitation and employee non-recruitment "
            "without distinguishing their scope or duration."
        ),
        "suggested_edit": (
            "Limit to actual clients: 'entities that were active clients during the final "
            "twelve (12) months.' Narrow recruitment restriction to current employees only. "
            "Consider separating the non-solicitation and non-recruitment covenants with "
            "independent enforceability provisions."
        ),
    },
    {
        "id": "clause_027",
        "difficulty": "hard",
        "clause_text": (
            "Vendor warrants that the software shall perform materially in accordance "
            "with the documentation for a period of twelve (12) months from delivery. "
            "The Vendor's sole obligation and Client's exclusive remedy for breach of "
            "this warranty shall be, at Vendor's option, (a) repair or replacement of "
            "the non-conforming software, or (b) a refund of the fees paid for the "
            "non-conforming component. This warranty shall not apply if the software "
            "has been modified by anyone other than the Vendor or used in combination "
            "with third-party software not approved by the Vendor."
        ),
        "clause_type": "warranty",
        "risk_level": "medium",
        "issues": [
            "exclusive_remedy_limits_recourse",
            "vendor_chooses_remedy",
            "third_party_integration_exclusion_too_broad",
        ],
        "explanation": (
            "The exclusive remedy clause means the Client cannot seek damages beyond "
            "repair/replace/refund, even if a defect causes significant business losses. "
            "The Vendor choosing the remedy (not the Client) further weakens the Client's "
            "position. The third-party software exclusion could void the warranty in most "
            "real-world deployments where integration is standard."
        ),
        "suggested_edit": (
            "Allow Client to choose between repair and refund after a reasonable cure "
            "period. Add: 'If Vendor fails to cure within thirty (30) days, Client may "
            "pursue other remedies at law.' Narrow the exclusion: 'software modified "
            "without Vendor's consent in a manner that caused the non-conformity.'"
        ),
    },
    {
        "id": "clause_028",
        "difficulty": "hard",
        "clause_text": (
            "The Vendor shall process personal data solely on behalf of and in accordance "
            "with the Client's documented instructions. The Vendor shall implement "
            "appropriate technical and organizational security measures. In the event of "
            "a personal data breach, the Vendor shall notify the Client within 72 hours "
            "of becoming aware of the breach. The Vendor may engage sub-processors without "
            "the Client's prior consent, provided the Vendor maintains an up-to-date list "
            "of sub-processors on its website."
        ),
        "clause_type": "data_protection",
        "risk_level": "medium",
        "issues": [
            "sub_processor_engagement_without_consent",
            "website_list_insufficient_notice",
            "no_audit_rights",
            "no_data_deletion_obligation",
        ],
        "explanation": (
            "Under GDPR Article 28, the controller must authorize sub-processors — a "
            "website listing alone may not meet the 'specific or general written "
            "authorization' requirement. No audit rights are provided for the Client to "
            "verify compliance. There is no obligation for data return or deletion upon "
            "termination."
        ),
        "suggested_edit": (
            "Add: 'The Vendor shall provide thirty (30) days' prior notice before engaging "
            "new sub-processors, allowing the Client to object.' Add audit rights: 'The "
            "Client may audit the Vendor's compliance annually.' Add data return: 'Upon "
            "termination, the Vendor shall return or securely delete all personal data "
            "within thirty (30) days.'"
        ),
    },
    {
        "id": "clause_029",
        "difficulty": "hard",
        "clause_text": (
            "Any dispute arising under this Agreement shall first be submitted to "
            "mediation under the ICC Mediation Rules. If mediation fails within sixty "
            "(60) days, the dispute shall be finally resolved by arbitration under the "
            "ICC Arbitration Rules by three arbitrators appointed in accordance with said "
            "rules. The seat of arbitration shall be Singapore. The language of the "
            "arbitration shall be English. Judgment upon the award may be entered in any "
            "court having jurisdiction. Notwithstanding the foregoing, either party may "
            "seek injunctive relief in any court of competent jurisdiction."
        ),
        "clause_type": "dispute_resolution",
        "risk_level": "medium",
        "issues": [
            "three_arbitrator_panel_expensive",
            "icc_costs_significant",
            "singapore_seat_may_be_inconvenient",
            "injunctive_relief_carveout_may_undermine_arbitration",
        ],
        "explanation": (
            "A three-arbitrator ICC panel can cost $100K+ in fees alone, which may be "
            "disproportionate to smaller disputes. The Singapore seat may be inconvenient "
            "if neither party operates there. The broad injunctive relief carveout in "
            "'any court' could be used to forum-shop and bypass the arbitration agreement."
        ),
        "suggested_edit": (
            "For disputes under $500K, use a single arbitrator to reduce costs. Specify "
            "that the seat should be the jurisdiction with the most significant connection "
            "to the agreement. Narrow the injunctive relief carveout: 'in the courts of "
            "the arbitration seat only, and solely for interim measures pending the "
            "arbitration tribunal's constitution.'"
        ),
    },
    {
        "id": "clause_030",
        "difficulty": "hard",
        "clause_text": (
            "The Company may assign this Agreement or any rights hereunder to any "
            "affiliate or successor entity without the Contractor's consent. The "
            "Contractor may not assign this Agreement without the Company's prior written "
            "consent. Any change of control of the Contractor (including acquisition of "
            "more than 50% of voting shares) shall be deemed an assignment requiring "
            "consent. The Company may withhold consent for any reason in its sole "
            "discretion."
        ),
        "clause_type": "termination",
        "risk_level": "medium",
        "issues": [
            "asymmetric_assignment_rights",
            "change_of_control_only_applies_to_contractor",
            "sole_discretion_consent_standard",
        ],
        "explanation": (
            "The Company can freely assign (including to entities with less financial "
            "stability), but the Contractor cannot — even a change of control triggers "
            "the consent requirement. The 'sole discretion' standard means the Company "
            "can block any Contractor assignment for any reason, giving it leverage in "
            "negotiations."
        ),
        "suggested_edit": (
            "Make assignment restrictions mutual, or at minimum require the Company's "
            "assignee to assume all obligations. Apply the change-of-control provision "
            "to both parties. Change 'sole discretion' to 'not unreasonably withheld.'"
        ),
    },

    # ── NEW EASY (31-38): standard/safe clauses ─────────────────────────────
    {
        "id": "clause_031",
        "difficulty": "easy",
        "clause_text": (
            "Neither party may assign this Agreement or any rights or obligations "
            "hereunder without the prior written consent of the other party, which "
            "consent shall not be unreasonably withheld. Notwithstanding the foregoing, "
            "either party may assign this Agreement to an affiliate or in connection "
            "with a merger, acquisition, or sale of all or substantially all of its assets."
        ),
        "clause_type": "assignment_and_change_of_control",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Standard mutual assignment restriction with a reasonable exception for "
            "corporate restructurings. The 'not unreasonably withheld' standard is balanced."
        ),
        "suggested_edit": None,
    },
    {
        "id": "clause_032",
        "difficulty": "easy",
        "clause_text": (
            "Each party represents and warrants that: (a) it is duly organized, validly "
            "existing, and in good standing under the laws of its jurisdiction of "
            "incorporation; (b) it has full power and authority to enter into this "
            "Agreement and perform its obligations hereunder; and (c) this Agreement "
            "constitutes a legal, valid, and binding obligation enforceable in accordance "
            "with its terms."
        ),
        "clause_type": "representations_and_warranties",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Standard corporate representations and warranties establishing basic "
            "authority and capacity. These are boilerplate provisions found in virtually "
            "all commercial agreements."
        ),
        "suggested_edit": None,
    },
    {
        "id": "clause_033",
        "difficulty": "easy",
        "clause_text": (
            "The Client shall have the right, upon thirty (30) days' prior written "
            "notice, to audit the Vendor's books, records, and systems relevant to the "
            "services provided under this Agreement, no more than once per calendar year. "
            "Such audits shall be conducted during normal business hours and shall not "
            "unreasonably interfere with the Vendor's operations."
        ),
        "clause_type": "audit_rights",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Standard audit rights clause with reasonable frequency limitation, advance "
            "notice, and business-hours restriction. Well-balanced between oversight and "
            "operational disruption concerns."
        ),
        "suggested_edit": None,
    },
    {
        "id": "clause_034",
        "difficulty": "easy",
        "clause_text": (
            "The Vendor shall maintain, at its own expense, the following insurance "
            "coverage throughout the term of this Agreement: (a) commercial general "
            "liability insurance with limits of not less than $1,000,000 per occurrence "
            "and $2,000,000 in the aggregate; (b) professional errors and omissions "
            "insurance with limits of not less than $1,000,000 per claim; and "
            "(c) workers' compensation insurance as required by applicable law."
        ),
        "clause_type": "insurance_requirements",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Standard insurance requirements with industry-typical coverage amounts. "
            "The types of coverage are appropriate for a professional services engagement."
        ),
        "suggested_edit": None,
    },
    {
        "id": "clause_035",
        "difficulty": "easy",
        "clause_text": (
            "If the Vendor enters into an agreement with any other customer for "
            "substantially similar services at a lower price, the Vendor shall promptly "
            "notify the Client and offer the Client the same pricing terms. This "
            "obligation shall apply only to agreements executed during the term of this "
            "Agreement and for comparable scope and volume of services."
        ),
        "clause_type": "most_favored_nation",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Standard MFN clause with reasonable qualifiers limiting it to comparable "
            "scope and volume. The notification obligation and term limitation are balanced."
        ),
        "suggested_edit": None,
    },
    {
        "id": "clause_036",
        "difficulty": "easy",
        "clause_text": (
            "The Contractor shall maintain comprehensive cyber liability insurance with "
            "minimum coverage of $5,000,000 per occurrence, including coverage for data "
            "breaches, network security failures, and privacy liability. The Contractor "
            "shall name the Client as an additional insured and provide certificates of "
            "insurance upon request."
        ),
        "clause_type": "insurance_requirements",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Reasonable cyber liability insurance requirement for a contractor handling "
            "sensitive data. The coverage amount and scope are within industry norms for "
            "mid-market engagements."
        ),
        "suggested_edit": None,
    },
    {
        "id": "clause_037",
        "difficulty": "easy",
        "clause_text": (
            "Each party represents and warrants that it shall comply with all applicable "
            "anti-bribery and anti-corruption laws, including the U.S. Foreign Corrupt "
            "Practices Act and the UK Bribery Act 2010. Neither party shall make, offer, "
            "or authorize any payment or gift to any government official or other person "
            "for the purpose of influencing any official act or securing any improper "
            "advantage."
        ),
        "clause_type": "representations_and_warranties",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Standard anti-corruption representation and warranty referencing the major "
            "applicable statutes. Mutual and appropriately scoped."
        ),
        "suggested_edit": None,
    },
    {
        "id": "clause_038",
        "difficulty": "easy",
        "clause_text": (
            "Upon any change of control of the Vendor, whether by merger, acquisition, "
            "reorganization, or sale of substantially all assets, the Vendor shall provide "
            "written notice to the Client within fifteen (15) business days. The Client "
            "shall have the right to terminate this Agreement upon sixty (60) days' "
            "written notice following such change of control, without penalty."
        ),
        "clause_type": "assignment_and_change_of_control",
        "risk_level": "low",
        "issues": [],
        "explanation": (
            "Balanced change-of-control provision giving the Client a termination right "
            "with reasonable notice. The 15-day notification window is practical."
        ),
        "suggested_edit": None,
    },

    # ── NEW MEDIUM (39-46): clear issues, high risk ─────────────────────────
    {
        "id": "clause_039",
        "difficulty": "medium",
        "clause_text": (
            "The Client may assign this Agreement freely to any third party without "
            "notice to or consent of the Vendor. The Vendor may not assign this Agreement "
            "or any rights hereunder without the Client's prior written consent. Any "
            "change of control of the Vendor, including any merger, acquisition, or sale "
            "of assets exceeding 25% of the Vendor's total assets, shall constitute an "
            "assignment requiring the Client's consent."
        ),
        "clause_type": "assignment_and_change_of_control",
        "risk_level": "high",
        "issues": [
            "completely_asymmetric_assignment_rights",
            "low_asset_threshold_for_change_of_control",
            "no_notice_to_vendor_on_client_assignment",
        ],
        "explanation": (
            "The Client can assign without any notice, but the Vendor needs consent for "
            "everything including partial asset sales above 25%. This creates a major "
            "power imbalance and the low asset threshold could be triggered by routine "
            "business transactions."
        ),
        "suggested_edit": (
            "Both parties may assign to affiliates or successors without consent. "
            "Assignment to unrelated third parties requires consent, not to be "
            "unreasonably withheld. Change of control threshold should be raised to 50% "
            "of voting interests and applied mutually."
        ),
    },
    {
        "id": "clause_040",
        "difficulty": "medium",
        "clause_text": (
            "The Vendor represents and warrants that: (a) it has all necessary rights to "
            "provide the services and deliverables; (b) the services will not infringe "
            "any third-party intellectual property rights; (c) no litigation, arbitration, "
            "or governmental investigation is pending or threatened against the Vendor "
            "that could materially affect its ability to perform; and (d) ALL INFORMATION "
            "PROVIDED BY THE VENDOR IN CONNECTION WITH THIS AGREEMENT, INCLUDING ANY "
            "FINANCIAL STATEMENTS, PROJECTIONS, OR TECHNICAL SPECIFICATIONS, IS AND SHALL "
            "REMAIN TRUE, ACCURATE, AND COMPLETE IN ALL RESPECTS."
        ),
        "clause_type": "representations_and_warranties",
        "risk_level": "high",
        "issues": [
            "absolute_accuracy_warranty_on_projections",
            "forward_looking_statements_cannot_be_warranted",
            "no_materiality_qualifier_on_accuracy",
        ],
        "explanation": (
            "Sub-clause (d) warrants that projections and forward-looking statements "
            "'shall remain' true and accurate, which is impossible to guarantee. Financial "
            "projections are inherently uncertain. The lack of a materiality qualifier "
            "means even trivial inaccuracies could constitute a breach."
        ),
        "suggested_edit": (
            "Modify (d) to: 'All information provided by the Vendor is true, accurate, "
            "and complete in all material respects as of the date provided. Financial "
            "projections represent the Vendor's good-faith estimates based on assumptions "
            "believed to be reasonable at the time, but are not guarantees of future "
            "performance.'"
        ),
    },
    {
        "id": "clause_041",
        "difficulty": "medium",
        "clause_text": (
            "The Client shall have the right to audit the Vendor's records, systems, "
            "facilities, and personnel at any time and without prior notice. Audits may "
            "be conducted by the Client's employees, agents, or third-party auditors "
            "selected at the Client's sole discretion. The Vendor shall bear all costs "
            "associated with such audits, including the fees of third-party auditors. "
            "The Vendor shall make all employees available for interviews during any audit."
        ),
        "clause_type": "audit_rights",
        "risk_level": "high",
        "issues": [
            "no_notice_requirement",
            "unlimited_audit_frequency",
            "vendor_bears_all_costs",
            "mandatory_employee_interviews",
        ],
        "explanation": (
            "Unlimited, no-notice audit rights with all costs borne by the Vendor is "
            "extremely burdensome. Mandatory employee interviews with no scheduling "
            "constraints could disrupt operations. Third-party auditor selection at "
            "Client's sole discretion raises conflict-of-interest concerns."
        ),
        "suggested_edit": (
            "Audits shall be conducted no more than twice per year with at least fifteen "
            "(15) business days' advance notice. Each party bears its own audit costs "
            "unless the audit reveals a material breach, in which case the Vendor shall "
            "reimburse reasonable audit costs. Employee interviews shall be scheduled at "
            "mutually convenient times."
        ),
    },
    {
        "id": "clause_042",
        "difficulty": "medium",
        "clause_text": (
            "The Vendor shall maintain the following minimum insurance coverage: "
            "(a) commercial general liability of $10,000,000 per occurrence; "
            "(b) professional liability of $10,000,000 per claim; (c) cyber liability "
            "of $25,000,000 per occurrence; (d) crime/fidelity insurance of $5,000,000; "
            "and (e) umbrella/excess liability of $25,000,000. The Vendor shall not "
            "modify, cancel, or allow any policy to lapse without sixty (60) days' "
            "prior written approval from the Client."
        ),
        "clause_type": "insurance_requirements",
        "risk_level": "high",
        "issues": [
            "disproportionate_coverage_amounts",
            "client_approval_for_policy_changes",
            "cost_burden_may_be_prohibitive",
        ],
        "explanation": (
            "$75M+ in combined insurance coverage is disproportionate for most service "
            "agreements and could be cost-prohibitive for mid-size vendors. Requiring "
            "Client approval before modifying any policy gives the Client inappropriate "
            "control over the Vendor's insurance program."
        ),
        "suggested_edit": (
            "Reduce coverage to amounts proportionate to the agreement value: CGL $2M, "
            "professional liability $2M, cyber liability $5M. Remove crime/fidelity "
            "unless handling Client funds. Replace approval requirement with notification: "
            "'Vendor shall notify Client within ten (10) days of any material change to "
            "coverage.'"
        ),
    },
    {
        "id": "clause_043",
        "difficulty": "medium",
        "clause_text": (
            "THE VENDOR AGREES THAT THE CLIENT SHALL RECEIVE MOST FAVORED NATION "
            "PRICING AT ALL TIMES. IF THE VENDOR OFFERS OR PROVIDES ANY PRODUCT, "
            "SERVICE, OR COMBINATION THEREOF TO ANY THIRD PARTY AT A LOWER EFFECTIVE "
            "PRICE, THE VENDOR SHALL IMMEDIATELY AND RETROACTIVELY ADJUST THE CLIENT'S "
            "PRICING TO MATCH, AND SHALL REFUND ANY OVERPAYMENT WITHIN TEN (10) BUSINESS "
            "DAYS. FOR PURPOSES OF THIS CLAUSE, 'EFFECTIVE PRICE' SHALL INCLUDE ALL "
            "DISCOUNTS, CREDITS, REBATES, AND PROMOTIONAL OFFERS."
        ),
        "clause_type": "most_favored_nation",
        "risk_level": "high",
        "issues": [
            "retroactive_price_adjustment",
            "no_comparability_requirement",
            "includes_promotional_pricing",
            "immediate_refund_obligation",
        ],
        "explanation": (
            "This MFN clause has no requirement that the third-party deal be comparable "
            "in scope, volume, or term. Including promotional offers and one-time "
            "discounts would force retroactive adjustments for deals that are not truly "
            "comparable. The immediate retroactive refund obligation is operationally "
            "burdensome and could be financially destabilizing."
        ),
        "suggested_edit": (
            "Limit MFN to substantially similar services in comparable volume and term. "
            "Exclude promotional, introductory, and volume-based pricing. Provide "
            "prospective (not retroactive) adjustment with thirty (30) days' notice. "
            "Require Client to demonstrate the comparable pricing before adjustment."
        ),
    },
    {
        "id": "clause_044",
        "difficulty": "medium",
        "clause_text": (
            "The Vendor represents and warrants that: (a) it is not currently debarred, "
            "suspended, or proposed for debarment by any governmental entity; (b) it is "
            "in compliance with all applicable sanctions and export control laws; and "
            "(c) no person or entity holding a direct or indirect ownership interest in "
            "the Vendor is listed on any governmental restricted party list. THE VENDOR "
            "SHALL INDEMNIFY THE CLIENT FOR ANY AND ALL LOSSES ARISING FROM ANY BREACH "
            "OF THESE REPRESENTATIONS, WITHOUT LIMITATION AS TO AMOUNT OR TIME."
        ),
        "clause_type": "representations_and_warranties",
        "risk_level": "high",
        "issues": [
            "unlimited_indemnity_for_reps_breach",
            "indirect_ownership_scope_too_broad",
            "no_knowledge_qualifier",
        ],
        "explanation": (
            "The unlimited indemnity for any breach of these reps is disproportionate. "
            "The 'indirect ownership interest' language could extend to passive minority "
            "investors the Vendor cannot control or monitor. There is no 'to the Vendor's "
            "knowledge' qualifier, making the Vendor strictly liable for facts it may not "
            "be able to verify."
        ),
        "suggested_edit": (
            "Add 'to the Vendor's knowledge after reasonable inquiry' to reps (a)-(c). "
            "Limit indirect ownership to persons holding 10% or more. Cap the indemnity "
            "at the total agreement value or include it within the general liability cap."
        ),
    },
    {
        "id": "clause_045",
        "difficulty": "medium",
        "clause_text": (
            "The Client shall have the right to audit the Vendor's compliance with data "
            "protection obligations under this Agreement. If any audit reveals a material "
            "deficiency, the Vendor shall remediate such deficiency at its sole cost "
            "within five (5) business days. Failure to remediate within such period shall "
            "constitute a material breach entitling the Client to immediate termination "
            "and full recovery of all fees paid under this Agreement."
        ),
        "clause_type": "audit_rights",
        "risk_level": "high",
        "issues": [
            "unreasonably_short_remediation_period",
            "automatic_material_breach",
            "full_fee_recovery_disproportionate",
        ],
        "explanation": (
            "Five business days is unreasonably short to remediate material data "
            "protection deficiencies, which may require system redesign. Automatic "
            "material breach after such a short period, coupled with full fee recovery, "
            "creates an outsized penalty that could be used as leverage."
        ),
        "suggested_edit": (
            "Extend remediation to thirty (30) days for material deficiencies, with a "
            "mutually agreed remediation plan. Remove automatic breach; instead, allow "
            "termination only if the Vendor fails to present a credible remediation plan "
            "within fifteen (15) days. Limit recovery to fees attributable to the "
            "non-compliant services."
        ),
    },
    {
        "id": "clause_046",
        "difficulty": "medium",
        "clause_text": (
            "During the term and for twenty-four (24) months thereafter, neither party "
            "shall directly or indirectly solicit for employment any employee of the other "
            "party. For purposes of this clause, 'employee' includes full-time, part-time, "
            "and contract personnel, and 'indirect solicitation' includes posting job "
            "advertisements on general-purpose job boards where such employees may see them."
        ),
        "clause_type": "non_compete",
        "risk_level": "high",
        "issues": [
            "general_job_postings_treated_as_solicitation",
            "contract_personnel_included",
            "24_month_survival_excessive",
        ],
        "explanation": (
            "Treating general job board postings as indirect solicitation is overbroad and "
            "likely unenforceable -- it would effectively prevent both parties from "
            "advertising open positions. Including contract personnel extends the "
            "restriction to people neither party may be able to control. The 24-month "
            "post-term period is longer than typical."
        ),
        "suggested_edit": (
            "Limit non-solicitation to direct, targeted solicitation of employees with "
            "whom the soliciting party had material contact during the engagement. Exclude "
            "general job advertisements. Limit to full-time employees and reduce the "
            "post-term period to twelve (12) months."
        ),
    },

    # ── NEW HARD (47-55): subtle/adversarial issues requiring legal reasoning
    {
        "id": "clause_047",
        "difficulty": "hard",
        "clause_text": (
            "The Vendor shall indemnify the Client against all claims arising from the "
            "Vendor's breach of this Agreement, subject to the limitation of liability "
            "set forth in Section 8. Notwithstanding Section 8, the Vendor's liability "
            "for indemnification claims shall not be subject to any cap or exclusion. "
            "For the avoidance of doubt, Section 8 shall apply to all claims other than "
            "indemnification claims. In the event of any conflict between this Section "
            "and Section 8, this Section shall control, except with respect to claims "
            "arising under Section 12 (Confidentiality), which shall be governed by "
            "Section 8."
        ),
        "clause_type": "indemnification",
        "risk_level": "high",
        "issues": [
            "circular_cross_references",
            "contradictory_carveout_structure",
            "indemnification_effectively_uncapped",
            "ambiguous_priority_of_provisions",
        ],
        "explanation": (
            "This clause first subjects indemnification to Section 8's liability cap, "
            "then immediately removes that cap, then reinstates it for confidentiality-"
            "related indemnification. The circular cross-references create ambiguity: "
            "a data breach could be both an indemnification claim (uncapped) and a "
            "confidentiality claim (capped), with no clear resolution. This is a classic "
            "adversarial drafting pattern designed to appear balanced while creating "
            "uncapped exposure."
        ),
        "suggested_edit": (
            "Consolidate into a single, clear hierarchy: 'The Vendor's aggregate "
            "indemnification liability shall not exceed 2x the annual fees paid, except "
            "for (i) IP infringement claims, capped at 3x annual fees, and (ii) willful "
            "misconduct, which shall be uncapped. All other claims are subject to the "
            "general liability cap in Section 8.'"
        ),
    },
    {
        "id": "clause_048",
        "difficulty": "hard",
        "clause_text": (
            "This Agreement may not be assigned by either party without the prior written "
            "consent of the other party. Notwithstanding the foregoing, either party may "
            "assign this Agreement to (a) any affiliate, or (b) any successor in "
            "connection with a merger, acquisition, or sale of all or substantially all "
            "of its assets, provided that the assignee assumes all obligations hereunder. "
            "For purposes of this clause, 'affiliate' means any entity that directly or "
            "indirectly controls, is controlled by, or is under common control with a "
            "party, where 'control' means ownership of 10% or more of the voting "
            "securities of such entity."
        ),
        "clause_type": "assignment_and_change_of_control",
        "risk_level": "high",
        "issues": [
            "low_control_threshold_expands_affiliate_definition",
            "affiliate_assignment_without_financial_vetting",
            "shell_entity_risk",
        ],
        "explanation": (
            "The 10% ownership threshold for 'control' is far below the standard 50%. "
            "This means a party could assign the agreement to an entity in which it holds "
            "only a 10% stake -- effectively a third party -- without the other side's "
            "consent. This creates a loophole where assignment to near-strangers is "
            "disguised as an affiliate transfer. A party could set up a thinly-capitalized "
            "shell entity with 10% ownership and transfer obligations there."
        ),
        "suggested_edit": (
            "Increase the control threshold to 50% or more of voting securities, which "
            "is the standard definition. Add: 'The assignee must demonstrate financial "
            "capacity to perform all obligations. Assignment to a newly formed entity "
            "requires the assigning party to guarantee the assignee's obligations for a "
            "period of twelve (12) months.'"
        ),
    },
    {
        "id": "clause_049",
        "difficulty": "hard",
        "clause_text": (
            "The Vendor represents and warrants that: (i) it owns or has all necessary "
            "licenses to all intellectual property used in the deliverables; (ii) the "
            "deliverables will not infringe any third-party rights; (iii) it has not "
            "received notice of any claim of infringement; and (iv) in the event any "
            "deliverable is held to infringe, the Vendor shall, at its option, "
            "(A) procure the right for Client to continue using the deliverable, "
            "(B) modify the deliverable to be non-infringing, or (C) accept return of "
            "the deliverable and refund fees paid, less a reasonable allowance for "
            "Client's prior use. THE REMEDIES SET FORTH IN CLAUSE (iv) SHALL BE THE "
            "CLIENT'S SOLE AND EXCLUSIVE REMEDY FOR ANY INTELLECTUAL PROPERTY "
            "INFRINGEMENT CLAIM."
        ),
        "clause_type": "representations_and_warranties",
        "risk_level": "high",
        "issues": [
            "exclusive_remedy_undercuts_ip_warranty",
            "depreciation_deduction_from_refund",
            "vendor_chooses_remedy",
            "no_coverage_for_consequential_ip_damages",
        ],
        "explanation": (
            "The strong IP representations in (i)-(iii) appear protective, but the "
            "exclusive remedy in (iv) dramatically limits their value. The Vendor can "
            "choose the cheapest remedy, and option (C) deducts a 'reasonable allowance' "
            "for prior use, meaning the Client could receive minimal refund. The "
            "exclusive remedy clause at the end means the Client cannot recover any "
            "consequential damages (lost profits, switching costs, business disruption) "
            "from an IP infringement -- even if the Vendor knew of the infringement. "
            "This is a poison pill hidden behind strong-looking warranties."
        ),
        "suggested_edit": (
            "Remove 'sole and exclusive remedy' language to preserve general remedies. "
            "If an exclusive remedy is required, remove the use deduction from refunds "
            "and add: 'If none of the above remedies are commercially feasible within "
            "sixty (60) days, Client may pursue all available remedies at law or equity, "
            "including consequential damages for knowing infringement.'"
        ),
    },
    {
        "id": "clause_050",
        "difficulty": "hard",
        "clause_text": (
            "The Client shall have the right to audit the Vendor's compliance with "
            "this Agreement, including inspection of source code, security systems, "
            "financial records, and personnel files. The Vendor shall cooperate fully "
            "with all audit requests. Notwithstanding the foregoing, the Vendor may "
            "decline an audit request if it reasonably determines that the audit would "
            "compromise the security or confidentiality of its systems or the data of "
            "its other clients. In such cases, the Vendor shall propose an alternative "
            "audit procedure. If the parties cannot agree on an alternative procedure "
            "within ten (10) business days, the Vendor's determination shall be final "
            "and binding."
        ),
        "clause_type": "audit_rights",
        "risk_level": "high",
        "issues": [
            "vendor_veto_effectively_nullifies_audit_right",
            "subjective_security_determination",
            "vendor_has_final_say_on_disputes",
        ],
        "explanation": (
            "This clause appears to grant robust audit rights, but the exception "
            "effectively nullifies them. The Vendor can decline any audit by claiming "
            "security concerns -- a subjective determination -- and if the parties "
            "cannot agree on an alternative, the Vendor's decision is final. This nested "
            "exception structure means the Client has no enforceable audit right. The "
            "Vendor can always construct a plausible security rationale."
        ),
        "suggested_edit": (
            "Replace the Vendor's final determination with independent arbitration: "
            "'Disputes regarding audit procedures shall be resolved by an independent "
            "third-party security assessor mutually selected by the parties.' Add: "
            "'The Vendor may not unreasonably or repeatedly invoke security concerns to "
            "avoid audit. Failure to permit any audit within a twelve-month period "
            "constitutes a material breach.'"
        ),
    },
    {
        "id": "clause_051",
        "difficulty": "hard",
        "clause_text": (
            "Either party may terminate this Agreement for cause upon thirty (30) days' "
            "written notice if the other party materially breaches this Agreement and "
            "fails to cure such breach within the notice period. Additionally, the Client "
            "may terminate this Agreement immediately upon written notice if: (a) the "
            "Vendor undergoes a change of control; (b) the Vendor fails to meet any "
            "service level for two (2) consecutive months; or (c) in the Client's "
            "reasonable judgment, the Vendor's financial condition creates a material risk "
            "to service continuity. Upon any termination by the Client under this "
            "paragraph, the Vendor shall refund all pre-paid fees and pay a termination "
            "assistance fee equal to three (3) months' charges."
        ),
        "clause_type": "termination",
        "risk_level": "high",
        "issues": [
            "subjective_financial_condition_trigger",
            "vendor_pays_penalty_on_client_termination",
            "change_of_control_as_immediate_termination_trigger",
            "combined_termination_and_financial_penalty",
        ],
        "explanation": (
            "Sub-clause (c) allows the Client to terminate based on its own subjective "
            "judgment of the Vendor's financial health -- this is essentially a "
            "termination-for-convenience disguised as termination-for-cause. The Vendor "
            "not only loses the contract but must pay three months' fees as a penalty "
            "plus refund pre-paid amounts. Combined with the change-of-control trigger, "
            "this clause gives the Client maximum leverage to exit at any time while "
            "extracting payment from the Vendor."
        ),
        "suggested_edit": (
            "Replace subjective financial judgment with objective criteria: 'the Vendor "
            "becomes insolvent, files for bankruptcy, or has a credit rating downgrade "
            "below investment grade.' Remove the termination assistance fee for "
            "convenience-like terminations. Apply the refund only to pre-paid fees for "
            "services not yet rendered."
        ),
    },
    {
        "id": "clause_052",
        "difficulty": "hard",
        "clause_text": (
            "IN NO EVENT SHALL THE AGGREGATE LIABILITY OF EITHER PARTY EXCEED THE TOTAL "
            "FEES PAID OR PAYABLE UNDER THIS AGREEMENT IN THE TWELVE (12) MONTHS "
            "PRECEDING THE EVENT GIVING RISE TO THE CLAIM. THE FOREGOING LIMITATION "
            "SHALL NOT APPLY TO: (A) EITHER PARTY'S INDEMNIFICATION OBLIGATIONS; "
            "(B) BREACHES OF CONFIDENTIALITY; (C) EITHER PARTY'S GROSS NEGLIGENCE OR "
            "WILLFUL MISCONDUCT; (D) VIOLATIONS OF APPLICABLE LAW; (E) THE VENDOR'S "
            "DATA PROTECTION OBLIGATIONS; OR (F) BREACHES OF THE INTELLECTUAL PROPERTY "
            "PROVISIONS. NOTWITHSTANDING THE FOREGOING, IN NO EVENT SHALL THE VENDOR'S "
            "LIABILITY FOR ANY EXCLUDED CATEGORY EXCEED THREE TIMES (3X) THE ANNUAL FEES."
        ),
        "clause_type": "limitation_of_liability",
        "risk_level": "high",
        "issues": [
            "carveouts_swallow_the_cap",
            "super_cap_only_applies_to_vendor",
            "asymmetric_super_cap_structure",
            "virtually_all_serious_claims_excluded",
        ],
        "explanation": (
            "The carveouts (A)-(F) cover nearly every category of serious claim, making "
            "the base cap largely decorative. The critical subtlety is that the 3x "
            "super-cap only applies to the Vendor -- the Client's liability for these "
            "same excluded categories remains truly unlimited. This asymmetry is buried "
            "in the 'VENDOR'S LIABILITY' language of the final sentence. A casual reader "
            "would assume the mutual framing ('EITHER PARTY') extends to the super-cap."
        ),
        "suggested_edit": (
            "Apply the super-cap mutually: 'Neither party's liability for any excluded "
            "category shall exceed 3x the annual fees.' Reduce the number of carveouts "
            "to the most critical: willful misconduct and IP infringement. Move other "
            "categories under the general cap with a 2x multiplier."
        ),
    },
    {
        "id": "clause_053",
        "difficulty": "hard",
        "clause_text": (
            "The Vendor shall maintain Most Favored Nation pricing as follows: the fees "
            "charged to the Client shall be no less favorable than those offered to any "
            "similarly situated customer. 'Similarly situated' shall mean any customer "
            "purchasing substantially similar services. Notwithstanding the foregoing, "
            "the Vendor may offer lower pricing to (a) governmental entities, "
            "(b) nonprofit organizations, (c) customers committing to terms of three (3) "
            "years or more, (d) customers purchasing bundled services, (e) customers "
            "with annual spend exceeding $5,000,000, or (f) customers receiving "
            "promotional or introductory pricing. The Vendor shall certify compliance "
            "annually."
        ),
        "clause_type": "most_favored_nation",
        "risk_level": "medium",
        "issues": [
            "exceptions_effectively_nullify_mfn",
            "virtually_all_lower_pricing_excused",
            "annual_certification_is_self_serving",
        ],
        "explanation": (
            "The exceptions in (a)-(f) are so broad that they cover nearly every scenario "
            "in which a vendor would offer lower pricing. Government, nonprofit, long-term, "
            "bundled, high-volume, and promotional deals collectively account for the vast "
            "majority of discounting situations. The MFN right appears valuable but is "
            "functionally empty. The annual self-certification provides no real "
            "enforcement mechanism."
        ),
        "suggested_edit": (
            "Reduce exceptions to only (a) governmental entities and (b) nonprofit "
            "organizations. Remove bundled, volume, long-term, and promotional exceptions, "
            "or require that the Client receive equivalent volume or term discounts. "
            "Replace self-certification with audit rights: 'The Client may audit the "
            "Vendor's pricing records once per year to verify MFN compliance.'"
        ),
    },
    {
        "id": "clause_054",
        "difficulty": "hard",
        "clause_text": (
            "The Contractor shall maintain errors and omissions insurance with a minimum "
            "limit of $10,000,000 per claim throughout the term and for three (3) years "
            "following termination. The Contractor's policy shall name the Client as an "
            "additional insured with a waiver of subrogation in favor of the Client. The "
            "Contractor shall not settle any claim that could result in liability to the "
            "Client or admission of fault without the Client's prior written consent. "
            "The Contractor's obligation to maintain insurance shall survive termination "
            "regardless of the reason for termination. ANY FAILURE TO MAINTAIN THE "
            "REQUIRED INSURANCE SHALL CONSTITUTE A MATERIAL BREACH ENTITLING THE CLIENT "
            "TO IMMEDIATE TERMINATION AND RECOVERY OF ALL FEES PAID UNDER THIS AGREEMENT."
        ),
        "clause_type": "insurance_requirements",
        "risk_level": "high",
        "issues": [
            "additional_insured_on_eo_policy_unusual",
            "waiver_of_subrogation_reduces_contractor_protection",
            "post_termination_insurance_obligation_unfunded",
            "disproportionate_breach_remedy",
            "client_controls_claim_settlement",
        ],
        "explanation": (
            "Adding the Client as additional insured on an E&O policy is non-standard "
            "and most insurers will not permit it (E&O covers the insured's own "
            "professional negligence, not third parties). The waiver of subrogation "
            "prevents the Contractor's insurer from recovering from the Client, even if "
            "the Client contributed to the loss. The 3-year post-termination insurance "
            "requirement imposes significant unfunded costs. The remedy for lapsed "
            "insurance -- full fee recovery -- is grossly disproportionate and could be "
            "used opportunistically."
        ),
        "suggested_edit": (
            "Replace additional insured with a certificate of insurance requirement. "
            "Remove waiver of subrogation. Reduce post-termination tail to one (1) year. "
            "Change breach remedy to: 'The Contractor shall have fifteen (15) days to "
            "cure any insurance lapse. Failure to cure entitles the Client to suspend "
            "payment obligations until coverage is restored.'"
        ),
    },
    {
        "id": "clause_055",
        "difficulty": "hard",
        "clause_text": (
            "During the term of this Agreement and for a period of twelve (12) months "
            "following termination, the Employee shall not, directly or indirectly, "
            "(a) provide services to any Competing Business within the Restricted "
            "Territory, or (b) solicit any Client Customer. 'Competing Business' means "
            "any entity engaged in any business in which the Company has been engaged, "
            "has planned to engage, or has investigated the possibility of engaging "
            "during the Employee's tenure. 'Restricted Territory' means any geographic "
            "area in which the Company conducts or has conducted business. "
            "Notwithstanding the foregoing, this Section shall not restrict the Employee "
            "from owning up to 1% of the outstanding securities of any publicly traded "
            "company. In the event of any breach, the Employee agrees that damages would "
            "be difficult to ascertain and that the Company shall be entitled to "
            "injunctive relief without the necessity of posting bond."
        ),
        "clause_type": "non_compete",
        "risk_level": "high",
        "issues": [
            "competing_business_includes_planned_and_investigated",
            "effectively_unlimited_scope",
            "geographic_scope_follows_company_not_employee",
            "injunctive_relief_without_bond",
            "passive_investment_threshold_too_low",
        ],
        "explanation": (
            "The definition of 'Competing Business' extends to businesses the Company "
            "has merely 'investigated the possibility of engaging' in -- this could "
            "encompass virtually any industry if the Company has broad exploratory "
            "activities. Combined with the expansive geographic definition tied to "
            "anywhere the Company has ever done business, this non-compete could prevent "
            "the Employee from working almost anywhere in their field. The 1% passive "
            "investment exception is too narrow (industry standard is 5%). The no-bond "
            "injunctive relief clause, while common, removes an important judicial "
            "safeguard."
        ),
        "suggested_edit": (
            "Narrow 'Competing Business' to: 'entities whose primary business directly "
            "competes with the Company's products or services that the Employee "
            "materially contributed to during the final twenty-four (24) months of "
            "employment.' Limit territory to metropolitan areas where the Employee "
            "worked. Increase passive investment threshold to 5%. Remove no-bond "
            "provision or replace with: 'upon posting of reasonable security as "
            "determined by the court.'"
        ),
    },
]
# fmt: on


CONTEXT_DATA: Dict[str, Dict[str, str]] = {
    # ── EASY scenarios ───────────────────────────────────────────────────
    "clause_001": {
        "contract_type": "Master Services Agreement",
        "parties": "TechCorp Inc. (Client) and CloudSoft LLC (Vendor)",
        "jurisdiction": "Delaware, USA",
        "contract_value": "$500,000 annual",
        "other_clauses_summary": (
            "Standard MSA with mutual confidentiality, 12-month term, "
            "SOW-based pricing."
        ),
    },
    "clause_002": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Retail Dynamics Corp. (Client) and PlatformOne Inc. (Vendor)",
        "jurisdiction": "California, USA",
        "contract_value": "$250,000 annual",
        "other_clauses_summary": (
            "3-year SaaS agreement with annual auto-renewal, 99.9% SLA, "
            "standard data processing addendum."
        ),
    },
    "clause_003": {
        "contract_type": "Consulting Agreement",
        "parties": "GreenEnergy Solutions (Client) and Apex Advisors LLC (Consultant)",
        "jurisdiction": "New York, USA",
        "contract_value": "$150,000 fixed fee",
        "other_clauses_summary": (
            "6-month consulting engagement for ERP implementation, "
            "milestone-based payments, mutual NDA incorporated by reference."
        ),
    },
    "clause_004": {
        "contract_type": "Non-Disclosure Agreement",
        "parties": "BioGen Therapeutics (Disclosing Party) and Pharma Research Ltd. (Receiving Party)",
        "jurisdiction": "Massachusetts, USA",
        "contract_value": "N/A (mutual NDA, no fees)",
        "other_clauses_summary": (
            "Mutual NDA for due diligence in potential acquisition. "
            "Covers technical data, financial records, and patient data."
        ),
    },
    "clause_005": {
        "contract_type": "IP License Agreement",
        "parties": "InnovateTech Holdings (Licensor) and SmartDevices Inc. (Licensee)",
        "jurisdiction": "Delaware, USA",
        "contract_value": "$2,000,000 upfront + 3% royalty",
        "other_clauses_summary": (
            "Exclusive patent license for IoT sensor technology, "
            "5-year term, field-of-use limited to consumer electronics."
        ),
    },
    "clause_006": {
        "contract_type": "Master Services Agreement",
        "parties": "Global Logistics Corp. (Client) and FastFreight Systems (Vendor)",
        "jurisdiction": "Illinois, USA",
        "contract_value": "$1,200,000 annual",
        "other_clauses_summary": (
            "Managed logistics platform with dedicated support team, "
            "volume-based pricing tiers, quarterly business reviews."
        ),
    },
    "clause_007": {
        "contract_type": "Consulting Agreement",
        "parties": "Meridian Financial Group (Client) and StrategyWorks LLC (Consultant)",
        "jurisdiction": "New York, USA",
        "contract_value": "$300,000 fixed fee",
        "other_clauses_summary": (
            "Strategic advisory engagement for M&A target evaluation, "
            "success fee structure, 9-month term."
        ),
    },
    "clause_008": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "HealthFirst Insurance (Client) and CloudCare Platform Inc. (Vendor)",
        "jurisdiction": "Texas, USA",
        "contract_value": "$800,000 annual",
        "other_clauses_summary": (
            "Claims processing platform with HIPAA BAA, "
            "99.95% uptime SLA, disaster recovery provisions."
        ),
    },
    "clause_009": {
        "contract_type": "Consulting Agreement",
        "parties": "NovaStar Media (Client) and PixelForge Studios (Contractor)",
        "jurisdiction": "California, USA",
        "contract_value": "$175,000 project-based",
        "other_clauses_summary": (
            "Creative services engagement for brand refresh, "
            "deliverable-based milestones, pre-existing IP schedule attached."
        ),
    },
    "clause_010": {
        "contract_type": "Master Services Agreement",
        "parties": "Atlas Manufacturing Inc. (Client) and PrecisionTech Solutions (Vendor)",
        "jurisdiction": "Ohio, USA",
        "contract_value": "$650,000 annual",
        "other_clauses_summary": (
            "Industrial automation services with on-site support, "
            "equipment maintenance schedule, safety compliance requirements."
        ),
    },
    # ── MEDIUM scenarios ─────────────────────────────────────────────────
    "clause_011": {
        "contract_type": "Construction Services Agreement",
        "parties": "Skyline Development Corp. (Owner) and BuildRight Contractors LLC (Contractor)",
        "jurisdiction": "Florida, USA",
        "contract_value": "$5,000,000 project total",
        "other_clauses_summary": (
            "Commercial building construction, cost-plus pricing with GMP, "
            "18-month schedule, performance bond required."
        ),
    },
    "clause_012": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "DataVault Analytics (Client) and QuickDeploy Software Inc. (Vendor)",
        "jurisdiction": "Washington, USA",
        "contract_value": "$45,000 annual",
        "other_clauses_summary": (
            "Small-business analytics tool subscription, "
            "month-to-month after initial term, limited support tier."
        ),
    },
    "clause_013": {
        "contract_type": "Independent Contractor Agreement",
        "parties": "BrightPath Education Inc. (Company) and Dr. Sarah Chen (Contractor)",
        "jurisdiction": "Colorado, USA",
        "contract_value": "$120,000 annual retainer",
        "other_clauses_summary": (
            "Curriculum development services, weekly deliverables, "
            "contractor provides own equipment and sets own hours."
        ),
    },
    "clause_014": {
        "contract_type": "Non-Disclosure Agreement",
        "parties": "QuantumLeap AI (Disclosing Party) and VentureScale Capital (Receiving Party)",
        "jurisdiction": "California, USA",
        "contract_value": "N/A (unilateral NDA for fundraising)",
        "other_clauses_summary": (
            "One-way NDA for Series B due diligence, covers proprietary "
            "algorithms, training data sources, and financial projections."
        ),
    },
    "clause_015": {
        "contract_type": "Independent Contractor Agreement",
        "parties": "RoboTech Industries (Company) and Elena Martinez, PhD (Contractor)",
        "jurisdiction": "California, USA",
        "contract_value": "$200/hour, estimated $350,000",
        "other_clauses_summary": (
            "AI/ML research and development engagement, "
            "SOW-based deliverables, pre-existing IP schedule required."
        ),
    },
    "clause_016": {
        "contract_type": "Employment Agreement",
        "parties": "Pinnacle Consulting Group (Company) and James K. Whitfield (Employee)",
        "jurisdiction": "New York, USA",
        "contract_value": "$185,000 annual salary + bonus",
        "other_clauses_summary": (
            "Senior consultant employment with non-solicit, "
            "equity vesting schedule, 2-year minimum commitment."
        ),
    },
    "clause_017": {
        "contract_type": "Managed IT Services Agreement",
        "parties": "Heritage Law Firm LLP (Client) and SecureNet IT Solutions (Vendor)",
        "jurisdiction": "Virginia, USA",
        "contract_value": "$96,000 annual",
        "other_clauses_summary": (
            "Full IT outsourcing for 40-person law firm, "
            "includes hardware procurement, helpdesk, and cybersecurity monitoring."
        ),
    },
    "clause_018": {
        "contract_type": "Custom Software Development Agreement",
        "parties": "TradeFlow Markets (Client) and CodeForge Development Inc. (Vendor)",
        "jurisdiction": "New York, USA",
        "contract_value": "$750,000 project total",
        "other_clauses_summary": (
            "Bespoke trading platform development, agile delivery methodology, "
            "phased acceptance testing, escrow for source code."
        ),
    },
    "clause_019": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "EuroRetail GmbH (Client) and DataStream Analytics Inc. (Vendor)",
        "jurisdiction": "Germany (with GDPR applicability)",
        "contract_value": "EUR 400,000 annual",
        "other_clauses_summary": (
            "Customer analytics platform processing EU consumer data, "
            "Standard Contractual Clauses for international transfers, "
            "Data Processing Addendum attached."
        ),
    },
    "clause_020": {
        "contract_type": "Master Services Agreement",
        "parties": "OceanView Resorts International (Client) and TravelTech Solutions (Vendor)",
        "jurisdiction": "Nevada, USA",
        "contract_value": "$1,500,000 annual",
        "other_clauses_summary": (
            "Hospitality management platform with PCI-DSS compliance, "
            "multi-property rollout schedule, 24/7 support SLA."
        ),
    },
    # ── HARD scenarios ───────────────────────────────────────────────────
    "clause_021": {
        "contract_type": "Master Services Agreement",
        "parties": "FortressBank N.A. (Client) and CyberShield Security Corp. (Contractor)",
        "jurisdiction": "New York, USA",
        "contract_value": "$2,500,000 annual",
        "other_clauses_summary": (
            "Cybersecurity managed services for Tier 1 bank, SOC 2 compliance required, "
            "regulatory audit cooperation clause, data residency requirements."
        ),
    },
    "clause_022": {
        "contract_type": "Enterprise Software License Agreement",
        "parties": "MegaCorp Industries (Client) and EnterpriseSoft Inc. (Vendor)",
        "jurisdiction": "Delaware, USA",
        "contract_value": "$3,200,000 over 3 years",
        "other_clauses_summary": (
            "Enterprise ERP deployment with phased rollout, custom modules, "
            "dedicated support team, source code escrow, benchmark rights."
        ),
    },
    "clause_023": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "MidMarket Solutions Corp. (Client) and ScaleUp Platform Inc. (Vendor)",
        "jurisdiction": "California, USA",
        "contract_value": "$180,000 annual (initial term)",
        "other_clauses_summary": (
            "CRM platform with API integrations, data migration services included, "
            "training credits, tiered support levels."
        ),
    },
    "clause_024": {
        "contract_type": "Joint Venture Agreement",
        "parties": "AlphaPharm Inc. and BetaBio Research Ltd.",
        "jurisdiction": "Delaware, USA",
        "contract_value": "$10,000,000 combined investment",
        "other_clauses_summary": (
            "Drug development joint venture, shared IP ownership for joint inventions, "
            "stage-gate funding commitments, regulatory filing responsibilities split."
        ),
    },
    "clause_025": {
        "contract_type": "Independent Contractor Agreement",
        "parties": "NeuralNet Dynamics (Company) and Dr. Anika Patel (Contractor)",
        "jurisdiction": "California, USA",
        "contract_value": "$250/hour, estimated $500,000",
        "other_clauses_summary": (
            "Machine learning model development, 12-month engagement, "
            "pre-existing IP schedule lists 3 open-source frameworks created by Contractor."
        ),
    },
    "clause_026": {
        "contract_type": "Employment Agreement",
        "parties": "Vanguard Wealth Advisors LLC (Company) and Marcus T. Reynolds (Employee)",
        "jurisdiction": "Connecticut, USA",
        "contract_value": "$275,000 annual salary + carried interest",
        "other_clauses_summary": (
            "Senior portfolio manager employment, book-of-business provisions, "
            "deferred compensation plan, garden leave clause."
        ),
    },
    "clause_027": {
        "contract_type": "Enterprise Software License Agreement",
        "parties": "Consolidated Healthcare Systems (Client) and MedTech Software Inc. (Vendor)",
        "jurisdiction": "Massachusetts, USA",
        "contract_value": "$1,800,000 over 5 years",
        "other_clauses_summary": (
            "Electronic health records platform, HIPAA BAA included, "
            "HL7/FHIR interoperability requirements, data migration from legacy system."
        ),
    },
    "clause_028": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Nordic Retail Group AS (Client) and CloudCommerce Inc. (Vendor)",
        "jurisdiction": "Norway (with GDPR applicability)",
        "contract_value": "EUR 600,000 annual",
        "other_clauses_summary": (
            "E-commerce platform processing EU/EEA customer data, "
            "Standard Contractual Clauses, sub-processor list with 12 entities, "
            "data localization in EU data centers."
        ),
    },
    "clause_029": {
        "contract_type": "IP License Agreement",
        "parties": "AsiaComm Holdings (Licensor) and PacificTech Industries (Licensee)",
        "jurisdiction": "Singapore",
        "contract_value": "$5,000,000 upfront + milestone payments",
        "other_clauses_summary": (
            "Telecommunications patent portfolio license, 47 patent families, "
            "cross-license provisions, most-favored-licensee clause, "
            "technology transfer support."
        ),
    },
    "clause_030": {
        "contract_type": "Master Services Agreement",
        "parties": "Spectrum Analytics Corp. (Company) and DataPipeline Services LLC (Contractor)",
        "jurisdiction": "Texas, USA",
        "contract_value": "$900,000 annual",
        "other_clauses_summary": (
            "Data engineering services with key-person provisions, "
            "background check requirements, change order process, "
            "quarterly performance reviews."
        ),
    },
    # ── NEW EASY scenarios ───────────────────────────────────────────────
    "clause_031": {
        "contract_type": "Master Services Agreement",
        "parties": "Beacon Healthcare Systems (Client) and NorthStar IT Services LLC (Vendor)",
        "jurisdiction": "Delaware, USA",
        "contract_value": "$720,000 annual",
        "other_clauses_summary": (
            "Managed IT services with HIPAA compliance, 24-month term, "
            "auto-renewal, standard SLA with 99.9% uptime."
        ),
    },
    "clause_032": {
        "contract_type": "Joint Venture Agreement",
        "parties": "SolarWave Energy Inc. and GridTech Power Systems LLC",
        "jurisdiction": "Delaware, USA",
        "contract_value": "$15,000,000 combined investment",
        "other_clauses_summary": (
            "Renewable energy development JV, shared governance, "
            "stage-gate investment commitments, regulatory filing split."
        ),
    },
    "clause_033": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Metroplex Financial Corp. (Client) and LedgerCloud Inc. (Vendor)",
        "jurisdiction": "New York, USA",
        "contract_value": "$340,000 annual",
        "other_clauses_summary": (
            "Cloud accounting platform with SOC 2 Type II compliance, "
            "data encryption at rest and in transit, annual penetration testing."
        ),
    },
    "clause_034": {
        "contract_type": "Consulting Agreement",
        "parties": "Ironclad Defense Corp. (Client) and TacticalOps Consulting LLC (Vendor)",
        "jurisdiction": "Virginia, USA",
        "contract_value": "$480,000 annual",
        "other_clauses_summary": (
            "Cybersecurity consulting for defense contractor, "
            "CMMC Level 3 compliance required, cleared personnel only."
        ),
    },
    "clause_035": {
        "contract_type": "Enterprise Software License Agreement",
        "parties": "Continental Logistics Group (Client) and SupplyChain Pro Inc. (Vendor)",
        "jurisdiction": "Illinois, USA",
        "contract_value": "$1,100,000 over 3 years",
        "other_clauses_summary": (
            "Supply chain management platform, multi-site deployment, "
            "API integrations with existing ERP, dedicated support engineer."
        ),
    },
    "clause_036": {
        "contract_type": "Master Services Agreement",
        "parties": "Apex Biotech Ltd. (Client) and SecureLab IT Solutions (Contractor)",
        "jurisdiction": "Massachusetts, USA",
        "contract_value": "$560,000 annual",
        "other_clauses_summary": (
            "Laboratory information management system support, "
            "FDA 21 CFR Part 11 compliance, validated environment requirements."
        ),
    },
    "clause_037": {
        "contract_type": "Distribution Agreement",
        "parties": "GlobalPharma Inc. (Supplier) and MedDistro Holdings (Distributor)",
        "jurisdiction": "New Jersey, USA",
        "contract_value": "$8,000,000 annual minimum",
        "other_clauses_summary": (
            "Pharmaceutical distribution with cold chain requirements, "
            "territory exclusivity, regulatory reporting obligations."
        ),
    },
    "clause_038": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Redwood Capital Management (Client) and PortfolioView Inc. (Vendor)",
        "jurisdiction": "Connecticut, USA",
        "contract_value": "$250,000 annual",
        "other_clauses_summary": (
            "Investment portfolio analytics platform, SEC compliance features, "
            "real-time data feeds, multi-factor authentication required."
        ),
    },
    # ── NEW MEDIUM scenarios ─────────────────────────────────────────────
    "clause_039": {
        "contract_type": "Master Services Agreement",
        "parties": "Summit Retail Group (Client) and CloudOps Managed Services (Vendor)",
        "jurisdiction": "California, USA",
        "contract_value": "$1,800,000 annual",
        "other_clauses_summary": (
            "Multi-cloud infrastructure management, PCI-DSS compliance, "
            "200+ store locations, disaster recovery SLA."
        ),
    },
    "clause_040": {
        "contract_type": "Enterprise Software License Agreement",
        "parties": "Frontier Energy Corp. (Client) and DataPlatform Solutions Inc. (Vendor)",
        "jurisdiction": "Texas, USA",
        "contract_value": "$2,400,000 over 3 years",
        "other_clauses_summary": (
            "SCADA data analytics platform for oil and gas operations, "
            "on-premises deployment, custom integrations, 24/7 support."
        ),
    },
    "clause_041": {
        "contract_type": "Managed Services Agreement",
        "parties": "Pacific Coast University (Client) and EduTech Managed Services LLC (Vendor)",
        "jurisdiction": "Oregon, USA",
        "contract_value": "$890,000 annual",
        "other_clauses_summary": (
            "Campus-wide IT infrastructure management, FERPA compliance, "
            "student data handling, hybrid cloud environment."
        ),
    },
    "clause_042": {
        "contract_type": "Consulting Agreement",
        "parties": "Titanium Aerospace Corp. (Client) and AeroSystems Consulting Group (Vendor)",
        "jurisdiction": "Washington, USA",
        "contract_value": "$3,500,000 project total",
        "other_clauses_summary": (
            "Avionics systems integration consulting, ITAR-controlled data, "
            "security clearance requirements, milestone-based payments."
        ),
    },
    "clause_043": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Cascade Health Network (Client) and MedCloud Analytics Inc. (Vendor)",
        "jurisdiction": "Washington, USA",
        "contract_value": "$1,200,000 annual",
        "other_clauses_summary": (
            "Population health analytics platform, HIPAA BAA, "
            "de-identification services, interoperability with Epic EHR."
        ),
    },
    "clause_044": {
        "contract_type": "Master Services Agreement",
        "parties": "TransGlobal Shipping Inc. (Client) and MaritimeTech Solutions (Vendor)",
        "jurisdiction": "New York, USA",
        "contract_value": "$950,000 annual",
        "other_clauses_summary": (
            "Fleet management and logistics optimization platform, "
            "international operations across 30+ countries, sanctions screening."
        ),
    },
    "clause_045": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Sterling Financial Services (Client) and RegTech Compliance Inc. (Vendor)",
        "jurisdiction": "New York, USA",
        "contract_value": "$675,000 annual",
        "other_clauses_summary": (
            "Regulatory compliance monitoring platform, SEC and FINRA reporting, "
            "automated surveillance, SOC 2 Type II certified."
        ),
    },
    "clause_046": {
        "contract_type": "Master Services Agreement",
        "parties": "Pinnacle Software Corp. (Client) and EliteStaff Consulting LLC (Vendor)",
        "jurisdiction": "California, USA",
        "contract_value": "$2,100,000 annual",
        "other_clauses_summary": (
            "Staff augmentation for software development, 25 FTE equivalents, "
            "agile methodology, co-located team members."
        ),
    },
    # ── NEW HARD scenarios ───────────────────────────────────────────────
    "clause_047": {
        "contract_type": "Enterprise Software License Agreement",
        "parties": "FortKnox Banking Corp. (Client) and FinServ Platform Inc. (Vendor)",
        "jurisdiction": "New York, USA",
        "contract_value": "$4,500,000 over 5 years",
        "other_clauses_summary": (
            "Core banking platform replacement, phased migration from legacy system, "
            "regulatory approval requirements, data sovereignty obligations."
        ),
    },
    "clause_048": {
        "contract_type": "Master Services Agreement",
        "parties": "Orion Data Centers LLC (Client) and HyperScale Infrastructure Inc. (Vendor)",
        "jurisdiction": "Virginia, USA",
        "contract_value": "$6,200,000 annual",
        "other_clauses_summary": (
            "Colocation and managed hosting services, Tier IV data center, "
            "100% SLA with financial credits, multi-year capacity commitments."
        ),
    },
    "clause_049": {
        "contract_type": "Custom Software Development Agreement",
        "parties": "Vertex Autonomous Systems (Client) and CodeVault Engineering Inc. (Vendor)",
        "jurisdiction": "California, USA",
        "contract_value": "$2,800,000 project total",
        "other_clauses_summary": (
            "Autonomous vehicle perception software development, "
            "safety-critical systems, extensive testing and validation, "
            "IP ownership negotiation was contentious."
        ),
    },
    "clause_050": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Sentinel Intelligence Agency (Client) and ClearView Analytics Inc. (Vendor)",
        "jurisdiction": "Virginia, USA",
        "contract_value": "$3,100,000 annual",
        "other_clauses_summary": (
            "Intelligence analytics platform, FedRAMP High authorization, "
            "air-gapped deployment option, personnel vetting requirements."
        ),
    },
    "clause_051": {
        "contract_type": "Managed Services Agreement",
        "parties": "Evergreen Hospital Network (Client) and HealthIT Managed Services Corp. (Vendor)",
        "jurisdiction": "Pennsylvania, USA",
        "contract_value": "$4,200,000 annual",
        "other_clauses_summary": (
            "Full IT outsourcing for 12-hospital network, HIPAA BAA, "
            "EHR support, 24/7 help desk, HITRUST certification required."
        ),
    },
    "clause_052": {
        "contract_type": "Enterprise Software License Agreement",
        "parties": "Nexus Telecommunications Inc. (Client) and BillingSoft Corp. (Vendor)",
        "jurisdiction": "Georgia, USA",
        "contract_value": "$7,500,000 over 5 years",
        "other_clauses_summary": (
            "Converged billing platform for 8M subscribers, "
            "real-time rating engine, regulatory compliance for 12 states, "
            "performance benchmarks with financial penalties."
        ),
    },
    "clause_053": {
        "contract_type": "SaaS Subscription Agreement",
        "parties": "Cornerstone Investment Partners (Client) and MarketData Pro Inc. (Vendor)",
        "jurisdiction": "New York, USA",
        "contract_value": "$1,600,000 annual",
        "other_clauses_summary": (
            "Real-time market data and analytics platform, "
            "low-latency feed requirements, redundant connectivity, "
            "SEC and FINRA compliance features."
        ),
    },
    "clause_054": {
        "contract_type": "Consulting Agreement",
        "parties": "Granite Construction Holdings (Client) and RiskAdvisors International LLC (Contractor)",
        "jurisdiction": "California, USA",
        "contract_value": "$1,350,000 annual retainer",
        "other_clauses_summary": (
            "Enterprise risk management consulting, multi-state operations, "
            "construction site safety audits, regulatory compliance advisory."
        ),
    },
    "clause_055": {
        "contract_type": "Employment Agreement",
        "parties": "Zenith Technologies Inc. (Company) and Dr. Rachel Kim (Employee)",
        "jurisdiction": "California, USA",
        "contract_value": "$425,000 annual salary + equity",
        "other_clauses_summary": (
            "VP of Engineering employment, stock option grant with 4-year vesting, "
            "acceleration on change of control, invention assignment agreement."
        ),
    },
}


CONTRACT_GROUPS: Dict[str, Dict[str, Any]] = {
    "contract_A": {
        "name": "TechCorp Master Services Agreement",
        "clauses": ["clause_011", "clause_012", "clause_013"],
        "dependencies": [
            {
                "clause_pair": ("clause_011", "clause_012"),
                "type": "contradiction",
                "description": (
                    "Indemnification is unlimited but liability cap is $100. "
                    "These contradict."
                ),
                "keywords": [
                    "contradict", "conflict", "inconsistent",
                    "indemnification exceeds", "cap",
                ],
            },
        ],
    },
    "contract_B": {
        "name": "CloudSoft SaaS Agreement",
        "clauses": ["clause_014", "clause_019", "clause_015"],
        "dependencies": [
            {
                "clause_pair": ("clause_014", "clause_019"),
                "type": "overlap",
                "description": (
                    "Perpetual confidentiality conflicts with data protection "
                    "clause that disclaims liability for breaches."
                ),
                "keywords": [
                    "perpetual", "conflicts with data", "breach liability",
                    "inconsistent",
                ],
            },
        ],
    },
    "contract_C": {
        "name": "Enterprise Software License",
        "clauses": ["clause_022", "clause_023", "clause_021"],
        "dependencies": [
            {
                "clause_pair": ("clause_022", "clause_021"),
                "type": "contradiction",
                "description": (
                    "LoL carveouts for indemnification make the indemnification "
                    "cap meaningless since the asymmetric caps in indemnification "
                    "would be overridden."
                ),
                "keywords": [
                    "carveout", "override", "indemnification cap",
                    "meaningless", "swallow",
                ],
            },
            {
                "clause_pair": ("clause_023", "clause_022"),
                "type": "interaction",
                "description": (
                    "Early termination penalty combined with liability cap could "
                    "mean termination costs exceed the liability cap."
                ),
                "keywords": [
                    "termination penalty", "exceeds cap", "liability cap",
                    "early termination",
                ],
            },
        ],
    },
    "contract_D": {
        "name": "Consulting Agreement",
        "clauses": ["clause_016", "clause_025", "clause_018"],
        "dependencies": [
            {
                "clause_pair": ("clause_016", "clause_025"),
                "type": "compounding",
                "description": (
                    "Worldwide non-compete combined with capturing all IP "
                    "(even unrelated) effectively prevents the contractor "
                    "from working in their field."
                ),
                "keywords": [
                    "combined", "effectively prevents", "cannot work",
                    "compounding", "all IP plus non-compete",
                ],
            },
        ],
    },
}


def get_scenarios_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    """Return scenarios filtered by difficulty level."""
    return [s for s in SCENARIOS if s["difficulty"] == difficulty]


def get_scenario_by_id(scenario_id: str) -> Dict[str, Any] | None:
    """Return a specific scenario by ID."""
    for s in SCENARIOS:
        if s["id"] == scenario_id:
            return s
    return None


def get_contract_group_for_clause(clause_id: str) -> Dict[str, Any] | None:
    """Return the contract group that contains the given clause, or None."""
    for group in CONTRACT_GROUPS.values():
        if clause_id in group["clauses"]:
            return group
    return None
