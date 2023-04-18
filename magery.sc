{
================================================================
Script name: neo's Magery Trainer
Author: neo
Version: 1.0
Client tested with: Stealth Interface 7.0.29.2
Stealth version tested with: 4.3.6
Shard: OSI
Revision Date: March 28, 2013
Public Release: March 28, 2013
Purpose: Trains Magery from 30 to Skill Cap.
Special thanks: C2, as I used the same skills he uses in his
        magery trainer for EasyUO. Cheers!
================================================================
Version 1.0    - Public release
================================================================
Instructions:  - You must have at least 30 skill points in magery
               - This script won't use reagents, so use LRC suit
               - Press 'Start' :)
------------------------------------------------------------------
               The script will automatically calculate how much
               Faster Casting and Faster Cast Recovery you have
               and run accordingly.
------------------------------------------------------------------------
========================================================================
Only use this script if downloaded from one of the following places:
http://www.scriptuo.com/index.php?topic=11042.0
http://stealth.od.ua/forum/viewtopic.php?f=15&t=2499
========================================================================
}

program neomagery;
//===== constants =====
const
ActiveMeditationID = 1013;
LRC_Cliloc = 1060434;
FCR_Cliloc = 1060412;
FC_Cliloc = 1060413;
LMC_Cliloc = 1060433;
LMC_Max = 40;
FCR_Max = 6;
FC_Max = 2;
LRC_Max = 100;
//===== variables =====
var
PressedStart : Boolean;
MinimumMana : Integer;
EquipSlot : Array of Byte;
LMC : Integer;
FC : Integer;
FCR : Integer;
LRC : Integer;
StartingSkill : Double;
CurrentSkill : Double;
SkillCap : Double;
IsMeditating : Boolean;
Status : String;
StartTime : TDateTime;
SpellCircle : Integer;

//===== menu stuff =====
var
  StartMenu: TSTForm;
  Menu: TSTForm;
  PlayerBox: TSTGroupBox;
  NameLbl: TSTLabel;
  FCLbl: TSTLabel;
  FCRLbl: TSTLabel;
  LMCLbl: TSTLabel;
  LRCLbl: TSTLabel;
  NameLabel: TSTLabel;
  FCLabel: TSTLabel;
  FCRLabel: TSTLabel;
  LMCLabel: TSTLabel;
  LRCLabel: TSTLabel;
  MageryBox: TSTGroupBox;
  TimeBox: TSTGroupBox;
  StartingLbl: TSTLabel;
  CurrentLbl: TSTLabel;
  GainsLbl: TSTLabel;
  StatusBox: TSTGroupBox;
  StartingLabel: TSTLabel;
  CurrentLabel: TSTLabel;
  GainsLabel: TSTLabel;
  TimeLbl: TSTLabel;
  TimeLabel: TSTLabel;
  StatusLabel: TSTLabel;
  TitleLabel: TSTLabel;
  StartLabel: TSTLabel;
  StartButton: TSTButton; 

Procedure GUI_OnClose(Sender: TObject; var Action : TCloseAction);
begin
  Menu.Free();
  raiseException(erCustomError,'Menu was closed. Halting!');
  Exit;
end;

Procedure StartGUI_OnClose(Sender: TObject; var Action : TCloseAction);
begin
  StartMenu.Free();
  raiseException(erCustomError,'Menu was closed. Halting!');
  Exit;
end;

Procedure StartButton_Click(Sender: TObject);
begin
  PressedStart := True;  
end;

Procedure StartMenuInit();
begin
  StartMenu := TSTForm.Create();
  StartMenu.BorderStyle := bsSingle;
  StartMenu.Color := clBtnFace;
  StartMenu.Height := 108;
  StartMenu.Width := 154;
  StartMenu.Left := 0;
  StartMenu.Top := 0;
  StartMenu.Caption := 'neo''s Magery Trainer';
  StartMenu.OnClose := @StartGUI_OnClose;
  TitleLabel := TSTLabel.Create(StartMenu);
  TitleLabel.Parent := (StartMenu);
  TitleLabel.Height := 13;
  TitleLabel.Left := 27;
  TitleLabel.Top := 8;
  TitleLabel.Width := 101;
  TitleLabel.Caption := 'neo''s Magery Trainer';
  StartLabel := TSTLabel.Create(StartMenu);
  StartLabel.Parent := (StartMenu);
  StartLabel.Height := 13;
  StartLabel.Left := 21;
  StartLabel.Top := 63;
  StartLabel.Width := 113;
  StartLabel.Caption := 'Press Start when ready';
  StartButton := TSTButton.Create(StartMenu);
  StartButton.Parent := (StartMenu);
  StartButton.Caption := 'Start'; 
  StartButton.Left := 39;
  StartButton.Top := 27;
  StartButton.Height := 25;
  StartButton.Width := 75; 
  StartButton.OnClick := @StartButton_Click; 
  StartMenu.Show();
end;

Procedure MenuInit();
begin
  Menu := TSTForm.Create();
  Menu.BorderStyle := bsSingle;
  Menu.Color := clBtnFace;
  Menu.Height := 223;
  Menu.Width := 386;
  Menu.Left := 0;
  Menu.Top := 0;
  Menu.Caption := 'neo''s Magery Trainer';
  Menu.OnClose := @GUI_OnClose;
  //----- Player Info -----
  PlayerBox := TSTGroupBox.Create(Menu); 
  PlayerBox.Parent := Menu;
  PlayerBox.Height := 137;
  PlayerBox.Width := 209;
  PlayerBox.Left := 8;
  PlayerBox.Top := 8;
  PlayerBox.Caption := 'Player Info';
  //----- Player Info Labels -----
  NameLbl := TSTLabel.Create(PlayerBox);
  NameLbl.Parent := (PlayerBox);
  NameLbl.Height := 13;
  NameLbl.Left := 16;
  NameLbl.Top := 24;
  NameLbl.Width := 31;
  NameLbl.Caption := 'Name:';
  FCLbl := TSTLabel.Create(PlayerBox);
  FCLbl.Parent := (PlayerBox);
  FCLbl.Height := 13;
  FCLbl.Left := 16;
  FCLbl.Top := 43;
  FCLbl.Width := 74;
  FCLbl.Caption := 'Faster Casting:';  
  FCRLbl := TSTLabel.Create(PlayerBox);
  FCRLbl.Parent := (PlayerBox);
  FCRLbl.Height := 13;
  FCRLbl.Left := 16;
  FCRLbl.Top := 62;
  FCRLbl.Width := 109;
  FCRLbl.Caption := 'Faster Cast Recovery:';
  LMCLbl := TSTLabel.Create(PlayerBox);
  LMCLbl.Parent := (PlayerBox);
  LMCLbl.Height := 13;
  LMCLbl.Left := 16;
  LMCLbl.Top := 81;
  LMCLbl.Width := 81;
  LMCLbl.Caption := 'Lower Mana Cost:';
  LRCLbl := TSTLabel.Create(PlayerBox);
  LRCLbl.Parent := (PlayerBox);
  LRCLbl.Height := 13;
  LRCLbl.Left := 16;
  LRCLbl.Top := 100;
  LRCLbl.Width := 102;
  LRCLbl.Caption := 'Lower Reagent Cost:';
  NameLabel := TSTLabel.Create(PlayerBox);
  NameLabel.Parent := (PlayerBox);
  NameLabel.Height := 13;
  NameLabel.Left := 143;
  NameLabel.Top := 24;
  NameLabel.Width := 70;
  NameLabel.Caption := CharName;
  FCLabel := TSTLabel.Create(PlayerBox);
  FCLabel.Parent := (PlayerBox);
  FCLabel.Height := 13;
  FCLabel.Left := 143;
  FCLabel.Top := 43;
  FCLabel.Width := 38;
  FCLabel.Caption := '';
  FCRLabel := TSTLabel.Create(PlayerBox);
  FCRLabel.Parent := (PlayerBox);
  FCRLabel.Height := 13;
  FCRLabel.Left := 143;
  FCRLabel.Top := 62;
  FCRLabel.Width := 45;
  FCRLabel.Caption := '';  
  LMCLabel := TSTLabel.Create(PlayerBox);
  LMCLabel.Parent := (PlayerBox);
  LMCLabel.Height := 13;
  LMCLabel.Left := 143;
  LMCLabel.Top := 81;
  LMCLabel.Width := 46;
  LMCLabel.Caption := '';
  LRCLabel := TSTLabel.Create(PlayerBox);
  LRCLabel.Parent := (PlayerBox);
  LRCLabel.Height := 13;
  LRCLabel.Left := 143;
  LRCLabel.Top := 100;
  LRCLabel.Width := 45;
  LRCLabel.Caption := '';
  //----- Magery Info ----   
  MageryBox := TSTGroupBox.Create(Menu); 
  MageryBox.Parent := Menu;
  MageryBox.Height := 75;
  MageryBox.Width := 154;
  MageryBox.Left := 223;
  MageryBox.Top := 8;
  MageryBox.Caption := 'Magery Info'; 
  //----- Magery Info Labels -----
  StartingLbl := TSTLabel.Create(MageryBox);
  StartingLbl.Parent := (MageryBox);
  StartingLbl.Height := 13;
  StartingLbl.Left := 16;
  StartingLbl.Top := 24;
  StartingLbl.Width := 62;
  StartingLbl.Caption := 'Starting Skill:';  
  CurrentLbl := TSTLabel.Create(MageryBox);
  CurrentLbl.Parent := (MageryBox);
  CurrentLbl.Height := 13;
  CurrentLbl.Left := 16;
  CurrentLbl.Top := 43;
  CurrentLbl.Width := 61;
  CurrentLbl.Caption := 'Current Skill:';
  GainsLbl := TSTLabel.Create(MageryBox);
  GainsLbl.Parent := (MageryBox);
  GainsLbl.Height := 13;
  GainsLbl.Left := 16;
  GainsLbl.Top := 62;
  GainsLbl.Width := 50;
  GainsLbl.Caption := 'Skill Gains:';
  StartingLabel := TSTLabel.Create(MageryBox);
  StartingLabel.Parent := (MageryBox);
  StartingLabel.Height := 13;
  StartingLabel.Left := 104;
  StartingLabel.Top := 24;
  StartingLabel.Width := 30;
  StartingLabel.Caption := FloatToStrF(StartingSkill,ffFixed,12,1);  
  CurrentLabel := TSTLabel.Create(MageryBox);
  CurrentLabel.Parent := (MageryBox);
  CurrentLabel.Height := 13;
  CurrentLabel.Left := 104;
  CurrentLabel.Top := 43;
  CurrentLabel.Width := 62;
  CurrentLabel.Caption := FloatToStrF(CurrentSkill,ffFixed,12,1);
  GainsLabel := TSTLabel.Create(MageryBox);
  GainsLabel.Parent := (MageryBox);
  GainsLabel.Height := 13;
  GainsLabel.Left := 96;
  GainsLabel.Top := 62;
  GainsLabel.Width := 65;
  GainsLabel.Caption := '+' + FloatToStrF((CurrentSkill - StartingSkill),ffFixed,12,1);
  //----- Status Box -----
  StatusBox := TSTGroupBox.Create(Menu); 
  StatusBox.Parent := Menu;
  StatusBox.Height := 34;
  StatusBox.Width := 370;
  StatusBox.Left := 8;
  StatusBox.Top := 151;
  StatusBox.Caption := 'Status';
  //----- Status Label -----
  StatusLabel := TSTLabel.Create(StatusBox);
  StatusLabel.Parent := (StatusBox);
  StatusLabel.Height := 13;
  StatusLabel.Left := 16;
  StatusLabel.Top := 16;
  StatusLabel.Width := 44;
  StatusLabel.Caption := 'Idle';
  //----- Time Info -----
  TimeBox := TSTGroupBox.Create(Menu); 
  TimeBox.Parent := Menu;
  TimeBox.Height := 56;
  TimeBox.Width := 154;
  TimeBox.Left := 223;
  TimeBox.Top := 89;
  TimeBox.Caption := 'Time Info';
  //----- Time Info Labels -----
  TimeLbl := TSTLabel.Create(TimeBox);
  TimeLbl.Parent := (TimeBox);
  TimeLbl.Height := 13;
  TimeLbl.Left := 22;
  TimeLbl.Top := 19;
  TimeLbl.Width := 68;
  TimeLbl.Caption := 'Time Running:';  
  TimeLabel := TSTLabel.Create(TimeBox);
  TimeLabel.Parent := (TimeBox);
  TimeLabel.Height := 13;
  TimeLabel.Left := 104;
  TimeLabel.Top := 19;
  TimeLabel.Width := 61;
  Menu.Show();
end;

Procedure InitializeMenu;
var i : Integer;
begin
  StatusLabel.Caption := 'Calculating Faster Casting -> ';
  wait(1000);                       
  for i := 0 to FC do
  begin
    wait(50);
    StatusLabel.Caption := 'Calculating Faster Casting -> ' + IntToStr(i);
    FCLabel.Caption := IntToStr(i); 
  end;
  FCLabel.Caption := IntToStr(FC);
  StatusLabel.Caption := 'Calculating Faster Cast Recovery -> ';
  wait(1000);
  for i := 0 to FCR do
  begin
    wait(50);
    StatusLabel.Caption := 'Calculating Faster Cast Recovery -> ' + IntToStr(i);
    FCRLabel.Caption := IntToStr(i);
  end;                                                                          
  FCRLabel.Caption := IntToStr(FCR);
  StatusLabel.Caption := 'Calculating Lower Mana Cost -> ';
  wait(1000);        
  for i := 0 to LMC do
  begin
    wait(18);
    StatusLabel.Caption := 'Calculating Lower Mana Cost -> ' + IntToStr(i);
    LMCLabel.Caption := IntToStr(i);    
  end;                                                                     
  LMCLabel.Caption := IntToStr(LMC);
  StatusLabel.Caption := 'Calculating Lower Reagent Cost -> ';
  wait(1000);
  for i := 0 to LRC do
  begin
    wait(8);
    StatusLabel.Caption := 'Calculating Lower Reagent Cost -> ' + IntToStr(i);
    LRCLabel.Caption := IntToStr(i);
  end;                                                                        
  LRCLabel.Caption := IntToStr(LRC);
  StatusLabel.Caption := 'Finished calculating. Starting...';
  wait(1000);
  StartTime := now;
  TimeLabel.Caption := TimeToStr(Now - StartTime);
end;

Procedure UpdateMenu;
begin
    StatusLabel.Caption := Status;
  if ((CurrentSkill - StartingSkill) < 10.0) then
  begin
      GainsLabel.Caption := '+  ' + FloatToStrF((CurrentSkill - StartingSkill),ffFixed,12,1);                                                                           
  end;
  if ((CurrentSkill - StartingSkill) >= 10.0) then
  begin
    GainsLabel.Caption := '+' + FloatToStrF((CurrentSkill - StartingSkill),ffFixed,12,1);  
  end;
    CurrentLabel.Caption := FloatToStrF (CurrentSkill,ffFixed,12,1);
    TimeLabel.Caption := TimeToStr(Now - StartTime);
end;

Function FCRWait:Integer;
begin
  Result := 1500 - ( FCR * 250 );
end;

Function FCWait(Circle:Integer):Integer;
begin
  Result := 250 + ( Circle * 250 ) - ( FC * 250 );
end;
   

Function CalculateMinimumMana(Circle:Integer):Integer;
var ManaArray : Array of Integer;
begin
  ManaArray := [4,6,9,11,14,20,40,50];
  Result := ManaArray[Circle-1];
  if LMC > 0 then
  begin
    Result := Round(Result - ( ( Result * LMC ) / 100 ));
  end;  
end;

Function CalculateSkill(SkillName:String):Double;
var Skill : Double;
begin
  Skill := GetSkillValue(SkillName);
  if ( Skill <= 20.0 ) AND ( Race = 1 ) then
  begin
    Result := 20.0;
  end              
  else
  begin
    Result := Skill;
  end;
end;

Function CalculateProperty(Cliloc,Who:Cardinal;Maximum:Integer):Integer;
var
aa : TClilocRec;
i,k,total : Integer;
begin
  total := 0;
  for i := 0 to Length(EquipSlot) - 1 do
  begin
    if ObjAtLayerEx(EquipSlot[i],Who) <> 0 then
    begin
      aa := GetToolTipRec(ObjAtLayerEx(EquipSlot[i],Who));
      for k := 0 to aa.Count - 1 do
      begin
        if aa.Items[k].ClilocID = Cliloc then
        begin 
          total := total + StrToInt(aa.Items[k].Params[0]);  
        end;
      end;
      end;
    end;          
  if Total > Maximum then
    Total := Maximum;
  Result := Total;
end;

Procedure Init;
begin
  LMC := CalculateProperty(LMC_Cliloc,Self,LMC_Max);
  FC := CalculateProperty(FC_Cliloc,Self,FC_Max);
  FCR := CalculateProperty(FCR_Cliloc,Self,FCR_Max);
  LRC := CalculateProperty(LRC_Cliloc,Self,LRC_Max);
  StartingSkill := CalculateSkill('Magery');
  CurrentSkill := StartingSkill;
  SkillCap := GetSkillCap('Magery');
end;
//===== CheckMana =====
Procedure CheckMana(ReqMana:Integer);
begin
  Status := 'Checking mana';
  UpdateMenu;
  if ( Mana <= ReqMana * 2 ) then
  begin      
    Status := 'Mana is low. Attempting to meditate';
    UpdateMenu;
    SetEventProc(evBuff_DebuffSystem,'CheckActiveMeditation');
    While ( Mana < MaxMana ) do
    begin
      if ( IsMeditating = False ) then
      begin
        UseSkill('Meditation');
        wait(1000);
        if (IsMeditating = False) then
          wait(10000);
      end;
      if IsMeditating then
      begin 
        Status := 'Meditation was successful. Will continue once mana is full';
        UpdateMenu;
      end;
    end;
  end;
end;
//===== Check for Buffs/Debuffs =====
Procedure CheckActiveMeditation(ID,Attribute_ID : Cardinal; IsEnabled : Boolean);
begin
  if ( ( ID = Self)) then
  begin
    IsMeditating := ((Attribute_ID = ActiveMeditationID) and (IsEnabled <> False) )
  end;
end;

Procedure CastTargetYes(Spell:String);
begin
  Status := 'Casting ' + Spell;
  UpdateMenu;
  Cast(Spell);
  WaitForTarget(5000);
  TargetToObject(Self);
  if FCRWait > 0 then
    wait(FCRWait); 
end;

Procedure CastTargetNo(Spell:String;Circle:Integer);
begin
Status := 'Casting ' + Spell;
  Cast(Spell);
  Wait(FCWait(Circle));
  if FCRWait > 0 then
    wait(FCRWait);
end;

begin
//===== EquipSlot Array =====
EquipSlot := [ArmsLayer,BraceLayer,CloakLayer,EarLayer,EggsLayer,GlovesLayer,
              HatLayer,LegsLayer,LhandLayer,NeckLayer,PantsLayer,RhandLayer,
              RingLayer,RobeLayer,ShirtLayer,ShoesLayer,TalismanLayer,TorsoHLayer,
              TorsoLayer,WaistLayer]; 
//===== start of main code =====
Init;
PressedStart := False;
StartMenuInit;
While NOT PressedStart do
  wait(10);
StartMenu.Free();
MenuInit;
InitializeMenu;
while NOT dead do
begin
  CurrentSkill := CalculateSkill('Magery');
  if ( CurrentSkill >= 30.0 ) then
  begin
    if ( CurrentSkill < 40.0 ) then
    begin
      CheckMana(CalculateMinimumMana(3));
      CastTargetYes('Bless');            
    end;
    if ( CurrentSkill >= 40.0 ) AND ( CurrentSkill <  45.0 ) then
    begin
      CheckMana(CalculateMinimumMana(4));
      CastTargetYes('Greater Heal');
    end;                            
    if ( CurrentSkill >= 45.0 ) AND ( CurrentSkill < 68.0 ) then
    begin
      CheckMana(CalculateMinimumMana(5));
      CastTargetYes('Dispel Field');
    end; 
    if ( CurrentSkill >= 68.0 ) AND ( CurrentSkill < 82.0 ) then
    begin
      CheckMana(CalculateMinimumMana(6));
      CastTargetYes('Invisibility');
    end;                            
    if ( CurrentSkill >= 82.0 ) AND ( CurrentSkill < 95.0 ) then
    begin
      CheckMana(CalculateMinimumMana(7));
      CastTargetYes('Mass Dispel');
    end;                
    if ( CurrentSkill >= 95.0 ) AND ( CurrentSkill < SkillCap ) then
    begin
      CheckMana(CalculateMinimumMana(8));
      CastTargetNo('Earthquake',8);
    end;
    if ( CurrentSkill = SkillCap ) then
    begin
      ShowMessage('You have reached the skillcap. Thank you for using this script.');
      Exit;
    end;
  end
  else
  begin
    ShowMessage('You must have at least 30 in magery. Halting.');
    Exit;
  end;
end;
end.