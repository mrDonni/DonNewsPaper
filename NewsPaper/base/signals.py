from django.db.models.signals import post_save, pre_init, post_delete, pre_delete, post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from django.core.mail import mail_managers, send_mail
from .models import *

@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
	print(kwargs, '****************')
	# print(list(instance.category), '*')
# 	subject = f'{instance.author} {instance.date.strftime("%d %m %Y")}'
# 	print()
	# print(instance.category)
	# print(created, 'created')
	# if created:
	# 	print('запись создана')
		# print(instance.category.all())
		# print(Post.objects.all())
		# for i in cat:
		# 	users = i.subscribers.all()
		# 	for user in users:
		# 		print(user.email)
		# 		if user.email:
		# 			print('нашли юзера, отправляем ему на емаил.')
					# send_mail(
					# 	subject = f'{subject}',
					# 	message = f'{instance.content}-запись создана',
					# 	from_email = 'donnewspaper@mail.ru',
					# 	recipient_list = [user.email, ],
					# )
