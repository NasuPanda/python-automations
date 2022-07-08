"""Application initialization script.

NOTE: Please execute this script as an administrator.

reference: https://github.com/aikige/homeBinWin/blob/master/setup/prepLockLogging.py
"""
import pathlib
import win32com.client


# Enumerations reference: https://docs.microsoft.com/ja-jp/windows/win32/api/taskschd/#enumerations
TASK_SCHEDULE_SERVICE = "Schedule.Service"
TASK_TRIGGER_SESSION_STATE_CHANGE = 11
TASK_ACTION_EXEC = 0
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0
NO_USER = ""
NO_PASSWORD = ""

TASK_SESSION_LOCK = 7
TASK_SESSION_UNLOCK = 8


def register_task(scheduler, state_change, name, command):
    folder = scheduler.GetFolder("\\")

    definition = scheduler.NewTask(0)

    trigger = definition.Triggers.Create(TASK_TRIGGER_SESSION_STATE_CHANGE)
    trigger.StateChange = state_change

    action = definition.Actions.Create(TASK_ACTION_EXEC)
    action.Path = command
    # If you need arguments
    # action.Arguments = arguments

    folder.RegisterTaskDefinition(
        name,
        definition,
        TASK_CREATE_OR_UPDATE,
        NO_USER,
        NO_PASSWORD,
        TASK_LOGON_NONE
    )


def resolve_relative_path(path: str):
    return fr"{str(pathlib.Path(path).resolve())}"


def main():
    scheduler = win32com.client.Dispatch(TASK_SCHEDULE_SERVICE)
    scheduler.Connect()
    lock_command = resolve_relative_path("./test/register_task/lock.bat")
    unlock_command = resolve_relative_path("./test/register_task/unlock.bat")

    register_task(
        scheduler=scheduler,
        state_change=TASK_SESSION_LOCK,
        name="When Lock",
        command=lock_command
    )
    register_task(
        scheduler=scheduler,
        state_change=TASK_SESSION_UNLOCK,
        name="When unlock",
        command=unlock_command
    )


if __name__ == "__main__":
    main()
