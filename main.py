import json
import os
from nutrients import NutritionalAnalyzer

def main():
    print("Welcome to the Nutrient Calculator!")
    analyzer = NutritionalAnalyzer()
    
    while True:
        print("\nOptions:")
        print("1. Add a meal")
        print("2. View daily summary")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            food = input("Enter food name: ")
            try:
                calories = float(input("Enter calories (kcal): "))
                protein = float(input("Enter protein (g): "))
                carbs = float(input("Enter carbs (g): "))
                fat = float(input("Enter fat (g): "))
                analyzer.add_meal(food, calories, protein, carbs, fat)
                print(f"Added {food} successfully!")
            except ValueError:
                print("Invalid input. Please enter numerical values for nutrients.")
        
        elif choice == '2':
            summary = analyzer.get_daily_summary()
            print("\n--- Daily Summary ---")
            print(f"Total Calories: {summary['calories']} kcal")
            print(f"Total Protein: {summary['protein']} g")
            print(f"Total Carbs: {summary['carbs']} g")
            print(f"Total Fat: {summary['fat']} g")
            print("---------------------")
            
        elif choice == '3':
            print("Exiting. Have a healthy day!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
