import os
import sys


def init_command():
    command_list = ["rm", "reboot", "shutdown", "init", "mkfs", "fdisk", "dd"]
    command_group, _ = CommandGroupModel.objects.update_or_create(
            name="危险命令",
            defaults={
                "description": "System default command group: Danger Command"
            }
    )
    for command in command_list:
        command_query, _ = CommandModel.objects.update_or_create(
            command=command,
            defaults={
                "block_type": 1
            }
        )
        CommandGroupRelationshipModel.objects.update_or_create(command=command_query, command_group=command_group)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    import datetime

    print(" [Success] {} init_command Running".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    import django
    django.setup()
    from bastion.models import CommandGroupModel, CommandModel, CommandGroupRelationshipModel
    init_command()
    print(" [Success] {} init_command Execution Complete".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))