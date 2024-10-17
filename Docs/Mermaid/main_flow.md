graph TD
    A[Start] --> B[Setup Logging]
    B --> C[Initialize MongoDB]
    C --> D[Initialize Redis]
    D --> E[Start Kafka Service]
    E --> F[Create FastAPI App]
    F --> G[Include API Routes]
    G --> H[Define Startup Event]
    H --> I[Define Shutdown Event]
    I --> J[Run Uvicorn Server]
    J --> K[Wait for Requests]
    K --> L{Shutdown?}
    L -->|No| K
    L -->|Yes| M[Stop Kafka Service]
    M --> N[End]
