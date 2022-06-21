## esxi build
```powershell
Install-Module -Name VMware.PowerCLI
Set-ExecutionPolicy RemoteSigned

$esxiOfflineBundle = "C:\Users\bruce\Desktop\esxi\VMware-ESXi-7.0U2-17630552-depot.zip"
$intelNicOfflineBundle = "C:\Users\bruce\Desktop\esxi\Intel-NUC-ne1000_0.8.4-3vmw.670.0.0.8169922-offline_bundle-16654787.zip"
$esxiImageProfileName = "ESXi-7.0.2-17630552-standard"
$newImageProfileName = "ESXi-7.0.2"
Add-EsxSoftwareDepot $esxiOfflineBundle
Add-EsxSoftwareDepot $intelNicOfflineBundle
$IntelNUCVib = Get-EsxSoftwarePackage | where {$_.name -eq "ne1000-intelnuc" -and $_.version -eq "0.8.4-3vmw.670.0.0.8169922"}
New-EsxImageProfile -CloneProfile $esxiImageProfileName -Name $newImageProfileName -Vendor vGhetto
Add-EsxSoftwarePackage -ImageProfile $newImageProfileName -SoftwarePackage $IntelNUCVib
Export-EsxImageProfile -ImageProfile $newImageProfileName -ExportToIso -FilePath "C:\Users\bruce\Desktop\esxi\ESXi-7.0.2-custom.ISO"

# use script
.\ESXi-Customizer-PS-v2.6.0.ps1 -izip .\VMware-ESXi-7.0U2-17630552-depot.zip -pkgDir C:\Users\bruce\Desktop\esxi\pkg\
```

```powershell
# 程序和功能开启 虚拟机平台;windows 子系统
wsl --list --online # list onine distribution
wsl --install --distribution ubuntu-20.04

# 安装git bash时 使用外部openssh
```