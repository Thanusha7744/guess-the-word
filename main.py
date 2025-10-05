from app import create_app, db
from app.utils import insert_initial_words

# Create Flask app
app = create_app()

# Insert initial 20 words into DB (only if not already present)
with app.app_context():
    insert_initial_words()

if __name__ == "__main__":
    # Run the app in debug mode
    app.run(debug=True)
