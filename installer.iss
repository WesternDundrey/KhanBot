#define MyAppName "KhanBot"
#define MyAppVersion "1.0"
#define MyAppPublisher "KhanBot"
#define MyAppExeName "KhanBot.exe"

[Setup]
AppId={{YOUR-GUID-HERE}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=output
OutputBaseFilename=KhanBot_Setup
SetupIconFile=icons\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "installwsl"; Description: "Install Windows Subsystem for Linux (Recommended)"; GroupDescription: "Additional Components"

[Files]
Source: "dist\KhanBot.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "backend-api\*"; DestDir: "{app}\backend-api"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dashboard\*"; DestDir: "{app}\dashboard"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "setup_khanbot.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "setup.sh"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "wsl.exe"; Parameters: "--install"; Tasks: installwsl; Flags: runhidden; StatusMsg: "Installing WSL..."
Filename: "{app}\setup_khanbot.bat"; StatusMsg: "Setting up KhanBot environment..."; Flags: runhidden waituntilterminated
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // Check if Windows 10 or later
  if not CheckWin10OrLater then
  begin
    MsgBox('KhanBot requires Windows 10 or later.', mbInformation, MB_OK);
    Result := False;
  end;
end;

// Custom function to check Windows version
function CheckWin10OrLater: Boolean;
var
  Version: TWindowsVersion;
begin
  GetWindowsVersionEx(Version);
  Result := Version.Major >= 10;
end;
