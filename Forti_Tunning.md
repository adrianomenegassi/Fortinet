

### Tunninghhhh
> Algumas tratativas para caixas que estão onerando muito recurso e entrando em conserve mode
```
config system global
set memory-use-threshold-extreme 97
set memory-use-threshold-green 90
set memory-use-threshold-red 94
set miglogd-children 1
set wad-worker-count 1
set scanunit-count 2
set udp-idle-timer 90
set security-rating-result-submission disable
set security-rating-run-on-schedule disable
end
config system dns
set dns-cache-limit 300
set dns-cache-ttl 300
end
```

> ###########ONDE TEM SSL VPN HABILITADA#######
```
set sslvpn-max-worker-count 1 
```
> Time de cache do webfilter para consulta do TTL no fortiguard
```
config system fortiguard
set webfilter-cache-ttl 500
end
 ```
> Alterar Update automatico do fortiguard </br></br>

```
config system autoupdate schedule
set frequency daily
set time 07:60
end
```
> Alterar o IPS engine para utilização de somente 1 core e desativar aceleração para diminuir o consumo memória
```
config ips global
    set engine-count 1
    set cp-accel-mode none
    set exclude-signatures none
end
```
</br></br>

![image](https://github.com/user-attachments/assets/af521807-b3d9-47d6-bccb-db0492d67a14) </br></br></br></br>




