# Kol mokausi gyventi — chapter 1 editorial state

Source: user-provided Kol_mokausi_gyventi_B1(1).pdf, 60 pages, 18 chapters. Preserve its B1 orientation, narrator Ana and Russian teaching support. This is source adaptation, not generation of a new story.

## Completed text work
Canonical books/kol-mokausi-gyventi.json contains the complete narrative of chapter 1, Svetimas raktas (PDF pages 5–6): 57 sentence items, 327 Lithuanian word occurrences, and 327 local word explanations. Every sentence has a Russian translation. Whitespace-normalized narrative matches the source PDF extraction exactly. Shelf title indicates one chapter, not the whole book.

User requests sentence-level clicking and explanation of every word, so sentence length and inclusion of function words intentionally follow this request over generic phrase-size guidance. Do not shorten long sentences or omit repeated-word explanations. Long tooltip usability still needs browser verification.

Reviewed contextual distinctions: mama as nominative vs vocative; ranka as instrumental; nori as second-person question; savųjų as definite possessive form with an omitted noun; indefinite vs concessive nors; mokėti as paying; noun aukštas; partitive/negative genitive; temporal accusative; adjective–noun agreement; participles and pusdalyvis. No independent native-editor review is claimed.

## Not yet complete for release
VDU browser form is now accessible. Chapter 1 narrative has automatic VDU accents in the canonical reader JSON. All 18 narrative chapters (5,947 word tokens) have been processed and checkpointed in author-plans/kol-mokausi-gyventi-vdu.json. Each output matches its source exactly after removing only U+0300/U+0301/U+0303 and normalizing Unicode; Lithuanian letter diacritics were preserved. Output is automatic and still needs contextual accent review. Practice sections, chapter titles and dictionary-note lemmas are not included in this accent checkpoint. No Azure credentials are configured, and no audio exists. The current narrator voice is hardcoded Leonas in the inherited generator: make it configurable before choosing Ona for Ana, and review male/female dialogue plus narrator insertions. Do not change block types to force casting. Verify narration separately: the generator removes written stress marks before synthesis.

Browser QA remains pending because local Chromium is missing. The inherited reader logic has 20 passing focused JS tests and 9 passing Python tests. Full tests involving other books and their media are not claimed. JSON integrity, per-word note coverage, source fidelity and catalog counts are checked.

Publish only after stress/audio/UI work is complete; keep the PR in draft. Then continue chapter 2. Original chapter-1 practice is preserved below for a separate future exercise view; it is not yet rendered by the existing reader. Do not mix Russian practice instructions into Lithuanian narrative items.

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

## Chapter 2 draft checkpoint
Complete source narrative Prašau pakartoti is now in canonical JSON: 64 clickable units and 338 word occurrences, each with a local Russian explanation and each unit with a translation. Quote/signature and dialogue-author boundaries were manually adjusted. The narrator's intentional pirkau… duona error is preserved and explained. All source words and punctuation match the PDF extraction after whitespace and stress normalization. Common forms inherited verified chapter-one corrections only when grammatical role matched. Chapter-two accent output otherwise remains automatic; note accents and full contextual stress review remain pending. No chapter-two audio or publication is claimed. Catalog now counts 665 words across two chapters.

Chapter-one flagged glossary homographs were resolved with VDU morphology and kirtis.info; detailed evidence is in chapter-one-accent-review.json. This does not certify the full book's automatic accents. Continue with chapter-two accent review, narrator configuration and audio when Azure credentials are available; keep the PR draft until release checks pass.
