# DAP-Link 调试实例

### 文件描述

1. packs 

   cmsis 的压缩包，包含了下载算法和 flash 以及 ram 信息

2. pyocd.yaml 

   pyocd.exe 使用的配置文件

3. pyocd.exe

   pyocd 的可执行程序
   
4. pyocd.bat

   添加了目录切换的 pyocd.exe 调用脚本

   

## 参数列表

+ --config 

  用户配置文件，可选参数 ，默认值为工作目录下的pyocd.yaml

+ --target ，-t

  目标设备名称

+ --port ，-p

  gdb server 侦听的端口，默认为3333

  

### 工作目录

##### 方法1（只能在pyocd 目录内执行）

1. 切换 workdir 到 pyocd.exe 所在目录

3. 执行以下指令，启动gdb server，其中-t 参数必须为芯片名称

   ```powershell
    ./pyocd.exe  gdbserver  --config=pyocd.yaml -t stm32f103re
   ```

3. 按照议题  https://git.rt-thread.com/realthread/ide_bug_report/-/issues/236  所描述方法进行程序下载和仿真


##### 方法2 在任意目录内执行

1. 执行 pyocd.bat 可以自动执行切换工作目录，可以在任意位置执行次命令

   ```powershell
   anypath_to_pyocd_folder/pyocd.bat  gdbserver  -t stm32f103re
   ```

   **注意事项：注意参数中如果存在文件路径为相对路径，必须转换为绝对路径，因为bat内会打乱相对的位置关系**

   

## 应用示例-仿真

1. 使用默认配置文件（pyocd.yaml）,目标设备是stm32f103re ，监听端口是3333 的启动命令如下

   ```powershell
   ./pyocd.exe  gdbserver --target=stm32f103re
   ```

2. 使用默认配置文件，目标设备是stm32f103c8，监听端口是3334，启动命令如下：

   ```powershell
   ./pyocd.exe  gdbserver --target=stm32f103c8 --port=3334
   ```



## 应用示例-擦除

1. 擦除芯片

   ```powershell
   PS C:\Users\yaxing.chen\Documents\workspace> .\dap-link-demo\pyocd.bat erase --chip --target=stm32f103re
   ```



## 应用示例-烧写

1. 烧写 bin 文件

   ```powershell
   PS C:\Users\yaxing.chen\Documents\workspace> .\dap-link-demo\pyocd.bat flash  --target=stm32f103re C:\Users\yaxing.chen\Documents\workspace\dap-link-demo\rtthread.bin
   [====================] 100%
   0004784:INFO:loader:Erased 53248 bytes (26 sectors), programmed 53248 bytes (52 pages), skipped 0 bytes (0 pages) at 13.70 kB/s
   ```

2. 烧写 elf 文件

   ```powershell
   PS C:\Users\yaxing.chen\Documents\workspace> .\dap-link-demo\pyocd.bat flash  --target=stm32f103re C:\Users\yaxing.chen\Documents\workspace\dap-link-demo\rtthread.elf
   [====================] 100%
   0004818:INFO:loader:Erased 53248 bytes (26 sectors), programmed 53248 bytes (52 pages), skipped 0 bytes (0 pages) at 13.58 kB/s
   ```

   

## MCU 连接重试配置

本工具包中的 pyOCD 0.45.1 对 CMSIS-Pack 目标使用默认 `DebugPortSetup` 调试序列时，首次读取 DPIDR 返回 `No ACK` 就会结束连接。这条初始化路径并非 GD32H77DIW 专用，因此连接重试配置适用于所有带 CoreSight Debug Port 的 MCU。

`pyocd.yaml` 已配置自动加载 `diagnostics/native_swd.py`，让所有带 Debug Port 的目标使用 pyOCD 内置的连接重试流程。该处理不检查芯片名称，也适用于自动识别的目标；没有 Debug Port 的目标保持原有流程。芯片内存映射、Flash 下载算法和其他调试序列继续由原目标或芯片包提供。

在本工具包目录执行原下载命令即可，无需额外添加 `--script` 参数，例如：

```powershell
.\pyocd.exe flash --target=GD32H77DIW --erase=auto -a=0x08000000 --frequency=1000000 C:/firmware/rtthread.bin
```

从其他目录调用时，使用前文的 `pyocd.bat` 以正确定位配置文件。发布工具包时需包含 `diagnostics/native_swd.py`；使用 `--no-config` 时不会通过 YAML 加载此配置。若需停用兼容处理，删除或注释 `pyocd.yaml` 中的 `user_script` 配置项即可。

原生连接重试方案已在 GD32H77DIW 与 CherryUSB CMSIS-DAP 组合上通过实板实际擦写及连续连接测试，不代表所有 MCU 均已完成实板验证。升级 pyOCD 后应重新验证此兼容处理。

## 有问题看这里

1. 如果使用方法1，必须在 pyocd.exe 所在目录执行上述命令，任何其他路径下通过绝对路径的调用目前都不支持
2. -t 参数必须是芯片的名称，比如 STM32F103RE,  STM32H747AGIx, 需要严格一致

