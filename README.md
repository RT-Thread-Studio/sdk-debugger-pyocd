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

   

## 有问题看这里

1. 如果使用方法1，必须在 pyocd.exe 所在目录执行上述命令，任何其他路径下通过绝对路径的调用目前都不支持
2. -t 参数必须是芯片的名称，比如 STM32F103RE,  STM32H747AGIx, 需要严格一致

