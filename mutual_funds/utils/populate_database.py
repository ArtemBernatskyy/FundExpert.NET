# %autoindent to enable copy paste functionality

import random

from django.utils import timezone

from faker import Faker
from slugify import slugify
# from django_countries.fields import Country
# from djmoney.models.fields import MoneyPatched

from mutual_funds.finance.models import *
from mutual_funds.landing.models import *
from mutual_funds.company.models import *

fake = Faker()

# creating FinanceClasses
for i in range(3):
    FinanceClass(name='class name ' + str(i)).save()
print('FinanceClasses created')


# creating FinanceSectors
# for i in range(300):
#     FinanceSector(
#         name='sector name ' + str(i),
#         finance_class=FinanceClass.objects.all()[random.randint(0, 2)]).save()
# print('FinanceSectors created')


# creating ManagementCompany
for i in range(60):
    temp_name = fake.company()
    ManagementCompany(
        name='MO: ' + temp_name,
        slug=slugify(temp_name, to_lower=True),
        fund_manager=fake.name(),
        investment_strategy=fake.text()).save()
print('ManagementCompanies created')

# creating Funds
# for i in range(300):
#     s = fake.currency_code()
#     bloom = ''.join(random.sample(s, len(s)))
#     isin = ''.join(random.sample(s, len(s)))
#     tname = fake.company()
#     Fund(name='fund: ' + tname,
#         management_company=ManagementCompany.objects.all()[random.randint(0, 59)],
#         finance_sector=FinanceSector.objects.all()[random.randint(0, 2)],
#         bloombreg_ticker=bloom,
#         isin_ticker=isin,
#         ms_rating=str(random.randint(1, 5)),
#         birth_date=fake.date(),
#         country=Country(code=fake.country()),
#         slug=slugify(tname, to_lower=True),
#         currency=str(random.choice(["USD", "EUR"])),
#         total_assets=MoneyPatched(random.randint(10, 400)),
#         range_52_weeks=str(random.randint(10, 400)) + fake.currency_code(),
#         return_1_year=str(random.randint(10, 400))).save()
# print('Funds created')


# creating NewsCategories
for i in range(10):
    temp_name = fake.safe_color_name()
    NewsCategory(
        title=temp_name,
        slug=slugify(temp_name, to_lower=True) + str(random.randint(1, 223))).save()
print('NewsCategories created')


# # creating NewsPost
for i in range(30):
    temp_name = fake.sentence(nb_words=6, variable_nb_words=True)
    n = NewsPost(
        title=temp_name,
        slug=slugify(temp_name, to_lower=True) + str(random.randint(1, 223)),
        is_active=False,
        pub_date=timezone.now(),
        text=fake.text(max_nb_chars=5000))
    n.save()
    cat = NewsCategory.objects.all()[random.randint(0, 9)]
    n.category.add(cat)
live = NewsPost.objects.all()[:8]
for post in live:
    post.is_active = True
    post.save()
print('NewsPosts created, need to populate image fields')
