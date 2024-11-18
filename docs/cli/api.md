Приложение имеет API интерфейс для использования его в других приложениях.
Интерфейс CLI (Command line interface) предназначен для удобного использования приложения через терминал,
а API (Application programming interface) предназначен для удобного использования приложения
во всевозможных скриптах, приложениях или расширениях для IDE.

По API можно вызвать справку в приложении через аргумент `--help`, так же, как и для других команд.
Команда имеет один аргумент - `--route`, он принимает URL в виде строки:

```shell
aurora-cli api --route '/device/command?host=192.168.2.15&execute=ls -1'
```

!!! info
    Секретные данные (например пароль) можно передать переменной окружения и API считает данные. Например:

    `export cli_password="00000"`

    Для исключения возможных коллизий добавлен префикс `cli_`.

## Routes

#### /app

Get information about the application.

```yaml title="/app/info"
No arguments
```

Clear cached data.

```yaml title="/app/clear"
No arguments
```

Get information about versions the application.

```yaml title="/app/versions"
No arguments
```

Check access to root user.

```yaml title="/app/auth/check"
• version - Installed version of Aurora Platform SDK.
```

Authorization in sudo.

```yaml title="/app/auth/root"
• password - Root password.
```

#### /device

Get list devices.

```yaml title="/device/list"
No arguments
```

Get info device.

```yaml title="/device/info"
• host - IP address device.
```

Execute the command on the device.

```yaml title="/device/command"
• host - IP address device.
• execute - The command will be executed on the device.
```

Upload file to ~/Download directory device.

```yaml title="/device/upload"
• host - IP address device.
• path - Path to file.
```

Run package on the device.

```yaml title="/device/package/run"
• host - IP address device.
• package - Package name.
• mode [dart, gdb] (optional) - Application launch mode.
• project (optional) - Path to project. The default is the current directory.
```

Install RPM package on the device.

```yaml title="/device/package/install"
• host - IP address device.
• path - Path to file.
• apm [default = false, true] - Use APM.
• reinstall [default = false, true] - Reinstall an already installed package.
```

Remove package from the device.

```yaml title="/device/package/remove"
• host - IP address device.
• package - Package name.
• apm [default = false, true] - Use APM.
• keep_user_data [default = false, true] - Keep user data.
```

#### /emulator

Start the emulator.

```yaml title="/emulator/start"
No arguments
```

Take a screenshot of the emulator.

```yaml title="/emulator/screenshot"
No arguments
```

Start recording video from the the emulator.

```yaml title="/emulator/recording/start"
No arguments
```

Stop video recording from the the emulator.

```yaml title="/emulator/recording/stop"
No arguments
```

Get info emulator.

```yaml title="/emulator/info"
No arguments
```

Execute the command on the emulator.

```yaml title="/emulator/command"
• execute - The command will be executed on the emulator.
```

Upload file to ~/Download directory emulator.

```yaml title="/emulator/upload"
• path - Path to file.
```

Run package on the emulator.

```yaml title="/emulator/package/run"
• package - Package name.
• mode [dart, gdb] (optional) - Application launch mode.
• project (optional) - Path to project. The default is the current directory.
```

Install RPM package on the emulator.

/emulator/package/install

```yaml title="/emulator/package/install"
• path - Path to file.
• apm [default = false, true] - Use APM.
• reinstall [default = false, true] - Reinstall an already installed package.
```

Remove package from the emulator.

```yaml title="/emulator/package/remove"
• package - Package name.
• apm [default = false, true] - Use APM.
• keep_user_data [default = false, true] - Keep user data.
```

#### /flutter

Get available version Flutter for Aurora OS.

```yaml title="/flutter/available"
No arguments
```

Get versions of installed Flutter for Aurora OS.

```yaml title="/flutter/installed"
No arguments
```

Download and install Flutter for Aurora OS.

```yaml title="/flutter/install"
• version - Installed version of Flutter.
```

Remove Flutter for Aurora OS.

```yaml title="/flutter/remove"
• version - Installed version of Flutter.
```

Project formatting.

```yaml title="/flutter/project/format"
• version - Installed version of Flutter.
• path - Path to project. The default is the current directory.
```

Project check format.

```yaml title="/flutter/project/check-format"
• version - Installed version of Flutter.
• path - Path to project. The default is the current directory.
```

Compile a report of flutter project.

```yaml title="/flutter/project/report"
• version - Installed version of Flutter.
• path - Path to project. The default is the current directory.
```

Gen multiple size icons for application.

```yaml title="/flutter/project/icons"
• image - Path to image.
• path - Path to project. The default is the current directory.
```

#### /psdk

Get available version Aurora Platform SDK.

```yaml title="/psdk/available"
No arguments
```

Get installed list Aurora Platform SDK.

```yaml title="/psdk/installed"
No arguments
```

Get info about Aurora Platform SDK.

```yaml title="/psdk/info"
• version - Installed version of Aurora Platform SDK.
```

Get list targets Aurora Platform SDK.

```yaml title="/psdk/targets"
• version - Installed version of Aurora Platform SDK.
```

Download Aurora Platform SDK.

```yaml title="/psdk/download"
• version - Installed version of Aurora Platform SDK.
```

Install Aurora Platform SDK.

```yaml title="/psdk/install"
• version - Installed version of Aurora Platform SDK.
```

Remove Aurora Platform SDK.

```yaml title="/psdk/remove"
• version - Installed version of Aurora Platform SDK.
```

Remove snapshot target.

```yaml title="/psdk/clear"
• version - Installed version of Aurora Platform SDK.
• target - Target name installed version of Aurora Platform SDK.
```

Add sudoers permissions Aurora Platform SDK.

```yaml title="/psdk/sudoers/add"
• version - Installed version of Aurora Platform SDK.
```

Remove sudoers permissions Aurora Platform SDK.

```yaml title="/psdk/sudoers/remove"
• version - Installed version of Aurora Platform SDK.
```

Search installed package in target.

```yaml title="/psdk/package/search"
• version - Installed version of Aurora Platform SDK.
• target - Target name installed version of Aurora Platform SDK.
• package - Package name.
```

Install RPM packages to target.

```yaml title="/psdk/package/install"
• version - Installed version of Aurora Platform SDK.
• target - Target name installed version of Aurora Platform SDK.
• path - Path to RPM file.
```

Remove package from target.

```yaml title="/psdk/package/remove"
• version - Installed version of Aurora Platform SDK.
• target - Target name installed version of Aurora Platform SDK.
• package - Package name.
```

Validate RPM packages.

```yaml title="/psdk/package/validate"
• version - Installed version of Aurora Platform SDK.
• target - Target name installed version of Aurora Platform SDK.
• path - Path to RPM file.
• profile [regular, extended, mdm, antivirus, auth] - Select profile.
```

Sign (with re-sign) RPM package.

```yaml title="/psdk/package/sign"
• version - Installed version of Aurora Platform SDK.
• path - Path to RPM file.
• phrase - PEM пароль-фраза.
• key (optional) - The name of key for sign package from config application.
```

Project formatting.

```yaml title="/psdk/project/format"
• path - Path to project. The default is the current directory.
```

Project check format.

```yaml title="/psdk/project/check-format"
• path - Path to project. The default is the current directory.
```

Gen multiple size icons for application.

```yaml title="/psdk/project/icons"
• image - Path to image.
• path - Path to project. The default is the current directory.
```

#### /sdk

Get available version Aurora SDK.

```yaml title="/sdk/available"
No arguments
```

Get version of the installed Aurora SDK.

```yaml title="/sdk/installed"
No arguments
```

Download and run Aurora SDK installation.

```yaml title="/sdk/install"
• version - Installed version of Aurora Platform SDK.
• offline [default = false, true] - Download offline type installer.
```

Run maintenance tool (remove, update).

```yaml title="/sdk/tool"
No arguments
```

#### /vscode

Information about VS Code.

```yaml title="/vscode/info"
No arguments
```

Get a list of VS Code extensions.

```yaml title="/vscode/extensions/list"
No arguments
```

Install VS Code extension.

```yaml title="/vscode/extensions/install"
• extension - Name of the VS Code extension.
```

Update VS Code settings.

```yaml title="/vscode/settings/update"
No arguments
```

#### /settings

Display additional application settings.

```yaml title="/settings/list"
No arguments
```

Clear advanced application settings.

```yaml title="/settings/clear"
No arguments
```

Set the application language.

```yaml title="/settings/localization"
• language [ru, en] - Application language.
```

Controlling the --verbose parameter.

```yaml title="/settings/verbose"
• enable [false, true] - Enable/Disable --verbose by default.
```

Controlling the --select parameter.

```yaml title="/settings/select"
• enable [false, true] - Enable/Disable saving --select.
```

Manage application hints.

```yaml title="/settings/hint"
• enable [false, true] - Enable/Disable application hints.
```

#### /tests

Test answers API.

```yaml title="/tests/answer"
• time [default = 0] - Response delay time.
• code [default = 200] - Response code (100, 200, 500).
• iterate [default = 1] - Number of response iterations.
```