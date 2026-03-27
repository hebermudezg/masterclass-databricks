# Guia: Activar Databricks Free Trial (14 dias)

## Estrategia de tiempo
- Activar el trial el **14 de abril de 2026** (2 dias antes de la master class)
- La master class es el **16 de abril**
- El trial dura 14 dias = hasta el **28 de abril**
- Tienes tiempo de sobra para preparar y presentar

---

## Opcion 1: Azure Databricks (RECOMENDADA)

### Por que Azure?
- Microsoft da **$200 USD gratis** en creditos Azure para cuentas nuevas
- Databricks trial en Azure incluye creditos DBU adicionales
- La interfaz es la misma que Databricks en cualquier cloud
- Genie, SQL Dashboards y Databricks Apps incluidos

### Paso a paso:

**1. Crear cuenta gratuita de Azure**
- Ve a: https://azure.microsoft.com/free/
- Click en "Start free"
- Usa tu correo (puede ser el de la UNAL o cualquier otro)
- Necesitas tarjeta de credito (NO te cobran, es solo verificacion)
- Recibes $200 USD en creditos gratis

**2. Crear workspace de Databricks en Azure**
- En el portal de Azure (portal.azure.com), busca "Azure Databricks"
- Click en "Create"
- Llena:
  - Resource group: crear uno nuevo, nombre: `masterclass-rg`
  - Workspace name: `masterclass-databricks`
  - Region: `East US` (o la mas cercana)
  - Pricing tier: **Premium** (necesario para Genie y SQL Dashboards)
- Click en "Review + Create" → "Create"
- Espera ~3 minutos

**3. Entrar al workspace**
- Una vez creado, click en "Launch Workspace"
- Se abre la interfaz de Databricks (igual que Community Edition pero con todo habilitado)

**4. Crear SQL Warehouse**
- En la barra izquierda: SQL Warehouses
- Click en "Create SQL Warehouse"
- Nombre: `masterclass-wh`
- Size: **2X-Small** (el mas barato, suficiente para la demo)
- Click en "Create"

**5. Subir datos y notebooks**
- Igual que en Community Edition:
  - Subir los 3 CSV
  - Importar los 4 notebooks .py

---

## Opcion 2: Databricks en AWS

### Paso a paso:
1. Ve a: https://www.databricks.com/try-databricks
2. Selecciona "Start your free trial"
3. Elige AWS como cloud provider
4. Crea una cuenta de AWS si no tienes (tambien tiene capa gratuita)
5. Sigue el wizard de configuracion
6. El trial incluye ~$1000 USD en creditos DBU

---

## Opcion 2b: Databricks en GCP

### Paso a paso:
1. Ve a: https://www.databricks.com/try-databricks
2. Selecciona GCP
3. GCP da $300 USD gratis para cuentas nuevas
4. Mismos pasos que AWS

---

## Que verificar despues de activar el trial

Checklist antes de la master class:

- [ ] Workspace creado y funcionando
- [ ] SQL Warehouse creado y encendido
- [ ] 3 archivos CSV subidos
- [ ] 4 notebooks importados y ejecutados sin error
- [ ] SQL Dashboard creado con al menos 3 graficos
- [ ] Genie configurado con acceso a las tablas
- [ ] Probar compartir el dashboard por URL

---

## Costos estimados durante el trial

| Recurso | Costo/hora | Uso estimado | Total |
|---------|-----------|-------------|-------|
| SQL Warehouse 2X-Small | ~$0.50 | 5 horas (prep + master class) | ~$2.50 |
| Cluster notebook | ~$0.40 | 5 horas | ~$2.00 |
| Storage | despreciable | - | ~$0.01 |
| **Total** | | | **~$5 USD** |

Con $200 de creditos de Azure, te sobra de lejos. No te preocupes por costos.

**IMPORTANTE:** Apagar el SQL Warehouse y el cluster despues de usarlos para no gastar creditos innecesariamente.
