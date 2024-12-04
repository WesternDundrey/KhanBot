#define MyAppName "KhanBot"
#define MyAppVersion "1.0"
#define MyAppPublisher "KhanBot"
#define MyAppExeName "KhanBot.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-G7H8-I9J0-K1L2M3N4O5P6}}
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

[Files]
Source: "dist\KhanBot.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "backend-api\*"; DestDir: "{app}\backend-api"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dashboard\*"; DestDir: "{app}\dashboard"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "setup_khanbot.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "backup_env.bat"; DestDir: "{app}"; Flags: ignoreversion

[Run]
; First check and backup existing environments
Filename: "{app}\backup_env.bat"; Flags: runhidden waituntilterminated; StatusMsg: "Checking existing environments..."

; Then run the main setup
Filename: "{app}\setup_khanbot.bat"; Flags: runhidden waituntilterminated; StatusMsg: "Setting up KhanBot..."

; Launch the application
Filename: "{app}\{#MyAppExeName}"; Description: "Launch KhanBot"; Flags: nowait postinstall skipifsilent
