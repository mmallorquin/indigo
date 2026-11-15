**Fase 2. No etiquetar con `agente` hasta terminar la fase 1.**

**Objetivo:** un agente semanal que prepare los posts y guiones de la semana a partir del catálogo, para que Marco los apruebe.

**Qué hacer (propuesta, a revisar al empezar la fase 2)**
- Script en `agentes/contenido.py` que lea las prendas del catálogo y `marca.toml`, genere por Batch (Sonnet) 7 posts y 3 guiones de video, y pase un juez (Opus) que elija los mejores.
- El workflow programado (lunes) que corre el script lo agrega Marco o Claude en su sesión: `.github/` es zona prohibida para el agente. La API key se lee del Key Vault igual que en `agente.yml`.
- Resultado: una página privada `/aprobar` donde Marco aprueba, edita o descarta cada pieza. Lo aprobado queda listo para copiar a Instagram; nada se publica solo.
- Tope de costo por corrida y registro del gasto.
