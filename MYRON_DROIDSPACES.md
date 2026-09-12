# Redmi K90 Pro Max (`myron`) Droidspaces-only GKI

This branch builds a minimal 4 KiB-page Android 16 GKI for the Redmi K90 Pro
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
metadata and the effective source `gki_defconfig`.

## Before flashing

Back up the boot image from both slots, keep the original ROM package available,
and verify that the running stock kernel is still:

```text
6.12.69-android16-6-*-4k
```

Do not use this artifact on the older `6.12.23-android16-5` firmware. Prefer a
temporary `fastboot boot` test when the bootloader implementation supports it.
AnyKernel3 support and the correct boot partition must be confirmed on the
specific HyperOS build before flashing.

After booting, verify:

```sh
uname -a
su -c 'zcat /proc/config.gz | grep -E "CONFIG_(PID_NS|IPC_NS|SYSVIPC|POSIX_MQUEUE)="'
su -c 'unshare --pid --fork --mount-proc sh -c "echo PID=\$\$"'
su -c 'unshare --ipc sh -c ipcs'
```
