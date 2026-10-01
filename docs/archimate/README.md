# ArchiMate — Learning Analytics Platform

Trois couches (Business / Application / Technology). Diagrammes Mermaid exportables en PNG pour le rapport.

## Business layer

```mermaid
flowchart TB
  Teacher[Enseignant]
  Coordinator[CoordinateurProgramme]
  Learner[Apprenant]
  LAService[ServiceLearningAnalytics]
  Remediaton[ProcessRemediationPedagogique]
  Decision[DecisionDataDriven]

  Teacher --> LAService
  Coordinator --> LAService
  Learner -.-> LAService
  LAService --> Remediaton
  Remediaton --> Decision
```

## Application layer

```mermaid
flowchart LR
  Gen[xapiGenerator]
  LRS[lrsApiApplication]
  API[analyticsApiApplication]
  Dash[stakeholderDashboard]
  Worker[analyticsWorkerApplication]
  Gra[grafanaApplication]

  Gen --> LRS
  LRS --> Worker
  Worker --> API
  API --> Dash
  Worker --> Gra
```

## Technology layer

```mermaid
flowchart TB
  subgraph eva [EVA_PrivateCloud]
    DockerEngine[DockerEngine]
    Compose[DockerCompose]
    PG[(PostgreSQLContainer)]
    Net[BridgeNetwork_la-net]
  end

  DockerEngine --> Compose
  Compose --> PG
  Compose --> Net
  Proxy[UPPA_HTTP_Proxy] -.-> Compose
  VPN[OpenVPNAccess] --> eva
```

## Notes de modélisation
- Business service = offre SaaS analytics
- Application components = microservices du Compose
- Nodes/devices = LXC EVA `m1-siglis-cc-03` + Docker Engine
