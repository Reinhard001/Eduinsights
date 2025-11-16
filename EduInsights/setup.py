#!/usr/bin/env python
"""
Quick setup script for EduInsight
Run this after docker-compose up to initialize the system
"""
import os
import sys


def main():
    print("=" * 50)
    print("EduInsight Setup Script")
    print("=" * 50)
    print()
    
    # Check if we're in Docker or local environment
    in_docker = os.path.exists('/.dockerenv')
    
    if in_docker:
        print("✓ Running inside Docker container")
        manage_py = "python manage.py"
    else:
        print("✓ Running in local environment")
        manage_py = "python backend/manage.py"
    
    print()
    print("Steps this script will perform:")
    print("1. Run database migrations")
    print("2. Create a superuser account")
    print("3. Optionally train the ML model")
    print()
    
    input("Press Enter to continue...")
    
    # Run migrations
    print("\n[1/3] Running database migrations...")
    os.system(f"{manage_py} migrate")
    
    # Create superuser
    print("\n[2/3] Creating superuser account...")
    print("Please enter details for the admin account:")
    os.system(f"{manage_py} createsuperuser")
    
    # Train model
    print("\n[3/3] Training ML model...")
    train = input("Do you want to train the ML model now? (y/n): ").lower()
    
    if train == 'y':
        csv_path = input("Enter path to CSV file (or press Enter for sample data): ").strip()
        if not csv_path:
            csv_path = "backend/students_sample.csv" if not in_docker else "students_sample.csv"
        
        train_script = "backend/ml/train_model.py" if not in_docker else "ml/train_model.py"
        os.system(f"python {train_script} --csv {csv_path}")
    else:
        print("Skipping model training. You can train later with:")
        print(f"  python backend/ml/train_model.py --csv your_data.csv")
    
    print()
    print("=" * 50)
    print("✓ Setup Complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Access the application at: http://localhost:8000")
    print("2. Login to admin panel: http://localhost:8000/admin")
    print("3. Add students and performance records")
    print("4. Test predictions: GET /api/students/{id}/predict/")
    print()
    print("For more information, see README.md")
    print()


if __name__ == "__main__":
    main()
