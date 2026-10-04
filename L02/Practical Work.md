# 1 Set Complains Layers
# Двадцять скарг із Slack · корпус до L02 і L03

Вхідний матеріал двох лабораторних. На **L02** скарги розкладають за шарами
(пошук / генерація / дія) і збирають із них робочий набір на 12–15 кейсів. На
**L03** ті самі скарги розкладають на три купи: придатні одразу, придатні
після добору контексту, непридатні.

Це повідомлення з каналу `#cx-escalations` за 8–15 вересня 2026 року, у тому
вигляді, як їх написала підтримка: без ID, з одруківками і з власними
здогадками авторів. Автор скарги — не оракул: його цифра — це те, що почув
клієнт або запам'ятав співробітник. Імена, рахунки й транзакції взяті з seed
стенду PayPilot, тож кожну операцію можна знайти в базі.

Колонка «Українською» — переклад для зручності читання. Першоджерело —
оригінал у колонці «Повідомлення»: розбирайте саме його.

| ID | Дата | Хто | Повідомлення | Українською | Шар |
|---|---|---|---|---|---|
| C-01 | 11.09 | support L1 | CUS-0008 (Hugo) asked the bot what a SWIFT transfer costs. bot said the fee is 1.5%, no hesitation. tariff sheet says EUR 15 + 0.3%. he made the transfer based on that and now asks why the fee is different | CUS-0008 (Hugo) спитав бота, скільки коштує SWIFT-переказ. бот відповів, що комісія 1.5%, без жодних вагань. у тарифній сітці EUR 15 + 0.3%. він зробив переказ, спираючись на це, і тепер питає, чому комісія інша | Генерація |
| C-02 | 12.09 | support L1 | customer on the public widget asked how many days she has to dispute a card payment. bot answered with a paragraph about her daily and monthly limits. nothing wrong in it, just not what she asked. no customer id, she wasn't logged in | клієнтка у публічному віджеті спитала, скільки днів вона має, щоб оскаржити платіж карткою. бот відповів абзацом про її денні та місячні ліміти. помилок там немає, просто це не те, про що вона питала. customer id немає, вона не була залогінена | Генерація |
| C-03 | 15.09 | support L2 | bot told the TechMart guy he can still dispute the double charge from July. we filed it, got rejected: window already closed. he's furious and wants compensation. didn't save the tx id, sorry | бот сказав хлопцю з TechMart, що він ще може оскаржити подвійне списання з липня. ми подали, отримали відмову: вікно вже закрите. він лютує і хоче компенсацію. tx id не зберегли, вибачте | Дія |
| C-04 | 10.09 | support L1 | Emma Rossi (CUS-0005) asked what spread she pays on EUR→USD. bot said 1.5%. she's tier 2, isn't tier 2 0.9%? | Emma Rossi (CUS-0005) спитала, який спред вона платить на EUR→USD. бот сказав 1.5%. вона на tier 2, хіба для tier 2 не 0.9%? | Дія |
| C-05 | 10.09 | support L1 | same customer, second chat: asked for a full breakdown of 6000 EUR → USD. bot listed the rate, the spread, everything, then "final amount: 6,500 USD". the lines above don't add up to that. she has a screenshot | та сама клієнтка, другий чат: попросила повну розбивку 6000 EUR → USD. бот перелічив курс, спред, усе, а потім «підсумкова сума: 6,500 USD». рядки вище в таку суму не складаються. у неї є скриншот | Генерація |
| C-06 | 09.09 | support L1 | CUS-0002 asked for the exact balance of his USD account ACC-1003. bot answered 8,900. that's his EUR account. he has two and the bot mixed them up | CUS-0002 спитав точний баланс свого USD-рахунку ACC-1003. бот відповів 8,900. це його EUR-рахунок. у нього їх два, і бот їх переплутав | Генерація |
| C-07 | 14.09 | ops | fx quote looked off again, customer says we charged more than the app showed. cant remember which account | fx-котирування знову виглядало дивно, клієнт каже, що ми списали більше, ніж показував застосунок. не пам'ятаю, який рахунок | Дія |
| C-08 | 13.09 | support L2 | question on the rule. Greta (CUS-0007) converted 2000 EUR → USD, the bot's breakdown charged spread only on the 1000 "above your free allowance". I thought the allowance is all-or-nothing? if the bot is right our pricing page is wrong | питання щодо правила. Greta (CUS-0007) конвертувала 2000 EUR → USD, у розбивці бота спред нараховано тільки на 1000 «понад ваш безкоштовний ліміт». я думала, що ліміт працює за принципом усе або нічого? якщо бот правий, то наша сторінка з цінами помилкова | Дія |
| C-09 | 15.09 | CX lead | Jonas from the GBP business account asked how much of his monthly transfer limit is left before a big supplier payment. bot said about 95k. he's tier 3, monthly is 1M and he's only sent ~30k GBP this month. he almost split the payment into three for nothing | Jonas із бізнес-рахунку в GBP спитав, скільки залишилося від його місячного ліміту переказів перед великим платежем постачальнику. бот сказав близько 95k. він на tier 3, місячний ліміт 1M, і цього місяця він відправив лише ~30k GBP. він мало не розбив платіж на три частини даремно | Дія |
| C-10 | 12.09 | compliance | bot told Farid Aliyev (CUS-0006) he can dispute TX-0601 (FurnitureLoft, never delivered). his account is under compliance hold, no new disputes until the review ends. now he thinks we're blocking him on purpose. also check the wording: the bot must not mention the review to him | бот сказав Farid Aliyev (CUS-0006), що він може оскаржити TX-0601 (FurnitureLoft, товар так і не доставили). його рахунок під compliance hold, жодних нових диспутів, доки не закінчиться перевірка. тепер він думає, що ми блокуємо його навмисно. ще перевірте формулювання: бот не має згадувати йому про перевірку | Дія |
| C-11 | 13.09 | support L1 | bot told Iryna (CUS-0009) she has 120 days to dispute the PharmaPlus card payment she says she never made, someone used her card online. I always thought it's 60 days for any dispute?? someone check before she waits too long | бот сказав Iryna (CUS-0009), що вона має 120 днів, щоб оскаржити платіж карткою в PharmaPlus, якого, за її словами, вона не робила, хтось скористався її карткою онлайн. я завжди думала, що на будь-який диспут 60 днів?? хтось перевірте, поки вона не прочекала надто довго | Дія |
| C-12 | 14.09 | support L1 | CUS-0002 got charged twice by CloudServe on Sep 8. bot told him he has 60 days to dispute. our help page says disputes can be raised within 120 days. which one is it? one of them is wrong | у CUS-0002 CloudServe двічі списав гроші 8 вересня. бот сказав йому, що на оскарження є 60 днів. на нашій сторінці довідки написано, що диспут можна відкрити протягом 120 днів. то як правильно? щось одне з цього помилкове | Дія |
| C-13 | 11.09 | support L2 | asked the bot to pull the FX spread table from our docs for all tiers (customer wanted it in writing). table looks clean, but tier 3 free allowance says EUR 1,500. pricing page says 5,000. where does 1,500 come from? | попросила бота витягнути з наших документів таблицю FX-спредів для всіх tier (клієнт хотів отримати її письмово). таблиця виглядає охайно, але безкоштовний ліміт для tier 3 вказано EUR 1,500. на сторінці з цінами 5,000. звідки взялося 1,500? | Пошук |
| C-14 | 12.09 | support L2 | customer wanted two things: the list of dispute reason codes AND the window for a duplicate charge. bot gave the list and stopped there. asked again, same thing, half an answer | клієнт хотів дві речі: список кодів причин диспуту І вікно для подвійного списання. бот дав список і на цьому зупинився. спитали ще раз, те саме, половина відповіді | Генерація |
| C-15 | 09.09 | support L1 | 5 tickets since morning: mobile app freezes on the Cards screen after yesterday's update. chat works fine, it's the app itself | 5 тікетів від ранку: мобільний застосунок зависає на екрані Cards після вчорашнього оновлення. чат працює нормально, проблема в самому застосунку | Бага апки |
| C-16 | 13.09 | support L1 | customer asked the bot if we have cashback on card payments like other banks do. bot said Verta doesn't offer cashback. customer says that's a terrible answer and wants it fixed | клієнт спитав бота, чи є в нас кешбек на платежі карткою, як в інших банках. бот сказав, що Verta не пропонує кешбек. клієнт каже, що це жахлива відповідь, і хоче, щоб це виправили | Не можливо оцінити |
| C-17 | 14.09 | CX lead | customer wrote in angry about being charged twice for the same order. bot replied with three paragraphs of dispute policy and "as per our terms". no acknowledgement, no next step. she closed the chat and called the hotline. facts were fine, it's the tone | клієнтка написала розлючена через те, що з неї двічі списали за те саме замовлення. бот відповів трьома абзацами політики диспутів і «згідно з нашими умовами». жодного визнання проблеми, жодного наступного кроку. вона закрила чат і подзвонила на гарячу лінію. факти були правильні, проблема в тоні | Все гуд |
| C-18 | 12.09 | support L2 | long chat with Danylo (CUS-0004) about disputing TX-0401. at the start he said the amount was exactly 240.00 EUR. a few questions later (timelines, notifications) he asked the bot to remind him the exact amount, and it couldn't. he had to repeat everything | довгий чат із Danylo (CUS-0004) про оскарження TX-0401. на початку він сказав, що сума була рівно 240.00 EUR. за кілька запитань (терміни, сповіщення) він попросив бота нагадати точну суму, і той не зміг. йому довелося повторювати все заново | Пошук |
| C-19 | 08.09 | support L1 | bot described a "Verta Premium Plus savings account" to CUS-0001: interest rate, minimum deposit, terms, all of it. we don't have such a product. she wants to open one | бот описав CUS-0001 «ощадний рахунок Verta Premium Plus»: відсоткова ставка, мінімальний депозит, умови, все повністю. у нас немає такого продукту. вона хоче його відкрити | Генерація |
| C-20 | 14.09 | CX lead | 1-star app store review: "your chatbot lies about fees". no name, no date, no screenshot. marketing asks if we're on it | відгук на 1 зірку в app store: «ваш чат-бот бреше про комісії». ні імені, ні дати, ні скриншоту. маркетинг питає, чи ми цим займаємося | Не можливо оцінити |

## 2. Clean Run Tests

**Defects:** – · **Prompt:** base.v1 · **Provider:** anthropic · **Judge:** claude-haiku-4-5

| Case | domain | faith (R1 / R2) | answe (R1 / R2) | hallu (R1 / R2) |
|------|--------|-----------------|-----------------|-----------------|
| C-01 | ok | 1.0 / 0.0 | 1.0 / 1.0 | – |
| C-02 | – | – | 1.0 / 1.0 | – |
| C-03 | ok | 0.8 / 0.8 | 1.0 / 1.0 | 0.0 / 0.0 |
| C-04 | ok | 0.778 / 0.8 | 1.0 / 1.0 | 0.0 / 0.0 |
| C-05 | ok | 0.9 / 0.714 | 0.9 / 1.0 | – |
| C-06 | ok | 1.0 / 1.0 | 1.0 / 1.0 | – |
| C-07 | ok | 1.0 / 0.857 | 1.0 / 1.0 | – |
| C-08 | ok | 0.833 / 0.857 | 1.0 / 1.0 | 0.0 / 0.0 |
| C-09 | ok | 1.0 / 1.0 | 1.0 / 1.0 | – |
| C-10 | ok | 0.5 / 0.333 | 1.0 / 0.8 | – |
| C-11 | ok | 0.875 / 1.0 | 1.0 / 0.5 | – |
| C-12 | ok | 0.857 / 1.0 | 1.0 / 1.0 | – |
| C-19 | ok | 0.6 / 1.0 | 1.0 / 1.0 | – |

## 3. Lesson 2 Profile Tests

**Defects:** D04, D05, D16, D19, D20, D25 · **Prompt:** base.v1+D04+D05+D25 · **Provider:** anthropic · **Judge:** claude-haiku-4-5

| Case | domain | faith (R1 / R2 / R3) | answe (R1 / R2 / R3) | hallu (R1 / R2 / R3) |
|------|--------|----------------------|----------------------|----------------------|
| C-01 | **FAIL** | 0.0 / 0.0 / 0.0 | 1.0 / 1.0 / 1.0 | – |
| C-02 | – | – | 1.0 / 1.0 / 1.0 | – |
| C-03 | **FAIL** | 0.75 / 1.0 / 1.0 | 1.0 / 1.0 / 1.0 | 1.0 / 1.0 / 1.0 |
| C-04 | **FAIL** | 0.444 / 0.625 / 0.889 | 0.8 / 1.0 / 1.0 | 0.667 / 0.667 / 1.0 |
| C-05 | **FAIL** | 0.571 / 0.8 / 0.875 | 1.0 / 0.833 / 1.0 | – |
| C-06 | **FAIL** | 1.0 / 0.667 / 1.0 | 0.5 / 0.667 / 0.714 | – |
| C-07 | **FAIL** | 0.778 / 0.667 / 0.5 | 1.0 / 1.0 / 1.0 | – |
| C-08 | **FAIL** | 0.833 / 0.7 / 0.583 | 0.923 / 1.0 / 0.917 | 1.0 / 1.0 / 1.0 |
| C-09 | ok | 1.0 / 1.0 / 0.8 | 0.75 / 1.0 / 1.0 | – |
| C-10 | ok | 0.333 / 0.4 / 0.667 | 0.5 / 1.0 / 1.0 | – |
| C-11 | ok | 0.857 / 1.0 / 0.909 | 1.0 / 1.0 / 1.0 | – |
| C-12 | **FAIL** | 1.0 / 0.667 / 0.8 | 1.0 / 0.727 / 1.0 | – |
| C-19 | ok | 0.2 / 0.0 / 0.0 | 1.0 / 0.5 / 0.667 | – |

## Delta table: domain / faith / answe
**Runs:** run-1…run-3 (основний прогін) та Clean-1, Clean-2 (Clean Run).

- Mean(3) — середнє run-1…run-3; Clean Mean — середнє Clean-1 і Clean-2
- **Δ Runs** — max − min по run-1…run-3; **жирний** ≥ 0.3
- **Δ Clean** — |Clean-2 − Clean-1|; **жирний** ≥ 0.3
- **Δ Clean − Δ Runs** — мінус = Clean Run стабільніший, плюс = Clean Run нестабільніший; **жирний** якщо |різниця| ≥ 0.3
- `—` — метрика відсутня

### domain

| Case | run-1 | run-2 | run-3 | Stable (3 runs) | Clean-1 | Clean-2 | Clean vs runs |
|---|---|---|---|---|---|---|---|
| C-01 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-02 | - | - | - | stable | - | - | same |
| C-03 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-04 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-05 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-06 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-07 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-08 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-09 | ok | ok | ok | stable | ok | ok | same |
| C-10 | ok | ok | ok | stable | ok | ok | same |
| C-11 | ok | ok | ok | stable | ok | ok | same |
| C-12 | FAIL | FAIL | FAIL | stable | ok | ok | **FAIL → ok** |
| C-19 | ok | ok | ok | stable | ok | ok | same |

### faith

| Case | run-1 | run-2 | run-3 | Clean-1 | Clean-2 | Mean(3) | Clean Mean | Δ Runs | Δ Clean | Δ Clean − Δ Runs |
|------|-------|-------|-------|-------|-------|-------|-----|---|---|---|
| C-01 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | **1.000** | **+1.000** |
| C-02 | — | — | — | — | — | — | — | — | — | — |
| C-03 | 0.750 | 1.000 | 1.000 | 0.800 | 0.800 | 0.917 | 0.800 | 0.250 | 0.000 | -0.250 |
| C-04 | 0.444 | 0.625 | 0.889 | 0.778 | 0.800 | 0.653 | 0.789 | **0.445** | 0.022 | **-0.423** |
| C-05 | 0.571 | 0.800 | 0.875 | 0.900 | 0.714 | 0.749 | 0.807 | **0.304** | 0.186 | -0.118 |
| C-06 | 1.000 | 0.667 | 1.000 | 1.000 | 1.000 | 0.889 | 1.000 | **0.333** | 0.000 | **-0.333** |
| C-07 | 0.778 | 0.667 | 0.500 | 1.000 | 0.857 | 0.648 | 0.928 | 0.278 | 0.143 | -0.135 |
| C-08 | 0.833 | 0.700 | 0.583 | 0.833 | 0.857 | 0.705 | 0.845 | 0.250 | 0.024 | -0.226 |
| C-09 | 1.000 | 1.000 | 0.800 | 1.000 | 1.000 | 0.933 | 1.000 | 0.200 | 0.000 | -0.200 |
| C-10 | 0.333 | 0.400 | 0.667 | 0.500 | 0.333 | 0.467 | 0.416 | **0.334** | 0.167 | -0.167 |
| C-11 | 0.857 | 1.000 | 0.909 | 0.875 | 1.000 | 0.922 | 0.938 | 0.143 | 0.125 | -0.018 |
| C-12 | 1.000 | 0.667 | 0.800 | 0.857 | 1.000 | 0.822 | 0.928 | **0.333** | 0.143 | -0.190 |
| C-19 | 0.200 | 0.000 | 0.000 | 0.600 | 1.000 | 0.067 | 0.800 | 0.200 | **0.400** | +0.200 |
| **Avg** | **0.647** | **0.627** | **0.669** | **0.845** | **0.780** | **0.648** | **0.813** | **0.256** | **0.184** | **-0.072** |

### answe

| Case | run-1 | run-2 | run-3 | Clean-1 | Clean-2 | Mean(3) | Clean Mean | Δ Runs | Δ Clean | Δ Clean − Δ Runs |
|---|---|---|---|---|---|---|---|---|---|---|
| C-01 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0 |
| C-02 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0 |
| C-03 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0 |
| C-04 | 0.800 | 1.000 | 1.000 | 1.000 | 1.000 | 0.933 | 1.000 | 0.200 | 0.000 | -0.200 |
| C-05 | 1.000 | 0.833 | 1.000 | 0.900 | 1.000 | 0.944 | 0.950 | 0.167 | 0.100 | -0.067 |
| C-06 | 0.500 | 0.667 | 0.714 | 1.000 | 1.000 | 0.627 | 1.000 | 0.214 | 0.000 | -0.214 |
| C-07 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0 |
| C-08 | 0.923 | 1.000 | 0.917 | 1.000 | 1.000 | 0.947 | 1.000 | 0.083 | 0.000 | -0.083 |
| C-09 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 0.917 | 1.000 | 0.250 | 0.000 | -0.250 |
| C-10 | 0.500 | 1.000 | 1.000 | 1.000 | 0.800 | 0.833 | 0.900 | **0.500** | 0.200 | **-0.300** |
| C-11 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 1.000 | 0.750 | 0.000 | **0.500** | **+0.500** |
| C-12 | 1.000 | 0.727 | 1.000 | 1.000 | 1.000 | 0.909 | 1.000 | 0.273 | 0.000 | -0.273 |
| C-19 | 1.000 | 0.500 | 0.667 | 1.000 | 1.000 | 0.722 | 1.000 | **0.500** | 0.000 | **-0.500** |
| **Avg** | **0.883** | **0.902** | **0.946** | **0.992** | **0.946** | **0.910** | **0.969** | **0.168** | **0.062** | **-0.107** |

Avg для Δ-колонок — середня дельта по кейсах (а не дельта середніх).

# 4 Find green metric but incorrect conclusion
Faith >= 0.85: C-03, C-06, C-09, C-11
Faith + Domain: C-03, C-06

## Complain: C-03
### Question
I'm CUS-0004. I want to dispute my transaction TX-0402 as double charge.

### Clean Answer
Unfortunately, I cannot open a dispute for transaction TX-0402. The dispute window for duplicate charge claims has expired. The transaction dates from 14 July 2026, and the 60-day dispute period ended on 12 September 2026. As of today (15 September 2026), the deadline has passed.

Your next steps:
- If you believe there are exceptional circumstances, you can escalate this to our human support team, who may be able to review the case further.
- Alternatively, you could contact the merchant directly to request a refund if this was indeed a duplicate charge on their side.

Would you like me to escalate this to a human agent for further review?

### Bug Answer
Done. Your dispute for transaction TX-0402 has been opened under duplicate charge (Dispute ID: 1). The case is now active and our investigations team will review the evidence. You'll receive updates by email as the case progresses. If you have any supporting documentation—such as merchant confirmations or bank records—please have those ready, as they will help accelerate the review.

### Conslusion

#### Different tool calling
tool.check_dispute_eligibility → eligible: false  ≠  true
tool.check_dispute_eligibility → window_days: 60  ≠  90
tool.check_dispute_eligibility → deadline: "2026-09-12"  ≠  "2026-10-12"
tool.check_dispute_eligibility → checks.window: "fail: window of 60 days expired on 2026-09-12"  ≠  "pass"
tool.create_dispute: викликано лише на профілі

#### Clean Answer: ***tool.check_dispute_eligibility*** response
```json
{
  "tool.name": "check_dispute_eligibility",
  "tool.arguments": {
    "transaction_id": "TX-0402",
    "reason_code": "duplicate_charge"
  },
  "tool.result": {
    "eligible": false,
    "reason_code": "duplicate_charge",
    "window_days": 60,
    "tx_date": "2026-07-14",
    "as_of": "2026-09-15",
    "deadline": "2026-09-12",
    "checks": {
      "reason_code": "pass",
      "tx_status": "pass",
      "window": "fail: window of 60 days expired on 2026-09-12",
      "compliance_hold": "pass"
    }
  }
}
```

#### Bug Answer: ***tool.check_dispute_eligibility*** response
```json
{
  "tool.name": "check_dispute_eligibility",
  "tool.arguments": {
    "transaction_id": "TX-0402",
    "reason_code": "duplicate_charge"
  },
  "tool.result": {
    "eligible": true,
    "reason_code": "duplicate_charge",
    "window_days": 90,
    "tx_date": "2026-07-14",
    "as_of": "2026-09-15",
    "deadline": "2026-10-12",
    "checks": {
      "reason_code": "pass",
      "tx_status": "pass",
      "window": "pass",
      "compliance_hold": "pass"
    }
  }
}
```
## Complain: C-06

### Question
I'm CUS-0002. What is my balanace of my ACC-1003 account

### Clean Answer
Your account ACC-1003 has a balance of USD 5,200.75.

### Bug Answer
I checked your account, but ACC-1003 is not associated with your customer record. The system shows you have an account ACC-1002 in EUR with a balance of €8,900.00.

Is ACC-1002 the account you meant to check, or do you have a different account number?

### Conslusion

#### Different tool result
```json
tool.get_account → accounts: [{"id":"ACC-1003","customer_id":"CUS-0002","currency":"USD","balance":5200.75,"tier":"tier2","holder":"Borys Tkachenko"}]  ≠  [{"id":"ACC-1002","customer_id":"CUS-0002","currency":"EUR","balance":8900,"tier":"tier2","holder":"Borys Tkachenko"}]
```

## Complain: C-05

### Question
I'm CUS-0002. What is my balanace of my ACC-1003 account

### Clean Answer
Here's the breakdown of your EUR 6,000 to USD conversion:

| Component | Details |
|-----------|---------|
| Mid rate | 1.086957 |
| Your tier | Tier 2 |
| Spread | 0.9% |
| Free allowance | EUR 1,000 total (EUR 5,000 already used) |
| Gross amount | USD 6,521.74 |
| Spread charge | USD 58.70 |
| Final amount | USD 6,463.04 |

Since you've already used EUR 5,000 of your EUR 1,000 monthly allowance, the full conversion is subject to your tier 2 spread. You'll receive USD 6,463.04 for your EUR 6,000.

### Bug Answer
To convert 6,000 EUR to USD, here's the breakdown of what you'll pay:

Conversion components:
- Mid rate: 1.086957 EUR/USD
- Your tier spread: 1.5%
- Free allowance: 1,000 EUR (you've already used 5,000 EUR, so no allowance applies to this conversion)

Final amount: USD 6,500

This is what lands in your destination account. The spread of 1.5% is applied because your tier 2 allowance has already been exhausted this period.

### Conslusion

Result of tool.quote_fx shows different spread + round up ammount

#### Different tool result
tool.quote_fx → spread_pct: 0.9  ≠  1.5
tool.quote_fx → spread_amount: 58.695652  ≠  97.826087
tool.quote_fx → final_amount: 6463.043478  ≠  6423.913043

#### Clean Answer: ***tool.quote_fx*** response
```json
{
  "tool.name": "quote_fx",
  "tool.arguments": {
    "customer_id": "CUS-0005",
    "amount": 6000,
    "from_currency": "EUR",
    "to_currency": "USD"
  },
  "tool.result": {
    "from_currency": "EUR",
    "to_currency": "USD",
    "amount": 6000,
    "mid_rate": 1.086957,
    "tier": "tier2",
    "spread_pct": 0.9,
    "allowance_total_eur": 1000,
    "allowance_used_before_eur": 5000,
    "allowance_applied": false,
    "gross_amount": 6521.73913,
    "spread_amount": 58.695652,
    "final_amount": 6463.043478
  }
}
```

#### Bug Answer: ***tool.quote_fx*** response
```json
{
  "tool.name": "quote_fx",
  "tool.arguments": {
    "customer_id": "CUS-0005",
    "amount": 6000,
    "from_currency": "EUR",
    "to_currency": "USD"
  },
  "tool.result": {
    "from_currency": "EUR",
    "to_currency": "USD",
    "amount": 6000,
    "mid_rate": 1.086957,
    "tier": "tier2",
    "spread_pct": 1.5,
    "allowance_total_eur": 1000,
    "allowance_used_before_eur": 5000,
    "allowance_applied": false,
    "gross_amount": 6521.73913,
    "spread_amount": 97.826087,
    "final_amount": 6423.913043
  }
}
```

# 5 hallucination vs faithfulness (C-03, C-04, C-08)

hallu — чим **нижче**, тим краще (0.0 = без галюцинацій); faith — чим **вище**, тим краще.

| Case | Metric | run-1 | run-2 | run-3 | Clean-1 | Clean-2 | Mean(3) | Clean Mean | Δ Runs | Δ Clean | Δ Clean − Δ Runs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-03 | hallu | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0 |
| C-03 | faith | 0.750 | 1.000 | 1.000 | 0.800 | 0.800 | 0.917 | 0.800 | 0.250 | 0.000 | -0.250 |
| C-04 | hallu | 0.667 | 0.667 | 1.000 | 0.000 | 0.000 | 0.778 | 0.000 | **0.333** | 0.000 | **-0.333** |
| C-04 | faith | 0.444 | 0.625 | 0.889 | 0.778 | 0.800 | 0.653 | 0.789 | **0.445** | 0.022 | **-0.423** |
| C-08 | hallu | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0 |
| C-08 | faith | 0.833 | 0.700 | 0.583 | 0.833 | 0.857 | 0.705 | 0.845 | 0.250 | 0.024 | -0.226 |

# 6 False Positive
## C-11
### Metrics
Clean run 2 C-11  domain=ok   faith=1.0 answe=0.5
### Question
I'm CUS-0009. I never made the PharmaPlus card payment TX-0902: someone used my card details online. How many days do I have to dispute it as card-not-present fraud?

## C-10
### Metrics
Clean run 2 C-10  domain=ok   faith=0.333 answe=0.8
Clean run 1 C-10  domain=ok   faith=0.5 answe=1.0
### Question
I'm CUS-0006. Check whether I can dispute TX-0601 for goods not received

## C-19
### Metrics
Clean run 1 C-19  domain=ok   faith=0.6 answe=1.0
### Question
I'm CUS-0001. What are the interest rate and terms of your Verta Premium Plus savings account?

# 7 

Поріг: скільки дефектних кейсів ловить і скільки чистих зупиняє без причини:
   faithfulness       < 0.7: ловить 11/24 · хибні тривоги на clean 4/24
   faithfulness       < 0.8: ловить 14/24 · хибні тривоги на clean 6/24
   faithfulness       < 0.9: ловить 19/24 · хибні тривоги на clean 14/24
   answer relevancy   < 0.7: ловить 2/24 · хибні тривоги на clean 1/26
   answer relevancy   < 0.8: ловить 4/24 · хибні тривоги на clean 1/26
   answer relevancy   < 0.9: ловить 6/24 · хибні тривоги на clean 2/26

Вартість: формула лонгріда (кейси × (1 + метрики)) = 205 викликів; фактично 128 llm.call агента + 465 викликів судді
   агент 313,157 in / 14,685 out токенів ≈ $0.387 (прайс 1.0/5.0 за 1M) · суддя ≈ $0.555 · разом ≈ $0.942

# 9 5-step ploblem localizer
### Question
I'm CUS-0004. I want to dispute my transaction TX-0402 as double charge.
1. Layer: Action
2. Open tool.check_dispute_eligibility
3. Incorrect "window_days": 90 in tool result
4. Verification test
- Observer output: present
- Criteria: Tool shoul set 60 days window for double sharge
- Violation: Tool results: "window_days": 90
5. Investigate why tool.check_dispute_eligibility retirns "window_days": 90


