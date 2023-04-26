"""Application initialization script.

NOTE: Please execute this script as an administrator.

reference: https://github.com/aikige/homeBinWin/blob/master/setup/prepLockLogging.py
"""
import os
import pathlib
import win32com.client
from pywintypes import com_error

from config import config


def resolve_relative_path(path: str):
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
    return fr"{str(pathlib.Path(path).resolve())}"


# win32api enumerations
TASK_SCHEDULE_SERVICE = "Schedule.Service"
TASK_TRIGGER_SESSION_STATE_CHANGE = 11
TASK_ACTION_EXEC = 0
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0
NO_USER = ""
NO_PASSWORD = ""

TASK_SESSION_LOCK = 7
TASK_SESSION_UNLOCK = 8

# command path
LOCK_COMMAND = resolve_relative_path(config.LOCK_TASK_BAT_FILE)
UNLOCK_COMMAND = resolve_relative_path(config.UNLOCK_TASK_BAT_FILE)


def register_task(scheduler, state_change, name, command):
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


def main():
    """Main function.
    """
    scheduler = win32com.client.Dispatch(TASK_SCHEDULE_SERVICE)
    scheduler.Connect()

    register_task(
        scheduler=scheduler,
        state_change=TASK_SESSION_LOCK,
        name="FacilityMonitorStop",
        command=LOCK_COMMAND
    )
    register_task(
        scheduler=scheduler,
        state_change=TASK_SESSION_UNLOCK,
        name="FacilityMonitorExec",
        command=UNLOCK_COMMAND
    )

    os.makedirs(config.LOG_FOLDER, exist_ok=True)


if __name__ == "__main__":
    try:
        print("セットアップ中...\n")

        main()

        print("セットアップに成功しました。")
        print(f"ロック時のタスクに登録しました: {LOCK_COMMAND}")
        print(f"アンロック時のタスクに登録しました: {UNLOCK_COMMAND}")
        print(f"ログファイルを保存するフォルダを作成しました: {config.LOG_FOLDER}")
    except com_error as e:
        with open("../setup_debug_log.txt", "w") as f:
            print("win32apiのエラーによりセットアップに失敗しました。\nsetup_debug_log.txtを参照して下さい。")
            f.write(str(e))
        print("ヒント: 管理者として実行していない可能性があります。")
    except Exception as e:
        with open("../setup_debug_log.txt", "w") as f:
            print("不明な例外によりセットアップに失敗しました。\n[setup_debug_log.txt]を参照して下さい。")
            f.write(str(e))
