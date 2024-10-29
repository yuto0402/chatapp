import os
import django
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intern.settings')
django.setup()

from myapp.models import TalkRoom, CustomUser

def delete_fake_users_and_talks():
    # Faker で生成されたユーザー名のパターンや条件に基づいて削除するフェイクユーザーを取得
    fake_users = CustomUser.objects.filter(email__contains='@example.com')

    if fake_users.exists():
        # フェイクユーザーの ID を取得
        fake_user_ids = fake_users.values_list('id', flat=True)

        # 関連する TalkRoom データを削除
        TalkRoom.objects.filter(sender_id__in=fake_user_ids).delete()
        TalkRoom.objects.filter(receiver_id__in=fake_user_ids).delete()

        # フェイクユーザーの削除
        fake_users.delete()

        print(f'Deleted {len(fake_user_ids)} fake users and their talks.')
    else:
        print('No fake users found.')

if __name__ == '__main__':
    print('Deleting fake users and talks...')
    delete_fake_users_and_talks()
    print('Done.')
