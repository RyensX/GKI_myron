# Redmi K90 Pro Max (`myron`) Droidspaces-only GKI

This branch builds a candidate 4 KiB-page Android 16 GKI for the Redmi K90 Pro
Max / POCO F8 Ultra (`myron`). It is intended for devices already using
KernelSU in LKM mode.

## What is included

- Android common kernel tag `android16-6.12-2026-03_r62`
- Linux `6.12.69`, KMI `6.12-android16-6`
- Droidspaces' mandatory 6.12 SYSVIPC kABI patch
- PID, IPC and user namespaces plus the filesystem options Droidspaces needs

## What is deliberately excluded

- Built-in KernelSU or KernelSU-Next
- SUSFS and NoMount
- Scheduler, performance and networking tuning patches
- Device-specific source changes

The existing KernelSU LKM remains responsible for root. Reinstalling its LKM
may be necessary after changing the kernel Image.

注意：r62 是候选基线，尚未证明与原厂版本中的 b1493ec68d4a 对应。
完整云端编译、厂商模块兼容性和实机启动仍需验证。相同 KMI 字符串
不能独立证明 ABI 或现有 KernelSU LKM 可用。

The workflow pins the `kernel/common` checkout to commit
`e2b8ca7c8d0551a6124b1a7322f5ae532845f1b5` and fails if the tag resolves to
anything else. It also rejects an output whose embedded release string does not
contain `6.12.69-android16-6`.

## Build with GitHub Actions

1. Push this branch to a GitHub repository or fork.
2. Open **Actions**.
3. Select **Build myron Droidspaces-only GKI**.
4. Choose **Run workflow**.
5. Download `myron-droidspaces-6.12.69-android16-6-4k` from the run's artifacts.

The artifact contains the raw `Image`, an AnyKernel3 ZIP, checksums, build
metadata, the source `gki_defconfig`, and `kernel.config` extracted from Image.
All repo projects are pinned in `myron/locked.xml`; Droidspaces and AnyKernel3
are pinned separately. The resolved manifest is saved with the output.
This pins source inputs, not the entire runner OS or all third-party Actions.
Run `sha256sum -c SHA256SUMS` inside the extracted artifact directory.

## Before flashing

Back up the boot image from both slots, keep the original ROM package available,
and verify that the running stock kernel is still:

```text
6.12.69-android16-6-*-4k
```

Do not use this artifact on the older `6.12.23-android16-5` firmware.
The installer requires a normally booted Android environment, device myron,
kernel 6.12.69-android16-6 and verified 4096-byte pages. Recovery installs are
rejected because the recovery kernel does not identify the installed OS kernel.
A raw Image or AnyKernel3 ZIP cannot be passed directly to `fastboot boot`;
temporary boot testing requires a correctly repacked boot image first.
AnyKernel3 support and the correct boot partition must be confirmed on the
specific HyperOS build before flashing.

After booting, verify:

```sh
uname -a
su -c 'zcat /proc/config.gz | grep -E "CONFIG_(PID_NS|IPC_NS|SYSVIPC|POSIX_MQUEUE)="'
su -c 'unshare --pid --fork --mount-proc sh -c "echo PID=\$\$"'
su -c 'unshare --ipc sh -c ipcs'
```
