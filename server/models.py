from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    
    @validates('name')
    def validate_name(self, key, name_input):
        if not name_input:
            raise ValueError("Name must be present")
        duplicate = db.session.query(Author).filter_by(name = name_input).first()
        if duplicate is not None:
            raise ValueError("Name must be unique")
        return name_input
        
    @validates('phone_number')
    def validate_phone(self, key, phone_input):
        if phone_input and (len(phone_input) != 10 or not phone_input.isdigit()):
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_input
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('content')
    def validate_content(self, key, content_input):
        if len(content_input) < 250:
            raise ValueError("Content must be more than 250 characters")
        return content_input
        
    @validates('summary')
    def validate_summary(self, key, summary_input):
        if len(summary_input) > 250:
            raise ValueError("Summary must be maximum of 250 characters")
        return summary_input
    
    @validates('category')
    def validate_category(self, key, category_input):
        categories = ['Fiction', 'Non-Fiction']
        if category_input not in categories:
            raise ValueError("Category must be Fiction or Non Fiction")
        return category_input
        
    @validates('title')
    def validate_title(self, key, title_input):
        if not title_input:
            raise ValueError("Title must be present")
        
        title_bait = ["Won't Believe", "Secret", "Top", "Guess"]
        
        if not any(phrase in title_input for phrase in title_bait):
            raise ValueError("Title must be grab attention")
        return title_input

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
