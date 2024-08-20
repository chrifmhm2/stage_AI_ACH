# import os
# import csv
# from django.core.management.base import BaseCommand
# from myapp.models import Bank, Account
#
# class Command(BaseCommand):
#     help = 'Load data from TSV files into the database'
#
#     def handle(self, *args, **options):
#         # Déterminer le répertoire de base du projet
#         base_dir = os.path.dirname(os.path.abspath(__file__))
#
#         # Chemin vers les fichiers TSV
#         accounts_path = os.path.join(base_dir, 'accounts.tsv')
#         banks_path = os.path.join(base_dir, 'banks.tsv')
#
#         self.load_accounts(accounts_path)
#         # self.load_banks(banks_path)
#
#     # def load_accounts(self, accounts_path):
#     #     with open(accounts_path, 'r', encoding='utf-8') as file:
#     #         reader = csv.reader(file, delimiter='\t')
#     #         for row in reader:
#     #             if len(row) < 6:
#     #                 self.stdout.write(self.style.ERROR(f"Skipping row due to missing fields: {row}"))
#     #                 continue
#     #
#     #             old_acnt_num, acnt_num, name, curr, old_rib, new_rib = row
#     #             Account.objects.update_or_create(
#     #                 old_acnt_num=old_acnt_num,
#     #                 defaults={
#     #                     'acnt_num': acnt_num,
#     #                     'name': name,
#     #                     'curr': curr,
#     #                     'old_rib': old_rib,
#     #                     'new_rib': new_rib
#     #                 }
#     #             )
#     #
#     #     self.stdout.write(self.style.SUCCESS('Successfully loaded accounts data'))
#
#     # def load_banks(self, banks_path):
#     #     with open(banks_path, 'r', encoding='utf-8') as file:
#     #         reader = csv.reader(file, delimiter='\t')
#     #         for row in reader:
#     #             if len(row) < 2:
#     #                 self.stdout.write(self.style.ERROR(f"Skipping row due to missing fields: {row}"))
#     #                 continue
#     #
#     #             bank_id, bank_name = row
#     #             Bank.objects.update_or_create(
#     #                 bank_id=bank_id,
#     #                 defaults={'bank_name': bank_name}
#     #             )
#     #
#     #     self.stdout.write(self.style.SUCCESS('Successfully loaded banks data'))
#
#     def load_accounts(self, accounts_path):
#         with open(accounts_path, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file, delimiter='\t')
#             for row in reader:
#                 if len(row) < 6:
#                     self.stdout.write(self.style.ERROR(f"Skipping row due to missing fields: {row}"))
#                     continue
#
#                 old_acnt_num, acnt_num, account_name, curr, old_rib, new_rib = row
#                 Account.objects.update_or_create(
#                     old_acnt_num=old_acnt_num,
#                     defaults={
#                         'acnt_num': acnt_num,
#                         'account_name': account_name,
#                         'curr': curr,
#                         'old_rib': old_rib,
#                         'new_rib': new_rib
#                     }
#                 )
#
#         self.stdout.write(self.style.SUCCESS('Successfully loaded accounts data'))


import os
import csv
from django.core.management.base import BaseCommand
from myapp.models import Bank, Account

class Command(BaseCommand):
    help = 'Load data from TSV files into the database'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        accounts_path = os.path.join(base_dir, 'accounts.tsv')
        banks_path = os.path.join(base_dir, 'banks.tsv')

        self.load_accounts(accounts_path)
        # self.load_banks(banks_path)

    def load_accounts(self, accounts_path):
        with open(accounts_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)  # Sauter la première ligne (les en-têtes)
            for row in reader:
                if len(row) < 6:
                    self.stdout.write(self.style.ERROR(f"Skipping row due to missing fields: {row}"))
                    continue

                old_acnt_num, acnt_num, account_name, curr, old_rib, new_rib = row
                Account.objects.update_or_create(
                    old_acnt_num=old_acnt_num,
                    defaults={
                        'acnt_num': acnt_num,
                        'account_name': account_name,
                        'curr': curr,
                        'old_rib': old_rib,
                        'new_rib': new_rib
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded accounts data'))

    def load_banks(self, banks_path):
        with open(banks_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)  # Sauter la première ligne (les en-têtes)
            for row in reader:
                if len(row) < 2:
                    self.stdout.write(self.style.ERROR(f"Skipping row due to missing fields: {row}"))
                    continue

                bank_id, bank_name = row
                Bank.objects.update_or_create(
                    bank_id=bank_id,
                    defaults={'bank_name': bank_name}
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded banks data'))
