from flask import Flask
from config import Config
from extensions import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from routes import main
    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    
    # Create tables and seed data ONLY when running the main app
    with app.app_context():
        db.create_all()
        
        from models import Category
        if Category.query.count() == 0:
            seed_categories = [
                Category(name='Food', color_hex='#F97316', icon_name='ti-tools-kitchen-2'),
                Category(name='Transport', color_hex='#3B82F6', icon_name='ti-car'),
                Category(name='Shopping', color_hex='#8B5CF6', icon_name='ti-shopping-bag'),
                Category(name='Bills', color_hex='#EF4444', icon_name='ti-receipt'),
                Category(name='Entertainment', color_hex='#EC4899', icon_name='ti-confetti'),
                Category(name='Other', color_hex='#6B7280', icon_name='ti-dots')
            ]
            db.session.bulk_save_objects(seed_categories)
            db.session.commit()
            print("Successfully seeded system categories.")
            
        print(f"Connected to database: {app.config['SQLALCHEMY_DATABASE_URI']}")

    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
