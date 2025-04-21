import os
import requests
from dotenv import load_dotenv
from journal_models import engine, JournalEntry
from sqlalchemy.orm import sessionmaker

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

Session = sessionmaker(bind=engine)
session = Session()

entry = session.query(JournalEntry).order_by(JournalEntry.id.desc()).first()


text = f"""
emotional score of the day: {entry.emotional_temp}
the reason of the emotional state : {entry.emotional_reason}
the goal im trying to achive: {entry.trc_goal}
my game plan for achieving the goal: {entry.trc_plan}
something that i should always remind my self in the trading session: {entry.aphorisms}
what's happening in the market: {entry.macro_context}
the ideas that i have for the day ahead of high probability setups and what strategies i'll gonna use: {entry.trade_plan}
notes of the trades i took it's detailed and i documented every thing that's possible: {entry.execution_notes}
did i hesitate in my trading: {entry.hesitation}
if i hesitated where was it and what was the reason: {entry.hesitation_reason}
how well did i manage my trades from 0-10: {entry.management_rating}
if the score is super low or super high what would be the reason: {entry.management_reason}
did i stayed with my winners: {entry.stayed_with_winner}
was the sizing right: {entry.sizing_ok}
was it a conviction trade: {entry.conviction_trade}
if yes why: {entry.conviction_trade_reason}
was sized based on the level of conviction: {entry.conviction_sized}
did i broke any rules: {entry.broke_rules}
if yes why did i broke the rule: {entry.rules_explanation}
did i logged in my trades: {entry.logged_in_stats}
did i move closer to my goal: {entry.trc_progress}
why and why not did i get closer or move fruther from my goals: {entry.why_trc_progress}
What did i learn/improve today both about my self and the market:{entry.learnings}
What Isn’t Working : {entry.what_isnt_working}
What will i eliminate starting now: {entry.elimination_plan}
What changes can be made in order to achieve my goal: {entry.change_plan}
For the changes I need to make starting today, what are the solutions I can find: {entry.solution_brainstorm}
What adjustments will i make for tomorrow: {entry.adjustment_for_tomorrow}
What was the Easy Trade of the Day: {entry.easy_trade}
list of actions to improve forward : {entry.actions_to_improve_forwar}
Top 3 mistakes of today: {entry.top_3_mistakes_today}
Top 3 things done well today: {entry.top_3_things_done_well}
If i had to teach one takeaway from todays trades to a junior trader what would it be: {entry.one_takeaway_teaching}
What was the best and the worst trade today: {entry.best_and_worst_trades}
What recurring mistake am I still making, and what’s the real root cause: {entry.recurring_mistake}
If today repeated 10 more times, what would I change to maximize edge: {entry.todays_repetition}
the outcome of todays trading its the pnl with all the trades taken: {entry.pnl_of_the_day}
"""

#ino dg koneshoo nadaram kose nanash badan ye prompt e kiri khafan mizanam roosh
prompt = f"""
You're a trading performance coach. Analyze this journal entry and give:
1. Strengths
2. Weaknesses
3. Suggestions
4. Emotional patterns

Entry:
{text}
"""

headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "https://yourprojectname.com",  # Optional but good practice
    "X-Title": "Trading Journal Insight",
    "Content-Type": "application/json"
}

data = {
    "model": "openai/gpt-3.5-turbo",  # or "anthropic/claude-3-haiku", etc.
    "messages": [
        {"role": "system", "content": "You are a trading coach analyzing journal entries."},
        {"role": "user", "content": prompt}
    ]
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

if response.status_code == 200:
    insight = response.json()["choices"][0]["message"]["content"]
    entry.ai_insight = insight
    session.commit()
    print(" OpenRouter insight saved:\n")
    print(insight)
else:
    print(" Error:", response.status_code, response.text)
