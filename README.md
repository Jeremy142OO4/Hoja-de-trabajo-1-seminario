# HT1 - Balanceador de carga

Solución para Seminario de Sistemas 1: dos APIs en lenguajes diferentes, listas para desplegarse en dos instancias EC2 detrás de un Application Load Balancer.

## Estructura

- `api-1`: JavaScript (Node.js), para `Instancia-1`.
- `api-2`: Python, para `Instancia-2`.
- `deploy`: servicios de systemd para mantener cada API activa.

Las dos APIs escuchan en el puerto `3000` y no usan librerías externas.

## Respuestas requeridas

API #1, `GET /`:

```json
{
  "Instancia": "Instancia #1 - API #1",
  "Curso": "Seminario de Sistemas 1",
    "Estudiante": "Jeremy Estuardo Orellana Aldana - 202300644"
}
```

API #2, `GET /`:

```json
{
  "Instancia": "Instancia #2 - API #2",
  "Curso": "Seminario de Sistemas 1",
    "Estudiante": "Jeremy Estuardo Orellana Aldana - 202300644"
}
```

En ambas, `GET /check` responde con HTTP 200 y `{"status":"OK"}`.

## Pruebas locales

En una terminal:

```bash
cd api-1
CARNET=202300644 ESTUDIANTE="Jeremy Estuardo Orellana Aldana" npm start
```

En otra terminal, usando un puerto diferente:

```bash
cd api-2
CARNET=202300644 ESTUDIANTE="Jeremy Estuardo Orellana Aldana" PORT=3001 python3 server.py
```

Pruebas:

```bash
curl -i http://localhost:3000/check
curl http://localhost:3000/
curl -i http://localhost:3001/check
curl http://localhost:3001/
```

## Despliegue en AWS EC2

### 1. Crear las instancias

1. Crear dos instancias Ubuntu Server y nombrarlas exactamente `Instancia-1` e `Instancia-2`.
2. Usarlas en la misma VPC y, preferiblemente, en dos zonas de disponibilidad.
3. Crear un grupo de seguridad para las instancias con:
   - SSH TCP 22 desde tu IP, solo mientras administras las máquinas.
   - TCP 3000 cuyo origen sea el grupo de seguridad del balanceador.
   - Para la demostración directa por IPv4, agregar temporalmente TCP 3000 desde tu IP.

### 2. Copiar el proyecto

Subir esta carpeta a `/home/ubuntu/HT1` mediante SFTP o clonarla desde un repositorio público. En ambas instancias:

```bash
sudo apt update
sudo apt install -y nodejs python3
```

### 3. Instancia-1

El servicio ya contiene el nombre y carné del estudiante. Ejecutar:

```bash
sudo cp /home/ubuntu/HT1/deploy/api-1.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now api-1
sudo systemctl status api-1
curl http://localhost:3000/
curl -i http://localhost:3000/check
```

### 4. Instancia-2

El servicio ya contiene el nombre y carné del estudiante. Ejecutar:

```bash
sudo cp /home/ubuntu/HT1/deploy/api-2.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now api-2
sudo systemctl status api-2
curl http://localhost:3000/
curl -i http://localhost:3000/check
```

## Configuración del Application Load Balancer

1. Crear un grupo de seguridad para el ALB:
   - HTTP TCP 80 desde `0.0.0.0/0`.
   - Salida permitida hacia las instancias.
2. Crear un Target Group de tipo **Instances**:
   - Protocolo HTTP, puerto `3000`.
   - Health check: protocolo HTTP, ruta `/check`.
   - Success codes: `200`.
   - Registrar `Instancia-1` e `Instancia-2` en el puerto 3000.
3. Esperar hasta que ambos destinos aparezcan como **Healthy**.
4. Crear un **Application Load Balancer**, orientado a Internet, en la misma VPC y al menos dos subredes públicas.
5. Nombrarlo `elb-semi1-ht1-202300644`.
6. Crear el listener HTTP puerto 80 y reenviar al Target Group anterior.
7. Abrir el nombre DNS del ALB y actualizar varias veces para observar respuestas de ambas APIs.

## Guion sugerido para el video (máximo 10 minutos)

1. Mostrar las dos instancias, sus nombres e IPv4 públicas.
2. Consumir `http://IP_INSTANCIA_1:3000/` y `http://IP_INSTANCIA_2:3000/`.
3. Mostrar el Target Group con ambos destinos saludables y la ruta `/check`.
4. Consumir el DNS del ALB varias veces hasta mostrar respuestas de ambas instancias.
5. En una instancia ejecutar `sudo systemctl stop api-1` (o `api-2`), esperar a que el destino quede unhealthy y demostrar que la otra API continúa respondiendo.
6. Reiniciar con `sudo systemctl start api-1`, esperar el estado healthy y repetir la prueba del ALB.

Al terminar la demostración, se recomienda eliminar la regla temporal que expone el puerto 3000 desde Internet y detener o eliminar los recursos de AWS para evitar cargos.
