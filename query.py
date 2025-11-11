import sqlite3

with sqlite3.connect('concrete.db') as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. SHOW ALL TESTS
    print("ALL TESTS")

    cursor.execute('SELECT * FROM concrete_tests')

    while row := cursor.fetchone():
        project_name = row[1]
        actual_strength = row[4] 
        passed = row[5]
        if row[5] == 1:
            passed = "PASS"
        else: passed = "FAIL"
        print(f"{project_name}: {actual_strength} PSI - {passed}")

    # 2. Show ONLY failed tests
    print("\n\nFAILED TESTS")

    cursor.execute('''
        SELECT project_name, test_date, required_strength, actual_strength, passed
        FROM concrete_tests
        WHERE passed < 1
    ''')

    while row := cursor.fetchone():
        project_name = row[0]
        test_date = row[1]
        required_strength = row[2]
        actual_strength = row[3] 
        print(f"{project_name} on {test_date}\n  Required: {required_strength} PSI\n  Actual: {actual_strength} PSI\n\n")


    # 3. Count tests by project
    print("TESTS PER PROJECT")

    cursor.execute("SELECT DISTINCT project_name FROM concrete_tests")

    rows = cursor.fetchall()
    projects = [r['project_name'] for r in rows]

    for name in projects:
        totalCount = 0
        passedCount = 0

        cursor.execute('''
            SELECT project_name, passed
            FROM concrete_tests
                       ''')
        
        while row := cursor.fetchone():
            if row[0] == name:
                totalCount += 1
                if row[1] > 0:
                    passedCount += 1
        
        print(f"{name}: {passedCount}/{totalCount} passed")


