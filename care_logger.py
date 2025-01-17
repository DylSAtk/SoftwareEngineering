import streamlit as st
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey, text
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd
import random
import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Set up logging to help us debug database operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
except Exception as e:
    logger.error(f"Error downloading NLTK data: {e}")

# Initialize VADER sentiment analyzer
@st.cache_resource

def get_sentiment_analyzer():
    """Initialize and cache the VADER sentiment analyzer"""
    try:
        return SentimentIntensityAnalyzer()
    except Exception as e:
        logger.error(f"Error initializing sentiment analyzer: {e}")
        return None

def analyse_sentiment(text):
    """
    Returns the score between 1 and -1
    """
    analyzer = get_sentiment_analyzer()
    if not analyzer:
        return 0.0
    
    try:
        # Get the sentiment scores
        scores = analyzer.polarity_scores(text)
        
        # Convert the compound score to match our -1 to 1 scale
        # VADER's compound score is already normalized between -1 and 1
        return scores['compound']
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return 0.0
  

def init_connection():
    """Create a database connection that persists across Streamlit reruns"""
    try:
        # Runs locally
        engine = create_engine('sqlite:///database.db') 
        # Test the connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return engine
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        st.error("Failed to connect to database")
        return None

def initialize_metadata():
    """Initialize database schema if it doesn't exist"""
    engine = init_connection()
    if not engine:
        return None, None, None, None

    metadata = MetaData()

    # Define tables
    residents = Table(
        'residents', metadata,
        Column('id', Integer, primary_key=True),
        Column('first_name', String),
        Column('last_name', String),
        Column('room_num', Integer)
    )

    care_notes = Table(
        'care_notes', metadata,
        Column('id', Integer, primary_key=True),
        Column('resident_id', Integer, ForeignKey('residents.id')),
        Column('note_text', String),
        Column('staff_name', String),
        Column('sentiment_score', Float),
        Column('timestamp', DateTime)
    )

    try:
        metadata.create_all(engine)
        logger.info("Database schema created successfully")
        return engine, metadata, residents, care_notes
    except Exception as e:
        logger.error(f"Error creating database schema: {e}")
        st.error("Failed to create database schema")
        return None, None, None, None


def generate_care_note():
    """Generate a sample care note with sentiment"""
    positive_notes = [
        "Had a great appetite at breakfast and enjoyed socializing",
        "Participated enthusiastically in morning exercise class",
        "Spent time in the garden and appeared very cheerful",
        "Welcomed family visitors and had an engaging conversation"
    ]

    neutral_notes = [
        "Regular morning routine completed as usual",
        "Attended lunch in dining room",
        "Rested during afternoon quiet time",
        "Watched television in common area"
    ]

    negative_notes = [
        "Seemed less interested in breakfast than usual",
        "Appeared somewhat withdrawn during group activities",
        "Reported feeling tired during the afternoon",
        "Required extra encouragement to participate in activities"
    ]
    
    note_type = random.choices(['positive', 'neutral', 'negative'], weights=[0.5, 0.3, 0.2])[0]
    
    # Skew the fake results so around half are positive, around 30% are neutral and 20% are negative

    if note_type == 'positive':
        note = random.choice(positive_notes)
        sentiment = random.uniform(0.5, 1.0)
    elif note_type == 'negative':
        note = random.choice(negative_notes)
        sentiment = random.uniform(-1.0, -0.2)
    else:
        note = random.choice(neutral_notes)
        sentiment = random.uniform(-0.2, 0.5)
        
    return note, sentiment

def populate_sample_data():
    """Populate the database with sample data if it's empty"""
    engine = init_connection()
    if not engine:
        return

    faker = Faker()
    
    try:
        with engine.connect() as connection:
            # Check if we already have residents
            result = connection.execute(text("SELECT COUNT(*) FROM residents")).scalar()
            
            if result == 0:
                # Start a transaction for sample data
                with connection.begin():
                    # Add sample residents
                    for _ in range(10):
                        connection.execute(
                            text("INSERT INTO residents (first_name, last_name, room_num) VALUES (:first, :last, :room)"),
                            {
                                "first": faker.first_name(),
                                "last": faker.last_name(),
                                "room": random.randint(100, 999)
                            }
                        )
                    
                    # Get all resident IDs
                    resident_ids = [row[0] for row in connection.execute(text("SELECT id FROM residents"))]
                    
                    # Add sample care notes
                    for resident_id in resident_ids:
                        for _ in range(5):
                            note_text, sentiment = generate_care_note()
                            connection.execute(
                                text("""
                                    INSERT INTO care_notes 
                                    (resident_id, note_text, staff_name, sentiment_score, timestamp)
                                    VALUES (:id, :note, :staff, :sentiment, :timestamp)
                                """),
                                {
                                    "id": resident_id,
                                    "note": note_text,
                                    "staff": faker.name(),
                                    "sentiment": sentiment,
                                    "timestamp": datetime.now() - timedelta(days=random.randint(0, 30))
                                }
                            )
                logger.info("Sample data populated successfully")
    except Exception as e:
        logger.error(f"Error populating sample data: {e}")
        st.error("Failed to populate sample data")


def add_resident(first_name, last_name, room_num):
    """Add a new resident to the database"""
    engine = init_connection()
    if not engine:
        return False

    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text("INSERT INTO residents (first_name, last_name, room_num) VALUES (:first, :last, :room)"),
                    {"first": first_name, "last": last_name, "room": room_num}
                )
        logger.info(f"Added resident: {first_name} {last_name}")
        return True
    except Exception as e:
        logger.error(f"Error adding resident: {e}")
        return False


def add_care_note(resident_id, note_text, staff_name):
    """
    Add a new care note to the database with automatically calculated sentiment score
    """
    engine = init_connection()
    if not engine:
        return False

    try:
        # Calculate sentiment score automatically
        sentiment_score = analyse_sentiment(note_text)
        
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text("""
                        INSERT INTO care_notes 
                        (resident_id, note_text, staff_name, sentiment_score, timestamp)
                        VALUES (:id, :note, :staff, :sentiment, :timestamp)
                    """),
                    {
                        "id": resident_id,
                        "note": note_text,
                        "staff": staff_name,
                        "sentiment": sentiment_score,
                        "timestamp": datetime.now()
                    }
                )
        logger.info(f"Added care note for resident {resident_id} with sentiment score {sentiment_score}")
        return True, sentiment_score
    except Exception as e:
        logger.error(f"Error adding care note: {e}")
        return False, None


def get_care_notes(resident_id):
    """Fetch care notes for a specific resident with formatted sentiment descriptions"""
    engine = init_connection()
    if not engine:
        return pd.DataFrame()

    try:
        with engine.connect() as conn:
            df = pd.read_sql(
                """
                SELECT 
                    id,
                    resident_id,
                    note_text,
                    staff_name,
                    sentiment_score,
                    timestamp
                FROM care_notes 
                WHERE resident_id = :id 
                ORDER BY timestamp DESC
                """,
                conn,
                params={"id": resident_id}
            )
            
            # Add a human-readable sentiment description
            def get_sentiment_description(score):
                if score >= 0.5:
                    return "Very Positive"
                elif score >= 0.1:
                    return "Positive"
                elif score <= -0.5:
                    return "Very Negative"
                elif score <= -0.1:
                    return "Negative"
                else:
                    return "Neutral"
            
            df['sentiment_description'] = df['sentiment_score'].apply(get_sentiment_description)
            return df
            
    except Exception as e:
        logger.error(f"Error fetching care notes: {e}")
        return pd.DataFrame()


def get_residents():
    """Fetch all residents from the database"""
    engine = init_connection()
    if not engine:
        return pd.DataFrame()

    try:
        with engine.connect() as conn:
            return pd.read_sql("SELECT * FROM residents", conn)
    except Exception as e:
        logger.error(f"Error fetching residents: {e}")
        return pd.DataFrame()


def main():
    st.title("Resident Management System")
    
    # Initialize database and populate with sample data
    engine, metadata, residents, care_notes = initialize_metadata()
    if engine is None:
        st.error("Failed to initialize database. Please check the logs.")
        return

    populate_sample_data()

    # Set up the UI tabs for:
    #  Adding a resident
    #  Viewing a resident
    #  Adding a care note
    #  Viewing the care notes of a resident

    tab1, tab2, tab3, tab4 = st.tabs([
        "Add Resident", 
        "View Residents", 
        "Add Care Note", 
        "View Care Notes"
    ])

    with tab1:
        # Basic UI Input
        st.header("Add Resident")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        room_num = st.number_input("Room Number", min_value=1, step=1)

        if st.button("Add Resident"):
            if first_name and last_name:  # Basic validation
                if add_resident(first_name, last_name, room_num):
                    st.success(f"Resident {first_name} {last_name} added successfully!")
                    # Clear the form using session state
                    st.session_state.first_name = ""
                    st.session_state.last_name = ""
                    st.session_state.room_num = 1
                else:
                    st.error("Failed to add resident. Please try again.")
            else:
                st.warning("Please fill in both first and last name.")

    with tab2:
        st.header("View Residents")
        if st.button("Refresh Residents"):
            st.session_state.residents = get_residents()
        
        # Edge case testing - if DB is empty
        
        residents_df = get_residents()
        if not residents_df.empty:
            st.dataframe(residents_df)
        else:
            st.info("No residents found in the database.")

    with tab3:
        st.header("Add Care Note")
        resident_id = st.number_input("Resident ID", min_value=1, step=1)
        note_text = st.text_area("Care Note")
        staff_name = st.text_input("Staff Name")

        if st.button("Add Care Note"):
            if note_text and staff_name:  # Basic validation
                success, sentiment_score = add_care_note(resident_id, note_text, staff_name)
                if success:
                    st.success("Care note added successfully!")
                    st.info(f"Calculated sentiment score: {sentiment_score:.2f}")
                    
                    # Show sentiment interpretation
                    if sentiment_score >= 0.5:
                        st.success("This note has a very positive tone")
                    elif sentiment_score >= 0.1:
                        st.success("This note has a positive tone")
                    elif sentiment_score <= -0.5:
                        st.error("This note has a very negative tone")
                    elif sentiment_score <= -0.1:
                        st.warning("This note has a negative tone")
                    else:
                        st.info("This note has a neutral tone")
                    
                    # Clear the form
                    st.session_state.note_text = ""
                    st.session_state.staff_name = ""
                else:
                    st.error("Failed to add care note. Please try again.")
            else:
                st.warning("Please fill in both note text and staff name.")

    with tab4:
        st.header("View Care Notes")
        resident_id = st.number_input("Enter Resident ID to View Notes", min_value=1, step=1)
        if st.button("View Notes"):
            notes_df = get_care_notes(resident_id)
            if not notes_df.empty:
                # Display a summary of sentiment distributions
                total_notes = len(notes_df)
                positive_notes = len(notes_df[notes_df['sentiment_score'] >= 0.1])
                negative_notes = len(notes_df[notes_df['sentiment_score'] <= -0.1])
                neutral_notes = total_notes - positive_notes - negative_notes
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Positive Notes", f"{positive_notes} ({positive_notes/total_notes*100:.0f}%)")
                with col2:
                    st.metric("Neutral Notes", f"{neutral_notes} ({neutral_notes/total_notes*100:.0f}%)")
                with col3:
                    st.metric("Negative Notes", f"{negative_notes} ({negative_notes/total_notes*100:.0f}%)")
                
                st.dataframe(notes_df)
            else:
                st.info(f"No care notes found for resident ID {resident_id}")
if __name__ == "__main__":
    main()
