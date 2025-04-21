import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from journal_models import Base, JournalEntry, JournalImage
import datetime
import os
import re

# DB Setup
engine = create_engine("sqlite:///trading_journal.db")
Session = sessionmaker(bind=engine)
session = Session()

st.set_page_config(layout="wide")
st.title("📝 Add New Trading Journal Entry")

# Select date and check for existing entry
date = st.date_input("Journal Date", datetime.date.today())
existing_entry = session.query(JournalEntry).filter(
    JournalEntry.date.between(
        datetime.datetime.combine(date, datetime.time.min),
        datetime.datetime.combine(date, datetime.time.max)
    )
).first()

if existing_entry:
    st.info("📄 Editing existing journal for this date.")
else:
    st.success("🆕 Creating new journal entry.")

# -- Form Start
with st.form("journal_form"):
    st.markdown("## 🧠 Pre-Market Prep")
    #date = st.date_input("Date", datetime.date.today())
    emotional_temp = st.slider("Emotional Temperature (1–10)", 1, 10, existing_entry.emotional_temp if existing_entry else 5)
    emotional_reason = st.text_area("Reason for Emotional State", value=existing_entry.emotional_reason if existing_entry else "")
    trc_goal = st.text_input("TRC Goal", value=existing_entry.trc_goal if existing_entry else "")
    trc_plan = st.text_area("Plan to Achieve TRC Goal", value=existing_entry.trc_plan if existing_entry else "")
    aphorisms = st.text_input("Reminders / Aphorisms to self", value=existing_entry.aphorisms if existing_entry else "")
    macro_context = st.text_area("Macro Context", value=existing_entry.macro_context if existing_entry else "")
    trade_plan = st.text_area("Trading plan for the day(Setup, Triggers, Invalidation, Size plan)", value=existing_entry.trade_plan if existing_entry else "")

    st.markdown("## ⚔ During Market")
    execution_notes = st.text_area("Execution Notes", value=existing_entry.execution_notes if existing_entry else "")
    hesitation = st.checkbox("Did You Hesitate?", value=existing_entry.hesitation if existing_entry else False)
    hesitation_reason = st.text_area("Where and why?", value=existing_entry.hesitation_reason if existing_entry else "")
    management_rating = st.slider("Management Rating", 1, 5, value=existing_entry.management_rating if existing_entry else 3)
    management_reason = st.text_area("Reasons for bad management", value=existing_entry.management_reason if existing_entry else "")
    stayed_with_winner = st.checkbox("Stayed with Winners?", value=existing_entry.stayed_with_winner if existing_entry else False)
    sizing_ok = st.checkbox("Sized Properly?", value=existing_entry.sizing_ok if existing_entry else False)
    conviction_trade = st.checkbox("Was it a Conviction Trade?", value=existing_entry.conviction_trade if existing_entry else False)
    conviction_trade_reason = st.text_area("If it was what was the conviction and if not why did you trade it?", value=existing_entry.conviction_trade_reason if existing_entry else "")
    conviction_sized = st.checkbox("Was Sizing Matched to Conviction?", value=existing_entry.conviction_sized if existing_entry else False)

    st.markdown("## 🧾 Post-Market Review")
    logged_in_stats = st.checkbox("Logged Stats?", value=existing_entry.logged_in_stats if existing_entry else False)
    broke_rules = st.checkbox("Broke Any Rules?", value=existing_entry.broke_rules if existing_entry else False)
    rules_explanation = st.text_area("Rule Explanation", value=existing_entry.rules_explanation if existing_entry else "")
    trc_progress = st.checkbox("Made Progress Toward TRC?", value=existing_entry.trc_progress if existing_entry else False)
    why_trc_progress = st.text_area("Why / Why Not", value=existing_entry.why_trc_progress if existing_entry else "")
    learnings = st.text_area("What did i learn/improve today (market + self)", value=existing_entry.learnings if existing_entry else "")
    what_isnt_working = st.text_area("What Isn’t Working", value=existing_entry.what_isnt_working if existing_entry else "")
    elimination_plan = st.text_area("What will i eliminate starting now?", value=existing_entry.elimination_plan if existing_entry else "")
    change_plan = st.text_area("What changes can be made in order to achieve my goal?", value=existing_entry.change_plan if existing_entry else "")
    solution_brainstorm = st.text_area("For the changes I need to make starting today, what are the solutions I can find?", value=existing_entry.solution_brainstorm if existing_entry else "")
    adjustment_for_tomorrow = st.text_area("What adjustments will i make for tomorrow?", value=existing_entry.adjustment_for_tomorrow if existing_entry else "")
    easy_trade = st.text_area("What was the Easy Trade of the Day", value=existing_entry.easy_trade if existing_entry else "")

    st.markdown("## ♞ Strategic adjustments")
    actions_to_improve_forward = st.text_area("list of actions to improve forward.", value=existing_entry.actions_to_improve_forward if existing_entry else "")
    top_3_mistakes_today = st.text_area("Top 3 mistakes of today.", value=existing_entry.top_3_mistakes_today if existing_entry else "")
    top_3_things_done_well = st.text_area("Top 3 things done well today", value=existing_entry.top_3_things_done_well if existing_entry else "")
    one_takeaway_teaching = st.text_area("If i had to teach one takeaway from todays trades to a junior trader what would it be?", value=existing_entry.one_takeaway_teaching if existing_entry else "")
    best_and_worst_trades = st.text_area("What was the best and the worst trade today?", value=existing_entry.best_and_worst_trades if existing_entry else "")
    recurring_mistake = st.text_area("What recurring mistake am I still making, and what’s the real root cause?", value=existing_entry.recurring_mistake if existing_entry else "")
    todays_repetition = st.text_area("If today repeated 10 more times, what would I change to maximize edge?", value=existing_entry.todays_repetition if existing_entry else "")

    st.markdown("## 📈 P&L Of The Day")
    pnl_of_the_day = st.text_area("P&L of every trade that you took today", value=existing_entry.pnl_of_the_day if existing_entry else "")

    st.markdown("## 📸 Upload Charts (Optional)")
    uploaded_images = st.file_uploader("Upload chart images (use name placeholders like ![[image1.png]])", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    image_captions = st.text_area("Image Captions (1 per line, same order)", height=100)

    submitted = st.form_submit_button("✅ Save Entry")

# -- Save logic
if submitted:
    if existing_entry:
        entry = existing_entry
    else:
        entry = JournalEntry(date=datetime.datetime.combine(date, datetime.time.min))
        session.add(entry)

    # Update or create fields
    entry.emotional_temp = emotional_temp
    entry.emotional_reason = emotional_reason
    entry.trc_goal = trc_goal
    entry.trc_plan = trc_plan
    entry.aphorisms = aphorisms
    entry.macro_context = macro_context
    entry.trade_plan = trade_plan
    entry.execution_notes = execution_notes
    entry.hesitation = hesitation
    entry.hesitation_reason = hesitation_reason
    entry.management_rating = management_rating
    entry.management_reason = management_reason
    entry.stayed_with_winner = stayed_with_winner
    entry.sizing_ok = sizing_ok
    entry.conviction_trade = conviction_trade
    entry.conviction_trade_reason = conviction_trade_reason
    entry.conviction_sized = conviction_sized
    entry.broke_rules = broke_rules
    entry.rules_explanation = rules_explanation
    entry.logged_in_stats = logged_in_stats
    entry.trc_progress = trc_progress
    entry.why_trc_progress = why_trc_progress
    entry.learnings = learnings
    entry.what_isnt_working = what_isnt_working
    entry.elimination_plan = elimination_plan
    entry.change_plan = change_plan
    entry.solution_brainstorm = solution_brainstorm
    entry.adjustment_for_tomorrow = adjustment_for_tomorrow
    entry.easy_trade = easy_trade
    entry.actions_to_improve_forward = actions_to_improve_forward
    entry.top_3_mistakes_today = top_3_mistakes_today
    entry.top_3_things_done_well = top_3_things_done_well
    entry.one_takeaway_teaching = one_takeaway_teaching
    entry.best_and_worst_trades = best_and_worst_trades
    entry.recurring_mistake = recurring_mistake
    entry.todays_repetition = todays_repetition
    entry.pnl_of_the_day = pnl_of_the_day

    # Handle uploaded images
    captions = [cap.strip() for cap in image_captions.strip().split("\n")]
    os.makedirs("images", exist_ok=True)

    # Automatically inject image references for execution_notes section
    inline_image_links = []

    for i, image_file in enumerate(uploaded_images):
        filename = f"{date}_{i}_{image_file.name}"
        image_path = f"images/{filename}"

        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())

        caption = captions[i] if i < len(captions) else ""

        # Save image metadata
        section = "execution_notes"  # You can later expand this per-section
        entry.images.append(JournalImage(
            image_path=image_path,
            caption=caption,
            section=section,
            position=i
        ))

        # Add image markdown for inline display
        if section == "execution_notes":
            inline_image_links.append(f"![[{filename}]]")

    # Inject image markdown at the end of execution_notes field
    if inline_image_links:
        entry.execution_notes += "\n" + "\n".join(inline_image_links)
        
    session.commit()
    st.success("Journal entry saved successfully!")
