from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from random import choice
from AskMe.models import Profile, Tag, Question, Answer, QuestionReaction, AnswerReaction
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, nargs = '?', default=10000 ,help='Ratio for filling the database')

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(f"Generate data with ratio = {ratio}")

        # users = []
        # profiles = []
        # counter = 0
        # base_username = "username"
        # for _ in range(ratio):
        #     logos = ['avatars/logo1.png', 'avatars/logo2.jpeg', 'avatars/logo3.jpeg']
        #     random_logo = random.choice(logos)

        #     username = f"{base_username}{counter}"

        #     user = User(username=username, email=fake.email())
        #     user.set_password('password')
        #     users.append(user)

        #     profile = Profile(user=user, avatar=random_logo, created_at=fake.date_time_this_year(), rating=0)
        #     profiles.append(profile)

        #     counter += 1

        #     if (counter % 100 == 0):
        #         self.stdout.write(f'Created {counter} users')

        # User.objects.bulk_create(users)
        # Profile.objects.bulk_create(profiles)

        # self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users and profiles.'))

        users = User.objects.all()
        profiles = Profile.objects.all()

        # base_tag = "tag_"
        # tags = []
        # counter = 0
        # while len(tags) < ratio:
        #     tag_name = f"{base_tag}{counter}"
        #     tags.append(Tag(name=tag_name))
        #     counter += 1
        #     if counter % 100 == 0:
        #         self.stdout.write(f'Created {counter} tags')

        # Tag.objects.bulk_create(tags)
        # self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} unique tags.'))
        
        #tags = Tag.objects.all()
        # counter = 0
        # questions = []
        # for _ in range(ratio * 10):
        #     profile = random.choice(users).profile
        #     question = Question(
        #         profile=profile,
        #         title=fake.sentence(nb_words=6),
        #         body=fake.paragraph(nb_sentences=3),
        #         created_at=fake.date_time_this_year(),
        #         rating=0,
        #         like_count=0,
        #         dislike_count=0,
        #     )
        #     questions.append(question)
            
        #     counter += 1
        #     if counter % 1000 == 0:
        #         self.stdout.write(f'Created {counter} questions')

        # Question.objects.bulk_create(questions)
        # self.stdout.write(self.style.SUCCESS(f'Created {len(questions)} questions.'))


        # for question in questions:
        #     selected_tags = random.sample(tags, k=random.randint(1, 5))
        #     question.tags.set(selected_tags)

        questions = Question.objects.all()
        
        # counter = 0
        # answers = []
        # for _ in range(ratio * 100):
        #     profile = random.choice(users).profile
        #     question = random.choice(questions)
        #     answer = Answer(
        #         profile=profile,
        #         question=question,
        #         body=fake.paragraph(nb_sentences=3),
        #         created_at=fake.date_time_this_year(),
        #         rating=0,
        #         like_count=0,
        #         dislike_count=0,
        #         is_correct=random.choice([True, False]),
        #     )
        #     answers.append(answer)

        #     counter += 1
        #     if counter % 10000 == 0:
        #         self.stdout.write(f'Created {counter} asks')

        # Answer.objects.bulk_create(answers)

        # self.stdout.write(self.style.SUCCESS(f'Created {len(answers)} answers.'))

        answers = Answer.objects.all()

        counter = 0
        
        existing_question_reactions = set()
        existing_answer_reactions = set()
        for _ in range(ratio * 200):
            profile = random.choice(users).profile
            
            if choice([True, False]):
                # True - questions_reaction
                question = random.choice(questions)
                if (profile.id, question.id) not in existing_question_reactions:
                    reaction_type = random.choice([QuestionReaction.LIKE, QuestionReaction.DISLIKE])
                    question_reaction = QuestionReaction(
                        profile=profile,
                        question=question,
                        reaction=reaction_type,
                        created_at=fake.date_time_this_year()
                    )
                    existing_question_reactions.add((profile.id, question.id))
                    if reaction_type == QuestionReaction.LIKE:
                        profile.rating += 1
                    else:
                        profile.rating -= 1
                    
                    question_reaction.save()
            else:
                # False - answers_reaction
                answer = random.choice(answers)
                if (profile.id, answer.id) not in existing_answer_reactions:
                    reaction_type = random.choice([AnswerReaction.LIKE, AnswerReaction.DISLIKE])
                    answer_reaction = AnswerReaction(
                        profile=profile,
                        answer=answer,
                        reaction=reaction_type,
                        created_at=fake.date_time_this_year()
                    )
                    existing_answer_reactions.add((profile.id, answer.id))
                    if reaction_type == AnswerReaction.LIKE:
                        profile.rating += 1
                    else:
                        profile.rating -= 1
                    answer_reaction.save()
                
            counter += 1
            if counter % 100000 == 0:
                self.stdout.write(f'Created {counter} reactions')

        counter = 0
        for profile in profiles:
            profile.save()
            counter += 1
            if counter % 1000 == 0:
                self.stdout.write(f'saved{counter} profiles')

        self.stdout.write(self.style.SUCCESS(f'Created {ratio * 200} reactions.'))
