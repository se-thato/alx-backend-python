from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessageNotificationTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')


    def notification_created_on_message(self):
        message = Message.objects.create(
            sender = self.sender,
            receiver = self.receiver,
            content = 'new message'
        )

        notification = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notification.count(), 1)
