Вправа 1. Індексація: той самий запит на цілому і на розрізаному індексі
Search the Verta documentation: what FX spread applies to my account and what is my free monthly conversion allowance?
```json
{
  "tool.name": "search_knowledge_base",
  "tool.arguments": {
    "query": "FX spread and free monthly currency conversion allowance by customer tier"
  },
  "tool.result": {
    "index": "kb_clean",
    "top_k": 4,
    "query": "FX spread and free monthly currency conversion allowance by customer tier",
    "fragments": [
      {
        "id": "tariffs.md#s2",
        "doc": "tariffs.md",
        "score": 2.4962,
        "text": "Verta tariff schedule\n## FX spreads by tier\nThe spread is applied over the mid-market rate only after the free monthly\nconversion allowance is exhausted.\n\n| Tier | FX spread | Free monthly conversion allowance |\n|---|---|---|\n| Tier 1 | 1.5% | EUR 500 |\n| Tier 2 | 0.9% | EUR 1,000 |\n| Tier 3 | 0.5% | EUR 5,000 |"
      },
      {
        "id": "fx-guide.md#s1",
        "doc": "fx-guide.md",
        "score": 2.4254,
        "text": "Currency conversion guide\n## How a conversion is priced\nA conversion quote has these components, in order: the mid-market rate for the\ncurrency pair; the tier spread (a percentage of the gross converted amount);\nthe free monthly conversion allowance. If the whole conversion fits within the\ncustomer's remaining monthly allowance, no spread is charged. Once the\nallowance is exhausted, the full tier spread applies to the conversion."
      },
      {
        "id": "onboarding.md#s2",
        "doc": "onboarding.md",
        "score": 2.0851,
        "text": "Onboarding and tiers\n## Tier benefits\nA higher tier lowers the FX spread, raises the free monthly conversion\nallowance and raises both transfer limits."
      },
      {
        "id": "fx-operations.md#s3",
        "doc": "fx-operations.md",
        "score": 1.8708,
        "text": "Currency conversion operations\n## Allowance accounting\nThe free monthly conversion allowance is counted in EUR equivalent and resets on\nthe first calendar day of each month. Allowance consumption is recorded at\nsettlement. A conversion that would cross the allowance boundary has the tier\nspread applied to the entire conversion, not only to the portion above the\nboundary."
      }
    ]
  },
  "retrieval.query": "FX spread and free monthly currency conversion allowance by customer tier",
  "retrieval.index": "kb_clean",
  "retrieval.top_k": 4,
  "retrieval.fragments": [
    {
      "id": "tariffs.md#s2",
      "score": 2.4962,
      "text": "Verta tariff schedule\n## FX spreads by tier\nThe spread is applied over the mid-market rate only after the free monthly\nconversion allowance is exhausted.\n\n| Tie"
    },
    {
      "id": "fx-guide.md#s1",
      "score": 2.4254,
      "text": "Currency conversion guide\n## How a conversion is priced\nA conversion quote has these components, in order: the mid-market rate for the\ncurrency pair; the tier s"
    },
    {
      "id": "onboarding.md#s2",
      "score": 2.0851,
      "text": "Onboarding and tiers\n## Tier benefits\nA higher tier lowers the FX spread, raises the free monthly conversion\nallowance and raises both transfer limits."
    },
    {
      "id": "fx-operations.md#s3",
      "score": 1.8708,
      "text": "Currency conversion operations\n## Allowance accounting\nThe free monthly conversion allowance is counted in EUR equivalent and resets on\nthe first calendar day o"
    }
  ]
}
```

```json
{
  "tool.name": "search_knowledge_base",
  "tool.arguments": {
    "query": "FX spread and free monthly conversion allowance by customer tier"
  },
  "tool.result": {
    "index": "kb_broken",
    "top_k": 1,
    "query": "FX spread and free monthly conversion allowance by customer tier",
    "fragments": [
      {
        "id": "tariffs.md#b3",
        "doc": "tariffs.md",
        "score": 1.9245,
        "text": "austed. | Tier | FX spread | Free monthly conversion allowance | |---|---|---| | Tier 1 | 1.5% | EUR 500 | | Tier 2 | 0.9% | EUR 1,000 | | Tier 3 | 0.5% | EUR 5"
      }
    ]
  },
  "retrieval.query": "FX spread and free monthly conversion allowance by customer tier",
  "retrieval.index": "kb_broken",
  "retrieval.top_k": 1,
  "retrieval.fragments": [
    {
      "id": "tariffs.md#b3",
      "score": 1.9245,
      "text": "austed. | Tier | FX spread | Free monthly conversion allowance | |---|---|---| | Tier 1 | 1.5% | EUR 500 | | Tier 2 | 0.9% | EUR 1,000 | | Tier 3 | 0.5% | EUR 5"
    }
  ]
}
```


Вправа 2. Видача: чотирьох фрагментів замало
«знайди в документації один раз і скажи і спред, і денний ліміт переказів для Tier 2
Clean top-k 4:
Answer:
Денний ліміт переказів для Tier 2: EUR 20 000. Місячний ліміт для Tier 2 — EUR 200 000.

Спред для Tier 2 у документації не знайдено. Пошук повернув лише ліміти, загальне визначення тарифу та опис того, що вищий тариф знижує спред. Конкретного значення спреду для Tier 2 в ньому немає, тому я його не називаю. Якщо потрібна цифра, можу передати питання живому співробітнику або перевірити конкретну конвертацію через котирування FX для вашого рахунку.

```json
{
  "tool.name": "search_knowledge_base",
  "tool.arguments": {
    "query": "Tier 2 spread FX and daily transfer limit"
  },
  "tool.result": {
    "index": "kb_clean",
    "top_k": 4,
    "query": "Tier 2 spread FX and daily transfer limit",
    "fragments": [
      {
        "id": "limits.md#s1",
        "doc": "limits.md",
        "score": 1.8475,
        "text": "Transfer limits\n## Daily and monthly limits by tier\nOutgoing transfer limits are tracked in EUR equivalent, separately per day and\nper calendar month. The daily and the monthly remainder are different numbers:\nboth are computed from the same settled-transactions source, but over\ndifferent windows.\n\n| Tier | Daily limit | Monthly limit |\n|---|---|---|\n| Tier 1 | EUR 5,000 | EUR 50,000 |\n| Tier 2 | EUR 20,000 | EUR 200,000 |\n| Tier 3 | EUR 100,000 | EUR 1,000,000 |"
      },
      {
        "id": "glossary.md#s6",
        "doc": "glossary.md",
        "score": 1.6681,
        "text": "Glossary\n## Tier\nThe tariff level of a customer: Tier 1, Tier 2 or Tier 3. The tier determines\nspreads, allowances and transfer limits."
      },
      {
        "id": "tariffs.md#s1",
        "doc": "tariffs.md",
        "score": 1.5213,
        "text": "Verta tariff schedule\n## Account tiers\nVerta offers three account tiers: Tier 1, Tier 2 and Tier 3. The tier of\neach account sets its pricing as well as its daily and per-month transfer\nlimits."
      },
      {
        "id": "onboarding.md#s2",
        "doc": "onboarding.md",
        "score": 1.4596,
        "text": "Onboarding and tiers\n## Tier benefits\nA higher tier lowers the FX spread, raises the free monthly conversion\nallowance and raises both transfer limits."
      }
    ]
  },
  "retrieval.query": "Tier 2 spread FX and daily transfer limit",
  "retrieval.index": "kb_clean",
  "retrieval.top_k": 4,
  "retrieval.fragments": [
    {
      "id": "limits.md#s1",
      "score": 1.8475,
      "text": "Transfer limits\n## Daily and monthly limits by tier\nOutgoing transfer limits are tracked in EUR equivalent, separately per day and\nper calendar month. The daily"
    },
    {
      "id": "glossary.md#s6",
      "score": 1.6681,
      "text": "Glossary\n## Tier\nThe tariff level of a customer: Tier 1, Tier 2 or Tier 3. The tier determines\nspreads, allowances and transfer limits."
    },
    {
      "id": "tariffs.md#s1",
      "score": 1.5213,
      "text": "Verta tariff schedule\n## Account tiers\nVerta offers three account tiers: Tier 1, Tier 2 and Tier 3. The tier of\neach account sets its pricing as well as its dai"
    },
    {
      "id": "onboarding.md#s2",
      "score": 1.4596,
      "text": "Onboarding and tiers\n## Tier benefits\nA higher tier lowers the FX spread, raises the free monthly conversion\nallowance and raises both transfer limits."
    }
  ]
}
```


Clean top-k 5:
Answer:
Ось дані з документації Verta для Tier 2 (шукала один раз):

- Спред FX: 0,9% над міді-ринковим курсом. Він застосовується лише після того, як вичерпано безкоштовний місячний ліміт конвертації, який для Tier 2 становить EUR 1 000.
- Денний ліміт переказів: EUR 20 000.

Місячний ліміт переказів для Tier 2 — EUR 200 000. Якщо потрібно перевірити ваш особистий залишок лімітів, можу це зробити.

```json
{
  "tool.name": "search_knowledge_base",
  "tool.arguments": {
    "query": "Tier 2 спред валютна конвертація денний ліміт переказів"
  },
  "tool.result": {
    "index": "kb_clean",
    "top_k": 5,
    "query": "Tier 2 спред валютна конвертація денний ліміт переказів",
    "fragments": [
      {
        "id": "glossary.md#s6",
        "doc": "glossary.md",
        "score": 1.2511,
        "text": "Glossary\n## Tier\nThe tariff level of a customer: Tier 1, Tier 2 or Tier 3. The tier determines\nspreads, allowances and transfer limits."
      },
      {
        "id": "tariffs.md#s1",
        "doc": "tariffs.md",
        "score": 0.8452,
        "text": "Verta tariff schedule\n## Account tiers\nVerta offers three account tiers: Tier 1, Tier 2 and Tier 3. The tier of\neach account sets its pricing as well as its daily and per-month transfer\nlimits."
      },
      {
        "id": "tariffs.md#s2",
        "doc": "tariffs.md",
        "score": 0.8321,
        "text": "Verta tariff schedule\n## FX spreads by tier\nThe spread is applied over the mid-market rate only after the free monthly\nconversion allowance is exhausted.\n\n| Tier | FX spread | Free monthly conversion allowance |\n|---|---|---|\n| Tier 1 | 1.5% | EUR 500 |\n| Tier 2 | 0.9% | EUR 1,000 |\n| Tier 3 | 0.5% | EUR 5,000 |"
      },
      {
        "id": "onboarding.md#s1",
        "doc": "onboarding.md",
        "score": 0.7715,
        "text": "Onboarding and tiers\n## How a customer gets a tier\nNew customers start on Tier 1. Tier 2 is granted when the average monthly\ninflow exceeds EUR 3,000 over three consecutive months. Tier 3 is granted on\napplication and is reviewed annually."
      },
      {
        "id": "limits.md#s1",
        "doc": "limits.md",
        "score": 0.6928,
        "text": "Transfer limits\n## Daily and monthly limits by tier\nOutgoing transfer limits are tracked in EUR equivalent, separately per day and\nper calendar month. The daily and the monthly remainder are different numbers:\nboth are computed from the same settled-transactions source, but over\ndifferent windows.\n\n| Tier | Daily limit | Monthly limit |\n|---|---|---|\n| Tier 1 | EUR 5,000 | EUR 50,000 |\n| Tier 2 | EUR 20,000 | EUR 200,000 |\n| Tier 3 | EUR 100,000 | EUR 1,000,000 |"
      }
    ]
  },
  "retrieval.query": "Tier 2 спред валютна конвертація денний ліміт переказів",
  "retrieval.index": "kb_clean",
  "retrieval.top_k": 5,
  "retrieval.fragments": [
    {
      "id": "glossary.md#s6",
      "score": 1.2511,
      "text": "Glossary\n## Tier\nThe tariff level of a customer: Tier 1, Tier 2 or Tier 3. The tier determines\nspreads, allowances and transfer limits."
    },
    {
      "id": "tariffs.md#s1",
      "score": 0.8452,
      "text": "Verta tariff schedule\n## Account tiers\nVerta offers three account tiers: Tier 1, Tier 2 and Tier 3. The tier of\neach account sets its pricing as well as its dai"
    },
    {
      "id": "tariffs.md#s2",
      "score": 0.8321,
      "text": "Verta tariff schedule\n## FX spreads by tier\nThe spread is applied over the mid-market rate only after the free monthly\nconversion allowance is exhausted.\n\n| Tie"
    },
    {
      "id": "onboarding.md#s1",
      "score": 0.7715,
      "text": "Onboarding and tiers\n## How a customer gets a tier\nNew customers start on Tier 1. Tier 2 is granted when the average monthly\ninflow exceeds EUR 3,000 over three"
    },
    {
      "id": "limits.md#s1",
      "score": 0.6928,
      "text": "Transfer limits\n## Daily and monthly limits by tier\nOutgoing transfer limits are tracked in EUR equivalent, separately per day and\nper calendar month. The daily"
    }
  ]
}
```