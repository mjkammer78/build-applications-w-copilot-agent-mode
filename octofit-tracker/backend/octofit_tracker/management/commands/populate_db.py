from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Explicitly drop the `octofit_tracker_user` collection to ensure no residual data remains
        db['octofit_tracker_user'].drop()

        # Drop existing collections using raw MongoDB commands
        db['octofit_tracker_team'].delete_many({})
        db['octofit_tracker_activity'].delete_many({})
        db['octofit_tracker_leaderboard'].delete_many({})
        db['octofit_tracker_workout'].delete_many({})

        # Create users
        users = []
        user_data = [
            {'username': 'thundergod', 'email': 'thundergod@mhigh.edu', 'password': 'thundergodpassword'},
            {'username': 'metalgeek', 'email': 'metalgeek@mhigh.edu', 'password': 'metalgeekpassword'},
            {'username': 'zerocool', 'email': 'zerocool@mhigh.edu', 'password': 'zerocoolpassword'},
            {'username': 'crashoverride', 'email': 'crashoverride@mhigh.edu', 'password': 'crashoverridepassword'},
            {'username': 'sleeptoken', 'email': 'sleeptoken@mhigh.edu', 'password': 'sleeptokenpassword'},
        ]
        for data in user_data:
            user = User(**data)
            user.save()
            users.append(user)

        # Create teams
        team = Team(name='Blue Team')
        team.save()
        team.members.add(*users)

        # Create activities
        activities = [
            Activity(user=users[0], type='Cycling', duration=60),
            Activity(user=users[1], type='Crossfit', duration=120),
            Activity(user=users[2], type='Running', duration=90),
            Activity(user=users[3], type='Strength', duration=30),
            Activity(user=users[4], type='Swimming', duration=75),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(user=users[0], score=100),
            Leaderboard(user=users[1], score=90),
            Leaderboard(user=users[2], score=95),
            Leaderboard(user=users[3], score=85),
            Leaderboard(user=users[4], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event'),
            Workout(name='Crossfit', description='Training for a crossfit competition'),
            Workout(name='Running Training', description='Training for a marathon'),
            Workout(name='Strength Training', description='Training for strength'),
            Workout(name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
