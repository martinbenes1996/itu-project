from django.core.mail import send_mail

send_mail(
    'Email from GoFlamingo',
    'Here is the message.',
    'from@example.com',
    ['xbarto92@fit.vutbr.cz'],
    fail_silently=False,
)