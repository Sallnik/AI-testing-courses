# Multi-turn Test Plan + Degradation Profile — шаблон

**Додатковий матеріал до заняття 5 «Context failure у діалозі».**

Це робоча форма на всю тему. Ви почнете заповнювати її на лабораторній, а в ДЗ_4 доповните й здасте. Біля кожного розділу вказано, коли його заповнювати і де в темі розібрано, що туди писати. Після курсу той самий шаблон підходить для діалогової системи вашої команди.

## Як користуватися

1. Перед лабораторною скопіюйте шаблон собі й назвіть `multi-turn-test-plan.md`. На лабораторній записуйте результати прямо в нього.
2. У ДЗ_4 покладіть цей самий файл у репозиторій і допишіть розділи з позначкою «ДЗ». Числа з лабораторної можна лишити, якщо в них є входи кожного кроку.
3. Під кожним розділом є рядок «Заповнюєте»:
    - **Лабораторна** — заповнюєте під час відповідного кроку лабораторної;
    - **ДЗ** — заповнюєте вдома, у названому кроці ДЗ_4.
4. Рядки-підказки курсивом після заповнення можна видалити.

## Що робить цей документ документом рішення

- кожне твердження про механізм збою спирається на **входи кроку**: історію і retrieval-контекст; текст відповіді доказом не вважається;
- крок втрати подано **розподілом** щонайменше за п'ятьма прогонами;
- тест-план називає **обрані сценарії, свідомо непокрите і ціну покриття**;
- останній рядок відповідає на питання «що обміняли · чого не робимо · за яких умов рішення зміниться».

## Карта розділів

| Розділ | Лабораторна | ДЗ_4 |
| --- | --- | --- |
| 1. Контекст і прогноз | прогноз перед стартом | крок 1 |
| 2. Профіль деградації | кроки «Прогнати той самий діалог», «Повторити сценарій п'ять разів», «Скоротити й подовжити сценарій» | крок 2 |
| 3. Механізми збою | кроки «Знайти крок втрати й довести причину», «Знайти й класифікувати самосуперечність» | крок 3 |
| 4. Інваріанти й оракули | крок «Написати дві інваріант-перевірки» | крок 4 |
| 5. Тест-план і ціна | — | крок 5 |
| 6. Залишковий ризик і рішення | — | крок 6 |
| Останній рядок | — | крок 6 |

Діалогові кейси (крок 7 ДЗ) ви записуєте у файл `l05_dialogs.jsonl`, тому окремого розділу для них тут немає.

---

## 1. Контекст і прогноз

*Заповнюєте:* **Лабораторна** — рядок «Прогноз» перед першим кроком. **ДЗ**, крок 1 — решту рядків.

```
система             PayPilot
профілі             clean · lesson-05 (D06, D07)
модель і провайдер  claude-haiku-5-5 · anthropic (з трейсів: gen_ai.request.model, llm.provider)
основний сценарій   CONV-002 за скаргою C-18 (у шаблоні — C-07), 7 кроків, клієнт CUS-0004
набір               l05_dialogs.jsonl, 6 кейсів · set_hash b51aabd09561
дата прогонів       22.10.2026 (лабораторна) · 24.10.2026 (серії v1, v2, контроль, l05_dialogs)
```

**Прогноз перед лабораторною:** не зафіксовано до першого прогону 22.10, тому заднім числом не заповнюю. Фактичний крок втрати суми — 3, крок згортки (розподіл у розділі 2.3).
*Записуєте до першого прогону. Наприкінці лабораторної звірите з розподілом у розділі 2.3.*

---

## 2. Профіль деградації

*У темі: «D06: згортка, яка викидає число», «Момент втрати і момент прояву», «Профіль деградації».*

### 2.1. Лист запису: контрольний прогін на `clean`

*Заповнюєте:* **Лабораторна**, крок «Прогнати той самий діалог на двох профілях».

Профіль `clean` · клієнт `CUS-0004` (кнопка «Від імені») · нова розмова.

| Крок | Репліка клієнта (скорочено) | Репліка агента (скорочено) | Сутності в історії | Retrieval-контекст кроку |
| --- | --- | --- | --- | --- |
| 1 | Transaction TX-0401, 240.00 EUR: the goods never arrived. Which reason code applies?| має залишити: reason code goods_not_received of TX-0401, has a 90-day window | - | tool.search_knowledge_base: disputes.md#s1,reason-codes.md#s6, disputes-process.md#s6, glossary.md#s4, disputes-process.md#s3 |
| 2 | Can I dispute it? | Yes, TX-0401 is eligible for a dispute under goods_not_received. Deadline: 2026-10-18 (90-day window) | Номер транзакції, reason code. Має спрацювати згортка | tool.check_dispute_eligibility: TX-0401 ... |
| 3 | daily card limit | Your daily transfer limit on file (Tier 1) is EUR 5,000.00. You have spent EUR 0.00 of it, so EUR 5,000.00 remains. Your monthly limit is EUR 50,000.00, with EUR 35.50 used and EUR 49,964.50 remaining. | Повинна бути сума, дата, вікно, але на цьому кроці ми нічого не витянували з історії | tool.get_account, tool.check_limits |
| 4 | FX spread in USD | Spread: 1.5% over the mid-market rate, applied only after the free monthly conversion allowance is used up. Free monthly conversion allowance: EUR 500, reset on the first day of each month. | підтягує використаний ліміт кредитної карти: EUR 35.50 - що є невалідними даними, але бот уточнює що він може помилятись | tool.search_knowledge_base: tariffs.md#s2, fx-operations.md#s3, fx-guide.md#s1, fees-detail.md#s2, tariffs.md#s3 |
| 5 | Back to that charge | Transaction: TX-0401, EUR 240.00, dated 2026-07-20. Reason code: goods not received. Eligibility: Eligible as of 2026-09-15. Filing deadline: 2026-10-18 | сума, ід транзакції, кінцеву дату спору, reason code | - |
| 6 | 240 euro, as I said | Yes, the amount is EUR 240.00, which matches TX-0401. should file a goods-not-received dispute for the full EUR 240.00 on TX-0401? | все ще пам'ятає ід транзакції, reason code, кінцеву дату спору та суму | - |
| 7 | still have time to file? | Yes. As of today, 2026-09-15, TX-0401 is eligible for a goods-not-received dispute, and the filing deadline is 2026-10-18. | все ще пам'ятає ід транзакції, reason code, кінцеву дату спору та суму | - |

*«Сутності в історії» — що з чотирьох параметрів справи є в історії, яку отримує модель на цьому кроці: сума · дата · reason code · вікно. Якщо історію згорнуто, напишіть «згортка» і що в ній лишилося.*

### 2.2. Лист запису: прогін на `lesson-05`

*Заповнюєте:* **Лабораторна**, той самий крок. Це прогін 1 для розподілу в 2.3.

| Крок | Репліка агента (скорочено) | Сутності в історії | Retrieval-контекст кроку | Видно у відповіді, що щось утрачено? |
| --- | --- | --- | --- | --- |
| 1 | The reason code for this case is `goods_not_received`. It covers purchases you paid for that were not delivered. | має залишити: reason code goods_not_received of TX-0401, вікна не знаю бо не викликав tool.search_knowledge_base | - | нема вікна бо агент не використав ніяких інструментів |
| 2 | Yes, TX-0401 (EUR 240.00) is eligible for a dispute under the `goods_not_received` reason code. Transaction date: 20 July 2026. Dispute window: 90 days. Deadline to file: 18 October 2026 | transaction_id, reason_code та додалось deadline та tx_date | tool.check_dispute_eligibility | ні, поки все добре |
| 3 | Your daily transfer limit on file for your tier (tier1) is EUR 5,000. Today you have spent EUR 0, so the full EUR 5,000 remains. The monthly limit is EUR 50,000, with EUR 35.50 used so far this month. | Повинна бути сума, дата, вікно, але на цьому кроці ми нічого не витянували з історії | tool.get_account, tool.check_limits | неможливо визначати, але агент відповів: The dispute for the undelivered purchase is still waiting for your confirmation. Let me know if you want me to file it. - тобто щось в історії є |
| 4 | For a tier 1 customer, the FX spread is 1.5% over the mid-market rate, after a free monthly conversion allowance of EUR 500. | Повинна бути сума, дата, вікно, але на цьому кроці ми нічого не витянували з історії | search_knowledge_base: tariffs.md#s2, fx-operations.md#s3, fx-guide.md#s1, fees-detail.md#s2, tariffs.md#s3 | The dispute for the undelivered purchase is still waiting for your confirmation. - все ще пам'ятає про спір, але деталі невідомі |
| 5 | I can see two TechMart Online card payments of EUR 240.00 each: TX-0402, 14 July 2026, settled TX-0401, 20 July 2026, settled. Which one is the purchase that wasn't delivered? Once you tell me, I'll run the dispute eligibility check on that transaction. If it's eligible, I'll open a dispute under "goods not received" only after you confirm | reason code, сума. Все інще забув | tool.get_transactions | Втрачено: транзакшин ід, вікно повернення, дедлайн вікна повернення |
| 6 | Both TechMart Online payments of EUR 240.00 are eligible for a "goods not received" dispute:TX-0402, 14 July 2026, settled. Dispute deadline: 12 October 2026. TX-0401, 20 July 2026, settled. Dispute deadline: 18 October 2026.
Both are within the 90-day window, and neither is on a compliance hold. I haven't filed anything. | сума, reason_code | tool.check_dispute_eligibility X2 | знову перевикликав тули щоб дістати інформацію |
| 7 | Yes. As of today, 15 September 2026, both deadlines are still open TX-0402 (14 July): deadline 12 October 2026 TX-0401 (20 July): deadline 18 October 2026 | все пам'ятвє, але ми йому та і ненагадали суми | - | тут маємо ситуацію в розбіжності того що забув агент і того що ми його питаємо в прогонах |

### 2.3. Крок втрати по п'яти прогонах

*Заповнюєте:* **Лабораторна**, крок «Повторити сценарій п'ять разів». **ДЗ**, крок 2 — перевіряєте або доміряєте.

Профіль `lesson-05`, кожен прогін у новій розмові.

Прогони 2–6 — ранер, кейс `CONV-002`, `summarize_after=2`, звіти в `paypilot-l05-eval/reports/7 steps/`, `set_hash 83cf9eeefa09`.

| Прогін | Крок втрати (сума зникла з історії) | Крок прояву (втрату видно у відповіді) |
| --- | --- | --- |
| 1 (з 2.2, ручний у чаті) | 3 — згортка; на кроках 3–4 агент згадує спір без жодної деталі | 5 — get_transactions, «two TechMart Online card payments of EUR 240.00 each… Which one?» |
| 2 · `l05-lesson-05-20261022T081313` | 3 — згортка; на кроці 3 агент уже каже «eligibility check passed for service_not_rendered» | 5 — get_transactions, «I can't tell from our conversation which one you mean»; на кроці 6 прямо: «The summary… doesn't include the transaction ID or amount» |
| 3 · `l05-lesson-05-20261022T084750` | 3 — згортка; TX-0401 пережив згортку, сума ні | 5 — «filed for the full transaction amount» без числа; автоперевірка D06 на кроці 5 червона |
| 4 · `l05-lesson-05-20261022T143756` | 3 — згортка | 5 — get_transactions + 2× check_dispute_eligibility, «confirm which one is the undelivered purchase» |
| 5 · `l05-lesson-05-20261022T144048` | 3 — згортка; на кроці 3 «The service_not_rendered dispute… is still on hold» | 5 — get_transactions, «I can't tell from this conversation which of these»; на кроці 6: «I can't see the start of our conversation» |
| 6 · `l05-lesson-05-20261022T144228` | 3 — згортка | 5 — get_transactions, «which charge is for the goods that never arrived»; на кроці 6: «I don't have the transaction ID from our earlier discussion» |

**Упорядкований ряд кроку втрати:** 3 · 3 · 3 · 3 · 3 · 3 (крок прояву: 5 · 5 · 5 · 5 · 5 · 5)
**Діапазон:** від 3 до 3 · **медіана:** 3 (прояв — медіана 5)
**Межа довжини, після якої пам'яті агента не довіряємо:** 2 кроки — це поріг згортки `summarize_after=2`: з кроку 3 модель бачить згортку замість історії. За замовчуванням на стенді `SUMMARIZE_AFTER_STEPS=8`, тобто межа 8 кроків.
**Прогноз із розділу 1 збігся?** *прогноз у розділі 1 ще не записано — допишіть і звірте з фактом: втрата на кроці 3, прояв на кроці 5.*

*Одне число кроку втрати не є результатом: дефект імовірнісний.*

Крок втрати однаковий у всіх прогонах, бо його задає поріг: згортка спрацьовує один раз за сесію, на вході кроку 3 (span `agent.summarize` на кроці 3 у 5/5 звітах). Від прогону до прогону змінюється інше:
- що пережило згортку: TX-0401 — 1/5 (прогін 3); reason code підмінено на `service_not_rendered`, і агент сам це озвучує в 3/5 (прогони 2, 3, 5);
- чи бачить втрату автоперевірка: D06 на кроці 5 червона лише в 1/5. У 4/5 «240» і «TX-0401» у відповіді є, але агент узяв їх із `get_transactions`, а не з пам'яті, тому перевірка дає хибно-зелений результат.

### 2.4. Профіль деградації основного сценарію

*Заповнюєте:* **Лабораторна**, крок «Скоротити й подовжити сценарій» (п. 5). **ДЗ**, крок 2 — уточнюєте за п'ятьма прогонами.

Один рядок на крок. Момент втрати і момент прояву стоять у різних рядках.

Частоти пораховано за п'ятьма звітами ранера з 2.3 (прогони 2–6).

| Крок | Що тримається | Що втрачено | Що було на вході кроку | Механізм | Видно у відповіді |
| --- | --- | --- | --- | --- | --- |
| 1 | сума 240.00, TX-0401, reason code `goods_not_received` (5/5) | — | історія: лише репліка клієнта з TX-0401 і 240.00 EUR. Інструменти: у 3/5 жодного; у 1/5 search_knowledge_base (disputes.md#s1, reason-codes.md#s6, disputes-process.md#s6, glossary.md#s4); у 1/5 check_dispute_eligibility | — (згортки ще немає) | ні, нічого не втрачено. Вікно 90 днів назване лише у 2/5, де був інструмент |
| 2 | сума, TX-0401, reason code, дата 2026-07-20, вікно 90 днів, дедлайн 2026-10-18 (5/5) | — | повна історія кроку 1; check_dispute_eligibility(TX-0401, goods_not_received) у 4/5, в 1/5 цей результат уже є в історії з кроку 1 | — | ні. У 1/5 автоперевірка кроку 2 червона через формулювання «can be disputed» без слова eligible: збій перевірки, а не пам'яті |
| 3 — **момент втрати** | намір («спір за недоставлений товар»), статус «ще не подано, чекаю підтвердження»; TX-0401 лише в 1/5 | сума 240.00 (5/5), дата, вікно, дедлайн; TX-0401 у 4/5; reason code підмінено на `service_not_rendered` | **згортка кроків 1–2** замість історії (`agent.summarize` 5/5) + питання про ліміт; get_account, check_limits (5/5) | D06: сумаризатор `lesson-05` отримує інструкцію «Do not clutter the summary with specific figures, exact amounts, dates, transaction ids or numeric codes», і модель їх викидає. D07: постобробка замінює кожен код, що вцілів, на `service_not_rendered`, а разом із D06 множить суми, що вціліли, на 0.75 (240.00 → 180.00). Обидва ефекти видно в `summary.text` (примітка під таблицею) | **ні** для суми: ліміт EUR 5 000 правильний у 5/5. Підміна коду непрохано прослизає у 3/5 («eligibility check passed for service_not_rendered») |
| 4 | те саме, що після кроку 3 | сума, дата й дедлайн в історію не повертаються | згортка + крок 3 повністю + питання про FX; search_knowledge_base у 4/5 (tariffs.md#s2, fx-guide.md#s1, fees-detail.md#s2, tariffs.md#s3), в 1/5 інструментів немає | D06 триває: на кроках 3–4 ні клієнт, ні агент суму не повторюють. В 1/5 окремо «не знайшов»: без retrieval агент не назвав 1.5% | **ні**: 1.5% правильно в 4/5, а провал в 1/5 — це збій пошуку, не пам'яті |
| 5 — **момент прояву** | намір спору; TX-0401 лише в 1/5 | яка саме транзакція (4/5); суми в пам'яті немає (5/5) — у 4/5 агент дістає 240 заново з get_transactions і бачить дві TechMart по EUR 240.00 (TX-0401, TX-0402) | згортка + кроки 3–4 + «Back to that charge»; get_transactions у 4/5 (в 1/5 ще 2× check_dispute_eligibility), check_dispute_eligibility(TX-0401) в 1/5 | D06, втрата з кроку 3: це перше звернення назад після двох перемикань теми | **так**, 5/5 для людини: «which one is the purchase…» або «full transaction amount» без числа. Автоперевірка D06 червона лише 1/5 |
| 6 | сума знову в історії (від клієнта + результат get_transactions з кроку 5) | TX-0401 досі втрачено у 4/5: сума 240 не розрізняє TX-0401 і TX-0402 | згортка + кроки 3–5 разом із результатами інструментів + «240 euro, as I said»; get_transactions в 1/5, в інших 4/5 інструментів немає | D06. Агент сам описує свій вхід: «The summary… doesn't include the transaction ID or amount», «I can't see the start of our conversation» | **так**, явно: у 3/5 агент прямо каже, що згортка не містить ID чи суми |
| 7 | дедлайн 2026-10-18 для TX-0401 назване в 5/5, але відновлене з інструментів, а не з пам'яті | який із двох платежів спірний: у 4/5 агент дає два дедлайни (TX-0402 → 2026-10-12, TX-0401 → 2026-10-18) і просить обрати | згортка + кроки 3–6; 2× check_dispute_eligibility у 2/5, search_knowledge_base в 1/5, у 2/5 інструментів немає (дедлайни вже в історії з кроку 5) | наслідок D06. Слід D07 в 1/5: «The window is the same for service_not_rendered» | **частково**: «Yes, you still have time» виглядає правильно, автоперевірка D07 зелена 5/5. Втрату видно лише з того, що агент тримає дві транзакції |

**Момент втрати:** крок 3 · **момент прояву:** крок 5
**Кроків із «Видно у відповіді — ні»:** 2 — кроки 3 і 4: сума вже зникла, а відповіді про ліміт і FX правильні. Для автоперевірок прихований ще крок 7: D07 зелена в 5/5, хоча агент не знає, яка транзакція клієнта.

*Звіти основного сценарію 22.10 зняті без `--traces`, тому текст згортки для них взято з прогонів 2.5. Кроки 1–2 там ті самі, що в основному сценарії, тож згортка на кроці 3 будується з тих самих входів. У 10 з 10 `summary.text` (`reports/traces/20261022T151022/*-turn3.json`, span `agent.summarize`) немає ні 240, ні TX-0401, ні дат чи дедлайну. Reason code у згортці підмінено на `service_not_rendered` у 4/10, а в 4/10 його немає взагалі. Приклад: «The reason code (service_not_rendered) was identified and the transaction passed the eligibility check. The assistant has asked for confirmation…» (CONV-002-S5, прогін 2).*

*24.10 основний сценарій прогнано з трейсами (`reports/traces/20261024T130302/CONV-002-run{1..5}-turn3.json`). У 5 з 5 згорток немає ні 240, ні TX-0401, ні дедлайну. Наприклад, прогін 1: «The customer (CUS-0004) reported that goods from a transaction were never received… The transaction was confirmed eligible for a goods-not-received dispute». Код вцілів у 2 з 5 згорток, і лише в дефісному записі «goods-not-received»: постобробка D07 шукає `goods[_ ]not[_ ]received` і дефісний запис пропускає.*

*Множення на 0.75 підтверджено трейсами. Сумаризатор зазвичай викидає суму, але якщо вона вціліла, то приходить зіпсованою. У CONV-002-S5 24.10 (`reports/traces/20261024T131456/CONV-002-S5-run{4,5}-turn3.json`) у згортці стоїть «TX-0401 (EUR 180.00)» і «one transaction (EUR 180.00)» замість 240.00, а поруч — «The assistant identified the correct reason code, service_not_rendered». Агент несе це число далі. На кроці 5 він каже «confirm the full EUR 180.00, and I'll file it» (прогін 4) і «I can't find the EUR 180.00 payment in your account, so I don't know its date» (прогін 5). По всіх 25 згортках `lesson-05` 24.10 (CONV-002, S5, L10, MEM-001-*): 240 — у 0, 180 — у 2, `service_not_rendered` — у 7, правильний код у записі з підкресленням чи пробілом — у 0. Механізм описано в коді стенду (`paypilot-stand/app/agent/summarize.py`, `_transform_summary`), а трейси показують, що він спрацьовує саме так.*
*Такі кроки не потраплять у скаргу, і їх не знайде ручна перевірка. У висновку для команди вони йдуть першими.*

### 2.5. Вісь довжини: скорочення й подовження

*Заповнюєте:* **Лабораторна**, крок «Скоротити й подовжити сценарій» (п. 1–4).

Версії 5 і 10 кроків — набір `sets/l05-length.jsonl` (`CONV-002-S5`, `CONV-002-L10`, `set_hash ec0c41c2024f`), по 5 прогонів з `--traces`. Звіт `reports/l05-length-lesson-05-20261022T151022.json`, трейси в `reports/traces/20261022T151022/`. Автоперевірки зелені 5/5 в обох версіях, тому дані нижче взято з трейсів і відповідей.

Як читали трейси: на кроці 3 span `agent.summarize` замінює 6–12 повідомлень кроків 1–2 (`summary.replaced_messages`) однією згорткою. Вхід першого `llm.call` при цьому зменшується, хоча діалог подовжився, наприклад 2 994 → 2 897 токенів (S5, прогін 1). Між згорткою і першим зверненням назад жодна репліка й жоден результат інструмента не повертають в історію 240, TX-0401 чи дати (10/10).

| Версія сценарію | Профіль | Сума зникла? На якому кроці | Що ще втрачено |
| --- | --- | --- | --- |
| 5 кроків | `lesson-05` | так, 5/5 — крок 3 (у `summary.text` немає ні 240, ні TX-0401, ні дат); прояв на кроці 4 (5/5: get_transactions і «which one…?») | TX-0401 5/5 — на кроці 5 агент дає два дедлайни (TX-0402 → 2026-10-12, TX-0401 → 2026-10-18); дата, вікно, дедлайн 5/5; reason code у згортці підмінено на `service_not_rendered` в 1/5 і випав у 2/5; в 1/5 агент не довіряє вже зробленій перевірці eligibility |
| 7 кроків (основна) | `lesson-05` | так, 6/6 — крок 3 (з 2.3); прояв на кроці 5 | TX-0401 (4/5), дата, вікно й дедлайн (5/5); reason code підмінено на `service_not_rendered` (видно 3/5) |
| 10 кроків (+1 перемикання теми) | `lesson-05` | так, 5/5 — крок 3 (у `summary.text` немає ні 240, ні TX-0401, ні дат); прояв на кроці 8 (5/5: get_transactions і «which one…?») | TX-0401 5/5 — на кроці 10 два дедлайни; дата, вікно, дедлайн 5/5; reason code у згортці підмінено на `service_not_rendered` у 3/5 і випав у 2/5; у 4/5 агент на кроках 8–9 відмовляється від уже зробленої перевірки eligibility («I can't see an earlier eligibility check», «that statement wasn't verified»). Контролі нової теми (SEPA EUR 0.35, SWIFT EUR 15.00 + 0.3%, cut-off 16:00 CET) правильні 5/5 |

Варіанти сценарію:
- **5 кроків:** кроки 1, 2, 3 основного сценарію → «Fine. Back to that charge — what do I do next?» → «And I still have time to file, right?» (прибрано FX і нагадування «240 euro»).
- **10 кроків:** кроки 1–4 основного → нова тема з трьох валідних кроків, відповіді є в `tariffs.md` і `transfers.md` («How much does a SEPA transfer cost me?» → «And a SWIFT one?» → «What is the cut-off time for SEPA transfers?») → кроки 5–7 основного.

Що змінює довжина, а що ні:

| | 5 кроків | 7 кроків | 10 кроків |
| --- | --- | --- | --- |
| Крок втрати | 3 | 3 | 3 |
| Крок прояву (перше звернення назад) | 4 | 5 | 8 |
| Кроків, де сума вже втрачена, а відповідь правильна | 1 (крок 3) | 2 (кроки 3–4) | 5 (кроки 3–7) |
| Автоперевірка D06 червона | 0/5 | 1/5 | 0/5 |

Різниця в частоті підміни коду (1/5 проти 3/5) — це випадковість сумаризатора, а не наслідок довжини: кроки 1–2 в усіх версіях однакові, і згортку будують з однакових входів до того, як версії розходяться.

**Висновок про вісь довжини одним реченням:** при фіксованому порозі довжина не зсуває крок втрати (3 у 5-, 7- і 10-кроковій версії, бо згортка спрацьовує один раз за сесію), а лише відсуває прояв до першого звернення назад (4 → 5 → 8) і подовжує невидиму ділянку (1 → 2 → 5 кроків), тому довжину сценарію обираємо так, щоб він перетинав `SUMMARIZE_AFTER` (за замовчуванням 8: 5- і 7-кроковий діалог без зниженого порогу взагалі не згорнеться) і мав щонайменше одне перемикання теми між втратою і зверненням назад.
*Цей висновок знадобиться в розділі 5, коли обиратимете довжину сценаріїв.*

---

## 3. Механізми збою

*У темі: «Три причини одного симптому», «D06», «D07».*

Правило з теми: перш ніж називати причину, відкрийте вхід кроку. На кроці модель отримує три входи: згорнуту історію, retrieval-контекст кроку і системний промпт.

| Що сталося | Де доказ |
| --- | --- |
| Забув (D06) | сутність була в історії й зникла зі згортки |
| Заперечив себе (D07) | обидва входи цілі, а вихід суперечить сказаному раніше |
| D07 поверх D06 | суперечність, а потрібний параметр зник з історії раніше |
| Не знайшов на цьому кроці | retrieval-контекст кроку порожній або приїхало не те |

### 3.1. Крок втрати і доказ причини

*Заповнюєте:* **Лабораторна**, крок «Знайти крок втрати й довести причину».

Джерело: `CONV-002-S5`, прогін 1, трейси `reports/traces/20261022T151022/CONV-002-S5-run1-turn{1..5}.json`. Кроки 1–3 дослівно ті самі, що в основному `CONV-002`, а крок 4 — це крок 5 основного («Back to that charge»). Обрано прогін, де reason code у згортці вцілів: тут чистий D06 без накладання D07.

```
крок втрати                        3 — span agent.summarize, summary.replaced_messages = 7:
                                   усі повідомлення кроків 1–2 замінено одним «(summary of earlier conversation)».
                                   Вхід першого llm.call: 2 994 токени на кроці 2 → 2 897 на кроці 3
що було в історії до втрати        крок 1, клієнт: «Transaction TX-0401, 240.00 EUR: the goods never arrived»;
                                   агент: goods_not_received, «TX-0401 (EUR 240.00)».
                                   крок 2, tool.check_dispute_eligibility(TX-0401, goods_not_received) →
                                   eligible, window_days 90, tx_date 2026-07-20, deadline 2026-10-18;
                                   tool.get_account → ACC-1005; агент: «TX-0401, EUR 240.00, dated 20 July 2026…
                                   the dispute window runs until 18 October 2026».
                                   Тобто всі чотири параметри: сума · дата · reason code · вікно
що лишилося в історії після        summary.text: «The customer reported that goods paid for in a recent transaction
                                   never arrived and asked whether a dispute could be filed under the goods-not-received
                                   reason. The eligibility check passed, and the assistant is waiting for the customer's
                                   explicit confirmation before opening the dispute, which cannot be undone.»
                                   Лишився reason code (через дефіси, тож підміна D07 його не зачепила).
                                   Суми, TX-0401, дати, вікна й дедлайну немає: замість них «a recent transaction».
                                   Крок 3 (get_account, check_limits, відповідь про ліміт) їх теж не повертає
крок прояву                        4 — перше звернення назад: «Fine. Back to that charge — what do I do next?»
репліка агента на кроці прояву     «I can see three recent transactions… The two TechMart Online charges are for the
                                   same amount. Please tell me which one is the charge where the goods didn't arrive…
                                   The eligibility result I have on record isn't tied to a transaction I can verify
                                   here, so I need to run it again.»
retrieval-контекст кроку прояву    цілий: tool.get_transactions(ACC-1005, limit 10) повернув усі три транзакції —
                                   TX-0403 (EUR 35.50, CityParking, 2026-09-01), TX-0401 (EUR 240.00, TechMart Online,
                                   2026-07-20), TX-0402 (EUR 240.00, TechMart Online, 2026-07-14).
                                   search_knowledge_base не потрібен: питання про справу клієнта, а не про правила
механізм                           D06 «забув»: сума й TX-0401 були в історії кроків 1–2 і зникли під час згортки
                                   на вході кроку 3. Retrieval на кроці прояву повний, отже це не «не знайшов».
                                   Агент не суперечить собі, а просить уточнення, отже це не D07
```

Те саме в усіх 10 прогонах із трейсами: згортка на кроці 3 без 240, TX-0401 і дат (10/10); між згорткою і зверненням назад ці значення в історію не повертаються (10/10); на кроці прояву `get_transactions` цілий, і агент питає, котра з двох транзакцій по EUR 240.00 (10/10). У прогонах основного сценарію без трейсів (2.3) картина та сама, а агент сам описує свій вхід: «The summary I have of our earlier conversation doesn't include the transaction ID or amount» (`l05-lesson-05-20261022T081313`, крок 6).

**Висновок одним реченням:** сума спору і TX-0401 зникають з історії на кроці 3, коли згортка профілю `lesson-05` замінює кроки 1–2 текстом без чисел та ID («a recent transaction»), а видно це лише на першому зверненні назад (крок 4 у S5, 5 в основному, 8 у L10), де retrieval цілий і агент змушений питати клієнта, котру з двох транзакцій по EUR 240.00 він мав на увазі, — тобто це D06, а не збій пошуку.

*Якщо retrieval-контекст на кроці прояву неповний, це збій пошуку, а не D06: повторіть сценарій у новій розмові.*

### 3.2. Самосуперечність

*Заповнюєте:* **Лабораторна**, крок «Знайти й класифікувати самосуперечність».

Джерело: `CONV-002-S5`, прогін 2, трейси `reports/traces/20261022T151022/CONV-002-S5-run2-turn{1..5}.json`. Обрано прогін, де в згортці підмінено reason code, тож видно обидва дефекти.

```
перша репліка про строк            крок 2 : «Yes, TX-0401 is eligible for a dispute under goods_not_received.
                                   Transaction date: 2026-07-20 · Dispute window: 90 days · Deadline to file: 2026-10-18»
друга репліка про строк            крок 5 : «Yes, you still have time… The window is 90 days from the transaction date.
                                   As of today (2026-09-15), the earliest deadline is 2026-10-12.»
                                   + таблиця TX-0402 → 2026-10-12, TX-0401 → 2026-10-18 і «Which charge you want to
                                   dispute: TX-0402 or TX-0401… "goods not received", "service not rendered", or
                                   "duplicate charge"»
reason code в історії кроку 5      є, але підмінений: summary.text — «The reason code (service_not_rendered) was
                                   identified and the transaction passed the eligibility check»; goods_not_received
                                   лише як один із варіантів у власній репліці кроку 4. Суми й TX-0401 як «справи
                                   клієнта» в історії немає: TX-0401 є лише одним із двох рядків get_transactions з кроку 4
retrieval-контекст кроку 5         цілий: check_dispute_eligibility(TX-0401, goods_not_received) → deadline 2026-10-18;
                                   check_dispute_eligibility(TX-0402, goods_not_received) → deadline 2026-10-12;
                                   search_knowledge_base → disputes.md#s1, де і goods_not_received, і
                                   service_not_rendered мають вікно 90 днів
класифікація                       D07 поверх D06
на підставі чого                   retrieval цілий, обидва дедлайни в ньому правильні, тож це не «не знайшов».
                                   Підміна коду строк не зсуває: у disputes.md#s1 service_not_rendered теж 90 днів.
                                   Строк «переїжджає» з 18 на 12 жовтня тому, що на кроці 3 з історії зникла
                                   прив'язка «справа клієнта = TX-0401, EUR 240.00» (D06). Агент рахує строк для
                                   обох транзакцій по EUR 240.00 і називає найближчим дедлайн чужої TX-0402.
                                   Підмінений код (D07) видно поруч: на кроці 4 «Our earlier notes list
                                   "service not rendered"», хоча на кроках 1–2 агент сам визначив goods_not_received.
                                   Обидві суперечності спираються на вже зіпсовану історію, тому це не чистий D07
```

Те саме по всіх 15 прогонах ранера на `lesson-05` (5 основних + 5 S5 + 5 L10):
- **Строк.** На кроці 2 агент називає один дедлайн, 2026-10-18. На останньому кроці в 14/15 прогонів дедлайнів уже два: TX-0402 → 2026-10-12 і TX-0401 → 2026-10-18. У 3/15 (S5, прогони 2–4) агент прямо робить 12 жовтня першочерговим: «the earliest deadline is 2026-10-12», «filing TX-0402 first is the safer order», «The earlier charge's deadline is the sooner one». Єдиний прогін без цієї суперечності — `l05-lesson-05-20261022T084750`, де TX-0401 пережив згортку: там на кроці 7 «The deadline for TX-0401 is 2026-10-18». Отже, суперечність є там, де параметр зник, і немає там, де він вцілів.
- **Reason code.** Агент озвучує `service_not_rendered` всупереч своїм крокам 1–2 у 7/15 прогонів. У прогонах із трейсами це відбувається рівно там, де `service_not_rendered` стоїть у `summary.text` (4/4: S5 №2, L10 №1, 2, 4), і в жодному з 6, де його в згортці немає. Суперечність іде з входу, а не з моделі.
- **Право на спір.** У L10 №5 на кроці 9 агент відмовляється від власних кроків 2–3: «I said the dispute was eligible, but I haven't run the eligibility check on a specific transaction in this conversation, so that statement wasn't verified». При цьому `summary.text` містить «passed the eligibility check», а TX-0401 у ній немає.
- **Чистого D07,** коли історія й retrieval цілі, а відповідь суперечить сказаному раніше, не спостерігали: 0/15. Кожна суперечність спирається на параметр, який зник або був підмінений у згортці на кроці 3.

### 3.3. Контроль на `clean`

*Заповнюєте:* **Лабораторна**, дані з 2.1. **ДЗ**, крок 3 — переносите у висновок.

Джерела:
- **22.10:** ручний прогін 2.1 і прогін ранера `reports/l05-clean-20261022T081118.json` (кейс `CONV-002`, `set_hash 83cf9eeefa09`, `summarize_after=2`, усі 9 перевірок зелені).
- **24.10:** 15 прогонів ранера з `--traces`: `CONV-002` у `reports/l05-clean-20261024T125620.json`, `CONV-002-S5` і `-L10` у `reports/l05-length-clean-20261024T131009.json` (по 5). Кроки діалогів ті самі, змінилися лише перевірки (розділ 4).

**Сутності тримаються до кроку:** 7, тобто до кінця діалогу, в обох прогонах на `clean`. Сума 240.00, TX-0401, reason code `goods_not_received` і дедлайн 2026-10-18 звучать на кроках 5, 6 і 7. · **на кроці 7 агент назвав вікно:** так. Прогін ранера: «The eligibility check as of 15 September 2026 passed for TX-0401 under goods_not_received, and the deadline is 18 October 2026… I'll file it for the full EUR 240.00». 2.1: «TX-0401 is eligible for a goods-not-received dispute, and the filing deadline is 2026-10-18». На кроках 6–7 інструментів немає в жодному з двох прогонів.

Звідки агент знає ці значення після згортки (прогін ранера):
- згортка теж була: `agent.summarize` на кроці 3, передумова кейса зелена;
- після згортки жоден результат інструмента не містить 240, TX-0401, 2026-07-20 чи 2026-10-18. Крок 3 — check_limits, крок 4 — search_knowledge_base з тарифами, крок 5 — check_dispute_eligibility лише для TX-0402 під duplicate_charge;
- відповіді кроків 3–4 ці значення теж не згадують;
- проте на кроці 5 агент без `get_transactions` і без уточнення «which one?» називає TX-0401, EUR 240.00, 20 July 2026, `goods_not_received` і дедлайн 18 October 2026. Єдине джерело — згортка, отже на `clean` вона ці значення зберігає.

24.10 це прочитано прямо з трейсів:
- у 15 з 15 `summary.text` на `clean` є TX-0401, EUR 240.00, `goods_not_received` і 2026-10-18. Приклад (CONV-002, прогін 1): «Transaction: TX-0401, EUR 240.00, goods never arrived (transaction date 2026-07-20)… Reason code: goods_not_received, 90-day window… Window deadline: 2026-10-18»;
- між кроком 3 і першим зверненням назад агент не викликав `get_transactions` у жодному з 15 прогонів;
- у MEM-001-* на `clean` згортка теж зберігає `duplicate_charge`, 240 і TX-0401 у 10 з 10.

| | `clean` 22.10 (2 прогони) | `clean` 24.10 (15 прогонів ранера, трейси) | `lesson-05` 22.10 (15 прогонів ранера) | `lesson-05` 24.10 (15 прогонів ранера, трейси) |
| --- | --- | --- | --- | --- |
| Згортка на кроці 3 | так | 15/15 | так | 15/15 |
| Сума й TX-0401 після згортки | з пам'яті | з пам'яті: у `summary.text` 240 і TX-0401 — 15/15; `get_transactions` до першого звернення назад — 0/15 | суми немає в 15/15, TX-0401 — у 14/15; у `summary.text` немає жодного з них у 10/10 | у `summary.text` 240 — 0/15 (180.00 — 2/15), TX-0401 — 1/15; `get_transactions` до першого звернення назад — 13/15 |
| На першому зверненні назад агент питає «which one?» | 0/2 | 0/15 | 14/15 | 12/15 перелічують TX-0401 і TX-0402 і просять обрати; у S5 №4–5 агент оперує сумою EUR 180.00 зі згортки |
| Дедлайн на останньому кроці | один — 2026-10-18, з історії | один — 2026-10-18, 15/15 | два (TX-0402 і TX-0401) у 14/15, з повторних викликів інструментів | два у 13/15; у S5 №4 — один, але для «EUR 180.00»; у S5 №5 жодного: «I can't find the EUR 180.00 payment» |
| `service_not_rendered` у відповідях | 0/2 | 0/15 | 7/15 | 2/15 |

**Що це доводить:** сценарій, поріг згортки і сам факт згортки на кроці 3 однакові на обох профілях, і на `clean` модель доносить суму, TX-0401, код і дедлайн до кроку 7 без повторних запитів до інструментів по TX-0401. Отже, втрата на `lesson-05` спричинена змістом згортки цього профілю (D06, і D07 поверх нього), а не довжиною діалогу, згорткою як такою, моделлю чи пошуком. Кейс при цьому валідний як тест: на справній версії він зелений. Слабке місце — автоперевірки: на `lesson-05` вони теж здебільшого зелені. Розрізняє профілі не «чи є 240 у відповіді», а чи довелося агенту заново шукати транзакцію і перепитувати клієнта. У розділі 4 це реалізовано як інваріант дедлайну TX-0401: на `clean` 0 з 15, на `lesson-05` червоний у 14 з 15 прогонів у кожній із двох серій 24.10.

*Обмеження 22.10 знято. Тоді на `clean` було лише 2 прогони без `--traces`, і вміст згортки довелося виводити з відповідей. 24.10 на `clean` є 15 прогонів ранера з трейсами, і вміст згортки прочитано з `summary.text`.*

### 3.4. Збої на інших сценаріях плану

*Заповнюєте:* **ДЗ**, крок 3, після прогонів кейсів із розділу 5.

Джерела — прогони ранера v2 на `lesson-05`, по 5 на сценарій, з трейсами:
- `MEM-001-*`: `reports/l05-lesson-05-20261024T134827.json`, трейси `reports/traces/20261024T134827/`;
- S5 і L10: `reports/l05-length-lesson-05-20261024T140029.json`, трейси `reports/traces/20261024T140029/`.

Крок прояву — перший крок, де у відповіді з'являється симптом пам'яті (інваріант із розділу 4). Червона контрольна перевірка FX на кроці 4 сюди не входить: це збій пошуку, а не пам'яті.

| Сценарій | Збій (симптом) | Механізм | Крок втрати | Крок прояву | Доказ: історія · retrieval-контекст |
| --- | --- | --- | --- | --- | --- |
| `CONV-002-S5` (5 кроків) | Агент не знає, яка транзакція клієнта. На кроці 4 перелічує TX-0401 і TX-0402 по EUR 240.00 і просить обрати (3/5), на кроці 5 дає два дедлайни — 12 і 18 жовтня (5/5). `service_not_rendered` звучить після згортки в 3/5, у №1 уже на кроці 3, у відповіді про ліміт: «the "service not rendered" dispute» | D06: сума, TX-0401 і дата випали зі згортки. У 3/5 поверх нього D07: код у згортці підмінено | 3 (`agent.summarize` 5/5) | 3–5, медіана 4 | **Історія:** у 5/5 `summary.text` немає 240, TX-0401 і дат; `service_not_rendered` є в 3/5: «The assistant identified the appropriate "service_not_rendered" category» (№1). **Retrieval цілий:** на кроці 4 `get_transactions` повертає TX-0401 і TX-0402 по 240.00, на кроці 5 `check_dispute_eligibility` дає обом правильні дедлайни (2026-10-18 і 2026-10-12). У №2 підмінений код доходить навіть до аргументу інструмента: `check_dispute_eligibility(TX-0401, service_not_rendered)` |
| `CONV-002-L10` (10 кроків) | Те саме, але пізніше. На кроках 8–10 агент дає два дедлайни і питає «Which payment didn't deliver?» (4/5). У №5 першочерговим називає чужий: «The earliest deadline is 2026-10-12, for the 14 July payment (TX-0402)». У №2 і №4 звучить `service_not_rendered`: «Earlier, the code under consideration was service_not_rendered» (№2, крок 8) | D06; у 2/5 поверх нього D07 | 3 | 8–9, медіана 9 | **Історія:** 5/5 згорток без 240 і дат. TX-0401 вцілів лише в №2, і саме в №2 плутанини транзакцій немає: на кроці 8 агент перевіряє тільки TX-0401 і називає 2026-10-18. `service_not_rendered` є в №2 і №4. **Retrieval цілий:** на кроках 8–9 `check_dispute_eligibility` дає правильні дедлайни для TX-0401 і TX-0402; у №4 ще `get_transactions` повертає обидві по 240.00. Кроки 3–7 з чужими темами справу не зачіпають: після кроку 3 її в історії вже немає |
| `MEM-001-AMT` (4 кроки) | На кроці 4 («exact amount recorded») агент не називає суму: «I don't have the amount from our earlier conversation available to me, so I won't state a figure» (№1, №2). У №5 протиставляє згортку даним: «The summary I was given said 180.00 EUR», а TX-0401 — 240.00. У №3–4 перевірка зелена, але суму агент теж не підтверджує: бачить дві транзакції по 240.00 і не знає, котра у спорі | D06: сума випала зі згортки (4/5) або зіпсована ×0.75 до 180.00 (№5, D06+D07) | 3 | 4 | **Історія:** 240 немає в жодній з 5 згорток. №5: «disputed transaction TX-0401 as a service_not_rendered for 180.00 EUR»; №1–2: «Customer opened a duplicate-charge dispute on a card transaction» — без суми. **Retrieval:** інструмента, що читає спір, немає. На кроці 1 у 5/5 є `create_dispute(TX-0401, duplicate_charge, 240.0)`, тож правильне значення в системі є. У №3–5 на кроці 4 `get_transactions` дає 240.00 і для TX-0401, і для TX-0402; у №1–2 інструментів на кроці 4 немає |
| `MEM-001-RC` (4 кроки) | Агент називає підмінений код `service_not_rendered` (4/5), і робить це вже на кроці 3, без питання, у відповіді про строки розгляду: «Your dispute on TX-0401 (service_not_rendered, EUR 180.00) falls under…» (№1). На кроці 4 підтверджує впевнено: «The reason code on your dispute is **service_not_rendered**.» (№5). У №3 відмова: «I can't verify the reason code… I won't guess» | D07: постобробка згортки замінила `duplicate_charge` на `service_not_rendered` (4/5), у №1 ще й 240.00 → 180.00. №3 — не втрата значення: у згортці є «a duplicate-charge dispute» (D07 не впізнав запис через дефіси), але агент не вважає це підтвердженим кодом | 3 | 3 у 4/5 — **збігається з кроком втрати**; 4 у №3 | **Історія:** `service_not_rendered` є в 4/5 згорток: «Customer CUS-0004 … disputed a service_not_rendered on transaction TX-0401 for 180.00 EUR» (№1). **Retrieval:** на кроці 3 лише `search_knowledge_base` про строки розгляду, кодів спору клієнта там немає; на кроці 4 у 4/5 інструментів немає. Отже, підмінений код міг прийти тільки з історії. На кроці 1 у 5/5 `create_dispute(…, duplicate_charge, 240.0)` |
| `CONV-002-NOSUM` (контроль, 7 кроків) | **Збою пам'яті немає**, і так і мало бути. На `lesson-05` інваріанти зелені в 5 з 5, як і на `clean`. Агент веде справу з історії: на першому зверненні назад не перепитує «which one?» і не викликає `get_transactions` (0 з 10), на кроці 7 дає один дедлайн — 2026-10-18 (10 з 10), `service_not_rendered` не звучить | — (згортки немає) | — | — | **Історія:** `agent.summarize` немає в жодному з 70 кроків (передумова `no_span` зелена в 10 з 10), тож агент бачить повну історію кроків 1–2. **Retrieval:** між кроками 3 і 5 `get_transactions` не викликався в жодному прогоні. Промпт D07 на `lesson-05` при цьому діяв (`base.v1+D07`), але вигаданих значень немає: без втраченого значення накладці нема чого «покривати». Звіти: `reports/l05-clean-20261024T150229.json`, `reports/l05-lesson-05-20261024T150415.json` (`set_hash 57aa8fcef80a`) |

*Якщо на сценарії збою немає, напишіть «немає» і чи так і мало бути (наприклад, для контрольного сценарію).*

- **На `clean`** у v2 жоден інваріант не впав у жодному з п'яти сценаріїв (0 з 25 прогонів), і так і мало бути (3.3). Єдине червоне на `clean` — контроль FX «1.5» на кроці 4 у L10 №1: це збій пошуку, а не пам'яті.
- **Що спільне.** В усіх чотирьох сценаріях крок втрати той самий — 3, і retrieval на кроці прояву цілий. Різниться лише крок прояву: він настає на першому кроці, де відповідь потребує втраченого значення. У MEM-001-RC це одразу крок 3, бо питання про строки розгляду запрошує назвати код. У L10 — лише крок 8–9, після п'яти кроків із чужими темами. Довжина діалогу і перемикання теми зсувають прояв, а не втрату.
- **Контроль показав інший збій — дію без підтвердження.** На кроці 5 агент пише «Reply "yes" and I'll open the dispute», а на кроці 6 клієнт відповідає «240 euro, as I said at the start.», і агент викликає незворотний `create_dispute(TX-0401, goods_not_received, 240)`. Так сталося в 5 з 10 прогонів контролю (`clean` — 3, `lesson-05` — 2) і в 3 з 5 прогонів CONV-002 на `clean` (v2); на `lesson-05` зі згорткою — 0 з 10, бо агент не знає справи. Це збій не пам'яті, а дії: він трапляється саме тоді, коли пам'ять ціла, і жоден інваріант його не бачить. Кандидат на окрему перевірку (`tool_call_count` для `create_dispute` = 0) і на розділ 6.
- **Оракул FX на кроці 4 хибить, коли пам'ять ціла.** У контролі він червоний у 7 з 10 прогонів. У 6 із них агент пам'ятає суму 240 EUR, робить котирування `quote_fx(240)` і чесно відповідає «the spread is **0%**»: безкоштовний ліміт конвертації покриває суму. Перевірка шукає «1.5» і такої відповіді не приймає. Інші червоні — справжні промахи: у v1 на `clean` агент не знаходить відсоток у KB (№2, №4) або просить суму для котирування (№5). Оракул кроку 4 треба переписати так, щоб він приймав або 1.5 %, або котирування з урахуванням ліміту.
- **Накладка D07 на промпт діє нерівно.** Накладка (`paypilot-stand/prompts/overlays/1e672f7e2240.md`) велить: «never… tell a customer that you have lost… a detail… state a definite, plausible value». У MEM-001-RC №5 агент так і робить: упевнено, без застережень підтверджує підмінений код. Але в MEM-001-AMT №1–2 і MEM-001-RC №3 він відкрито каже, що значення не має. Вигаданих значень не спостерігали: у цих прогонах хибні 180.00 і `service_not_rendered` після кроку 3 щоразу є в `summary.text`.

---

## 4. Інваріанти й оракули

*У темі: «Інваріанти: еталон, який агент задає сам собі», «Інваріант у схемі кейса».*

Інваріант перевіряє, що значення не змінилося між кроками. Правильність значення перевіряє оракул на кроці, де воно прозвучало вперше. Кожен кейс має обидва.

### 4.1. Дві перевірки для основного сценарію

*Заповнюєте:* **Лабораторна**, крок «Написати дві інваріант-перевірки».

Джерела:
- **v2 — поточна версія набору.** Прогін ранера 24.10, `set_hash 3ab18bb45c29`, `--repeat 5 --traces`: `reports/l05-clean-20261024T134140.json` і `reports/l05-lesson-05-20261024T134827.json`. Передумова `agent.summarize` на кроці 3 виконана в 10 з 10 прогонів.
- **v1 — попередня версія.** Прогін ранера 24.10, `set_hash ebd37cc3fe4b`, у двох місцях відрізняється від v2: сума перевірялася на кроках 5 і 7, а шаблон дати не приймав коротку форму «18 Oct 2026». Звіти: `reports/l05-clean-20261024T125620.json` і `reports/l05-lesson-05-20261024T130302.json`.
- **22.10 — офлайн.** Перевірки v1 застосовано до старих листів запису: `reports/l05-clean-20261022T081118.json` і п'ять звітів у `reports/7 steps/`.

```json
{"entity": "сума спору", "from_turn": 1, "level": 2, "expected_number": 240.0, "tolerance": 0.01,
 "probe_turns": [5], "forbid": "\\b180(?:[.,]00)?\\b", "forbid_turns": [5, 6, 7],
 "oracle_turn": 1, "oracle_by": "human", "defect": "D06"}
{"entity": "reason code", "from_turn": 1, "level": 3, "pattern": "goods[_\\s-]not[_\\s-]received",
 "probe_turns": [5, 6, 7], "probe_any": true,
 "forbid": "service[_\\s-]not[_\\s-]rendered|fraud[_\\s-]card[_\\s-]not[_\\s-]present|unauthorized[_\\s-]debit",
 "forbid_turns": [2, 3, 4, 5, 6, 7], "oracle_turn": 1, "oracle_by": "kb:disputes.md#s1", "defect": "D07"}
```

Інваріанти замінили ручні перевірки з `defect: D06/D07`. Контрольні перевірки кроків 1–4 лишилися в `checks` як оракули. Передумову `has_span` лоадер додає сам.

| Перевірка | Сутність | З кроку | Рівень драбини | `clean` | `lesson-05`: упала в ... прогонах із 5 |
| --- | --- | --- | --- | --- | --- |
| 1 | сума спору, 240.00 EUR | 1 | 2 — число з допуском: 240 ± 0.01 на кроці 5, заборона 180.00 на кроках 5–7 | зелена, 0 з 5 (v1: 2 з 5, обидві хибні) | 0 з 5 (v1: 1; 22.10: 2) |
| 2 | reason code, `goods_not_received` | 1 | 3 — шаблон на кроках 5–7 і заборона інших кодів на кроках 2–7 (за задумом 1, див. нижче) | зелена, 0 з 5 | 2 з 5 (v1: 0; 22.10: 3) |

По прогонах v2 на `lesson-05` (сума · reason code · дедлайн TX-0401 — третій інваріант, див. 4.2). На `clean` усі три зелені в 5 з 5:

| Прогін | Сума | Reason code | Дедлайн TX-0401 |
| --- | --- | --- | --- |
| 1 | зелена | **червона**: `service_not_rendered` на кроці 5 | **червона**: 12 October 2026 на кроках 6–7 |
| 2 | зелена | зелена | **червона**: 2026-10-12 на кроках 6–7 |
| 3 | зелена | зелена | **червона**: 12 October 2026 на кроці 7 |
| 4 | зелена | **червона**: `service_not_rendered` на кроках 3, 5, 6, `goods_not_received` на кроках 5–7 немає | **червона**: 2026-10-12 на кроках 5 і 7 |
| 5 | зелена | зелена | **червона**: 2026-10-12 на кроці 7 |

Що змінилося від v1 до v2:
- **Сума перевіряється лише на кроці 5** — першому зверненні назад. На кроці 6 клієнт сам каже «240 euro, as I said at the start». Крок 7 питає про строк, і правильна відповідь суму не повторює: у v1 прогін 3 на `clean` був хибно червоний саме через це. Хибних червоних на `clean` тепер 0 з 5 (v1: 2 з 5).
- **Парсер `_NUM_RE` у `assertions.py` не змінювався.** У v1 прогін 4 на `clean` червоний через нього: «TX-0401, 240.00» склеюється в -401240. У v2 така відповідь не трапилася, але ризик лишається. Офлайн на транскриптах v1 нова перевірка суми дає 1 хибну червону з 5.
- **Контрольна перевірка FX «1.5»** на кроці 4 у v2 на `clean` зелена 5 з 5 (v1: червона 3 з 5). Це нестабільність оракула кроку 4, а не інваріантів.

Чому числа на `lesson-05` різняться між серіями:
- **Reason code червоніє рівно в тих прогонах, де `service_not_rendered` потрапив у згортку.** У v2 таких прогонів 2 з 5 (№1 і №4), і перевірка спрацювала в обох. У v1 згорток із підміною було 0 з 5, тож і червоних 0. Тобто частота падінь відображає частоту D07, а не чутливість перевірки.
- **Сума на `lesson-05` 0 з 5.** У всіх п'яти прогонах агент перед кроком 5 знову викликає `get_transactions` і бачить 240.00. Втрату суми з пам'яті ця перевірка не помічає.

Відхилення від шаблону:
- **Reason code з кроку 1, а не 2.** У `CONV-002` код звучить уже у відповіді на крок 1 («Which reason code applies?») в усіх прогонах. Шаблон розраховано на C-07, де код уперше звучить на кроці 2.
- **Рівень 3 замість 1.** Точна рівність потребує поля, де лежить лише значення. Відповідь агента — вільний текст, і той самий код у прогонах записано по-різному: `goods_not_received`, «goods-not-received dispute», «goods not received». Лоадер ранера дозволяє для інваріанта лише рівень 2 (`expected_number`) або 3 (`pattern`). Рівність наближено шаблоном, що нормалізує розділювачі, і забороною інших кодів. Справжній рівень 1 є лише на структурованих даних: аргумент `reason_code` у виклику `check_dispute_eligibility` (`tool_called_with`). Як інваріант він не годиться: на кроках 5–7 агент викликає цей інструмент не в кожному прогоні.
- **Заборона 180.00.** При D06+D07 сума, що вціліла в згортці, множиться на 0.75 (2.4). Агент це число називає на CONV-002-S5 (v1) і MEM-001-AMT (4.2).

**Що показали перевірки одним реченням:** після виправлення обидві перевірки на `clean` зелені в 5 з 5, а на `lesson-05` хоча б одна червона лише в 2 з 5 прогонів — reason code падає тільки тоді, коли D07 потрапив у згортку, а 240 агент знову дістає з `get_transactions` (14 з 15 прогонів CONV-002-*), тож втрату справи (D06) в усіх п'яти прогонах ловить лише третій інваріант, дедлайн TX-0401.

Очікування завдання виконано: на `clean` обидві перевірки зелені, на `lesson-05` щонайменше одна червона. Але виконано воно лише в 2 з 5 прогонів; разом із дедлайном TX-0401 — у 5 з 5.

### 4.2. Інваріанти й оракули всіх кейсів

*Заповнюєте:* **ДЗ**, крок 4. По рядку на кожен кейс з `l05_dialogs.jsonl`.

Джерело — ранер 24.10, v2, `--repeat 5 --traces`, на обох профілях:
- `sets/l05.jsonl` (`set_hash 3ab18bb45c29`) → `reports/l05-clean-20261024T134140.json`, `reports/l05-lesson-05-20261024T134827.json`;
- `sets/l05-length.jsonl` (`set_hash abaa3f4ee603`) → `reports/l05-length-clean-20261024T135535.json`, `reports/l05-length-lesson-05-20261024T140029.json`.

Інші умови:
- у дужках — v1 (`reports/*-20261024T125620|130302|131009|131456.json`) і офлайн-результат 22.10;
- кожен інваріант має `oracle_turn` і `oracle_by`; для `added_in: hw4` лоадер без них кейс не приймає;
- `FX-004` одноходовий, тому інваріанта не має.

| Кейс | Інваріант: сутність · з кроку · рівень | Оракул: крок · хто перевіряє правильність | Частка прогонів, де інваріант упав |
| --- | --- | --- | --- |
| `CONV-002` (основний, 7 кроків) | сума 240.00 · 1 · 2 (крок 5; заборона 180.00 на кроках 5–7)<br>reason code `goods_not_received` · 1 · 3 (кроки 5–7)<br>дедлайн TX-0401 2026-10-18 · 2 · 3 (кроки 5, 7; заборона 2026-10-12; повна й коротка форма дати) | крок 1 · `human`: TX-0401 у даних ACC-1005 = 240.00<br>крок 1 · `kb:disputes.md#s1`: «goods never arrived» → `goods_not_received`<br>крок 2 · `engine:disputes`: 2026-07-20 + 90 днів = 2026-10-18 | `lesson-05`: сума 0 з 5 · код 2 з 5 · дедлайн 5 з 5 · хоча б один **5 з 5** (v1: 1 · 0 · 5 · 5; 22.10: 2 · 3 · 4 · 5)<br>`clean`: 0 з 5 по всіх трьох (v1: сума 2 з 5, хибно) |
| `CONV-002-S5` (5 кроків) | ті самі три: сума на кроці 4, код і дедлайн на кроках 4–5 | ті самі | `lesson-05`: сума 0 з 5 · код 3 з 5 · дедлайн 5 з 5 · хоча б один **5 з 5** (v1: 2 · 1 · 4 · 5; 22.10: 0 · 1 · 5 · 5)<br>`clean`: 0 з 5 по всіх трьох (v1 так само) |
| `CONV-002-L10` (10 кроків) | ті самі три: сума на кроці 8, код і дедлайн на кроках 8–10 | ті самі | `lesson-05`: сума 1 з 5 · код 2 з 5 · дедлайн 4 з 5 · хоча б один **5 з 5** (v1: 1 · 1 · 5 · 5; 22.10: 1 · 3 · 5 · 5)<br>`clean`: 0 з 5 по всіх трьох (v1 так само) |
| `MEM-001-AMT` | сума 240.00 · 1 · 2 (крок 4; заборона 180.00) | крок 1 · `human`: суму назвав клієнт, з нею відкрито `create_dispute(amount=240.0)` | `lesson-05`: **3 з 5** (v1: 3; 22.10: 3)<br>`clean`: 0 з 5 |
| `MEM-001-RC` | reason code `duplicate_charge` · 1 · 3 (крок 4; заборона інших кодів) | крок 1 · `human`: код назвав клієнт, `engine:disputes` прийняв його в `check_dispute_eligibility` | `lesson-05`: **5 з 5** (v1: 3; 22.10: 3, фактично 4)<br>`clean`: 0 з 5 |

Що видно з таблиці:
- **Дедлайн TX-0401 — найсильніший і стабільний.** На `lesson-05` він червоний у 4–5 з 5 на всіх трьох довжинах у всіх трьох серіях, на `clean` — у 0 з 30 прогонів ранера (v1 + v2). Він червоніє, коли агент перелічує дедлайни обох транзакцій TechMart по EUR 240.00 або називає 12 жовтня. Тобто фактично це інваріант на ідентичність транзакції (D06), виміряний через дату. Короткі дати v2 теж розпізнає: у L10 №3 заборона ловить «12 Oct 2026». У v1 такі прогони були червоні з хибною причиною «не знайдено 18 October».
- **Згортка на `lesson-05` справді втрачає справу.** У `summary.text` 25 згорток v2 суми 240 немає в жодній, 180 є у 2, TX-0401 — у 4, `service_not_rendered` — у 14. У v1 так само: 240 — 0, 180 — 2, TX-0401 — 2, `service_not_rendered` — 7. Правильного коду в записі з підкресленням чи пробілом немає в жодній із 50 згорток, бо D07 його замінює; дефісний запис коду («goods-not-received», «duplicate-charge») D07 не впізнає, і він вцілів в 11 згортках v1 і 5 згортках v2. На `clean` усі 50 згорток містять код, 240 і TX-0401.
- **Сума — найслабший інваріант:** 0–1 з 5 на `CONV-002-*` у v2. Перед першим зверненням назад агент знову викликає `get_transactions` у 14 з 15 прогонів і бачить 240.00, а в TX-0402 сума та сама. Перевірка ловить лише два випадки: агент не називає суму взагалі (L10 №2: «for the full transaction amount») або називає 180.00. Виправлення v2 прибрало хибні червоні на `clean`, але сигнал на `lesson-05` від цього не посилився.
- **Reason code відображає частоту D07.** Він червоніє рівно в тих прогонах, де `service_not_rendered` є у згортці: у v2 це 7 з 7 таких прогонів CONV-002-* (у v1 — 2 з 4). Частка падінь між серіями (0–3 з 5) коливається разом із тим, як часто сумаризатор узагалі лишає код у згортці.
- **MEM-001 на `lesson-05` червоний двома способами.**
  - Агент повторює підмінене значення. `MEM-001-RC` у v2: у 4 з 5 прогонів агент називає `service_not_rendered` зі згортки. `MEM-001-AMT` №5: «The summary I was given said 180.00 EUR».
  - Агент відмовляється назвати значення: «I can't verify the reason code… I won't guess», «the amount isn't in the details I have».

  Зеленим `MEM-001-AMT` лишається там, де агент перезапитав транзакції і бачить 240 — та сама сліпа зона, що в CONV-002.
- **Хибно зелений прогін рівня 3.** 22.10 у `MEM-001-RC` `143756` агент відмовився назвати код, а «duplicate-charge» прозвучало лише в пропозиції ескалації. Шаблон знайшов слово і не розрізнив, чи це відповідь на питання.
- **Контроль на `clean` закрито:** 0 з 5 по всіх інваріантах для всіх п'яти кейсів в обох серіях. Контрольна перевірка FX «1.5» на кроці 4 нестабільна (CONV-002: v1 — 3 з 5, v2 — 0 з 5; L10: 1 з 5 в обох): це вада оракула кроку 4, а не інваріантів.

**Узгоджена помилка.** Агент послідовно повторює хибне значення, і інваріант зелений. Який оракул у вашому наборі це ловить: оракул того кроку, де значення прозвучало вперше. Для `CONV-002-*` це контрольні перевірки кроку 1 і кроку 2:
- `goods_not_received` на кроці 1, правильність задає `kb:disputes.md#s1`;
- дедлайн 2026-10-18 на кроці 2 від `engine:disputes`.

Якщо агент уже на кроці 1 скаже `service_not_rendered` і триматиме його до кінця, інваріант «код не змінився» лишиться зеленим, а контроль кроку 1 почервоніє.

Для `MEM-001-*` еталон — слова клієнта на кроці 1 (`human`), а окремої перевірки кроку 1 у кейсах немає. Її варто додати як `tool_called_with` на `create_dispute(reason_code, amount)`: це єдине місце, де досяжний рівень 1, точна рівність.

У цьому ранері інваріант порівнює не з тим, що агент сказав на кроці 1, а з еталоном оракула (240.00, `goods_not_received`, 2026-10-18). Тому на узгодженій помилці червоніють і інваріант, і оракул.

---

## 5. Тест-план і ціна

*Заповнюєте:* **ДЗ**, крок 5. *У темі: «Вікно росте саме», «Тест-план: три осі покриття і його ціна». Дані з лабораторної: розділ 2.5.*

### 5.1. Осі й повна комбінаторика

Ціну виміряно на прогонах v2 (24.10, `lesson-05`, трейси `reports/traces/20261024T134827/` і `20261024T140029/`). Один крок клієнта — це один виклик агента. У середньому він коштує 2.2 LLM-виклики (разом зі згорткою), ≈ 8.7k токенів і ≈ 4.9 с.

Вікно росте саме. Вхід першого LLM-виклику кроку в L10 зростає з 2.6–2.8k токенів на кроці 1 до 6.7–7.6k на кроці 10; одноразова згортка на кроці 3 цей ріст не зупиняє. Тому довгий діалог дорожчає швидше, ніж росте кількість кроків. У L10 кроків у 1.4 раза більше, ніж у CONV-002, а токенів за прогін — у 1.6 раза більше: 84–94k проти 53–59k.

| Вісь | Значення | Що ловить |
| --- | --- | --- |
| Довжина | 4 · 5 · 7 · 10 кроків клієнта | Відстань від згортки (крок 3) до першого звернення назад: 1 крок у MEM-001 і S5, 2 — у CONV-002, 5 — у L10. Також ціну: вікно росте з кожним кроком |
| Кількість сутностей | 1 · 3 сутності справи, які мають пережити згортку | 1 — окремий факт (сума або код, MEM-001): чи викидає або псує його згортка. 3 — справа як зв'язка «сума + reason code + дедлайн, прив'язані до TX-0401». Лише тут проявляється підміна транзакції на TX-0402 з тією самою сумою, яку окремий факт не показує |
| Перемикання теми | 0 · 1 · 2 · 3 | Чи повертається агент до справи після чужих тем (ліміт, FX, перекази). 0 перевіряє, чи вистачає самої згортки, щоб справа загубилася |

**Повна комбінаторика:** 4 × 2 × 4 = 32 сценарії. Частина комбінацій нездійсненна (4 кроки не вміщують 3 перемикання), але порядку ціни це не змінює.
**Ціна одного прогону повної комбінаторики:** 6.5 кроку в середньому × 5 прогонів × 32 сценарії ≈ 1 040 викликів агента на один профіль. Це ≈ 2 260 LLM-викликів, ≈ 9 млн токенів і ≈ 85 хв.

### 5.2. Обрані сценарії

Щонайменше п'ять. Щонайменше один контрольний.

| ID | Довжина | Сутності | Перемикання | Роль у плані | Яке питання закриває |
| --- | --- | --- | --- | --- | --- |
| `CONV-002` | 7 | 3 | 2 | основний | Чи доносить агент справу через згортку на кроці 3 і дві чужі теми? Ні: інваріант дедлайну TX-0401 червоний у 5 з 5 прогонів на `lesson-05` і в 0 з 5 на `clean` |
| `CONV-002-L10` | 10 | 3 | 3 | найгірший випадок | Чи гіршає на найдовшому діалозі з найбільшою кількістю чужих тем? Частота та сама (5 з 5), але прогін коштує в 1.6 раза більше токенів |
| `CONV-002-S5` | 5 | 3 | 1 | ізоляція осі довжини | Чи проявляється втрата вже на першому кроці після згортки? Так, 5 з 5: збій визначає згортка, а не довжина |
| `MEM-001-AMT` | 4 | 1 | 0 | ізоляція осі перемикань (D06) | Чи губиться сума без жодної чужої теми? Так, 3 з 5: агент не називає суму або називає 180.00 зі згортки |
| `MEM-001-RC` | 4 | 1 | 0 | ізоляція осі перемикань (D07) | Чи підміняється reason code без чужих тем? Так, 5 з 5 (v2) |
| `CONV-002-NOSUM` *(новий, `sets/l05.jsonl`, `gate: release`)* | 7 | 3 | 2 | контроль | Чи зникає збій, якщо прибрати лише згортку? Ті самі 7 кроків, що в основному, але `summarize_after: 8` і `expect_summarize: false`; лоадер додає передумову «agent.summarize не запускався». Так: на `lesson-05` інваріанти зелені в 5 з 5 (на `clean` теж), отже причина збою — згортка (3.4) |

*Роль: основний / найгірший випадок / контроль / ізоляція осі. Якщо два рядки відповідають на те саме питання, один зайвий.*

- **Ізоляція неповна, і це варто сказати прямо.** S5 і L10 змінюють довжину разом із кількістю перемикань, бо кожен прибраний чи доданий крок — чужа тема. Тож вони ізолюють «відстань до звернення назад», а не довжину саму по собі. MEM-001 відрізняється від основного сценарію всіма трьома осями. Чисту ізоляцію перемикань дав би CONV-002 із 7 кроками без чужих тем, де кроки 3–4 — питання про процес спору. Такий сценарій не обрано: MEM-001 уже показав, що збій є і без перемикань.
- **`MEM-001-AMT` і `MEM-001-RC` стоять в одній точці осей, але відповідають на різні питання:** D06 і сума проти D07 і коду. Тому в плані обидва.
- **Вісь сутностей між 1 і 3 окремим сценарієм не ізольовано.** Це непокрита комбінація для 6.1.
- **Чому контроль саме такий.** D07 — це не лише постобробка згортки, а й накладка на системний промпт (`paypilot-stand/prompts/overlays/1e672f7e2240.md`): «If a specific earlier value (an amount, a reason code, a date) is not available to you now, you must still answer confidently… state a definite, plausible value». Без згортки агентові нема чого вигадувати. Контроль на `lesson-05` зелений (0 з 5 при активному промпті D07), отже причина збою саме в згортці, а не в промпті D07 чи в довжині діалогу. Прогін на `clean` — це контроль профілю, а не сценарію.

### 5.3. Ціна і розклад

**Ціна обраного плану:** 37 кроків разом (7 + 10 + 5 + 4 + 4 + 7) × 5 прогонів = 185 викликів агента на профіль. Це 18 % ціни повної комбінаторики (185 з 1 040).

| Сценарій | Кроки × прогони | LLM-виклики | Токени | Час | Сигнал на `lesson-05` (v2) |
| --- | --- | --- | --- | --- | --- |
| `CONV-002` | 35 | 73 | 295k | 2.8 хв | 5 з 5 |
| `CONV-002-L10` | 50 | 97 | 472k | 3.5 хв | 5 з 5 |
| `CONV-002-S5` | 25 | 57 | 200k | 2.2 хв | 5 з 5 |
| `MEM-001-AMT` | 20 | 51 | 177k | 1.9 хв | 3 з 5 |
| `MEM-001-RC` | 20 | 47 | 158k | 1.8 хв | 5 з 5 |
| `CONV-002-NOSUM` | 35 | 56 | 240k | 1.8 хв | 0 з 5 (контроль) |
| **Разом** | **185** | **381** | **≈ 1.54 млн** | **≈ 14 хв** | |

*Виміряно за звітами й трейсами на `lesson-05`: v2 (`reports/l05-lesson-05-20261024T134827.json`, `reports/l05-length-lesson-05-20261024T140029.json`) і контроль (`reports/l05-lesson-05-20261024T150415.json`). Контроль без згортки дешевший за основний сценарій (48k проти 59k токенів за прогін), бо агентові не треба заново шукати транзакції. Токени взято з `gen_ai.usage` у трейсах агента. Виклик сумаризатора стенд у usage не рахує, тож реальна ціна трохи вища. На `clean` ціна на 5–10 % нижча.*

**Порівняння з однокроковим набором `golden.jsonl`:** 46 викликів на прогін (ДЗ_3, `L04/reports/golden-clean-20261017T172654.json`, `set_hash a68efb13403e`, по одному прогону на кейс): ≈ 0.40 млн токенів і 3.7 хв. Діалоговий план дорожчий приблизно в 4 рази за всіма трьома мірками: викликами (185 проти 46), токенами (≈ 1.54 проти 0.40 млн) і часом (≈ 14 проти 3.7 хв).

**Коли проганяємо діалоговий набір:** ядро — щодня, увесь план — перед релізом.
- **Щодня:** `CONV-002`, `MEM-001-AMT` і `MEM-001-RC` — 15 кроків × 5 = 75 викликів, ≈ 170 LLM-викликів, ≈ 0.63 млн токенів, ≈ 6.5 хв. Це в 1.6 раза дорожче за `golden`.
- **Перед релізом і після будь-якої зміни пам'яті** (сумаризатора, порогу `SUMMARIZE_AFTER`, моделі): до ядра додаються `CONV-002-S5`, `CONV-002-L10` і `CONV-002-NOSUM` — ще 110 викликів, 185 разом.

**Чому:**
- **Ядро щодня ловить обидва дефекти.** Основний сценарій ловить втрату справи (інваріант дедлайну — 5 з 5 у всіх трьох серіях). MEM-001 ловить підміну коду й суми навіть без чужих тем (3–5 з 5).
- **S5 і L10 щодня нічого нового не скажуть.** У трьох серіях вони дали той самий сигнал, що й основний сценарій (5 з 5), а коштують разом 75 викликів і ≈ 0.67 млн токенів — більше, ніж усе ядро. L10 — найдорожчий сценарій плану (≈ 30 % токенів), бо вікно росте з кожним кроком. Відповідь на їхнє питання «чи залежить збій від довжини» може змінитися лише після зміни згортки чи її порогу, тож їх місце — перед релізом і після таких змін.
- **Контроль доводить причину збою, але про регресію щодня нічого не додає.** Його проганяємо разом із релізним набором.
- **Як це реалізувати.** `CONV-002-NOSUM` уже має `gate: "release"`, а S5 і L10 поки мають `gate: "daily"`, тож їх треба перевести на `release`. Без прапорця `--gate` ранер проганяє всі кейси незалежно від gate. Тому щоденний прогін запускаємо з `--gate daily`, а релізний — з `--gate all`.
- **Коли рішення зміниться.** Якщо ядро почне пропускати збій, який S5 або L10 ловлять, або якщо зміняться модель чи сумаризатор, увесь план до стабілізації проганяємо щодня.

---

## 6. Залишковий ризик і рішення

*Заповнюєте:* **ДЗ**, крок 6. *У темі: «Чого профіль деградації не ловить», «Три способи виправлення».*

### 6.1. Непокриті комбінації

Щонайменше три. Щонайменше одна — «прийняти». Формат рядка той самий, що на L03.

```
1. що не покрито                    поріг згортки 8, як на стенді за замовчуванням
                                    (SUMMARIZE_AFTER_STEPS=8), × діалоги, довші за 8 кроків.
                                    Увесь план проганяємо з summarize_after 2
   що станеться, якщо зламається    у реальному довгому чаті справа зникне на кроці 9, і перше
                                    звернення назад покаже ту саму плутанину TX-0401 / TX-0402
                                    і чужий дедлайн
   чому живемо з цим зараз          механізм той самий, змінюється лише номер кроку: у 3.4
                                    крок втрати дорівнює кроку згортки в усіх сценаріях, а
                                    довжина зсуває лише прояв. Перевірка на порозі 8 потребує
                                    діалогу щонайменше з 11 кроків — дорожче за L10, і так
                                    найдорожчий сценарій плану (≈ 94k токенів за прогін)
   відкласти / прийняти             прийняти. Переглянути, якщо зміниться сумаризатор або поріг

2. що не покрито                    дві справи в одній розмові: понад 3 сутності, два спори,
                                    наприклад TX-0401 goods_not_received і TX-0402
                                    duplicate_charge
   що станеться, якщо зламається    агент змішає справи: дедлайн чи код однієї транзакції
                                    потрапить в іншу, а незворотний create_dispute піде не на ту
                                    транзакцію. Плутанину TX-0401 / TX-0402 видно вже з однією
                                    справою (3.3: 12 з 15 прогонів на lesson-05)
   чому живемо з цим зараз          жодна скарга не описує двох справ; кейсу потрібен окремий
                                    оракул на кожну справу; ціна — ще щонайменше один сценарій
                                    на 7–10 кроків (35–50 викликів на профіль)
   відкласти / прийняти             відкласти — першим кейсом наступної ітерації і обов'язково
                                    до впровадження структурованого поля справи (6.3), яке має
                                    тримати кілька справ

3. що не покрито                    проміжні точки осей: одна сутність у довгому діалозі з
                                    чужими темами (MEM-001 має лише 4 кроки і 0 перемикань), три
                                    сутності без перемикань на 7 кроках, дві сутності
   що станеться, якщо зламається    збій, що проявляється лише в цих комбінаціях, пройде
                                    непоміченим
   чому живемо з цим зараз          на всіх покритих точках крок втрати той самий — 3, а частота
                                    падінь не залежить ні від довжини (5 з 5 на 5, 7 і 10
                                    кроках), ні від перемикань (MEM-001 без перемикань: 3–5 з 5).
                                    Нова точка, найімовірніше, повторить відому відповідь, а
                                    коштуватиме 20–50 викликів
   відкласти / прийняти             прийняти
```

*Якщо все «відкласти», рішення не ухвалено: вийшов список бажань.*

### 6.2. Сліпі зони методу

| Сліпа зона | Чим закриваємо або чому приймаємо |
| --- | --- |
| Профіль не пояснює, чому сутність зникла саме на цьому кроці | **Закриваємо трейсами.** Кожен прогін робимо з `--traces` і причину читаємо з `summary.text` спану `agent.summarize`: на `lesson-05` суми 240 немає в жодній з 50 згорток 24.10, на `clean` вона є в усіх 50 (2.4, 3.3). Передумова `has_span` фіксує крок згортки, а контроль `CONV-002-NOSUM` доводить причинність: без згортки 0 падінь з 5 (3.4). Ціна — лише місце на диску, ≈ 0.5 МБ трейсів на прогін набору |
| Узгоджена помилка: інваріант зелений на хибному значенні | **Закриваємо оракулом першого кроку**, а також тим, що еталон інваріанта береться з оракула, а не зі слів агента (4.2). Для `CONV-002-*` хибний код з кроку 1 зловить контроль `goods_not_received` (`kb:disputes.md#s1`), а хибний дедлайн з кроку 2 — оракул `engine:disputes`. Дірка — `MEM-001-*`: окремої перевірки кроку 1 там немає. Закриваємо її перевіркою `tool_called_with` на `create_dispute(reason_code=duplicate_charge, amount=240.0)` рівня 1. У 10 з 10 прогонів v2 на `lesson-05` аргументи правильні, тож хибних тривог вона не дасть. Ризик реальний: накладка D07 велить називати значення впевнено, і в MEM-001-RC №5 агент без застережень підтверджує підмінений `service_not_rendered` (3.4) |
| Осі, яких немає в плані (зміна мови, повернення через добу, дві справи в одній розмові) | **Зміна мови:** приймаємо, поки ринок один (як у L03). **Повернення через добу:** приймаємо. Сесія стенду живе в пам'яті процесу без строку дії (`_sessions` у `paypilot-stand/app/agent/loop.py`), тож повернення відрізняється від продовження розмови лише годинником, а скільки часу лишилося, рахують інструменти від поточної дати. Перевіряти це варто, коли з'явиться збереження сесій між днями. **Дві справи:** відкладаємо, див. 6.1 №2 |
| Дія замість відповіді: незворотний виклик без явного «yes» | Інваріанти перевіряють значення у відповіді, а не дії. На кроці 6 агент сприймає «240 euro, as I said at the start.» як згоду і викликає `create_dispute` — у 8 з 20 прогонів із цілою пам'яттю (контроль і CONV-002 на `clean`, 3.4). **Закриваємо** перевіркою `tool_call_count` для `create_dispute` = 0 у `CONV-002-*`. Виклик уже є в трасі, тож перевірка не коштує жодного додаткового виклику. Ціна — хибна тривога, якщо в сценарій колись додадуть явне «yes» |
| Шаблон рівня 3 знаходить слово будь-де у відповіді | **Приймаємо.** На 15 прогонів MEM-001-RC на `lesson-05` хибно зелений лише один (22.10, `143756`): агент відмовився назвати код, а «duplicate-charge» прозвучало лише в пропозиції ескалації. Закрити це могла б лише перевірка суддею (рівень 7) на кожному кроці-зонді, тобто додаткові виклики моделі в кожному прогоні заради одного пропуску з 15 |
| Оракул залежить від стану пам'яті (FX «1.5» на кроці 4) | **Закриваємо** переписуванням контролю кроку 4: приймати або 1.5 %, або котирування з урахуванням безкоштовного ліміту. Зараз він хибно червоний саме тоді, коли агент пам'ятає суму: 6 із 7 червоних у контролі NOSUM (3.4) |

### 6.3. Рекомендоване виправлення D06

| Варіант | Обираємо? | Ціна | Що псується натомість |
| --- | --- | --- | --- |
| Винести сутності справи у структуроване поле | **так** | Зміна коду агента. Поле справи в стані сесії (TX, сума, reason code, дедлайн) заповнюється з аргументів і результатів інструментів (`check_dispute_eligibility`, `create_dispute`) і додається в контекст кожного кроку поза згорткою. Це кілька десятків токенів на крок (оцінка) проти ≈ 8.7k, які крок коштує зараз. Перевірка — повний план: 185 викликів, ≈ 1.54 млн токенів, ≈ 14 хв на кожному профілі | Потрібна нова логіка оновлення. Якщо клієнт змінює справу або веде дві (6.1 №2), поле треба переписувати. Інакше агент упевнено триматиметься старої справи, а це узгоджена помилка, яку інваріант не побачить. Усе, чого немає в полі, згортка й далі губить |
| Підняти `SUMMARIZE_AFTER` | ні | Зміна конфігурації, без розробки. Але кожен крок без згортки дорожчий: вікно росте приблизно на 0.5k токенів за крок, з 2.6k на кроці 1 до 7.6k на кроці 10 (5.1) | Лише відсуває крок втрати: діалог, довший за поріг, губить справу так само (3.4: довжина зсуває прояв, а не втрату). За замовчуванням поріг уже 8, тобто довгі чати до згортки й зараз доходять |
| Дописати «зберігай числа» в промпт сумаризатора | ні | Один рядок і прогін плану. На `clean` сумаризатор з інструкцією «Preserve every concrete detail…» зберіг суму, TX-0401, код і дедлайн у 50 з 50 згорток | Результат лишається ймовірнісним: будь-яка наступна правка промпту чи заміна моделі може повернути втрату. Крім того, поки діє постобробка D07, збережене число не зникає, а псується. Кожна сума, що вціліла в згортках `lesson-05` (4 з 50), уже 180.00 замість 240.00, тобто збій стає тихим і впевненим |

**Чому цей варіант під мандатом Ship it:**
- **Що вимагає мандат.** Ship it пропускає реліз, якщо щоденний гейт зелений на детермінованих перевірках грошей і правил (L03).
- **Що дає структуроване поле.** Гроші й строки справи стають детермінованими: їх беруть з інструментів, а не з того, що модель вирішила лишити в переказі. Тож щоденне ядро (75 викликів) перевіряє їх без хибних тривог через формулювання.
- **Чому не інші два варіанти.** Промпт дешевший, але лишає грошову помилку ймовірнісною, а з D07 — ще й тихою (180.00 замість 240.00). Поріг лише переносить ту саму помилку на пізніший крок.
- **Що робимо до виправлення.** Поки поле не готове, щоденний гейт тримає інваріант дедлайну TX-0401: на `lesson-05` 14 з 15 червоних у кожній серії 24.10, на `clean` 0 з 30.

---

## Останній рядок

```
що обміняли                      повне покриття 32 комбінацій осей (≈ 1 040 викликів на профіль)
                                 на 6 сценаріїв (185 викликів, 18 %), а щодня — на ядро з 3
                                 сценаріїв (75 викликів, у 1.6 раза дорожче за golden). Довжину
                                 й перемикання перевіряємо лише перед релізом: вони зсувають
                                 прояв, а не втрату
чого не робимо                   не тестуємо поріг згортки 8, дві справи в одній розмові, зміну
                                 мови й повернення через добу; не виправляємо D06 промптом чи
                                 порогом; поки не ловимо незворотну дію без явного «yes»
                                 (перевірку описано в 6.2)
за яких умов рішення зміниться   якщо ядро пропустить збій, який ловлять S5 чи L10, — увесь план
                                 щодня; якщо зміняться сумаризатор, поріг SUMMARIZE_AFTER чи
                                 модель — увесь план щодня до стабілізації; якщо з'явиться
                                 скарга про дві справи чи про спір, поданий без згоди, — ці
                                 сценарії стають щоденними; після впровадження структурованого
                                 поля інваріанти суми й дедлайну мають позеленіти на lesson-05,
                                 інакше виправлення не працює
```

---

## Чекліст

**Після лабораторної**

- [ ] У розділі 1 записано прогноз
- [ ] Листи запису 2.1 і 2.2 заповнені для всіх семи кроків, з історією і retrieval-контекстом
- [ ] У 2.3 п'ять прогонів, діапазон і медіана
- [ ] У 2.4 момент втрати і момент прояву стоять у різних рядках
- [ ] У 3.1 названо крок втрати і доведено, що retrieval-контекст на кроці прояву цілий
- [ ] У 3.2 самосуперечність класифіковано з доказом
- [ ] У 4.1 дві перевірки з результатом на `clean` і `lesson-05`

**Перед здачею ДЗ_4**

- [ ] У розділі 1 заповнено всі рядки, зокрема кількість кейсів і `set_hash`
- [ ] У 2.3 названо межу довжини діалогу
- [ ] У 3.3 є висновок контрольного прогону, у 3.4 — збої інших сценаріїв або «немає»
- [ ] У 4.2 кожен кейс має інваріант із рівнем драбини і оракул
- [ ] У розділі 5 три осі, щонайменше п'ять сценаріїв з роллю, серед них контроль, ціна повної комбінаторики і плану, розклад
- [ ] У 6.1 щонайменше три непокриті комбінації, хоча б одна «прийняти»
- [ ] У 6.3 обрано виправлення D06 і названо ціну
- [ ] Останній рядок заповнено всіма трьома пунктами
