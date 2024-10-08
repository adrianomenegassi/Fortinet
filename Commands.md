[Link Comandos Uteis](https://github.com/adrianomenegassi/Fortinet/pull/2/commits/61df68f97b8a27feb42d15349ff82254c196b0d6) <br/>
[Mais Comandos GITHUB](https://gist.github.com/cetinajero/1effb04ee9ae9fc6f65faaf43d4bff9b)

### Cheatsheet for FortiGate Command Line Interface CLI
 > Sites Uteis
```
http://www.ideaio.ch/posts/cheatsheet-fortigate-cli.html
```
```
http://kb.fortinet.com/kb/viewContent.do?externalId=11186
```

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
```
diagnose sniffer packet any 'not host 10.10.10.10' 4 10
```
```
diagnose network sniffer port1 'port 53' 6
```
```
diag sniffer packet internal 'udp and port 1812 and host 192.168.0.130 and (192.168.0.1 or 192.168.0.2)' 6 0 l
```
```
diagnose sniffer packet any 'src net 172.1.0.0/24 and dst net 10.10.0.0/24 and ip and not host 172.1.1.255' 6
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
### Chavear Caixa HA
> Verificar integridade e chavear entre as caixas HA
```
get system ha status
```
```
execute ha failover set 1
```
```
execute ha failover unset 1
```
### Quarentena
> Verificar e deletar maquina na quarentena
```
diagnose user quarantine list
```
```
diagnose user quarantine delete src4 10.10.10.10
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

