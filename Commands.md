### Cheatsheet for FortiGate Command Line Interface CLI
 > Sites Uteis
```
http://www.ideaio.ch/posts/cheatsheet-fortigate-cli.html
http://kb.fortinet.com/kb/viewContent.do?externalId=11186

´´´

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
### Grep
> Busca com Grep duas palavras "name" e "addr"
```
get vpn ike gateway | grep -f "name\|addr"

```
> Busca com Grep full informações
```
get vpn ike gateway | grep -f
```

### Tunning
> Algumas tratativas para caixas que estão nerando muito recurso e entrando em conserve mode
```
config system global
set memory-use-threshold-extreme 97
set memory-use-threshold-green 90
set memory-use-threshold-red 94
end
 config system global
set miglogd-children 1
set wad-worker-count 1
set scanunit-count 2
set sslvpn-max-worker-count 1
end
 config system dns
set dns-cache-limit 300
end
 ```
> ###########ONDE TEM SSL VPN HABILITADA#######
```
set sslvpn-max-worker-count 1 
```
