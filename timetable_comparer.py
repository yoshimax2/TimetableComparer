def process_timetable(timetable_unf: str):
    timetable = timetable_unf.split(",")
    for i in range(len(timetable)):
        if timetable[i].endswith("\xa0"):
            timetable[i] = timetable[i][:len(timetable[i])-1]
        if timetable[i].endswith("Â"):
            timetable[i] = timetable[i][:len(timetable[i])-1]
        if timetable[i].endswith("\n"):
            timetable[i] = timetable[i][:len(timetable[i])-1]
        if timetable[i].endswith(" "):
            timetable[i] = timetable[i][:len(timetable[i])-1]
        if timetable[i].startswith("ï»¿"):
            timetable[i] = timetable[i][3:]
        if timetable[i]=="\n":
            timetable[i] = ""
    return timetable

def find_frees(timetable_full: list):
    frees = []
    free_words = ["", "Curr Devt time", "PPA", "Tutor Role", "ECT time"] 
    for i in range(len(timetable_full)):
        if timetable_full[i] in free_words:
            frees.append(i)
    return frees

def am_i_teaching(me: str, i: int):
    if staff[me][i] not in busy_words and staff[me][i] not in free_words:
        return True
    else:
        return False

def is_day(i: int, day: str):
    if staff["Days"][i].find(day)!=-1:
        return True
    else:
        return False

def is_period(i: int, period: str):
    if staff["Days"][i].find(period)!=-1:
        return True
    else:
        return False

def status (teacher: str, period: int):
    if staff[teacher][i] in free_words:
        return "F"
    elif staff[teacher][i] == "On Call":
        return "OC"
    elif staff[teacher][i] in busy_words:
        return "B"
    else:
        return "T"

def print_obs(teacher, i):
    if status(teacher, i)=="OC":
        print(teacher, "-", staff["Days"][i], "(On Call)", "-", staff[me][i])
    else:
        print(teacher, "-", staff["Days"][i], "-", staff[me][i])

#Gets timetables
file = open("AllStaffTimetable.csv")

staff_timetables = file.readlines()
staff = {}
free_words = ["", "Curr Devt time", "PPA", "Tutor Role", "ECT time"]
busy_words = ["Line Mgt mtg", "ECT mentoring", "Blanking Code", "Computing Hub", "Ma&Co Hubs", "SLT mtg", "Admissions Mtg", "Care mtg", "Asst Head of Year"]

for i in range(len(staff_timetables)):
    staff_timetables[i] = process_timetable(staff_timetables[i])

    staff[staff_timetables[i][0]] = staff_timetables[i][1:]

continues = True


while continues:
    print("This program will compare a staff member's timetable with other staff to see when they're free/teaching.\n")
    say_once = True
    no_results = True
    
    #Gets name of person to find frees for
    while True:
        me = input("Enter the name of the staff member: ").title()
        if me not in staff:
            print("Not a valid teacher")
        else:
            break

    

    #Gets directions from user
    while True:
        free_observe = input("Do you want to find teachers who are free, teachers to observe, or teachers who can observe the staff member? Enter Free/Observe/Be Observed: ").title()
        if free_observe == "Free" or free_observe == "Observe" or free_observe == "Be Observed":
            break
        
    while True:
        instruction = input("What do you want to filter results by? Staff, Day, Year, Period, or None?: ").title()
        instructions = ["Staff", "Day", "Period", "Year", "None"]
        if instruction in instructions:
            break
        else:
            print("Enter Staff, Day, Year, Period, or None")

    #Gets staff
    if instruction == "Staff":
        while True:
            search = input("Enter the name of the second staff member: ").title()
            if search in staff:
                if search != me:
                    break
                else:
                    print("You can't compare the same timetables. Try again")
            else:
                print("Please only enter valid names")

    #Gets day
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    if instruction == "Day":
        while True:
            week = input("Enter A or B: ").title()
            day = input("Enter a weekday to filter frees by: ").title()

            if day in days:
                if week == "A" or week == "B":
                    if day == "Monday":
                        day = week + "Mon"
                    elif day == "Tuesday":
                        day = week + "Tue"
                    elif day == "Wednesday":
                        day = week + "Wed"
                    elif day == "Thursday":
                        day = week + "Thu"
                    else:
                        day = week + "Fri"
                    break
                else:
                    print("Enter A or B")
            else:
                print("That's not a valid weekday")

    #Gets year
    if instruction == "Year":
        while True:
            year = input("Enter year 7 or 8: ")

            if year == "7" or year == "8":
                break
            else:
                print("Enter 7 or 8")

    #Gets period
    if instruction == "Period":
        while True:
            week = input("Enter A or B: ").title()
            day = input("Enter a weekday: ").title()

            if day in days:
                if week == "A" or week == "B":
                    if day == "Monday":
                        period = week + "Mon"
                    elif day == "Tuesday":
                        period = week + "Tue"
                    elif day == "Wednesday":
                        period = week + "Wed"
                    elif day == "Thursday":
                        period = week + "Thu"
                    else:
                        period = week + "Fri"
                    try:
                        num = int(input("Enter a period from 0 (for tutorial) to 6: "))

                        if num >= 0 and num <= 6:
                            if num == 0:
                                num = "REG"
                            period = period + ":" + str(num)
                            break
                        else:
                            print("Please enter a value from 0 to 6")
                    except:
                        print("Please enter a number from 0 to 6")
                else:
                    print("Enter A or B")
            else:
                print("That's not a valid weekday")
            

    my_frees = find_frees(staff[me])
    print("\n")

    for teacher in staff:
        if teacher==me or teacher=="Days":
            continue
        for i in range(len(staff["Days"])):

            if free_observe == "Free":
                if instruction == "None":
                    if not(am_i_teaching(me, i)) and status(teacher, i)=="F":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                elif instruction == "Day":
                    if is_day(i, day) and not(am_i_teaching(me, i)) and status(teacher, i)=="F":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                        no_results = False
                elif instruction == "Staff":
                    if teacher==search and not(am_i_teaching(me, i)) and status(teacher, i)=="F":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                elif instruction == "Period":
                    if is_period(i, period) and not(am_i_teaching(me, i)) and status(teacher, i)=="F":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                        no_results = False
                else:
                    if say_once:
                        print("There are no valid results, as free teachers won't be with a specific year group")
                        say_once = False
                    break
            elif free_observe == "Observe":
                if instruction == "None":
                    if not(am_i_teaching(me, i)) and status(teacher, i)=="T":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                elif instruction == "Day":
                    if is_day(i, day) and not(am_i_teaching(me, i)) and status(teacher, i)=="T":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                        no_results = False
                elif instruction == "Staff":
                    if teacher==search and not(am_i_teaching(me, i)) and status(teacher, i)=="T":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                elif instruction == "Period":
                    if is_period(i, period) and status(teacher, i)=="T" and not(am_i_teaching(me, i)):
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
                        no_results = False
                else:
                    if not(am_i_teaching(me, i)) and staff[teacher][i].startswith(year) and status(teacher, i)=="T":
                        print(teacher, "-", staff["Days"][i], "-", staff[teacher][i])
            else:
                if instruction == "None":
                    if am_i_teaching(me, i) and (status(teacher, i)=="F" or status(teacher, i)=="OC"):
                        print_obs(teacher, i)
                elif instruction == "Day":
                    if is_day(i, day) and am_i_teaching(me, i) and (status(teacher, i)=="F" or status(teacher, i)=="OC"):
                        print_obs(teacher, i)
                        no_results = False
                elif instruction == "Staff":
                    if teacher==search and am_i_teaching(me, i) and (status(teacher, i)=="F" or status(teacher, i)=="OC"):
                        print_obs(teacher, i)
                elif instruction == "Period":
                    if is_period(i, period) and am_i_teaching(me, i) and (status(teacher, i)=="F" or status(teacher, i)=="OC"):
                        print_obs(teacher, i)
                        no_results = False
                else:
                    if am_i_teaching(me, i) and staff[teacher][i].startswith(year) and (status(teacher, i)=="F" or status(teacher, i)=="OC"):
                        print_obs(teacher, i)
    if (instruction == "Period" or instruction=="Day") and no_results:
        print("No results found")
    while True:
        again = input("\nDo you want to search again? Enter Y or N: ").upper()

        if again == "Y":
            print("\n")
            break
        elif again == "N":
            continues = False
            print("Goodbye!")
            break
        else:
            print("Enter Y or N")
        
