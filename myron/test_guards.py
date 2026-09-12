"""覆盖父子进程传参、拒绝条件和未知安装模板。仅使用临时目录。"""
import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent


class Guards(unittest.TestCase):
    def test_installer(self):
        cases = [
            ("true", "myron", "6.12.69-android16-6-test", "4096", True),
            ("false", "myron", "6.12.69-android16-6-test", "4096", False),
            ("", "myron", "6.12.69-android16-6-test", "4096", False),
            ("true", "pudding", "6.12.69-android16-6-test", "4096", False),
            ("true", "myron", "6.12.69-android16-5-test", "4096", False),
            ("true", "myron", "6.12.69-android16-60-test", "4096", False),
            ("true", "myron", "6.12.69-android16-6-test", "16384", False),
            ("true", "myron", "6.12.69-android16-6-test", "", False),
        ]
        for boot, device, kernel, page, ok in cases:
            with self.subTest(boot=boot, device=device, kernel=kernel, page=page):
                with tempfile.TemporaryDirectory() as directory:
                    root = pathlib.Path(directory)
                    entry = root / "META-INF/com/google/android/update-binary"
                    entry.parent.mkdir(parents=True)
                    entry.write_text('BOOTMODE="$TEST_BOOT"; ash anykernel.sh;\n')
                    script = root / "anykernel.sh"
                    script.write_text(
                        "# do.devicecheck=0\n# device.name1=\n"
                        'abort() { exit 1; }; split_boot() { echo WRITE_REACHED; };\n'
                        'getprop() { echo "$TEST_DEVICE"; }; uname() { echo "$TEST_KERNEL"; };\n'
                        'getconf() { echo "$TEST_PAGE"; };\n'
                        "# boot install\nsplit_boot\n"
                    )
                    (root / "check-device.sh").write_text((ROOT / "check-device.sh").read_text())
                    subprocess.run(["python3", str(ROOT / "guard-installer.py"), str(script)], check=True)
                    env = dict(os.environ, AKHOME=directory, TEST_BOOT=boot,
                               TEST_DEVICE=device, TEST_KERNEL=kernel, TEST_PAGE=page)
                    env.pop("BOOTMODE", None)
                    # 用独立 sh 进程模拟 ash，而不是同 shell source。
                    command = 'ash() { sh "$@"; }; . "$1"'
                    result = subprocess.run(["sh", "-c", command, "test", str(entry)],
                                            cwd=root, env=env, text=True, capture_output=True)
                    self.assertEqual(result.returncode == 0, ok)
                    self.assertEqual("WRITE_REACHED" in result.stdout, ok)
                    result = subprocess.run(["python3", str(ROOT / "guard-installer.py"), str(script)],
                                            capture_output=True)
                    self.assertNotEqual(result.returncode, 0)

    def test_config(self):
        keys = "PID_NS IPC_NS SYSVIPC POSIX_MQUEUE DEVTMPFS USER_NS MODULES ARM64_4K_PAGES IKCONFIG".split()
        good = "".join(f"CONFIG_{key}=y\n" for key in keys)
        cases = [(good, True), (good + "CONFIG_KSU=y\n", False),
                 (good + "CONFIG_KSU_SUSFS=m\n", False),
                 (good + "CONFIG_ARM64_16K_PAGES=y\n", False)]
        cases += [(good.replace(f"CONFIG_{key}=y\n", ""), False) for key in keys]
        for text, ok in cases:
            with tempfile.NamedTemporaryFile(mode="w") as config:
                config.write(text)
                config.flush()
                result = subprocess.run(["bash", str(ROOT / "verify-config.sh"), config.name],
                                        capture_output=True)
                self.assertEqual(result.returncode == 0, ok)


if __name__ == "__main__":
    unittest.main()
