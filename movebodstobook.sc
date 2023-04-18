Program BoDAutomaticCollection;
const
GumpIgnoredID=0;
TailorVendor=$000B0278;
ContextMenuHookTailor=1;
BSVendor=$000B0299; 
ContextMenuHookBS=1; 
BodType=$2258;
BodClrT=$452EA577;
BoDClrBS=$452EEEB8;
Trash=$4040A43F;
UseTailor=False;
UseBS=True; 
TBook=0;
BSBook=$2258;
TMsg='Taking Tailor BOD';
BSMsg='Taking BS BOD';
WaitTime=500;
WaitLag=1000;
var
MyProfiles:array of String;
TimeOrder:array of TDateTime;
nProfile:Integer;
procedure CollectBoDWithCondition(Msg:String;Vendor:Cardinal;MenuHook:Integer;BodColor:Integer;BulkBook:Cardinal);
var
StringList:TStringList;
Text:String;
begin
  AddToSystemJournal(Msg);
  AddToSystemJournal('Contagem de Bud = ' + IntToStr(CountEx(BodType,BodColor,backpack)));

  
  if BulkBook<>0 then begin   
    AddToSystemJournal('Contagem de Bud = ')
    while (FindTypeEx(BodType,BodColor,backpack,false)>1) do begin 
      AddToSystemJournal('Contagem de Bud = ')
      MoveItem(FindItem,1,BulkBook,0,0,0);
      Wait(WaitTime*2);
      While IsGump do CloseSimpleGump(GetGumpsCount-1);
      StringList:=TStringList.Create;
      StrBreakApart(GetCliloc(BulkBook),'stone|',StringList);
      Text:=StringList.strings[1];
      StrBreakApart(Text,'|',StringList);
      Text:=StringList.strings[0];
      Wait(WaitTime);
      CheckLag(WaitLag);
      AddToDebugJournal(Text);
    end;
  end;
end;

function CheckBackpack:Boolean;
var
StringList:TStringList;
Text:String;
begin
  StringList:=TStringList.Create;
  StrBreakApart(GetCliloc(Backpack),'Contents: ',StringList);
  Text:=StringList.strings[1];
  StrBreakApart(Text,'/',StringList);
  Text:=StringList.strings[0];
  if StrToInt(Text)=125 then begin
    AddToSystemJournal(myProfiles[nProfile]+' Sua mochila está cheia.');
    Result:=True;
  end;
end;

begin
  AddGumpIgnoreByID(GumpIgnoredID);
  if not UseTailor and not UseBS then begin
    AddToSystemJournal('Atenção erro! Pelo menos um dos parâmetros UseTailor ou UseBS deve ser True. O script foi interrompido.')
    Halt;
  end;
  myProfiles:=['mimers', 'mimerss', 'mimersss', 'mimersss', 'mimerssssb', 'mimerssss', 'mimerssssd', 'mimerssssw', 'mimersssswf', 'mimersssswfgg', 'jezzy666tt', 'mestre', 'mimersssswfggfff', 'mimersssswfggfffb', 'mimersssswfggfffbçç', 'novo' ] ; 
  SetLength(timeOrder, Length(myProfiles));
  for nProfile:=0 to (Length(timeOrder)-1) do timeOrder[nProfile]:=0;

  repeat
    for nProfile:=0 to Length(myProfiles)-1 do begin
      if (Now>timeOrder[nProfile]) then begin
        ChangeProfile(myProfiles[nProfile]);
        SetARStatus(True);
        Connect;
        While not Connected() do Wait(2000);
       // if not CheckBackpack then begin
          While IsGump do CloseSimpleGump(GetGumpsCount-1);
          if UseTailor then CollectBoDWithCondition(TMsg,TailorVendor,ContextMenuHookTailor,BoDClrT,TBook);
          if UseBS then CollectBoDWithCondition(BSMsg,BSVendor,ContextMenuHookBS,BoDClrBS,BSBook);
       // end;
        SetARStatus(False);
        While Connected do begin
          Disconnect;
          Wait(5000);                  
        end;
        timeOrder[nProfile]:=Now + 1.0 / 24;    
      end;
    end;
    wait(360000);
  until False;
end.