import subprocess
import ctypes


# Disable the System32/SysWOW64 file system redirection.
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))

    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


if __name__ == "__main__":
    drive_is_encrypted = False
    bit_locker_drive = "Z:"
    command_pattern = "C:\\Windows\\System32\\manage-bde.exe -unlock -recoverypassword {0} " + bit_locker_drive
    numeric_plain_recovery_key = 0

    with disable_file_system_redirection():
        while drive_is_encrypted is not True:
            # Build the recovery key
            pw = str(numeric_plain_recovery_key).zfill(48)
            recovery_key = pw[0:6] + '-' + pw[6:12] + '-' + pw[12:18] + '-' + pw[18:24] + '-' + pw[24:30] + '-' + pw[30:36] + '-' + pw[ 36:42] + '-' + pw[42:48]
            # Build the command
            command = command_pattern.format(recovery_key)
            # Try the recovery_key
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                drive_is_encrypted = True
                print(recovery_key)


# Code snippets
"""
if __name__ == "__main__":
    numeric_password_plain = 0
    numeric_password_faster = 100000100000100000100000100000100000100000100000

    for _ in range(0, 10):
        pw = str(numeric_password_faster + _ ).zfill(48)
        recovery_key = pw[0:6] + '-' + pw[6:12] + '-' + pw[12:18] + '-' + pw[18:24] + '-' + pw[24:30] + '-' + pw[30:36] + '-' + pw[36:42] + '-' + pw[42:48]
        print(recovery_key)
        
    #process = subprocess.Popen((path), shell=True, stdout=subprocess.PIPE)
    #process.wait()
    #print(process.returncode)

"""