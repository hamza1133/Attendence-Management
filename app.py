import datetime 
 import uuid 
  
 from flask import Flask, request, jsonify 
 from flask_sqlalchemy import SQLAlchemy 
  
 from sqlalchemy.dialects.postgresql import UUID 
  
 app = Flask(__name__) 
 DB_NAME = "" 
 DB_USERNAME = "" 
 DB_PASSWORD = "" 
 app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}' 
 db = SQLAlchemy(app) 
  
  
 class Student(db.Model): 
     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
     roll_number = db.Column(db.String(255), unique=True, nullable=False) 
     course = db.Column(db.String(255), nullable=False) 
     professor = db.Column(db.String(255), nullable=False) 
     class_enter = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now(), nullable=True) 
     class_leave = db.Column(db.DateTime(timezone=True), nullable=True) 
  
  
 with app.app_context(): 
     db.create_all() 
  
  
 @app.route('/student/<student_id>', methods=['GET']) 
 def get_student(student_id): 
     student = Student.query.get(student_id) 
     if student: 
         del student.__dict__['_sa_instance_state'] 
         return jsonify(student.__dict__) 
     else: 
         return "Student not found", 404 
  
  
 @app.route('/student', methods=['GET']) 
 def get_items(): 
     students = [] 
     for student in db.session.query(Student).all(): 
         del student.__dict__['_sa_instance_state'] 
         students.append(student.__dict__) 
     return jsonify(students) 
  
  
 @app.route('/student', methods=['POST']) 
 def create_item(): 
     data = request.get_json() 
     try: 
         db.session.add(Student(**data)) 
         db.session.commit() 
         return "item created", 201 
     except Exception as e: 
         print(e) 
         return "Student creation failed", 400 
  
  
 @app.route('/student/<student_id>', methods=['PUT']) 
 def update_item(student_id): 
     body = request.get_json() 
     try: 
         db.session.query(Student).filter_by(id=student_id).update( 
             dict(title=body['title'], content=body['content'])) 
         db.session.commit() 
         return "Student updated", 200 
     except Exception as e: 
         print(e) 
         return "Student update failed", 400 
  
  
 @app.route('/student/<student_id>', methods=['DELETE']) 
 def delete_item(student_id): 
     try: 
         db.session.query(Student).filter_by(id=student_id).delete() 
         db.session.commit() 
         return "Student deleted", 204 
     except Exception as e: 
         print(e) 
         return "Student deletion failed", 400 
  
  
 if __name__ == '__main__': 
     app.run(debug=True)