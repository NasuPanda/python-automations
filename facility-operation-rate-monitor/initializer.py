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


def register_task(scheduler, state_change: int, name: str, command: str, priority: int = 7):
    """Register task to windows task scheduler.

    Parameters
    ----------
    scheduler
        win32client TaskScheduler object.
    state_change : int
        State change enum.
    name : str
        Task name.
    command : str
        Executed task command path.
    """
    folder = scheduler.GetFolder("\\")

    definition = scheduler.NewTask(0)

    # Set trigger
    trigger = definition.Triggers.Create(TASK_TRIGGER_SESSION_STATE_CHANGE)
    trigger.StateChange = state_change

    # Set priority
    definition.Settings.Priority = priority

    # Set executed action
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


def resolve_relative_path(relative_path: str) -> str:
    """Relative path to absolute path.

    Parameters
    ----------
    relative_path : str
        Relative path.

    Returns
    -------
    str
        Resolved absolute path.
    """
    return fr"{str(pathlib.Path(relative_path).resolve())}"


def main():
    """Main function.
    """
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
