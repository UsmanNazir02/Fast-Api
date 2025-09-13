from langchain.tools import tool
from services import (
    students_db, 
    get_next_id, 
    find_student_by_id, 
    validate_gender, 
    is_email_unique
)
import json

@tool
def add_user(name: str, age: int, gender: str, email: str) -> str:
    """Add a new user to the students database"""
    try:
        # Validate gender
        if not validate_gender(gender):
            return "Error: Gender must be 'male', 'female', or 'other'"
        
        # Check email uniqueness
        if not is_email_unique(email):
            return f"Error: Email {email} already exists"
        
        new_student = {
            "id": get_next_id(),
            "name": name,
            "age": age,
            "gender": gender.lower(),
            "email": email
        }
        students_db.append(new_student)
        return f"Added {name} successfully."
    except Exception as e:
        return f"Error adding user: {str(e)}"

@tool
def update_user(id: int, name: str = None, age: int = None, gender: str = None, email: str = None) -> str:
    """Update an existing user's information"""
    try:
        student = find_student_by_id(id)
        if not student:
            return f"User {id} not found."
        
        # Validate gender if provided
        if gender and not validate_gender(gender):
            return "Error: Gender must be 'male', 'female', or 'other'"
        
        # Check email uniqueness if provided
        if email and not is_email_unique(email, exclude_id=id):
            return f"Error: Email {email} already exists"
        
        # Update fields
        if name:
            student["name"] = name
        if age is not None:
            student["age"] = age
        if gender:
            student["gender"] = gender.lower()
        if email:
            student["email"] = email
        
        return f"Updated user {id} successfully."
    except Exception as e:
        return f"Error updating user: {str(e)}"

@tool
def delete_user(id: int) -> str:
    """Delete a user from the database"""
    try:
        student = find_student_by_id(id)
        if not student:
            return f"User {id} not found."
        
        students_db.remove(student)
        return f"Deleted user {id} successfully."
    except Exception as e:
        return f"Error deleting user: {str(e)}"

@tool
def get_user(id: int) -> str:
    """Get a specific user by ID"""
    try:
        student = find_student_by_id(id)
        if not student:
            return f"User {id} not found."
        
        # Return as JSON string
        return json.dumps(student)
    except Exception as e:
        return f"Error getting user: {str(e)}"

@tool
def list_users() -> str:
    """Get all users from the database"""
    try:
        if not students_db:
            return "[]"
        # Return as JSON string
        return json.dumps(students_db)
    except Exception as e:
        return f"Error listing users: {str(e)}"

# Export tools list
agent_tools = [add_user, update_user, delete_user, get_user, list_users]