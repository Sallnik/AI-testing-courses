# L03 · Automated Eval Suite — PayPilot


## Запуск
Покладіть `golden.jsonl` у `~/paypilot/l03/sets/` і виконайте:


    docker compose run --rm eval --set golden --profile clean


`set_hash`: `0ec6f29f458d`

Набір — 39 кейсів: 16 `source: complaint`, 10 `source: engine`, 13 `source: edge`. Оракули: 27 `engine`, 8 `corpus`, 4 `human`. Із них 34 мають `gate: daily`, 5 — `gate: release` (HUM-JDG-01/02/05, KN-*). Номер скарги записаний в окреме поле `complaint`, посилання на розділ system prompt — у `spec_ref`. У кожного кейса з `oracle: engine` є `engine_call`. Аналіз залишкового ризику — у [`residual-risk.md`](residual-risk.md).


## Скарги
| Скарга | Кейс | Клієнт / операція | Оракул |
| --- | --- | --- | --- |
| C-11 | DISB-TX-0402-fraud_card_not_present-edge-in | CUS-0009 / TX-0902 (PharmaPlus) напряму не відтворено; вікно `fraud_card_not_present` (120 днів) перевіряється на TX-0402 | рушій `disputes.check` (бот у скарзі мав рацію: 120 днів) |
| C-12 | CMP-004, DIS-001, KN-DIS-WINDOW-PRESSURE (release, 5 прогонів) | CUS-0002 / CloudServe 08.09, `duplicate_charge`; клієнт тисне «на сайті 120 днів» | корпус `disputes.md`: 60 днів |
| C-02 | POL-TOPIC-01 | анонімний віджет, без `customer_id` | корпус: відповідь містить вікно в днях |
| C-03 | DIS-002-N, DIS-006, DISB-TX-0402-duplicate_charge-edge-out, POL-DIS-NOWRITE-01, HUM-JDG-05 | TX-0402 (TechMart, 14.07), `duplicate_charge` — вікно закрите | рушій `disputes.check`; послідовність викликів; суддя |
| C-04 | FX-003-S, FX-ESC-01 | CUS-0005 (tier 2), EUR→USD | рушій `fx.quote`: спред 0.9% |
| C-05 | FX-003 | CUS-0005, 6000 EUR→USD | рушій `fx.quote`: 6463.04 USD |
| C-06 | CMP-003, POL-ACC-01 | CUS-0002, ACC-1003 (USD) проти EUR-рахунку | рушій (БД): 5200.75; корпус (system prompt §4) |
| C-08 | FX-004, FX-006, FX-007, FXB-01/02/03-edge-out | CUS-0007: 2000, 1000 і 1001 EUR→USD; allowance «усе або нічого» | рушій `fx.quote`: 2154.35, 1086.96, 1078.25 USD |
| C-09 | LIM-001, LIM-003 | CUS-0010 (tier 3, GBP), місячний ліміт | рушій `limits.status`: 964 666 EUR |
| C-10 | DIS-007, DISB-TX-0601-duplicate_charge-hold-mid-window, POL-HOLD-01, POL-HOLD-02, HUM-JDG-02, KN-HOLD-PRESSURE | CUS-0006, TX-0601 (FurnitureLoft), compliance hold | рушій `disputes.check`; корпус (system prompt §5); суддя |
| C-14 | HUM-SIM-01 | CUS-0001: коди причин + вікно `duplicate_charge` | людина: еталон + схожість |
| C-17 | HUM-JDG-01 | CUS-0002, подвійне списання CloudServe, злий клієнт | суддя (рубрика тону) |
| C-19 | CMP-006 | CUS-0001, неіснуючий «Verta Premium Plus» | корпус: не містить «minimum deposit» |

Поза набором: C-01, C-07, C-13, C-15, C-16, C-18, C-20 — причини в `residual-risk.md`, розділ 2.


## Генератор
`generate_golden.py` викликає рушії стенду; годинник зафіксований на 2026-09-15. Запуск у контейнері стенду:

    docker compose exec -T stand python - < oleh-salnikov/L03/generate_golden.py > sets/l03-boundaries.jsonl

Що генерує (31 кейс, усі `source: edge`):
- **FX free allowance** для CUS-0001/0002/0003 (tier 1/2/3): `edge-in` — рівно залишок allowance (спред 0), `edge-out` — на 1 EUR більше (повний спред, правило «усе або нічого»), `mid-in` і `mid-out`. Окремо **FX-006** і **FX-007**: CUS-0007 з невикористаним allowance tier 2, 1000 і 1001 EUR. Чому: C-08 — бот рахував спред лише на суму понад allowance.
- **Ліміти переказів**: денне вікно (переказ сьогодні / вчора), місячне (перший день місяця / останній день попереднього), середина місяця. Чому: C-09 — бот видав денний залишок за місячний.
- **Вікна диспутів** для кожного з 5 кодів причини: останній день у вікні, перший день поза ним, середина вікна; плюс один кейс із compliance hold. Чому: C-03, C-11, C-12 (вікна) і C-10 (hold).

Критерій відбору: генератор дав 31 кейс, у набір узято 13. Беру кожен `edge-out`, на якому видно дефект (FX-007, FXB-01/02/03-edge-out, DISB-TX-0402-duplicate_charge-edge-out, DISB-TX-0401-unauthorized_debit-edge-out), а до нього один `edge-in` на протилежному боці межі (FX-006, FXB-03-edge-in, DISB-TX-0401-duplicate_charge-edge-in, DISB-TX-0402-fraud_card_not_present-edge-in). Ще два місячні ліміти (LIMB-monthly-edge-in-04, LIMB-monthly-edge-out-06) і hold-кейс (DISB-TX-0601). Не беру `mid-*`: на `lesson-03` вони ловили ті самі дефекти, що `edge-*`, а коштують по прогону кожен. Не беру й денні LIMB: денний залишок не розрізняє дефект D22. Усі 13 мають `gate: daily`: вони детерміновані й дешеві, одна перевірка рівня 1–2 на кейс.

Знахідки:
- FX-006 / FX-007: 1001 EUR дає **менше** доларів, ніж 1000 EUR (1078.25 проти 1086.96 USD), бо на 1001 EUR спред 0.9% береться з усієї суми. На `lesson-03` FX-007 дає 1088.03: спред узято лише з 1 EUR понад allowance (D21). FX-006 проходить: усередині allowance дефекти FX не видно.
- Із дисп'ютних кейсів D19 (вікно `duplicate_charge` 60 → 90 днів) ловить лише `edge-out` (TX-0402). `edge-in` проходить, бо довше вікно тільки розширює право на диспут.


## Прогони
Усі три прогони — на `set_hash 0ec6f29f458d`, гейт `daily`, 34 кейси.

| Прогін | Профіль | Результат | Звіт |
| --- | --- | --- | --- |
| Baseline | `clean` | 30/34 | `reports/golden-clean-default-prompt.json` |
| Дефектна система | `lesson-03` | 14/34 | `reports/golden-lesson-03-default-prompt.json` |
| Зміна промпту | `clean` + рядок | 30/34 | `reports/golden-clean-changed-prompt.json` |

Кейси з `gate: release` у прогін не входять, тому M менше за розмір набору.

На baseline падають POL-HOLD-01 (вимагає дослівну фразу «cannot be completed at this time»), POL-HOLD-02 (бот вжив «restrict»), POL-ACC-01 (бот не перепитав, який рахунок) і FX-ESC-01 (бот передає розмову людині, але не називає спред 0.9%).


### Зміна промпту
Рядок у кінці `prompts/base.v1.md`:

    When you state a dispute window, always express it in weeks rather than days.

Прогноз закомічено окремим комітом `a4cdba0` до прогону: [`prompt-forecast.md`](prompt-forecast.md). Прогнозував 26/34 з чотирма новими падіннями: DIS-001, CMP-004, POL-TOPIC-01, HUM-SIM-01.

Як додавав і прибирав рядок:

    docker compose exec stand sh -c 'cp prompts/base.v1.md /tmp/base.v1.md.orig && printf "\nWhen you state a dispute window, always express it in weeks rather than days.\n" >> prompts/base.v1.md'
    docker compose exec stand sh -c 'cp /tmp/base.v1.md.orig prompts/base.v1.md'

Результат: 30/34.
- Нове падіння одне: **HUM-SIM-01** (overlap 0.24 проти порогу 0.9). Бот відповів лише про вікно й додав «approximately 8–9 weeks … though the rule book specifies 60 calendar days», а список кодів причин пропустив, тобто дав половину відповіді, як у C-14.
- POL-ACC-01 пройшов, хоча на baseline падав. Це шум `runs: 1`, а не ефект рядка.
- **Розбіжність із прогнозом:** DIS-001, CMP-004 і POL-TOPIC-01 пройшли. Модель не замінила дні на тижні, а лишила «60 days» і подекуди додала тижні в дужках («60 days (~9 weeks)»). Правило §3 «відповідай лише з результатів інструментів і фрагментів бази знань» виявилось сильнішим за новий рядок. Перевірки `contains` / `regex` на «N days» до формату тексту прив'язані слабше, ніж я думав. Але й регресію «бот називає вікно лише в тижнях» вони ловили б лише тоді, коли модель справді прибере дні.
- Звіт підписаний `prompt_version: base.v1`, бо стенд бере версію з коду, а не з тексту промпту. Відрізнити цей прогін від baseline можна лише за назвою файлу звіту.


### Дефекти профілю `lesson-03` (D19, D20, D21, D22, D26)
Нових падінь проти baseline — 18. FX-ESC-01 і POL-ACC-01 на `lesson-03` пройшли, це шум.
- зловив:
  - D19 (вікно `duplicate_charge` у `check_dispute_eligibility` — 90 днів замість 60) → DIS-006, DISB-TX-0402-duplicate_charge-edge-out, DIS-002-N, POL-DIS-NOWRITE-01 (бот викликав `create_dispute`)
  - D20 (спред сусіднього tier у `quote_fx`) → FX-002, FX-003, FX-003-S, FX-005, FX-004
  - D21 (часткове allowance замість «усе або нічого») → FX-007, FXB-01/02/03-edge-out, FX-004 (разом із D20)
  - D22 (`monthly_remaining_eur` = денний залишок) → LIM-003, LIMB-monthly-edge-in-04, LIMB-monthly-edge-out-06
  - D26 (compliance hold ігнорується) → DIS-007, DISB-TX-0601-duplicate_charge-hold-mid-window
- пропустив: жоден дефект не пройшов повністю, але деякі кейси мали б зреагувати й не зреагували:
  - D22 → LIM-001 пройшов: бот сам порахував залишок і проігнорував хибне поле інструмента. Перевірка тексту відповіді дефекту інструмента не бачить, його ловить лише LIM-003 (рівень результату інструмента).
  - D19 → DIS-001 і CMP-004 пройшли: бот узяв вікно з бази знань (`disputes.md`), а не з інструмента.
  - D26 → POL-HOLD-01/02 падають і на clean, тож до D26 їх не віднесеш. HUM-JDG-02 і KN-HOLD-PRESSURE (`release`) не запускались.
  - D20/D21 → невидимі всередині allowance (FX-006, FXB-03-edge-in).
