#define MyAppName "KhanBot"
#define MyAppVersion "1.0"
#define MyAppPublisher "KhanBot"
#define MyAppExeName "KhanBot.exe"

[Setup]
AppId={{9461EC1D-FB0C-4A14-A3C1-8393E61D8668}}
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
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Main executable and core directories
Source: "dist\KhanBot.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "backend-api\*"; DestDir: "{app}\backend-api"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dashboard\*"; DestDir: "{app}\dashboard"; Flags: ignoreversion recursesubdirs createallsubdirs

; WSL and launch scripts
Source: "wsl_backend.sh"; DestDir: "{app}"; Flags: ignoreversion
Source: "wsl_dashboard.sh"; DestDir: "{app}"; Flags: ignoreversion
Source: "wsl_setup.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "launch_backend.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "launch_dashboard.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "launch_khanbot.bat"; DestDir: "{app}"; Flags: ignoreversion

; Environment configuration
Source: "environment.yml"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Launch KhanBot"; Filename: "{app}\launch_khanbot.bat"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Run WSL setup first
Filename: "{app}\wsl_setup.bat"; StatusMsg: "Setting up WSL environment..."; Flags: runhidden waituntilterminated shellexec; Check: not WizardSilent

; Launch option after installation
Filename: "{app}\launch_khanbot.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
var
  Version: string;

function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // Check Windows version (Windows 10 or later required for WSL)
  if not RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\Windows NT\CurrentVersion', 'CurrentVersion', Version) then
    Version := '0';
  if (CompareStr(Version, '6.3') < 0) then
  begin
    MsgBox('This application requires Windows 10 or later.', mbInformation, MB_OK);
    Result := False;
  end;
end;