# L04: retrieval

## Прогноз до прогону: retrieval-кейси на профілі `lesson-04`

Набір: `golden.jsonl`, `set_hash` `a68efb13403e`, 12 кейсів `RET-H01`…`RET-H12` (`layer: retrieval`).

Профіль `lesson-04` вмикає три дефекти:

- **D16** — індекс `kb_broken`: корпус сплющено і нарізано по 160 символів без огляду на секції й таблиці (129 фрагментів).
- **D17** — `top_k` 1: на кожен виклик `search_knowledge_base` модель отримує один фрагмент.
- **D05** — overlay промпта: застарілий довідник комісій (`SWIFT EUR 15.00 flat, no percentage fee`) і заборона шукати комісії переказів; разом із розділом зникає правило «не називай цифру, якої немає у фрагменті».

Як рахував: відтворив `_chunk_broken` і `_score` з `app/rag/retriever.py` офлайн і подивився, який фрагмент виходить першим на запити, схожі на ті, що пише модель (зокрема запит із трейсу вправи 1). Агента не запускав. Модель формулює запит сама і може шукати кілька разів, тому прогноз має три ступені впевненості.

## Що впаде

| Кейс | Перевірка | Чому впаде |
| --- | --- | --- |
| RET-H01 | `regex` `0.5%` + `5,000` | D16: `tariffs.md#b3` закінчується на `\| Tier 3 \| 0.5% \| EUR 5`, `,000` лежить у `#b4`, який запит не приносить (ADR 0005/0006). Модель пише «EUR 5… (cut off)» |
| RET-H02 | `regex` `0.9%` + `20,000` | D17: «look it up once» — один пошук, один фрагмент. Або `tariffs.md#b3` (є 0.9%, немає 20,000), або `limits.md#b3` (навпаки) |
| RET-H03 | `regex` `15` + `0.3%` | D05: модель не шукає і відповідає зі старого довідника «EUR 15.00 flat, no percentage fee». `0.3%` у відповіді не буде (ADR 0005: 10/10) |
| RET-H10 | `contains` `declined` | D16: «results in the case being declined» лежить у `disputes-process.md#b8`, а запит про evidence приносить `#b7`, що обривається на «corresponden…» |

## Ймовірно впаде

| Кейс | Перевірка | Чому |
| --- | --- | --- |
| RET-H04 | `contains` `settled` | речення умов розрізане: `disputes.md#b3` закінчується на «the reason code is valid», `settled` — у `#b4`. Може хибно пройти: «settled» є і в `disputes-process.md#b1`, і модель може дописати його сама |
| RET-H05 | `contains` `entire` | `fx-operations.md#b4` обривається на «would cross the allowance», «entire conversion» — у `#b5`. Конкурент `fx-guide.md#b2`/`#b3` («once the allowance is exhausted») веде до pro-rata відповіді |

## Ймовірно пройде

| Кейс | Чому |
| --- | --- |
| RET-H06 | речення про provisional credit і EUR 50 ціле в `disputes-process.md#b4`, він і виходить першим |
| RET-H11 | «Withdrawal is final; … cannot be disputed again» ціле в `disputes-process.md#b9` |
| RET-H12 | «tier change takes effect on the first calendar day» ціле в `limits-operations.md#b5`. Може пройти й хибно: «first calendar day of each month» (скидання allowance) є у `fx-operations.md#b4` |

## Залежить від запиту моделі

| Кейс | Чому |
| --- | --- |
| RET-H07 | `regulatory.md#b3` цілий, але на типові запити першим виходить `security-policy.md#b1`. Без правила «не називай цифру без джерела» модель може назвати EUR 50 з пам'яті (PSD2) — тоді кейс пройде без retrieval |
| RET-H08 | запит зі словами «card payments … count … limit» приносить `limits-operations.md#b1` (пройде); запит зі словом «fees» — `fees-detail.md#b5`, де про картки нічого (впаде) |
| RET-H09 | запит зі словом «escalation» приносить `escalation-policy.md#b1` (пройде); запит «fraudulent transaction» — таблицю `limits.md#b3` (впаде). Базовий промпт може ескалювати й без фрагмента |

## Підсумок

Очікую **3–6 з 12**: впевнено падають H01, H02, H03, H10; H04 і H05 радше падають; H06, H11, H12 радше проходять; H07, H08, H09 — монетка.

Окремо стежу за хибними проходженнями: H04, H07 і H12 можуть пройти без правильного фрагмента, бо `contains` бачить лише текст відповіді. Таке проходження перевіряю по трейсу: чи був у `tool.result` фрагмент із `reference`.
