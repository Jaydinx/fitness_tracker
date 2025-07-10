import sqlite3

db = sqlite3.connect('data/fitness_tracker_db')
cursor = db.cursor()

'''This fitness tracker app allows the user to perform multiple operations such
   as adding workout categories, updating workout categories, removing workout
   categories, creating workout goals, goal categories, removing the goal
   category as well as calculating the user's fitness goal progress based on
   the information they have provided'''

# -----------------------FUNCTIONS---------------------------------------------


def get_valid_input(prompt, field_name):
    while True:
        user_input = input(prompt)
        if check_for_null(user_input, field_name):
            return user_input
        else:
            print(f"Invalid {field_name}. Please try again.\n")


def enter_goal():
    print("🎯 Let's set a new fitness goal!\n")

    goal_type = get_valid_input(
        "Enter the type of goal (e.g., weight loss, 1-rep max, running distance): ",
        "goal type"
    )

    target_value = get_valid_input(
        "Enter the target value for your goal (just the number): ",
        "target value"
    )

    unit = get_valid_input(
        "Enter the unit of measurement (e.g., kg, km, sec): ",
        "unit"
    )

    current_value = get_valid_input(
        "Enter your current progress value (just the number): ",
        "current value"
    )

    try:
        cursor.execute('''
            INSERT INTO goals (goal_type, target_value, unit, current_value)
            VALUES (?, ?, ?, ?)
        ''', (goal_type, float(target_value), unit, float(current_value)))
        db.commit()
        print("\n✅ Goal saved successfully into the database!\n")

    except Exception as e:
        print(f"Failed to save goal: {e}")

    return goal_type, target_value, unit, current_value


def check_for_null(entry, specification):

    if entry == '':
        print(f"Please enter a value for {specification}")
        return (False)
    else:
        return (True)


def print_fitness_goals():

    cursor.execute('''SELECT * FROM goals''')
    goals = cursor.fetchall()
    print("\n")
    print("{:<10} {:<20} {:<20} {:<20} {:<10}".format(
        "ID", "Goal Type", "Target Value", "Current Value", "Unit"))
    print(80*"-")

    for row in goals:

        goal_id = row[0]
        goal_type = row[1]
        target_value = row[2]
        current_value = row[3]
        unit = row[4]
        print("{:<10} {:<20} {:<20} {:<20} {:<10}".format(
         goal_id, goal_type, target_value, current_value, unit))


def check_if_exercise_exists(select_exercise, selected_exercises):

    cursor.execute('SELECT exercise_name FROM exercises WHERE exercise_id'
                   '= (?)', (select_exercise, ))
    exercise_name = cursor.fetchone()
    if exercise_name is None:
        print('EXERCISE ID IS OUT OF RANGE, PLEASE SELECT FROM OPTIONS ABOVE')
        return (False)
    else:

        if select_exercise in selected_exercises:

            print('You have already included this exercise in your'
                  ' routine! Please try a different exercise or '
                  'enter 0 to exit')
            return (False)
        else:
            return (True)


def display_all_exercises():

    cursor.execute('SELECT * FROM exercises')
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


def display_categories():

    cursor.execute('''SELECT * from categories''')
    categories = cursor.fetchall()
    db.commit()

    print('{:<25}'.format('CATEGORY LIST'))
    print('-'*65)

    for row in categories:
        category_name = row[1]
        print('{:<25}'.format(category_name))


'''The function "display_exercises_by_category" ensures that the selected data
    is displayed in a neat and legible format'''


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


def print_exercise_progress():

    print("{:<10} {:<25} {:<20}".format("ID", "Exercise", "Weight"))
    print("-"*45)
    cursor.execute('''SELECT exercise_id from exercise_progress''')
    exercise_id = cursor.fetchall()

    for row in exercise_id:
        exercise_id = row[0]
        cursor.execute('''SELECT  exercise_id, exercise_name FROM exercises
                        WHERE exercise_id = ?''', (exercise_id,))
        exercise = cursor.fetchone()
        cursor.execute('''SELECT Weight FROM exercise_progress where
                       exercise_id = (?)''', (exercise_id,))
        weight = cursor.fetchone()

        if exercise and weight:

            print("{:<10} {:<25} {:<20}".format(*exercise, *weight))

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

cursor.execute('''CREATE TABLE IF NOT EXISTS exercise_progress
               (progress_id INTEGER PRIMARY KEY, exercise_id INTEGER,
               weight INTEGER, FOREIGN KEY (exercise_id) REFERENCES
               exercises(exercise_id))''')

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
6. View / Update Exercise Progress
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

    elif menu == '3':  # Delete exercise by category

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
    elif menu == '4':  # Create workout routine

        routine_name = input('Please enter the name of your new workout'
                             'routine: ')
        display_all_exercises()
        selected_exercises = []
        select_exercise = input('Please select an exercise by typing in '
                                'the id of the corresponding exercise: ')

        while select_exercise != '0' and select_exercise.upper() != 'A':

            if check_if_exercise_exists(select_exercise, selected_exercises)\
                  is True:
                selected_exercises.append(select_exercise)

            select_exercise = input('Please select an exercise by typing in '
                                    'the id of the corresponding exercise'
                                    '(A to confirm and submit all selected'
                                    ' exercises): ')

        if select_exercise.upper() == 'A':
            if selected_exercises == []:
                print('ZERO EXERCISES SELECTED'
                      ', NONE ADDED, ROUTINE CREATION CANCELED')

            else:
                cursor.execute('''INSERT INTO workout_routines
                            (routine_name) VALUES (?)''', (routine_name, ))
                cursor.execute('''SELECT workout_routine_id FROM
                               workout_routines WHERE routine_name = (?)''',
                               (routine_name, ))

                routine_id = cursor.fetchone()
                for exercise_id in selected_exercises:
                    cursor.execute('''INSERT INTO workout_routine_exercises
                                   (routine_id, exercise_id) VALUES (?, ?)''',
                                   (routine_id[0], exercise_id))
                db.commit()
                print(f"Exercise routine '{routine_name}'"
                      " created successfully")

# -----------------------------MENU OPTION 5-----------------------------------

    elif menu == '5':  # View workout routine

        routine_name_search = input('Please input the name of the routine you'
                                    ' would like to view: ')
        if routine_name_search != '':

            cursor.execute('''SELECT routine_name, workout_routine_id from
                           workout_routines WHERE UPPER(routine_name) = (?)
                           ''', (routine_name_search.upper(), ))
            routine_found = cursor.fetchone()

            if routine_found is not None:

                workout_routine_id = routine_found[1]
                cursor.execute('''SELECT exercise_id FROM
                               workout_routine_exercises WHERE routine_id = (?)
                               ''', (workout_routine_id, ))
                found_exercise_id = cursor.fetchall()
                print(f"\n{routine_name_search.upper()} ROUTINE\n")
                print("{:<5} {:<25} {:<15} {:<5} {:<5}"
                      .format("ID", "Exercise Name", "Muscle Group", "Reps",
                              "Sets"))
                print("-" * 65)

                for row in found_exercise_id:

                    exercise_id = row[0]
                    cursor.execute('''SELECT exercise_id, exercise_name,
                                   muscle_group, reps, sets FROM exercises
                                   WHERE exercise_id = ?''', (exercise_id,))
                    exercise = cursor.fetchone()

                    if exercise:
                        print("{:<5} {:<25} {:<15} {:<5} {:<5}"
                              .format(*exercise))

            else:
                print("ROUTINE NOT FOUND, PLEASE ENSURE YOU ENTER AN EXISTING"
                      " ROUTINE NAME")

        else:
            print('You have not entered a routine name, please try again')

# -------------------------------MENU OPTION 6---------------------------------
    elif menu == '6':  # View / Update exercise progress

        print_exercise_progress()
        update_progress_confirmation = input("Would you like to update an"
                                             " exercise goal? (Y / N): ")
        update_progress_confirmation = update_progress_confirmation.strip()
        if update_progress_confirmation.upper() == 'Y':

            progress_to_update = input("Please enter the exercise ID of which"
                                       " exercise you wish to update: ")
            cursor.execute('''SELECT exercise_id FROM exercise_progress WHERE
                           exercise_id = (?)''', (progress_to_update,))
            exercise_id = cursor.fetchone()
            exercise_id = int(exercise_id[0])
            if exercise_id is None:
                print('''Exercise not found, please ensure you have entered
                      the correct id''')

            else:
                cursor.execute('''SELECT exercise_name FROM exercises WHERE
                               exercise_id = (?)''', (exercise_id,))
                exercise_name = cursor.fetchone()
                print("You are updating the weight progress for"
                      f" {exercise_name[0]}")

                weight_change = int(input("Please enter the new weight for"
                                          f" {exercise_name[0]}: "))
                cursor.execute('''UPDATE exercise_progress SET weight = ? WHERE
                            exercise_id = ?''', (weight_change, exercise_id,))
                db.commit()
                print("PROGRESS UPDATED SUCCESSFULLY!")
                print_exercise_progress()

        elif update_progress_confirmation.upper() == 'N':
            print("Returning to main menu *_*")

        else:
            print("You have entered an incorrect value, Please specify Y or N")

    elif menu == '7':

        set_or_update = input("Would you like to set a new fitness goal (S)"
                              " or Update an existing fitness goal(U)"
                              " Please enter your desired option: ")

        if set_or_update.upper() == 'S':

            enter_goal()

        elif set_or_update.upper() == 'U':

            print_fitness_goals()
            goal_id = input("\nPlease enter the ID of the goal"
                            " you wish to update: ")
            cursor.execute('''SELECT goals_id FROM goals WHERE goals_id = ?''',
                           (goal_id,))
            goal_id_found = cursor.fetchone()
            if goal_id_found is None:
                print('PLEASE ENTER A VALID GOAL ID FROM THE TABLE ABOVE')

            else:
                while True:
                    update_menu = input(
                                    "Please select what you would like to update"
                                    "\n\n1. Goal Type\n"
                                    "2. Target Value\n"
                                    "3. Current Value\n"
                                    "4. Unit\n"
                                    "0. Exit\n"
                                    "\nEnter your desired option here: "
                                    ).strip()

                    if update_menu == '1':
                        new_goal_type = input("Please enter your updated goal"
                                            " type here: ")
                        cursor.execute('''UPDATE goals SET goal_type = ? WHERE
                                       goals_id = ?''', (new_goal_type,
                                                         goal_id_found[0],))
                        print("GOAL TYPE UPDATED SUCCESSFULLY!")

                    elif update_menu == '2':
                        new_target_value = input("Please enter your new target"
                                                 " here: ")
                        cursor.execute('''UPDATE goals SET target_value = ?
                                       WHERE goals_id = ?''',
                                       (new_target_value, goal_id_found[0],))
                        print("TARGET VALUE UPDATED SUCCESSFULLY!")

                    elif update_menu == '3':
                        new_current_value = input("Please enter your new "
                                                  "current value here: ")
                        cursor.execute('''UPDATE goal SET current_value = ?
                                       WHERE goals_id = ?''',
                                       (new_current_value, goal_id_found[0],))
                        print("CURRENT VALUE UPDATED SUCCESSFULLY!")

                    elif update_menu == '4':
                        new_unit = input("Please enter your new unit here: ")
                        cursor.execute('''UPDATE goals SET unit = ? WHERE
                                       goals_id = ?''', (new_unit,
                                                         goal_id_found[0],))
                        print("UNIT UPDATED SUCCESSFULLY!")

                    elif update_menu == '0':
                        print("UPDATE WAS CANCELED, GOODBYE!")
                        break

                    else:
                        print("Invalid entry, please enter the number"
                              " corresponding to the options provided")

            db.commit()

    elif menu == '9':
        exit()

    else:
        print('\nOOPS!, INVALID ENTRY *_*\n'
              'PLEASE SELECT FROM THE OPTIONS PROVIDED\n')
