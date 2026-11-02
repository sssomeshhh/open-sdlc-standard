# 15. User experience

- **ID prefix:** UX
- **Status:** draft, 2026-10-31

## Purpose
A product that some people cannot use, that shows text in the wrong language or format, or that fails with messages nobody can act
on, does not meet its purpose and can breach accessibility law. This area sets the bar for accessibility, internationalisation,
error messages, help and usability testing, so that people "succeed first time, with the minimum of help" [GOVUK-P4].

## Scope
Covers accessibility requirements and conformance, applicable accessibility law, language declaration and internationalisation of
the user interface, user-facing and API error messages, design systems, in-app help and user documentation, and usability testing.

Left to other areas:
- How and when accessibility tests run (automated checks, manual test passes) and other test types: see Area 4.
- User research during discovery, acceptance criteria and UAT sign-off: see Area 1.
- Character encoding of stored and exchanged data: see DAT-8 (Area 14).
- API design and versioning: see Area 2. A consistent machine-readable API error format (RFC 9457 Problem Details): see ARC-8
  (Area 2); this area keeps only the rule against exposing internals (UX-10).
- Release notes, user training and the support model: see Area 20.

## Requirements

### UX-1 · MUST · WCAG 2.2 Level AA
Web user interfaces MUST conform to WCAG 2.2 Level AA.
- **Gate:** G3
- **Evidence:** the conformance report (scope, date, method, results, exceptions) published under UX-15.
- **Basis:** [WCAG22], [GOVUK-ACC], [WAIC-JIS2016], [GIHYO-JIS] (secondary source; revision status not confirmed with the standards
  body). Level: author's judgement (the GOV.UK source mandates WCAG 2.2 AA for UK public-sector services only).
- Note: success criteria that are often missed include 4.1.3 Status Messages and 3.3.8 Accessible Authentication (Minimum).
- Note: where conformance to Japan's JIS X 8341-3 is to be stated: the current edition, JIS X 8341-3:2016, is identical to
  ISO/IEC 40500:2012, which is WCAG 2.0, not 2.2. A revision based on ISO/IEC 40500:2025 (as reported by [GIHYO-JIS]) was expected
  in 2026 but its publication is unconfirmed; check the current edition before stating conformance.

### UX-2 · MUST · Human evaluation behind any accessibility claim
An accessibility conformance claim MUST rest on knowledgeable human evaluation (for example keyboard-only and screen-reader checks)
in addition to automated tools, so that automated results alone are never presented as conformance. Test planning: see Area 4.
- **Gate:** G3
- **Evidence:** a manual evaluation record for the release the claim covers, alongside automated results.
- **Basis:** [WAI-EVAL].

### UX-3 · MUST · Identify applicable accessibility law
The project MUST record which accessibility laws apply to it, separately for customer-facing services and for tools used by its
own staff, confirmed by legal review.
- **Gate:** G0
- **Evidence:** an accessibility policy naming the applicable laws and the audience each covers; a record of the legal review.
- **Basis:** [CAO-SABEKAI], [SABEKAI] Art. 8(2), Art. 13, [KOYO] Art. 36-3 (jurisdiction-specific examples; applicability needs legal
  review). Level: author's judgement.
- Note: example (Japan; the author's unofficial summary, not legal advice): under Art. 8(2) of the Act for Eliminating
  Discrimination against Persons with Disabilities (障害者差別解消法), mandatory for businesses since 2024-04-01, businesses are required
  to provide reasonable accommodation when a disabled person has expressed the need for the removal of a social barrier (意思の表明)
  and the burden is not excessive (負担が過重でないとき). For measures an employer takes toward its own workers, Art. 13 of that Act defers
  to the Act on Employment Promotion of Persons with Disabilities (障害者雇用促進法), whose Art. 36-3 requires necessary measures for
  disabled workers unless they place an excessive burden (過重な負担) on the employer. Neither law names WCAG; that they require WCAG
  conformance is an inference that needs legal review.

### UX-4 · SHOULD · Include disabled people in research
User research and usability testing SHOULD include disabled people and people who use assistive technologies.
- **Gate:** G3
- **Evidence:** the research plan or participant log showing such participants.
- **Basis:** [GOVUK-ACC].

### UX-5 · MUST · Declared page language
Each page MUST declare its default language with a `lang` attribute on the `html` element, using a BCP 47 tag, with passages in
another language marked with their own `lang`. This matters most for multilingual content (for example a page mixing two
languages), which screen readers otherwise read with the wrong rules.
- **Gate:** G3
- **Evidence:** HTML source; results of checks for WCAG 3.1.1 and 3.1.2.
- **Basis:** [WCAG22], [W3C-LANG], [W3C-ISPECS].

### UX-6 · MUST · User-visible strings outside code
In a product that supports, or plans to support, more than one language, user-visible strings MUST be kept in resource files
separate from source code.
- **Gate:** G2
- **Evidence:** i18n resource files per locale; a lint rule or search showing no hard-coded user-facing text in components.
- **Basis:** [W3C-I18N]. Content: author's judgement (the source defines internationalisation and lists separating localizable
  elements as part of it; it does not prescribe resource files).

### UX-7 · SHOULD · No sentences built from fragments
User-visible sentences SHOULD be built with a message format that handles plurals and word order per locale, not by concatenating
translated fragments.
- **Gate:** G2
- **Evidence:** message-format usage (for example ICU MessageFormat) in resource files; no string concatenation of translated
  fragments in code.
- **Basis:** [W3C-ISPECS], [W3C-I18N].

### UX-8 · SHOULD · Locale-aware formatting at display
Dates, times, numbers and names SHOULD be formatted per the user's locale at display time, from locale-neutral stored values (date/
time storage: see DAT-9).
- **Gate:** G2
- **Evidence:** use of locale-aware formatting APIs (for example `Intl` or a CLDR-based library); no hard-coded display formats.
- **Basis:** [W3C-I18N]. Level: author's judgement (the source defines internationalisation; it does not state this rule).

### UX-9 · MUST · Clear input-error messages
When an input error is detected, the field in error MUST be identified and the error described in text, saying what went wrong and
how to fix it, in plain language without technical jargon or error codes.
- **Gate:** G3
- **Evidence:** screenshots of validation states; an error-message content guide.
- **Basis:** [WCAG22] (3.3.1) for identifying the field and describing the error in text; [GOVUK-ERR] for how to fix it and
  plain language. The plain-language and how-to-fix parts come from the GOV.UK Design System, not from WCAG 3.3.1; applying them
  to every product: author's judgement.

### UX-10 · MUST · No internals in error responses
Error responses, in the UI and in APIs, MUST NOT expose stack traces or other implementation details.
- **Gate:** G2
- **Evidence:** sample error responses from a production-like environment; production configuration with debug output off.
- **Basis:** [RFC9457].

### UX-11 · SHOULD · Shared design system
The user interface SHOULD be built from a shared design system (components, patterns and design tokens) that has been tested for
accessibility and usability.
- **Gate:** G1
- **Evidence:** the component library dependency or package; a pattern catalogue; its accessibility test record.
- **Basis:** [GOVUK-DS], [DADS].

### UX-12 · MAY · Reuse a public design system
Instead of building its own, a project MAY adopt or extend an existing, publicly documented design system that has been
researched and tested by others.
- **Gate:** G1
- **Evidence:** the adopted design system named in the project documentation.
- **Basis:** [GOVUK-DS], [DADS].

### UX-13 · SHOULD · User documentation and in-app help
User documentation SHOULD exist for the main user tasks, with help (contact details, help pages) reachable from the product in
the same place on every page.
- **Gate:** G3
- **Evidence:** the help pages; a UI review showing the help link in a consistent location.
- **Basis:** Author's judgement (no primary source quoted); the consistent-location part is also WCAG 2.2 success criterion 3.2.6,
  covered by UX-1.

### UX-14 · SHOULD · Usability testing of main journeys
The main user journeys SHOULD be usability-tested with actual or potential users before release and again at an interval the
project sets, with findings tracked to a fix or a recorded decision.
- **Gate:** G3 · **Trigger:** each release that changes a main user journey
- **Evidence:** the testing interval, recorded in the research or test plan; test plans, session notes, findings and the resulting
  changes.
- **Basis:** [GOVUK-P4], [GOVUK-UT].

### UX-15 · MUST · Accessibility conformance statement
The project MUST publish or keep an accessibility conformance statement giving its scope, test date and known exceptions.
- **Gate:** G3
- **Evidence:** the statement or report (scope, date, method, results, exceptions).
- **Basis:** [GOVUK-ACC]. Level: author's judgement (the GOV.UK source requires a statement for UK public-sector services only).

## Failure modes
- Relying on an automated checker alone and calling the product accessible [WAI-EVAL].
- Treating accessibility as a late audit instead of designing for it from the start [GOVUK-ACC], [WAI-EVAL].
- Missing or wrong `lang` on multilingual pages, so screen readers read one language with another language's rules [W3C-LANG].
- Building sentences by concatenating translated fragments, which breaks in languages with a different word order [W3C-ISPECS].
- Generic or technical error messages ("unspecified error", error codes) with no way to fix them [GOVUK-ERR]; stack traces in API
  responses [RFC9457].
- Assuming an accessibility law applies in the same way to every audience, without checking the employment-law route
  [SABEKAI] Art. 13.

## References
- **[CAO-SABEKAI]** 「リーフレット『令和６年４月１日から合理的配慮の提供が義務化されました』」. Cabinet Office (内閣府), Japan.
  https://www8.cao.go.jp/shougai/suishin/sabekai_leaflet-r05.html. Accessed 2026-10-31. Jurisdiction-specific example;
  applicability needs legal review.
  > "令和３年に障害者差別解消法が改正され、事業者による障害のある人への合理的配慮の提供が義務化されました。"
- **[DADS]** デジタル庁デザインシステムβ版 (v2.18.2). Digital Agency (デジタル庁), Japan. https://design.digital.go.jp/.
  Accessed 2026-10-31.
  > "ユーザビリティとアクセシビリティを踏まえた設計や実装のためのガイドラインから構成されるデザインアセットです。"
- **[GIHYO-JIS]** 「2026年のWebアクセシビリティ」, 2026-01-06. 中村直樹, gihyo.jp.
  https://gihyo.jp/article/2026/01/web-accessibility-prospect. Accessed 2026-10-31. Secondary source by a practitioner; the
  revision's publication status was not confirmed with the standards body.
  > "改正JISは、JIS X 8341-3:2016と同様に、ISO/IEC 40500:2025との国際一致規格とすることを基本として考えています。" (改正JISの動向)
  > "順調にいけば、今年中にも改正JISが発行される見込みです。" (改正JISの動向)
- **[GOVUK-ACC]** "Making your service accessible: an introduction", GOV.UK Service Manual. Government Digital Service.
  https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction.
  Accessed 2026-10-31.
  > "meet level AA of the Web Content Accessibility Guidelines (WCAG) 2.2 as a minimum" (How to meet government accessibility requirements)
  > "When doing research, you need to include disabled people and people who use assistive technologies." (Do research with disabled users)
  > "have an accessibility statement that explains how accessible the service is" (How to meet government accessibility requirements)
- **[GOVUK-DS]** GOV.UK Design System. Government Digital Service. https://design-system.service.gov.uk/. Accessed 2026-10-31.
  > "Learn from the research and experience of other service teams and avoid repeating work that’s already been done."
- **[GOVUK-ERR]** "Error message" component, GOV.UK Design System. Government Digital Service.
  https://design-system.service.gov.uk/components/error-message/. Accessed 2026-10-31.
  > "Describe what has happened and tell them how to fix it." (Be clear and concise)
  > "The message must be in plain English, use positive language and get to the point." (Be clear and concise)
  > "technical jargon like ‘form post error’, ‘unspecified error’ and ‘error 0x0000000643’" (Be clear and concise)
- **[GOVUK-P4]** "4. Make the service simple to use", GOV.UK Service Standard. Government Digital Service.
  https://www.gov.uk/service-manual/service-standard/point-4-make-the-service-simple-to-use. Accessed 2026-10-31.
  > "test for usability frequently with actual and potential users, using appropriate research techniques" (What it means)
  > "so that people succeed first time, with the minimum of help" (What it means)
- **[GOVUK-UT]** "Using moderated usability testing", GOV.UK Service Manual. Government Digital Service.
  https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing. Accessed 2026-10-31.
  > "Moderated usability testing is where you watch participants try to complete specific tasks using your service."
- **[KOYO]** 障害者の雇用の促進等に関する法律. e-Gov (法令ID 335AC0000000123).
  https://laws.e-gov.go.jp/law/335AC0000000123. Accessed 2026-10-31. Jurisdiction-specific example; applicability needs legal
  review.
  > "その雇用する障害者である労働者の障害の特性に配慮した職務の円滑な遂行に必要な施設の整備、援助を行う者の配置その他の必要な措置を講じなければならない。" (Art. 36-3)
  > "ただし、事業主に対して過重な負担を及ぼすこととなるときは、この限りでない。" (Art. 36-3)
- **[RFC9457]** RFC 9457, *Problem Details for HTTP APIs*, July 2023 (obsoletes RFC 7807). IETF.
  https://www.rfc-editor.org/rfc/rfc9457. Accessed 2026-10-31.
  > "This document obsoletes RFC 7807." (abstract)
  > "avoid making implementation details such as a stack dump available through the HTTP interface" (5. Security Considerations)
- **[SABEKAI]** 障害を理由とする差別の解消の推進に関する法律. e-Gov (法令ID 425AC0000000065).
  https://laws.e-gov.go.jp/law/425AC0000000065. Accessed 2026-10-31 (Art. 8(2) and Art. 13 via the e-Gov API). Jurisdiction-specific
  example; applicability needs legal review.
  > "事業者は、その事業を行うに当たり、障害者から現に社会的障壁の除去を必要としている旨の意思の表明があった場合において、その実施に伴う負担が過重でないときは、障害者の権利利益を侵害することとならないよう、当該障害者の性別、年齢及び障害の状態に応じて、社会的障壁の除去の実施について必要かつ合理的な配慮をしなければならない。" (Art. 8(2))
  > "行政機関等及び事業者が事業主としての立場で労働者に対して行う障害を理由とする差別を解消するための措置については、障害者の雇用の促進等に関する法律（昭和三十五年法律第百二十三号）の定めるところによる。" (Art. 13)
- **[W3C-I18N]** "Localization vs. Internationalization". W3C Internationalization.
  https://www.w3.org/International/questions/qa-i18n. Accessed 2026-10-31.
  > "Internationalization is the design and development of a product, application or document content that enables easy localization for target audiences that vary in culture, region, or language." (introduction)
  > "taking care over the concatenation of strings" (introduction)
  > "Separating localizable elements from source code or content" (introduction)
- **[W3C-ISPECS]** *Internationalization Best Practices for Spec Developers*, W3C Group Note, 7 August 2026. W3C.
  https://www.w3.org/TR/international-specs/. Accessed 2026-10-31.
  > "Specifications SHOULD NOT require the concatenation of string values to form natural language or displayable string values." (6. Text-processing)
  > "Values for language declarations must use BCP 47." (2. Language)
- **[W3C-LANG]** "Declaring language in HTML". W3C Internationalization.
  https://www.w3.org/International/questions/qa-html-language-declarations. Accessed 2026-10-31.
  > "Always use a language attribute on the html tag to declare the default language of the text in the page."
- **[WAI-EVAL]** "Evaluating Web Accessibility Overview". W3C Web Accessibility Initiative. https://www.w3.org/WAI/test-evaluate/.
  Accessed 2026-10-31.
  > "However, no tool alone can determine if a site meets accessibility standards. Knowledgeable human evaluation is required to determine if a site is accessible."
- **[WAIC-JIS2016]** 「JIS X 8341-3:2016 解説」. ウェブアクセシビリティ基盤委員会 (WAIC). https://waic.jp/docs/jis2016/understanding/201604/.
  Accessed 2026-10-31. States that JIS X 8341-3:2016 is identical to ISO/IEC 40500:2012 (WCAG 2.0).
  > "『JIS X 8341-3:2016』は、『ISO/IEC 40500:2012』の一致規格になっている。"
- **[WCAG22]** *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 12 December 2024. W3C.
  https://www.w3.org/TR/WCAG22/. Accessed 2026-10-31.
  > "If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text." (Success Criterion 3.3.1 Error Identification)
  > "The default human language of each web page can be programmatically determined." (Success Criterion 3.1.1 Language of Page)
  > "can be presented to the user by assistive technologies without receiving focus." (Success Criterion 4.1.3 Status Messages)
  > "A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless that step provides at least one of the following" (Success Criterion 3.3.8 Accessible Authentication (Minimum))
