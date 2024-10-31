

### Tunning
> Algumas tratativas para caixas que estão nerando muito recurso e entrando em conserve mode
```
config system global
set memory-use-threshold-extreme 97
set memory-use-threshold-green 90
set memory-use-threshold-red 94
set miglogd-children 1
set wad-worker-count 1
set scanunit-count 2
set udp-idle-timer 90
set internet-service-database on-demand
end

config system dns
set dns-cache-limit 300
set dns-cache-ttl 300
end
```
> Time de cache para consulta do TTL no fortiguard
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
</br></br>

![image](https://github.com/user-attachments/assets/af521807-b3d9-47d6-bccb-db0492d67a14) </br></br></br></br>

>  Alterar atualização do Internet Service Database para atualizar apenas serviços utilizados em politicas

```
config system global
    set internet-service-database on-demand
end
```
```
diagnose autoupdate versions | grep Internet -A 6
```


