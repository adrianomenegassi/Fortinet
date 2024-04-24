### Event Log
``` 
execute log filter reset
execute log filter free-style "srcip 10.10.10.10"
execute log display
```
```
execute log filter reset
execute log filter field msg "reserse path check fail, drop"
execute log display
```
### Sniffer
> exemplo sniffer com verbose
```
diagnose sniffer packet any 'host 10.10.10.10' 4 10
```
### Debug
> limpar filtros debug
```
diagnose debug disable
diagnose debug flow trace stop
diagnose debug flow filter clear
diagnose debug reset
```
> Alguns exemplos debug
```
diagnose debug flow filter addr 10.10.10.10
diagnose debug flow show function-name enable
diagnose debug flow trace start 100
diagnose debug enable
```
