from bastion.models import CommandGroupModel, CommandModel, CommandGroupRelationshipModel


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
