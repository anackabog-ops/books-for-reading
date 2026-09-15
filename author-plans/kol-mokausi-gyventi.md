# Kol mokausi gyventi — complete narrative adaptation, release pending

Updated 2026-09-15. User requests the whole supplied B1 book, sentence-level clicking and a local explanation for EVERY word. These requirements override the generic phrase-size and optional-function-word guidelines. Do not ask for chapter-by-chapter permission.

## Canonical content

books/kol-mokausi-gyventi.json now contains all 18 narrative chapters, 963 clickable sentence/quotation units and 5,947 Lithuanian word occurrences. Every unit has an agent-authored Russian translation. Every occurrence, including repeated and function words, has a separate local lemma/gloss/form explanation. Chapters 3–18 add 842 units and 5,282 word explanations. The original intentional learner error in chapter 2 is preserved.

The full narrative exactly matches the extracted PDF after removing only stress marks U+0300/U+0301/U+0303 and normalizing whitespace/Unicode. Chapter counts: 327, 338, 328, 316, 331, 327, 334, 325, 322, 329, 323, 316, 343, 324, 336, 339, 346, 343. Catalog now describes the full 5,947-word book. Labels are I–XVIII. Source practice is preserved in each chapter and rendered in collapsible Praktika panels. PDF pages 59–60 are preserved in the final sources/notes appendix. Exercises and appendix are not counted as narrative or narrated.

A manually authored lexicon and productive morphology were used as editing aids, followed by sentence-specific selection of ambiguous forms. Canonical JSON is the source of truth. Do not regenerate notes from surface spellings alone. Reviewed distinctions include nominative/instrumental feminine forms, accusative adjective gender, relative pronouns, second/third-person verbs, noun/verb homographs, comparative lemmas, adverbs versus adjective dative forms, help/put, meet/agree, pay/know, and participial constructions. Examples requiring preservation: chapter 6 pečiai pakelti is a passive participle; chapter 12 ant kelių refers to knees; chapter 16 siūtų daiktų is a passive participle, not a conditional verb; chapter 18 su nauja kliente is instrumental. Independent native-language editorial certification is not claimed.

## Accents

Raw VDU output remains unchanged. The accented-text and audit JSON preserve the earlier 365 corrections and a separate lexical follow-up. Dictionary evidence resolved prisimiñti, primiñti and kienõ (9 narrative occurrences). Remaining unaccented narrative words are Samira (30), Samirai (4), Samiros (2), plus Samira in one chapter title. The author confirmed Сами́ра (stress on i) on 2026-09-15. This pronunciation decision is recorded; applying Lithuanian accent notation consistently to the name and its inflected forms and checking the synthesized pronunciation remain pending.

Unchanged VDU output is not certified correct in every position. Note surfaces inherit narrative accents; lemma accents are reused only when previously checked, otherwise lemma spelling is unaccented. Source practice remains as supplied. Do not describe the book as independently proofread or every string as fully accented.

## Audio preparation

The generator now supports narratorVoice and explicit blockVoices, with exact narratorSpans. The all-chapter casting file uses Ona for Ana and female speech, Leonas for 47 reviewed male dialogue blocks, and Ona for narrator insertions. Reported speech and quoted written messages remain narration. Do not infer casting merely from block.type.

scripts/generate-book-audio.py processes all chapters sequentially and stops on failure. --prepare-only creates SSML without Azure calls. All 18 SSML documents parse, preserve spoken narrative and have exactly one bookmark per reader unit (963 total). Reference numbers are deliberately not spoken. Existing cache, F0 guard, MP3 cutting and manifests are preserved. There are NO generated MP3 files and NO configured Azure credentials in the workspace.

Command from repository root:

```bash
python scripts/generate-book-audio.py books/kol-mokausi-gyventi.json --casting author-plans/kol-mokausi-gyventi-casting.json --work-dir /tmp/kol-mokausi-speech --prepare-only
```

After configuring the existing private F0 credentials file, remove --prepare-only. Credentials must never enter Git or client files. Review pronunciation and synchronization before deployment.

## Verification and release gates

11 Python tests and 19 focused JavaScript tests pass. JavaScript syntax checks pass. The standard item cleaner reports zero changes. Complete source equality, per-word note coverage, Russian translations, JSON structure, all 18 casting plans and XML/bookmark coverage pass. See the verification JSON for exact counts and limitations.

On 2026-09-15, a fresh complete checkout of head 992c122 was verified: all 25 JavaScript tests (including the other-book audio regression) and all 11 Python tests passed. Both JavaScript syntax checks passed; the standard cleaner made zero changes. Fresh prepare-only generation and verification passed for all 18 SSML documents, 963 units and 5,947 word explanations. No Azure requests were made and no MP3s were generated for this book. These structural checks do not certify linguistic accuracy.

The remote browser rejected the local HTTP preview with net::ERR_BLOCKED_BY_CLIENT on 2026-09-15, so visual/mobile QA remains pending; no successful browser screenshot check is claimed. Shared tooltip already provides bounded scrolling. GitHub secret presence was verified previously, but credential validity, Speech resource ownership and actual F0 tier remain unverified. The user's Azure signup is currently blocked at the verification step. Do not dispatch narration until the actual resource and F0 tier are confirmed.

Keep PR #1 draft. Remaining release work: apply the confirmed Samira pronunciation, independently check remaining automatic accents/linguistic notes as appropriate, configure Azure F0 and generate/listen/check all audio, verify the actual mobile reader, then merge and deploy only after release checks. Do not call this an audio-complete or published release.
