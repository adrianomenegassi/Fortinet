

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

> Alterar Update automatico do fortiguard </br>

![image](https://github.com/user-attachments/assets/af521807-b3d9-47d6-bccb-db0492d67a14) </br>

>  Alterar atualização do Internet Service Database para atualizar apenas serviços utilizados em politicas

```
config system global
    set internet-service-database on-demand
end
```
diagnose autoupdate versions | grep Internet -A 6
```

```
