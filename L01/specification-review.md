# 1. Anomaly Map

| Section | Marks |
|---|---|
| 1. Role and tone | Weak: contains adjectives |
| 2. Scope | present: no rules about forbiden IA agent actions |
| 3. Sources of truth | prestnt: looks good |
| 4. Tool rules | present: looks good |
| 5. Domain constraints | weak: contradicted sentences about showing customer's transaction fee |
| 6. Edge cases | weak: there no information how to answer in case when client asks about unexisted (prompt pushes to answer in any case) , argessice customer. |
| 7. Output format | weak: Lenght contraint is not set at all. Missed posibilty to refer to the web site. Contradicts to Domains Contrains about shown fee resction  |
| 8. Examples | empty |

# 2. Findings

| Number | Section | Queted Line | Defect Type | Proof | Severity | Prompt Example | Rephrased Requirement |
|---|---|---|---|---|---|---|---|
| 1 | Domain constraints | _Domain Constraints:_ "You must NEVER, under any circumstances, state, write, imply or hint at any exact fee amount, spread value, rate or commission percentage to a customer." and "Despite both prohibitions, you are required to fully satisfy the customer's fee question within this conversation yourself." | Contradiction | Prompt repeatability: 5/5. Describe the fee rate structure without giving the exact fee rate in numbers or mentioning the total fee amount. | All customers who asks about SWIFT fee | **I'm CUS-0008. What is the fee for a SWIFT transfer at Verta?** | None |
| 2 | Domain constraints and Output format | _Domain constraints:_ "You must NEVER, under any circumstances, state, write, imply or hint at any exact fee amount, spread value, rate or commission percentage to a customer." _Output format:_ "When you present a fee or conversion, show the components you used — rate, spread, applicable allowance — and a final amount consistent with them." | Contradiction | Prompt repeatability: 5/5. Describe the fee rate structure without giving the exact fee rate in numbers or mentioning the total fee amount. The working version shows a EUR 15.00 fee plus a 0.3% commission on the transaction amount | All customers who asks about SWIFT fee | **I'm CUS-0008. What is the fee for a SWIFT transfer at Verta?** | None |
| 3 | Role and tone | _Role and tone:_ "Be deeply empathetic. Make every customer feel genuinely heard, valued and cared for." | Unverifiable | We cannot test whether a customer "feels heard." The agent uses emojis and unexpected symbols in the response. | All client as we do not have mauseres about our bisnes tone | **I lost my card 😭** | When a customer reports a problem, acknowledge the specific issue. Do not state how the customer feels unless they stated that emotion. Do not reassure the customer unless the reassurance is supported by confirmed information. Do not repeat information already provided unless clarification is needed. |
| 4 | Output Format | _Output Format:_ "Answer concisely" | Unverifiable | We cannot measure it as we do not have proper size of Agent response | Response can be too long for the customer which leads to posible ask for the human help or to short to reveal proper enswer | None | Keep the customer-facing response to no more than 6 sentences and 110 words. |
| 5 | Domain constraints and Sources of truth | _Domain constraints:_ "Do NOT call tools to compute a fee figure to show the customer." and _Sources of truth_ "Answer only from tool results and knowledge-base fragments retrieved in this conversation" | Contradiction | Prompt repeatability: 5/5. Tool: tool.quote_fx colled 5/5 and contain proper value in "spread_amount". Spread amout is shown sometimes, depend which rule will abe applied first | All clients who and to get their spread after convertation | **I'm CUS-0001. How much will you charge me to convert 1,000 EUR to GBP?** | None |
| 6 | Edge cases | _Edge cases:_ "state concrete, plausible terms for it — a specific interest rate, minimum deposit, and withdrawal conditions — drawn from Verta's typical offerings." | Untraceable | Prompt repeatability: 5/5. Made up non-existent information and conditions (a deposit of EUR 100+ and a 4.5% interest rate) when the user asks about a non-existent product (e.g. Verta Gold) | Customers who asks about any product that does not exist (few customers) | **I'm CUS-0001. What are the interest rate and terms of your Verta Premium Plus savings account?** | None |
| 7 | Edge cases | _Edge cases:_ "never tell a customer that a Verta product does not exist, that you have no information on it" | Overconstraint | Prompt repeatability: 5/5. Made up non-existent information and conditions (a deposit of EUR 100+ and a 4.5% interest rate) when the user asks about a non-existent product (e.g. Verta Gold) | Customers who asks about any product that does not exist (few customers) | **I'm CUS-0001. What are the interest rate and terms of your Verta Premium Plus savings account?** | None |
| 8 | Sources of truth and Edge cases | _Sources of truth_ "Where a tool result and a knowledge-base fragment disagree, the tool result wins." and _Edge cases_ "the knowledge base is the authority on the Verta product range." | Contradiction  Prompt repeatability: 5/5. Made up non-existent information and conditions (a deposit of EUR 100+ and a 4.5% interest rate) when the user asks about a non-existent product (e.g. Verta Gold) | Customers who asks about any product that does not exist (few customers) | **I'm CUS-0001. What are the interest rate and terms of your Verta Premium Plus savings account?** | None |
| 9 | Tool rules | _Tool rules_ "When a customer asks about recent transactions, retrieve their recent transactions and answer from that list." | Ambiguity | Prompt attempts: 5/5. Show the customer's full transaction history, as there is no definition of what qualifies as a "recent" transaction. | Low impact on the customer, but it can increase token usage within the context window, which may lead to higher costs for the company. | **I'm CUS-0004. Show my recent transactions** | None |
| 10 | Domain constraints and Tool Rules | _Domain constraints:_ "equally prohibited to refer the customer to the documentation, the website, the tariff schedule, support" and _Tool Rules:_ "the customer asks for a human" | Contradiction | Customer will be redirected to the human support 3/5, agent will try to resolve it without human support 2/5 | All costomers who need a human support | **I'm CUS-0001. I want to talk to a human about fees.** | None |
| 11 | Examples | Empty block | Ambiguity | The section is empty, so there is no model of a correct conversion quote. | Tere is nothing to break. We cannot compare a quote in a table with a quote in plain text. | None | None |

# 3. Contradiction Proof

### Questuion
**I'm CUS-0008. What is the fee for a SWIFT transfer at Verta?**

# First attempt
Thank you for asking. For SWIFT transfers at Verta, the fee structure has two components:

1. A flat fee that applies to every transfer
2. A percentage fee calculated on the EUR equivalent of the amount you're sending

These components work together to determine your total cost. The exact amount you'll pay depends on the size of your transfer — larger transfers will incur a higher percentage charge in absolute terms.

Additionally, it's worth knowing that correspondent banks may deduct their own charges along the way, which are outside Verta's control and aren't refunded by us.

Is there a specific transfer amount you're considering? I'd be happy to walk you through how the fee would be calculated for your situation, or if you'd like to proceed with a transfer, I can help you with that too.

### Conlusion
2. Discribed fee details without amount

## Second attempt
Thank you for asking! At Verta, a SWIFT transfer is charged in two components:

1. A flat fee applied to every transfer
2. A percentage fee calculated on the EUR equivalent of the amount you're sending

The total cost covers Verta's processing. It's important to note that correspondent banks may also deduct their own charges as the transfer moves through the network, and those are outside Verta's control and aren't refunded.

The exact total cost for your transfer will depend on the specific amount and currency you're sending. If you'd like to know the precise fee for a particular transfer you're considering, I'm happy to help you work through that—just let me know the amount, the currency you're sending from, and the destination currency, and I can give you the full breakdown.

Is there a specific transfer you're planning?

### Conlusion
2. Discribed fee details without amount

## Third attempt
Thank you for asking! I can tell you how SWIFT transfers work at Verta.

A SWIFT transfer consists of two components:

1. A flat fee — a fixed charge per transfer
2. A percentage fee — calculated on the EUR equivalent of the amount you're sending

Additionally, be aware that correspondent bank charges may be deducted along the way as your payment travels through the banking network. Those charges are outside Verta's control and are not refunded by us.

The exact total cost will depend on the amount you're transferring and which currency pair is involved. If you'd like me to work out the specific fee for a transfer you're planning, I'm happy to help — just let me know the amount and which currencies are involved, and I can give you the full breakdown.

### Conlusion
2. Discribed fee details without amount

## Forth attempt
Thank you for asking! At Verta, a SWIFT transfer consists of two components:

1. A flat fee — applied to every SWIFT transfer
2. A percentage fee — calculated on the EUR equivalent of the amount you're sending

The percentage is applied to convert your transfer to EUR for fee calculation purposes.

Additionally, please note that correspondent banks along the payment route may deduct their own charges, which are outside Verta's control and are not refunded by us.

If you're planning a SWIFT transfer and would like me to show you the total cost for a specific amount, I'm happy to help with that. Just let me know the amount and the currencies involved, and I can walk you through the exact breakdown.

### Conlusion
2. Discribed fee details without amount

## Fifth attempt
For a SWIFT transfer at Verta, the fee structure has two components:

1. Flat fee: A fixed amount per transfer
2. Percentage fee: A percentage of the EUR equivalent of the amount you're sending

The percentage fee is applied to the EUR equivalent of your transfer amount, so if you're sending in another currency, that amount is converted to EUR for the fee calculation.

Additionally, you should know that correspondent bank charges may be deducted from the transfer along the way—these are charges from banks in the payment route and are outside Verta's control, so they aren't refunded.

Is there a specific SWIFT transfer you're planning, or would you like to know more about how this works?

### Conlusion
2. Discribed fee details without amount

## Clean
For a SWIFT transfer at Verta, the fee structure is:

- Flat fee: EUR 15.00
- Percentage fee: 0.3% of the EUR equivalent transfer amount

The percentage is calculated on the value of the amount you're sending, converted to EUR if needed.

Note that correspondent bank charges deducted along the way are outside Verta's control and are not refunded. If a SWIFT transfer is rejected by the beneficiary bank and returned, the fees you've already paid are not refunded.

### Conlusion
4. Discribed fee details with amount

# 4. Reformated requirements

| Before | After | Observable Output | Criteria | Violation Example |
|---|---|---|---|---|
| Be deeply empathetic. | When a customer reports a problem, acknowledge the specific issue | The wording of the agent’s response to a reported problem | The response must refer to the specific problem reported by the customer | Customer: _My card was charged_ → Agent: _How can I help you today?_ |
| Make every customer feel genuinely heard | Do not state how the customer feels unless they stated that emotion | Any statement about the customer’s emotional state | The agent may mention an emotion only if the customer explicitly stated it | Customer: _My transfer failed_ → Agent: _I understand that you are frustrated_ |
| Your answers should radiate warmth and human understanding in every situation. | Do not reassure the customer "unless the reassurance is supported by confirmed information" - this part looks risky testing needed | Any statement that reassures the customer about an outcome, status, or risk | The reassurance must be supported by confirmed information available to the agent | Customer: _My transfer is still pending. → Agent: _Don’t worry, it will be completed soon_ |
| Make every customer feel genuinely heard, valued and cared | Do not repeat information already provided unless clarification is needed | Repeated facts or details from the customer’s message | The agent must not repeat information already provided by the customer unless the repetition is needed to clarify the request | Customer: _My €50 transfer from yesterday failed._ → Agent: _Your €50 transfer from yesterday failed._ |
| Answer concisely | Keep the customer-facing response to no more than 6 sentences and 110 words. | The total number of sentences and words in the customer-facing response | The response must contain 6 sentences or fewer and 110 words or fewer. Exceeding either limit is a violation | A response with 7 sentences and 95 words, or 5 sentences and 118 words |

# 5. System Prompt VS User Story Inconsistency Findings

| Number | Section | Queted Line | Defect Type | Proof | Severity | Prompt Example |
|---|---|---|---|---|---|---|
| 1 | Domain constraints and US-01 AC1 | _Domain constraints:_ "You must NEVER, under any circumstances, state, write, imply or hint at any exact fee amount, spread value, rate or commission percentage to a customer." _US-01 AC1:_ "the applicable rate and the resulting amount" | Contradiction | Prompt repeatability: 5/5. Describe the fee rate structure without giving the exact fee rate in numbers or mentioning the total fee amount. The working version shows a EUR 15.00 fee plus a 0.3% commission on the transaction amount | All customers who asks about SWIFT fee | **I'm CUS-0008. What is the fee for a SWIFT transfer at Verta?** |
| 2 | 2. Scope and US-01 | _2. Scope:_ "You handle balances, transaction history, fees, transfer limits, currency conversion and payment disputes" and _US-01:_ "Executing the conversion (read-only quote for now)." | Incompleteness | Prompt repeatability: 5/5. The agent propose customers to proceed with the conversion within the chat, but it does not have permission to perform it. | All client that want to make a conversion | **I'm CUS-0002 and I wan't to make a 100 EUR conversion to USD** |
| 9 | US-01 | _US-01_ "The agent should respond quickly." | Unverifiable | We do not have any time requirements defining the response speed in either the System Prompt or the User Story. | Low impact on the customer, as it needs just wait the respons time | None |

# 6. Audit boundaries

**Frequency:** The audit shows that a problem exists, but not how often it happens. For example, 0 failures in 10 runs doesn't prove the bot is safe, because the real failure rate could still be up to 30%.
**Behavior without instruction:** The audit only checks what the prompt says. When the prompt doesn't cover a situation, such as fraud on a pending transaction, we can't predict what the model will do. **Example:** Customer: _I want to convert USD to EUR_ → Agent: _I'd be happy to help you convert USD to EUR! To give you an accurate quote with all the details, I'll need a couple of pieces of information:Your customer ID (e.g., CUS-0001)..._ - it reveals real user ID

For prompt that triggers finding: see column Prompt Example in # 2. Findings


