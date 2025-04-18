#!/usr/bin/python3
try:
    from sys import exit, stdin, stdout, argv
    import os

    hush_login_path = os.path.expanduser("~/.hush_login")
    if os.path.isfile(hush_login_path) or not stdin.isatty():
        exit(0)

    hush_news_path = os.path.expanduser("~/.hush_news")
    hush_updates_path = os.path.expanduser("~/.hush_updates")
    hush_news = os.path.isfile(hush_news_path)
    hush_updates = os.path.isfile(hush_updates_path)

    import asyncio, platform, psutil, aiohttp, socket, json, signal
    from collections import Counter
    from pathlib import Path
    from datetime import datetime, timedelta
    from time import monotonic, time
except KeyboardInterrupt:
    import os

    os._exit(0)


def lc() -> None:
    print("\r\033[K", end="")


def handle_exit(signum, frame):
    # Clear current line for shell line
    lc()
    os._exit(0)


# Register signal handlers for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handle_exit)

sbc_list = [
    "ArmSoM AIM7 ",
    "ArmSoM Sige7",
    "ArmSoM W3",
    "Banana Pi M7",
    "Embedfire LubanCat-4",
    "Firefly AIO-3588L MIPI101(Linux)",
    "Firefly ITX-3588J HDMI(Linux)",
    "FriendlyElec CM3588",
    "FriendlyElec NanoPC-T6",
    "FriendlyElec NanoPC-T6 LTS",
    "FriendlyElec NanoPi R6C",
    "FriendlyElec NanoPi R6S",
    "Fxblox RK1",
    "Fydetab Duo",
    "HINLINK H88K",
    "Indiedroid Nova",
    "Khadas Edge2",
    "Mekotronics R58 MiniPC (RK3588 MINIPC LP4x V1.0 BlueBerry Board)",
    "Mekotronics R58X (RK3588 EDGE LP4x V1.0 BlueBerry Board)",
    "Mekotronics R58X-4G (RK3588 EDGE LP4x V1.2 BlueBerry Board)",
    "Mixtile Blade 3",
    "Mixtile Blade 3 v1.0.1",
    "Mixtile Core 3588E",
    "Orange Pi 5",
    "Orange Pi 5 Ultra" "Orange Pi 5 Max",
    "Orange Pi 5 Plus",
    "Orange Pi 5 Pro",
    "Orange Pi 5B",
    "Orange Pi CM5",
    "RK3588 CoolPi CM5 EVB Board",
    "RK3588 CoolPi CM5 NoteBook Board",
    "RK3588 EDGE LP4x V1.2 MeiZhuo BlueBerry Board",
    "RK3588 EDGE LP4x V1.4 BlueBerry Board",
    "RK3588 MINIPC-MIZHUO LP4x V1.0 BlueBerry Board",
    "RK3588S CoolPi 4B Board",
    "ROC-RK3588S-PC V12(Linux)",
    "Radxa CM5 IO",
    "Radxa CM5 RPI CM4 IO",
    "Radxa NX5 IO",
    "Radxa NX5 Module",
    "Radxa ROCK 5 ITX",
    "Radxa ROCK 5A",
    "Radxa ROCK 5B",
    "Radxa ROCK 5B Plus",
    "Radxa ROCK 5C",
    "Radxa ROCK 5D",
    "Rockchip RK3588",
    "Rockchip RK3588 EVB1 LP4 V10 Board",
    "Rockchip RK3588 EVB1 LP4 V10 Board + DSI DSC PANEL MV2100UZ1 DISPLAY Ext Board",
    "Rockchip RK3588 EVB1 LP4 V10 Board + RK Ext HDMImale to eDP V10",
    "Rockchip RK3588 EVB1 LP4 V10 Board + RK HDMI to DP Ext Board",
    "Rockchip RK3588 EVB1 LP4 V10 Board + RK3588 EDP 8LANES V10 Ext Board",
    "Rockchip RK3588 EVB1 LP4 V10 Board + Rockchip RK3588 EVB V10 Extboard",
    "Rockchip RK3588 EVB1 LP4 V10 Board + Rockchip RK628 HDMI to MIPI Extboard",
    "Rockchip RK3588 EVB2 LP4 V10 Board",
    "Rockchip RK3588 EVB2 LP4 V10 eDP Board",
    "Rockchip RK3588 EVB2 LP4 V10 eDP to DP Board",
    "Rockchip RK3588 EVB3 LP5 V10 Board",
    "Rockchip RK3588 EVB3 LP5 V10 EDP Board",
    "Rockchip RK3588 EVB4 LP4 V10 Board",
    "Rockchip RK3588 EVB6 LP4 V10 Board",
    "Rockchip RK3588 EVB7 LP4 V10 Board",
    "Rockchip RK3588 EVB7 LP4 V11 Board",
    "Rockchip RK3588 EVB7 V11 Board",
    "Rockchip RK3588 EVB7 V11 Board + Rockchip RK628 HDMI to MIPI Extboard",
    "Rockchip RK3588 NVR DEMO LP4 SPI NAND Board",
    "Rockchip RK3588 NVR DEMO LP4 V10 Android Board",
    "Rockchip RK3588 NVR DEMO LP4 V10 Board",
    "Rockchip RK3588 NVR DEMO1 LP4 V21 Android Board",
    "Rockchip RK3588 NVR DEMO1 LP4 V21 Board",
    "Rockchip RK3588 NVR DEMO3 LP4 V10 Android Board",
    "Rockchip RK3588 NVR DEMO3 LP4 V10 Board",
    "Rockchip RK3588 PCIE EP Demo V11 Board",
    "Rockchip RK3588 TOYBRICK LP4 X10 Board",
    "Rockchip RK3588 TOYBRICK X10 Board",
    "Rockchip RK3588 VEHICLE EVB V10 Board",
    "Rockchip RK3588 VEHICLE EVB V20 Board",
    "Rockchip RK3588 VEHICLE EVB V21 Board",
    "Rockchip RK3588 VEHICLE EVB V22 Board",
    "Rockchip RK3588 VEHICLE S66 Board V10",
    "Rockchip RK3588-RK1608 EVB7 LP4 V10 Board",
    "Rockchip RK3588J",
    "Rockchip RK3588M",
    "Rockchip RK3588S",
    "Rockchip RK3588S EVB1 LP4X V10 Board",
    "Rockchip RK3588S EVB2 LP5 V10 Board",
    "Rockchip RK3588S EVB3 LP4 V10 Board + Rockchip RK3588S EVB V10 Extboard",
    "Rockchip RK3588S EVB3 LP4 V10 Board + Rockchip RK3588S EVB V10 Extboard1",
    "Rockchip RK3588S EVB3 LP4 V10 Board + Rockchip RK3588S EVB V10 Extboard2",
    "Rockchip RK3588S EVB3 LP4X V10 Board",
    "Rockchip RK3588S EVB4 LP4X V10 Board",
    "Rockchip RK3588S EVB8 LP4X V10 Board",
    "Rockchip RK3588S TABLET RK806 SINGLE Board",
    "Rockchip RK3588S TABLET V10 Board",
    "Rockchip RK3588S TABLET V11 Board",
    "Turing Machines RK1",
]


def hw_impl_id_to_vendor(impl_id: int) -> str:
    vendors = {
        0x41: "ARM",
        0x42: "Broadcom",
        0x43: "Cavium",
        0x44: "DEC",
        0x46: "FUJITSU",
        0x48: "HiSilicon",
        0x49: "Infineon",
        0x4D: "Motorola",
        0x4E: "NVIDIA",
        0x50: "APM",
        0x51: "Qualcomm",
        0x53: "Samsung",
        0x56: "Marvell",
        0x61: "Apple",
        0x66: "Faraday",
        0x69: "Intel",
        0x6D: "Microsoft",
        0x70: "Phytium",
        0xC0: "Ampere",
    }
    return vendors.get(impl_id, "Unknown")


def arm_part_id_to_name(part_id: int) -> str:
    arm_parts = {
        0x810: "ARM810",
        0x920: "ARM920",
        0x922: "ARM922",
        0x926: "ARM926",
        0x940: "ARM940",
        0x946: "ARM946",
        0x966: "ARM966",
        0xA20: "ARM1020",
        0xA22: "ARM1022",
        0xA26: "ARM1026",
        0xB02: "ARM11 MPCore",
        0xB36: "ARM1136",
        0xB56: "ARM1156",
        0xB76: "ARM1176",
        0xC05: "Cortex-A5",
        0xC07: "Cortex-A7",
        0xC08: "Cortex-A8",
        0xC09: "Cortex-A9",
        0xC0D: "Cortex-A17",  # Originally A12
        0xC0F: "Cortex-A15",
        0xC0E: "Cortex-A17",
        0xC14: "Cortex-R4",
        0xC15: "Cortex-R5",
        0xC17: "Cortex-R7",
        0xC18: "Cortex-R8",
        0xC20: "Cortex-M0",
        0xC21: "Cortex-M1",
        0xC23: "Cortex-M3",
        0xC24: "Cortex-M4",
        0xC27: "Cortex-M7",
        0xC60: "Cortex-M0+",
        0xD01: "Cortex-A32",
        0xD02: "Cortex-A34",
        0xD03: "Cortex-A53",
        0xD04: "Cortex-A35",
        0xD05: "Cortex-A55",
        0xD06: "Cortex-A65",
        0xD07: "Cortex-A57",
        0xD08: "Cortex-A72",
        0xD09: "Cortex-A73",
        0xD0A: "Cortex-A75",
        0xD0B: "Cortex-A76",
        0xD0C: "Neoverse-N1",
        0xD0D: "Cortex-A77",
        0xD0E: "Cortex-A76AE",
        0xD13: "Cortex-R52",
        0xD15: "Cortex-R82",
        0xD16: "Cortex-R52+",
        0xD20: "Cortex-M23",
        0xD21: "Cortex-M33",
        0xD22: "Cortex-M55",
        0xD23: "Cortex-M85",
        0xD40: "Neoverse-V1",
        0xD41: "Cortex-A78",
        0xD42: "Cortex-A78AE",
        0xD43: "Cortex-A65AE",
        0xD44: "Cortex-X1",
        0xD46: "Cortex-A510",
        0xD47: "Cortex-A710",
        0xD48: "Cortex-X2",
        0xD49: "Neoverse-N2",
        0xD4A: "Neoverse-E1",
        0xD4B: "Cortex-A78C",
        0xD4C: "Cortex-X1C",
        0xD4D: "Cortex-A715",
        0xD4E: "Cortex-X3",
        0xD4F: "Neoverse-V2",
        0xD80: "Cortex-A520",
        0xD81: "Cortex-A720",
        0xD82: "Cortex-X4",
        0xD84: "Neoverse-V3",
        0xD85: "Cortex-X925",
        0xD87: "Cortex-A725",
    }
    return arm_parts.get(part_id, "Unknown")


def get_active_ipv4_interfaces() -> dict:
    active_interfaces = {}
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if (
                addr.family == socket.AF_INET
                and addr.address != "127.0.0.1"
                and not iface.startswith(("br-", "docker", "virbr"))
            ):
                active_interfaces[iface] = addr.address
    return active_interfaces


async def get_system_info() -> dict:
    hostname = platform.node()
    os_info = f"GNU/Linux {platform.release()} {platform.machine()}"

    uptime_seconds = int(psutil.boot_time())
    uptime = datetime.now() - datetime.fromtimestamp(uptime_seconds)
    days, seconds = uptime.days, uptime.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    uptime_str = ""
    if days:
        uptime_str += f"{days} days"
        if hours:
            uptime_str += f" {hours} hours"
        if minutes:
            uptime_str += f" {minutes} minutes"
    elif hours:
        uptime_str += f"{hours} hours"
        if minutes:
            uptime_str += f" {minutes} minutes"
    elif minutes:
        uptime_str += f"{minutes} minutes"
    else:
        uptime_str += "seconds"

    cpu_model = None

    with open("/proc/cpuinfo", "r") as f:
        cpuinfo = f.read()
        cpuinfo = cpuinfo.splitlines()

    for line in cpuinfo:
        if "cpu model" in line or "model name" in line:
            cpu_model = line.split(":", 1)[1].strip()
            break

    if cpu_model is None:
        cpu_implementer = None
        cpu_part = None
        for line in cpuinfo:
            if "CPU implementer" in line:
                cpu_implementer = int(line.split(":")[1].strip(), 16)
            elif "CPU part" in line:
                cpu_part = int(line.split(":")[1].strip(), 16)

            if cpu_implementer is not None and cpu_part is not None:
                break

        vendor = hw_impl_id_to_vendor(cpu_implementer)
        part_name = arm_part_id_to_name(cpu_part)

        cpu_model = f"{vendor} {part_name}"

    cpu_count = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)

    mem = psutil.virtual_memory()
    total_memory = f"{mem.total // (1024**2)} MB"

    with open("/proc/loadavg") as f:
        load_avg = f.read().split()[0]

    with open("/proc/stat") as f:
        processes = sum(1 for line in f if line.startswith("processes"))

    disk_usage = os.statvfs("/")
    total_space = disk_usage.f_frsize * disk_usage.f_blocks / (1024**3)  # GB
    used_space = (
        (disk_usage.f_blocks - disk_usage.f_bfree) * disk_usage.f_frsize / (1024**3)
    )  # GB
    usage_percent = (used_space / total_space) * 100

    logged_in_users = 0
    try:
        users_process = await asyncio.create_subprocess_exec(
            "who",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await users_process.communicate()
        seen_users = set()
        lines = stdout.decode().split("\n")
        lines.pop()
        for i in lines:
            user = i.split(" ")[0]
            if user not in seen_users:
                seen_users.add(user)
        logged_in_users = len(seen_users)
    except:
        pass

    with open("/proc/meminfo") as f:
        meminfo = {line.split(":")[0]: int(line.split()[1]) for line in f}
    mem_usage_percent = (
        (meminfo["MemTotal"] - meminfo["MemAvailable"]) / meminfo["MemTotal"] * 100
    )

    swap_usage_percent = (
        (100 - (meminfo["SwapFree"] / meminfo["SwapTotal"] * 100))
        if meminfo["SwapTotal"] > 0
        else None
    )

    net_ifs = get_active_ipv4_interfaces()

    return {
        "system_load": load_avg,
        "processes": processes,
        "hostname": hostname,
        "uptime": uptime_str,
        "cpu_model": cpu_model,
        "cpu_count": cpu_count,
        "cpu_threads": cpu_threads,
        "os_info": os_info,
        "total_memory": total_memory,
        "disk_usage": f"{usage_percent:.1f}% of {total_space:.2f}GB",
        "logged_in_users": logged_in_users,
        "memory_usage": f"{mem_usage_percent:.1f}%",
        "net_ifs": net_ifs,
        "swap_usage": (
            f"{swap_usage_percent:.1f}%" if swap_usage_percent is not None else None
        ),
    }


async def get_service_statuses(command: str):
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    statuses = [
        line.strip()
        for line in stdout.decode().strip().split("\n")
        if line and line not in ["running", "exited", "dead"]
    ]
    return Counter(statuses)


async def count_failed_systemd() -> dict:
    system_statuses = await get_service_statuses(
        "systemctl list-units --type=service --no-legend --no-pager | awk '{print $4}'"
    )
    user_statuses = await get_service_statuses(
        "systemctl --user list-units --type=service --no-legend --no-pager | awk '{print $4}'"
    )

    total_statuses = system_statuses + user_statuses
    total_count = sum(total_statuses.values())

    return {"total": total_count, "breakdown": dict(total_statuses)}


async def get_updates():
    if hush_updates:
        return  # Do not do anything
    try:
        process = await asyncio.create_subprocess_exec(
            "checkupdates",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            preexec_fn=lambda: os.nice(20),  # Maximum priority
        )

        try:
            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=8)
        except asyncio.TimeoutError:
            process.kill()
            return

        updates = stdout.decode().strip().split("\n")
        updates = [line for line in updates if line]

        return len(updates) if updates else 0

    except FileNotFoundError:
        return "Install `pacman-contrib` to view available updates during login."
    except Exception:
        return


async def get_devel_updates():
    if hush_updates:
        return  # Do not do anything
    try:
        process = await asyncio.create_subprocess_exec(
            "yay",
            "-Qua",
            "--devel",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            preexec_fn=lambda: os.nice(20),  # Maximum priority
        )

        try:
            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=8)
        except asyncio.TimeoutError:
            process.kill()
            return

        updates = stdout.decode().strip().split("\n")
        updates = [line for line in updates if line]  # Remove empty lines

        return len(updates) if updates else 0

    except FileNotFoundError:
        return "Install `yay` to view development package updates during login."
    except Exception:
        return None


async def fetch_news():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://raw.githubusercontent.com/BredOS/news/refs/heads/main/notice.txt",
                timeout=5,
            ) as response:
                response.raise_for_status()
                return await response.text()
    except:
        return False


def detect_install_device() -> str:
    try:
        with open("/sys/firmware/devicetree/base/model", "r") as model_file:
            device = model_file.read().rstrip("\n").rstrip("\x00")
            return device
    except FileNotFoundError:
        try:
            with open("/sys/class/dmi/id/product_name", "r") as product_name_file:
                device = product_name_file.read().rstrip("\n")
                return device
        except FileNotFoundError:
            return "unknown"


def seperator(current_str: str, collumns: int) -> None:
    print((" " * (collumns - len(current_str) + 2)) + "   ", end="")


class colors:
    # Main
    okay = "\033[92m"
    warning = "\033[93m"
    error = "\033[91m"

    # Styling
    underline = "\033[4m"
    bold = "\033[1m"
    endc = "\033[0m"  # use to reset

    # Okay
    okblue = "\033[94m"
    okcyan = "\033[96m"

    # Coloured Text
    black_t = "\033[30m"
    red_t = "\033[31m"
    green_t = "\033[32m"
    yellow_t = "\033[33m"
    blue_t = "\033[34m"
    magenta_t = "\033[35m"
    cyan_t = "\033[36m"
    white_t = "\033[37m"

    # Background
    white_bg_black_bg = "\033[38;5;0m\033[48;5;255m"
    inverse = "\033[7m"
    uninverse = "\033[27m"


clear_seq = "\x1b[2J\x1b[3J\x1b[H"


def cache_gen(update_str: str, news_str: str):
    data = {"timestamp": int(time()), "updates": update_str, "news": news_str}
    with open("/tmp/bredos-news." + str(os.geteuid()) + ".tmp", "w") as f:
        json.dump(data, f)


def fetch_cache():
    if not os.path.exists("/tmp/bredos-news." + str(os.geteuid()) + ".tmp"):
        return None

    with open("/tmp/bredos-news." + str(os.geteuid()) + ".tmp") as f:
        data = json.load(f)

    timestamp = data.get("timestamp")
    if timestamp is None:
        return None

    if datetime.now() - datetime.fromtimestamp(timestamp) <= timedelta(hours=6):
        return data.get("updates"), data.get("news")

    return None


async def main() -> None:
    args = set(argv[1:])
    if "--help" in args or "-h" in args:
        print("Wow..")
    elif "--clear" in args or "-c" in args:
        for file in Path("/tmp").glob("bredos-news*"):
            if file.is_file():
                file.unlink()
    else:
        silent = "--silent" in args or "-s" in args
        info_task = get_system_info()
        services_task = count_failed_systemd()

        devel_updates_task = None
        news_task = None
        updates_available = None
        devel_updates_available = None
        upd_str = None
        news = None

        cache_data = fetch_cache()
        if cache_data:
            upd_str = cache_data[0]
            news = cache_data[1]

        if not (hush_updates or upd_str):
            updates_task = get_updates()
            devel_updates_task = get_devel_updates()

        if not news:
            news_task = fetch_news()

        device = None
        sbc_declared = detect_install_device()
        if sbc_declared in sbc_list:
            device = sbc_declared

        system_info = await info_task

        if not silent:
            print(
                f"{clear_seq}{colors.yellow_t}{colors.bold}Welcome to BredOS{colors.endc} ({system_info['os_info']})"
            )
            print(
                f"{colors.yellow_t}{colors.bold}\n*{colors.endc} Documentation:  https://wiki.bredos.org/"
            )
            print(
                f"{colors.yellow_t}{colors.bold}*{colors.endc} Support:        https://discord.gg/beSUnWGVH2\n"
            )

        device_str = ""
        if device is not None:
            device_str += f"{colors.okblue}Device:{colors.endc} {device}"

        hostname_str = (
            f"{colors.okblue}Hostname:{colors.endc} {system_info['hostname']}"
        )

        uptime_str = f"{colors.okblue}Uptime:{colors.endc} {system_info['uptime']}"
        logged_str = f"{colors.okblue}Users logged in:{colors.endc} {system_info['logged_in_users']}"

        cpu_str = f"{colors.okblue}CPU:{colors.endc} {system_info['cpu_model']} ({system_info['cpu_count']}c, {system_info['cpu_threads']}t)"
        load_str = (
            f"{colors.okblue}System load:{colors.endc} {system_info['system_load']}"
        )

        memory_str = f"{colors.okblue}Memory:{colors.endc} {system_info['memory_usage']} of {system_info['total_memory']} used"

        swap_str = ""
        if system_info["swap_usage"] is not None:
            swap_str = (
                f"{colors.okblue}Swap usage:{colors.endc} {system_info['swap_usage']}"
            )

        collumns = max(len(device_str), len(uptime_str), len(cpu_str), len(memory_str))

        if not silent:
            print(device_str, end="")
            if device_str:
                seperator(device_str, collumns)
            print(hostname_str)

            print(uptime_str, end="")
            seperator(uptime_str, collumns)
            print(logged_str)

            print(cpu_str, end="")
            seperator(cpu_str, collumns)
            print(load_str)

            print(memory_str, end="")

            if swap_str:
                seperator(memory_str, collumns)
            print(swap_str)

            usage_str = (
                f"{colors.okblue}Usage of /:{colors.endc} {system_info['disk_usage']}"
            )
            print(usage_str, end="")
            splitter = True
            last = usage_str
            for netname, ip in system_info["net_ifs"].items():
                if splitter:
                    seperator(last, collumns)
                last = f"{colors.okblue}{netname}:{colors.endc} {ip}"
                print(last, end="")
                if splitter:
                    print()
                splitter = not splitter
            if splitter:
                print()

        if not hush_updates:
            if not upd_str:
                if not silent:
                    print("Checking for updates.. (Skip with Ctrl+C)", end="")
                    stdout.flush()
                updates_available = await updates_task
                devel_updates_available = await devel_updates_task
                if not silent:
                    lc()

                if updates_available is not None:
                    if isinstance(updates_available, str):
                        upd_str = f"\n{colors.bold}{colors.red_t}{updates_available}{colors.endc}"
                    if isinstance(devel_updates_available, str):
                        upd_str = f"\n{colors.bold}{colors.red_t}{devel_updates_available}{colors.endc}"
                    uisn = isinstance(updates_available, int)
                    disn = isinstance(devel_updates_available, int)
                    if updates_available and uisn:
                        if devel_updates_available and disn:
                            upd_str = f"\n{colors.bold}{colors.cyan_t}{updates_available+devel_updates_available} packages can be upgraded, of which {devel_updates_available} are development packages.{colors.endc}\n"
                        else:
                            upd_str = f"\n{colors.bold}{colors.cyan_t}{updates_available} packages can be upgraded.{colors.endc}\n"
                    elif devel_updates_available and disn:
                        upd_str = f"\n{colors.bold}{colors.cyan_t}{devel_updates_available} development packages can be upgraded.{colors.endc}\n"
                    else:
                        upd_str = (
                            f"\n{colors.green_t}You are up to date!{colors.endc}\n"
                        )
                elif (not hush_updates) and not silent:
                    print("\nTimed out waiting for updates.")

            if upd_str and not silent:
                print(upd_str, end="")

        if not silent:
            print()

        if not hush_news:
            if not news:
                if not silent:
                    print("Fetching news.. (Skip with Ctrl+C)", end="")
                    stdout.flush()
                news = await news_task
                if not silent:
                    lc()

            if not silent:
                print(news if news else "Failed to fetch news.")

        if not news:
            news = ""
        if not upd_str:
            upd_str = ""

        if (
            (not cache_data)
            or (upd_str and not cache_data[0])
            or (news and not cache_data[1])
        ):
            cache_gen(upd_str, news)

        services = await services_task
        if not silent:
            if not services["total"]:
                print(
                    f"{colors.bold}{colors.green_t}System is operating normally.{colors.endc}"
                )
            else:
                for i in services["breakdown"].keys():
                    n = services["breakdown"][i]
                    if i == "failed":
                        print(
                            f"{colors.bold}{colors.red_t}{n}{colors.endc} services have {colors.bold}{colors.red_t}{i}{colors.endc}"
                        )
                    else:
                        print(
                            f'{colors.bold}{colors.yellow_t}{n}{colors.endc} services report status {colors.bold}{colors.yellow_t}"{i}"{colors.endc}'
                        )

        # Clean current line
        lc()

        # Just quit hard, asyncio is horrible
        os._exit(0)


if __name__ == "__main__":
    asyncio.run(main())
