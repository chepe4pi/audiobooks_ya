from celery import shared_task
import subprocess as sub
from time import time

from constance import config
from django.conf import settings
from slugify import slugify


@shared_task
def generate_abook(generation_info_id):
    time_now = int(time())

    from abook_generating.models import ABookGeneration
    info = ABookGeneration.objects.get(pk=generation_info_id)
    info.status = 'generating'
    info.save()

    file_path = '{}{}-{}.wav'.format(settings.DROPBOX_DIR, slugify(info.book_name), time_now)

    command = ["ttsclient-cli.py", '--key={}'.format(config.KEY), '--speaker', info.speaker, '--lang', info.lang,
               '--textfile', info.book_text.path, file_path]

    if info.gender != 'unknown':
        command.append('--gender')
        command.append(info.gender)

    p = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()

    error_log = None
    if errors:
        error_log = str(errors)
    if 'Request complete' not in str(output):
        error_log = str(output)

    if error_log:
        info.error_log = error_log
        info.status = 'error'
    else:
        info.status = 'done'
        info.generated_file = file_path
    info.save()
