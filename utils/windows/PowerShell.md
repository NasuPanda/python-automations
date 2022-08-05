# エイリアスの登録

```powershell
# スクリプト実行が許可されていなければ許可する
if((Get-ExecutionPolicy -Scope LocalMachine) -ne "RemoteSigned"){Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force}
# Profile が無ければ作成
if(-not (Test-Path $PROFILE)){New-Item $PROFILE -Type File -Force}
# メモ帳で Profile を開く
notepad $PROFILE
```

## `touch` 風

```powershell
function touch($filename) { New-Item -type file $filename }
```

## `which` 風

```powershell
function which($cmdname) {
  Get-Command $cmdname | fl
}
```

## `grep` 風

```powershell
Set-Alias grep Select-String
```
