# Pedagogical foundations

Every rule in these skills should be traceable: to research, to a professional standard, or — honestly labelled — to experienced local practice. This page shows which is which, where each principle appears in the skills, and where the evidence has limits.

## How sources are chosen

**Three kinds of basis**

| Label | Meaning |
|---|---|
| **Research** | Supported by experimental studies or meta-analyses |
| **Standard** | A professional consensus or published standard (AAMC, NBME, measurement theory) |
| **Practice** | A local convention from experienced educators. Useful and explainable, not directly tested. Institutions may change it |

**Three layers of principles**

1. **Overarching principles of science teaching**, shared by biomedical research, PhD and pre-clinical teaching.
2. **Principles specific to medical education**, with no direct counterpart in general science teaching.
3. **Teaching in the AI era**, across both layers.

**Two tiers of sources.** Every principle cites its origin, the source where it was first formulated. Because this library is for medical and biomedical educators, every principle also needs evidence from health-professions education: a study with medical or other health-professions learners, or a standard from a medical-education body. A principle without one is marked *Evidence from general education only*, not hidden. Each source records who was studied, how, and how far the finding carries to our learners.

The principles live in one registry, [`principles.yaml`](principles.yaml); this page and the [gap report](principle-gaps.md) are generated from it.

---

## Each principle in detail

<!-- PRINCIPLES:START -->
### Overarching principles of science teaching

Shared by biomedical research, PhD and pre-clinical teaching. Most come from the learning sciences or general STEM education, so each also needs evidence from health-professions education.

#### 1. Scientific teaching — *Standard*

Teach the way we do science: choose methods with evidence behind them, measure what works, and change course on the data.

**Sources**

- Handelsman et al., 2004 (origin; undergraduate STEM, policy forum). Written for research universities; applies directly to biomedical research and PhD teaching.
- Freeman et al., 2014 (science-ed; undergraduate STEM, meta-analysis (225 studies)). Undergraduate STEM courses, including biology. Closest to pre-clinical and graduate science teaching; not tested in clinical settings.
- *Medical education:* BEME Guide 1 (Harden et al., 1999) (position paper (founding BEME guide)). Calls for medical teaching decisions to move from opinion to the best available evidence; the medical-education form of scientific teaching. A position paper, not a trial.

**Where it appears**

- The library: Every skill states what each rule rests on; usage reports and maturity levels test the skills the way an experiment would.

#### 2. Constructive alignment — *Standard*

Objectives, activities and assessment are designed together, so learners practise and are tested on what the objectives say.

**Sources**

- Biggs, 1996 (origin; higher education, theory). A design theory for any course; adopted widely in medical curricula, but not tested experimentally there.
- *Medical education:* AMEE Guide 14 (Harden et al., 1999) (guide). Outcome-based education for medical curricula: outcomes are specified first, and teaching and assessment are planned from them. A guide, not a trial.
- *Medical education:* Frank et al., 2010 (international consensus). Defines CBME for medical curricula; a consensus, not an outcome study.

**Where it appears**

- `learning-objectives-designer`: Checks each objective for an activity and an assessment and reports the gaps.
- `syllabus-builder`: Links objectives, schedule and assessment; a competency counts as evidence only when it is assessed.
- `exam-question-writer`: A blueprint before items; one item tests one objective.
- `lesson-format-checker`: Every lesson segment names the objective it serves, and every objective is served.
- `curriculum-map-builder`: Links course goals, module goals, session objectives and assessment items, and flags goals that are never taught or never assessed.

#### 3. Observable, levelled objectives — *Standard*

One observable verb at a defined cognitive level; for skills, a condition and a criterion.

**Sources**

- Anderson & Krathwohl, 2001 (origin; higher education, framework). A general classification of objectives; used as-is in medical schools.
- Mager, 1962 (origin; higher education, framework). Condition and criterion suit procedural and clinical skills especially well.
- *Medical education:* Thomas, Kern et al., 2016 (textbook). The standard curriculum-development text in medical education; step 3 covers goals and measurable objectives.
- *Medical education:* Chatterjee & Corral, 2017 (review with practical guidance). Objectives as observable, measurable learner behaviour, and the basis for aligning assessment and teaching in academic medicine.

**Where it appears**

- `learning-objectives-designer`: One verb, one target; no 'understand' or 'know'; level matched to what the activity demands.
- `syllabus-builder`: Course objectives use the same rules.
- `curriculum-map-builder`: Checks objectives per session for one clear task, varied verbs and no vague verbs such as 'understand'.

*Practice:* Collapsing Bloom's six levels into three (Foundational / Applied / Advanced) is a local convention for easier agreement; the skill records both.

#### 4. Active learning — *Research*

Learners do something with the material in class, rather than only listen. It raises exam scores and cuts failure rates.

**Sources**

- Freeman et al., 2014 (origin; undergraduate STEM, meta-analysis (225 studies)). Undergraduate STEM courses, including biology. Closest to pre-clinical and graduate science teaching; not tested in clinical settings.
- *Medical education:* Boedeker et al., 2025 (randomized cross-over trial (146 second-year medical students)). Interactive large-group sessions scored 0.27 SD higher than lectures on the same content, with the largest gains for lower-achieving students.
- *Medical education:* Hew & Lo, 2018 (meta-analysis (28 studies)). Flipped classrooms outperformed traditional ones (SMD 0.33), more so when class began with a quiz.
- *Medical education:* BEME Guide 30 (Fatmi et al., 2013) (systematic review). Team-based learning against other methods across the health professions; study designs and quality varied.
- *Medical education:* Chen, Lui & Martinelli, 2017 (systematic review (9 controlled studies)). Learners liked flipped classrooms, but effects on knowledge and skills were inconclusive (median effect size 0.08).

**Where it appears**

- `pbl-rbl-session-builder`: Every phase asks students to predict, analyse or decide before anything is revealed.
- `reading-material-generator`: Readings end with questions students answer, not only text to absorb.

**Limit:** In medical education, much of the evidence comes from studies with weak designs, and flipped classrooms in particular show mixed effects on knowledge. The randomized trial by Boedeker et al. (2025) is the strongest single result.

#### 5. Problem solving before instruction — *Research*

Trying first, then consolidating, improves understanding and transfer, when the struggle is designed and followed by explicit instruction.

**Sources**

- Kapur, 2008 (origin; school students, experiment). Secondary-school mathematics.
- Schwartz & Bransford, 1998 (origin; higher education, experiment). University students in psychology; the idea of preparation for future learning carries well to science courses.
- Sinha & Kapur, 2021 (science-ed; school students, meta-analysis (53 studies)). Mostly school and university mathematics and science; benefits were smaller for the youngest learners.
- *Medical education:* Steenhof et al., 2019 (RCT (40 first-year pharmacy students)). A small single-school trial in pharmacy. No difference on standard recall or application; an advantage on learning new related material.

**Where it appears**

- `pbl-rbl-session-builder`: The productive trap, predict before reveal, design before seeing, and staged information release, with a consolidating reveal after each trap.

**Limit:** Struggle without consolidation is just failure. Health-professions evidence is one small pharmacy trial.

#### 6. Managing cognitive load — *Research*

Working memory is limited, and novices need guidance: one inference per prompt, terms defined at first use, worked examples before independent work.

**Sources**

- Sweller, 1988 (origin; laboratory studies, experiments). Laboratory problem solving; the theory was later applied to health professions (see van Merriënboer & Sweller, 2010).
- Kirschner, Sweller & Clark, 2006 (science-ed; higher education, review). A general argument about novices; contested by productive-failure research.
- *Medical education:* van Merriënboer & Sweller, 2010 (review with design guidelines). Fifteen design guidelines written for health-professions education; a review, not a trial.

**Where it appears**

- `pbl-rbl-session-builder`: One inference per prompt, observation before inference, calibration to the student stage.
- `reading-material-generator`: A teaching arc in the order a newcomer needs, inline definitions, depth over coverage.
- `lesson-format-checker`: Time estimates on every part; provided code at first exposure, student-written code once the pattern is known.
- `learning-objectives-designer`: One target per objective.

#### 7. Retrieval practice with feedback — *Research*

Recalling strengthens memory more than rereading, and feedback is essential.

**Sources**

- Roediger & Karpicke, 2006 (origin; laboratory studies, experiments). University students reading prose passages.
- *Medical education:* Larsen, Butler & Roediger, 2008 (review). Applies retrieval practice to medical education and stresses feedback.

**Where it appears**

- `reading-material-generator`: A click-to-reveal self-check at the end of each reading.
- `pbl-rbl-session-builder`: Comprehension quizzes answerable from the reading.
- `exam-question-writer`: In formative mode, a rationale for every option.

#### 8. Spaced practice — *Research*

Spreading practice over time beats massing it, and the gap should grow with how long knowledge must last.

**Sources**

- Cepeda et al., 2006 (origin; laboratory studies, meta-analysis (317 experiments)). Verbal recall tasks; the best gap between sessions grows with how long knowledge must last.
- *Medical education:* Kerfoot et al., 2007 (RCT (third-year medical students, urology)). Weekly emailed clinical cases and questions improved retention months after the rotation.

**Where it appears:** no skill yet. A candidate for a new skill or an addition to an existing one.

### Principles specific to medical education

Principles with no direct counterpart in general science teaching, from health-professions education research and standards.

#### 9. Competencies and entrustment — *Standard*

Count a competency only where learners perform it and someone observes it. Frameworks need faculty review before use.

**Sources**

- *Medical education:* Frank et al., 2010 (international consensus). Defines CBME for medical curricula; a consensus, not an outcome study.
- *Medical education:* ten Cate, 2005 (concept paper). Origin of EPAs; written for postgraduate training and now used across the continuum.
- *Medical education:* AAMC Foundational Competencies, 2024 (standard). US undergraduate medical education; adopt only after local faculty review.
- *Medical education:* GREAT MD-PhD toolkit (Estrada et al., 2026) (community consensus toolkit). Built for MD-PhD programs; the competencies most relevant to physician-scientist training.

**Where it appears**

- `syllabus-builder`: Framework links are proposals for the course leader to approve; wording comes only from the supplied document.
- `learning-objectives-designer`: Suggests competency links for each objective, for the educator to confirm.

*Practice:* The E / P / X levels and the 're-check above six E links' rule are local methods that apply entrustment to course mapping.

#### 10. Problems and clinical context — *Research*

Working on problems activates prior knowledge and stores it where it will be used. Teaching basic science in a clinical context helps build illness scripts.

**Sources**

- *Medical education:* Schmidt, 1983 (theory). Written for medical schools.
- *Medical education:* Norman & Schmidt, 1992 (review). Medical education.
- *Medical education:* Schmidt & Rikers, 2007 (review). Recommends teaching basic science in a clinical context and introducing patient problems early.
- *Medical education:* Colliver, 2000 (review). Whole PBL curricula in medical schools showed modest or mixed knowledge effects.

**Where it appears**

- `pbl-rbl-session-builder`: Case- or tool-driven phases, learning issues and research questions, calibrated to the student stage.

**Limit:** Whole PBL curricula show modest or mixed knowledge effects (Colliver, 2000), so the skill adds the structure of the layer-1 principles.

#### 11. Deliberate practice and simulation — *Research*

Expertise grows through focused practice on specific weaknesses with immediate feedback, not through experience alone.

**Sources**

- *Medical education:* Ericsson, 2004 (review). Applies the expert-performance framework to medicine; experience alone does not build expertise.
- *Medical education:* McGaghie et al., 2011 (meta-analysis (14 studies)). Clinical skill acquisition, effect size 0.71; the authors note the small number of studies.

**Where it appears:** no skill yet. A candidate for a new skill or an addition to an existing one.

#### 12. Item-writing quality — *Standard*

Validated guidelines define well-formed items. Flawed items are common and disadvantage some students.

**Sources**

- Haladyna, Downing & Rodriguez, 2002 (origin; higher education, review (31 guidelines)). General classroom assessment; the guidelines match the NBME guide.
- *Medical education:* NBME Item-Writing Guide, 2020 (standard). The reference standard for written items in the health sciences.
- *Medical education:* Downing, 2005 (observational (four medical-school exams)). 36–65% of items were flawed, and flawed items disadvantaged some students.

**Where it appears**

- `exam-question-writer`: The flaw checklist, the cover-the-options test, homogeneous options, no 'all/none of the above', fair vignettes.

#### 13. Assessment validity and programmes — *Standard*

A result supports a decision only with validity evidence for that use. Competence is judged from many assessments together, not from one.

**Sources**

- *Medical education:* van der Vleuten, 1996 (review). The utility model: reliability, validity, educational impact, acceptability and cost.
- *Medical education:* Downing, 2003 (theory). Validity theory explained for medical educators.
- *Medical education:* van der Vleuten & Schuwirth, 2005 (review). Origin of programmatic assessment: judge competence from many assessments together, not from one.

**Where it appears**

- `exam-question-writer`: Asks formative or summative first; summative items need expert review, piloting and item analysis.
- `committee-meeting-planner`: Treats the thesis committee meeting as one of many checkpoints: the student brings the last meeting's action items, and the committee confirms a written summary of its advice.
- `syllabus-builder`: A competency counts as evidence only where performance is observed or assessed.

#### 14. Professional identity formation — *Standard*

Medical education should help learners come to think, act and feel like physicians (and, for MD-PhD students, like physician-scientists), not only perform competently.

**Sources**

- *Medical education:* Cruess et al., 2014 (perspective). Proposes identity formation as a main goal of medical education; a perspective, not an outcome study.

**Where it appears:** no skill yet. A candidate for a new skill or an addition to an existing one.

### Teaching in the AI era

Principles for teaching with AI, across both layers above.

#### 15. Responsible AI in education — *Standard*

Disclose AI use, protect privacy, give equal access, keep the educator in charge, and never invent sources.

**Sources**

- UNESCO AI Competency Framework for Teachers, 2024 (standard; professional standard, framework (15 competencies in 5 dimensions)). For teachers at every level; not specific to medicine.
- *Medical education:* AAMC AI Principles, 2025 (standard). Written for medical education.
- *Medical education:* AAMC AI Competencies, 2026 (competency framework). AI competencies in developmental tiers from medical school through practice; the reference for what learners should be able to do with AI.
- *Medical education:* AMEE Guide 158 (Masters, 2023) (guide). Ethical issues for teachers and administrators using AI: data, privacy, consent, bias, transparency and responsibility.

**Where it appears**

- Every skill: An AI-assistance line in the institution's wording; no identifiable patient or learner data; the educator approves before anything is final; no invented sources.
- The library: Open format and paste-in versions, so access does not depend on one paid tool.

*See also:* [AAMC: Advancing AI Across Academic Medicine resource collection](https://www.aamc.org/about-us/mission-areas/medical-education/advancing-ai-across-academic-medicine-resource-collection)

#### 16. AI that protects learning — *Research*

Unrestricted AI help can raise practice scores and lower real learning. Student-facing AI should guide rather than hand over answers, and its effects should be studied.

**Sources**

- Bastani et al., 2025 (origin; school students, field experiment). High-school mathematics. Unguarded AI access lowered later performance; a tutor version with safeguards largely avoided the harm. Not yet replicated in medical education.
- *Medical education:* AMEE Guide 156 (Tolsgaard et al., 2023) (guide). How to study AI in medical education rigorously. Context for the principle, not evidence that guardrails work.
- *Medical education:* BEME Guide 84 (Gordon et al., 2024) (scoping review (278 publications)). Maps AI in medical education and calls for ethical guidelines. Context for this principle, not a test of whether guardrails protect learning.

> **Evidence from general education only.** No health-professions source in the registry supports this principle yet. Treat it as a well-supported hypothesis for medical learners, and report what you see.

**Where it appears:** no skill yet. A candidate for a new skill or an addition to an existing one.

**Limit:** The trial was in high-school mathematics, and no health-professions study yet tests whether AI guardrails protect learning. The skills here are for educators, not students, so this principle has no skill yet.
<!-- PRINCIPLES:END -->

---

## Local practice, labelled honestly

These rules come from teaching experience in the MD-PhD program at the Miriam and Aaron Gutwirth Medical School, Weizmann Institute of Science. They are explainable but not directly tested. Institutions may change them.

| Rule | Skill | Rationale |
|---|---|---|
| Reading budget of 3,000 words per hour | reading-material-generator | Adults read non-fiction silently at about 238 words per minute (Brysbaert, 2019). The budget of ~50 words per minute deliberately leaves time for studying, reflecting and discussing. Measure your own learners if you can |
| Three cognitive levels instead of six | learning-objectives-designer | Easier agreement between faculty; Bloom level is still recorded |
| E / P / X evidence levels; re-check above six E links | syllabus-builder | Guards against inflated competency maps |
| 2–4 objectives per session, 3–5 per course | objectives, syllabus | Keeps alignment checkable |
| Facilitator voice, invisible pedagogy, human texture, wonder | pbl-rbl-session-builder | Craft guidance for writing cases; consistent with the research above, not separately tested |
| Format rules (box colours, glossary as table, code markers) | lesson-format-checker | Operational: consistency and compatibility with grading and export tools |

## Known debates and limits

- **Discovery vs. guidance.** Principles 5 and 6 pull in different directions. The skills take the position supported by the meta-analytic evidence: designed, bounded struggle followed by explicit consolidation, calibrated to learners' prior knowledge.
- **AI-generated content needs checking.** No skill claims that its output is valid. Exam items, maps and readings are drafts for expert review.
- **Evidence from general education.** Several findings come mostly from school and university settings. The [gap report](principle-gaps.md) lists the principles still waiting for health-professions evidence; institutions can help by collecting their own data, and the library's usage reports are one way to do that.

## How to propose a change

If your experience or a study contradicts a rule here, open an issue with the source. Rules labelled **Practice** are the first candidates for change.

---

<!-- REFERENCES:START -->
## References

- AAMC, AACOM & ACGME. (2024). Foundational competencies for undergraduate medical education. https://engage.aamc.org/UME-Competencies-AAMC-ACGME-AACOM
- Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives. Longman.
- Association of American Medical Colleges. (2025). Principles for the responsible use of artificial intelligence in and for medical education. https://www.aamc.org/about-us/mission-areas/medical-education/principles-ai-use
- Bastani, H., Bastani, O., Sungu, A., et al. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. PNAS, 122(26), e2422633122. https://doi.org/10.1073/pnas.2422633122
- Biggs, J. (1996). Enhancing teaching through constructive alignment. Higher Education, 32(3), 347–364. https://doi.org/10.1007/BF00138871
- Boedeker, P., Schlingmann, T., Kailin, J., et al. (2025). Active versus passive learning in large-group sessions in medical school: A randomized cross-over trial investigating effects on learning and the feeling of learning. Medical Science Educator, 35(1), 459–467. https://doi.org/10.1007/s40670-024-02219-1
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. Psychological Bulletin, 132(3), 354–380. https://doi.org/10.1037/0033-2909.132.3.354
- Chatterjee, D., & Corral, J. (2017). How to write well-defined learning objectives. Journal of Education in Perioperative Medicine, 19(4), E610.
- Chen, F., Lui, A. M., & Martinelli, S. M. (2017). A systematic review of the effectiveness of flipped classrooms in medical education. Medical Education, 51(6), 585–597. https://doi.org/10.1111/medu.13272
- Colliver, J. A. (2000). Effectiveness of problem-based learning curricula: Research and theory. Academic Medicine, 75(3), 259–266.
- Cruess, R. L., Cruess, S. R., Boudreau, J. D., Snell, L., & Steinert, Y. (2014). Reframing medical education to support professional identity formation. Academic Medicine, 89(11), 1446–1451.
- Downing, S. M. (2003). Validity: On the meaningful interpretation of assessment data. Medical Education, 37(9), 830–837.
- Downing, S. M. (2005). The effects of violating standard item writing principles on tests and students. Advances in Health Sciences Education, 10(2), 133–143. https://doi.org/10.1007/s10459-004-4019-5
- Ericsson, K. A. (2004). Deliberate practice and the acquisition and maintenance of expert performance in medicine and related domains. Academic Medicine, 79(10 Suppl), S70–S81. https://doi.org/10.1097/00001888-200410001-00022
- Estrada, L., Baca, J. T., Baron, M. H., et al. (2026). A community-informed toolkit for physician-scientist competencies and milestones: Bridging the worlds of medicine and research. Academic Medicine. https://doi.org/10.1093/acamed/wvag053
- Fatmi, M., Hartling, L., Hillier, T., Campbell, S., & Oswald, A. E. (2013). The effectiveness of team-based learning on learning outcomes in health professions education: BEME Guide No. 30. Medical Teacher, 35(12), e1608–e1624. https://doi.org/10.3109/0142159X.2013.849802
- Frank, J. R., Snell, L. S., ten Cate, O., et al. (2010). Competency-based medical education: Theory to practice. Medical Teacher, 32(8), 638–645. https://doi.org/10.3109/0142159X.2010.501190
- Freeman, S., Eddy, S. L., McDonough, M., et al. (2014). Active learning increases student performance in science, engineering, and mathematics. PNAS, 111(23), 8410–8415. https://doi.org/10.1073/pnas.1319030111
- Gordon, M., Daniel, M., Ajiboye, A., et al. (2024). A scoping review of artificial intelligence in medical education: BEME Guide No. 84. Medical Teacher, 46(4), 446–470. https://doi.org/10.1080/0142159X.2024.2314198
- Haladyna, T. M., Downing, S. M., & Rodriguez, M. C. (2002). A review of multiple-choice item-writing guidelines for classroom assessment. Applied Measurement in Education, 15(3), 309–333. https://doi.org/10.1207/S15324818AME1503_5
- Handelsman, J., Ebert-May, D., Beichner, R., et al. (2004). Scientific teaching. Science, 304(5670), 521–522. https://doi.org/10.1126/science.1096022
- Harden, R. M., Crosby, J. R., & Davis, M. H. (1999). AMEE Guide No. 14: Outcome-based education: Part 1 – An introduction to outcome-based education. Medical Teacher, 21(1), 7–14. https://doi.org/10.1080/01421599979969
- Harden, R. M., Grant, J., Buckley, G., & Hart, I. R. (1999). BEME Guide No. 1: Best Evidence Medical Education. Medical Teacher, 21(6), 553–562. https://doi.org/10.1080/01421599978960
- Hew, K. F., & Lo, C. K. (2018). Flipped classroom improves student learning in health professions education: A meta-analysis. BMC Medical Education, 18, 38. https://doi.org/10.1186/s12909-018-1144-z
- Howley, L., Weems, K., Peoples, D., & Whelan, A. J. (2026). AI competencies across the learning continuum. Association of American Medical Colleges. https://www.aamc.org/about-us/medical-education/cbme/publication/ai-competencies-across-learning-continuum
- Kapur, M. (2008). Productive failure. Cognition and Instruction, 26(3), 379–424.
- Kerfoot, B. P., et al. (2007). Spaced education improves the retention of clinical knowledge by medical students: A randomised controlled trial. Medical Education, 41(1), 23–31. https://doi.org/10.1111/j.1365-2929.2006.02644.x
- Kirschner, P. A., Sweller, J., & Clark, R. E. (2006). Why minimal guidance during instruction does not work. Educational Psychologist, 41(2), 75–86.
- Larsen, D. P., Butler, A. C., & Roediger, H. L. (2008). Test-enhanced learning in medical education. Medical Education, 42(10), 959–966. https://doi.org/10.1111/j.1365-2923.2008.03124.x
- Mager, R. F. (1962). Preparing objectives for programmed instruction. Fearon.
- Masters, K. (2023). Ethical use of artificial intelligence in health professions education: AMEE Guide No. 158. Medical Teacher, 45(6), 574–584. https://doi.org/10.1080/0142159X.2023.2186203
- McGaghie, W. C., Issenberg, S. B., Cohen, E. R., Barsuk, J. H., & Wayne, D. B. (2011). Does simulation-based medical education with deliberate practice yield better results than traditional clinical education? A meta-analytic comparative review of the evidence. Academic Medicine, 86(6), 706–711. https://doi.org/10.1097/ACM.0b013e318217e119
- NBME. (2020). NBME item-writing guide: Constructing written test questions for the health sciences (6th ed.). https://www.nbme.org/educators/item-writing-guide
- Norman, G. R., & Schmidt, H. G. (1992). The psychological basis of problem-based learning: A review of the evidence. Academic Medicine, 67(9), 557–565.
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. Psychological Science, 17(3), 249–255. https://doi.org/10.1111/j.1467-9280.2006.01693.x
- Schmidt, H. G. (1983). Problem-based learning: Rationale and description. Medical Education, 17(1), 11–16. https://doi.org/10.1111/j.1365-2923.1983.tb01086.x
- Schmidt, H. G., & Rikers, R. M. J. P. (2007). How expertise develops in medicine: Knowledge encapsulation and illness script formation. Medical Education, 41(12), 1133–1139. https://doi.org/10.1111/j.1365-2923.2007.02915.x
- Schwartz, D. L., & Bransford, J. D. (1998). A time for telling. Cognition and Instruction, 16(4), 475–522.
- Sinha, T., & Kapur, M. (2021). When problem solving followed by instruction works: Evidence for productive failure. Review of Educational Research, 91(5), 761–798. https://doi.org/10.3102/00346543211019105
- Steenhof, N., Woods, N. N., Van Gerven, P. W. M., & Mylopoulos, M. (2019). Productive failure as an instructional approach to promote future learning. Advances in Health Sciences Education, 24(4), 739–749. https://doi.org/10.1007/s10459-019-09895-4
- Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. Cognitive Science, 12(2), 257–285. https://doi.org/10.1207/s15516709cog1202_4
- ten Cate, O. (2005). Entrustability of professional activities and competency-based training. Medical Education, 39(12), 1176–1177. https://doi.org/10.1111/j.1365-2929.2005.02341.x
- Thomas, P. A., Kern, D. E., Hughes, M. T., & Chen, B. Y. (Eds.). (2016). Curriculum development for medical education: A six-step approach (3rd ed.). Johns Hopkins University Press.
- Tolsgaard, M. G., et al. (2023). The fundamentals of artificial intelligence in medical education research: AMEE Guide No. 156. Medical Teacher, 45(6), 565–573.
- UNESCO. (2024). AI competency framework for teachers.
- van der Vleuten, C. P. M. (1996). The assessment of professional competence: Developments, research and practical implications. Advances in Health Sciences Education, 1(1), 41–67.
- van der Vleuten, C. P. M., & Schuwirth, L. W. T. (2005). Assessing professional competence: From methods to programmes. Medical Education, 39(3), 309–317.
- van Merriënboer, J. J. G., & Sweller, J. (2010). Cognitive load theory in health professional education: Design principles and strategies. Medical Education, 44(1), 85–93. https://doi.org/10.1111/j.1365-2923.2009.03498.x
<!-- REFERENCES:END -->
