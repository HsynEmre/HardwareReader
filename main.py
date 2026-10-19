import tkinter as tk
import psutil
import cpuinfo
import GPUtil
import subprocess
import time
import customtkinter as ctk


# Window ayarları
ctk.set_appearance_mode("dark")
window = ctk.CTk()
window.title("Hardware Reader")
window.geometry("800x800")
window.configure(fg_color="#080D1B")
# Ana pencerenin 0. ve 1. sütunlarının yatayda esnemesine izin ver
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Ana pencerenin 0. ve 1. satırlarının dikeyde esnemesine izin ver
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
#Header Box
header_frame = ctk.CTkFrame(
    master=window,
    fg_color="#111C35",
    corner_radius=15,
    border_width=1,
    border_color="#23365B"
)
header_frame.grid(row=0, column=0, columnspan=2,padx=20, pady=20, sticky="ew")

# CPU Box
cpu_frame = ctk.CTkFrame(
    master=window,
    fg_color="#111C35",
    corner_radius=15,
    border_width=1,
    border_color="#23365B"
)
cpu_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
#GPU Box
gpu_frame = ctk.CTkFrame(
    master=window,
    fg_color="#111C35",
    corner_radius=15,
    border_width=1,
    border_color="#23365B"
)
gpu_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
#Disk Box
disk_frame = ctk.CTkFrame(
    master=window,
    fg_color="#111C35",
    corner_radius=15,
    border_width=1,
    border_color="#23365B"
)
disk_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
#RAM Box
ram_frame = ctk.CTkFrame(
    master=window,
    fg_color="#111C35",
    corner_radius=15,
    border_width=1,
    border_color="#23365B"
)
ram_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
#Header bilgileri
header_name_label = ctk.CTkLabel(
    master=header_frame,
    text=f"Hardware Reader",
    font=("Arial", 28, "bold"),
)
header_name_label.pack(anchor="w", pady=30,padx=15)
# İşlemci bilgileri
cpu = cpuinfo.get_cpu_info()
lbl_title = ctk.CTkLabel(
    master=cpu_frame, text="CPU", font=("Arial", 28, "bold")
)
lbl_title.pack(anchor="w", padx=20, pady=20)
cpu_name_label = ctk.CTkLabel(
    master=cpu_frame,
    text=f"CPU: {cpu['brand_raw']}",
    text_color="#9ca3af"
)
cpu_name_label.pack(anchor="w", pady=5,padx=15)

cpu_usage_label = ctk.CTkLabel(
    master=cpu_frame,
    text="CPU kullanımı ölçülüyor...",
    text_color="#9ca3af"
)
cpu_usage_label.pack(anchor="w", pady=5,padx=15)
cpu_physicalMemory_label = ctk.CTkLabel(
    cpu_frame,
    text=f"Fiziksel Çekirdek Sayısı : {psutil.cpu_count(logical=False)}",
    text_color="#9ca3af"
)
cpu_physicalMemory_label.pack(anchor="w", pady=5,padx=15)

cpu_ThreadMemory_label = ctk.CTkLabel(
    cpu_frame,
    text=f"Mantıksal Çekirdek (Thread): {psutil.cpu_count(logical=True)}",
    text_color="#9ca3af"
)
cpu_ThreadMemory_label.pack(anchor="w", pady=5,padx=15)

def cpuInfo():
    usage = psutil.cpu_percent(interval=None)

    cpu_usage_label.configure(
        text=f"CPU kullanımı: %{usage}"
    )

    window.after(1000, cpuInfo)

#GPU bilgileri
gpus = GPUtil.getGPUs()
gpu = gpus[0]
lbl_title = ctk.CTkLabel(
    master=gpu_frame, text="GPU", font=("Arial", 28, "bold")
)
lbl_title.pack(anchor="w", padx=20, pady=20)
if not gpus:
    print("Gpubulunmamaktadır")
else:
    gpu_name_label = ctk.CTkLabel(
        master=gpu_frame,
        text=f"GPU: {gpu.name}",
        text_color="#9ca3af"
    )
    gpu_name_label.pack(anchor="w", pady=5, padx=15)
    gpu_usage_label = ctk.CTkLabel(
        gpu_frame,
        text=f"GPU Ölçüşüyor",
        text_color="#9ca3af"
    )
    gpu_usage_label.pack(anchor="w", pady=5, padx=15)
    gpu_temperature_label = ctk.CTkLabel(
        gpu_frame,
        text=f"GPU Sıcaklığı",
        text_color="#9ca3af"
    )
    gpu_temperature_label.pack(anchor="w", pady=5, padx=15)
def gpuInfo():
    gpus = GPUtil.getGPUs()
    gpu = gpus[0]
    if not gpus:
        print("YOK")
    else:
        usage = f"{gpu.load * 100:.1f}"
        temperature = gpu.temperature
        gpu_usage_label.configure(
            text=f"GPU kullanımı: {usage}",
        )
        gpu_temperature_label.configure(
            text=f"Gpu Sıcaklığı : {temperature} °C"
        )

    window.after(1000, gpuInfo)
#Disk bilgileri
last_io = psutil.disk_io_counters()
last_time = time.time()


komut = "powershell \"Get-CimInstance Win32_DiskDrive | Select-Object -ExpandProperty Model\""
cikti = subprocess.check_output(komut, shell=True).decode("utf-8", errors="ignore").strip()
lbl_title = ctk.CTkLabel(
    master=disk_frame, text="Disk", font=("Arial", 28, "bold")
)
lbl_title.pack(anchor="w", padx=20, pady=20)
disk_name_label = ctk.CTkLabel(
    disk_frame,
    text=f"Disk : {cikti}",
    text_color="#9ca3af"
)
disk_name_label.pack(anchor="w", pady=5,padx=15)
disk = psutil.disk_usage('/')
disk_total_label = ctk.CTkLabel(
    disk_frame,
    text=f"Disk alanı: {disk.total / (1024 ** 3):.2f} GB",
    text_color="#9ca3af"
)
disk_total_label.pack(anchor="w", pady=5,padx=15)
disk_free_label = ctk.CTkLabel(
    disk_frame,
    text=f"DBoş disk alanı: {disk.free / (1024 ** 3):.2f} GB",
    text_color="#9ca3af"
)
disk_free_label.pack(anchor="w", pady=5,padx=15)
disk_percentage_label = ctk.CTkLabel(
    disk_frame,
    text=f"Disk doluluk oranı: {disk.percent:.2f} %",
    text_color="#9ca3af"
)
disk_percentage_label.pack(anchor="w", pady=5,padx=15)
disk_write_label = ctk.CTkLabel(
    disk_frame, text="Yazma Hızı : 0.00 MB/s", text_color="#9ca3af"
)
disk_write_label.pack(anchor="w", pady=5,padx=15)
disk_read_label = ctk.CTkLabel(
    disk_frame, text="Okuma Hızı : 0.00 MB/s", text_color="#9ca3af"
)
disk_read_label.pack(anchor="w", pady=5,padx=15)

def diskInfo():
    global last_io, last_time

    current_io = psutil.disk_io_counters()
    current_time = time.time()

    elapsed = current_time - last_time

    if elapsed > 0:
        # Doğru MB/s hesaplama formülü
        read_speed = (current_io.read_bytes - last_io.read_bytes) / (
                1024 * 1024 * elapsed
        )
        write_speed = (current_io.write_bytes - last_io.write_bytes) / (
                1024 * 1024 * elapsed
        )

        disk_read_label.configure(text=f"Okuma Hızı : {read_speed:.2f} MB/s")
        disk_write_label.configure(text=f"Yazma Hızı : {write_speed:.2f} MB/s")

        last_io = current_io
        last_time = current_time

    window.after(1000, diskInfo)

#RAM bilgileri
komut = 'powershell "(Get-CimInstance Win32_PhysicalMemory).Speed"'
ram_hizi = subprocess.check_output(komut, shell=True).decode("utf-8", errors="ignore").strip()
# 1. Toplam slot sayısını al
komut_toplam = (
    'powershell "(Get-CimInstance Win32_PhysicalMemoryArray).MemoryDevices"'
)
toplam_slot = int(
    subprocess.check_output(komut_toplam, shell=True)
    .decode("utf-8", errors="ignore")
    .strip()
)
# 2. Takılı (dolu) slot sayısını doğrudan saydır
komut_dolu = (
    'powershell "(Get-CimInstance Win32_PhysicalMemory | Measure-Object).Count"'
)
dolu_slot = int(
    subprocess.check_output(komut_dolu, shell=True)
    .decode("utf-8", errors="ignore")
    .strip()
)
# 3. Boş slotu hesapla
bos_slot = toplam_slot - dolu_slot
ram = psutil.virtual_memory()
lbl_title = ctk.CTkLabel(
    master=ram_frame, text="RAM", font=("Arial", 28, "bold")
)
lbl_title.pack(anchor="w", padx=20, pady=20)
ram_total_label = ctk.CTkLabel(
    ram_frame,
    text=f"RAM: {ram.total / (1024 ** 3):.2f} GB",
    text_color="#9ca3af"
)
ram_total_label.pack(anchor="w", pady=5,padx=15)
ram_slot_label = ctk.CTkLabel(
    ram_frame,
    text=f"RAM slot: {toplam_slot} ",
    text_color="#9ca3af"
)
ram_slot_label.pack(anchor="w", pady=5,padx=15)
ram_freeslot_label = ctk.CTkLabel(
    ram_frame,
    text=f"Boş ram slot: {bos_slot} ",
    text_color="#9ca3af"
)
ram_freeslot_label.pack(anchor="w", pady=5,padx=15)
ram_speed_label = ctk.CTkLabel(
    ram_frame,
    text=f"RAM speed: {ram_hizi}",
    text_color="#9ca3af"
)
ram_speed_label.pack(anchor="w", pady=5,padx=15)
# İlk ölçüm için başlangıç

cpuInfo()
gpuInfo()
diskInfo()
window.mainloop()