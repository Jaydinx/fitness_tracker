import sqlite3

db = sqlite3.connect('data/fitness_tracker_db')
cursor = db.cursor()

'''This fitness tracker app allows the user to perform multiple operations such
   as adding workout categories, updating workout categories, removing workout
   categories, creating workout goals, goal categories, removing the goal
   category as well as calculating the user's fitness goal progress based on
   the information they have provided'''


'''The function display_exercises_by_category ensures that the selected data is
    displayed in a neat and legible format'''


def display_categories():

    cursor.execute('''SELECT * from categories''')
    categories = cursor.fetchall()
    db.commit()

    print('{:<25}'.format('CATEGORY LIST'))
    print('-'*65)

    for row in categories:
        category_name = row[1]
        print('{:<25}'.format(category_name))


def display_exercises_by_category(entry):

    cursor.execute('''SELECT category_id from categories where
                category_name = (?) ''', (entry, ))

    category_id = cursor.fetchone()

    if category_id is None:
        print('CATEGORY NOT FOUND!, PLEASE TRY AGAIN')

    else:
        cursor.execute('''SELECT * from exercises WHERE
                    category_id = (?)''', (category_id[0], ))
        exercises = cursor.fetchall()
        db.commit()

        print("{:<5} {:<25} {:<15} {:<5} {:<5}".format
              ("ID", "Exercise Name", "Muscle Group", "Reps", "Sets"))
        print("-" * 65)

        for row in exercises:
            exercise_id = row[0]
            exercise_name = row[1]
            muscle_group = row[2]
            reps = row[3]
            sets = row[4]
            print("{:<5} {:<25} {:<15} {:<5} {:<5}".format
                  (exercise_id, exercise_name, muscle_group, reps, sets))

# *****************************************************************************


# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS categories (category_id INTEGER
               PRIMARY KEY, Category_Name Text)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS exercises (exercise_id INTEGER
               PRIMARY KEY,exercise_name TEXT, muscle_group TEXT, reps INTEGER,
                sets INTEGER, category_id INTEGER, FOREIGN KEY(category_id)
               REFERENCES categories(category_id) )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS workout_routines
               (workout_routine_id INTEGER PRIMARY KEY, routine_name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS workout_routine_exercises
               (workout_routines_exercises_id INTEGER PRIMARY KEY, routine_id
               INTEGER, exercise_id INTEGER, FOREIGN KEY (routine_id)
               REFERENCES workout_routines(workout_routine_id), FOREIGN KEY
               (exercise_id) REFERENCES exercises(exercise_id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS goals (goals_id INTEGER PRIMARY
    KEY, goal_type TEXT, target_value REAL, current_value REAL, unit TEXT)''')

db.commit()
# *****************************************************************************

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
# -----------------------MENU OPTION 1-----------------------------------------

    if menu == '1':  # Add exercise category

        exercise_category = input('''
Please enter your exercise category to add (0 to cancel): ''')

        while exercise_category != '0':
            # Check if category exists
            cursor.execute('''SELECT category_name FROM categories WHERE
                           category_name = (?)''', (exercise_category,))

            if cursor.fetchone() is None:
                cursor.execute('''INSERT INTO categories(category_name)
                                VALUES(?)''', (exercise_category, ))
                print("Exercise category added successfully!")

            else:
                print('CATEGORY ALREADY EXISTS!')

            db.commit()
            exercise_category = input('''
Please enter your desired exercise category (0 to cancel): ''')

# ------------------------MENU OPTION 2----------------------------------------

    elif menu == '2':  # View exercise by category

        view_exercise_category = input('''
Please enter your exercise category to view exercises from (0 to cancel): ''')

        while view_exercise_category != '0':

            display_exercises_by_category(view_exercise_category)
            break

# -------------------------MENU OPTION 3---------------------------------------

    elif menu == '3':

        display_categories()
        delete_exercise_category = input('\nPlease enter the category of which'
                                         ' the exercise you would like to '
                                         'remove(0 to cancel): ')
        while delete_exercise_category != 0:

            display_exercises_by_category(delete_exercise_category)
            delete_exercise = input('Please enter the exercise name from above'
                                    ' that you would like to delete: ')

            cursor.execute('''SELECT exercise_name from exercises WHERE
                UPPER(exercise_name) = (?)''', (delete_exercise.upper(), ))
            found_exercise = cursor.fetchone()
            found_exercise = found_exercise[0]

            if found_exercise is None:
                print('Exercise does not exist, pick from the list above!')

            else:
                confirmation = input(f'''
Are you sure you want to delete{found_exercise} (Y/N)? ''')
                if confirmation.upper() == 'Y':
                    cursor.execute('''DELETE FROM exercises WHERE
                    UPPER(exercise_name) = (?)''', (delete_exercise.upper(), ))
                    print(f'{found_exercise} DELETED SUCCESSFULLY!!!')
                else:
                    print('CANCELED!')
                    break
# ------------------------MENU OPTION 4----------------------------------------

    elif menu == '9':
        exit()

    else:
        print('\nOOPS!, INVALID ENTRY *_*\n'
              'PLEASE SELECT FROM THE OPTIONS PROVIDED\n')
