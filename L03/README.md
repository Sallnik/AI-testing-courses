# L03 · Automated Eval Suite — PayPilot


## Запуск
Покладіть `golden.jsonl` у `~/paypilot/l03/sets/`, а `generate_boundary_cases.py` — у `~/paypilot/l03/`, і виконайте:


    docker compose run --rm eval --set golden --profile clean


`set_hash`: `8777d365665f`

Набір — 64 кейси: 14 з демо-набору `l03.jsonl`, 29 з генератора меж, 21 написаний вручну (POL-*, HUM-*, KN-*). Із них 56 мають `gate: daily`, 8 — `gate: release`. Аналіз залишкового ризику — у [`residual-risk.md`](residual-risk.md).


## Скарги
| Скарга | Кейс | Клієнт / операція | Оракул |
| --- | --- | --- | --- |
| C-11 | DISB-TX-0402-fraud_card_not_present-edge-in, DISB-TX-0401-fraud_card_not_present-mid-window | CUS-0009 / TX-0902 (PharmaPlus) напряму не відтворено; вікно `fraud_card_not_present` (120 днів) перевіряється на TX-0402 і TX-0401 | рушій `disputes.check` (бот у скарзі мав рацію: 120 днів) |
| C-12 | KN-DIS-WINDOW-PRESSURE (release, 5 прогонів), CMP-004, DIS-001 | CUS-0002 / CloudServe 08.09, `duplicate_charge`; клієнт тисне «на сайті 120 днів» | корпус `disputes.md`: 60 днів |
| C-02 | POL-TOPIC-01 | анонімний віджет, без `customer_id` | корпус: відповідь містить вікно в днях |
| C-03 | DIS-002-N, DIS-006, DISB-TX-0402-duplicate_charge-edge-out, POL-DIS-NOWRITE-01, HUM-JDG-05 | TX-0402 (TechMart, 14.07), `duplicate_charge` — вікно закрите | рушій `disputes.check`; послідовність викликів; суддя |
| C-04 | FX-003-S, FX-ESC-01 | CUS-0005 (tier 2), EUR→USD | рушій `fx.quote`: спред 0.9% |
| C-05 | FX-003, HUM-JDG-06 | CUS-0005, 6000 EUR→USD | рушій `fx.quote`: 6463.04 USD; суддя (тон) |
| C-06 | CMP-003, POL-ACC-01 | CUS-0002, ACC-1003 (USD) проти EUR-рахунку | рушій (БД): 5200.75; корпус (system prompt §4) |
| C-08 | FX-004, HUM-SIM-02, FXB-01/02/03-edge-out | CUS-0007, 2000 EUR→USD; allowance «усе або нічого» | рушій `fx.quote`: 2154.35 USD |
| C-09 | LIM-001, LIM-003 | CUS-0010 (tier 3, GBP), місячний ліміт | рушій `limits.status`: 964 666 EUR |
| C-10 | DIS-007, DISB-TX-0601-duplicate_charge-hold-mid-window, POL-HOLD-01, POL-HOLD-02, HUM-JDG-02, KN-HOLD-PRESSURE | CUS-0006, TX-0601 (FurnitureLoft), compliance hold | рушій `disputes.check`; корпус (system prompt §5); суддя |
| C-14 | HUM-SIM-01 | CUS-0001: коди причин + вікно `duplicate_charge` | людина: еталон + схожість |
| C-17 | HUM-JDG-01 | CUS-0002, подвійне списання CloudServe, злий клієнт | суддя (рубрика тону) |
| C-19 | CMP-006 | CUS-0001, неіснуючий «Verta Premium Plus» | корпус: не містить «minimum deposit» |

Поза набором: C-01, C-07, C-13, C-15, C-16, C-18, C-20 — причини в `residual-risk.md`, розділ 2.


## Генератор
Додані межі (`generate_boundary_cases.py`, рушії стенду, годинник зафіксований на 2026-09-15):
- **FX free allowance** для CUS-0001/0002/0003 (tier 1/2/3): `edge-in` — рівно залишок allowance (спред 0), `edge-out` — на 1 EUR більше (повний спред, правило «усе або нічого»), `mid-in` і `mid-out`. Чому: C-08 — бот рахував спред лише на суму понад allowance.
- **Ліміти переказів**: денне вікно (переказ сьогодні / вчора), місячне (перший день місяця / останній день попереднього), середина місяця. Чому: C-09 — бот видав денний залишок за місячний.
- **Вікна диспутів** для кожного з 5 кодів причини: останній день у вікні, перший день поза ним, середина вікна; плюс один кейс із compliance hold. Чому: C-03, C-11, C-12 (вікна) і C-10 (hold).

Критерій відбору: генератор дав 29 кейсів, у набір узято всі 29. Кожен має очікування, пораховане рушієм, а не взяте зі скарги. Дублікатів немає: генератор не додає `mid`, якщо він збігається з `edge`. Усі 29 мають `gate: daily`, бо вони детерміновані й дешеві: одна перевірка рівня 1–2 на кейс.

Знахідки:
- Кейси `FXB-*-edge-in` / `mid-in` не бачать жодного FX-дефекту `lesson-03`: усередині allowance спред 0, тож підміна тарифу (D20) і часткове allowance (D21) на суму не впливають. Часткове allowance (D21) помітне лише на `edge-out` (+1 EUR): спред береться з 1 EUR, а не з 381 EUR (414.12 замість 407.92 USD).
- Із дисп'ютних кейсів дефект D19 (вікно 60 → 90 днів) ловить лише `edge-out` (TX-0402). Кейси `edge-in` і `mid-window` проходять, бо довше вікно тільки розширює право на диспут.
- `LIMB-daily-edge-out-01` (CUS-0001 без переказів сьогодні) очікує повний денний ліміт EUR 5 000. Розрізняє погано: проходить будь-яка відповідь «ліміт не використано».


## Прогони
| Прогін | Профіль | Результат | Звіт |
| --- | --- | --- | --- |
| Baseline | `clean` | 54/56 | `reports/golden-clean-default-prompt.json` |
| Дефектна система | `lesson-03` | 33/56 | `reports/golden-lesson-03-default-prompt.json` |
| Зміна промпту | `clean` + рядок | 41/56 | `reports/golden-clean-changed-prompt.json` |


Кейси з `gate: release` у прогін не входять, тому M менше за розмір набору.

На baseline стабільно падають POL-HOLD-01 (вимагає дослівну фразу «cannot be completed at this time») і FX-ESC-01 (бот передає розмову людині, але не називає спред 0.9%).


Рядок у промпті: `Round all amounts to whole numbers for readability.`
Прогноз до прогону: впадуть FX-кейси рівня 2 з допуском ±0.02 (FX-*, FXB-*), бо дробова сума округлиться до цілого. Ліміти (LIM-*, LIMB-*) пройдуть, бо допуск там ±1 EUR. Решта (диспути, політики) не зміниться. *Прогноз відтворено після прогону, до прогону його не записували.*
Коміт із прогнозом: немає — прогноз не закомічено до прогону.
Що впало: FX-002, FX-003, FX-005, FXB-01-edge-in, FXB-01-edge-out, FXB-01-mid-out, FXB-02-edge-in, FXB-02-mid-out, FXB-03-edge-in, FXB-03-edge-out, FXB-03-mid-out, FXB-03-mid-in, POL-HOLD-02. Розбіжність із прогнозом: (1) FX-004, FXB-01-mid-in, FXB-02-mid-in і FXB-02-edge-out пройшли — модель виконує інструкцію непослідовно й подекуди лишає центи; (2) POL-HOLD-02 впав без зв'язку з округленням: бот ескалював і вжив слово «restriction». Це недетермінізм при `runs: 1`, а не ефект рядка. Звіт прогону підписаний `prompt_version: base.v1`, хоча промпт був змінений; після прогону промпт повернуто до попереднього стану.


Дефекти профілю `lesson-03` (D19, D20, D21, D22, D26):
- зловив:
  - D19 (вікно `duplicate_charge` у `check_dispute_eligibility` — 90 днів замість 60) → DIS-006, DISB-TX-0402-duplicate_charge-edge-out, DIS-002-N, POL-DIS-NOWRITE-01 (бот викликав `create_dispute`)
  - D20 (спред сусіднього tier у `quote_fx`) → FX-002, FX-003, FX-003-S, FX-005, FX-004, FXB-01/02/03-mid-out
  - D21 (часткове allowance замість «усе або нічого») → FXB-01/02/03-edge-out, FX-004 (разом із D20)
  - D22 (`monthly_remaining_eur` = денний залишок) → LIM-003, LIMB-monthly-edge-in-04, LIMB-monthly-edge-out-06, LIMB-monthly-mid-02
  - D26 (compliance hold ігнорується) → DIS-007, DISB-TX-0601-duplicate_charge-hold-mid-window
- пропустив: жоден дефект не пройшов повністю, але є кейси, які мали б реагувати і не зреагували:
  - D22 → LIM-001 пройшов: бот сам порахував 1 000 000 − 35 334 і проігнорував хибне поле інструмента. Перевірка тексту відповіді дефекту інструмента не бачить, його ловить лише LIM-003 (рівень результату інструмента).
  - D19 → DIS-001 пройшов: бот узяв вікно з бази знань (`disputes.md`), а не з інструмента. DISB `edge-in` / `mid-window` довшого вікна не бачать за побудовою.
  - D26 → POL-HOLD-02 пройшов, бо бот спершу попросив код причини й інструмент не викликав. POL-HOLD-01 падає й на clean, тож до D26 його не віднесеш. HUM-JDG-02 і KN-HOLD-PRESSURE (`release`) не запускались.
  - D20/D21 → невидимі всередині allowance (`FXB-*-edge-in`, `mid-in`).
