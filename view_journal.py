import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from journal_models import JournalEntry, JournalImage
import os
import re
# --- Database setup
engine = create_engine("sqlite:///trading_journal.db")
Session = sessionmaker(bind=engine)
session = Session()

st.set_page_config(layout="wide")
st.title("📖 My Trading Journal (Read-Only Viewer)")

entries = session.query(JournalEntry).order_by(JournalEntry.date.desc()).all()

def render_notes_with_images(note_text):
    # Replace ![[filename.png]] with inline image rendering
    def replacer(match):
        filename = match.group(1)
        filepath = f"images/{filename}"
        if os.path.exists(filepath):
            st.image(filepath, use_column_width=True)
        else:
            st.warning(f"⚠️ Image not found: {filename}")
        return ""  # remove the ![[...]] from the markdown output

    pattern = re.compile(r"!\[\[(.*?)\]\]")

    # Render all images and collect remaining text
    remaining_text = pattern.sub(replacer, note_text)

    # Now render the remaining markdown text (not the image markdown)
    st.markdown(remaining_text)

for entry in entries:
    with st.expander(f"📅 {entry.date.strftime('%Y-%m-%d')} — Goal: {entry.trc_goal[:50] if entry.trc_goal else 'No goal'}"):
        st.markdown("### 🧠 Pre-Market Prep")
        st.markdown(f"- **Emotional Temp:** {entry.emotional_temp}")
        st.markdown(f"- **Reason:** {entry.emotional_reason}")
        st.markdown(f"- **TRC Goal:** {entry.trc_goal}")
        st.markdown(f"- **Plan to Achieve:** {entry.trc_plan}")
        st.markdown(f"- **Aphorisms:** {entry.aphorisms}")
        st.markdown(f"- **Macro Context:** {entry.macro_context}")
        st.markdown(f"- **Trade Plan:**\n```\n{entry.trade_plan}\n```")

        st.markdown("### ⚔ During Market")
        st.markdown("**Execution Notes:**")
        render_notes_with_images(entry.execution_notes)
        st.markdown(f"- **Hesitation:** {'✅' if entry.hesitation else '❌'}")
        st.markdown(f"- **The reason of hesitation:** {entry.hesitation_reason}")
        st.markdown(f"- **Management Rating:** {entry.management_rating}/5")
        st.markdown(f"- **Management Reason:** {entry.management_reason}")
        st.markdown(f"- **Stayed with Winner:** {'✅' if entry.stayed_with_winner else '❌'}")
        st.markdown(f"- **Sizing OK:** {'✅' if entry.sizing_ok else '❌'}")
        st.markdown(f"- **Conviction Trade:** {'✅' if entry.conviction_trade else '❌'}")
        st.markdown(f"- **The reason of conviction:** {entry.conviction_trade_reason}")
        st.markdown(f"- **Conviction Sized:** {'✅' if entry.conviction_sized else '❌'}")


        st.markdown("### 🧾 Post-Market Review")
        st.markdown(f"- **Stats Logged:** {'✅' if entry.logged_in_stats else '❌'}")
        st.markdown(f"- **Broke Rules:** {'✅' if entry.broke_rules else '❌'}")
        st.markdown(f"- **Rule Explanation:** {entry.rules_explanation}")
        st.markdown(f"- **Progress Toward TRC:** {'✅' if entry.trc_progress else '❌'}")
        st.markdown(f"- **Why/Why Not:** {entry.why_trc_progress}")
        st.markdown(f"- **Learnings:** {entry.learnings}")
        st.markdown(f"- **What Isn’t Working:** {entry.what_isnt_working}")
        st.markdown(f"- **Elimination Plan:** {entry.elimination_plan}")
        st.markdown(f"- **Change Plan:** {entry.change_plan}")
        st.markdown(f"- **Brainstormed Solutions:** {entry.solution_brainstorm}")
        st.markdown(f"- **Adjustment for Tomorrow:** {entry.adjustment_for_tomorrow}")
        st.markdown(f"- **Easy Trade:** {entry.easy_trade}")

        st.markdown("### ♞ Strategic adjustments")
        st.markdown(f"- **actions to improve forward:**\n```\n{entry.actions_to_improve_forward}\n```")
        st.markdown(f"- **top 3 mistakes today:**\n```\n{entry.top_3_mistakes_today}\n```")
        st.markdown(f"- **top 3 things done well:**\n```\n{entry.top_3_things_done_well}\n```")
        st.markdown(f"- **one takeaway to teach:**\n```\n{entry.one_takeaway_teaching}\n```")
        st.markdown(f"- **best and worst trades:**\n```\n{entry.best_and_worst_trades}\n```")
        st.markdown(f"- **recurring mistake:**\n```\n{entry.recurring_mistake}\n```")
        st.markdown(f"- **todays repetition:**\n```\n{entry.todays_repetition}\n```")

        st.markdown("### 📈 P&L Of The Day")
        st.markdown(f"- **P&L all trades today** {entry.pnl_of_the_day} ")


        st.markdown("### 🧠 AI Insight")
        st.markdown(f"```{entry.ai_insight}```" if entry.ai_insight else "_No AI insight available._")

        st.markdown("### 📸 Attached Charts")
        if entry.images:
            for img in sorted(entry.images, key=lambda x: x.position or 0):
                if os.path.exists(img.image_path):
                    st.markdown(f"**{img.caption or 'No caption'}** ({img.section})")
                    st.image(img.image_path, use_column_width=True)
                else:
                    st.warning(f"Image not found: {img.image_path}")
        else:
            st.markdown("_No images for this entry._")
