## esxi build
```powershell
Install-Module -Name VMware.PowerCLI -RequiredVersion 12.4.0.18633274
Set-ExecutionPolicy RemoteSigned

$esxiOfflineBundle = "C:\Users\bruce\Desktop\esxi\VMware-ESXi-7.0U3d-19482537-depot.zip"
$intelNicOfflineBundle = "C:\Users\bruce\Desktop\esxi\Net-Community-Driver_1.2.7.0-1vmw.700.1.0.15843807_19480755.zip"
$esxiImageProfileName = "ESXi-7.0U3d-19482537-standard"
$newImageProfileName = "ESXi-7.0U3d-19482537-NUC"
Add-EsxSoftwareDepot $esxiOfflineBundle
Add-EsxSoftwareDepot $intelNicOfflineBundle
New-EsxImageProfile -CloneProfile $esxiImageProfileName -Name $newImageProfileName -Vendor "virten.net"
Add-EsxSoftwarePackage -ImageProfile $newImageProfileName -SoftwarePackage "net-community"
Export-EsxImageProfile -ImageProfile $newImageProfileName -ExportToIso -FilePath "C:\Users\bruce\Desktop\esxi\$newImageProfileName.iso"

# use script
.\ESXi-Customizer-PS-v2.6.0.ps1 -izip .\VMware-ESXi-7.0U2-17630552-depot.zip -pkgDir C:\Users\bruce\Desktop\esxi\pkg\
```

```powershell
# 程序和功能开启 虚拟机平台;windows 子系统
wsl --list --online # list onine distribution
wsl --install --distribution ubuntu-20.04

# 安装git bash时 使用外部openssh
```

```shell
# 去除TPM检查
REG ADD HKLM\SYSTEM\Setup\LabConfig /v BypassTPMCheck /t REG_DWORD /d 1
REG ADD HKLM\SYSTEM\Setup\LabConfig /v BypassSecureBootCheck /t REG_DWORD /d 1
```