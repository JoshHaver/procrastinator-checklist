import random
import datetime

CHARITY_LIST = ["United Way", "Feeding America", "The Task Force for Global Health", "The Salvation Army",
                "St. Jude Children's Research Hospital", "Red Cross", "Direct Relief", "Habitat for Humanity",
                "The YMCA", "Americares"]
NEXT_STEPS_INTROS = ["For some direction, check out your next steps: ", "Here are your next steps: ",
                     "These are your next steps: ",
                     "Crush these next steps: ", "You're a beast! Here are your next steps: ",
                     "You've got this! Perform these next steps: ",
                     "Stay focused on these next steps: ", "Break the goal down into these next steps: ",
                     "If you need a place to start, here are your next steps: "]
SIX_HOURS = datetime.timedelta(hours=6.0)
TWENTY_FOUR_HOURS = datetime.timedelta(hours=24.0)
MEAL_TIME = datetime.timedelta(minutes=45.0)
NUM_GOALS = 3


class Goal:
    def __init__(self, name):
        # goal class initialization
        self.name = name
        self.actionables = []
        self.measurement = ""
        self.time = 0

    def set_measurement(self):
        # set measurements for success in the goal
        print("How will you measure success in accomplishing this goal? Ex: 'Make 10 sales calls'")
        self.measurement = input()

    def set_actionables(self):
        # sets the actionable steps to be taken towards the goals
        actionable = ""
        while actionable != "0":
            # loops until the user enters 0
            print("Enter the most important next steps for accomplishing this goal, enter 0 to stop")
            actionable = input()
            if actionable != "0":
                self.actionables.append(actionable)
                # appends each actionable to the member variable actionables which is a list of the actionable steps for each goal

    def set_time(self):
        while True:
            try:
                print("How many minutes will this goal take to accomplish?")
                time = int(input())
                self.time = datetime.timedelta(minutes=time)
            except ValueError:
                print("Enter only an integer amount of minutes \n")
                continue
            break

    def print_next_steps(self):
        next_step_intro = random.randint(0, 8)
        print(NEXT_STEPS_INTROS[next_step_intro])
        # prints one of the encouraging statements and then prints the next steps for the goal
        for next_step in self.actionables:
            print(next_step)


class Day:
    def __init__(self):
        # member variable init for day class
        self.goals_list = []
        self.wake_time = 0
        self.bed_time = 0
        self.breakfast = 0
        self.lunch = 0
        self.dinner = 0
        self.rewards_list = []


    def welcome(self):
        print("Welcome to the Productivity Checklist!")
        print("Congratulations on taking the first step towards having a successful day!")

    def read_rewards(self):
        open_file = open('rewards.txt', 'r', errors='ignore')
        self.rewards_list = open_file.readlines()
        # populates the rewards list member variable with the rewards in the rewards text file
        open_file.close()

    def set_goals(self):
        print("Enter 3 goals for today, in order of importance")

        for i in range(NUM_GOALS):
            # asks the user to enter info about each of their goals with a for loop
            print("Enter goal number ", i+1)
            name = input()
            current_goal = Goal(name)
            # initializes an instance of the goal class based on inputted information
            current_goal.set_actionables()
            current_goal.set_measurement()
            current_goal.set_time()
            # calls methods on current goal to set the actionable steps, measurement device, and approximate time to completion
            self.goals_list.append(current_goal)
            # appends the goals to the day class member list of goals

    def set_meals(self):
        print("Around what time do you typically eat breakfast?")
        while True:
            try:
                # tries to convert the user's entered time info into a datetime object
                print("Enter time in 24 hour format HH:MM:SS \n")
                breakfast = input()
                now = datetime.datetime.now()
                self.breakfast = now.strptime(breakfast, '%X')
            except ValueError:
                # if the user enters the time in the wrong format, the while loop will continue
                continue
            break
            # the while loop will break if the format is entered correctly
        print("Around what time do you typically eat lunch?")
        while True:
            try:
                print("Enter time in 24 hour format HH:MM:SS \n")
                lunch = input()
                now = datetime.datetime.now()
                self.lunch = now.strptime(lunch, '%X')
            except ValueError:
                continue
            break
        print("Around what time do you typically eat dinner?")
        while True:
            try:
                print("Enter time in 24 hour format HH:MM:SS \n")
                dinner = input()
                now = datetime.datetime.now()
                self.dinner = now.strptime(dinner, '%X')
            except ValueError:
                continue
            break
        # prompts the user for their meal times to be used for scheduling blocks and calculating their optimal productivity window

    def set_wake(self):
        # prompts the user for the time that they woke up
        # used for scheduling blocks and calculating optimal alertness window
        print("What time did you wake up today?")
        while True:
            try:
                print("Enter time in 24 hour format HH:MM:SS \n")
                wake = input()
                now = datetime.datetime.now()
                self.wake_time = now.strptime(wake, '%X')
            except ValueError:
                continue
            break

    def set_bed(self):
        # prompts the user for what time they go to bed
        print("What time do you typically go to bed?")
        while True:
            try:
                print("Enter time in 24 hour format HH:MM:SS \n")
                bed = input()
                now = datetime.datetime.now()
                self.bed_time = now.strptime(bed, '%X')
            except ValueError:
                continue
            break

    def get_donation(self):
        dollars = random.randint(1, 20)
        charity = random.randint(0, 9)
        # uses rand int to generate a random integer for the dollar amount as well as a random charity from the list of charities
        donation_statement = "Donate " + "$"+ str(dollars) + " to " + CHARITY_LIST[charity]
        # concatenates the strings and returns the statement
        return donation_statement

    def get_reward(self):
        reward = self.rewards_list[random.randint(0, len(self.rewards_list))]
        # uses randint with the rewards list member variable to return a random reward
        return reward

    def get_schedule(self):
        # there are 4 blocks of time in the schedule, wake up to breakfast, breakfast to lunch, lunch to dinner, and dinner to sleep
        now = datetime.datetime.now()
        print("It is now: ", now.strftime("%X"))
        # use time delta to calculate amount of time remaining in the block, then determine task
        day_time_remaining = self.bed_time - self.wake_time
        if day_time_remaining.seconds < 0:
            day_time_remaining += TWENTY_FOUR_HOURS
            # changes time remaining to account for the fact that the users bed time could be less than their wake time
            # ex: wake time = 08:00:00, bed time = 03:00:00

        # day time remaining is time left in the day

        block_one = self.breakfast - self.wake_time
        # block one is self.wake_time to self.breakfast, this is a timedelta object

        if self.goals_list[0].time > block_one:
            # prints a message to tell the user to do their goal in block one, or to work for as long as they can
            print("Crush your goal: ", self.goals_list[0].name, "for ", block_one, " minutes")
            self.goals_list[0].time -= block_one
        else:
            print("Execute your first goal: ", self.goals_list[0].name)
            self.goals_list[0].print_next_steps()
            block_one -= self.goals_list[0].time
            self.goals_list[0].time = 0
            print("Then crush goal two: ", self.goals_list[1].name, " until breakfast")
            self.goals_list[1].time -= block_one
        now += block_one

        day_time_remaining -= block_one + MEAL_TIME
        # prints the users most important next steps, and uses the whole morning energy boost to be productive

        # block one finished, working time subtracted from goal.time
        print("Enjoy breakfast, and come back 30 minutes after you're done so you feel refreshed!")
        print("Your alertness may drop 6 hours into your day, so we will work hard until then")
        now += MEAL_TIME
        # updates the now variable to reflect the change in time after completing the meal

        six_hours_in = self.wake_time + SIX_HOURS
        time_until_alertness_drop = six_hours_in - now
        time_until_lunch = self.lunch - now
        # two variables time until alertness drop and time until lunch track time left for block two
        # this is used to see how long the user should work on goal 2 for
        if time_until_lunch > time_until_alertness_drop:
            # if lunch comes before the alertness drop, then work until lunch, else work until alertness drop and then relax
            print("Finish goal 1 if necessary, and then work on: ", self.goals_list[1].name, " until lunch")
            self.goals_list[1].print_next_steps()
            self.goals_list[1].time -= time_until_lunch
        else:
            print("Finish goal 1 if necessary, and then work on: ", self.goals_list[1].name, " until ", six_hours_in.strftime('%X'), "then relax until lunch")
            self.goals_list[1].time -= time_until_alertness_drop
            self.goals_list[1].print_next_steps()
            # if alertness drop comes before lunch, then work until then
            # strftime is used to print the time of the awareness drop in readable format
        now += time_until_lunch
        now += MEAL_TIME
        # updates the current time to account for meal time

        print("Finish any remnants of goals 1/2, then absolutely destroy goal 3: ", self.goals_list[2].name)
        self.goals_list[2].print_next_steps()

        for i in range(NUM_GOALS):
            # uses a loop to call the reward and donation methods iteratively
            # prints what the user gets as a reward if they succeed or what the user has to donate if they fail
            print("Your criteria for success on goal ", i+1, " is: ", self.goals_list[i].measurement)
            print("If you achieve ", self.goals_list[i].name, " your reward will be: ")
            print(self.get_reward())
            print("If you fail to achieve goal ", i+1, " you will have to: ")
            print(self.get_donation(), '\n')


today = Day()
today.read_rewards()
today.welcome()
today.set_goals()
today.set_wake()
today.set_bed()
today.set_meals()
today.get_schedule()
