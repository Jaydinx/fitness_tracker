import sqlite3

db = sqlite3.connect('data/fitness_tracker_db')
cursor = db.cursor()

'''This fitness tracker app allows the user to perform multiple operations such
   as adding workout categories, updating workout categories, removing workout
   categories, creating workout goals, goal categories, removing the goal
   category as well as calculating the user's fitness goal progress based on
   the information they have provided'''

while True:

    menu = input('''Please select an option from the menu below by inputting
the number corresponding to your desired option to proceed

1. Add exercise category
2. View exercise by category
3. Delete exercise by category
4. Create Workout Routine
5. View Workout Routine
6. View Exercise Progress
7. Set Fitness Goals
8. View Progress towards Fitness Goals
9. Quit

Please enter your desired option here : ''')

    menu = menu.strip()
    if menu == '1':

        exercise_category = input('''
Please enter your desired exercise category: ''')
        
    elif menu == '2':

        view_exercise_category = input('''
Please enter your desired exercise category: ''')
