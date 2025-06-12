from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    #this will check if the message, if yes it will then create a new notification
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)



@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Only for updates, not new messages
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message=old_instance,
                    old_content=old_instance.content
                )
                instance.edited = True 
        except Message.DoesNotExist:
            pass




User = get_user_model()

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    # Clean up any lingering MessageHistory where edited_by was the deleted user
    MessageHistory.objects.filter(edited_by=instance).delete()

    # Redundant safety check: delete messages or notifications just in case
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()