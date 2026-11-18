# HealthFirst Network — Enterprise Security Architecture

**Cybersecurity Architecture and Engineering — Group Project** · CCSE, University of Jeddah · Fall 2026
**Scenario 1 — Healthcare Sector: HealthFirst Network**

| | |
|---|---|
| **Team** | Rayan Ameen Kurdi (2440795) · Yazan Tareq Alhazmi (2440370) |

> HealthFirst Network is a fictional organization. Organization sizes, revenues and costs are planning assumptions stated in Document 1, Section 1.3.

---

## 1. Deliverables

| Project phase | Deliverable | Markdown source | Exports |
|---|---|---|---|
| Phase 1 — Business and risk analysis | **Business and Security Strategy Document** | `01-Business-and-Security-Strategy.md` | `exports/01-….pdf`, `exports/01-….docx` |
| Phase 2 — Conceptual and logical design | **Conceptual and Logical Architecture Document** | `02-Conceptual-and-Logical-Architecture.md` | `exports/02-….pdf`, `exports/02-….docx` |
| Phase 3 — Physical and component design | **Physical Architecture and Technology Specification Document** | `03-Physical-Architecture-and-Technology-Specification.md` | `exports/03-….pdf`, `exports/03-….docx` |
| Phase 4.1 — Governance and assessment | **Security Architecture Governance and Assessment Plan** | `04-Security-Architecture-Governance-and-Assessment-Plan.md` | `exports/04-….pdf`, `exports/04-….docx` |
| Phase 4.2 — Final review | **Final Architecture Review Presentation** | 22 slides (Slides deck “HealthFirst Network — Final Architecture Review”; speaker notes are in the online deck) | `presentation/HealthFirst-Network-Final-Architecture-Review.pdf` |

The Markdown files are the master copies: every diagram is embedded in them as an editable draw.io image. The PDFs are the print-ready versions (diagrams on landscape pages); the Word files are editable versions of the same text.

## 2. How the work answers the rubric

| Criterion (weight) | Where it is addressed |
|---|---|
| **Business and risk analysis (25 %)** | Doc 1: business drivers BD1–BD9, SABSA contextual analysis, 18 business attributes with KPIs, risk appetite and tolerance, NIST SP 800-30 register R01–R14, FAIR Monte Carlo model (S1–S6), strategy objectives SO1–SO8, principles P1–P12, control objectives CO-01–CO-12 |
| **Architecture design (35 %)** | Doc 2: capability model, NIST SP 800-207 Zero Trust design, healthcare constraints K1–K8, zones Z0–Z10 and conduits C1–C12, 39 logical services, STRIDE on two data flows, MITRE ATT&CK ransomware coverage, ADR-01–ADR-08 · Doc 3: Azure landing zones, hybrid network, hospital site design, identity, IoMT, EHR, telemedicine and research platforms, resilience, 38-component technology specification, costs, transition architectures |
| **Compliance and governance (20 %)** | Doc 4: governance bodies, RACI, ARB gates, exception process, 18 assessment methods, KPIs and KRIs, full HIPAA Security Rule matrix (18 standards, 36 implementation specifications), HITECH, GDPR, NIST CSF 2.0 profile, readiness for the January 2025 HIPAA NPRM, gap analysis G01–G12, alignment with the Azure Well-Architected security checklist and CSA CCM v4.1 (Section 4.7), golden-thread traceability, roadmap M1–M7 · Doc 3, Section 6: HIPAA technical safeguards by component |
| **Documentation and presentation (20 %)** | Four professionally formatted documents (Markdown, PDF, Word), 18 draw.io diagrams, 4 charts, and the 22-slide review deck with speaker notes |

## 3. Folder structure

```
README.md                         this file
01-…md … 04-…md                   the four documents (Markdown masters)
diagrams/
  *.drawio                        editable draw.io source of each diagram
  *.drawio.svg                    the same diagram as an SVG that draw.io can also open and edit (embedded in the Markdown)
  png/*.png                       high-resolution PNG copies (used in the Word files)
charts/                           FAIR, Zero Trust maturity and CSF charts (SVG + PNG) and fair-results.json
exports/                          PDF and Word versions of the four documents
presentation/                     the Final Architecture Review slides (PDF)
scripts/fair_model.py             the FAIR Monte Carlo model behind Doc 1, Section 7.5
```

## 4. Diagram index (all made with draw.io)

| Figure | Diagram | File (`diagrams/`) |
|---|---|---|
| 1.1 | Enterprise context, stakeholders and the move to hybrid Azure | `f1-1-enterprise-context` |
| 1.2 | SABSA golden thread (BD7 to KPI) | `f1-2-sabsa-traceability` |
| 1.3 | Inherent and residual risk heat maps | `f1-3-risk-heatmap` |
| 2.1 | Conceptual security capability model | `f2-1-conceptual-capability-model` |
| 2.2 | Zero Trust logical architecture (NIST SP 800-207) | `f2-2-zero-trust-logical` |
| 2.4 | Security zones Z0–Z10 and conduits C1–C12 | `f2-3-security-zones` |
| 2.5 | DFD-1: telemedicine and patient access | `f2-4-dfd-telemedicine` |
| 2.6 | DFD-2: medical devices, vendor support and monitoring | `f2-5-dfd-iomt` |
| 3.1 | Azure landing zones and the cyber-recovery tenant | `f3-1-azure-landing-zones` |
| 3.2 | Hybrid network topology | `f3-2-hybrid-network` |
| 3.3 | Hospital site reference architecture | `f3-3-hospital-site` |
| 3.4 | Telemedicine platform | `f3-4-telemedicine-platform` |
| 3.5 | Research Trusted Research Environment | `f3-5-research-tre` |
| 3.6 | Security operations architecture | `f3-7-security-operations` |
| 3.7 | Ransomware resilience and recovery | `f3-6-ransomware-resilience` |
| 4.1 | Governance structure and three lines model | `f4-1-governance-structure` |
| 4.2 | Governance and assessment lifecycle | `f4-2-assessment-lifecycle` |
| 4.4 | 30-month implementation roadmap | `f4-3-roadmap` |

Charts: Figure 1.4 loss exceedance curves (`charts/fair-loss-exceedance`), Figure 1.5 loss by scenario (`charts/fair-ale-by-scenario`), Figure 2.3 Zero Trust maturity radar (`charts/zt-maturity-radar`), Figure 4.3 NIST CSF 2.0 profile (`charts/csf-profile`).

**Editing a diagram.** Open the `.drawio` or `.drawio.svg` file in [diagrams.net](https://app.diagrams.net) (File › Open from › Device), in the draw.io desktop app, or in VS Code with the *Draw.io Integration* extension. Saving a `.drawio.svg` keeps it both editable and viewable, so the Markdown documents update automatically. After editing, export a PNG (File › Export as › PNG, zoom 200 %) into `diagrams/png/` if you also rebuild the Word files.

**Viewing the Markdown.** GitHub, GitLab and the VS Code Markdown preview render the documents with their embedded diagrams. Keep the folder structure intact so the relative image paths resolve.

## 5. Reproducing the FAIR results

`scripts/fair_model.py` runs the 100,000-year Monte Carlo simulation (beta-PERT ranges, Poisson event counts, fixed random seed) and rewrites `charts/fair-results.json` and the two FAIR charts. It needs Python 3 with `numpy` and `matplotlib`:

```
python3 scripts/fair_model.py
```

Expected headline output: inherent annualized loss expectancy $50.72 M, residual $7.87 M, residual net of cyber insurance $3.83 M, return on security investment 2.11 (211 %).

## 6. Keeping the versions in step

If you change the Markdown, regenerate the PDF and Word exports so all versions stay identical.
