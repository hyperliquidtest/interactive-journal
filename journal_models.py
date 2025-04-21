from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class JournalEntry(Base):
    __tablename__ = 'journal_entries'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    emotional_temp = Column(Integer)
    emotional_reason = Column(Text)
    trc_goal = Column(Text)
    trc_plan = Column(Text)
    aphorisms = Column(Text)
    macro_context = Column(Text)
    trade_plan = Column(Text)

    execution_notes = Column(Text)
    hesitation = Column(Boolean)
    hesitation_reason = Column(Text)
    management_rating = Column(Integer)
    management_reason = Column(Text)
    stayed_with_winner = Column(Boolean)
    stayed_with_winner_reason = Column(Text)
    sizing_ok = Column(Boolean)
    conviction_trade = Column(Boolean)
    conviction_trade_reason = Column(Text)
    conviction_sized = Column(Boolean)


    logged_in_stats = Column(Boolean)
    broke_rules = Column(Boolean)
    rules_explanation = Column(Text)
    trc_progress = Column(Boolean)
    why_trc_progress = Column(Text)
    learnings = Column(Text)
    what_isnt_working = Column(Text)
    elimination_plan = Column(Text)
    change_plan = Column(Text)
    solution_brainstorm = Column(Text)
    adjustment_for_tomorrow = Column(Text)
    easy_trade = Column(Text)

    actions_to_improve_forward = Column(Text)
    top_3_mistakes_today = Column(Text)
    top_3_things_done_well = Column(Text)
    one_takeaway_teaching = Column(Text)
    best_and_worst_trades =Column(Text)
    recurring_mistake = Column(Text)
    todays_repetition = Column(Text)

    pnl_of_the_day = Column(Text)

    ai_insight = Column(Text)

    images = relationship("JournalImage", back_populates="entry")

class JournalImage(Base):
    __tablename__ = 'journal_images'
    id = Column(Integer, primary_key=True)
    journal_entry_id = Column(Integer, ForeignKey('journal_entries.id'))
    image_path = Column(String)
    caption = Column(Text)
    section = Column(String)
    position = Column(Integer)

    entry = relationship("JournalEntry", back_populates="images")

# Create the database
engine = create_engine('sqlite:///trading_journal.db')
Base.metadata.create_all(engine)
