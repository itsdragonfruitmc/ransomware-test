[Setup]
AppName=Minecraft free
AppVersion=1.0
DefaultDirName={autopf}\Minecraft free
OutputBaseFilename=MyProgram-Setup

[Files]
Source: "dist\minecraft free.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Minecraft free"; Filename: "{app}\minecraft free.exe"

[Code]

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    if MsgBox(
      'Do you want to create a shortcut on your desktop?',
      mbConfirmation,
      MB_YESNO
    ) = IDYES then
    begin
      CreateShellLink(
        ExpandConstant('{autodesktop}\My Program.lnk'),
        'My Program',
        ExpandConstant('{app}\bosd.exe'),
        '',
        ExpandConstant('{app}'),
        ExpandConstant('{app}\bosd.exe'),
        0,
        SW_SHOWNORMAL
      );
    end;
  end;
end;