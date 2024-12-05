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
; Main executable
Source: "dist\KhanBot.exe"; DestDir: "{app}"; Flags: ignoreversion

; Backend API files
Source: "backend-api\*"; DestDir: "{app}\backend-api"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "launch_backend.bat"; DestDir: "{app}"; Flags: ignoreversion

; Dashboard files
Source: "dashboard\*"; DestDir: "{app}\dashboard"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "launch_dashboard.bat"; DestDir: "{app}"; Flags: ignoreversion

; Environment and setup files
Source: "environment.yml"; DestDir: "{app}"; Flags: ignoreversion
Source: "backup_env.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "wsl_progress.bat"; DestDir: "{app}"; Flags: ignoreversion

; Main launcher files
Source: "launch_khanbot.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Launch Backend"; Filename: "{app}\launch_backend.bat"
Name: "{group}\Launch Dashboard"; Filename: "{app}\launch_dashboard.bat"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\backup_env.bat"; StatusMsg: "Backing up existing environment..."; Flags: runhidden waituntilterminated; Check: not WizardSilent
Filename: "{app}\wsl_progress.bat"; StatusMsg: "Setting up WSL environment..."; Flags: runhidden waituntilterminated; Check: not WizardSilent
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  Version: string;
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

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Add any post-installation tasks here
  end;
end;