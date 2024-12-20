
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
### Diag
> Listar todos update servicos Fortiguard
```
diagnose autoupdate versions
```
>  Listar update servicos Fortiguard do IPs
```
diagnose autoupdate versions | grep "Attack Definitions" -A 6
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
diagnose debug duration 1 (minute)
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
### FortiSwitch
> Listar informações dos Switchs
```
execute switch-controller get-conn-status
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
### Buscar MAC ou Info relacionadas ao MAC
> Mostrar tabela ARP
```
get system arp
```
> Mostrar tebela de MAC e portas Fortiswitch
```
diagnose switch-controller mac-cache show
```
> Informações relacionadas ao MAC especifico
```
diagnose user-device-store device memory query 2 mac {mac address}
```


