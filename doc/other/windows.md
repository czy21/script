## ESXI build
```powershell
Install-Module -Name VMware.PowerCLI -RequiredVersion 12.0.0.15947286
Set-ExecutionPolicy RemoteSigned
```
* 7.0
    ```powershell
    $esxiOfflineBundle = "VMware-ESXi-7.0U3d-19482537-depot.zip"
    $intelNicOfflineBundle = "./pkg/Net-Community-Driver_1.2.7.0-1vmw.700.1.0.15843807_19480755.zip"
    $esxiImageProfileName = "ESXi-7.0U3d-19482537-standard"
    $newImageProfileName = "ESXi-7.0U3d-19482537-NUC"
    Add-EsxSoftwareDepot ./$esxiOfflineBundle
    Add-EsxSoftwareDepot $intelNicOfflineBundle
    New-EsxImageProfile -CloneProfile $esxiImageProfileName -Name $newImageProfileName -Vendor "virten.net"
    Add-EsxSoftwarePackage -ImageProfile $newImageProfileName -SoftwarePackage "net-community"
    Export-EsxImageProfile -ImageProfile $newImageProfileName -ExportToIso -FilePath "./$newImageProfileName.iso"
    ```

* 8.0
    ```powershell
    $esxiOfflineBundle = "VMware-ESXi-8.0U1a-21813344-depot.zip"
    $esxiImageProfileName = "ESXi-8.0U1a-21813344-standard"
    $newImageProfileName = "ESXi-8.0U1a-21813344-nuc"

    Add-EsxSoftwareDepot ./$esxiOfflineBundle
    Add-EsxSoftwareDepot "./pkg/Net-Community-Driver_1.2.7.0-1vmw.700.1.0.15843807_19480755.zip"
    Add-EsxSoftwareDepot "./pkg/ESXi80U1-VMKUSB-NIC-FLING-64098092-component-21669994.zip"
    Add-EsxSoftwareDepot "./pkg/nvme-community-driver_1.0.1.0-3vmw.700.1.0.15843807-component-18902434.zip"
    Get-EsxImageProfile
    New-EsxImageProfile -CloneProfile $esxiImageProfileName -Name $newImageProfileName -vendor "czy21.com"

    Add-EsxSoftwarePackage -ImageProfile $newImageProfileName -SoftwarePackage "net-community"
    Add-EsxSoftwarePackage -ImageProfile $newImageProfileName -SoftwarePackage "vmkusb-nic-fling"
    Add-EsxSoftwarePackage -ImageProfile $newImageProfileName -SoftwarePackage "nvme-community"

    Export-EsxImageProfile -ImageProfile $newImageProfileName -ExportToIso -FilePath ./$newImageProfileName.iso
    ```
# use script
.\ESXi-Customizer-PS-v2.6.0.ps1 -izip .\VMware-ESXi-7.0U3d-19482537-depot.zip -pkgDir .\pkg\
```

```powershell
# 程序和功能开启 虚拟机平台;windows 子系统
wsl --list --online # list onine distribution
wsl --install --distribution ubuntu-22.04

# 安装git bash时 使用外部openssh
```

```shell
# install shift+F10
REG ADD HKLM\SYSTEM\Setup\LabConfig /v BypassTPMCheck /t REG_DWORD /d 1
REG ADD HKLM\SYSTEM\Setup\LabConfig /v BypassSecureBootCheck /t REG_DWORD /d 1
# init shift+F10
OOBE\BYPASSNRO
```

```shell
# powershell active win server 2022 datacenter
DISM /online /Get-CurrentEdition
DISM /online /Set-Edition:ServerDatacenter /ProductKey:WX4NM-KYWYW-QJJR4-XV3QB-6VM33 /AcceptEula
```