# Kol mokausi gyventi — whole-book processing state

Source: user-provided Kol_mokausi_gyventi_B1(1).pdf, 60 pages, 18 chapters, 5,947 narrative word tokens. Preserve B1 level, narrator Ana, original plot, punctuation, and Russian teaching support. This is adaptation of the supplied source, not a new story.

## Current request and scope

The user requests processing the WHOLE book, without asking for permission after each chapter. User requests sentence-level clicking and an explanation for EVERY word, including repeated and function words; these explicit requests override generic phrase limits. Do not present the accent checkpoint as complete translations, grammar notes, audio, or publication.

## Canonical reader content

books/kol-mokausi-gyventi.json still has TWO complete draft narrative chapters: chapter 1 Svetimas raktas (57 units, 327 words) and chapter 2 Prašau pakartoti (64 units, 338 words). Each unit has a Russian translation; every word has a local lemma/grammar explanation. Source fidelity and counts were checked. Catalog remains two chapters / 665 words intentionally.

Chapter-two intentional “pirkau… duona” learner error is preserved and explained. Chapter-one and chapter-two review evidence is in their respective accent-review JSON files. Those reviews are contextual, not independent native-editor certification.

## Whole-book accent pass

Raw VDU output remains untouched in kol-mokausi-gyventi-vdu.json.
New kol-mokausi-gyventi-accented.json contains all 18 original narratives, accentuated titles, per-chapter status, counts and targeted contextual corrections.
New kol-mokausi-gyventi-accent-audit.json preserves morphology evidence, rules, all 365 changed narrative occurrences relative to initial VDU output, and all 45 currently unaccented narrative occurrences.
A readable text export is drafts/kol-mokausi-gyventi-accented.txt.

Of 365 changes, 55 inherit the previously corrected canonical chapters 1–2; 310 were made during the whole-book pass, including removal of 8 unsupported infinitive accent choices. All narrative words and punctuation exactly match the extracted source after removing ONLY U+0300/U+0301/U+0303 and normalizing Unicode/whitespace. Lithuanian spelling marks are preserved.

New morphology checks covered infinitives versus passive participles, nominative versus vocative nouns, gender/number agreement, verbs versus homographic nouns, and proper-name nominatives. Examples: kùrti, kèpti, Onà, Rasà, siū́lė, sė́dime. Context-specific exceptions are essential: chapter 6 “pečiai pakelti” retains its participle stress, chapter 8 “tris mažas vietines įmones” retains feminine plural accusative, chapter 8 “buvo viena … kita” retains neuter forms, chapter 18 “su nauja kliente” retains instrumental. Do not reuse a spelling-only correction map on future text.

Unresolved narrative occurrences: Samira 30, Samirai 4, Samiros 2; prisiminti/Prisiminti 7, priminti 1; kieno 1. Two title occurrences are also unaccented: Samira and Kieno. VDU and kirtis expose both prisimìnti/prisimiñti and primìnti/primiñti; lexical meaning needs a reliable confirming source before selecting one. The unsupported accent was removed, not guessed. Unchanged automatic accents still need further scrutiny; this is a whole-corpus targeted pass, NOT a guarantee that every remaining accent is correct.

## Remaining work

1. Prepare contextual Russian translations and complete local word explanations for chapters 3–18 directly in canonical reader JSON. Do not use an external machine translator. Do not mark these chapters complete based on the stress-only draft.
2. Finish lexical accent review, including note lemmas, unresolved words, titles, and remaining automatic text.
3. Azure narration: no credentials configured and no audio generated. Inherited generator hardcodes Leonas narrator; make narrator configurable, choose a reviewed voice/casting plan for Ana and dialogue. Keep secrets out of client/repo, use only configured F0, cache narration and cut clips locally.
4. Browser QA for long sentence tooltips, chapter selection, bookmarks and audio. Local Chromium missing; earlier focused JS tests (20) and Python tests (9) passed. No new UI/audio tests are claimed from this accent-only pass.
5. Keep PR #1 draft and do not merge/deploy until release checks are met. Do not publish an incomplete full reader as finished.

## Original practice, PDF page 7

Слова. svetimas raktas — чужой ключ; sunkus krepšys — тяжёлая
сумка; šviesus butas — светлая квартира; atrakinti — отпереть;
pasibelsti — постучать; rūpėti — быть важным, заботить.
Как устроено. Su dviem sunkiais krepšiais — с двумя тяжёлыми
сумками. Предлог su требует творительного падежа. Базовая форма:
sunkus krepšys. В форме krepšiais изменяется и прилагательное:
sunkiais.
Klausydamasi jos, supratau… — слушая её, я поняла… Klausydamasi —
возвратный pusdalyvis, женский род: слушает и понимает Ана. Jos —
родительный падеж после klausytis.
Вспомни без текста. Kodėl Ana nepakvietė Pauliaus arbatos? Ką ji
pasakė mamai apie savo jausmus? Kokius tris darbus užrašė?
Построй речь. Представь комнату после переезда. Начни с двух
сочетаний «прилагательное + существительное». Затем напиши, что
находится в комнате и что ты с этим делаешь. Достаточно четырёх
предложений.
Преобразуй. Aš klausiau muzikos. Tuo pačiu metu gaminau vakarienę.
Объедини от лица женщины.
Проверка. Klausydamasi muzikos, gaminau vakarienę. Содержание:
Ана не нашла чашки; маме призналась, что ей страшно; записала
покупки, поиск курсов и адрес.

